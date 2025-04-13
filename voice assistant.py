import sys
import speech_recognition as sr
import pyttsx3
import smtplib
import webbrowser
import os
import pyautogui
import time
import pywhatkit
from datetime import datetime

listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

WAKE_WORD = "assistant"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        audio = listener.listen(source)
    try:
        command = listener.recognize_google(audio)
        print("Heard:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print(f"Request error from Google Speech Recognition service; {e}")
        return ""

def send_email(to_address, message):
    try:
        your_email = "dibbadasindhuja310@gmail.com"
        your_password = "avga itdo kgom lhke"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(your_email, your_password)
        server.sendmail(your_email, to_address, message)
        server.quit()
        speak("Email has been sent.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't send the email.")

def system_control(command):
    try:
        if 'shutdown' in command:
            speak("Shutting down the system.")
            os.system("shutdown /s /t 60")
        elif 'restart' in command or 'reboot' in command:
            speak("Restarting the system.")
            os.system("shutdown /r /t 60")
        else:
            speak("System command not recognized.")
    except Exception as e:
        print("System control error:", e)
        speak("Sorry, I couldn't perform that action.")

def open_app(command):
    print(f"Received command: {command}")
    command = command.lower().strip()

    try:
        if 'chrome' in command:
            os.system("start chrome")
        elif 'notepad' in command:
            os.system("start notepad")
        elif 'cmd' in command or 'command prompt' in command:
            os.system("start cmd")
        elif 'explorer' in command:
            os.system("start explorer")
        elif 'youtube' in command:
            webbrowser.open("https://www.youtube.com")
        else:
            speak("Application not configured. Please add it.")
    except Exception as e:
        print("Error opening app:", e)
        speak("Something went wrong while trying to open the application.")

def close_app(command):
    command = command.lower().strip()
    print(f"Close Command: {command}")

    try:
        if 'chrome' in command:
            os.system("taskkill /f /im chrome.exe")
        elif 'notepad' in command:
            os.system("taskkill /f /im notepad.exe")
        elif 'cmd' in command or 'command prompt' in command:
            os.system("taskkill /f /im cmd.exe")
        elif 'explorer' in command:
            os.system("taskkill /f /im explorer.exe")
        else:
            speak("Application not configured for closing.")
    except Exception as e:
        print("Error closing app:", e)
        speak("Something went wrong while trying to close the application.")

def handle_command(command):
    command = command.lower().strip()

    if 'open' in command:
        open_app(command)

    elif command == 'hello':
        speak("Hello, what can I do for you?")

    elif 'close' in command:
        close_app(command)

    elif command in ['how are you', 'how are you doing', 'how do you do']:
        speak("I'm great, what help can I do for you?")

    elif 'search' in command:
        search_query = command.replace("search", "")
        speak(f"Searching {search_query}")
        webbrowser.open(f"https://www.google.com/search?q={search_query.strip()}")

    elif 'shutdown' in command or 'restart' in command or 'reboot' in command:
        system_control(command)

    elif 'send email' in command:
        speak("What should I say?")
        message = listen()
        speak("Please say the recipient's email address.")
        to_address = listen().replace(" ", "").replace("address", "@").replace("dot", ".").replace("underscore", "_").strip()
        send_email(to_address, message)

    elif 'screenshot' in command:
        try:
            img = pyautogui.screenshot()
            filename = f"screenshot_{int(time.time())}.png"
            img.save(filename)
            speak(f"Screenshot saved as {filename}")
        except Exception as e:
            print("Screenshot error:", e)
            speak("Sorry, I couldn't take the screenshot.")

    elif 'time' in command:
        now = datetime.now()
        current_time = now.strftime("%I:%M %p").lstrip("0")
        speak(f"The current time is {current_time}")

    elif 'play' in command and 'youtube' in command:
        video = command.replace('play', '').replace('on youtube', '').strip()
        speak(f"Playing {video} on YouTube.")
        pywhatkit.playonyt(video)

    elif 'stop' in command or 'exit' in command:
        speak("Goodbye!")
        sys.exit()

    else:
        speak("Sorry, I didn't understand that.")

# Start assistant
speak("Voice assistant activated. Say the wake word to begin.")

while True:
    command = listen()
    if WAKE_WORD in command:
        speak("Yes, how can I help you?")
        while True:
            new_command = listen()
            if new_command:
                if 'stop' in new_command or 'exit' in new_command or 'quit' in new_command:
                    speak("Goodbye!")
                    sys.exit()
                else:
                    handle_command(new_command)
                    speak("Say something else or say stop to exit.")
