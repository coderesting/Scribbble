"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import List

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QImage, QMouseEvent, QResizeEvent, QPen
from PyQt5.QtWidgets import QWidget

from canvasElements.CanvasElement import CanvasElement
from canvasElements.Curve import Curve
from canvasElements.Line import Line
from toolSettings.ToolSettings import pen_from_json


class Canvas(QWidget):
    """
       Paints CanvasElements in a Widget to the screen.
       For performance reasons only the newest element is always repainted.
       All other elements are cached in an image which is only repainted when elements in it change.

       :signal mouse_press(QMouseEvent): mouse pressed on canvas
       :signal mouse_move(QMouseEvent): mouse moved on canvas
       :signal mouse_release(QMouseEvent): mouse released on canvas
       :signal resize(): canvas was resized
    """
    mouse_press = pyqtSignal(object)
    mouse_move = pyqtSignal(object)
    mouse_release = pyqtSignal(object)
    resize = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Fire mouse move events even if no button is pressed
        self.setMouseTracking(True)

        self.elements = None
        self.current_element = None
        self.background = None
        self.guides = 'no'

        self.active_tool = None
        # Keep all elements, except the current one, rendered in this image to increase performance
        self.cached_image = QImage(self.size(), QImage.Format_RGB32)
        self.clear()

    def clear(self):
        """ Removes all elements from the canvas and sets the background to white """
        self.elements = []
        self.current_element = None
        self.background = QColor("white")
        self.repaint_cached_image()

    def set_background(self, color: QColor):
        """ Sets the background of the canvas

        :param color: color for the background
        """
        self.background = color
        self.repaint_cached_image()

    def set_guides(self, guides):
        """ Sets the guides of the canvas

        :param guides: guides to show. One in ['no', 'horizontal', 'vertical', 'grid']
        """
        self.guides = guides
        self.update()

    def set_active_tool(self, tool):
        """
        :param tool: new active tool
        """
        self.active_tool = tool
        self.update()

    def add_element(self, element: CanvasElement):
        """ Adds a canvas element to the canvas. Currently Line and Curve are implemented

        :param element: element to add
        """
        # replace the current element if it already exists
        if self.current_element:
            self.elements.append(self.current_element)
            self.repaint_cached_image()

        self.current_element = element

        self.update()
        # keep track of changing elements to repaint them
        element.changed.connect(lambda: self.element_changed(element))

    def get_elements(self) -> List[CanvasElement]:
        """
        :returns: All elements currently in the canvas
        """
        return self.elements if self.current_element is None else self.elements + [self.current_element]

    def remove_element(self, element):
        """ Removes an element from the canvas

        :param element: element to remove
        """
        if element in self.elements:
            self.elements.remove(element)
        elif element == self.current_element:
            self.current_element = None
        self.repaint_cached_image()

    def element_changed(self, element):
        """ Internal method to repaint when an element changed

        :param element: element that changed
        """
        if element != self.current_element:
            self.repaint_cached_image()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        # Limit to left button because no tool currently uses the right mouse button
        if event.button() == Qt.LeftButton:
            self.mouse_press.emit(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        self.mouse_move.emit(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.mouse_release.emit(event)

    def resizeEvent(self, a0: QResizeEvent):
        # Create and repaint the cached image
        self.cached_image = QImage(self.size(), QImage.Format_RGB32)
        self.repaint_cached_image()
        self.resize.emit()

    def paintEvent(self, event):
        """ Paints all cached elements from the cached image and adds the current element and active tool on top.
        The active tool doesn't have to paint anything but it has the option to do so
        """
        # you should only create and use the QPainter object in this method, it should be a local variable
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.cached_image, self.cached_image.rect())
        if self.current_element:
            self.current_element.paint(painter)

        self.paint_guides(painter)
        self.active_tool.paint(painter)

    def paint_guides(self, painter: QPainter):
        painter.setPen(QColor('#BDBDBD'))
        # Draw horizontal/vertical/grid lines at a distance of 30px to each other
        if self.guides == "horizontal" or self.guides == "grid":
            for i in range(0, self.height(), 30):
                painter.drawLine(0, i, self.width(), i)
        if self.guides == "vertical" or self.guides == "grid":
            for i in range(0, self.width(), 30):
                painter.drawLine(i, 0, i, self.height())

    def repaint_cached_image(self):
        painter = QPainter(self.cached_image)
        painter.fillRect(0, 0, self.width(), self.height(), self.background)
        for element in self.elements:
            element.paint(painter)
        self.update()

    def to_json(self):
        """ Converts the canvas to a json serializable representation of the canvas """
        json_elements = []
        for element in self.elements:
            json_elements.append(element.to_json())
        if self.current_element:
            json_elements.append(self.current_element.to_json())
        return {
            "background": self.background.name(),
            "guides": self.guides,
            "elements": json_elements
        }

    def load_json(self, json_canvas):
        """ Loads all values from the json serialized representation of the canvas into the canvas

        param json_canvas: json representation of a canvas
        """
        self.set_background(QColor(json_canvas['background']))
        self.set_guides(json_canvas['guides'])
        for json_element in json_canvas['elements']:
            element = None
            if json_element['type'] == "Curve":
                element = Curve(pen_from_json(json_element['pen']))
            elif json_element['type'] == "Line":
                element = Line(pen_from_json(json_element['pen']))

            element.load_json(json_element)
            self.add_element(element)

    def render_image(self) -> QImage:
        """
        :returns: an image of the painted canvas
        """
        self.repaint_cached_image()
        painter = QPainter(self.cached_image)
        if self.current_element:
            self.current_element.paint(painter)
        return self.cached_image
