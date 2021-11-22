"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QToolButton, QHBoxLayout, \
    QButtonGroup


class CapTypeInput(QWidget):
    """
    Shows a selection of three buttons to select the cap type (round, square and flat)

    :signal change: cap type changed
    """
    change = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Create a join_type_group to ensure only one button is active
        self.cap_type_group = QButtonGroup(self)

        round_button = QToolButton()
        # Set the data attribute to associate it later on click
        round_button.data = Qt.RoundCap
        round_button.setToolTip('Round')
        round_button.setIcon(QIcon("icons/lineCapRound.png"))
        round_button.setCheckable(True)
        self.cap_type_group.addButton(round_button)
        # Select the round cap type because it is the one users probably expect
        round_button.setChecked(True)

        square_button = QToolButton()
        square_button.data = Qt.SquareCap
        square_button.setToolTip("Square")
        square_button.setIcon(QIcon("icons/lineCapSquare.png"))
        square_button.setCheckable(True)
        self.cap_type_group.addButton(square_button)

        flat_button = QToolButton()
        flat_button.data = Qt.FlatCap
        flat_button.setToolTip("Flat")
        flat_button.setIcon(QIcon("icons/lineCapFlat.png"))
        flat_button.setCheckable(True)
        self.cap_type_group.addButton(flat_button)

        # Forward the change event
        self.cap_type_group.buttonToggled.connect(self.change.emit)
        self.cap_type_group.buttonToggled.connect(lambda e: print(e))

        h_box = QHBoxLayout()
        h_box.addWidget(round_button)
        h_box.addWidget(square_button)
        h_box.addWidget(flat_button)
        h_box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h_box)

    def get_cap_type(self):
        return self.cap_type_group.checkedButton().data

    def set_cap_type(self, cap_type):
        for button in self.cap_type_group.buttons():
            if button.data == cap_type:
                button.setChecked(True)
