# -----------------------------------------------------------#
# Created by William Desrosiers                              #
# -----------------------------------------------------------#
import os

from PySide6 import QtGui


def getIconPathFromFileName(fileName):
    """ Create a QIcon from the supplied file name

    :param fileName: The name of the file we're going to create an QIcon for
    :type fileName: str

    :return: A QIcon instance representing the file
    :rtype: <class: QtWidgets.QIcon>
    """

    return os.path.join(os.path.dirname(__file__), 'icons', fileName)


def getStyleForWidget(widget):
    """ Get the appropriate styleSheet for the supplied widget. Start by querying the widget's objectName, then its type

    :param widget: Which widget this function will query the style for
    :type widget: <class: QtWidgets.QWidget>

    :return: The found styleSheet string
    :rtype: str
    """

    styleSheetsRoot = os.path.join(os.path.dirname(__file__), 'styleSheets')

    widgetNameStyleFile = os.path.join(styleSheetsRoot, '{}.qss'.format(widget.objectName()))
    widgetTypeStyleFile = os.path.join(styleSheetsRoot, '{}.qss'.format(widget.__class__.__name__))
    widgetBaseTypeStyleFile = os.path.join(styleSheetsRoot, '{}.qss'.format(widget.__class__.__bases__[0].__name__))

    targetStyleFile = None
    if os.path.isfile(widgetNameStyleFile):
        targetStyleFile = widgetNameStyleFile

    elif os.path.isfile(widgetTypeStyleFile):
        targetStyleFile = widgetTypeStyleFile

    elif os.path.isfile(widgetBaseTypeStyleFile):
        targetStyleFile = widgetBaseTypeStyleFile

    if targetStyleFile is None:
        return ''

    with open(targetStyleFile, 'r') as styleFileBuffer:
        return styleFileBuffer.read()


ICON_CLOSE = getIconPathFromFileName('mycrelicclose_hr1.png')