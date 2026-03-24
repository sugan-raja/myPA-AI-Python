import wikipedia
import webbrowser as wb
from handlers.voice import speak
from handlers.listener import takeCommand


def handle(query):
    if "search on google" in query or "open website" in query:
        speak("What should i search or open?")
        search = takeCommand().lower()
        wb.open_new_tab(search + '.com')
    else:
        speak("searching...")
        for word in ["wikipedia", "search", "what", "when", "where", "who", "is"]:
            query = query.replace(word, "")
        try:
            result = wikipedia.summary(query, sentences=2)
            print(query)
            print(result)
            speak(result)
        except wikipedia.exceptions.PageError:
            speak("Sorry, I could not find any results for that. Please try a different search.")
        except wikipedia.exceptions.DisambiguationError as e:
            speak("That search has multiple results. Please be more specific. For example: " + str(e.options[0]))
