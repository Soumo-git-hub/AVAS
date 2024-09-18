import os
import eel
from engine.features import playassistantsound  # Adjust the import based on actual function location
from engine.command import *  # Assuming relevant commands from the module are used elsewhere

def start():
    eel.init("www")  # Initialize Eel with the folder containing web files

    # Play the assistant sound on startup
    playassistantsound()

    # Open Microsoft Edge in app mode for the local web app
    os.system('start msedge --app="http://localhost:8000/index.html"')

    # Start the Eel app with specified settings (localhost, no GUI mode)
    eel.start('index.html', mode=None, host='localhost', block=True)