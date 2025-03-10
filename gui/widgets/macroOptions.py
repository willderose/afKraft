# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtGui
from PySide6 import QtWidgets

from gui.widgets import keybindSelector

import afKraftResources

import afKraftCommands


class MacroOptions(QtWidgets.QWidget):
    """ Contains the options for individual macros
    """

    # To account for server ticks or oddities, add this to the time a macro takes
    ADDITIONAL_SAFETY_END_TIME = 1.2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.liEdMacroLength.setPlaceholderText('Macro time (seconds)')
        self.liEdMacroLength.setStyleSheet(afKraftResources.getStyleForWidget(self.liEdMacroLength))
        self.liEdMacroLength.setFixedHeight(26)

        self.hBoxGlobal.setContentsMargins(0, 0, 0, 0)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.liEdMacroLength = QtWidgets.QLineEdit(parent=self)
        self.liEdMacroLength.setValidator(QtGui.QIntValidator(1, 10))

        self.qkMacroKeybind = keybindSelector.KeybindSelector(keybindTarget='Macro', parent=self)

        self.hBoxGlobal = QtWidgets.QHBoxLayout()
        self.hBoxGlobal.addWidget(self.qkMacroKeybind)
        self.hBoxGlobal.addWidget(self.liEdMacroLength)

        self.setLayout(self.hBoxGlobal)

    def macroTime(self):
        """ Convenience to quickly ge the time this macro will take

        :return: The converted integer value of the macro time line edit
        :rtype: int
        """

        return int(self.liEdMacroLength.text() or 0) * 1000

    def macroEndTime(self):
        """ To account for game shenanigans, add an additional wait time at the end of a craft

        :return: The converted integer value of the macro timeline edit with the added safety time
        :rtype: int
        """

        return (float(self.liEdMacroLength.text() or 0) + self.ADDITIONAL_SAFETY_END_TIME) * 1000

    def runCommand(self):
        """ Run the command attached to this widget
        """

        afKraftCommands.runKeybind(self.qkMacroKeybind.keySequence())
