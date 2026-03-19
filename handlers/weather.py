import requests
from handlers.voice import speak
from handlers.listener import takeCommand


def handle(query):
    api_key = "YOUR-API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("tell me which city")
    city_name = takeCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    x = requests.get(complete_url).json()
    if x["cod"] != "404":
        y = x["main"]
        z = x["weather"]
        r = (f"in {city_name} Temperature is {int(y['temp'] - 273.15)} degree celsius "
             f", atmospheric pressure {y['pressure']} hpa unit"
             f", humidity is {y['humidity']} percent and {z[0]['description']}")
        print(r)
        speak(r)
    else:
        speak(" City Not Found ")
