"""
Name: Yannick Brandt
Student number: 3077620
"""

from typing import Optional

from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QIcon, QPen, QCursor, QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QApplication

from canvasElements.Curve import Curve, AnchorPoint
from tools.Tool import Tool


class Pen(Tool):
    """
    Pen Tool
    Creates Curves by adding and manipulating anchor points
    """

    def __init__(self, canvas):
        super().__init__("Pen", QIcon("icons/pen.png"), Qt.Key_P)
        self.canvas = canvas

        self.cursor = QCursor(QPixmap('icons/pen_cursor.png'), 1, 1)

        self.current_curve: Optional[Curve] = None
        self.selected_anchor_point = None
        self.selected_control_handle = None
        self.preview_curve_color = QColor('#1565C0')

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def deactivate(self):
        self.canvas.unsetCursor()
        self.current_curve = None
        self.selected_anchor_point = None
        self.selected_control_handle = None

    def mouse_press(self, event):
        collision = self.check_collision(event.pos())
        if collision['anchor']:
            if self.current_curve is None:
                # Select the clicked curve
                self.current_curve = collision['curve']
            self.selected_anchor_point = collision['anchor']
            self.selected_control_handle = collision['control']
        else:
            if self.current_curve is None:
                # Create a new curve if no collision occurred and no current curve to add a point exists
                self.current_curve = Curve(self.pen)
                self.canvas.add_element(self.current_curve)
            new_anchor_point = AnchorPoint(event.pos(), event.pos(), event.pos())
            self.current_curve.add_anchor_point(new_anchor_point)
            self.selected_anchor_point = new_anchor_point
            # Set the forward control handle as default
            self.selected_control_handle = 1

        self.canvas.update()

    def mouse_move(self, event):
        alt_key_down = (QApplication.keyboardModifiers() & Qt.AltModifier) == Qt.AltModifier
        mouse_down = event.buttons() == Qt.LeftButton

        if mouse_down and self.selected_anchor_point:
            if self.selected_control_handle is not None:
                self.selected_anchor_point.set_control_handle_position(self.selected_control_handle, event.pos())
                # Move the opposite control handle together with the selected one if alt is not held down
                if not alt_key_down:
                    opposite_control = (self.selected_anchor_point.root - event.pos()) + self.selected_anchor_point.root
                    opposite_control_index = 1 - self.selected_control_handle
                    self.selected_anchor_point.set_control_handle_position(opposite_control_index, opposite_control)
            else:
                # Move anchor
                delta = event.pos() - self.selected_anchor_point.root
                self.selected_anchor_point.move(delta)

    def key_press(self, event):
        # Deselect the current curve
        if event.key() == Qt.Key_Escape and self.current_curve:
            self.current_curve = None
            self.selected_anchor_point = None
            self.selected_control_handle = None
            self.canvas.update()

        # Delete the current anchor point
        elif event.key() == Qt.Key_Backspace and self.selected_anchor_point:
            self.current_curve.remove_anchor_point(self.selected_anchor_point)
            self.selected_anchor_point = None
            self.selected_control_handle = None

    def check_collision(self, mouse_pos: QPoint):
        collision = {
            "curve": None,
            "anchor": None,
            "control": None
        }
        threshold = 10
        # only check points on the current curve if current curve is available
        elements = [self.current_curve] if self.current_curve else self.canvas.get_elements()
        for element in elements:
            if isinstance(element, Curve):
                for anchor_point in element.anchor_points:
                    # Check control points first otherwise they would become inaccessible
                    # when not dragged out from under the anchor point
                    if (mouse_pos - anchor_point.controls[1]).manhattanLength() < threshold:
                        collision['curve'] = element
                        collision['anchor'] = anchor_point
                        collision['control'] = 1
                    elif (mouse_pos - anchor_point.controls[0]).manhattanLength() < threshold:
                        collision['curve'] = element
                        collision['anchor'] = anchor_point
                        collision['control'] = 0
                    elif (mouse_pos - anchor_point.root).manhattanLength() < threshold:
                        collision['curve'] = element
                        collision['anchor'] = anchor_point

        return collision

    def paint(self, painter: QPainter):
        if self.current_curve:
            self.paint_preview_curve(painter, self.current_curve)
            self.paint_preview_anchor_points(painter, self.current_curve.anchor_points, self.selected_anchor_point, 4)
            if self.selected_anchor_point:
                self.paint_preview_handles(painter, self.selected_anchor_point)
        else:
            # Paint all curves with smaller points if no curve is selected
            for element in self.canvas.get_elements():
                if isinstance(element, Curve):
                    self.paint_preview_curve(painter, element)
                    self.paint_preview_anchor_points(painter, element.anchor_points, None, 3)

    def paint_preview_curve(self, painter: QPainter, curve: Curve):
        """ Paint a preview curve on top of the real one

        :param painter: painter to paint to
        :param curve: curve to paint
        """
        painter.setPen(QPen(self.preview_curve_color))
        painter.setBrush(QBrush(Qt.transparent))
        path = curve.get_path()
        painter.drawPath(path)

    def paint_preview_anchor_points(self, painter, anchor_points, selected_anchor_point, size):
        """ Paint preview anchor points top of the real curve

        :param painter: painter to paint to
        :param anchor_points: anchor_points to paint
        :param selected_anchor_point: selected anchor point will be highlighted
        :param size: size of the painted anchor points
        """
        painter.setPen(QPen(self.preview_curve_color))
        painter.setBrush(QBrush(Qt.white))
        for anchor_point in anchor_points:
            color = self.preview_curve_color if anchor_point == selected_anchor_point else Qt.white
            painter.setBrush(QBrush(color))
            painter.drawEllipse(anchor_point.root, size, size)

    def paint_preview_handles(self, painter, anchor_point):
        """ Paint preview handle points

        :param painter: painter to paint to
        :param anchor_point: anchor_point with preview handles to paint
        """
        painter.setPen(QPen(self.preview_curve_color))
        painter.setBrush(QBrush(Qt.white))
        # Draw connections to the anchor point
        painter.drawLine(anchor_point.root, anchor_point.controls[0])
        painter.drawLine(anchor_point.root, anchor_point.controls[1])

        painter.drawRect(self.create_rect_at_point(anchor_point.controls[0], 3))
        painter.drawRect(self.create_rect_at_point(anchor_point.controls[1], 3))

    def create_rect_at_point(self, point: QPoint, size: float):
        """ Create a rectangle around a point

        :param point: point to paint
        :param size: size of the rectangle
        """
        offset = QPoint(size, size)
        return QRectF(point - offset, point + offset)

    def pen_change(self, pen):
        super().pen_change(pen)
        # Apply changes made to the settings while creating a curve to the current curve
        if self.current_curve:
            self.current_curve.set_pen(pen)
