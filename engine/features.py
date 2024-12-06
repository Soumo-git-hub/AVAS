import os
import time
from playsound import playsound
import eel
import webbrowser
import sqlite3
import pywhatkit as kit
import pvporcupine
import pyaudio
import struct
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
from engine.helper import extract_yt_term

# Database connection
con = sqlite3.connect("avas.db")
cursor = con.cursor()

# Play assistant startup sound
@eel.expose
def playassistantsound():
    music_dir = "www\\assets\\audio\\startsound1.mp3" 
    playsound(music_dir)

# Function to open commands (apps or websites)
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()

    if app_name := query:
        try:
            # Check for application path in the database
            cursor.execute('SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if results:
                speak(f"Opening {app_name}")
                os.startfile(results[0][0])

            # If not found, check for website URL
            else:
                cursor.execute('SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()

                if results:
                    speak(f"Opening {app_name}")
                    webbrowser.open(results[0][0])
                else:
                    speak(f"Opening {app_name}")
                    os.system(f'start {app_name}')
        except Exception as e:
            speak(f"Something went wrong: {e}")

# Play a YouTube video based on the query
def PlayYoutube(query):
    search_term = extract_yt_term(query)

    if search_term:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    else:
        speak("I couldn't understand what you want to say.")


# Hotword detection using Porcupine
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Create Porcupine instance with the custom keyword file
        porcupine = pvporcupine.create(
            access_key='cLPoj1XYFrimJwyEqf/ZdcoT4BRx1HasbgzRZWiLWzeF/suDOTHofw==',
            keyword_paths=['C:\\Users\\acer\\Downloads\\Activate_en_windows_v3_0_0\\Activate_en_windows_v3_0_0.ppn'],
            sensitivities=[0.7]  # Adjust the sensitivity if needed
        )

        # Initialize PyAudio
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate,
                                 channels=1,
                                 format=pyaudio.paInt16,
                                 input=True,
                                 frames_per_buffer=porcupine.frame_length)

        # Loop to continuously listen for the hotword
        while True:
            keyword_data = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword_data)

            # Check if the hotword is detected
            if porcupine.process(keyword) >= 0:
                print("Hotword 'Activate' detected")

                # Simulate pressing the Win+S shortcut
                pyautogui.keyDown("win")
                pyautogui.press("A")
                time.sleep(2)
                pyautogui.keyUp("win")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up resources
        if porcupine:
            porcupine.delete()
        if audio_stream:
            audio_stream.close()
        if paud:
            paud.terminate()