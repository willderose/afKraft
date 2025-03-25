# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import afKraftResources


class MousePosPicker(QtWidgets.QPushButton):
    """ Used to track the cursor position to calibrate where the "Synthesize" button is in-game
    """

    positionPicked = QtCore.Signal()

    # The text to display when a user has yet to pick a position
    DEFAULT_TEXT = 'Pick {} button position'

    # The text to display when in the process of picking a position
    PICKING_TEXT = 'Return or Escape to pick position'

    # The text to display when a user has picked a position
    PICKED_TEXT = '{} button at {}'

    def __init__(self, targetButtonText, *args, **kwargs):
        """ Set our default values and properly initialise our widget

        :param targetButtonText: The text appearing in in-game buttons
        :type targetButtonText: str
        """
        super().__init__(*args, **kwargs)

        self._targetButtonText = targetButtonText
        self.pickedCursorPosition = None

        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.setText(self.DEFAULT_TEXT.format(self._targetButtonText))
        self.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.setFixedHeight(30)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.pressed.connect(self.onTrackingStarted)

    def keyPressEvent(self, keyEvent):
        """ Make sure we register the cursor position when return or escape are pressed
        """

        if keyEvent.key() == QtCore.Qt.Key_Escape or keyEvent.key() == QtCore.Qt.Key_Return:
            self.clearFocus()
            self.onTrackingEnded()

    def focusOutEvent(self, event):
        """ Adjust this button's test to better serve as a tutorial for a user
        """
        super().focusOutEvent(event)
        self.setText(self.DEFAULT_TEXT.format(self._targetButtonText))

    def onTrackingStarted(self):
        """ Adjust this button's test to better serve as a tutorial for a user
        """
        self.setText(self.PICKING_TEXT)

    def onTrackingEnded(self):
        """ Save the in-game button position to this widget for later use
        """

        currentCursorPosition = (QtGui.QCursor.pos().x(), QtGui.QCursor.pos().y())
        self.setText(self.PICKED_TEXT.format(self._targetButtonText, currentCursorPosition))
        self.pickedCursorPosition = currentCursorPosition
        self.positionPicked.emit()
