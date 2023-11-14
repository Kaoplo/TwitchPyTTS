import gtts
from playsound import playsound


def speak(message):
    tts = gtts.gTTS(message)
    tts.save('voice.mp3')
    playsound('voice.mp3')
