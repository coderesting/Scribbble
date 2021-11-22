"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPen, QPainter, QMouseEvent

from canvasElements.Line import Line
from tools.Tool import Tool


class Brush(Tool):
    """
    Brush Tool
    Creates line from mouse positions
    """

    def __init__(self, canvas):
        super().__init__("Brush", QIcon("icons/brush.png"), Qt.Key_B)
        self.canvas = canvas

        # Store the currently drawn line
        self.current_line: Optional[Line] = None

        # Store the preview position to display a brush preview circle
        self.preview_pos: Optional[QPoint] = None

    def activate(self):
        # Hide the default cursor to draw a preview of the brush size on the canvas
        self.canvas.setCursor(Qt.BlankCursor)

    def deactivate(self):
        self.canvas.unsetCursor()
        self.current_line = None
        self.preview_pos = None

    def mouse_press(self, event):
        # Create a new line and add it to the canvas
        self.current_line = Line(self.pen)
        self.current_line.add_point(event.pos())
        self.canvas.add_element(self.current_line)

    def mouse_move(self, event: QMouseEvent):
        if self.current_line:
            self.current_line.add_point(event.pos())

        self.preview_pos = event.pos()
        # Update the canvas to show the preview point
        self.canvas.update()

    def mouse_release(self, event):
        self.current_line = None

    def paint(self, painter: QPainter):
        if self.preview_pos:
            # Draw a preview point with a black and white outline to make it visible on all backgrounds
            painter.setPen(QPen(Qt.black))
            painter.drawEllipse(self.preview_pos, self.pen.width() / 2, self.pen.width() / 2)
            painter.setPen(QPen(Qt.white))
            painter.drawEllipse(self.preview_pos, self.pen.width() / 2 + 1, self.pen.width() / 2 + 1)
