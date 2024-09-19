import os
import eel
from engine.features import playassistantsound  # Adjust the import based on actual function location

def start():
    eel.init("www")  # Initialize Eel with the folder containing web files

    # Play the assistant sound on startup
    playassistantsound()

    # Open Microsoft Edge in kiosk mode for the local web app
    os.system('start msedge --kiosk "http://localhost:8000/index.html"')

    # Start the Eel app with specified settings (localhost, no GUI mode)
    eel.start('index.html', mode=None, host='localhost', block=True)
