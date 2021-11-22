"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog, QToolButton


class ColorInput(QToolButton):
    """
    Shows a colored circle button with a color picker when clicked.

    :signal change: color changed
    """

    change = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

        self.current_color = None

        self.color_picker = QColorDialog(parent)
        self.color_picker.setModal(True)
        self.color_picker.colorSelected.connect(self.set_color)

        self.clicked.connect(self.open_color_picker)

        # Make the button square
        self.setMaximumWidth(20)
        self.setMaximumHeight(20)

        # indicate a clickable area by changing the cursor
        self.setCursor(Qt.PointingHandCursor)

        # Scribbble app orange as default
        self.set_color(QColor('#FF6F00'))

    def open_color_picker(self):
        self.color_picker.setCurrentColor(self.current_color)
        self.color_picker.open()

    def set_color(self, color: QColor):
        self.current_color = color
        # update the color picker
        self.color_picker.setCurrentColor(color)
        # update the buttons background
        self.setStyleSheet("background-color: " + color.name() + "; border-radius:10px")
        self.change.emit()

    def get_color(self):
        return self.color_picker.currentColor()
