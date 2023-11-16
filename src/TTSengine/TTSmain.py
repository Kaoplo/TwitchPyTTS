from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow

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



class MainWindow(QMainWindow):

    def print_debug(append):
        print("DEBUG: " + append)

    async def on_ready(self, ready_event: EventData):
        await ready_event.chat.join_room(TARGET_CHANNEL)
        self.print_debug("ready!")

    async def on_message(self, msg: ChatMessage):
        if msg.text[0] != '!':
            to_say = msg.user.name + ": " + msg.text
            self.print_debug("Saying: " + to_say)
            speak(to_say)
        else:
            self.print_debug("Ignoring command: " + msg.text)

    async def run(self):
        self.print_debug("Connecting to channel: " + TARGET_CHANNEL)
        twitch = await Twitch(APP_ID, APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

        chat = await Chat(twitch)

        chat.register_event(ChatEvent.READY, self.on_ready)
        chat.register_event(ChatEvent.MESSAGE, self.on_message)

        chat.start()
        self.print_debug("Connected!")

        try:
            input('press ENTER to stop\n')
        finally:
            self.print_debug("stopping...")
            chat.stop()
            await twitch.close()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.start_tts)

    @Slot()
    async def start_tts(self):
        # asyncio.create_task(self.run())
        self.ui.listWidget.addItem("Connecting")
        self.print_debug("TTS started!")




