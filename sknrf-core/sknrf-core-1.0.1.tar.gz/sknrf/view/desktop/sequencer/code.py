import sys

from PySide2 import QtCore
from PySide2.QtCore import Qt, QSize, QRect, QObject, QMetaObject
from PySide2.QtGui import QPixmap, QPainter
from PySide2.QtWidgets import QApplication, QPlainTextEdit, QDialog, QDialogButtonBox, QWidget
from PySide2.QtWidgets import QVBoxLayout

from sknrf.icons import red_32_rc, green_32_rc

__author__ = 'dtbespal'


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super(LineNumberArea, self).__init__(parent=editor)
        self.code_editor = editor

    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_paint_event(event)

    def mousePressEvent(self, event):
        if not (event.buttons() and Qt.LeftButton):  # if not left button
            return
        self.code_editor.clicked_break_points(event.pos())


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super(CodeEditor, self).__init__(parent)
        self._breakpoint_radius = self.fontMetrics().height()
        self._gap_width = 3
        self._line_number_area = LineNumberArea(self)
        self._breakpoints = set()
        self._active_breakpoint = -1
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.update_line_number_area_width(0)

    def set_breakpoints(self, breakpoints):
        self._breakpoints = breakpoints
        self._line_number_area.repaint()

    def set_active_breakpoint(self, active_breakpoint):
        self._active_breakpoint = active_breakpoint
        self._line_number_area.repaint()

    def clicked_break_points(self, position):
        pass
        # text_block = self.cursorForPosition(position)
        # selected_line = text_block.blockNumber() + 1
        # if selected_line in self._breakpoints:
        #     self._breakpoints.remove(selected_line)
        # else:
        #     self._breakpoints.add(selected_line)
        # self._line_number_area.repaint()

    def line_number_paint_event(self, event):
        painter = QPainter(self._line_number_area)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        radius = self._breakpoint_radius
        gap = self._gap_width
        painter.setPen(Qt.black)
        source_rect = QRect(0, 0, 32, 32)

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                if block_number + 1 in self._breakpoints:
                    rect = QRect(self._line_number_area.width() - radius - gap, top, 2*radius, 2*radius)
                    painter.drawPixmap(rect, QPixmap(":/PNG/red/32/form_oval.png"), source_rect)
                if block_number + 1 == self._active_breakpoint:
                    rect = QRect(self._line_number_area.width() - radius - gap, top, 2*radius, 2*radius)
                    painter.drawPixmap(rect, QPixmap(":/PNG/green/32/arrow-right.png"), source_rect)
                painter.setPen(Qt.black)
                number = str(block_number + 1)
                painter.drawText(0, top, self._line_number_area.width() - 2 * gap - radius, self.fontMetrics().height(),
                                 Qt.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def line_number_area_width(self):
        digits = 1
        max_ = max(1, self.blockCount())
        while max_ >= 10:
            max_ /= 10
            digits += 1
        space = self._gap_width + self.fontMetrics().width('9') * digits + \
            self._gap_width + self._breakpoint_radius + self._gap_width
        return space

    def resizeEvent(self, event):
        super(CodeEditor, self).resizeEvent(event)

        cr = self.contentsRect()
        self._line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

    def update_line_number_area_width(self, new_block_count):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self._line_number_area.scroll(0, dy)
        else:
            self._line_number_area.update(0, rect.y(), self._line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)


class Ui_codeDialog(object):
    def setupUi(self, codeDialog):
        codeDialog.setObjectName("codeDialog")
        codeDialog.resize(567, 560)
        codeDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(codeDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.codePlainTextEdit = CodeEditor(codeDialog)
        self.codePlainTextEdit.setReadOnly(True)
        self.codePlainTextEdit.setObjectName("codePlainTextEdit")
        self.verticalLayout.addWidget(self.codePlainTextEdit)
        self.buttonBox = QDialogButtonBox(codeDialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(codeDialog)
        QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), codeDialog.accept)
        QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), codeDialog.reject)
        QMetaObject.connectSlotsByName(codeDialog)

    def retranslateUi(self, codeDialog):
        codeDialog.setWindowTitle(QApplication.translate("codeDialog", "Sequencer Code", None, -1))


class CodeDialog(QDialog, Ui_codeDialog):
    def __init__(self, py_code, breakpoints=set(), active_breakpoint=-1, parent=None):
        super(CodeDialog, self).__init__(parent=parent)
        self.setupUi(self)
        self.codePlainTextEdit.setPlainText(py_code)
        self.set_breakpoints(breakpoints)
        self.set_active_breakpoint(active_breakpoint)
        self.codePlainTextEdit.set_active_breakpoint(active_breakpoint)

    def set_breakpoints(self, breakpoints):
        self.codePlainTextEdit.set_breakpoints(breakpoints)

    def set_active_breakpoint(self, active_breakpoint):
        self.codePlainTextEdit.set_active_breakpoint(active_breakpoint)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CodeDialog(
        "Hello\n World\n Dylan\nHello\n World\n Dylan\nHello\n World\n Dylan\nHello\n World\n Dylan\nHello\n World\n Dylan\nHello\n World\n Dylan\n")
    dialog.show()
    app.exec_()
