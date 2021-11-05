#!/usr/bin/python
import json
import os
import shutil
import subprocess
import sys
import traceback
import time
import re

import pkg_resources
from inspect import isgeneratorfunction
from os import listdir
from os.path import join, isdir, isfile
from random import randint

try:
    import requests
    from PyQt5 import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
except ImportError as e:
    print("looks like you are missing some pip libraries. go back to the github page and download them.\n")
    raise e

app = QApplication(sys.argv)
version = '1.2.2'
items = []
install_path = join(os.sep, 'opt', 'Qnverter')
base_path = join(os.path.expanduser('~'), 'Qnverter')
config_path = join(base_path, 'config')
icons_path = join(base_path, 'icons')
resources_path = join(base_path, 'resources')
scripts_path = join(base_path, 'scripts')

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.setWindowTitle('Qnverter')
        tbh = 35  # PLEASE, its "TitleBar Height" NOT "To Be Honest".
        self.last_event = Item.example
        settings.setdefault("highlight_code", False)

        # move to schreen centre
        self.resize(800, 800)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # build user interface
        self.text_box_a = CodeEditor('a')
        self.text_box_b = CodeEditor('b')

        self.text_box_a.highlighter = Highlighter(self.text_box_a.document())
        self.text_box_b.highlighter = Highlighter(self.text_box_b.document())

        self.command_button = QPushButton('Open command selection')
        self.command_button.setMinimumHeight(tbh)
        self.command_button.setMaximumWidth(320)
        self.command_button.clicked.connect(self.start_selection)

        self.reload_button = QToolButton()
        self.reload_button.setIcon(QIcon(join(resources_path, 'reload.png')))
        self.reload_button.setIconSize(QSize(tbh - 10, tbh - 10))
        self.reload_button.setMinimumHeight(tbh)
        self.reload_button.setMinimumWidth(tbh)
        self.reload_button.setToolTip('reload scripts')
        self.reload_button.clicked.connect(load_scripts)

        self.info_button = QToolButton()
        self.info_button.setIcon(QIcon(join(resources_path, 'menu.png')))
        self.info_button.setIconSize(QSize(tbh - 10, tbh - 10))
        self.info_button.setMinimumHeight(tbh)
        self.info_button.setMinimumWidth(tbh)
        self.info_button.setToolTip('show info')
        self.info_button.clicked.connect(self.shortcut_window)

        self.highlight_checkbox = QToolButton()
        self.highlight_checkbox.setCheckable(True)
        self.highlight_checkbox.setChecked(settings["highlight_code"])
        self.highlight_checkbox.setIcon(QIcon(join(resources_path, 'highlighter.png')))
        self.highlight_checkbox.setIconSize(QSize(tbh - 10, tbh - 10))
        self.highlight_checkbox.setMinimumHeight(tbh)
        self.highlight_checkbox.setMinimumWidth(tbh)
        self.highlight_checkbox.setToolTip('syntax highlight coming soon :)')
        self.highlight_checkbox.clicked.connect(self.highlight_button_event)

        self.add_script_button = AddScriptButton()
        self.add_script_button.setIcon(QIcon(join(resources_path, 'add-file.png')))
        self.add_script_button.setIconSize(QSize(tbh - 10, tbh - 10))
        self.add_script_button.setMinimumHeight(tbh)
        self.add_script_button.setMinimumWidth(tbh)
        self.add_script_button.setToolTip('Add script')
        self.add_script_button.clicked.connect(self.add_script_button.on_click)

        # glue user interface
        self.main_layout = QVBoxLayout()
        self.text_box_splitter = QSplitter(Qt.Horizontal)
        self.titlebar = QHBoxLayout()
        self.main_layout.addLayout(self.titlebar)
        self.main_layout.addWidget(self.text_box_splitter)
        self.text_box_splitter.setHandleWidth(10)
        self.main_layout.setSpacing(0)
        self.text_box_splitter.addWidget(self.text_box_a)
        self.text_box_splitter.addWidget(self.text_box_b)
        self.titlebar.addWidget(self.add_script_button)
        self.titlebar.addSpacing(5)
        self.titlebar.addWidget(self.highlight_checkbox)
        self.titlebar.addStretch()
        self.titlebar.addWidget(self.command_button, 1)
        self.titlebar.addStretch()
        self.titlebar.addWidget(self.reload_button)
        self.titlebar.addSpacing(5)
        self.titlebar.addWidget(self.info_button)
        self.setLayout(self.main_layout)
        app.exec()

    def shortcut_window(self):
        class short_cut_render(QHBoxLayout):
            def __init__(self, keys: tuple, description: str) -> None:
                super().__init__()
                for i in keys:
                    label = QLabel()
                    label.setText(f'<code>{i}</code>')
                    label.setStyleSheet('border: 1px solid black;')
                    self.addWidget(label)
                    if keys.index(i) < len(keys) - 1:
                        l = QLabel()
                        l.setText(' + ')
                        self.addWidget(l)
                t = QLabel()
                t.setText(description)
                self.addWidget(t)
                self.addStretch()

        # register the shortcuts
        ctrl_P = short_cut_render(('ctrl', 'P'), 'open the selection screen')
        ctrl_R = short_cut_render(('ctrl', 'R'), 'reexecute last command')
        ctrl_Q = short_cut_render(('ctrl', 'Q'), 'swap the two textboxes')
        ctrl_S = short_cut_render(('ctrl', 'S'), 'save textbox content to file')
        ctrl_O = short_cut_render(('ctrl', 'O'), 'import textbox content to file')

        # build user interface
        text_edit = QTextEdit()
        res = ''
        for i in items:
            res += f'<p align="center">{i.name} script by {i.author}</span></p>'
        text_edit.setHtml(f'<html><head/><body>{res}</body></html>')
        text_edit.setReadOnly(True)

        icon_size = 128
        icon_label = QLabel()
        icon = QPixmap(join(resources_path, 'icon.png'))
        icon = icon.scaledToHeight(icon_size)
        icon = icon.scaledToWidth(icon_size)
        icon_label.setPixmap(icon)
        icon_label.setAlignment(Qt.AlignHCenter)

        title_label = QLabel()
        title_label.setText('Qnverter')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet('font-size: 18px;')

        version_label = QLabel()
        version_label.setText(version)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet('font-size: 14px;')

        license_label = QLabel()
        license_label.setText(
            '<p>This program comes with absolutely no warranty.<br/>See <a href="https://opensource.org/licenses/mit-license.php">The MIT Licence (MIT)</a> for details.</p>')
        license_label.setAlignment(Qt.AlignCenter)

        author_label = QLabel()
        author_label.setText(
            '<p><a href="https://github.com/Nicky5/Qnverter">Programm</a> created by <a href="https://github.com/Nicky5">nicky</a></p>')
        author_label.setAlignment(Qt.AlignCenter)

        directory_button = QPushButton()
        directory_button.setText('open base directory')
        directory_button.clicked.connect(lambda: open_on_external_programm(base_path))

        reset_button = QPushButton()
        reset_button.setText('reset scripts')
        reset_button.clicked.connect(reset_scripts)

        grid = QGridLayout()
        v_layout = QVBoxLayout()

        # glue user interface
        grid.addWidget(QLabel('global shortcuts'), 0, 0)
        grid.addWidget(QLabel('textbox shortcuts'), 0, 1)
        grid.addLayout(ctrl_O, 1, 1)
        grid.addLayout(ctrl_S, 2, 1)
        grid.addLayout(ctrl_Q, 1, 0)
        grid.addLayout(ctrl_P, 2, 0)
        grid.addLayout(ctrl_R, 3, 0)
        button_layout = QHBoxLayout()
        button_layout.addWidget(directory_button)
        button_layout.addStretch()
        button_layout.addWidget(reset_button)
        v_layout.addWidget(icon_label)
        v_layout.addWidget(title_label)
        v_layout.addWidget(version_label)
        v_layout.addWidget(license_label)
        v_layout.addWidget(author_label)
        v_layout.addWidget(text_edit)
        v_layout.addLayout(grid)
        v_layout.addLayout(button_layout)

        # start subwindow
        dlg = QDialog()
        dlg.setWindowTitle("Shortcut Guide")
        dlg.setLayout(v_layout)
        dlg.setWindowFlag(Qt.FramelessWindowHint)
        centre = (self.x() + (self.frameGeometry().width() // 2) - (dlg.width() // 2),
                  self.y() + (self.frameGeometry().height() // 2) - (dlg.height() // 2))
        dlg.move(centre[0], centre[1])
        dlg.exec()

    def start_selection(self):
        # start selection window
        dialogue = QDialog()
        dialogue.setWindowFlags(Qt.FramelessWindowHint)
        dialogue.setWindowModality(Qt.ApplicationModal)
        centre = (self.x() + (self.frameGeometry().width() // 2) - (320 // 2),
                  self.y() + (self.frameGeometry().height() // 2) - (485 // 2))
        dialogue.move(centre[0], centre[1])
        selection_menu = Selection()
        selection_menu.setParent(dialogue)
        uuid = dialogue.exec()

        if uuid is None:
            print('uuid was none')
            return
        script = get_script_from_uuid(uuid)
        if script is None:
            print('script was none')
            return

        # execute fetched script
        self.last_event = script.event
        self.execute_event(script.event)

    def execute_event(self, event):
        # if isgeneratorfunction(event):
        #     self.text_box_b.setPlainText('')
        #     try:
        #         for i in event(self.get_text_object()):
        #             if i is not None:
        #                 self.text_box_b.insertPlainTextAtEnd(i)
        #     except Exception as e:
        #         Exeption_handler(e, True)
        # else:
        result = 'error'
        try:
            result = event(self.get_text_object())
        except Exception as e:
            Exeption_handler(e, True)
        if result is not None:
            self.text_box_b.setPlainText(str(result))

    def highlight_button_event(self):
        settings["highlight_code"] = self.highlight_checkbox.isChecked()
        self.text_box_a.highlighter.rehighlight()
        self.text_box_a.highlighter.rehighlight()

    def on_exit_save(self):
        self.text_box_a.on_exit_save()
        self.text_box_b.on_exit_save()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_P:
                self.start_selection()
            elif e.key() == Qt.Key_R:
                self.execute_event(self.last_event)
            elif e.key() == Qt.Key_Q:
                text_a = self.text_box_a.text()
                text_b = self.text_box_b.text()
                self.text_box_a.setPlainText(text_b)
                self.text_box_b.setPlainText(text_a)
        super().keyPressEvent(e)

    def get_text_object(self, textbox='a'):
        if textbox == 'a':
            return Text(self.text_box_a.text(), self.text_box_a.text()[
                                                self.text_box_a.textCursor().selectionStart():self.text_box_a.textCursor().selectionEnd()])
        return Text(self.text_box_b.text(), self.text_box_b.text()[
                                            self.text_box_b.textCursor().selectionStart():self.text_box_b.textCursor().selectionEnd()])

class Highlighter(QSyntaxHighlighter):

    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False', 'null', 'Null', 'end', 
        'private', 'public', 'static', 'var', 'val', 'let', 
        'export', 'fun', 'function', 'func', 'new', 'as', 
        'where', 'select', 'delete', 'add', 'limit', 'update', 'insert'
    ]

    types = [
        'bool', 'boolean', 'int', 'integer', 'byte', 'short',
        'long', 'float', 'double', 'array', 'list', 'dict', 
        'dictionary', 'tuple'
    ]

    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',
    ]

    # braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        settings.setdefault("styles", {})
        settings["styles"].setdefault('keyword', [[200, 120, 50], 'bold'])
        settings["styles"].setdefault('types', [[108, 149, 235]])
        settings["styles"].setdefault('operator', [[150, 150, 150]])
        settings["styles"].setdefault('brace', ['darkGray'])
        settings["styles"].setdefault('string', [[20, 110, 100]])
        settings["styles"].setdefault('string2', [[30, 120, 110]])
        settings["styles"].setdefault('comment', [[128, 128, 128]])
        settings["styles"].setdefault('self', [[150, 85, 140], 'italic'])
        settings["styles"].setdefault('numbers', [[100, 150, 190]])

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), QRegExp("'''"), 1, format(*settings['styles']['string2']))
        self.tri_double = (QRegExp('"""'), QRegExp('"""'), 2, format(*settings['styles']['string2']))
        self.multi_dash = (QRegExp('\/\*'), QRegExp('\*\/'), 3, format(*settings['styles']['string2']))

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, format(*settings['styles']['keyword']))
                  for w in Highlighter.keywords]
        rules += [(r'\b%s\b' % w, 0, format(*settings['styles']['types']))
                  for w in Highlighter.types]
        rules += [(r'%s' % o, 0, format(*settings['styles']['operator']))
                  for o in Highlighter.operators]
        rules += [(r'%s' % b, 0, format(*settings['styles']['brace']))
                  for b in Highlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, format(*settings['styles']['self'])),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\(""")]*(\\.[^"\\]*)*"', 0, format(*settings['styles']['string'])),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\(''')]*(\\.[^'\\]*)*'", 0, format(*settings['styles']['string'])),

            # From '#' or '//' until a newline
            (r'#[^\n]*', 0, format(*settings['styles']['comment'])),
            (r'(\/\/)[^\n]*', 0, format(*settings['styles']['comment'])),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, format(*settings['styles']['numbers'])),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, format(*settings['styles']['numbers'])),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, format(*settings['styles']['numbers']))
        ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]
        self.default_format = QTextCharFormat()
        self.default_format.setForeground(QPalette().windowText().color())

    def highlightBlock(self, text):
        # Do other syntax formatting
        if settings["highlight_code"]:
            for expression, nth, format in self.rules:
                index = expression.indexIn(text, 0)

                while index >= 0:
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)


            # Do multi-line strings
            self.setCurrentBlockState(0)
            in_multiline = self.match_multiline(text, *self.tri_single)
            if not in_multiline:
                in_multiline = self.match_multiline(text, *self.tri_double)
            if not in_multiline:
              in_multiline = self.match_multiline(text, *self.multi_dash)
        else:
            palette = QPalette()
            self.setFormat(0, len(text), palette.windowText().color())

    def match_multiline(self, text, start_delimiter, end_delimiter, in_state, style):
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = start_delimiter.indexIn(text)
            # Move past this match
            add = start_delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = end_delimiter.indexIn(text, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + end_delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = start_delimiter.indexIn(text, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False

class LineNumberArea(QWidget):
    def __init__(self, editor):
        QWidget.__init__(self, editor)
        self._code_editor = editor

    def sizeHint(self):
        return QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._code_editor.lineNumberAreaPaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, type_: str, no_rec=False):
        super().__init__()
        self.type = type_
        self.sm_key = f'text_box_{self.type}'
        self.setPlainText(settings.setdefault(self.sm_key, ''))

        self.line_number_area = LineNumberArea(self)
        self.result_board = CodeEditor(no_rec=True) if no_rec else None

        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width()
        self.highlight_current_line()

    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), self.palette().button())
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        offset = self.contentOffset()
        top = self.blockBoundingGeometry(block).translated(offset).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(self.palette().windowText().color())
                width = self.line_number_area.width()
                height = self.fontMetrics().height()
                painter.drawText(0, int(top), width, height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(self.palette().button())
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def setPlainText(self, p_str):
        cursor = QTextCursor(self.textCursor())
        cursor.beginEditBlock()
        cursor.select(QTextCursor.Document)
        cursor.insertText(p_str)
        cursor.movePosition(QTextCursor.End)
        cursor.endEditBlock()

    def insertPlainTextAtEnd(self, p_str):
        cursor = QTextCursor(self.textCursor())
        cursor.beginEditBlock()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(p_str)
        cursor.movePosition(QTextCursor.End)
        cursor.endEditBlock()

    def text(self):
        temp = self
        return temp.toPlainText()

    def save(self):
        filename = saveFileDialog(self)
        f = open(filename, "w")
        f.write(self.text())

    def import_(self):
        filename = openFileNameDialog(self)
        f = open(filename, "r")
        self.setPlainText(f.read())

    def on_exit_save(self):
        settings[self.sm_key] = self.text()
        settings.save()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_S:
                self.save()
            if e.key() == Qt.Key_O:
                self.import_()
            if e.key() == Qt.Key_Y:
                self.redo()
        super().keyPressEvent(e)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        f = open(event.mimeData().urls()[0].toLocalFile(), "r")
        try:
            text = f.read()
        except Exception as e:
            Exeption_handler(e, True)
        else:
            self.setPlainText(text)
            f.close()

class Selection(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("command selection")
        self.setFixedWidth(320)
        self.setFixedHeight(640)

        self.setAcceptDrops(True)
        self.scroll = QScrollArea()
        self.widget = QWidget()
        self.main_Layout = QVBoxLayout()
        self.script_Layout = QVBoxLayout()
        self.script_Layout = QVBoxLayout()
        self.script_Layout.setAlignment(Qt.AlignTop)

        self.titlebar = QHBoxLayout()

        self.model = QStringListModel()

        temp = []
        for i in items:
            temp.extend(i.keys)

        self.model.setStringList(set(temp))
        self.completer = QCompleter()
        self.completer.setModel(self.model)

        self.searchbar = QLineEdit()
        self.searchbar.setText(settings.get('search_bar_text', ''))
        self.searchbar.textChanged.connect(self.update_items)
        self.searchbar.setCompleter(self.completer)
        self.titlebar.addWidget(self.searchbar, 1)

        self.main_Layout.setAlignment(Qt.AlignTop)
        self.script_Layout.setAlignment(Qt.AlignTop)
        self.titlebar.setAlignment(Qt.AlignRight)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.main_Layout.addLayout(self.titlebar)
        self.main_Layout.addWidget(self.scroll)

        self.update_items()
        self.setLayout(self.main_Layout)
        self.setMaximumWidth(320)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for i in event.mimeData().urls():
            self.add_script(i.toLocalFile())

    def add_script(self, path):
        if is_valid_script(path):
            shutil.copy(path, scripts_path)
            load_script(path)
            self.update_items()
        else:
            Exeption_handler('invalid script', True)

    def update_items(self):
        settings['search_bar_text'] = self.searchbar.text()
        temp = []
        for i in items:
            temp.extend(i.keys)
        self.model.setStringList(set(temp))

        for i in get_children(self.script_Layout):
            i.setParent(None)

        for i in items:
            if self.searchbar.text() is None or search_help(i.keys, self.searchbar.text()):
                self.script_Layout.addWidget(i.itemrender(i))

        self.widget.setLayout(self.script_Layout)
        self.scroll.setWidget(self.widget)

class AddScriptButton(QToolButton):

    def on_click(self):
        files = openFileNamesDialog(self)
        for path in files:
            self.add_script(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for i in event.mimeData().urls():
            self.add_script(i.toLocalFile())

    def add_script(self, path):
        if is_valid_script(path):
            shutil.copy(path, scripts_path)
            load_script(path)
            return
        Exeption_handler('invalid script', True)

class Itemrender(QAbstractButton):
    icon_size = 32

    def __init__(self, item):
        super().__init__(None)
        self.item = item
        self.blocked = not self.item.are_dependecies_present()
        if self.blocked:
            self.missing_dependecies = ', '.join(self.item.get_missing_dependecies())
        
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignLeft)

        self.icon_label = QLabel()
        self.icon = QPixmap(item.icon)
        if self.icon.isNull():
            self.icon = QPixmap('icon.png')
        self.icon = self.icon.scaledToHeight(Itemrender.icon_size)
        self.icon = self.icon.scaledToWidth(Itemrender.icon_size)
        self.icon_label.setPixmap(self.icon)

        self.title = QLabel(item.name)
        self.title.setStyleSheet('font-size: 17px;')
        self.title.setMaximumWidth(420)
        self.description = QLabel(item.description)
        if self.blocked:
            self.description.setText(f"please install {self.missing_dependecies} first")
        self.description.setMaximumWidth(420)
        self.label_box = QVBoxLayout()
        self.label_box.addWidget(self.title)
        self.main_layout.addSpacing(5)
        self.label_box.addWidget(self.description)
        self.label_box.setAlignment(Qt.AlignTop)
        self.label_box.setSpacing(10)

        self.main_layout.addWidget(self.icon_label)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(self.label_box)
        tooltip_text = f'author: {self.item.author} [{self.item.tags}]'
        if self.blocked:
            tooltip_text = f"{self.missing_dependecies} packages are needed to use the script. install tehm from pip \n" + tooltip_text
        self.setToolTip(tooltip_text)
        self.setLayout(self.main_layout)

        self.title.setWordWrap(True)
        self.description.setWordWrap(True)
        self.title.adjustSize()
        self.description.adjustSize()
        self.clicked.connect(self.mouse_action)

        self.label_box.setSpacing(0)
        self.main_layout.setSpacing(0)
        self.setMinimumHeight(self.title.height() + self.description.height())

    def mouse_action(self):
        if not self.blocked:
            self.parent().parent().parent().parent().parent().done(self.item.uuid)

    def paintEvent(self, QPaintEvent):
        if self.hasFocus():
            painter = QPainter(self)
            painter.fillRect(self.rect(), self.palette().highlight().color())
            if self.blocked:
                painter.fillRect(self.rect(), QColor(255, 0, 0, 130))
        else:
            painter = QPainter(self)
            painter.fillRect(self.rect(), self.palette().window().color())
            if self.blocked:
                painter.fillRect(self.rect(), QColor(255, 0, 0, 30))

class Text:

    def __init__(self, text, selected):
        self.full_text: str = text
        self.selected: str = selected
        self.text: str = text
        if selected:
            self.text: str = selected

class Item:

    def __init__(self, script, name="example name", tags="some tags spearated by space", icon="icon.png",
                 author="me",
                 description="default description", dependecies=None, icon_link=None):
        if dependecies is None:
            dependecies = []
        if not isdir(icons_path):
            os.mkdir(icons_path)
        if icon_link is not None and not isfile(join(icons_path, icon)):
            f = open(join(icons_path, icon), 'wb')
            f.write(requests.get(icon_link, allow_redirects=True).content)
            f.close()
        self.script = script
        self.name = name
        self.tags = tags
        self.dependecies = dependecies
        self.icon = join(icons_path, icon)
        self.author = author
        self.description = description
        self.uuid = randint(-2147483648, 2147483648)
        self.reload_script()
        self.itemrender = Itemrender
        self.keys = [self.name] + self.tags.split(' ')
        try:
            self.keys.remove('')
        except ValueError:
            pass

    @staticmethod
    def example(text: Text):
        return text.text
    
    def reload_script(self):
        loc = {}
        try:
            exec(self.script, globals(), loc)
            self.event = loc['func']
        except Exception as e:
            Exeption_handler(f'failed to initialize {self.name} script \n{e}', silent=False)
            self.event = Item.example
    
    def are_dependecies_present(self):
        if len(self.dependecies) < 1:
            return True
        return all([i in [i.key for i in pkg_resources.working_set] for i in self.dependecies])
    
    def get_missing_dependecies(self):
        if len(self.dependecies) < 1:
            return []
        return [i for i in self.dependecies if i not in [i.key for i in pkg_resources.working_set]]

class Settings(dict):

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.path: str = path

    def load(self, no_override=False):
        self._check_file()
        try:
            f = open(self.path, 'r')
            j = json.loads(f.read())
            f.close()
        except json.decoder.JSONDecodeError:
            f = open(self.path, 'w')
            f.write('{}')
            f.close()
        finally:
            f = open(self.path, 'r')
            j = json.loads(f.read())
            f.close()
            for key in j:
                if no_override:
                    self.setdefault(key, j[key])
                else:
                    self[key] = j[key]

    def save(self):
        self._check_file()
        f = open(self.path, "w")
        f.write(json.dumps(self, indent=2))
        f.close()

    def _check_file(self, path=None):
        if path is None:
            path = self.path

        p = path.split(os.sep)
        if path[0] == os.sep:
            p[0] = os.sep + p[0]

        for i in range(len(p) - 1):
            i += 1
            if not os.path.isdir(os.sep.join(p[:i])):
                os.mkdir(os.sep.join(p[:i]))

        if not os.path.isfile(path):
            f = open(path, 'w')
            f.write('{}')
            f.close()

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format

def search_help(my_list: list, query: str):
    for i in my_list:
        if query in i or i in query:
            return True
    return False

def get_children(layout):
    return [layout.itemAt(i).widget() for i in range(layout.count())]

def get_script_from_uuid(uuid):
    for i in items:
        if i.uuid == uuid:
            return i

def load_scripts():
    files = listdir(scripts_path)
    files.sort()
    for i in files:
        n = join(scripts_path, i)
        if not os.path.isdir(n) and isfile(n) and is_valid_script(n):
            load_script(n)

def load_script(path):
    f = open(path, 'r')
    text = f.read()
    f.close()
    data: list = text.split('# data:')
    script = text.split('# script:')[1]
    data: dict = json.loads(data[1])
    try:
        index = [i.name for i in items].index(data['name'])
    except ValueError:
        index = len(items)
        items.append(1)
    items[index] = Item(script=script, name=data['name'], author=data['author'], icon=data.get('icon'), tags=data.get('tags'),
                        description=data.get('description'), dependecies=data.get('dependecies'), icon_link=data.get('icon_link'))

def is_valid_script(path, external=False):
    if external:
        for i in listdir(scripts_path):
            if join(scripts_path, i) == path:
                return False
    if os.path.isdir(path) or not isfile(path):
        return False
    f = open(path, 'r')
    try:
        text = f.read()
    except Exception:
        return False
    f.close()
    data = text.split('# data:')
    script = text.split('# script:')
    return len(data) == 3 and len(script) == 3

def open_on_external_programm(path):
    if sys.platform == "linux" or sys.platform == "linux2":
        subprocess.call(['xdg-open', path])
    elif sys.platform == "darwin":
        subprocess.call(['open', path])
    elif sys.platform == "win32":
        subprocess.call(['start', path])

def openFileNameDialog(parent=None):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(parent, "QFileDialog.getOpenFileName()", "",
                                              "All Files (*);;Python Files (*.txt)", options=options)
    if fileName:
        return fileName

def openFileNamesDialog(parent=None):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    files, _ = QFileDialog.getOpenFileNames(parent, "QFileDialog.getOpenFileNames()", "",
                                            "All Files (*);;Python Files (*.py)", options=options)
    return files

def saveFileDialog(parent=None):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getSaveFileName(parent, "QFileDialog.getSaveFileName()", "",
                                              "All Files (*);;Text Files (*.txt)", options=options)
    if fileName:
        return fileName

def reset_scripts():
    if not isdir(base_path):
        os.mkdir(base_path)
        
    if not isdir(resources_path):
        os.mkdir(resources_path)
    for i in listdir(join(install_path ,'resources')):
        source = join(install_path ,'resources', i)
        if isfile(join(resources_path, i)):
            os.remove(join(resources_path, i))
        shutil.copy(source, resources_path)
            
    if not isdir(scripts_path):
        os.mkdir(scripts_path)
    for i in listdir(join(install_path ,'scripts')):
        source = join(install_path ,'scripts', i)
        if isfile(join(scripts_path, i)):
            os.remove(join(scripts_path, i))
        shutil.copy(source, scripts_path)

def is_first_run():
    setting = Settings(join(config_path, 'first_run.json'), first_run=True)
    setting.load()
    first_run = setting['first_run']
    if first_run:
        setting['first_run'] = False
        setting.save()
        return True
    return False

def Exeption_handler(e, silent=False):
    print('an exeption has occurred', e)
    error_dialog = QErrorMessage()
    error_dialog.showMessage(str(e))
    error_dialog.exec()
    if not silent:
        raise e

def main():
    try:
        if is_first_run():
            reset_scripts()

        load_scripts()
        window = Window()
        window.setWindowIcon(QIcon(join(resources_path, 'icon.png')))
        window.on_exit_save()
    except Exception as e:
        Exeption_handler(e)
        # raise e
    settings.save()

settings = Settings(join(config_path, 'config.json'))
settings.load()
if __name__ == "__main__":
    main()