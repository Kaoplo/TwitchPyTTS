from PySide6.QtCore import QObject, Signal, QThread

from src.TTSengine.engine import speak

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage

import json
import asyncio

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
        to_say = msg.user.name + ": " + msg.text
        if msg.text[0] != '!':
            self.worker.print_debug(to_say)
            speak(to_say)
        else:
            self.worker.print_debug("Ignoring command: " + to_say)

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