import pyttsx3
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage
import asyncio
import json

with open('config.json', 'r') as f:
    config = json.load(f)

APP_ID = config['AppID']
APP_SECRET = config['AppSecret']
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
TARGET_CHANNEL = config['Channel']


def speak_message(message):
    print("saying: " + message)
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()


async def on_ready(ready_event: EventData):
    await ready_event.chat.join_room(TARGET_CHANNEL)
    print("ready!")


async def on_message(msg: ChatMessage):
    if msg.text[0] != '!':
        to_say = msg.user.name + ": " + msg.text
        speak_message(to_say)


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)

    chat.start()

    try:
        input('press ENTER to stop\\n')
    finally:
        chat.stop()
        await twitch.close()


asyncio.run(run())
