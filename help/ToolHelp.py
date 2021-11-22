"""
Name: Yannick Brandt
Student number: 3077620
"""
from PyQt5.QtWidgets import QWidget, QLabel, QFormLayout, QGridLayout, QHBoxLayout, QVBoxLayout, QGroupBox


class ToolHelp(QWidget):
    """
        Shows help information for a single tool
    """

    def __init__(self, icon, title, description, movie, keys):
        super().__init__()

        help_layout = QGridLayout()

        info_layout = QVBoxLayout()

        # title with icon and title
        header_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(icon)
        header_layout.addWidget(icon_label)
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size:16px")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        info_layout.addLayout(header_layout)

        description_label = QLabel(description)
        description_label.setContentsMargins(0, 20, 20, 20)
        description_label.setWordWrap(True)
        info_layout.addWidget(description_label)
        info_layout.addStretch()
        help_layout.addLayout(info_layout, 0, 0)

        video_label = QLabel()
        video_label.setMovie(movie)
        movie.start()
        help_layout.addWidget(video_label, 1, 0, 1, 2)

        keys_group = QGroupBox("Keyboard shortcuts")
        keys_layout = QFormLayout()
        for key in keys:
            keys_layout.addRow(key[0], QLabel(key[1]))
        keys_group.setLayout(keys_layout)

        help_layout.addWidget(keys_group, 0, 1)
        self.setLayout(help_layout)
