import os
import eel
from engine.features import playassistantsound

def start():
    try:
        eel.init("www")  # Initialize Eel with the folder containing the web files
        playassistantsound()  # Play the assistant sound on startup

        # Open Microsoft Edge in kiosk mode for the local web app
        os.system('start msedge --kiosk "http://localhost:8000/index.html"')

        # Start the Eel app (localhost, no GUI mode)
        eel.start('index.html', mode=None, host='localhost', block=True)

    except Exception as e:
        print(f"Error during startup: {e}")
