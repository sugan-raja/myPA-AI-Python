import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
default_voice_index = 1 if len(voices) > 1 else 0
engine.setProperty('voice', voices[default_voice_index].id)
engine.setProperty('volume', 1)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def voice_change(v):
    try:
        idx = int(v)
    except (TypeError, ValueError):
        idx = 0
    if idx < 0 or idx >= len(voices):
        idx = 0
    engine.setProperty('voice', voices[idx].id)
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
