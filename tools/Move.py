"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QMouseEvent

from Canvas import Canvas
from toolSettings.ToolSettings import ToolSettings
from tools.Tool import Tool


class Move(Tool):
    """
    Move Tool
    Moves all items in the canvas
    """

    def __init__(self, canvas: Canvas):
        super().__init__("Move", QIcon("icons/move.png"), Qt.Key_M)
        self.canvas = canvas

        # Store last mouse position to calculate movement delta
        self.last_pos = None

        # Store the settings to display the size of the canvas
        self.settings = None

    def configure_settings(self, settings: ToolSettings):
        self.settings = settings
        self.canvas_resize()
        # Configure the settings to show move settings
        settings.show_move_settings()

    def canvas_resize(self):
        # Update the displayed size of the canvas in settings
        self.settings.size.setText("{0} x {1}px".format(self.canvas.size().width(), self.canvas.size().height()))

    def activate(self):
        self.canvas.setCursor(Qt.OpenHandCursor)

    def deactivate(self):
        self.canvas.unsetCursor()
        self.last_pos = None

    def mouse_press(self, event):
        # Show a grabbing hand on mouse down
        self.canvas.setCursor(Qt.ClosedHandCursor)

    def mouse_move(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.last_pos:
            for element in self.canvas.get_elements():
                element.move(event.pos() - self.last_pos)

        self.last_pos = event.pos()

    def mouse_release(self, event):
        # Show a released hand on mouse release
        self.canvas.setCursor(Qt.OpenHandCursor)
