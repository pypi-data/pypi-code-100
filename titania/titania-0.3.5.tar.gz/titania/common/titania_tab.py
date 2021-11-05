from abc import ABC, abstractmethod
from titania.data.data_core import TitaniaDataInterface
from titania.plots.base_plot import PlotInterface


class TitaniaTabInterface(ABC):
    def __init__(self, data: TitaniaDataInterface):
        self.data = data
        self.title = self.set_title()
        self.control_panel = self.create_control_panel()

    @abstractmethod
    def create_control_panel(self):
        pass

    @abstractmethod
    def set_title(self):
        pass

    @abstractmethod
    def initiate(self):
        pass


class TitaniaPlotTabInterface(ABC):

    @abstractmethod
    def set_plot(self) -> PlotInterface:
        pass

    def initiate(self):
        self.plot = self.set_plot()
        self.plot.pre_draw()
        self.plot.draw_plot()


class TitaniaPlotTab(TitaniaTabInterface, TitaniaPlotTabInterface):

    def __init__(self, data: TitaniaDataInterface):
        TitaniaTabInterface.__init__(self, data=data)
        TitaniaPlotTabInterface.__init__(self)

    def initiate(self):
        TitaniaPlotTabInterface.initiate(self)
