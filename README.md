## Privacy and Local Inference

All LLM queries are processed locally on your machine via Ollama. No user data or queries are sent to external servers, ensuring privacy and control over your data.

## Model Weights and Data

Model weights (such as Qwen2.5 0.5B) are not included in this repository. You must download them using:

```
ollama pull qwen2.5:0.5b
```

Refer to the [Ollama documentation](https://ollama.com/library/qwen) for more details.
# Ollama + Qwen2.5 0.5B Integration

This project now supports local LLM-powered responses using [Ollama](https://ollama.com/) and the Qwen2.5 0.5B model.

## How to Enable Ollama Integration

1. Install Ollama from https://ollama.com/download
2. Pull the Qwen2.5 0.5B model:
        ```
        ollama pull qwen2.5:0.5b
        ```
3. Make sure Ollama is running (default: http://localhost:11434)
4. Install Python dependencies:
        ```
        pip install -r requirements.txt
        ```
5. Run the assistant as usual. The model will be preloaded at startup for fast responses.

## Usage

- If your query is not handled by a specific handler, you can extend the code to use Ollama as a fallback for open-ended questions or creative tasks.

## Example Ollama Query Function

See `main.py` for the `ollama_query` function and warm-up logic.

---
# Taskmate AI

![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)

A Python 3 voice-controlled virtual assistant.

## Project Structure

```
myPA-AI-Python/
├── main.py                  # Entry point — dispatcher loop
├── handlers/
│   ├── voice.py             # TTS engine, speak(), voice_change()
│   ├── listener.py          # Microphone input, wishme(), wishme_end()
│   ├── datetime_handler.py  # Time and date
│   ├── personal.py          # About Taskmate / developer info
│   ├── search.py            # Wikipedia + Google/website search
│   ├── email_handler.py     # Send email via Gmail SMTP
│   ├── system.py            # Shutdown / restart / logout / music
│   ├── reminder.py          # Create and read reminders
│   ├── screenshot.py        # Take screenshots
│   ├── system_info.py       # CPU and battery usage
│   ├── jokes.py             # Random jokes
│   ├── weather.py           # Weather via OpenWeatherMap API
│   ├── features.py          # List all capabilities
│   └── greeting.py          # Greetings and time-aware responses
├── requirements.txt
└── about.txt                # Developer info (read by personal handler)
```

### Prerequisite for Linux Users: Download Piper Executable

Download and extract the Piper TTS binary (required for voice features):

```
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
tar -xzf piper_amd64.tar.gz
# Move the piper binary to the piper/ directory if needed
cd piper_amd64
mv piper/ ..
cd ..
rm -rf piper_amd64
```

## Installation

1. Clone the repository

        git clone https://github.com/sugan-raja/myPA-AI-Python.git

2. Open the project directory

        cd myPA-AI-Python

3. Install dependencies

        pip install -r requirements.txt

4. Configure the following before running:

   - **Email** — set your Gmail credentials in `handlers/email_handler.py`
   - **Weather** — set your OpenWeatherMap API key in `handlers/weather.py`
   - **Screenshots** — update the save path in `handlers/screenshot.py`
   - **Music** — update the songs directory path in `handlers/system.py`

5. Run

        python main.py

## Requirements

| Package | Version | Purpose |
|---|---|---|
| pyttsx3 | 2.90 | Text-to-speech engine |
| SpeechRecognition | 3.15.1 | Microphone voice input |
| wikipedia | 1.4.0 | Wikipedia search |
| psutil | 5.9.5 | CPU and battery stats |
| PyAutoGUI | 0.9.54 | Screenshots |
| pyjokes | 0.6.0 | Random jokes |
| requests | 2.32.4 | Weather API calls |
| Pillow | 11.3.0 | Image handling for screenshots |
| beautifulsoup4 | 4.14.3 | HTML parsing (wikipedia dep) |
| comtypes | 1.4.16 | Windows COM interface (pyttsx3 dep) |
| PyGetWindow | 0.0.9 | Window management (pyautogui dep) |
| PyScreeze | 1.0.1 | Screen capture (pyautogui dep) |
| pytweening | 1.2.0 | Mouse animation (pyautogui dep) |
| pywin32 | 311 | Windows API (pyttsx3 dep) |
| MouseInfo | 0.1.3 | Mouse info (pyautogui dep) |
| PyMsgBox | 2.0.1 | Message boxes (pyautogui dep) |
| PyRect | 0.2.0 | Rectangle geometry (pyautogui dep) |
| pyperclip | 1.11.0 | Clipboard (pyautogui dep) |

## Commands

### Date & Time
*What is the current time?*  
*What is the current date?*

### About Taskmate
*Who are you?*  
*Tell me about yourself*  
*Tell me about your developer*

### Search
*Check Wikipedia for Marvel*  
*What is the infinity gauntlet?*  
*Who is Iron Man?*  
*Search on google for comic stores near me*  
*Open the website youtube.com*

### Email
*Send email to my boss*

### System
*What is the current CPU and battery?*  
*Logout of my account*  
*Restart my computer*  
*Shut down my computer*

### Music
*Play songs*

### Reminders
*Create a reminder list*  
*Reminder: buy eggs*  
*Do you know anything?*

### Screenshot
*Take a screenshot*

### Jokes
*Tell me a joke*

### Weather
*What is the weather?*  
*Tell me the temperature*

### Voice
*Change voice to female*  
*Change voice to male*

### Exit
*I am done*  
*Bye bye Taskmate*