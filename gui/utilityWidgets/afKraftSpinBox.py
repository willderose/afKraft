# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtCore
from PySide6 import QtWidgets

import afKraftResources


class AfKraftSpinBox(QtWidgets.QWidget):
    """ A Custom Spinbox to better imitate the 14 style
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._setupConnections()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.labTitle.setStyleSheet(afKraftResources.getStyleForWidget(self.labTitle))

        self.spbValue.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.spbValue.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spbValue.setMinimumWidth(85)
        self.spbValue.setFixedHeight(26)
        self.spbValue.setAlignment(QtCore.Qt.AlignCenter)

        self.pbAdd.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.pbAdd.setFixedSize(30, 28)
        self.pbAdd.setText('+')

        self.pbSubtract.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.pbSubtract.setFixedSize(30, 28)
        self.pbSubtract.setText('-')
        self.pbSubtract.setEnabled(False)

        self.hBoxGlobal.setContentsMargins(6, 0, 6, 0)
        self.hBoxGlobal.setAlignment(QtCore.Qt.AlignVCenter)
        self.hBoxGlobal.setSpacing(3)

    def _setupConnections(self):
        """ Connect this widget and its subwidgets' signals to their slots
        """

        self.pbAdd.clicked.connect(self.onValueAdded)

        self.pbSubtract.clicked.connect(self.onValueSubtracted)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.labTitle = QtWidgets.QLabel(parent=self)

        self.spbValue = QtWidgets.QSpinBox(parent=self)
        self.spbValue.setObjectName('spbValue')
        self.spbValue.setMinimum(0)
        self.spbValue.setMaximum(10000)

        self.pbAdd = QtWidgets.QPushButton(parent=self)

        self.pbSubtract = QtWidgets.QPushButton(parent=self)

        self.hBoxGlobal = QtWidgets.QHBoxLayout(self)
        self.hBoxGlobal.addWidget(self.labTitle)
        self.hBoxGlobal.addStretch()
        self.hBoxGlobal.addWidget(self.spbValue)
        self.hBoxGlobal.addWidget(self.pbAdd)
        self.hBoxGlobal.addWidget(self.pbSubtract)

    @QtCore.Slot()
    def onValueAdded(self):
        """ Adds 1 to the value of our spinbox
        """

        self.spbValue.setValue(self.spbValue.value() + self.spbValue.singleStep())

        self.pbSubtract.setEnabled(True)

    @QtCore.Slot()
    def onValueSubtracted(self):
        """ Remove 1 from the value of our spinbox
        """

        self.spbValue.setValue(self.spbValue.value() - self.spbValue.singleStep())

        if self.spbValue.value() == self.spbValue.minimum():
            self.pbSubtract.setEnabled(False)

    def setTitle(self, newTitle):
        """ Convenience method to set this widget's label's displayed text

        :param newTitle: Which text we're going to display
        :type newTitle: str
        """

        self.labTitle.setText(newTitle)

    def value(self):
        """ Convenience to allow higher level widgets easy access to this spinbox' value

        :return: The value of our QSpinBox
        :rtype: int
        """

        return self.spbValue.value()