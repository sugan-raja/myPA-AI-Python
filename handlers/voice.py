import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def voice_change(v):
    engine.setProperty('voice', voices[int(v)].id)
    speak("done sir")


def handle(query):
    if "voice" in query:
        speak("for female say female and, for male say male")
        from handlers.listener import takeCommand
        q = takeCommand()
        if "female" in q:
            voice_change(1)
        elif "male" in q:
            voice_change(0)
    elif "female" in query:
        voice_change(1)
    elif "male" in query:
        voice_change(0)
