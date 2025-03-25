# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from gui.utilityWidgets import afKraftSpinBox, mousePosPicker, afKraftSection


class AfKraftOptions(afKraftSection.AfKraftSection):
    """ Option container for AfKraft
    """

    def _setupAppearance(self):
        """ Visually customize this widget and it's subwidgets
        """
        super()._setupAppearance()

        self.synthButtonLocator.setFixedHeight(48)

        self.setTitle('Options')

        self.delayOptions.setTitle('Startup delay (ms):')
        self.delayOptions.spbValue.setSingleStep(100)

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