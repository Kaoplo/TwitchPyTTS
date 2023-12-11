import gtts
from playsound import playsound
import os

filepath = 'voice.mp3'


def speak(message):
    tts = gtts.gTTS(message)
    tts.save(filepath)
    playsound(filepath)
    os.remove(filepath)
