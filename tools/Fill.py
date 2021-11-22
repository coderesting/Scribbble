"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor, QPixmap

from Canvas import Canvas
from toolSettings.ToolSettings import ToolSettings
from tools.Tool import Tool


class Fill(Tool):
    """
    Fill Tool
    Fills the background on click with the specified color
    """

    def __init__(self, canvas: Canvas):
        super().__init__("Fill Background", QIcon("icons/fill.png"), Qt.Key_F)
        self.canvas = canvas

        self.cursor = QCursor(QPixmap('icons/fill.png'))

    def configure_settings(self, settings: ToolSettings):
        # Configure the settings to show fill settings
        return settings.show_fill_settings()

    def activate(self):
        # Set the cursor to a fill icon
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.canvas.unsetCursor()

    def mouse_press(self, event):
        self.canvas.set_background(self.pen.color())
