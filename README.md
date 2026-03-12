# Jarvis AI - Cross-Platform Virtual Assistant

![Python](https://img.shields.io/badge/python-3670A0?style=plastic&logo=python&logoColor=ffdd54)

# Description

A lightweight, cross-platform virtual assistant built in Python. Works on Windows, macOS, and Linux.

Say "Help" or "Tell me your features" and Jarvis will list all its capabilities.

# Installation

1. Clone the Repository

        git clone https://github.com/sugan-raja/myPA-AI-Python.git

2. Open the Project Directory

        cd myPA-AI-Python

3. Install the Required Python Modules

        pip install -r requirements.txt

4. Run the Script

        python jarvis.py

# How To Use

Once Jarvis is in its listening state, you can speak commands naturally.

## Features

- Tell you the current time and date
- Tell you the current weather (requires OpenWeatherMap API key)
- Tell you jokes
- Open any website
- Search Wikipedia for information
- Change voice from male to female and vice-versa
- Create reminders (saved to file)

## Commands

### Date & Time

*What is the current time?*  
*What is the current date?*

### About Jarvis

*Who are you?*  
*Tell me about yourself*

### Search Capabilities

*Check Wikipedia for Marvel*  
*What is the infinity gauntlet?*  
*Who is Iron Man?*  
*Search on google for [topic]*  
*Open the website [website.com]*

### Weather

*What is the weather?*  
*Tell me the temperature*

### Jokes

*Tell me a joke*

### Voice

*Change voice to male voice*  
*Change voice to female voice*

### Shutdown Jarvis

*I am done*  
*Bye bye Jarvis*

# Platform Support

- Windows ✓
- macOS ✓
- Linux ✓

# Requirements

- Python 3.7+
- Microphone for voice input
- Internet connection for weather and Wikipedia features

# Configuration

To use weather features, get a free API key from [OpenWeatherMap](https://openweathermap.org/api) and replace `YOUR-API_KEY` in the code.

# Removed Features (Windows-Only)

The following Windows-specific features have been removed for cross-platform compatibility:

- Screenshots
- System shutdown/restart/logout
- Music playback
- CPU and battery monitoring
- Email sending

# License

See LICENSE file for details.
