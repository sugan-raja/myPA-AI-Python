import os
from handlers.voice import speak


def handle(query):
    if "logout" in query:
        os.system("shutdown -1")
    elif "restart" in query:
        os.system("shutdown /r /t 1")
    elif "shut down" in query:
        os.system("shutdown /s /t 1")
    elif "play songs" in query:
        speak("Playing...")
        songs_dir = "C:\\Music"
        songs = os.listdir(songs_dir)
        os.startfile(os.path.join(songs_dir, songs[1]))
        return "EXIT"
