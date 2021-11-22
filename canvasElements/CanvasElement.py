"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import QMarginsF, QRect, pyqtSignal, QPoint
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import QWidget


class CanvasElement(QWidget):
    """ Abstract class for canvas elements.
    It provides functionality for:
     - only recalculating the painter path when coordinates changed.
     - setting/getting the pen

    :signal changed(): the canvas element needs to be repainted
    """
    changed = pyqtSignal()

    def __init__(self, pen):
        super().__init__()
        self.pen = pen
        self.cached_path = None
        self.changed.connect(self.invalidate_cached_path)

    def set_pen(self, pen):
        self.pen = pen
        self.changed.emit()

    def get_pen(self):
        return self.pen

    def paint(self, painter):
        """Paints this element with its pen and path
        :param painter: painter to draw with
        """
        painter.setPen(self.pen)
        painter.drawPath(self.get_path())

    def get_bounding_rect(self) -> QRect:
        """Calculates the outer bounding rect of this canvas element
        :returns: outer bounding rect
        """
        margin = self.pen.width() / 2
        if self.cached_path is None:
            self.cached_path = self.get_path()
        return self.cached_path.boundingRect().marginsAdded(QMarginsF(margin, margin, margin, margin))

    def get_path(self) -> QPainterPath:
        """
        :returns: painter path
        """
        if self.cached_path is None:
            self.cached_path = self.calculate_path()
        return self.cached_path

    def calculate_path(self) -> QPainterPath:
        """This method should be overwritten by the implementing class and return the painter path for this element
        :returns: painter path
        """
        return QPainterPath()

    def invalidate_cached_path(self):
        self.cached_path = None


def point_to_json(point: QPoint):
    """ Helper method to convert a QPoint into a json serializable representation of a point

    :param point: point to convert
    """
    return {
        "x": point.x(),
        "y": point.y()
    }


def point_from_json(json_point):
    """ Helper method to convert a json serializable representation of a point into a QPoint

    :param json_point: json point to convert
    """
    return QPoint(json_point['x'], json_point['y'])
