"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import List

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainterPath

from canvasElements.CanvasElement import CanvasElement, point_from_json, point_to_json
from toolSettings.ToolSettings import pen_to_json


class Line(CanvasElement):
    """
    A canvas element to show a connected line consisting of multiple points
    """

    def __init__(self, pen):
        super().__init__(pen)
        # all points are painted relative to the origin.
        # This makes moving the line fast because all points don't need to update their coordinated
        self.origin = QPoint(0, 0)
        self.points: List[QPoint] = []

    def add_point(self, point: QPoint):
        """
        :param point: point to add
        """
        self.points.append(point)
        self.changed.emit()

    def move(self, delta: QPoint):
        """Move the whole line

        :param delta: delta of movement
        """
        self.origin += delta
        self.changed.emit()

    def calculate_path(self) -> QPainterPath:
        path = QPainterPath()
        if len(self.points) > 0:
            path.moveTo(self.origin + self.points[0])
            for point in self.points:
                path.lineTo(self.origin + point)
        return path

    def to_json(self):
        """ Converts the line to a json serializable representation of the line"""
        json_points = []
        for point in self.points:
            json_points.append(point_to_json(point))
        return {
            "type": "Line",
            "points": json_points,
            "origin": point_to_json(self.origin),
            "pen": pen_to_json(self.pen)
        }

    def load_json(self, json_line):
        """ Loads all values from the serialized representation of the line into the line

        :param json_line: json representation of a line
        """
        self.move(point_from_json(json_line['origin']))
        for json_point in json_line['points']:
            self.add_point(point_from_json(json_point))
