# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

import sys

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from gui.widgets import afKraftTitleBar
from gui.widgets import afKraftOptions
from gui.widgets import commandQueue

import afKraftResources


class AfCraftWindow(QtWidgets.QMainWindow):
    """ FF14 AFK crafting utility. Sets up your macro commands, and let it rip
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.pbLaunchCommand.setText('Launch Command(s)')
        self.pbLaunchCommand.setMinimumHeight(40)
        self.pbLaunchCommand.setFixedWidth(210)
        self.pbLaunchCommand.setEnabled(False)
        self.pbLaunchCommand.setStyleSheet(afKraftResources.getStyleForWidget(self.pbLaunchCommand))

        self.vBoxGlobal.setContentsMargins(8, 0, 8, 12)
        self.vBoxGlobal.setAlignment(self.pbLaunchCommand, QtCore.Qt.AlignRight)
        self.vBoxGlobal.setSpacing(8)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)# | QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.setMinimumSize(550, 850)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.pbLaunchCommand.clicked.connect(self.runCommandQueue)
        self.commandQueue.queueChanged.connect(self.validateLaunch)
        self.afCraftOptions.synthButtonLocator.positionPicked.connect(self.validateLaunch)
        self.wTitleBar.pbClose.clicked.connect(self.close)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.wCentralWidget = QtWidgets.QWidget(parent=self)

        self.wTitleBar = afKraftTitleBar.AfKraftTitleBar(parent=self)

        self.afCraftOptions = afKraftOptions.AfKraftOptions(parent=self)

        self.commandQueue = commandQueue.CommandQueue(parent=self)

        self.pbLaunchCommand = QtWidgets.QPushButton(parent=self)
        self.pbLaunchCommand.setObjectName('pbLaunchCommand')

        self.vBoxGlobal = QtWidgets.QVBoxLayout(self.wCentralWidget)
        self.vBoxGlobal.addWidget(self.wTitleBar)
        self.vBoxGlobal.addWidget(self.commandQueue)
        self.vBoxGlobal.addWidget(self.afCraftOptions)
        self.vBoxGlobal.addWidget(self.pbLaunchCommand)

        self.setObjectName('afCraftWindow')
        self.setCentralWidget(self.wCentralWidget)

    @QtCore.Slot()
    def validateLaunch(self):
        """ Check for the validity of the command queue so that afKraft can block the launch and any new commands
        should those conditions not be met.
        """

        queueIsValid = all([
            # self.commandQueue.commandQueueWidgets,
            self.afCraftOptions.synthButtonPosition()
        ])
        self.pbLaunchCommand.setEnabled(queueIsValid)

    @QtCore.Slot()
    def runCommandQueue(self):
        """ Start the command queue
        """

        self.commandQueue.synthButtonPos = self.afCraftOptions.synthButtonPosition()

        self.commandQueue.qtStartTimer.setInterval(self.afCraftOptions.delayTimer())
        self.commandQueue.qtStartTimer.start()

    #TODO This raises in its current state, check for a workaround
    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()
    #
    # def mouseMoveEvent(self, event):
    #     delta = QtCore.QPoint(event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()

if __name__ == '__main__':
    resonantQApp = QtWidgets.QApplication([])
    resonantApp = AfCraftWindow()
    resonantApp.show()
    sys.exit(resonantQApp.exec())
