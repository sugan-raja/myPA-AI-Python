from handlers.listener import wishme, wishme_end, takeCommand
import handlers.datetime_handler as datetime_handler
import handlers.personal as personal
import handlers.search as search
import handlers.email_handler as email_handler
import handlers.system as system
import handlers.reminder as reminder
import handlers.screenshot as screenshot
import handlers.system_info as system_info
import handlers.jokes as jokes
import handlers.weather as weather
import handlers.features as features
import handlers.greeting as greeting
import handlers.voice as voice


def dispatch(query):
    if 'time' in query or 'date' in query:
        datetime_handler.handle(query)
    elif any(w in query for w in ["tell me about yourself", "about you", "who are you", "yourself"]):
        personal.handle(query)
    elif any(w in query for w in ["developer", "father", "who develop you"]):
        personal.handle(query)
    elif any(w in query for w in ['wikipedia', 'what', 'who', 'when', 'where', 'search on google', 'open website']):
        search.handle(query)
    elif "send email" in query:
        email_handler.handle(query)
    elif any(w in query for w in ["logout", "restart", "shut down", "play songs"]):
        system.handle(query)
    elif any(w in query for w in ["create a reminder list", "reminder", "do you know anything", "remember"]):
        reminder.handle(query)
    elif "screenshot" in query:
        screenshot.handle(query)
    elif any(w in query for w in ["cpu and battery", "battery", "cpu"]):
        system_info.handle(query)
    elif any(w in query for w in ["tell me a joke", "joke"]):
        jokes.handle(query)
    elif any(w in query for w in ["weather", "temperature"]):
        weather.handle(query)
    elif any(w in query for w in ["tell me your powers", "help", "features"]):
        features.handle(query)
    elif any(w in query for w in ["hii", "hello", "goodmorning", "goodafternoon", "goodnight", "morning", "noon", "night"]):
        greeting.handle(query)
    elif any(w in query for w in ["voice", "male", "female"]):
        voice.handle(query)
    elif any(w in query for w in ['i am done', 'bye bye jarvis', 'go offline jarvis', 'bye', 'nothing']):
        wishme_end()


if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()
        dispatch(query)
