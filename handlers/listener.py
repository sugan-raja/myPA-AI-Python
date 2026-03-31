#import speech_recognition as sr
import datetime
import json
import os
import pyaudio
from handlers.voice import speak
from vosk import Model, KaldiRecognizer

# 1. LOAD THE MODEL GLOBALLY (Do this at the top of your script!)
print("Loading Vosk Model into memory...")
model_path = "vosk-model-small-en-us-0.15"

if not os.path.exists(model_path):
    print(f"Error: Please download the model and place it at {model_path}")
    exit(1)
    
model = Model(model_path)
print("Model loaded successfully.")
def takeCommand():
    # Initialize the Recognizer
    rec = KaldiRecognizer(model, 16000)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, 
                    channels=1, 
                    rate=16000, 
                    input=True, 
                    frames_per_buffer=8000)
    
    stream.start_stream()
    print("myPA: Listening... (Speak now)")
    
    try:
        # 3. Stream audio in real-time
        while True:
            # Read a small chunk of audio
            data = stream.read(4000, exception_on_overflow=False)
            
            # AcceptWaveform returns True the moment it detects you stopped speaking
            if rec.AcceptWaveform(data):
                # Parse the JSON response
                result = json.loads(rec.Result())
                text = result.get("text", "")
                
                # If it actually heard words, return them
                if text:
                    print(f"You said: {text}")
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
                    return text
                else:
                    # If it just heard a cough or background noise, keep listening
                    print("Listening...")
                    
    except Exception as e:
        print(f"Microphone Error: {e}")
        
    # Cleanup if something goes wrong
    stream.stop_stream()
    stream.close()
    p.terminate()
    return "None"


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


def wishme_end(*args, **kwargs):
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