import datetime
from handlers.voice import speak


def handle(query):
    if 'time' in query:
        speak("The current time is")
        speak(datetime.datetime.now().strftime("%H:%M:%S"))
    elif 'date' in query:
        now = datetime.datetime.now()
        speak("The current date is")
        speak(str(now.day))
        speak(str(now.month))
        speak(str(now.year))
