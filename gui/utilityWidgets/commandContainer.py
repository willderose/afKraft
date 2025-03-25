# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtCore
from PySide6 import QtWidgets

import afKraftResources


class CommandContainer(QtWidgets.QFrame):
    """ Shared parent widget of all commands we can add to the command queue
    """

    commandRemoved = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, commandType, *args, **kwargs):
        """ Initialises the widget with the supplied args

        :param commandType: The type of command we're going to use as this widget's title
        :type commandType: str
        """
        super().__init__(*args, **kwargs)

        self.commandType = commandType
        self.commandWidget = None

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.containerLabel.setText(self.commandType)

        self.pbRemove.setFixedSize(22, 22)
        self.pbRemove.setText('X')
        self.pbRemove.setFlat(True)

        self.hBoxTitleBar.setContentsMargins(0, 0, 0, 0)

        self.vBoxGlobal.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(afKraftResources.getStyleForWidget(self))

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.pbRemove.clicked.connect(self.onCommandRemoved)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.containerLabel = QtWidgets.QLabel(parent=self)
        self.containerLabel.setObjectName('containerLabel')

        self.pbRemove = QtWidgets.QPushButton(parent=self)
        self.pbRemove.setObjectName('pbRemove')

        self.hBoxTitleBar = QtWidgets.QHBoxLayout()
        self.hBoxTitleBar.addWidget(self.containerLabel)
        self.hBoxTitleBar.addWidget(self.pbRemove)

        self.vBoxGlobal = QtWidgets.QVBoxLayout()
        self.vBoxGlobal.addLayout(self.hBoxTitleBar)

        self.setLayout(self.vBoxGlobal)
        self.setObjectName('commandContainer')

    def addWidget(self, widgetToAdd):
        """ Add a widget to this group box' layout
        """

        self.commandWidget = widgetToAdd
        self.vBoxGlobal.addWidget(widgetToAdd)

    def onCommandRemoved(self):
        self.commandRemoved.emit(self)