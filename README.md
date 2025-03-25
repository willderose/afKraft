# afKraft

Af Kraft is a crafting utility made mainly for personal use within FFXIV.

It allows a user to set up a list of actions to run in sequence as to allow for passive crafting.

A couple of dependencies need to be installed for it to properly work, if you wish to use it yourself:
- PySide (any version _should_ do, but this project was built with PySide6)
  - Can be installed using `python -m pip install pyside6` from a windows command prompt
- pyautogui
  - Can be installed using `python -m pip install pyautogui` from a windows command prompt

# How to use
If you're launching this from a release:
- Run the included afKraft.exe as administrator (it seems pyautogui requires it)

If you're launching this from a cloned repo:
From a Python terminal, run the afKraft.py file under the gui module:
- `python {pathToRepo}/gui/afKraft.py`

From there, users are free to setup the command queue through the "Add New..." options.
A "Craft" command allows a user to chain macros together for a craft.
The "Keypress" command allows a user to set a generic input (mouse or keyboard) to be run with a delay

Once the queue is built, set the location of the in-game Synthesize button (on the crafting window, bottom right), set a start delay, if desired, then Launch your queue with the "Launch Command(s)" button at the bottom.

Still very much a WIP, so broken functionalities are to be expected.
