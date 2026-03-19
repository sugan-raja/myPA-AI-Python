import pyjokes
from handlers.voice import speak


def handle(query):
    j = pyjokes.get_joke()
    print(j)
    speak(j)
