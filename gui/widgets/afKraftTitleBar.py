# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

import afKraftResources


class AfKraftTitleBar(QtWidgets.QWidget):
    """ AfKraft's window title bar, simply to imitate 14's style better than the OS' defaults
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.labTitle.setText('Af Kraft')

        self.pbClose.setIcon(QtGui.QIcon(afKraftResources.ICON_CLOSE))
        self.pbClose.setFixedSize(40, 40)
        self.pbClose.setIconSize(QtCore.QSize(48, 48))
        self.pbClose.setFlat(True)

        self.hBoxTitle.setContentsMargins(0, 0, 0, 0)

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.labTitle = QtWidgets.QLabel(parent=self)
        self.labTitle.setObjectName('afCraftTitle')

        self.pbClose = QtWidgets.QPushButton(parent=self)
        self.pbClose.setObjectName('pbClose')

        self.hBoxTitle = QtWidgets.QHBoxLayout(self)
        self.hBoxTitle.addWidget(self.labTitle)
        self.hBoxTitle.addWidget(self.pbClose)
