# -----------------------------------------------------------#
# Created by willderose                                      #
# -----------------------------------------------------------#

from gui.widgets import keybindSelector

import afKraftCommands


class SingleCommandOptions(keybindSelector.KeybindSelector):
    """ Convenience widget to route the command to the proper function in the command list
    """

    def runCommand(self, *args, **kwargs):
        """ Trigger the job change keybind
        """

        afKraftCommands.runKeybind(self.keySequence())