"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QLabel, QToolBar, QWidget, QSizePolicy

from toolSettings.inputs.CapTypeInput import CapTypeInput
from toolSettings.inputs.ColorInput import ColorInput
from toolSettings.inputs.JoinTypeInput import JoinTypeInput
from toolSettings.inputs.LineTypeInput import LineTypeInput
from toolSettings.inputs.ThicknessInput import ThicknessInput


class ToolSettings(QToolBar):
    """
    Shows a toolbar with all kinds off settings and info about the selected tool and canvas.
    use the methods show_x to only show a selection of settings for specific tools.

    :signal pen_change(QPen): at least one of the settings changed
    """
    pen_change = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        # Add spacing between and around the toolbar items
        self.setStyleSheet("QToolBar{spacing:8px; padding: 7px}")

        # Create labels, actions and connections to the update_pen method
        self.size = QLabel("?")

        self.color_input = ColorInput(self)
        self.color_input.change.connect(self.update_pen)

        self.thickness_input = ThicknessInput()
        self.thickness_input.valueChanged.connect(self.update_pen)

        self.line_type_input = LineTypeInput()
        self.line_type_input.currentTextChanged.connect(self.update_pen)

        self.cap_type_input = CapTypeInput()
        self.cap_type_input.change.connect(self.update_pen)

        self.join_type_input = JoinTypeInput()
        self.join_type_input.change.connect(self.update_pen)

        self.size_label = self.addWidget(QLabel("Size:"))
        self.size_action = self.addWidget(self.size)
        self.size_spacer = self.addSeparator()

        self.color_label = self.addWidget(QLabel("Color:"))
        self.color_action = self.addWidget(self.color_input)
        self.color_spacer = self.addSeparator()

        self.thickness_label = self.addWidget(QLabel("Thickness:"))
        self.thickness_action = self.addWidget(self.thickness_input)
        self.thickness_spacer = self.addSeparator()

        self.line_type_label = self.addWidget(QLabel("Type:"))
        self.line_type_action = self.addWidget(self.line_type_input)
        self.line_type_spacer = self.addSeparator()

        self.cap_type_label = self.addWidget(QLabel("Cap:"))
        self.cap_type_action = self.addWidget(self.cap_type_input)
        self.cap_type_spacer = self.addSeparator()

        self.join_type_label = self.addWidget(QLabel("Join:"))
        self.join_type_action = self.addWidget(self.join_type_input)

        # Spacer at the end to prevent stretching of the existing items
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(spacer)

    def show_general_settings(self):
        """Shows settings for lines and curves"""
        self.hide_all_settings()
        self.color_label.setVisible(True)
        self.color_action.setVisible(True)
        self.color_spacer.setVisible(True)

        self.thickness_label.setVisible(True)
        self.thickness_action.setVisible(True)
        self.thickness_spacer.setVisible(True)

        self.line_type_label.setVisible(True)
        self.line_type_action.setVisible(True)
        self.line_type_spacer.setVisible(True)

        self.cap_type_label.setVisible(True)
        self.cap_type_action.setVisible(True)
        self.cap_type_spacer.setVisible(True)

        self.join_type_label.setVisible(True)
        self.join_type_action.setVisible(True)

    def show_fill_settings(self):
        self.hide_all_settings()
        self.color_label.setVisible(True)
        self.color_action.setVisible(True)

    def show_move_settings(self):
        self.hide_all_settings()
        self.size_label.setVisible(True)
        self.size_action.setVisible(True)

    def hide_all_settings(self):
        self.size_label.setVisible(False)
        self.size_action.setVisible(False)
        self.size_spacer.setVisible(False)

        self.color_label.setVisible(False)
        self.color_action.setVisible(False)
        self.color_spacer.setVisible(False)

        self.thickness_label.setVisible(False)
        self.thickness_action.setVisible(False)
        self.thickness_spacer.setVisible(False)

        self.line_type_label.setVisible(False)
        self.line_type_action.setVisible(False)
        self.line_type_spacer.setVisible(False)

        self.cap_type_label.setVisible(False)
        self.cap_type_action.setVisible(False)
        self.cap_type_spacer.setVisible(False)

        self.join_type_label.setVisible(False)
        self.join_type_action.setVisible(False)

    def apply_pen(self, pen: QPen):
        """uses a pen to update the displayed settings

        :param pen: pen to use settings from
        """
        self.color_input.set_color(pen.color())
        self.thickness_input.setValue(pen.width())
        self.line_type_input.set_line_type(pen.style())
        self.cap_type_input.set_cap_type(pen.capStyle())
        self.join_type_input.set_join_type(pen.joinStyle())

    def update_pen(self):
        color = self.color_input.get_color()
        thickness = self.thickness_input.value()
        line_type = self.line_type_input.currentData()
        cap_type = self.cap_type_input.get_cap_type()
        join_type = self.join_type_input.get_join_type()

        pen = QPen(color, thickness, line_type, cap_type, join_type)
        self.pen_change.emit(pen)


def pen_to_json(pen: QPen):
    """ Helper method to convert a QPen into a json serializable representation of a pen

    :param pen: pen to convert
    """
    return {
        "color": pen.color().name(),
        "thickness": pen.width(),
        "line_type": pen.style(),
        "cap_type": pen.capStyle(),
        "join_type": pen.joinStyle()
    }


def pen_from_json(json_pen):
    """ Helper method to convert a json serializable representation of a pen into a QPen

    :param json_pen: json pen to convert
    """
    return QPen(QPen(QColor(json_pen['color']), json_pen['thickness'], json_pen['line_type'], json_pen['cap_type'],
                     json_pen['join_type']))
