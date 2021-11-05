import os
import sys
from os import path
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QTabWidget, QGridLayout
from PyQt5 import QtCore
import PyQt5

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MainWindow(QWidget):
    def __init__(self, height=None, width=None, tab_config=None):
        super().__init__()
        self.height = height
        self.width = width
        self.init_ui()
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../resources/main_window.css')
        file = open(filename)
        self.setStyleSheet(file.read())
        file.close()
        self.top_tab = QTabWidget(self)
        self.widgets = tab_config
        self.set_widgets()
        grid_layout.addWidget(self.top_tab, 0, 1, 1, 3)

    def set_widgets(self):
        for widget in self.widgets:
            self.top_tab.addTab(WidgetCreator(widget, parent=self, config=self.widgets),
                                widget)

    def init_ui(self):
        if self.width is not None and self.height is not None:
            self.resize(self.width - 100, self.height - 100)

        self.center()
        self.setWindowTitle('Titania')
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../../resources/cern.gif')

        self.setWindowIcon(QIcon(filename))

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return path.join(sys._MEIPASS, relative_path)
        return path.join(path.abspath(""), relative_path)


class WidgetCreator(QWidget):
    def __init__(self, parent_tab=None, parent=None, config=None):
        super().__init__()
        self.parent = parent
        self.parent_tab = parent_tab
        self.config = config
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.child_tab = QTabWidget(self)
        self.set_tab()
        self.grid_layout.addWidget(self.child_tab, 0, 1)
        self.setLayout(self.grid_layout)

    def set_tab(self):
        for widget in self.config[self.parent_tab]:
            try:
                widget_object = widget(self)
                self.child_tab.addTab(widget_object, widget_object.title)
                widget_object.initiate()
            except Exception as e:
                print("Creation of tab of type {} has failed.\n".format(widget))
                raise e



