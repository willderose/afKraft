# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from gui.widgets import afKraftSection
from gui.widgets import mousePosPicker
from gui.widgets import afKraftSpinBox


class GlobalOptions(afKraftSection.AfKraftSection):
    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """
        super()._setupAppearance()

        self.synthButtonLocator.setMinimumHeight(48)

        self.setTitle('Global Options')

        self.delayOptions.setTitle('Startup delay, in milliseconds:')

    def _setupUi(self):
        """ Create and lay out this widget's subwidgets
        """

        super()._setupUi()

        self.synthButtonLocator = mousePosPicker.MousePosPicker(targetButtonText='Synthesize', parent=self)
        self.synthButtonLocator.setObjectName('synthButtonLocator')

        self.delayOptions = afKraftSpinBox.AfKraftSpinBox(parent=self)

        self.addWidget(self.synthButtonLocator)
        self.addWidget(self.delayOptions)

    def synthButtonPosition(self):
        """ Wrapper to allow higher level widgets easy access to the position picked as the Synthesis button position
        """

        return self.synthButtonLocator.pickedCursorPosition

    def delayTimer(self):
        """ Wrapper to allow higher level widgets easy access to the user's chosen delay timer

        :return: The delay widget's spinbox value
        :rtype: int
        """

        return self.delayOptions.value()