"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QToolBar, QActionGroup

from toolSettings.ToolSettings import ToolSettings
from tools.Brush import Brush
from tools.Fill import Fill
from tools.Move import Move
from tools.Pen import Pen
from tools.Select import Select


class Toolbox(QToolBar):
    select_tool = pyqtSignal(object)

    def __init__(self, canvas, tool_settings: ToolSettings):
        super().__init__()
        self.canvas = canvas
        self.tool_settings = tool_settings

        self.active_tool = None
        self.tools = [Move(canvas), Select(canvas), Brush(canvas), Pen(canvas), Fill(canvas)]

        # Notify the active tool about a change in settings
        self.tool_settings.pen_change.connect(lambda pen: self.active_tool.pen_change(pen))

        # Notify the active tool about mouse events
        self.canvas.mouse_press.connect(lambda evt: self.active_tool.mouse_press(evt))
        self.canvas.mouse_move.connect(lambda evt: self.active_tool.mouse_move(evt))
        self.canvas.mouse_release.connect(lambda evt: self.active_tool.mouse_release(evt))
        # Notify the active tool about canvas resize
        self.canvas.resize.connect(lambda: self.active_tool.canvas_resize())

        # Steal the focus from the thickness spinbox when the user clicks on the canvas
        self.canvas.mouse_press.connect(self.setFocus)

        # Create an action join_type_group to only allow one tool to be active
        action_group = QActionGroup(self)

        for tool in self.tools:
            # include the tool (t) in the lambdas' closure (needed because the loop has no separated closure)
            def lambda_generator(t):
                return lambda: self.set_active_tool(t)

            action = tool.get_action()
            action.setCheckable(True)
            action.setActionGroup(action_group)
            action.triggered.connect(lambda_generator(tool))
            action.setShortcut(QKeySequence(tool.get_shortcut_key()))
            self.addAction(action)

        # Activate the paint brush by default because it is the most intuitive tool
        self.tools[2].get_action().trigger()

    def set_active_tool(self, new_tool):
        """ Sets a new tool as active tool and deactivates the old tool
        :param new_tool: new active tool
        """
        if self.active_tool:
            self.active_tool.deactivate()

        self.active_tool = new_tool
        self.active_tool.configure_settings(self.tool_settings)
        self.tool_settings.update_pen()
        self.active_tool.activate()
        self.canvas.set_active_tool(self.active_tool)
