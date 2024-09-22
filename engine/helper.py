import re

import eel
import pyautogui

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s*(?:on\s+youtube)?$'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name, otherwise return None
    extracted_term = match.group(1).strip() if match else None
    # Check if the extracted term is empty or None
    return extracted_term if extracted_term else None

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