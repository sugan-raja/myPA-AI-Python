import datetime
from handlers.voice import speak


def _checktime(tt):
    hour = datetime.datetime.now().hour
    if "morning" in tt:
        speak("Good morning sir" if 6 <= hour < 12 else
              "it's Good afternoon sir" if 12 <= hour < 18 else
              "it's Good Evening sir" if 18 <= hour < 24 else "it's Goodnight sir")
    elif "afternoon" in tt:
        speak("it's Good afternoon sir" if 12 <= hour < 18 else
              "Good morning sir" if 6 <= hour < 12 else
              "it's Good Evening sir" if 18 <= hour < 24 else "it's Goodnight sir")
    else:
        speak("it's night sir!")


def handle(query):
    for word in ["mypa", "hi", "hello"]:
        query = query.replace(word, "")
    if any(w in query for w in ["morning", "night", "goodnight", "afternoon", "noon"]):
        _checktime(query)
    else:
        speak("what can i do for you")
