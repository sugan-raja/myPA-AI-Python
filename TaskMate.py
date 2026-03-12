import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import platform
import pyjokes
import requests
import json

engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('volume', 1)


# Change voice
def voice_change(v):
    x = int(v)
    if x < len(voices):
        engine.setProperty('voice', voices[x].id)
        speak("done sir")
    else:
        speak("voice not available")


# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Time function
def time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(current_time)


# Date function
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)


def checktime(tt):
    hour = datetime.datetime.now().hour
    if "morning" in tt:
        if 6 <= hour < 12:
            speak("Good morning sir")
        elif 12 <= hour < 18:
            speak("it's Good afternoon sir")
        elif 18 <= hour < 24:
            speak("it's Good Evening sir")
        else:
            speak("it's Goodnight sir")
    elif "afternoon" in tt:
        if 12 <= hour < 18:
            speak("it's Good afternoon sir")
        elif 6 <= hour < 12:
            speak("Good morning sir")
        elif 18 <= hour < 24:
            speak("it's Good Evening sir")
        else:
            speak("it's Goodnight sir")
    else:
        speak("it's night sir!")


# Welcome function
def wishme():
    speak("Welcome Back")
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir")
    elif 18 <= hour < 24:
        speak("Good Evening sir")
    else:
        speak("Goodnight sir")

    speak("TaskMate at your service, Please tell me how can i help you?")


def wishme_end():
    speak("signing off")
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good afternoon")
    elif 18 <= hour < 24:
        speak("Good Evening")
    else:
        speak("Goodnight.. Sweet dreams")
    quit()


# Command by user function
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 0.5
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
    except Exception as e:
        print(e)
        speak("Say that again please...")
        return "None"

    return query


# Weather condition
def weather():
    api_key = "YOUR-API_KEY"  # Generate your own API key from openweathermap.org
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("tell me which city")
    city_name = take_command()
    
    if city_name == "None":
        return
    
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    try:
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != "404":
            main_data = data["main"]
            current_temperature = main_data["temp"]
            current_pressure = main_data["pressure"]
            current_humidity = main_data["humidity"]
            weather_data = data["weather"]
            weather_description = weather_data[0]["description"]
            
            result = (f"in {city_name} Temperature is "
                     f"{int(current_temperature - 273.15)} degree celsius, "
                     f"atmospheric pressure {current_pressure} hpa unit, "
                     f"humidity is {current_humidity} percent "
                     f"and {weather_description}")
            print(result)
            speak(result)
        else:
            speak("City Not Found")
    except Exception as e:
        print(f"Error fetching weather: {e}")
        speak("Unable to fetch weather information")


def personal():
    speak("I am TaskMate, an AI assistant, "
          "I am a cross-platform virtual assistant")
    speak("Now i hope you know me")


def jokes():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)


if __name__ == "__main__":
    wishme()
    while True:
        query = take_command().lower()

        # Time
        if 'time' in query:
            time()

        # Date
        elif 'date' in query:
            date()

        # Personal info
        elif any(phrase in query for phrase in ["tell me about yourself", "about you", "who are you", "yourself"]):
            personal()

        # Wikipedia search
        elif any(keyword in query for keyword in ['wikipedia', 'what', 'who', 'when', 'where']):
            speak("searching...")
            search_query = query
            for word in ["wikipedia", "search", "what", "when", "where", "who", "is"]:
                search_query = search_query.replace(word, "")
            
            try:
                result = wikipedia.summary(search_query, sentences=2)
                print(search_query)
                print(result)
                speak(result)
            except Exception as e:
                print(f"Error searching Wikipedia: {e}")
                speak("Unable to find information on Wikipedia")

        # Open website
        elif "open website" in query or "search on google" in query:
            speak("What should i search or open?")
            search = take_command().lower()
            if search != "None":
                wb.open_new_tab("https://" + search + ".com")

        # Jokes
        elif "tell me a joke" in query or "joke" in query:
            jokes()

        # Weather
        elif "weather" in query or "temperature" in query:
            weather()

        # Features
        elif any(phrase in query for phrase in ["tell me your powers", "help", "features"]):
            features = """I can help you with many things like:
            - Tell you the current time and date
            - Tell you the current weather
            - Create reminders
            - Send emails
            - Tell you jokes
            - Open any website
            - Search Wikipedia for information
            - Change my voice from male to female and vice-versa
            Tell me what can I do for you?"""
            print(features)
            speak(features)

        # Greetings
        elif any(greeting in query for greeting in ["hi", "hello", "goodmorning", "goodafternoon", "goodnight", "morning", "noon", "night"]):
            query = query.replace("jarvis", "").replace("hi", "").replace("hello", "")
            if any(time_phrase in query for time_phrase in ["morning", "night", "goodnight", "afternoon", "noon"]):
                checktime(query)
            else:
                speak("what can i do for you")

        # Changing voice
        elif "voice" in query:
            speak("for female say female and, for male say male")
            voice_choice = take_command().lower()
            if "female" in voice_choice:
                voice_change(1)
            elif "male" in voice_choice:
                voice_change(0)

        # Exit function
        elif any(exit_phrase in query for exit_phrase in ['i am done', 'bye bye taskmate', 'go offline taskmate', 'bye', 'nothing']):
            wishme_end()
