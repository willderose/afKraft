# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

import time
import pyautogui


def runKeybind(sequenceStr: str):
    """ Run a virtual keybind from a series of keys
    """

    if not sequenceStr:
        return

    modifierCorrespondence = {
        'Ctrl': 'ctrlleft',
        'Alt': 'altleft',
        'Shift': 'shiftleft'
    }

    pyautoKeys = [modifierCorrespondence.get(key, key).lower() for key in sequenceStr.split('+')]
    pyautogui.hotkey(*pyautoKeys, interval=0.05)


def mouseClick():
    time.sleep(0.5)
    pyautogui.leftClick()
    pyautogui.mouseUp()
    time.sleep(1.5)


def moveMouseToSynthButton(mousePos):
    pyautogui.moveTo(mousePos)
