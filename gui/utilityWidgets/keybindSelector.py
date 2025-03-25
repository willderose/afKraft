# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtWidgets

import afKraftResources


class KeybindSelector(QtWidgets.QKeySequenceEdit):
    """ UX oriented layer for the QKeySequenceEdit widget.
    """

    # The text to display when this widget is fresh
    DEFAULT_TEXT = '{} keybind'

    # The text to display when this widget is accepting inputs
    AWAITING_TEXT = 'Awaiting input...'

    def __init__(self, keybindTarget, *args, **kwargs):
        """ Initialise the necessary variables for this widget

        :param keybindTarget: What the purpose of this keybind is going to be
        :type keybindTarget: str
        """
        super().__init__(*args, **kwargs)

        self._keybindTarget = keybindTarget

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.liEdMacroKeybind.setPlaceholderText(self.DEFAULT_TEXT.format(self._keybindTarget))
        self.liEdMacroKeybind.setStyleSheet(afKraftResources.getStyleForWidget(self.liEdMacroKeybind))
        self.liEdMacroKeybind.setFixedHeight(30)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.liEdMacroKeybind = self.findChild(QtWidgets.QLineEdit, 'qt_keysequenceedit_lineedit')
        self.setMaximumSequenceLength(1)

    def focusInEvent(self, event):
        super().focusInEvent(event)

        self.clear()
        self.liEdMacroKeybind.setPlaceholderText(self.AWAITING_TEXT)

    def focusOutEvent(self, event):
        super().focusInEvent(event)

        self.liEdMacroKeybind.setPlaceholderText(self.DEFAULT_TEXT.format(self._keybindTarget))
