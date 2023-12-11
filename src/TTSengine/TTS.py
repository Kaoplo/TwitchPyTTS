from PySide6.QtCore import QObject, Signal, QThread

from src.TTSengine.engine import speak
from src.twitch.twitchapi import Twitch

import json


def parse_config_pronunciation(message, username):
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


def get_ignorelist():
    with open('config.json', 'r') as f:
        config = json.load(f)
        ignorelist = config['ignorelist'].split(', ')
        f.close()
    return ignorelist


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
        self.stop_requested = False

        self.pronunciation = ""
        self.TARGET_CHANNEL = ""

    def get_config(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.pronunciation = config['pronunciation']
        self.TARGET_CHANNEL = config['Channel']
        f.close()

    def stop(self):
        self.stop_requested = True

    def on_message(self, message):
        msg = f'{message["username"]}: {message["message"]}'
        self.worker.print_debug(msg)
        if msg[0] != '!':
            if message["username"] not in get_ignorelist():
                speak(parse_config_pronunciation(message["message"], message["username"]))
        else:
            self.worker.print_debug("Ignoring command: " + message)

    def run(self):
        self.stop_requested = False
        self.get_config()
        if self.TARGET_CHANNEL == "":
            self.worker.print_debug("Hit configure, before starting!")
            return
        self.worker.print_debug("Connecting to channel: " + self.TARGET_CHANNEL)
        twitch = Twitch()
        twitch.connect(self.TARGET_CHANNEL)
        twitch.register_event(self.on_message)
        self.worker.print_debug("Connected!")
        self.ready.emit()

        try:
            while not self.stop_requested:
                pass
        finally:
            self.worker.print_debug("stopping...")
            twitch.close()
            self.worker.print_debug("stopped!")
        # async def runTTS():
        #     self.stop_requested = False
        #     self.get_config()
        #     if self.APP_ID == "" or self.APP_SECRET == "" or self.TARGET_CHANNEL == "":
        #         self.worker.print_debug("Hit configure, before starting!")
        #         return
        #     self.worker.print_debug("Connecting to channel: " + self.TARGET_CHANNEL)
        #     twitch = await Twitch(self.APP_ID, self.APP_SECRET)
        #     auth = UserAuthenticator(twitch, self.USER_SCOPE)
        #     token, refresh_token = await auth.authenticate()
        #     await twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)
        #
        #     chat = await Chat(twitch)
        #
        #     chat.register_event(ChatEvent.READY, self.on_ready)
        #     chat.register_event(ChatEvent.MESSAGE, self.on_message)
        #
        #     chat.start()
        #     self.worker.print_debug("Connected!")
        #     self.ready.emit()
        #
        #     try:
        #         while not self.stop_requested:
        #             await asyncio.sleep(1)
        #
        #     finally:
        #         self.worker.print_debug("stopping...")
        #         chat.stop()
        #         await twitch.close()
        #         self.worker.print_debug("stopped!")
        # asyncio.run(runTTS())
