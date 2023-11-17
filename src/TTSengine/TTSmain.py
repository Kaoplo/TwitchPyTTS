from PySide6.QtCore import Slot, QThread, Signal, QObject
from PySide6.QtWidgets import QMainWindow, QListWidgetItem

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
import asyncio
import json
from src.TTSengine.engine import speak

from src.gui.ui_mainwindow import Ui_MainWindow

with open('config.json', 'r') as f:
    config = json.load(f)

APP_ID = config['AppID']
APP_SECRET = config['AppSecret']
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = config['Channel']


class UpdateListWorker(QObject):
    item_added = Signal(str)

    def print_debug(self, append):
        print("DEBUG: " + str(append))
        self.item_added.emit(str(append))


class TTS(QThread):
    finished = Signal()

    def __init__(self, worker):
        super().__init__()
        self.worker = worker

    async def on_ready(self, ready_event: EventData):
        await ready_event.chat.join_room(TARGET_CHANNEL)
        self.worker.print_debug("ready!")

    async def on_message(self, msg: ChatMessage):
        if msg.text[0] != '!':
            to_say = msg.user.name + ": " + msg.text
            self.worker.print_debug("Saying: " + to_say)
            speak(to_say)
        else:
            self.worker.print_debug("Ignoring command: " + msg.text)

    def run(self):
        async def runTTS():
            self.worker.print_debug("Connecting to channel: " + TARGET_CHANNEL)
            twitch = await Twitch(APP_ID, APP_SECRET)
            auth = UserAuthenticator(twitch, USER_SCOPE)
            token, refresh_token = await auth.authenticate()
            await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

            chat = await Chat(twitch)

            chat.register_event(ChatEvent.READY, self.on_ready)
            chat.register_event(ChatEvent.MESSAGE, self.on_message)

            chat.start()
            self.worker.print_debug("Connected!")

            try:
                input('press ENTER to stop\n')
            finally:
                self.worker.print_debug("stopping...")
                self.finished.emit()
                chat.stop()
                await twitch.close()
                self.worker.print_debug("stopped!")
        asyncio.run(runTTS())


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_tts)

        self.worker = UpdateListWorker()
        self.tts = TTS(self.worker)
        self.worker.item_added.connect(self.update_list_widget)

    @Slot()
    def start_tts(self):
        self.tts.finished.connect(self.thread_finished)
        self.tts.start()

    def update_list_widget(self, text):
        item = QListWidgetItem(text)
        self.ui.listWidget.addItem(item)

    def thread_finished(self):
        self.tts.quit()
        self.tts.wait()
