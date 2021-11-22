"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QMovie
from PyQt5.QtWidgets import QDialog, QTabWidget, QVBoxLayout

from help.ToolHelp import ToolHelp


class HelpWindow(QDialog):
    """
    Shows help information about the Scribbble application.
    This includes a general overview, information about each tool with keyboard shortcuts and example videos
    """

    def __init__(self, parent):
        super().__init__(parent, Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        # Disable the maximize button on macOS
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setModal(True)
        self.setWindowTitle('Scribbble Help')
        self.setWindowIcon(QIcon('icons/help.png'))

        tabs = QTabWidget()

        app_img = QPixmap('icons/app.png')
        general_help = ToolHelp(app_img.scaledToWidth(24), 'Scribbble',
                                ('How to create a masterpiece 101:\n'
                                 '1. Choose a tool from the toolbox on the left\n'
                                 '2. Configure the tool by using the settings on the top.\n'
                                 '3. I you are not done go to 1.\n'
                                 '4. Export your work from the file menu\n'
                                 '5. Enjoy your work :)'),
                                QMovie('help/videos/app.gif'),
                                [['Ctrl+O', 'Open a file'], ['Ctrl+S', 'Save your work'],
                                 ['Ctrl+E', 'Export your work'], ['Ctrl+D', 'Clear the canvas'], ['Ctrl+Q', 'Exit']])
        tabs.addTab(general_help, 'General')

        move_help = ToolHelp(QPixmap('icons/move.png'), 'Move Tool',
                             ('Press the left mouse button to grab the canvas and move it.\n'
                              'The current size of the canvas is shown in the tool settings.\n'
                              'Resize the window to increase or decrease the size of the canvas.'),
                             QMovie('help/videos/move.gif'), [['m', 'Select this tool']])
        tabs.addTab(move_help, 'Move Tool')

        select_help = ToolHelp(QPixmap('icons/select.png'), 'Selection Tool',
                               ('Click on any element to select it.\n'
                                'he selected Element can be\n'
                                '- dragged with the left mouse button\n'
                                '- modified by changing the respective settings'),
                               QMovie('help/videos/select.gif'),
                               [['v', 'Select this tool'], ['⌫', 'Delete the selected element']])
        tabs.addTab(select_help, 'Selection Tool')

        brush_help = ToolHelp(QPixmap('icons/brush.png'), 'Brush Tool',
                              'Click and hold the left mouse button to draw a line with the specified settings',
                              QMovie('help/videos/brush.gif'),
                              [['b', 'Select this tool']])
        tabs.addTab(brush_help, 'Brush Tool')

        pen_help = ToolHelp(QPixmap('icons/pen.png'), 'Pen Tool',
                            ('Draw lines by creating anchor points.\n'
                             'Click and drag to create an anchor point\n'
                             'Click and drag on existing anchor points/control handles to move them\n'),
                            QMovie('help/videos/pen.gif'),
                            [['p', 'Select this tool'], ['ESC', 'Deselect the current curve'],
                             ['⌫', 'Delete the selected anchor point'],
                             ['ALT', 'Disable control point mirroring']])
        tabs.addTab(pen_help, 'Pen Tool')

        fill_help = ToolHelp(QPixmap('icons/fill.png'), 'Fill Tool',
                             'Click anywhere on the canvas to fill the background with the selected color',
                             QMovie('help/videos/fill.gif'), [['f', 'Select this tool']])
        tabs.addTab(fill_help, 'Fill Tool')

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

        # Fix the window size to the minimum size
        self.setFixedSize(layout.minimumSize())
