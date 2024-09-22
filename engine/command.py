import os
import pyttsx3
import speech_recognition as sr
import eel
import pyautogui
import time
import requests
import datetime
import random

from engine.config import ASSISTANT_NAME
from engine.helper import close_program

# Your OpenWeatherMap API key
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
        engine.setProperty('voice', voices[1].id)
        engine.setProperty('rate', 140)
        eel.DisplayMessage(text)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speak function: {e}")


def wish_me():
    """Function to greet the user based on the time of day."""
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning! How may I help you?")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon! How may I assist you?")
    else:
        speak("Good evening! How may I assist you?")


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
        r.pause_threshold = 1
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
def TaskExecution():
    """Function to execute tasks based on voice commands."""
    global greeted
    
    # Greet the user only once
    if not greeted:
        wish_me()
        greeted = True
    
    try:
        query = takecommand()
        if not query:
            eel.DisplayMessage("No command detected.")
            return

        if "what's the weather" in query:
            # Extract the city after "in" if present in the query
            city = query.replace("what's the weather", "").strip()
            if "in" in city:
                city = city.split("in")[-1].strip()
            else:
                city = get_current_location()  # Use the current location if no city is specified

            weather_info = get_weather(city)
            speak(weather_info)
            eel.DisplayMessage(weather_info)  # Weather


        elif "where am i" in query or "what is my location" in query:
            location_info = get_current_location() or "Unable to determine your location."
            speak(location_info)
            eel.DisplayMessage(location_info)

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
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy', 'I am okay! How are you?']
            ans_q = random.choice(stMsgs)
            speak(ans_q)

        elif "who made you" in query:
            ans_m = "For your information, Soumyadyuti Dey created me! I give a lot of thanks to him."
            speak(ans_m)
            eel.DisplayMessage(ans_m)

        elif "who are you" in query:
            about = "I am AVAS (Advanced Voice Assistant System), an AI-based assistant to help you like a close friend! I can perform tasks and provide information as needed."
            speak(about)
            eel.DisplayMessage(about)

        elif "hello" in query or "hello AVAS" in query:
            speak('Hello sir')

        elif "your name" in query:
            speak("Thanks for asking my name! I am AVAS.")

        else:
            eel.DisplayMessage("Command not recognized.")

    except Exception as e:
        print(f"Error in task execution: {e}")
        eel.DisplayMessage("An error occurred while processing the command.")
    finally:
        eel.ShowHood()  # Return to idle state after each command
