from psychometric_tests.anagram.setup import Anagram_Setup
from psychometric_tests.anagram.widget import Anagram_Widget
from psychometric_tests.defs import QtWidgets
from psychometric_tests.shared.results_dialog import ResultsDialog


def anagram():
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])

    dialog = Anagram_Setup()
    dialog.make()
    if dialog.exec() == QtWidgets.QDialog.Accepted:
        exp_setup = dialog.setup_info
        widget = Anagram_Widget(exp_setup)
        widget.show()
        app.exec()

        app = QtWidgets.QApplication.instance()
        if app is None:
            app = QtWidgets.QApplication([])

        if exp_setup['Show Results']:
            results = ResultsDialog(widget.header, widget.record)
            results.setWindowTitle('Results ({})'.format(widget.title))
            results.exec()


if __name__ == "__main__":
    anagram()
