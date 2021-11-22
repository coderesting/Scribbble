"""
Name: Yannick Brandt
Student number: 3077620
"""

import json
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox

from Canvas import Canvas
from MenuBar import MenuBar
from toolSettings.ToolSettings import ToolSettings
from tools.Toolbox import Toolbox


class PaintingApplication(QMainWindow):
    """
        Main window of Scribbble.
        Connects Toolbox, ToolSettings, Canvas an Menu in on window.
        It is responsible for all IO operations like open,save and export
    """

    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle('Scribbble - Paint Application')

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the application icon
        # windows version
        self.setWindowIcon(QIcon('./icons/app.png'))
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap('./icons/app.png')))

        self.canvas = Canvas()
        self.setCentralWidget(self.canvas)

        self.tool_settings = ToolSettings()
        self.addToolBar(Qt.TopToolBarArea, self.tool_settings)

        self.toolbox = Toolbox(self.canvas, self.tool_settings)
        self.addToolBar(Qt.LeftToolBarArea, self.toolbox)

        menu_bar = MenuBar()
        menu_bar.set_guides('no')
        menu_bar.open_file.connect(self.open_file)
        menu_bar.save_file.connect(self.save_file)
        menu_bar.export_file.connect(self.export_file)
        menu_bar.clear_canvas.connect(self.clear_canvas)
        menu_bar.change_guides.connect(self.canvas.set_guides)
        self.setMenuBar(menu_bar)

        # Prepare error box for invalid Scribbble file
        self.parse_error_box = QMessageBox()
        self.parse_error_box.setIcon(QMessageBox.Critical)
        self.parse_error_box.setText('Error')
        self.parse_error_box.setWindowTitle('Parsing Error')
        self.parse_error_box.setInformativeText('This is not a Scribbble file')

    def keyPressEvent(self, event):
        # forward any keypress events to the active tool
        self.toolbox.active_tool.key_press(event)

    # open a file
    def open_file(self):
        """ Loads a user chosen Scribbble json file from disk """
        filePath, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Scribbble(*.scribbble)')
        if filePath == '':
            return
        with open(filePath) as file:
            try:
                json_data = json.load(file)
                self.clear_canvas()
                self.canvas.load_json(json_data)
                self.menuBar().set_guides(json_data['guides'])
            except Exception as e:
                print(e)
                self.clear_canvas()
                self.parse_error_box.show()

    def save_file(self):
        """ Saves the Scribbble json file to a user chosen location on disk """
        filePath, _ = QFileDialog.getSaveFileName(self, 'Save Image', 'masterpiece', 'Scribbble(*.scribbble)')
        if filePath == '':
            return
        with open(filePath, 'w') as f:
            json.dump(self.canvas.to_json(), f)

    def export_file(self):
        """ Saves the rendered image to a user chosen location on disk """
        filePath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                                  'PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)')
        if filePath == '':  # if the file path is empty
            return  # do nothing and return
        self.canvas.render_image().save(filePath)  # save file image to the file path

    def clear_canvas(self):
        # de- and reactivate the current tool keep the tool and canvas state in sync
        self.toolbox.active_tool.deactivate()
        self.toolbox.active_tool.get_action().trigger()
        self.canvas.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Avoid a reported bug in QT where background and text color of the active tab is white.
    # See https://bugreports.qt.io/browse/QTBUG-85940
    app.setStyleSheet("""
        QTabBar::tab:selected {
            background-color: #0082FF;
            color: white;
        }
    """)
    window = PaintingApplication()
    window.show()
    app.exec()
