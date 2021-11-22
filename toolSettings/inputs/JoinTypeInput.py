"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QToolButton, QButtonGroup, QHBoxLayout


class JoinTypeInput(QWidget):
    """
    Shows a selection of three buttons to select the join type (round, bevel and miter)

    :signal change: join type changed
    """
    change = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        # Create a join_type_group to ensure only one button is active
        self.join_type_group = QButtonGroup(self)

        round_button = QToolButton()
        # Set the data attribute to associate it later on click
        round_button.data = Qt.RoundJoin
        round_button.setToolTip("Round")
        round_button.setIcon(QIcon("icons/lineJoinRound.png"))
        round_button.setCheckable(True)
        self.join_type_group.addButton(round_button)
        # Select the round join type because it is the one users probably expect
        round_button.setChecked(True)

        bevel_button = QToolButton()
        bevel_button.data = Qt.BevelJoin
        bevel_button.setToolTip("Bevel")
        bevel_button.setIcon(QIcon("icons/lineJoinBevel.png"))
        bevel_button.setCheckable(True)
        self.join_type_group.addButton(bevel_button)

        miter_button = QToolButton()
        miter_button.data = Qt.MiterJoin
        miter_button.setToolTip("Miter")
        miter_button.setIcon(QIcon("icons/lineJoinMiter.png"))
        miter_button.setCheckable(True)
        self.join_type_group.addButton(miter_button)

        # Forward the change event
        self.join_type_group.buttonToggled.connect(self.change.emit)

        h_box = QHBoxLayout()
        h_box.addWidget(round_button)
        h_box.addWidget(bevel_button)
        h_box.addWidget(miter_button)
        h_box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(h_box)

    def get_join_type(self):
        return self.join_type_group.checkedButton().data

    def set_join_type(self, join_type):
        for button in self.join_type_group.buttons():
            if button.data == join_type:
                button.setChecked(True)
