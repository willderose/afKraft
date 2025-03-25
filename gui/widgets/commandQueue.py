# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtWidgets
from PySide6 import QtCore

import afKraftResources
from gui.utilityWidgets import commandContainer, afKraftSection, genericInputOptions
from gui.queueWidgets import craftWidget


class CommandQueue(afKraftSection.AfKraftSection):
    """ Widget to contain the various commands we add to the queue
    """

    queueChanged = QtCore.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.commandQueueWidgets = []

        # To be set by afCraft's main window to avoid having to juggle with this widget's parents
        self.synthButtonPos = None

        self._setupConnections()

        self.addCraft()
        self.addKeypress()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        super()._setupAppearance()

        self.saCommandQueueArea.setStyleSheet(afKraftResources.getStyleForWidget(self.saCommandQueueArea))
        self.wCommandQueue.setStyleSheet('QWidget#wCommandQueue { background-color: rgba(0, 0, 0, 0) }')

        self.vBoxCommandQueue.setContentsMargins(0, 0, 0, 0)
        self.vBoxCommandQueue.setAlignment(QtCore.Qt.AlignTop)

        self.cmbAddCommand.addItem('Add New...')
        commandSignalMap = [('Craft', self.addCraft), ('Keypress', self.addKeypress), ]
        for commandText, commandSignal in commandSignalMap:
            self.cmbAddCommand.addItem(commandText, userData=commandSignal)

        self.cmbAddCommand.setStyleSheet(afKraftResources.getStyleForWidget(self.cmbAddCommand))
        self.cmbAddCommand.setFixedHeight(28)

        self.setTitle('Command Queue')

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.cmbAddCommand.activated.connect(self.onCommandAdded)
        self.qtStartTimer.timeout.connect(self.runCommandQueue)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """
        super()._setupUi()

        self.wCommandQueue = QtWidgets.QWidget(parent=self)
        self.wCommandQueue.setObjectName('wCommandQueue')

        self.cmbAddCommand = QtWidgets.QComboBox(parent=self)

        self.vBoxCommandQueue = QtWidgets.QVBoxLayout()
        self.vBoxCommandQueue.addWidget(self.cmbAddCommand)

        self.saCommandQueueArea = QtWidgets.QScrollArea(parent=self)
        self.saCommandQueueArea.setWidget(self.wCommandQueue)
        self.saCommandQueueArea.setWidgetResizable(True)
        self.saCommandQueueArea.setObjectName('saCommandQueueArea')
        self.wCommandQueue.setLayout(self.vBoxCommandQueue)

        self.addWidget(self.saCommandQueueArea)

        self.qtStartTimer = QtCore.QTimer(parent=self)
        self.qtStartTimer.setSingleShot(True)
        self.qtStartTimer.setTimerType(QtCore.Qt.PreciseTimer)

    @QtCore.Slot()
    def onCommandAdded(self, idx):
        """ Since each item in the comboBox' list need to fire separate signals, filter and fire them here
        """

        signalToFire = self.cmbAddCommand.itemData(idx, QtCore.Qt.UserRole)
        if not signalToFire:
            return

        signalToFire()
        self.cmbAddCommand.setCurrentIndex(0)

        self.queueChanged.emit(len(self.commandQueueWidgets) > 0)

    @QtCore.Slot()
    def onCommandRemoved(self, commandWidget):
        """ Remove the supplied command widget from the command queue
        """

        commandIndex = self.vBoxCommandQueue.indexOf(commandWidget)
        self.commandQueueWidgets.pop(commandIndex)
        self.vBoxCommandQueue.removeWidget(commandWidget)
        commandWidget.deleteLater()

        self.queueChanged.emit(len(self.commandQueueWidgets) > 0)

    def addCommandToQueue(self, commandWidget, commandType):
        """ Insert a command widget in the command queue
        """

        newCommandWidget = commandContainer.CommandContainer(commandType)
        newCommandWidget.addWidget(commandWidget)
        newCommandWidget.commandRemoved.connect(self.onCommandRemoved)

        self.vBoxCommandQueue.insertWidget(len(self.commandQueueWidgets), newCommandWidget)
        self.commandQueueWidgets.append(commandWidget)

    def addCraft(self):
        """ Add a craft widget to the command queue
        """

        self.addCommandToQueue(
            commandWidget=craftWidget.CraftWidget(parent=self),
            commandType='New Craft'
        )

    def addKeypress(self):
        """ Add a keypress change widget to the command queue
        """

        self.addCommandToQueue(
            commandWidget=genericInputOptions.GenericInputOptions(parent=self),
            commandType='New Generic Input'
        )

    def runCommandQueue(self):
        """ Run the commands that a user has queued
        """

        # Create the chain of commands that will be executed
        for queuedCommandWidget in self.commandQueueWidgets:
            queuedCommandWidget.synthButtonPos = self.synthButtonPos
            widgetQueueIndex = self.commandQueueWidgets.index(queuedCommandWidget)
            nextCommandIndex = widgetQueueIndex + 1
            if nextCommandIndex == len(self.commandQueueWidgets):
                break
            queuedCommandWidget.commandFinished.connect(self.commandQueueWidgets[nextCommandIndex].runCommand)

        self.commandQueueWidgets[0].runCommand()
