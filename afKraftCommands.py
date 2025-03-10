# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

import time
import pyautogui


def runKeybind(qKeySequence):
    if not qKeySequence.count():
        return

    modifierCorrespondence = {
        'Ctrl': 'ctrlleft',
        'Alt': 'altleft',
        'Shift': 'shiftleft'
    }

    pyautoKeys = [modifierCorrespondence.get(key, key).lower() for key in qKeySequence.toString().split('+')]
    pyautogui.hotkey(*pyautoKeys, interval=0.05)


def moveMouseToSynthButton(mousePos):
    pyautogui.moveTo(mousePos)


def mouseClick():
    time.sleep(0.5)
    pyautogui.leftClick()
    pyautogui.mouseUp()
    time.sleep(1.15)
