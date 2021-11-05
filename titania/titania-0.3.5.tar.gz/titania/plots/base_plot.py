from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class PlotInterface(ABC):

    @abstractmethod
    def get_plot_widget(self):
        pass

    def pre_draw(self):
        pass

    @abstractmethod
    def draw_plot(self):
        pass


class FinalMetaPlot(type(PlotInterface), type(FigureCanvas)):
    pass


class BaseCanvasPlot(PlotInterface, FigureCanvas, metaclass=FinalMetaPlot):
    def __init__(self, parent=None, widget=None):
        plt.rcParams.update({'figure.max_open_warning': 0})
        self.parent = parent
        self.plot_number = 111
        self.figure = plt.figure()
        self.widget = widget
        FigureCanvas.__init__(self, self.figure)

    def get_plot_widget(self):
        return self


class MplPlot(BaseCanvasPlot):
    def get_plot_widget(self, row=0):
        return self

    def pre_draw(self):
        self.figure.clear()


class NavToolbarPlot(MplPlot):

    def get_plot_widget(self, row=10):
        self.toolbar = NavigationToolbar(self, self.widget)
        self.widget.plot_panel_grid.addWidget(self.toolbar, row, 1)
        return self

    def draw_plot(self):
        ax = self.figure.add_subplot(self.plot_number)
        ax.plot(self.widget.data.fetch(), '*-')
        self.draw()
