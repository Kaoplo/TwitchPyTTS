import gtts
from playsound import playsound
import os


def speak(message):
    tts = gtts.gTTS(message)
    tts.save('voice.mp3')
    playsound('voice.mp3')
    os.remove('voice.mp3')
