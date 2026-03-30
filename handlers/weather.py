import requests
from handlers.voice import speak
from handlers.listener import takeCommand

# WMO Weather interpretation codes mapped to conversational phrases
weather_descriptions = {
    0: "clear skies",
    1: "mainly clear skies",
    2: "partly cloudy skies",
    3: "overcast skies",
    45: "foggy conditions",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow fall",
    73: "moderate snow fall",
    75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorms",
    96: "thunderstorms with slight hail",
    99: "thunderstorms with heavy hail"
}

def handle(query):
    speak("tell me which city")
    city_name = takeCommand()
    if city_name: 
        # Step 1: Geocoding (City Name -> Coordinates)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1&language=en&format=json"
        
        try:
            geo_data = requests.get(geo_url).json()
            
            if "results" in geo_data and len(geo_data["results"]) > 0:
                lat = geo_data["results"][0]["latitude"]
                lon = geo_data["results"][0]["longitude"]
                resolved_city = geo_data["results"][0]["name"] 
                
                # Step 2: Fetch the weather using coordinates
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_data = requests.get(weather_url).json()
                
                # Extract temperature and the WMO weather code
                current_temp = weather_data["current_weather"]["temperature"]
                weather_code = weather_data["current_weather"]["weathercode"]
                
                # Translate the code to a string, defaulting to "unknown conditions" if the code isn't in the dictionary
                condition = weather_descriptions.get(weather_code, "unknown conditions")
                
                # Format the final string for the voice assistant
                r = f"In {resolved_city}, it is currently {int(current_temp)} degrees Celsius with {condition}."
                print(r)
                speak(r)
                
            else:
                error_msg = f"I couldn't find the weather for {city_name}."
                print(error_msg)
                speak(error_msg)
                
        except Exception as e:
            error_msg = "Sorry, I am having trouble connecting to the weather service right now."
            print(error_msg)
            speak(error_msg)
