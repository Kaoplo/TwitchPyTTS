import pyttsx3
from twitch_chat_irc import twitch_chat_irc


def speak_message(message):
    toSay = message['display-name'] + ": " + message['message']
    print(toSay)
    print(message)
    engine = pyttsx3.init()
    engine.say(toSay)
    engine.runAndWait()



channel = "kaoplo"

connection = twitch_chat_irc.TwitchChatIRC()

messages = connection.listen(channel, on_message=speak_message)


