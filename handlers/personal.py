from handlers.voice import speak


def handle(query):
    if "developer" in query or "father" in query or "who develop you" in query:
        with open("about.txt", 'r') as res:
            speak("here is the details: " + res.read())
    else:
        speak("I am Jarvis, version 1.0, I am an AI assistent, I am developed by Praveen on 29 may 2020 in INDIA")
        speak("Now i hope you know me")
