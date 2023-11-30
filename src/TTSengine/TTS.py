from PySide6.QtCore import QObject, Signal, QThread

from src.TTSengine.engine import speak

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage

import json
import asyncio


def parse_config(message, username):
    with open('config.json', 'r') as f:
        config = json.load(f)
        pronunciation = config['pronunciation']
        f.close()
    out = pronunciation
    if '{username}' in pronunciation:
        out = out.replace('{username}', username)
    if '{message}' in pronunciation:
        out = out.replace('{message}', message)
    return out


class UpdateListWorker(QObject):
    item_added = Signal(str)

    def print_debug(self, append):
        print("DEBUG: " + str(append))
        self.item_added.emit(str(append))


class TTS(QThread):
    stop_request = Signal()
    ready = Signal()

    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.stop_request.connect(self.stop)

    def get_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.APP_ID = config['AppID']
        self.APP_SECRET = config['AppSecret']
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.TARGET_CHANNEL = config['Channel']
        self.pronunciation = config['pronunciation']
        f.close()

    def stop(self):
        self.stop_requested = True

    async def on_ready(self, ready_event: EventData):
        await ready_event.chat.join_room(self.TARGET_CHANNEL)
        self.worker.print_debug("ready!")

    async def on_message(self, msg: ChatMessage):
        message = f'{msg.user.name}: {msg.text}'
        if msg.text[0] != '!':
            self.worker.print_debug(message)
            speak(parse_config(msg.text, msg.user.name))
        else:
            self.worker.print_debug("Ignoring command: " + message)

    def run(self):
        async def runTTS():
            self.stop_requested = False
            self.get_config()
            if self.APP_ID == "" or self.APP_SECRET == "" or self.TARGET_CHANNEL == "":
                self.worker.print_debug("Hit configure, before starting!")
                return
            self.worker.print_debug("Connecting to channel: " + self.TARGET_CHANNEL)
            twitch = await Twitch(self.APP_ID, self.APP_SECRET)
            auth = UserAuthenticator(twitch, self.USER_SCOPE)
            token, refresh_token = await auth.authenticate()
            await twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)

            chat = await Chat(twitch)

            chat.register_event(ChatEvent.READY, self.on_ready)
            chat.register_event(ChatEvent.MESSAGE, self.on_message)

            chat.start()
            self.worker.print_debug("Connected!")
            self.ready.emit()

            try:
                while not self.stop_requested:
                    await asyncio.sleep(1)

            finally:
                self.worker.print_debug("stopping...")
                chat.stop()
                await twitch.close()
                self.worker.print_debug("stopped!")
        asyncio.run(runTTS())
