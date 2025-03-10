# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtCore
from PySide6 import QtWidgets

import afKraftCommands
from gui.widgets import afKraftSpinBox
from gui.widgets import macroListOptions
from gui.widgets import craftProgBar

import afKraftResources


class CraftWidget(QtWidgets.QStackedWidget):
    """ Contains the various widgets for a specific craft
    """

    craftFinished = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.finishedCrafts = 0
        self.isCraftPaused = False
        self._craftAmount = 0

        # Convenience attribute to avoid juggling around this widget's parents
        self.synthButtonPos = None

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

        self.wCraftProgress.setCraftingData('Moqueca HQ', 150, 3600)
        self.wCraftProgress.setProgress(75)
        self.setCurrentIndex(1)

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.liEdCraftName.setPlaceholderText('Craft Name')
        self.liEdCraftName.setFixedHeight(26)
        self.liEdCraftName.setStyleSheet(afKraftResources.getStyleForWidget(self.liEdCraftName))

        self.labCraftAmount.setText('Amount to craft:')
        self.labCraftAmount.setStyleSheet(afKraftResources.getStyleForWidget(self.labCraftAmount))

        self.vBoxCraftOptions.setContentsMargins(2, 2, 2, 2)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.wCraftProgress.craftResumed.connect(self.onCraftResumed)
        self.wCraftProgress.craftPaused.connect(self.onCraftPaused)
        self.wCraftProgress.craftCanceled.connect(self.onCraftCanceled)

        self.macroListWidget.commandFinished.connect(self.runCommand)
        self.macroListWidget.commandFinished.connect(self.updateProgress)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.liEdCraftName = QtWidgets.QLineEdit(parent=self)

        self.labCraftAmount = QtWidgets.QLabel(parent=self)

        self.spbCraftAmount = afKraftSpinBox.AfKraftSpinBox(parent=self)

        self.hBoxCraftAmount = QtWidgets.QHBoxLayout()
        self.hBoxCraftAmount.addWidget(self.labCraftAmount)
        self.hBoxCraftAmount.addStretch()
        self.hBoxCraftAmount.addWidget(self.spbCraftAmount)

        self.macroListWidget = macroListOptions.MacroListOptions(parent=self)

        self.vBoxCraftOptions = QtWidgets.QVBoxLayout()
        self.vBoxCraftOptions.addWidget(self.liEdCraftName)
        self.vBoxCraftOptions.addWidget(self.macroListWidget)
        self.vBoxCraftOptions.addLayout(self.hBoxCraftAmount)

        self.wCraftOptions = QtWidgets.QWidget(parent=self)
        self.wCraftOptions.setLayout(self.vBoxCraftOptions)

        self.wCraftProgress = craftProgBar.CraftProgBar(parent=self)

        self.addWidget(self.wCraftOptions)
        self.addWidget(self.wCraftProgress)

    def craftAmount(self):
        """ The amount of this craft to perform
        """

        return self.spbCraftAmount.spbValue.value()

    def runCommand(self):
        """ Run the attached macros for the amount of desired crafts, displaying the progress bar
        """

        # Don't start a new craft if user has paused the chain
        if self.isCraftPaused:
            return

        if self.finishedCrafts == self.craftAmount():
            self.craftFinished.emit()
            return

        self.wCraftProgress.setCraftingData(
            self.liEdCraftName.text(),
            self.craftAmount(),
            self.totalCraftTime()
        )

        self.setCurrentIndex(1)
        afKraftCommands.moveMouseToSynthButton(self.synthButtonPos)
        afKraftCommands.mouseClick()
        self.macroListWidget.runMacros()
        self.finishedCrafts += 1

    def totalCraftTime(self):
        """ Calculate the total time for this macro combos

        :return: The amount of time these crafts will take
        :rtype: int
        """

        return (self.macroListWidget.totalMacroTime() * self.craftAmount()) / 1000

    def updateProgress(self):
        """ Update the progress bar with the relevant information
        """

        self.wCraftProgress.setProgress(self.finishedCrafts)

    @QtCore.Slot()
    def onCraftPaused(self):
        """ Pause this craft, preventing new crafts until it is resumed
        """

        self.isCraftPaused = True

    @QtCore.Slot()
    def onCraftResumed(self):
        """ Resume this craft
        """

        self.isCraftPaused = False
        self.runCommand()

    @QtCore.Slot()
    def onCraftCanceled(self):
        """ Reset this craft's display
        """

        for qTimer in self.macroListWidget._macroTimers:
            qTimer.stop()

        self.finishedCrafts = 0
        self.setCurrentIndex(0)