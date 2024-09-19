import pyttsx3
import speech_recognition as sr
import eel
import pyautogui
import time
import requests

from engine.config import ASSISTANT_NAME

# Your OpenWeatherMap API key
API_KEY = '4ad432a816fb1ab0e83d962d52909803'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


def speak(text):
    """Function to speak text and display it."""
    print(f"Speaking: {text}")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


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
        eel.ShowHood()
        return ""
    except sr.RequestError as e:
        speak(f"Network error: {e}")
        eel.ShowHood()
        return ""


def process_weather_command(query):
    """Function to process weather-related commands."""
    city = query.replace(ASSISTANT_NAME, "").replace("weather", "").strip()
    if city:
        weather_info = get_weather(city)
    else:
        current_location = get_current_location()
        if current_location:
            weather_info = get_weather(current_location)
        else:
            weather_info = "Unable to determine your current location."
    
    speak(weather_info)
    eel.DisplayMessage(weather_info)


def close_program():
    """Function to close/minimize the GUI program."""
    try:
        close_button_x, close_button_y = 1900, 10
        pyautogui.moveTo(close_button_x, close_button_y)
        pyautogui.click()
        eel.DisplayMessage("Program closed.")
    except Exception as e:
        print(f"Error while trying to close the program: {e}")
        eel.DisplayMessage("Error while closing the program.")


# Function to execute tasks based on commands
@eel.expose
def TaskExecution():
    try:
        query = takecommand()  # Capture voice command
        print(query)

        if "weather" in query:
            # Remove any assistant name from the query and clean it up
            city = query.replace(ASSISTANT_NAME, "").replace("weather", "").strip()
            
            if "in" in city:  # Check if a specific location was mentioned
                city = city.split("in")[-1].strip()  # Get the location after 'in'
            
            if city and not city.lower().startswith("tell me the"):
                # If a valid city is mentioned
                weather_info = get_weather(city)
                speak(weather_info)
                eel.DisplayMessage(weather_info)
            else:
                # If no specific city is mentioned, get the weather of the current location
                current_location = get_current_location()
                if current_location:
                    weather_info = get_weather(current_location)
                    speak(weather_info)
                    eel.DisplayMessage(weather_info)
                else:
                    speak("Unable to determine your current location.")
                    eel.DisplayMessage("Unable to determine your current location.")
        elif "where am i" in query or "what is my location" in query:
            location_info = get_current_location()
            speak(location_info)
            eel.DisplayMessage(location_info)
        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "dismiss" in query:
            speak("Okay,I am closing the program")
            eel.DisplayMessage("Stopping all processes...")
            close_program()
        elif "sleep" in query:
            speak("Okay, I'll go to sleep now.")
            eel.DisplayMessage("Assistant is in sleep mode.")
            eel.SetAssistantState("sleep")  # Signal UI for sleep mode
        else:
            eel.DisplayMessage("Command not recognized.")
    except Exception as e:
        print(f"Error in task execution: {e}")
        eel.DisplayMessage("An error occurred while processing the command.")

    eel.ShowHood()  # Return to idle state after each command