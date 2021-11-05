#
# import subprocess
#
# subprocess.check_call(["python3", "../../src/main.py"])

import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../resources")

from titania.QtGUI.base_tab import SimpleTab
from titania.QtGUI.main_window import MainWindow
from titania.plots.line_plot import QtLinePlot


import sys
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)


class MainWindowTest(unittest.TestCase):

    def setUp(self):
        self.config_dict = {
            "VELOView": [],
            "RUNView": []
        }

    def test_framework_tabs_creation(self):
        # GIVEN 4 tabs only
        self.assertEqual(0, len(self.config_dict['RUNView']))

        # WHEN add tab to app
        self.config_dict['RUNView'].append(JustForTest)
        self.main_window = MainWindow(tab_config=self.config_dict)
        main_tabs = []
        for i in range(self.main_window.top_tab.count()):
            main_tabs.append(self.main_window.top_tab.widget(i))

        # THEN app got 2 main tabs
        self.assertEqual(2, len(main_tabs))

        # maybe put some mock in the future
        self.assertEqual(1, main_tabs[1].child_tab.count())

    def test_framework_deleting_tabs(self):
        # GIVEN 4 tabs only
        self.assertEqual(0, len(self.config_dict['RUNView']))

        # WHEN add  tab from Runview
        self.config_dict['RUNView'].append(JustForTest)
        self.main_window = MainWindow(tab_config=self.config_dict)
        main_tabs = []
        for i in range(self.main_window.top_tab.count()):
            main_tabs.append(self.main_window.top_tab.widget(i))

        self.assertEqual(2, len(main_tabs))

        # THEN app got 3 tabs
        self.assertEqual(1, main_tabs[1].child_tab.count())
        self.config_dict['RUNView'].append(JustForTest)


class JustForTest(SimpleTab):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()

    def set_plot(self):
        return QtLinePlot(parent=self.parent, widget=self)

    def set_title(self):
        return "TestPlot"


if __name__ == "__main__":
    unittest.main()
