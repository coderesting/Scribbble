"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox


class LineTypeInput(QComboBox):
    """
    Shows a drop down menu with different line types
    """

    def __init__(self):
        super().__init__()

        # After hours of research and failed attempts, I came to the conclusion that it is very hard to create
        # a dropdown where the items have no text and an image as background.
        # Even a custom menu as dropdown seems not plausible.
        # The line types are now represented by text. This seems fine for now.
        self.addItem("─────────", Qt.SolidLine)
        self.addItem("—  —  —  — ", Qt.DashLine)
        self.addItem("·  ·  ·  ·  ·", Qt.DotLine)
        self.addItem("— · — · — ·", Qt.DashDotLine)
        self.addItem("— · · — · —", Qt.DashDotDotLine)
        # Comic Sans because it's available on macOS and Windows and represents the line type pretty well
        self.setFont(QFont("Comic Sans MS", 9, QFont.Bold))

    def set_line_type(self, line_type):
        index = self.findData(line_type)
        self.setCurrentIndex(index)
