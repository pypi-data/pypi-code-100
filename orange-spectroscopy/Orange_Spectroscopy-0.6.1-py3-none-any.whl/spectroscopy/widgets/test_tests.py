import unittest

from AnyQt.QtCore import pyqtSignal as Signal
from AnyQt.QtTest import QTest

from Orange.widgets.tests.base import WidgetTest
from Orange.widgets.widget import OWWidget


class OWCrash(OWWidget):

    crash_w_signal = Signal()

    def __init__(self):
        self.crash_w_signal.connect(self.crash)

    def crash(self):
        print("WIDGET: I should crash")
        crashAndBurn

    def crash_through_signal(self):
        self.crash_w_signal.emit()


class TestCrash(WidgetTest):

    def setUp(self):
        self.widget = self.create_widget(OWCrash)

    def test_explicit(self):
        print("explicit")
        self.widget.crash()

    def test_signal(self):
        print("implicit")
        self.widget.crash_through_signal()
        QTest.qWait(1000)
        print("I even waited but I passed.")


if __name__ == "__main__":
    unittest.main()
