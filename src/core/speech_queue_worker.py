"""Owns the "speak chat messages one at a time" pipeline.

This is a QObject meant to be moved to its own QThread (see main_window.py)
so that synthesizing/playing audio never blocks the IRC socket thread (the
old code's `speak()` call ran directly inside the socket-reading thread,
which meant no chat could be received while a message was being read out)
or the GUI thread.

Talks to the rest of the app purely through signals/slots:
  in  - enqueue_message(ChatMessage): a new message to (maybe) speak
  in  - skip_current(): interrupt whatever's currently playing
  in  - clear_queue(): also drop everything still waiting
  out - message_started/message_finished(ChatMessage): drives the "currently
        being read" highlight in the UI
  out - speech_error(str): surfaced in the UI log
"""

from __future__ import annotations

import logging
import queue

from PySide6.QtCore import QObject, Signal, Slot

from src.app_config import AppConfig
from src.core.chat_message import ChatMessage
from src.tts.playback import InterruptiblePlayer
from src.tts.piper_engine import VoiceModelError

logger = logging.getLogger(__name__)


class SpeechQueueWorker(QObject):
    message_started = Signal(ChatMessage)
    message_finished = Signal(ChatMessage)
    speech_error = Signal(str)
    log = Signal(str)

    def __init__(self, engine_factory, config: AppConfig):
        """`engine_factory` is a zero-arg callable that builds a VoiceEngine.
        It's called lazily on the worker thread the first time it's needed,
        so a slow first-time model download doesn't block anything else."""
        super().__init__()
        self._engine_factory = engine_factory
        self._engine = None
        self._config = config
        self._player = InterruptiblePlayer()
        self._queue: "queue.Queue[ChatMessage]" = queue.Queue()
        self._running = False
        logger.debug("SpeechQueueWorker created")

    @Slot()
    def run(self):
        """Connect this to the owning QThread's `started` signal."""
        logger.info("Speech queue worker started")
        self._running = True
        while self._running:
            try:
                message = self._queue.get(timeout=0.25)
            except queue.Empty:
                continue
            logger.debug("Dequeued message id=%s user=%s", message.id, message.username)
            self._speak(message)

    @Slot()
    def stop(self):
        logger.info("Speech queue worker stopping")
        self._running = False
        self._player.interrupt()

    @Slot(ChatMessage)
    def enqueue_message(self, message: ChatMessage):
        logger.debug("Enqueued message id=%s user=%s", message.id, message.username)
        self._queue.put(message)

    @Slot()
    def skip_current(self):
        logger.info("Skipping current message on request")
        self.log.emit("Skipping current message (mod command).")
        self._player.interrupt()

    @Slot()
    def clear_queue(self):
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass

    def _speak(self, message: ChatMessage):
        try:
            logger.debug("Ensuring voice engine for message id=%s", message.id)
            engine = self._get_engine()
        except VoiceModelError as exc:
            logger.exception("Voice engine initialization failed")
            self.speech_error.emit(str(exc))
            return

        text = self._config.format_message(message.text, message.username)
        logger.info("Speaking message id=%s user=%s", message.id, message.username)
        self.message_started.emit(message)
        try:
            samples, sample_rate = engine.synthesize(text)
            self._player.play(samples, sample_rate, volume=self._config.speech_volume)
        except Exception as exc:  # keep the queue alive even if one line fails
            logger.exception("TTS playback failed for message id=%s", message.id)
            self.speech_error.emit(f"TTS error: {exc}")
        finally:
            self.message_finished.emit(message)

    def _get_engine(self):
        if self._engine is None:
            logger.info("Initializing voice engine")
            self._engine = self._engine_factory()
            logger.info("Voice engine initialized")
        return self._engine
