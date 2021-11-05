from titania.plots.base_plot import NavToolbarPlot


class RootScatterPlot(NavToolbarPlot):
    def __init__(self, parent=None, widget=None):
        NavToolbarPlot.__init__(self, parent=parent, widget=widget)

    def draw_plot(self):
        self.figure.clear()
        data = self.widget.data.fetch()
        ax = self.figure.add_subplot(self.plot_number)
        data.plot(x='one', y='two', kind='scatter', ax=ax)
        self.draw()

    def get_name(self):
        return "asd"
