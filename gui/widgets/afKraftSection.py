# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from PySide6 import QtWidgets

import afKraftResources


class AfKraftSection(QtWidgets.QFrame):
    """ Frame and label to contain various sections of AfKraft
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._setupUi()
        self._setupAppearance()

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """

        self.vBoxGlobal.setContentsMargins(6, 0, 6, 5)
        self.vBoxGlobal.setSpacing(2)

        self.setStyleSheet(afKraftResources.getStyleForWidget(self))
        self.titleLabel.setStyleSheet(afKraftResources.getStyleForWidget(self))

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        self.titleLabel = QtWidgets.QLabel(parent=self)
        self.titleLabel.setObjectName('titleLabel')

        self.vBoxGlobal = QtWidgets.QVBoxLayout()
        self.vBoxGlobal.addWidget(self.titleLabel)

        self.setLayout(self.vBoxGlobal)
        self.setObjectName('afKraftSection')

    def setTitle(self, newTitle):
        """ Sets this widget's label text to the supplied string

        :param newTitle: Which string we'll display
        :type newTitle: str
        """

        self.titleLabel.setText(newTitle)

    def addWidget(self, widget):
        """ Add the supplied widget to this widget's layout

        :param widget: Which widget we're adding
        :type widget: <class: QtWidgets.QWidget>
        """

        self.vBoxGlobal.addWidget(widget)

    def addLayout(self, layout):
        """ Add the supplied layout to this widget's layout

        :param layout: Which layout we'll be adding
        :type layout: <class: QtWidgets.QLayout>
        """

        self.vBoxGlobal.addLayout(layout)