# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtCore
from PySide6 import QtWidgets

import afKraftResources

from gui.utilityWidgets import genericInputOptions


class MacroListOptions(QtWidgets.QGroupBox):
    """ Contains the various macro options widgets to run during a craft
    """

    commandFinished = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._macroWidgets = []

        self._macroTimers = []

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

        self.onMacroAdded()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.setTitle('Craft Macro List')
        self.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.setFlat(True)

        self.pbAddMacro.setText('Add Macro')
        self.pbAddMacro.setFixedHeight(28)
        self.pbAddMacro.setStyleSheet(afKraftResources.getStyleForWidget(self.pbAddMacro))

        self.vBoxGlobal.setContentsMargins(2, 6, 2, 6)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.pbAddMacro.clicked.connect(self.onMacroAdded)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.pbAddMacro = QtWidgets.QPushButton(parent=self)

        self.vBoxGlobal = QtWidgets.QVBoxLayout()
        self.vBoxGlobal.addWidget(self.pbAddMacro)

        self.setLayout(self.vBoxGlobal)

    @QtCore.Slot()
    def onMacroAdded(self):
        """ Add a macro options picker to the list
        """

        newInputWidget = genericInputOptions.GenericInputOptions(parent=self)
        self.vBoxGlobal.insertWidget(len(self._macroWidgets), newInputWidget)
        self._macroWidgets.append(newInputWidget)

    def runMacros(self):
        """ Build the series of macro keybinds and times from our list of macro option widgets
        """

        if not self._macroTimers:
            self.setupMacroTimers()

        self._macroWidgets[0].runCommand()
        self._macroTimers[0].start()

    def setupMacroTimers(self):
        """ Create the timers that will take care of launching the sequence of macros
        """

        # First timer (first macro time) launches second macro, second the third, etc.
        # Last timer ends the craft and starts a new one

        for macroWidget in self._macroWidgets:
            timer = self.createTimer(macroWidget.macroTime())
            self._macroTimers.append(timer)

        for timerIndex, macroTimer in enumerate(self._macroTimers):
            nextIndex = timerIndex + 1
            try:
                macroTimer.timeout.connect(self._macroWidgets[nextIndex].runCommand)
                macroTimer.timeout.connect(self._macroTimers[nextIndex].start)
            except IndexError:
                macroTimer.setInterval(self._macroWidgets[-1].macroEndTime())
                macroTimer.timeout.connect(self.commandFinished.emit)

    def createTimer(self, timerMSecs):
        """ Create a QTimer with the standard values with the supplied time

        :return: A pre set QTimer instance
        :rtype: <class: QtCore.QTimer>
        """

        newTimer = QtCore.QTimer(parent=self)
        newTimer.setTimerType(QtCore.Qt.PreciseTimer)
        newTimer.setInterval(timerMSecs)
        newTimer.setSingleShot(True)

        return newTimer

    def totalMacroTime(self):
        """ Calculate the total time this list's macros will take

        :return: The total time the macros will take
        :rtype: int
        """

        totalMacroTime = 0
        for macroWidget in self._macroWidgets:
            totalMacroTime += macroWidget.macroEndTime()

        return totalMacroTime
