import smtplib
import os
from handlers.voice import speak
from handlers.listener import takeCommand


def _sendEmail(to, content):
    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    if not email_user or not email_password:
        raise RuntimeError("Email credentials are not configured. Please set EMAIL_USER and EMAIL_PASSWORD environment variables.")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email_user, email_password)
    server.sendmail(email_user, to, content)
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
