from handlers.voice import speak

FEATURES = """i can help to do lot many things like..
    i can tell you the current time and date,
    i can tell you the current weather,
    i can tell you battery and cpu usage,
    i can create the reminder list,
    i can take screenshots,
    i can send email to your boss or family or your friend,
    i can shut down or logout or hibernate your system,
    i can tell you non funny jokes,
    i can open any website,
    i can search the thing on wikipedia,
    i can change my voice from male to female and vice-versa
    And yes one more thing, My boss is working on this system to add more features...,
    tell me what can i do for you??
    """


def handle(query):
    print(FEATURES)
    speak(FEATURES)
