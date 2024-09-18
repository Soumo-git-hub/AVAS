import pyttsx3
import speech_recognition as sr
import eel
import pyautogui
import time

# Function to speak text
def speak(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 140)
    eel.DisplayMessage(text)  # Display message on UI
    engine.say(text)
    engine.runAndWait()

# Function to listen for commands
def takecommand():
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
        eel.DisplayMessage(query)  # Display recognized command
        time.sleep(2)
    except sr.UnknownValueError:
        eel.DisplayMessage("Sorry, I couldn't understand that. Please tell me again.")
        speak("Sorry, I couldn't understand that. Please tell me again.")
        eel.ShowHood()  # Return to idle state
        return ""
    except sr.RequestError as e:
        eel.DisplayMessage(f"Network error: {e}")
        speak(f"Network error: {e}")
        eel.ShowHood()
        return ""

    return query.lower()

# Function to close/minimize the GUI program
def close_program():
    try:
        # Coordinates of the close button; adjust based on your screen resolution or minimize the window
        close_button_x, close_button_y = 1900, 10  # Example coordinates for the close button
        pyautogui.moveTo(close_button_x, close_button_y)
        pyautogui.click()  # Click the close button to simulate closing the window
        eel.DisplayMessage("Program closed.")
    except Exception as e:
        print(f"Error while trying to close the program: {e}")
        eel.DisplayMessage("Error while closing the program.")

# Function to execute tasks based on commands
@eel.expose
def TaskExecution():
    try:
        query = takecommand()  # Capture the voice command
        print(f"TaskExecution received: {query}")

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "dismiss" in query or "close program" in query:
            speak("Okay, stopping all processes and closing the program.")
            eel.DisplayMessage("Stopping all processes and closing the program...")
            close_program()  # Call the function to close the program
        else:
            eel.DisplayMessage("Command not recognized. Please try again.")
    except Exception as e:
        print(f"Error in task execution: {e}")
        eel.DisplayMessage("An error occurred while processing the command.")

    eel.ShowHood()  # Return to idle state if no other command is matched