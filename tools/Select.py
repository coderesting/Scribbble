"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPen, QPainter, QMouseEvent, QColor, QPixmap

from Canvas import Canvas
from canvasElements.CanvasElement import CanvasElement
from toolSettings.ToolSettings import ToolSettings
from tools.Tool import Tool


class Select(Tool):
    """
    Select Tool
    Moves, changes and deletes elements in the canvas
    """

    def __init__(self, canvas: Canvas):
        super().__init__("Select", QIcon("icons/select.png"), Qt.Key_V)
        self.canvas = canvas

        self.current_selection: Optional[CanvasElement] = None
        # Store the last mouse position to calculate a movement delta
        self.last_pos = None
        self.active = False
        self.settings = None

    def configure_settings(self, settings: ToolSettings):
        # Store settings to change them according to the selected element
        self.settings = settings
        return settings.show_general_settings()

    def deactivate(self):
        self.current_selection = None
        self.last_pos = None
        self.active = False

    def mouse_press(self, event):
        self.current_selection = None
        for element in self.canvas.get_elements():
            if element.get_bounding_rect().contains(event.pos()):
                self.current_selection = element
                # Update the settings to show the selected element's settings
                self.settings.apply_pen(self.current_selection.get_pen())
        self.canvas.update()

    def mouse_move(self, event: QMouseEvent):
        if self.current_selection and event.buttons() == Qt.LeftButton and self.last_pos is not None:
            self.current_selection.move(event.pos() - self.last_pos)

        self.last_pos = event.pos()

    def key_press(self, event):
        # Use backspace instead of delete for macOS users
        if event.key() == Qt.Key_Backspace and self.current_selection is not None:
            self.canvas.remove_element(self.current_selection)
            self.current_selection = None
            self.canvas.update()

    def paint(self, painter: QPainter) -> None:
        # Material design blue 800 for good visibility
        painter.setPen(QPen(QColor("#1565C0")))
        if self.current_selection:
            rect = self.current_selection.get_bounding_rect()
            painter.drawRect(rect)
            # Draw movable icon to indicate dragging
            painter.drawPixmap(rect.center() - QPoint(20, 20), QPixmap("icons/movable.png"))

    def pen_change(self, pen):
        super(Select, self).pen_change(pen)
        # Apply changes made to the settings while an element is selected to the selected element
        if self.current_selection:
            self.current_selection.set_pen(pen)
