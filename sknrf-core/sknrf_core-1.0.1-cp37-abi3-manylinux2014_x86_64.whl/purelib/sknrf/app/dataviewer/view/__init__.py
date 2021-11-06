__author__ = 'dtbespal'


class DataViewerView:

    def __init__(self):
        self.pre_plot_widget = DataViewerPrePlotView()
        self.post_plot_widget = DataViewerPostPlotView()
        self.plot_tabs = 0
        self.current_tab = 0
        self.current_axis = 0
        self.current_plot = 0


class DataViewerPlotTab:

    def __int__(self):
        self.num_rows = 1
        self.num_cols = 1
        self.current_axis = 0
        self.current_plot = 0


class DataViewerPrePlotView:

    def __int__(self):
        self.plot_selector_panel = 0
        self.dataset_tab_container = 0
        self.dataset_panel = 0
        self.equation_panel = 0

    def dataset_tab_selected(self):
        pass

    def minimize(self):
        pass

    def close(self):
        pass


class DataViewerPostPlotView:

    def __int__(self):
        self.plot_property_table = 0
        self.filter_tab_container = 0
        self.real_filters_panel = 0
        self.complex_filters_panel = 0

    def filter_tab_selected(self):
        pass

    def minimize(self):
        pass

    def close(self):
        pass


