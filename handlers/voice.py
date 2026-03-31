import os
import platform
import subprocess


def speak(text):
    print(f"myPA: {text}")
    if platform.system().lower() == "linux":
        piper_exe = "./piper/piper"
        model_path = "en_US-amy-low.onnx"
        output_file = "temp_voice.wav"
        command = f'echo "{text}" | {piper_exe} --model {model_path} --output_file {output_file}'
        try:
            subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.system(f"aplay -q {output_file}")
            os.remove(output_file)
        except Exception as e:
            print(f"Piper TTS Error: {e}")
    else:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 190)
            voices = engine.getProperty('voices')
            default_voice_index = 1 if len(voices) > 1 else 0
            engine.setProperty('voice', voices[default_voice_index].id)
            engine.setProperty('volume', 1)
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 Error: {e}")


def voice_change(v):
    try:
        idx = int(v)
    except (TypeError, ValueError):
        idx = 0
    if idx < 0 or idx >= len(voices):
        idx = 0
    engine.setProperty('voice', voices[idx].id)
    speak("done sir")


def handle(query):
    if "voice" in query:
        speak("for female say female and, for male say male")
        from handlers.listener import takeCommand
        q = takeCommand()
        if "female" in q:
            voice_change(1)
        elif "male" in q:
            voice_change(0)
    elif "female" in query:
        voice_change(1)
    elif "male" in query:
        voice_change(0)
