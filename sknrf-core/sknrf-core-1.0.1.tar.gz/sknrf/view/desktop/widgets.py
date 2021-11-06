from PySide2 import QtCore
from PySide2.QtWidgets import QFileDialog, QWidget, QLineEdit, QPushButton
from PySide2.QtWidgets import QHBoxLayout


class QFileEdit(QWidget):

    def __init__(self, text="", placeholder_text="", caption="", file_types="All Files (*.)", parent=None):
        super(QFileEdit, self).__init__(parent=parent)
        self.edit = QLineEdit("", parent=self)
        self.edit.setPlaceholderText(placeholder_text)
        button = QPushButton("...")
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.edit), layout.addWidget(button)
        self.setLayout(layout)
        button.clicked.connect(self.select_file)
        self.caption = caption
        self.file_types = file_types

    @QtCore.Slot()
    def select_file(self):
        if self.file_types == "dir":
            filename = QFileDialog.getExistingDirectory(self, self.caption, '')
        else:
            filename, filter_ = QFileDialog.getOpenFileName(self, self.caption, '', filter=self.file_types)
        self.edit.setText(filename)