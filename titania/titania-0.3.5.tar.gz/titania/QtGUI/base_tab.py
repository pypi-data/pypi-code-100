from abc import ABC, abstractmethod, ABCMeta
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout

from titania.common.titania_tab import TitaniaTabInterface, TitaniaPlotTab, TitaniaPlotTabInterface
from titania.data.data_core import TitaniaDataInterface, EmptyTitaniaData
from titania.panels.main_control_panel import EmptyControlPanel, ControlPanelInterface
from titania.plots.base_plot import PlotInterface, NavToolbarPlot
from titania.plots.line_plot import QtLinePlot


class FinalMetaQtTab(type(QWidget), type(TitaniaTabInterface)):
    """
    This class helps to fix the warning of:
    'TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases'
    """
    pass


class QtTabInterface(TitaniaTabInterface, QWidget, metaclass=FinalMetaQtTab):
    def __init__(self, data: TitaniaDataInterface):
        QWidget.__init__(self)
        TitaniaTabInterface.__init__(self, data)
        self.plot_panel_grid = None
        self.lineLayout = None
        self.grid_layout = None


class QtPlotTab(QtTabInterface, TitaniaPlotTabInterface):

    def __init__(self, data: TitaniaDataInterface):
        QtTabInterface.__init__(self, data)
        TitaniaPlotTabInterface.__init__(self)

    def initiate(self):
        TitaniaPlotTabInterface.initiate(self)


class QtBaseLayoutTab(QtPlotTab):
    def __init__(self, data: TitaniaDataInterface, parent=None):
        QtPlotTab.__init__(self, data)
        self.parent = parent
        self.plot_panel_grid = QGridLayout()
        self.lineLayout = QVBoxLayout()
        self.grid_layout = QGridLayout()

    def add_layout(self):
        self.grid_layout.addLayout(self.control_panel.get_control_panel(), 0, 0)
        self.grid_layout.addLayout(self.lineLayout, 0, 1)
        self.grid_layout.addLayout(self.plot_panel_grid, 0, 2, 2, 3)

    def add_plots_to_layout(self):
        if self.plot is not None:
            self.plot_panel_grid.addWidget(self.plot.get_plot_widget(), 0, 0, 1, 3)

    def set_layout(self):
        self.setLayout(self.grid_layout)

    def set_separator_line(self):
        container = QWidget(self)
        container.setStyleSheet("background-color:black;")
        container.setMinimumWidth(2)
        container.setMaximumWidth(2)
        container.showMaximized()
        self.lineLayout.addWidget(container)

    def construct(self):
        self.set_separator_line()
        self.add_layout()
        self.add_plots_to_layout()
        self.set_layout()

    def initiate_for_web(self):
        QtPlotTab.initiate(self)

    def initiate(self):
        QtPlotTab.initiate(self)
        self.construct()

    def set_plot(self):
        return NavToolbarPlot(widget=self)

    def is_web(self):
        return False


class SimpleTab(QtBaseLayoutTab):
    def __init__(self, data=None, parent=None, control_panel=EmptyControlPanel):
        data = data if data is not None else EmptyTitaniaData()
        self.control_panel = control_panel
        QtBaseLayoutTab.__init__(self, data, parent)

    def set_title(self):
        return "Base Title"

    def create_control_panel(self):
        return self.control_panel(data=self.data, widget=self)

    def set_plot(self):
        return QtLinePlot(widget=self)

    def initiate(self):
        QtBaseLayoutTab.initiate(self)


class CommonBase(QtBaseLayoutTab, TitaniaPlotTab, metaclass=ABCMeta):
    def __init__(self, data=EmptyTitaniaData(), parent=None):
        if self.is_web():
            TitaniaPlotTab.__init__(self, data=data)
        else:
            QtBaseLayoutTab.__init__(self, data=data, parent=parent)
