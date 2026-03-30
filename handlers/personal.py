from handlers.voice import speak


def handle(query):
    if "developer" in query or "father" in query or "who develop you" in query:
        with open("about.txt", 'r') as res:
            speak("here is the details: " + res.read())
    else:
        speak("I am myPA, your AI assistant. I am here to help you with your tasks and questions.")
        speak("Now i hope you know me")
