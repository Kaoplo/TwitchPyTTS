from __future__ import annotations

import logging
import queue
from functools import partial

from PySide6.QtCore import QThread, QTimer, Qt, Signal, Slot
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QListWidgetItem, QMainWindow

from src.app_config import AppConfig
from src.core.chat_message import ChatMessage
from src.core.commands import evaluate_command, CommandOutcome
from src.core.speech_queue_worker import SpeechQueueWorker
from src.gui.config_window import ConfigWindow
from src.gui.ui.ui_mainwindow import Ui_MainWindow
from src.tts.piper_engine import PiperEngine
from src.twitch.irc_client import IrcClient

HIGHLIGHT_BACKGROUND = QBrush(QColor("#3a7bd5"))
HIGHLIGHT_FOREGROUND = QBrush(QColor("#ffffff"))
DEFAULT_BACKGROUND = (
    QBrush()
)  # empty brush -> item falls back to the view's normal background
DEFAULT_FOREGROUND = QBrush()

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    # Emitted from the GUI thread, consumed by the speech worker's thread -
    # Qt automatically delivers these via a queued connection since the
    # sender/receiver live on different threads.
    speech_start_requested = Signal()
    irc_start_requested = Signal(str)
    speak_requested = Signal(ChatMessage)
    skip_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = AppConfig.load()
        logger.info(
            "Loaded config for channel #%s using voice model %s",
            self.config.channel or "<unset>",
            self.config.voice_model,
        )

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startButton.clicked.connect(self.toggle_running)
        self.ui.configButton.clicked.connect(self.open_config_window)

        self._items_by_message_id: dict[str, QListWidgetItem] = {}
        self._currently_highlighted: QListWidgetItem | None = None
        self._running = False
        self.config_window = None
        self._pending_chat_messages: queue.Queue[ChatMessage] = queue.Queue()

        self._chat_timer = QTimer(self)
        self._chat_timer.setInterval(50)
        self._chat_timer.timeout.connect(self._drain_chat_messages)

        self.irc_thread: QThread | None = None
        self.irc_client: IrcClient | None = None
        self.speech_thread: QThread | None = None
        self.speech_worker: SpeechQueueWorker | None = None

    # ---- lifecycle -------------------------------------------------

    @Slot()
    def toggle_running(self):
        if self._running:
            self._stop()
        else:
            self._start()

    def _start(self):
        logger.info("Start requested")
        self.config = AppConfig.load()
        logger.debug(
            "Reloaded config: channel=%r voice_model=%r speech_volume=%s",
            self.config.channel,
            self.config.voice_model,
            self.config.speech_volume,
        )
        if not self.config.channel:
            self._log("Hit configure before starting - no channel set.")
            logger.info("Start aborted because no channel is configured")
            return

        self._items_by_message_id.clear()
        self._currently_highlighted = None
        self.ui.listWidget.clear()

        self.ui.startButton.setEnabled(False)
        self.ui.startButton.setText("starting...")

        self._chat_timer.start()
        logger.debug("Starting speech worker")
        self._start_speech_worker()
        logger.debug("Starting IRC client")
        self._start_irc_client()

        self._running = True
        self.ui.startButton.setEnabled(True)
        self.ui.startButton.setText("stop")
        logger.info("Startup sequence complete")

    def _stop(self):
        logger.info("Stop requested")
        self.ui.startButton.setEnabled(False)
        self.ui.startButton.setText("stopping...")

        if self.irc_client is not None:
            self.irc_client.stop()
        if self.irc_thread is not None:
            self.irc_thread.quit()
            self.irc_thread.wait(3000)

        if self.speech_worker is not None:
            self.speech_worker.stop()
        if self.speech_thread is not None:
            self.speech_thread.quit()
            self.speech_thread.wait(3000)

        self._chat_timer.stop()
        self._drain_chat_messages()

        self._running = False
        self.ui.startButton.setEnabled(True)
        self.ui.startButton.setText("start")
        logger.info("Stopped")

    def _start_speech_worker(self):
        engine_factory = partial(
            PiperEngine,
            voice_name=self.config.voice_model,
            progress=self._log_from_any_thread,
        )
        logger.debug(
            "Creating speech worker for voice model %s", self.config.voice_model
        )
        self.speech_worker = SpeechQueueWorker(engine_factory, self.config)
        self.speech_thread = QThread(self)
        self.speech_worker.moveToThread(self.speech_thread)

        self.speech_start_requested.connect(self.speech_worker.run, Qt.QueuedConnection)
        self.speech_worker.message_started.connect(
            self._on_message_started, Qt.QueuedConnection
        )
        self.speech_worker.message_finished.connect(
            self._on_message_finished, Qt.QueuedConnection
        )
        self.speech_worker.speech_error.connect(self._log, Qt.QueuedConnection)
        self.speech_worker.log.connect(self._log, Qt.QueuedConnection)

        self.speak_requested.connect(self.speech_worker.enqueue_message)
        self.skip_requested.connect(self.speech_worker.skip_current)
        self.speech_thread.finished.connect(self.speech_worker.deleteLater)

        self.speech_thread.start()
        self.speech_start_requested.emit()
        logger.debug("Speech worker thread started")

    def _start_irc_client(self):
        logger.debug("Creating IRC client for channel #%s", self.config.channel)
        self.irc_client = IrcClient()
        self.irc_thread = QThread(self)
        self.irc_client.moveToThread(self.irc_thread)

        self.irc_start_requested.connect(self.irc_client.start, Qt.QueuedConnection)
        self.irc_client.message_received.connect(
            self._queue_chat_message, Qt.QueuedConnection
        )
        self.irc_client.status_changed.connect(self._log, Qt.QueuedConnection)
        self.irc_client.connection_error.connect(
            self._on_connection_error, Qt.QueuedConnection
        )
        self.irc_thread.finished.connect(self.irc_client.deleteLater)

        self.irc_thread.start()
        self.irc_start_requested.emit(self.config.channel)
        logger.debug("IRC thread started")

    def closeEvent(self, event):
        self._stop()
        super().closeEvent(event)

    # ---- config window ----------------------------------------------

    @Slot()
    def open_config_window(self):
        if not self.config_window or not self.config_window.isVisible():
            self.config_window = ConfigWindow(self)
            self.config_window.show()

    # ---- chat message handling ---------------------------------------

    @Slot(ChatMessage)
    def _queue_chat_message(self, message: ChatMessage):
        logger.debug("Queued chat message id=%s user=%s", message.id, message.username)
        self._pending_chat_messages.put(message)

    @Slot()
    def _drain_chat_messages(self):
        while True:
            try:
                message = self._pending_chat_messages.get_nowait()
            except queue.Empty:
                return
            self._process_chat_message(message)

    def _process_chat_message(self, message: ChatMessage):
        logger.debug(
            "Processing chat message id=%s user=%s", message.id, message.username
        )
        item = QListWidgetItem(message.display())
        self._items_by_message_id[message.id] = item
        self.ui.listWidget.addItem(item)
        self.ui.listWidget.scrollToBottom()

        outcome = evaluate_command(message, self.config)
        if outcome is CommandOutcome.SKIP_REQUESTED:
            self._log(f"{message.username} used the skip command.")
            logger.info("Skip requested by %s", message.username)
            if self.speech_worker is not None:
                self.speech_worker.skip_current()
        elif outcome is CommandOutcome.SKIP_DENIED:
            self._log(f"{message.username} tried to skip but isn't a mod.")
            logger.info("Skip denied for %s", message.username)
        elif outcome is CommandOutcome.UNKNOWN_COMMAND:
            pass  # commands are never spoken, nothing else to do
        elif self.config.is_ignored(message.username):
            pass
        else:
            if self.speech_worker is not None:
                self.speech_worker.enqueue_message(message)

    # ---- highlighting the message currently being read ----------------

    @Slot(ChatMessage)
    def _on_message_started(self, message: ChatMessage):
        self._set_highlight(self._items_by_message_id.get(message.id))

    @Slot(ChatMessage)
    def _on_message_finished(self, message: ChatMessage):
        item = self._items_by_message_id.get(message.id)
        if item is not None and item is self._currently_highlighted:
            self._set_highlight(None)

    def _set_highlight(self, item: QListWidgetItem | None):
        if self._currently_highlighted is not None:
            self._currently_highlighted.setBackground(DEFAULT_BACKGROUND)
            self._currently_highlighted.setForeground(DEFAULT_FOREGROUND)
        if item is not None:
            item.setBackground(HIGHLIGHT_BACKGROUND)
            item.setForeground(HIGHLIGHT_FOREGROUND)
            self.ui.listWidget.scrollToItem(item)
        self._currently_highlighted = item

    # ---- logging -------------------------------------------------------

    @Slot(str)
    def _log(self, text: str):
        logger.info(text)
        self.ui.listWidget.addItem(QListWidgetItem(f"[system] {text}"))
        self.ui.listWidget.scrollToBottom()

    @Slot(str)
    def _on_connection_error(self, err: str):
        self._log(f"Error: {err}")

    def _log_from_any_thread(self, text: str):
        # Called by PiperEngine's progress callback, which may run on the
        # speech worker's thread - go through the worker's `log` signal
        # instead of touching the QListWidget directly from another thread.
        logger.debug("Worker progress: %s", text)
        if self.speech_worker is not None:
            self.speech_worker.log.emit(text)
        else:
            logger.info(text)
