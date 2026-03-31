
"""
myPA-AI-Python: Main Entry Point

This script starts your personal assistant, handles user queries, and integrates with Ollama for LLM-powered responses.
"""

# =========================
# Imports
# =========================
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


import logging
import requests
# =========================
# Logging Setup
# =========================
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)

# =========================
# Ollama Integration
# =========================
def ollama_query(prompt, model="qwen2.5:0.5b"):
    """
    Send a prompt to Ollama and return the response.
    Args:
        prompt (str): The user input or question.
        model (str): The Ollama model to use (default: qwen:0.5b).
    Returns:
        str: The response from the Ollama model, or an error message.
    """
    url = "http://localhost:11434/api/generate"
    # Add instruction for brevity
    concise_prompt = f"{prompt}\n\nPlease answer in 50 words or less."
    payload = {
        "model": model,
        "prompt": concise_prompt,
        "num_predict": 100  # ~50 words, adjust as needed
    }
    logging.debug(f"Sending prompt to Ollama: {prompt}")
    try:
        response = requests.post(url, json=payload, timeout=30, stream=True)
        if response.ok:
            result = ""
            import json
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'response' in data:
                            result += data['response']
                    except Exception as e:
                        logging.error(f"Ollama JSON parse error: {e}")
            logging.debug(f"Ollama response: {result}")
            return result
        else:
            logging.error(f"Ollama error: {response.status_code}")
            return f"[Ollama error: {response.status_code}]"
    except Exception as e:
        logging.error(f"Ollama exception: {e}")
        return f"[Ollama exception: {e}]"

# =========================
# Query Dispatching
# =========================
def dispatch(query):
    """
    Routes the user's query to the appropriate handler.
    Uses a list of (condition, handler) pairs for clarity and maintainability.
    """
    logging.info(f"Recognized speech/text: {query}")
    conditions = [
        (lambda q: 'time' in q or 'date' in q, datetime_handler.handle),
        (lambda q: any(w in q for w in ["tell me about yourself", "about you", "who are you", "yourself"]), personal.handle),
        (lambda q: any(w in q for w in ["developer", "father", "who develop you"]), personal.handle),
        (lambda q: any(w in q for w in ["cpu and battery", "battery", "cpu"]), system_info.handle),
        (lambda q: any(w in q for w in ["weather", "temperature"]), weather.handle),
        (lambda q: any(w in q for w in ['wikipedia', 'search on google', 'open website']), search.handle),
        (lambda q: "send email" in q, email_handler.handle),
        (lambda q: any(w in q for w in ["logout", "restart", "shut down", "play songs"]), system.handle),
        (lambda q: any(w in q for w in ["create a reminder list", "reminder", "do you know anything", "remember"]), reminder.handle),
        (lambda q: "screenshot" in q, screenshot.handle),
        (lambda q: any(w in q for w in ["tell me a joke", "joke"]), jokes.handle),
        (lambda q: any(w in q for w in ["tell me your powers", "help", "features"]), features.handle),
        (lambda q: any(w in q for w in ["hii", "hello", "goodmorning", "goodafternoon", "goodnight", "morning", "noon", "night"]), greeting.handle),
        (lambda q: any(w in q for w in ["voice", "male", "female"]), voice.handle),
        (lambda q: any(w in q for w in ['i am done', 'bye bye myPA', 'go offline myPA', 'bye', 'nothing']), wishme_end),
    ]
    for condition, handler in conditions:
        if condition(query):
            handler_name = getattr(handler, "__name__", repr(handler))
            handler_module = getattr(handler, "__module__", "<unknown>")
            logging.info(f"Dispatching to handler: {handler_module}.{handler_name}")
            handler(query)
            return
    # Fallback: Use Ollama for unmatched queries
    logging.info("No handler matched. Using Ollama fallback.")
    response = ollama_query(query)
    # Fallback truncation if model exceeds word limit
    words = response.split()
    if len(words) > 50:
        response = ' '.join(words[:50]) + '...'
    print("Ollama:", response)
    # Voice over the Ollama response
    try:
        from handlers.listener import speak
        speak(response)
    except Exception as e:
        logging.error(f"Failed to voice Ollama response: {e}")

# =========================
# Main Program Loop
# =========================
if __name__ == "__main__":
    wishme()
    # --- Preload Ollama model (warm-up) ---
    # This sends a dummy query to load the model into memory for faster responses.
    logging.info("Warming up Ollama model...")
    _ = ollama_query("Hello", model="qwen2.5:0.5b")
    logging.info("Ollama model ready.")
    while True:
        logging.info("Listening for user input...")
        query = takeCommand().lower()
        dispatch(query)
