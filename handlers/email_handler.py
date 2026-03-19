import smtplib
from handlers.voice import speak
from handlers.listener import takeCommand


def _sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("user-name@xyz.com", "pwd")
    server.sendmail("user-name@xyz.com", to, content)
    server.close()


def handle(query):
    try:
        speak("What is the message for the email")
        content = takeCommand()
        _sendEmail('reciever@xyz.com', content)
        speak("Email has sent")
    except Exception as e:
        print(e)
        speak("Unable to send email check the address of the recipient")
