"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import List

from PyQt5.QtCore import pyqtSignal, QPoint
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QWidget

from canvasElements.CanvasElement import CanvasElement, point_from_json, point_to_json
from toolSettings.ToolSettings import pen_to_json


class Curve(CanvasElement):
    """
    A canvas element to show a curve consisting of multiple anchor points with handles
    """

    def __init__(self, pen):
        super().__init__(pen)
        self.anchor_points: List[AnchorPoint] = []

    def add_anchor_point(self, anchor_point):
        """
        :param anchor_point: anchor point to add
        """
        anchor_point.changed.connect(self.changed.emit)
        self.anchor_points.append(anchor_point)
        self.changed.emit()

    def remove_anchor_point(self, anchor_point):
        """
        :param anchor_point: anchor point to remove
        """
        self.anchor_points.remove(anchor_point)
        self.changed.emit()

    def move(self, delta: QPoint):
        """Move the whole curve

        :param delta: amount of movement
        """
        for anchor_point in self.anchor_points:
            anchor_point.move(delta)

    def calculate_path(self) -> QPainterPath:
        path = QPainterPath()
        if len(self.anchor_points) > 0:
            path.moveTo(self.anchor_points[0].root)
            for idx in range(len(self.anchor_points) - 1):
                current_point = self.anchor_points[idx]
                next_point = self.anchor_points[idx + 1]
                # The cubic bezier curve is constructed from the current point,
                # next point and the control handles in between
                path.cubicTo(current_point.controls[1], next_point.controls[0], next_point.root)
        return path

    def to_json(self):
        """ Convert the curve into a json serializable representation of the curve """
        json_anchor_points = []
        for anchor_point in self.anchor_points:
            json_anchor_points.append(anchor_point.to_json())
        return {
            "type": "Curve",
            "anchor_points": json_anchor_points,
            "pen": pen_to_json(self.pen)
        }

    def load_json(self, json_curve):
        """ Loads all values from the json serialized representation of the curve into the curve

        param json_curve: json representation of a curve
        """
        for json_point in json_curve['anchor_points']:
            anchor_point = AnchorPoint(None, None, None)
            anchor_point.load_json(json_point)
            self.add_anchor_point(anchor_point)


class AnchorPoint(QWidget):
    """
    An anchor point for use in a curve
    It has a root point and two control handles

    :signal changed: the anchor point needs to be repainted
    """
    changed = pyqtSignal()

    def __init__(self, root, control1, control2):
        super().__init__()
        self.root = root
        self.controls = [control1, control2]

    def move(self, delta: QPoint):
        """ Move the anchor point and its control handles

        :param delta: amount of movement
        """
        self.root += delta
        self.controls[0] += delta
        self.controls[1] += delta
        self.changed.emit()

    def set_control_handle_position(self, index, position: QPoint):
        """ Sets one of the control handles

        :param index: index of the control handle to change
        :param position: new control handle position
        """
        self.controls[index] = position
        self.changed.emit()

    def to_json(self):
        """ Converts the anchor point to a json serializable representation of the anchor point"""
        return {
            "root": point_to_json(self.root),
            "control0": point_to_json(self.controls[0]),
            "control1": point_to_json(self.controls[1])
        }

    def load_json(self, json_anchor_point):
        """ Loads all values from the serialized representation of the anchor point into the anchor point

        :param json_anchor_point: json representation of an anchor point
        """
        self.root = point_from_json(json_anchor_point['root'])
        self.controls[0] = point_from_json(json_anchor_point['control0'])
        self.controls[1] = point_from_json(json_anchor_point['control1'])
