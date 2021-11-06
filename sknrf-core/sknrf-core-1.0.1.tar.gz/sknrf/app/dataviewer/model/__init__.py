__author__ = 'dtbespal'

from sknrf.app.dataviewer.model.dataset import DatagroupModel
from sknrf.app.dataviewer.model.equation import DatasetEquationModel
from PySide2.QtGui import QStandardItemModel

class DataViewerModel():

    def __init__(self):
        self.dataset_groups_list = QStandardItemModel()
        self.equations_list = QStandardItemModel()
        self.dataset_map = ()

    def add_dataset(self, dataset):
        pass

    def remove_dataset(self, name):
        pass

    def add_equation(self, name, value):
        pass

    def remove_equation(self, name):
        pass

    def swap_equation(self, name1, name2):
        pass


class PlotDataModel():

    def __init__(self):
        self.category = 0
        self.type = 0
        self.args_string = []
        self.args = []
        self.options = []

    def eval(self, dataset_map):
        pass



