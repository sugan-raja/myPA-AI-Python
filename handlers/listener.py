import speech_recognition as sr
import datetime
from handlers.voice import speak


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"
    return query


def _greet_by_hour(hour):
    if hour >= 6 and hour < 12:
        speak("Good Morning sir!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon sir")
    elif hour >= 18 and hour < 24:
        speak("Good Evening sir")
    else:
        speak("Goodnight sir")


def wishme():
    speak("Welcome Back")
    _greet_by_hour(datetime.datetime.now().hour)
    speak("myPA at your service, Please tell me how can I help you?")


def wishme_end():
    speak("signing off")
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon")
    elif hour >= 18 and hour < 24:
        speak("Good Evening")
    else:
        speak("Goodnight.. Sweet dreams")
    quit()
