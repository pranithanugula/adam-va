import speech_recognition as sr
import pyttsx3
import datetime as dt
import pywhatkit as pw
import os

listener = sr.Recognizer()
speaker = pyttsx3.init()
speaker.setProperty('rate', 150)

def speak(text):
    speaker.say(text)
    speaker.runAndWait()

def take_note():
    speak("What would you like to note down?")
    note = take_com()
    with open("notes.txt", "a") as file:
        file.write(note + "\n")
    speak("Note saved.")

va = "adam"
speak("Hey, how can I help you")

def take_com():
    try:
        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = listener.listen(source, timeout=5, phrase_time_limit=5)
            command = listener.recognize_google(audio)
            command = command.lower()
            if va in command:
                command = command.replace(va, '').strip()
            return command
    except sr.WaitTimeoutError:
        print("Timeout: No response")
        speak("I didn't hear you. Please repeat.")
        return ""
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("I'm having trouble connecting to the service.")
        return ""

while True:
    command = take_com()

    if not command:
        continue
    
    if "time" in command:
        time_now = dt.datetime.now().strftime("%I:%M %p")
        print(time_now)
        speak(time_now)

    elif "date" in command:
        date_now = dt.datetime.now().strftime("%A, %d %B %Y")
        print(date_now)
        speak(date_now)

    elif any(phrase in command for phrase in ['play', 'youtube', 'you tube']):
        for phrase in ['play', 'youtube', 'you tube']:
            if phrase in command:
                query = command.replace(phrase, '').strip()
        print(query)
        speak(f"Opening YouTube to play {query}")
        pw.playonyt(query)
        break

    elif any(phrase in command for phrase in ['search', 'search for', 'google', 'find']):
        if 'search' in command:
            searching = command.replace('search', '').strip()
        elif 'search for' in command:
            searching = command.replace('search for', '').strip()
        elif 'google' in command:
            searching = command.replace('google', '').strip()
        elif 'find' in command:
            searching = command.replace('find', '').strip()                
        print(searching)
        speak(f"searching for {searching}")
        pw.search(searching)
        break

    elif any(phrase in command for phrase in ['wikipedia', 'wiki pedia', 'wiki']):
        for phrase in ['wikipedia', 'wiki pedia', 'wiki']:
            if phrase in command:
                query = command.replace(phrase, '').strip()
        pw.info(query, lines = 5)

    elif 'open notepad' in command or 'notepad':
        os.system('notepad')
        speak("Opening Notepad")

    elif 'open calculator' in command or 'calculator' in command:
        os.system('calc')
        speak("Opening Calculator")
    
    elif 'note' in command or 'take a note' in command:
        take_note()

    elif any(phrase in command for phrase in ['shutdown', 'shut down']):
        print("Are you sure you want to shutdown? Please say yes or no.")
        speak("Are you sure you want to shutdown? Please say yes or no.")
        confirmation = take_com()
        if any(phrase in confirmation for phrase in ['yes', 'y']):
            speak("Shutting down")
            os.system("shutdown /s /t 0")
        else:
            speak("Shutdown aborted")

    elif any(phrase in command for phrase in ['stop', 'exit', 'close', 'terminate']):
        print("Okay, terminating.")
        speak("Okay, terminating.")
        break

    else:
        print(command)
        pw.search(command)
        break
