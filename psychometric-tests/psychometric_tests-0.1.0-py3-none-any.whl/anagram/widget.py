import random
import time
from distutils.util import strtobool
from itertools import cycle
from pathlib import Path

import psychometric_tests.shared.misc_funcs as mf
from psychometric_tests import defs
from psychometric_tests.defs import QtCore, QtGui, QtWidgets
from psychometric_tests.shared.colours import tab10_rgb

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class Anagram_Widget(QtWidgets.QWidget):
    def __init__(self, setup_info):
        super().__init__()

        self.init_file = str(defs.project_root() / 'anagram.ini')
        self.settings = defs.settings()['anagram']
        self.title = 'Anagram Task'
        self.setWindowIcon(
            QtGui.QIcon(str(defs.resource_dir() / 'anagram.svg')))
        self.main_layout = QtWidgets.QVBoxLayout(self)

        self.setup_info = setup_info
        self.save_path = Path(
            setup_info['Save Directory']) / self.settings['save_name'].format(
            **setup_info)
        self.timeout = setup_info['Duration']  # minutes
        self.show_sol = setup_info['Show Solution']
        self.sol_shown = False

        self.questions = mf.read_csv(
            defs.anagram_ques_dir() / setup_info['Test Questions'],
            encoding='utf-8')
        random.shuffle(self.questions)

        self.header = ['index', 'Q_num', 'question', 'solution',
                       'input', 'duration', 'correct?']

        self.ques_count = 0
        self.current_ques_num = None
        self.current_ques = None
        self.current_sol = None
        self.colours = list(tab10_rgb.values())

        # results
        self.record = []
        self.in_answer = {}

        self.title_font = QtGui.QFont(self.settings['title_font'],
                                      self.settings['title_font_size'],
                                      self.settings['title_font_weight'])
        self.ques_font = QtGui.QFont(self.settings['ques_font'],
                                     self.settings['ques_font_size'],
                                     self.settings['ques_font_weight'])
        self.answer_font = QtGui.QFont(self.settings['answer_font'],
                                       self.settings['answer_font_size'],
                                       self.settings['answer_font_weight'])
        self.sol_font = QtGui.QFont(self.settings['sol_font'],
                                    self.settings['sol_font_size'],
                                    self.settings['sol_font_weight'])

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.title_label = QtWidgets.QLabel(self)
        self.question_frame, self.sentence_blocks = QtWidgets.QFrame(self), []
        self.answer_frame = QtWidgets.QFrame(self)
        self.answer_frame.setMinimumHeight(100)
        self.answer_layout = QtWidgets.QHBoxLayout(self.answer_frame)
        self.next_button = QtWidgets.QPushButton(self)
        self.sol_label = QtWidgets.QLabel(self)
        self.ques_timer_label = QtWidgets.QLabel(self)
        self.glob_timer_label = QtWidgets.QLabel(self)

        self.setup_ui()

        self.refresh_clock_timer = QtCore.QTimer()
        self.refresh_clock_timer.timeout.connect(self.update_timer_labels)
        self.ques_start_time = time.time()
        self.end_timer = QtCore.QTimer()
        self.end_timer.timeout.connect(self.close)  # close programme at timeout

        self.next_button.clicked.connect(self.next_button_pressed)

    def setup_ui(self):
        self.resize(650, 500)
        self.setWindowTitle(self.title)
        self.setLayout(self.main_layout)

        self.title_label.setText(self.settings["intro_text1"])
        self.title_label.setStyleSheet(self.settings['intro_text1_style'])
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(self.title_font)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch()

        self.question_frame, self.sentence_blocks = \
            self.create_question_frame([self.settings["intro_text2"]])
        for obj in self.answer_frame.children():
            if isinstance(obj, QtWidgets.QLabel):
                obj.setStyleSheet(self.settings['intro_text2_style'])
        self.main_layout.addWidget(self.question_frame)
        self.main_layout.addStretch()

        self.answer_frame = QtWidgets.QFrame(self)
        self.answer_frame.setMinimumHeight(100)
        self.answer_layout = QtWidgets.QHBoxLayout(self.answer_frame)
        self.answer_layout.addStretch()
        self.answer_layout.addStretch()
        self.main_layout.addWidget(self.answer_frame)
        self.main_layout.addStretch()

        if self.show_sol:
            sol_layout = QtWidgets.QHBoxLayout()
            sol_layout.addStretch()
            sol_layout.addWidget(self.sol_label)
            self.sol_label.setFont(self.sol_font)
            sol_layout.addStretch()

            self.main_layout.addLayout(sol_layout)
        else:
            self.main_layout.addStretch()
        self.main_layout.addStretch()

        self.next_button.setText(self.settings['next_button_text'])
        self.next_button.setFont(self.title_font)
        self.main_layout.addWidget(self.next_button)

        timer_layout = QtWidgets.QHBoxLayout()
        self.glob_timer_label.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        timer_layout.addWidget(self.glob_timer_label)
        timer_layout.addStretch()
        self.ques_timer_label.setAlignment(
            QtCore.Qt.AlignTop | QtCore.Qt.AlignRight)
        timer_layout.addWidget(self.ques_timer_label)

        self.main_layout.insertLayout(0, timer_layout)

        if Path(self.init_file).is_file():
            settings = QtCore.QSettings(self.init_file,
                                        QtCore.QSettings.IniFormat)
            self.gui_restore(settings)

    def create_question_frame(self, sentence_parts):
        question_frame = QtWidgets.QFrame(self)
        h_layout = QtWidgets.QHBoxLayout(question_frame)
        question_frame.setLayout(h_layout)

        color = cycle(self.colours)
        sentence_blocks = []
        for text in sentence_parts:
            button = QtWidgets.QPushButton(question_frame)
            button.setFlat(True)
            button.setText('{}'.format(text))
            button.setFont(self.ques_font)
            button.pressed.connect(self.block_pressed)
            button.setFocusPolicy(QtCore.Qt.NoFocus)
            button.setStyleSheet(f'color: rgb{str(next(color))};')
            h_layout.addWidget(button, alignment=QtCore.Qt.AlignCenter)
            sentence_blocks.append(button)

        return question_frame, sentence_blocks

    def block_pressed(self):
        if self.sender() in self.in_answer:
            self.remove_block_from_answer(self.sender())
        else:
            self.add_block_to_answer(self.sender())

    def add_block_to_answer(self, block):
        text = block.text()
        style = block.styleSheet()
        answer_block = QtWidgets.QLabel(
            self.answer_frame, text=text, font=self.answer_font)
        answer_block.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                   QtWidgets.QSizePolicy.Minimum)
        answer_block.setStyleSheet(style)

        self.in_answer[block] = answer_block
        self.answer_layout.insertWidget(len(self.in_answer), answer_block,
                                        alignment=QtCore.Qt.AlignCenter)

    def remove_block_from_answer(self, block):
        self.in_answer[block].deleteLater()
        del self.in_answer[block]

    def update_timer_labels(self):
        self.glob_timer_label.setText(
            'Time Remaining\n' + mf.convert_time(
                float(self.end_timer.remainingTime()) / 1000))
        self.ques_timer_label.setText(
            'Question Duration\n' + mf.convert_time(
                time.time() - self.ques_start_time))

    def next_question(self):
        self.ques_count += 1
        if self.ques_count > len(self.questions):
            self.close()
        else:
            ques_row = list(filter(None, self.questions[self.ques_count - 1]))

            self.current_ques_num = ques_row[0]
            self.current_ques = random.sample(ques_row[1:], len(ques_row[1:]))
            self.current_sol = ques_row[1:]

            self.title_label.setText(
                self.settings['question_format'].format(self.ques_count))
            frame_index = self.main_layout.indexOf(self.question_frame)
            self.question_frame.deleteLater()
            self.question_frame, self.sentence_blocks = \
                self.create_question_frame(self.current_ques)
            self.main_layout.insertWidget(frame_index, self.question_frame)

            self.in_answer = {}
            for obj in self.answer_frame.children():
                if isinstance(obj, QtWidgets.QLabel):
                    obj.deleteLater()

            self.ques_start_time = time.time()  # restart duration 'timer'

    def record_answer(self):
        ans = [a.text() for a in self.in_answer.keys()]
        duration = time.time() - self.ques_start_time
        correct = True if ans == self.current_sol else False
        self.record.append([self.ques_count,
                            self.current_ques_num,
                            self.settings['delimiter'].join(self.current_ques),
                            self.settings['delimiter'].join(self.current_sol),
                            self.settings['delimiter'].join(ans), duration, correct])
        return ans, correct

    def next_button_pressed(self):
        if self.ques_count > 0:
            if len(self.in_answer) == len(self.current_ques):
                if not self.show_sol:
                    self.record_answer()
                    self.next_question()
                else:
                    if self.sol_shown:
                        self.question_frame.setDisabled(False)
                        self.sol_label.setText('')
                        self.sol_shown = False
                        self.next_question()
                    else:
                        ans, correct = self.record_answer()
                        self.question_frame.setDisabled(True)
                        if correct:
                            self.sol_label.setText('\u2713')
                            self.sol_label.setStyleSheet('color: blue')
                        else:
                            self.sol_label.setText(self.settings['delimiter'].join(self.current_sol))
                            self.sol_label.setStyleSheet('color: red')
                        self.sol_shown = True

            else:
                QtWidgets.QMessageBox.critical(self, 'Error', self.settings['use_all_button_text'])
        else:
            self.title_label.setStyleSheet("")
            self.end_timer.start(int(self.timeout * 60 * 1000))
            self.refresh_clock_timer.start(30)
            self.next_question()

    def save_results(self):
        try:
            self.save_path.parent.mkdir(exist_ok=True)
            mf.save_csv(self.save_path, self.record, self.header,
                        encoding=self.setup_info['Save Encoding'])
        except Exception as error:
            QtWidgets.QMessageBox.critical(self, 'Error',
                                           'Could not save!\n{}'.format(error))

    def closeEvent(self, event):
        self.save_results()
        settings = QtCore.QSettings(self.init_file,
                                    QtCore.QSettings.IniFormat)
        self.gui_save(settings)
        event.accept()

    def wheelEvent(self, wheel_event):
        if QtWidgets.QApplication.keyboardModifiers() \
                == QtCore.Qt.ControlModifier:
            fontsize_title = self.title_font.pointSize()
            fontsize_answer = self.answer_font.pointSize()
            fontsize_ques = self.ques_font.pointSize()
            fontsize_sol = self.sol_font.pointSize()
            if wheel_event.angleDelta().y() > 0:
                fontsize_title += 4
                fontsize_answer += 4
                fontsize_ques += 4
                fontsize_sol += 4
                self.title_font.setPointSize(fontsize_title)
                self.answer_font.setPointSize(fontsize_answer)
                self.ques_font.setPointSize(fontsize_ques)
                self.sol_font.setPointSize(fontsize_sol)
            elif wheel_event.angleDelta().y() < 0:
                fontsize_title -= 4
                fontsize_answer -= 4
                fontsize_ques -= 4
                fontsize_sol -= 4
                self.title_font.setPointSize(fontsize_title)
                self.answer_font.setPointSize(fontsize_answer)
                self.ques_font.setPointSize(fontsize_ques)
                self.sol_font.setPointSize(fontsize_sol)

            self.title_label.setFont(self.title_font)
            for button in self.sentence_blocks:
                button.setFont(self.ques_font)

            for obj in self.answer_frame.children():
                if isinstance(obj, QtWidgets.QLabel):
                    obj.setFont(self.answer_font)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        event.accept()

    def gui_save(self, settings):
        settings.setValue('Widget/geometry', self.saveGeometry())
        settings.setValue('Widget/maximized', self.isMaximized())
        settings.setValue('Widget/full_screen', self.isFullScreen())

        defs.update_settings('anagram', 'title_font_size',
                             self.title_font.pointSize())
        defs.update_settings('anagram', 'ques_font_size',
                             self.ques_font.pointSize())
        defs.update_settings('anagram', 'answer_font_size',
                             self.answer_font.pointSize())
        defs.update_settings('anagram', 'sol_font_size',
                             self.sol_font.pointSize())

    def gui_restore(self, settings):
        if settings.value('Widget/geometry') is not None:
            self.restoreGeometry(settings.value('Widget/geometry'))
        if settings.value('Widget/maximized') is not None:
            if strtobool(settings.value('Widget/maximized')):
                self.showMaximized()
        if settings.value('Widget/full_screen') is not None:
            if strtobool(settings.value('Widget/full_screen')):
                self.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    exp_setup = {'Participant ID': '1',
                 'Session': 'A',
                 'Date-Time': '',
                 'Duration': 5.0,
                 'Test Questions': '8_letters.csv',
                 'Save Encoding': 'utf-8',
                 'Show Solution': True,
                 'Save Directory': ''}

    widget = Anagram_Widget(exp_setup)
    widget.show()

    widget.title_label.setText('')

    app.exec()
