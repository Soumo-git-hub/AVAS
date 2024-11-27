import os
import winsound
import pyttsx3
import speech_recognition as sr
import eel
import requests
import datetime
import random
import wolframalpha
import datefinder
from datetime import datetime, time
from engine.config import ASSISTANT_NAME
from engine.helper import close_program
from playsound import playsound

# Initialize WolframAlpha client
try:
    app = wolframalpha.Client("EEQ3YE-EP5UQKUAQQ")
except Exception as e:
    print("Error initializing WolframAlpha client:", e)

# OpenWeatherMap API details
API_KEY = '4ad432a816fb1ab0e83d962d52909803'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# Flag to check if greeting has been given
greeted = False

def speak(text):
    """Function to speak text and display it."""
    try:
        print(f"Speaking: {text}")
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 140)
        eel.DisplayMessage(text)
        eel.receiverText(text)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")

def wish():
    """Function to greet the user based on the current time."""
    current_time = datetime.now().strftime("%I:%M %p")  # Use datetime to get the current time
    hour = datetime.now().hour

    if 0 <= hour < 12:
        speak(f"Good morning sir, it's {current_time}")
    elif 12 <= hour < 18:
        speak(f"Good afternoon sir, it's {current_time}")
    else:
        speak(f"Good evening sir, it's {current_time}")

    speak("How may I help you?")


from playsound import playsound

def set_alarm():
    """Function to set an alarm at a specified time."""
    try:
        speak("Please tell me the time to set the alarm in 'HH:MM AM/PM' format.")
        alarm_time = takecommand()

        # Extract the alarm time using datefinder
        dTimeA = list(datefinder.find_dates(alarm_time))
        
        if not dTimeA:
            speak("Could not understand the time. Please try again.")
            return
        
        alarm_datetime = dTimeA[0]
        hourA = alarm_datetime.hour
        minA = alarm_datetime.minute

        speak(f"Alarm set for {alarm_datetime.strftime('%I:%M %p')}.")

        while True:
            current_time = datetime.now()
            if current_time.hour == hourA and current_time.minute == minA:
                speak("The alarm is going on now!")
                # Use the playsound function to play the alarm sound
                music_dir = "www\\assets\\audio\\alarm.mp3"
                playsound(music_dir)
                break
            elif current_time.hour > hourA or (current_time.hour == hourA and current_time.minute > minA):
                break

    except Exception as e:
        speak("An error occurred while setting the alarm.")
        print(f"Error in set_alarm: {e}")

def get_weather(location):
    """Function to get weather data for a location."""
    if not location:
        return "Please provide a location for the weather report."
    location = location.strip().title()

    try:
        response = requests.get(BASE_URL, params={
            'q': location,
            'appid': API_KEY,
            'units': 'metric'
        })
        data = response.json()

        if data['cod'] == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {location} is {weather_description} with a temperature of {temperature}°C."
        elif data['cod'] == "404":
            return f"Error: City '{location}' not found. Please check the city name."
        else:
            return f"Error: {data.get('message', 'Unable to get weather data.')}"
    except Exception as e:
        return f"An error occurred while fetching the weather: {e}"

def get_current_location():
    """Function to get the current city based on IP address."""
    try:
        response = requests.get('http://ip-api.com/json/')
        data = response.json()
        if data['status'] == 'fail':
            return None
        return data['city']
    except Exception as e:
        print(f"Error getting current location: {e}")
        return None

def takecommand():
    """Function to listen for and return a voice command."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        eel.DisplayMessage('Listening...')
        sr.pause_threshold = 3.0
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=6)
        except sr.WaitTimeoutError:
            eel.DisplayMessage('No speech detected.')
            return ""
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"Command: {query}")
        eel.DisplayMessage(query)
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that. Please tell me again.")
        return ""
    except sr.RequestError as e:
        speak(f"Network error: {e}")
        return ""

@eel.expose
def TaskExecution(message=1):
    """Function to execute tasks based on voice commands."""
    global greeted

    # If no message is passed, take voice command
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    # Greet the user only once
    if not greeted:
        wish()
        greeted = True

    try:
        if not query:
            eel.DisplayMessage("No command detected.")
            return

        query = query.lower()

        if "what's the weather" in query:
            city = query.replace("what's the weather", "").strip()
            if "in" in city:
                city = city.split("in")[-1].strip()
            else:
                city = get_current_location()

            weather_info = get_weather(city)
            speak(weather_info)
            eel.DisplayMessage(weather_info)

        elif "where am i" in query or "what is my location" in query:
            location_info = get_current_location() or "Unable to determine your location."
            speak(location_info)
            eel.DisplayMessage(location_info)

        elif "set the alarm" in query:
            set_alarm()

           

        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "dismiss" in query:
            speak("Okay, I am closing the program.")
            eel.DisplayMessage("Stopping all processes...")
            close_program()

        elif "sleep" in query:
            speak("Okay, I'll go to sleep now.")
            eel.DisplayMessage("Assistant is in sleep mode.")
            eel.SetAssistantState("sleep")

        elif "shutdown" in query:
            speak("Shutting down.")
            os.system('shutdown -s')

        elif "what's up" in query or "how are you" in query:
            stMsgs = [
                'Just doing my thing!', 
                'I am fine!', 
                'Nice!', 
                'I am nice and full of energy!', 
                'I am okay! How are you?'
            ]
            ans_q = random.choice(stMsgs)
            speak(ans_q)

        elif "who made you" in query:
            ans_m = "For your information, Soumyadyuti Dey created me! I give a lot of thanks to him."
            speak(ans_m)
            eel.DisplayMessage(ans_m)

        elif "who are you" in query:
            about = "I am AVA (Advanced Voice Assistant), an AI-based assistant to help you like a close friend! I can perform tasks and provide information as needed."
            speak(about)
            eel.DisplayMessage(about)

        elif "hello" in query or "hello avas" in query:
            speak("Hello sir!")

        elif "your name" in query:
            speak("Thanks for asking my name! I am AVAS.")

        else:

            from engine.features import chatBot
            chatBot(query)
            # WolframAlpha query handling
            try:
                res = app.query(query)
                answer = next(res.results).text
                speak(answer)
                eel.DisplayMessage(answer)
            except Exception as e:
                print("Error:", e)
                speak("Sorry, I couldn't find the answer to your query.")

    except Exception as e:
        print(f"Error in task execution: {e}")
        eel.DisplayMessage("An error occurred while processing the command.")
    
    finally:
        eel.ShowHood()  # Return to idle state after each command