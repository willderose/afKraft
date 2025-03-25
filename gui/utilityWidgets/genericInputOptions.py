# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#
import time

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import afKraftResources.styleSheets
from gui.utilityWidgets import mousePosPicker
from gui.utilityWidgets import keybindSelector

import core.inputTypes
import afKraftResources.afKraft


class GenericInputOptions(QtWidgets.QWidget):
    """ Widget allowing a user to pick from a simple mouse click or
    """

    commandFinished = QtCore.Signal()

    # To account for server ticks or oddities, add this to the time a macro takes
    ADDITIONAL_SAFETY_END_TIME = 1.2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.synthButtonPos = None

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.chbInputType.setChecked(True)
        self.chbInputType.setText('Mouse / KB?')
        self.chbInputType.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.chbInputType.setStyleSheet(afKraftResources.getStyleForWidget(self.chbInputType))

        self.liEdInputDelay.setPlaceholderText('0')
        self.liEdInputDelay.setStyleSheet(afKraftResources.getStyleForWidget(self.liEdInputDelay))
        self.liEdInputDelay.setFixedHeight(30)
        self.liEdInputDelay.setFixedWidth(90)

        self.hBoxGlobal.setAlignment(QtCore.Qt.AlignLeft)
        self.hBoxGlobal.setContentsMargins(2, 6, 2, 6)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.chbInputType.toggled.connect(self.onInputTypeChanged)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.chbInputType = QtWidgets.QCheckBox(parent=self)

        self.pbMousePosPicker = mousePosPicker.MousePosPicker(targetButtonText='Generic', parent=self)

        self.qkKeybindTarget = keybindSelector.KeybindSelector(keybindTarget='Generic', parent=self)

        self.liEdInputDelay = QtWidgets.QLineEdit(parent=self)
        self.liEdInputDelay.setValidator(QtGui.QIntValidator(1, 10))

        self.hBoxGlobal = QtWidgets.QHBoxLayout()
        self.hBoxGlobal.addWidget(self.chbInputType)
        self.hBoxGlobal.addWidget(self.pbMousePosPicker)
        self.hBoxGlobal.addWidget(self.qkKeybindTarget)
        self.hBoxGlobal.addWidget(self.liEdInputDelay)

        self.setLayout(self.hBoxGlobal)

    def macroTime(self):
        """ Convenience to quickly ge the time this macro will take

        :return: The converted integer value of the macro time line edit
        :rtype: int
        """

        return int(self.liEdInputDelay.text() or 0) * 1000

    def macroEndTime(self):
        """ To account for game shenanigans, add an additional wait time at the end of a craft

        :return: The converted integer value of the macro timeline edit with the added safety time
        :rtype: int
        """

        return (float(self.liEdInputDelay.text() or 0) + self.ADDITIONAL_SAFETY_END_TIME) * 1000

    def runCommand(self):
        """ Run the command attached to this widget
        """

        if self.chbInputType.isChecked():
            core.inputTypes.runKeybind(self.qkKeybindTarget.keySequence().toString())
        else:
            core.inputTypes.moveMouseToSynthButton(self.pbMousePosPicker.pickedCursorPosition)
            core.inputTypes.mouseClick()

        self.commandFinished.emit()

    @QtCore.Slot()
    def onInputTypeChanged(self, newState: bool):
        """ Show / hide the appropriate input pickers according to the active input type
        """

        self.pbMousePosPicker.setVisible(not newState)
        self.qkKeybindTarget.setVisible(newState)
