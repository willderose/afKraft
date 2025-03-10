# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

import datetime

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import afKraftResources


class CraftProgBar(QtWidgets.QFrame):
    """ Simple progress bar to show the progress of a craft
    """

    craftPaused = QtCore.Signal()

    craftResumed = QtCore.Signal()

    craftCanceled = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.totalCraftTime = None

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.labProgressIcon.setPixmap(QtGui.QPixmap(afKraftResources.getIconPathFromFileName('craftIcon.png')))

        self.hBoxProgressTitle.setContentsMargins(3, 3, 0, 8)

        self.fProgressTitle.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)

        self.labTimeRemainingTitle.setText('Remaining Time')

        self.labRemainingTime.setAlignment(QtCore.Qt.AlignRight)

        self.vBoxProgressTime.setAlignment(QtCore.Qt.AlignVCenter)

        self.wProgressTime.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)

        self.prbProgress.setTextVisible(False)
        self.prbProgress.setMaximumHeight(18)

        self.pbPauseCommand.setText('Pause')
        self.pbPauseCommand.setFixedSize(85, 28)
        self.pbPauseCommand.setStyleSheet(afKraftResources.getStyleForWidget(self.pbPauseCommand))

        self.pbResumeCommand.setText('Resume')
        self.pbResumeCommand.setFixedSize(85, 28)
        self.pbResumeCommand.setStyleSheet(afKraftResources.getStyleForWidget(self.pbResumeCommand))
        self.pbResumeCommand.setVisible(False)

        self.pbCancelCommand.setText('Cancel')
        self.pbCancelCommand.setFixedSize(85, 28)
        self.pbCancelCommand.setStyleSheet(afKraftResources.getStyleForWidget(self.pbCancelCommand))

        self.vBoxProgBarActions.setContentsMargins(12, 20, 12, 0)

        self.hBoxProgressInfo.setContentsMargins(0, 0, 0, 0)

        self.hBoxProgressActions.setAlignment(QtCore.Qt.AlignRight)
        self.hBoxProgressActions.setContentsMargins(0, 0, 0, 0)

        self.labProgressCount.setAlignment(QtCore.Qt.AlignBottom)

        self.vBoxGlobal.setSpacing(0)
        self.vBoxGlobal.setContentsMargins(0, 0, 0, 0)

        self.setStyleSheet(afKraftResources.getStyleForWidget(self))

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.pbPauseCommand.clicked.connect(self.craftPaused.emit)
        self.pbPauseCommand.clicked.connect(self.onCraftPaused)

        self.pbResumeCommand.clicked.connect(self.craftResumed.emit)
        self.pbResumeCommand.clicked.connect(self.onCraftResumed)

        self.pbCancelCommand.clicked.connect(self.craftCanceled.emit)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.labProgressIcon = QtWidgets.QLabel(parent=self)

        self.labProgressTitle = QtWidgets.QLabel(parent=self)
        self.labProgressTitle.setObjectName('labProgressTitle')

        self.labProgressCount = QtWidgets.QLabel(parent=self)
        self.labProgressCount.setObjectName('labProgressCount')

        self.hBoxProgressTitle = QtWidgets.QHBoxLayout()
        self.hBoxProgressTitle.addWidget(self.labProgressIcon)
        self.hBoxProgressTitle.addWidget(self.labProgressTitle)
        self.hBoxProgressTitle.addStretch()
        self.hBoxProgressTitle.addWidget(self.labProgressCount)

        self.fProgressTitle = QtWidgets.QFrame(parent=self)
        self.fProgressTitle.setLayout(self.hBoxProgressTitle)
        self.fProgressTitle.setObjectName('fProgressTitle')

        self.labTimeRemainingTitle = QtWidgets.QLabel(parent=self)
        self.labTimeRemainingTitle.setObjectName('labTimeRemainingTitle')

        self.labRemainingTime = QtWidgets.QLabel(parent=self)
        self.labRemainingTime.setObjectName('labRemainingTime')

        self.vBoxProgressTime = QtWidgets.QVBoxLayout()
        self.vBoxProgressTime.addWidget(self.labTimeRemainingTitle)
        self.vBoxProgressTime.addWidget(self.labRemainingTime)

        self.wProgressTime = QtWidgets.QWidget()
        self.wProgressTime.setLayout(self.vBoxProgressTime)
        self.wProgressTime.setObjectName('wProgressTime')

        self.pbPauseCommand = QtWidgets.QPushButton(parent=self)

        self.pbCancelCommand = QtWidgets.QPushButton(parent=self)

        self.pbResumeCommand = QtWidgets.QPushButton(parent=self)

        self.hBoxProgressActions = QtWidgets.QHBoxLayout()
        self.hBoxProgressActions.addWidget(self.pbPauseCommand)
        self.hBoxProgressActions.addWidget(self.pbResumeCommand)
        self.hBoxProgressActions.addWidget(self.pbCancelCommand)

        self.prbProgress = QtWidgets.QProgressBar(parent=self)

        self.vBoxProgBarActions = QtWidgets.QVBoxLayout()
        self.vBoxProgBarActions.addWidget(self.prbProgress)
        self.vBoxProgBarActions.addLayout(self.hBoxProgressActions)

        self.hBoxProgressInfo = QtWidgets.QHBoxLayout()
        self.hBoxProgressInfo.addWidget(self.wProgressTime)
        self.hBoxProgressInfo.addLayout(self.vBoxProgBarActions)

        self.vBoxGlobal = QtWidgets.QVBoxLayout()
        self.vBoxGlobal.addWidget(self.fProgressTitle)
        self.vBoxGlobal.addLayout(self.hBoxProgressInfo)

        self.setLayout(self.vBoxGlobal)
        self.setObjectName('craftProgBar')

    def setCraftingData(self, craftName, craftAmount, totalCraftTime):
        """ Prepare the progress bar info with the supplied data

        :param craftName: What name we're going to display
        :type craftName: str

        :param craftAmount: How many items we're going to be crafting
        :type craftAmount: int

        :param totalCraftTime: How much time the entirety of the craft is estimated to take (in seconds)
        :type totalCraftTime: int
        """

        self.labProgressTitle.setText(craftName or 'Unknown')
        self.prbProgress.setMinimum(1)
        self.prbProgress.setMaximum(craftAmount)
        self.totalCraftTime = totalCraftTime
        self.setRemainingCraftTime(totalCraftTime)

    def setRemainingCraftTime(self, timeRemaining):
        """ Set the remaining time estimate's text

        :param timeRemaining: The remaining time, in seconds
        :type timeRemaining: int
        """

        self.labRemainingTime.setText(str(datetime.timedelta(seconds=timeRemaining)).split('.')[0])

    def setProgress(self, progressValue):
        """ Update the progress bar and the accompanying widgets

        :param progressValue: The new progress value we're going to display
        :type progressValue: int
        """

        self.prbProgress.setValue(progressValue)
        self.labProgressCount.setText('{}/{} '.format(progressValue, self.prbProgress.maximum()))
        self.setRemainingCraftTime(
            self.totalCraftTime - ((self.totalCraftTime / self.prbProgress.maximum()) * self.prbProgress.value())
        )

    @QtCore.Slot()
    def onCraftPaused(self):
        """ Hide the Pause button and show the Resume button
        """

        self.pbPauseCommand.setVisible(False)
        self.pbResumeCommand.setVisible(True)

    @QtCore.Slot()
    def onCraftResumed(self):
        """ Hide the Resume button and show the Pause button
        """

        self.pbPauseCommand.setVisible(True)
        self.pbResumeCommand.setVisible(False)