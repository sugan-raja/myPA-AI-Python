import pyautogui
from handlers.voice import speak


def handle(query):
    img = pyautogui.screenshot()
    img.save("C:\\Users\\Jarvis-AI-using-python3-\\screenshots\\ss.png")
    speak("Done!")
