import pyautogui
from handlers.voice import speak
import os


def handle(query):
    img = pyautogui.screenshot()

    # Determine screenshot directory: configurable via SCREENSHOT_DIR,
    # defaulting to a "screenshots" folder in the user's home directory.
    screenshot_dir = os.environ.get(
        "SCREENSHOT_DIR",
        os.path.join(os.path.expanduser("~"), "screenshots"),
    )

    # Ensure the directory exists before saving.
    os.makedirs(screenshot_dir, exist_ok=True)

    screenshot_path = os.path.join(screenshot_dir, "ss.png")
    img.save(screenshot_path)

    speak("Done!")
