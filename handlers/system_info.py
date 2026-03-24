import psutil
from handlers.voice import speak


def handle(query):
    usage = str(psutil.cpu_percent())
    speak('CPU usage is at ' + usage)
    print('CPU usage is at ' + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(str(battery.percent))
    print("battery is at:" + str(battery.percent))
