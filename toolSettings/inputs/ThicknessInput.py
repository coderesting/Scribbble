"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtWidgets import QSpinBox


class ThicknessInput(QSpinBox):
    """
    Shows a spinbox for thickness with the suffix 'px'
    """

    def __init__(self):
        super().__init__()
        self.setValue(10)
        # prevent half pixel increments
        self.setSingleStep(1)
        self.setRange(1, 9999)
        self.setSuffix("px")
