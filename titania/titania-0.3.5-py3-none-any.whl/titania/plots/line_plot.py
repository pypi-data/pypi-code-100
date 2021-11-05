from titania.plots.base_plot import NavToolbarPlot, MplPlot

class LinePlot(MplPlot):
    def __init__(self, parent=None, *args, **kwargs):
        MplPlot.__init__(self, parent=parent)

    def draw_plot(self, data=None):
        self.figure.clear()
        ax = self.figure.add_subplot(self.plot_number)
        ax.plot(self.parent.data.fetch(), '*-')
        self.draw()


class QtLinePlot(NavToolbarPlot):
    def __init__(self, parent=None, widget=None):
        NavToolbarPlot.__init__(self, parent=parent, widget=widget)

    def draw_plot(self, data=None):
        self.figure.clear()
        ax = self.figure.add_subplot(self.plot_number)
        ax.plot(self.widget.data.fetch(), '*-')
        self.draw()

    def get_name(self):
        return "asd"
