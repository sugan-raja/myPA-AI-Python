from handlers.voice import speak
from handlers.listener import takeCommand


def handle(query):
    if "create a reminder list" in query or "reminder" in query:
        speak("What is the reminder?")
        data = takeCommand()
        speak("You said to remember that" + data)
        with open("data.txt", 'a') as f:
            f.write('\n' + data)
    elif "do you know anything" in query or "remember" in query:
        with open("data.txt", 'r') as f:
            speak("You said me to remember that: " + f.read())
