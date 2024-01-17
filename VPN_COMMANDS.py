import cv2
import numpy as np
import pyautogui
import Logger
import time
import os

absolute_path=os.path.dirname(__file__)

# Load the button image from a file
disconnect_button_image_relative_path='assets/disconnect_button.png'
disconnect_button_image_path = os.path.normpath(os.path.join(absolute_path, disconnect_button_image_relative_path))
disconnect_button_image = cv2.imread(disconnect_button_image_path, cv2.IMREAD_UNCHANGED)
connect_button_image_relative_path='assets/connect_button.png'
connect_button_image_path=os.path.normpath(os.path.join(absolute_path, connect_button_image_relative_path))
connect_button_image=cv2.imread(connect_button_image_path, cv2.IMREAD_UNCHANGED)

similarity_threshold = 0.5

# Function to find the button on the screen
def find_button_on_screen(button_img):
    # Take a screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # Use template matching to find the button's location on the screen
    result = cv2.matchTemplate(screenshot, button_img, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc

    if max_val < similarity_threshold:
        return None

    top_left = max_loc
    return top_left


# Function to click the button given the coordinates
def click_button(coordinates,button_image):
    pyautogui.moveTo(coordinates[0] + button_image.shape[1]//2, coordinates[1] + button_image.shape[0]//2)
    pyautogui.click()


#VPN COMMANDS
def RESTART_VPN():
    button_location = find_button_on_screen(disconnect_button_image)
    if button_location is not None:
        click_button(button_location, disconnect_button_image)
        time.sleep(1.5)
        click_button(button_location, connect_button_image)
        Logger.LOG("RESTARTED VPN")
    else:
        Logger.LOG("ERROR: UNABLE TO FIND BUTTON, CANNOT RESTART VPN.")

def STOP_VPN():
    button_location = find_button_on_screen(disconnect_button_image)
    if button_location is not None:
        click_button(button_location, disconnect_button_image)
        time.sleep(1.5)
        Logger.LOG("STOPPED VPN")
    else:
        Logger.LOG("ERROR: UNABLE TO FIND BUTTON, CANNOT STOP VPN.")

def START_VPN():
    button_location = find_button_on_screen(connect_button_image)
    if button_location is not None:
        click_button(button_location, disconnect_button_image)
        time.sleep(1.5)
        Logger.LOG("STARTED VPN")
    else:
        Logger.LOG("ERROR: UNABLE TO FIND BUTTON, CANNOT START VPN.")

# STOP_VPN()
# START_VPN()
# RESTART_VPN()