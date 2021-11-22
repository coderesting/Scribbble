"""
Name: Yannick Brandt
Student number: 3077620
"""

from PyQt5.QtCore import pyqtSignal, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QActionGroup

from help.AboutWindow import AboutWindow
from help.HelpWindow import HelpWindow


class MenuBar(QMenuBar):
    """
       Provides the menu with file operations and help/about windows

       :signal open_file(): request to open a Scribbble json file
       :signal save_file(): request to save a Scribbble json file
       :signal export_file(): request to export a rendered image of the canvas
       :signal clear_canvas(): request to clear the canvas
    """
    open_file = pyqtSignal()
    save_file = pyqtSignal()
    export_file = pyqtSignal()
    clear_canvas = pyqtSignal()
    change_guides = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        # store references of the windows to prevent garbage collection
        self.help_window = HelpWindow(self)
        self.about_window = AboutWindow(self)

        # the zero width space is required as 'File' is reserved in Mac
        file_menu = self.addMenu('​File')

        # open menu item
        open_action = QAction(QIcon('./icons/open.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file.emit)
        file_menu.addAction(open_action)

        # save menu item
        save_action = QAction(QIcon('./icons/save.png'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file.emit)
        file_menu.addAction(save_action)

        # export menu item
        export_action = QAction(QIcon('./icons/export.png'), 'Export', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_file.emit)
        file_menu.addAction(export_action)

        # clear menu item
        clear_action = QAction(QIcon('./icons/clear.png'), 'Clear', self)
        clear_action.setShortcut('Ctrl+D')
        clear_action.triggered.connect(self.clear_canvas.emit)
        file_menu.addAction(clear_action)

        # exit menu item
        exit_action = QAction(QIcon('./icons/quit.png'), 'Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(QCoreApplication.quit)
        file_menu.addAction(exit_action)

        # the zero width space is required as 'View' is reserved in Mac
        view_menu = self.addMenu('​View')
        # Prevent multiple guides to be checked
        view_action_group = QActionGroup(self)
        # Create a dict to sync the selected guide in the menu with an opened file
        self.guides_actions = {}

        # Create all guide actions
        for guide in ['no', 'horizontal', 'vertical', 'grid']:
            icon = QIcon('./icons/guides_{0}.png'.format(guide))
            action = QAction(icon, '{0} guides'.format(guide.capitalize()), self, checkable=True)

            # include the guide type (g) in the lambdas' closure (needed because the loop has no separated closure)
            def lambda_generator(g):
                return lambda: self.change_guides.emit(g)

            action.triggered.connect(lambda_generator(guide))
            view_action_group.addAction(action)
            view_menu.addAction(action)
            self.guides_actions[guide] = action

        # help menu
        help_menu = self.addMenu('Help')

        # help menu item. Space is required to prevent macOS from moving this to another location
        helpAction = QAction(QIcon('./icons/help.png'), ' Help ', self)
        helpAction.setShortcut('Ctrl+?')
        helpAction.triggered.connect(self.help_window.show)
        help_menu.addAction(helpAction)

        # about menu item. Space is required to prevent macOS from moving this to another location
        aboutAction = QAction(QIcon('./icons/app.png'), ' About ', self)
        aboutAction.setShortcut('Ctrl+A')
        aboutAction.triggered.connect(self.about_window.show)
        help_menu.addAction(aboutAction)

    def set_guides(self, guides):
        self.guides_actions[guides].setChecked(True)
