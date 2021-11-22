"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import Optional

from PyQt5.QtGui import QPen, QKeySequence
from PyQt5.QtWidgets import QWidget, QAction

from toolSettings.ToolSettings import ToolSettings


class Tool(QWidget):
    """
    Abstract class for a Tool.
    A tool has access to the pen property and can overwrite required methods.
    """

    def __init__(self, name, icon, shortcut_key):
        super().__init__()
        self.pen: Optional[QPen] = None

        # Create an action for the toolbox
        self.action = QAction()
        # Show name and keyboard shortcut as tooltip
        self.action.setText("{0} ({1})".format(name, QKeySequence(shortcut_key).toString()))
        self.action.setIcon(icon)

        self.shortcut_key = shortcut_key

    def pen_change(self, pen):
        self.pen = pen

    def get_action(self):
        return self.action

    def activate(self):
        pass

    def deactivate(self):
        pass

    def configure_settings(self, settings: ToolSettings):
        # Configure the settings to show general (line/curve) settings
        return settings.show_general_settings()

    def mouse_press(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_release(self, event):
        pass

    def key_press(self, event):
        pass

    def canvas_resize(self):
        pass

    def paint(self, painter):
        pass

    def get_shortcut_key(self):
        return self.shortcut_key
