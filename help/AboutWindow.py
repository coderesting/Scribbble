"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout


class AboutWindow(QDialog):
    """
    Shows information about the Scribbble application
    """

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        # Prevent the window from being in the background
        self.setModal(True)
        self.setWindowTitle("About Scribbble")
        self.setWindowIcon(QIcon("icons/app.png"))

        about_layout = QHBoxLayout()

        app_image = QLabel()
        app_image.setPixmap(QPixmap("icons/app.png"))
        app_image.setAlignment(Qt.AlignTop)
        about_layout.addWidget(app_image)

        info_layout = QVBoxLayout()

        name_label = QLabel("Scribbble v1.0")
        name_label.setStyleSheet("font-size:20px")
        info_layout.addWidget(name_label)

        developer_label = QLabel("Designed and developed by Yannick Brandt")
        info_layout.addWidget(developer_label)

        description_label = QLabel("""Scribbble is a small student project designed and developed for an assignment \
at Griffith College Dublin. It resembles a rudimentary drawing application using pyQT. 
Basic tools like move/select/brush/pen and fill are available.
        """)
        description_label.setWordWrap(True)
        info_layout.addWidget(description_label)
        info_layout.setSpacing(10)
        info_layout.addStretch()

        about_layout.addLayout(info_layout)
        about_layout.setSpacing(10)
        about_layout.addStretch()

        self.setLayout(about_layout)

        # Fix the window size to the minimum size
        self.setFixedSize(self.sizeHint())
