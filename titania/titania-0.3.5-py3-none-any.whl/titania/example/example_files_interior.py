def main_file(project_name):
    return """import sys
from PyQt5.QtWidgets import QApplication

from titania.QtGUI.main_window import MainWindow
from config import config

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    ex = MainWindow(height=height, width=width, tab_config=config)
    ex.show()
    sys.exit(app.exec_())""".format(project_name)


def config_file(project_name):
    return """from views.thresholds_gui import ThresholdsTab
""" + """config = {
    "ExampleTab": [ThresholdsTab],
}"""


def thresholds_file():
    return """from titania.common.titania_tab import TitaniaPlotTab
from titania.data.examplary_generated_data import RandomNList
from titania.plots import LinePlot


class Thresholds(TitaniaPlotTab):
    def __init__(self, plot_cls=LinePlot):
        TitaniaPlotTab.__init__(self, data=RandomNList())
        self.PlotClass = plot_cls

    def add_plots_to_layout(self):
        self.grid_layout.addLayout(self.control_panel.get_control_panel(), 0, 0)
        plot1 = self.PlotClass(parent=self.parent, widget=self).get_plot_widget(row=1)
        plot1.draw_plot(data=self.data)
        self.plot_panel_grid.addWidget(plot1, 0, 0, 1, 3)

    def set_plot(self):
        return LinePlot(parent=self)

    def set_title(self):
        return "ExampleSubTab"

    def create_control_panel(self):
        pass"""


def thresholds_tab_file():
    return """from titania.QtGUI import QtBaseLayoutTab
from titania.data.examplary_generated_data import RandomNList
from titania.plots import QtLinePlot
from views.thresholds import Thresholds
from panels.control_panel import ControlPanel


class ThresholdsTab(QtBaseLayoutTab, Thresholds):
    def __init__(self, parent=None):
        self.parent = parent
        QtBaseLayoutTab.__init__(self, data=RandomNList(), parent=parent)
        Thresholds.__init__(self, QtLinePlot)


    def add_plots_to_layout(self):
        Thresholds.add_plots_to_layout(self)

    def set_plot(self):
        return self.PlotClass(parent=self.parent, widget=self)

    def create_control_panel(self):
        return ControlPanel(widget=self)"""


def control_panel_file():
    return """from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QLabel, QComboBox, QPushButton, QTextEdit, QWidget, QCheckBox, QRadioButton

from titania.panels import ControlPanelInterface


class ControlPanel(ControlPanelInterface):
    def __init__(self, data=None, widget=None):
        self.control_panel = QGridLayout()
        self.data_buttons_group = QGridLayout()

        self.sensor_id_label = QLabel("Sensor ID:")
        self.sensor_id_combo_box = QComboBox()
        self.sensor_id_combo_box.addItem("1")
        self.sensor_id_combo_box.addItem("2")
        self.sensor_id_combo_box.addItem("3")

        self.previous_button = QPushButton("Previous")
        self.next_button = QPushButton("Next")
        self.prev_four_button = QPushButton("Prev Four")
        self.next_four_button = QPushButton("Next Four")

        self.data_buttons_group.addWidget(self.sensor_id_label, 1, 0, alignment=QtCore.Qt.AlignRight)
        self.data_buttons_group.addWidget(self.sensor_id_combo_box, 1, 1)
        self.data_buttons_group.addWidget(self.previous_button, 2, 0)
        self.data_buttons_group.addWidget(self.next_button, 2, 1)
        self.data_buttons_group.addWidget(self.prev_four_button, 3, 0)
        self.data_buttons_group.addWidget(self.next_four_button, 3, 1)

        self.notification_label = QLabel("Notifications:")
        self.notification_text_box = QTextEdit()
        self.notification_text_box.setMaximumSize(400, 600)
        self.notification_text_box.setText("TEST NOTIFICATION")

        self.split_line = QWidget()
        self.split_line.setStyleSheet("background-color:black;")
        self.split_line.setMinimumSize(400, 2)
        self.split_line.setMaximumSize(400, 2)

        self.display_references_button = QCheckBox("Display references")
        self.overlay_button = QRadioButton("Overlay")
        self.data_ref_button = QRadioButton("data - Ref")
        self.data_slash__button = QRadioButton("data/Ref")

        self.split_line2 = QWidget()
        self.split_line2.setStyleSheet("background-color:black;")
        self.split_line2.setMinimumSize(400, 2)
        self.split_line2.setMaximumSize(400, 2)

        self.run_number_label = QLabel("Run number:")

        self.run_number_combo_box = QComboBox()
        self.run_number_combo_box.addItem("12345")
        self.run_number_combo_box.addItem("54321")

        self.reference_number_label = QLabel("Reference number:")

        self.reference_number_combo_box = QComboBox()
        self.reference_number_combo_box.addItem("Auto")
        self.reference_number_combo_box.addItem("12345")
        self.reference_number_combo_box.addItem("54321")

        self.control_panel.addLayout(self.data_buttons_group, 0, 0)
        self.control_panel.addWidget(self.notification_label, 4, 0)
        self.control_panel.addWidget(self.notification_text_box, 5, 0)
        self.control_panel.addWidget(self.split_line, 6, 0)
        self.control_panel.addWidget(self.display_references_button, 7, 0)
        self.control_panel.addWidget(self.overlay_button, 8, 0)
        self.control_panel.addWidget(self.data_ref_button, 9, 0)
        self.control_panel.addWidget(self.data_slash__button, 10, 0)
        self.control_panel.addWidget(self.split_line2, 11, 0)
        self.control_panel.addWidget(self.run_number_label, 12, 0)
        self.control_panel.addWidget(self.run_number_combo_box, 13, 0)
        self.control_panel.addWidget(self.reference_number_label, 14, 0)
        self.control_panel.addWidget(self.reference_number_combo_box, 15, 0)

    def get_control_panel(self):
        return self.control_panel"""
