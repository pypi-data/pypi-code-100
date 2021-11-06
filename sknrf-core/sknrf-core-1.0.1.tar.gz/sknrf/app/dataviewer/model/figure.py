from enum import Enum
from collections.abc import MutableMapping
from collections import OrderedDict
from itertools import cycle

import torch as th
import numpy as np

from sknrf.settings import Settings
from sknrf.utilities import rf
from sknrf.widget.propertybrowser.view import Domain


class AxesType(Enum):
    Rectangular = 0
    Polar = 1
    Smith = 2


class PlotType(Enum):
    Scatter = 0
    Line = 1
    Contour = 2
    Contourf = 3


class AxisType(Enum):
    Linear = 0
    Log = 1
    LinearLog = 2  # Show log data on a linear scale.


class FormatType(Enum):
    Lin_Mag = 0
    dBm = 1
    dB = 2
    Re = 3
    Im = 4
    Angle_Deg = 5
    Angle_Rad = 6


format_map = OrderedDict((
    (FormatType.Lin_Mag, th.abs),
    (FormatType.dBm, rf.rW2dBm),
    (FormatType.dB, rf.rW2dBW),
    (FormatType.Re, rf.real),
    (FormatType.Im, rf.imag),
    (FormatType.Angle_Deg, rf.angle_deg),
    (FormatType.Angle_Rad, rf.angle)
))

options_map = {
    PlotType.Scatter: {"marker": ".", "picker": 5},
    PlotType.Line: {"pickradius": 5},
    PlotType.Contour: {"marker": ".", "markeredgewidth": 0.0, "markevery": 0.1, "markersize": 10, "picker": 5, "inline": 1, "fontsize": 10},
    PlotType.Contourf: {"marker": ".", "markeredgewidth": 0.0, "markevery": 0.1, "markersize": 10, "picker": 5, "fontsize": 50, "cmap": "plasma"}
}


class PlotModel(MutableMapping):

    def __init__(self, type=PlotType.Scatter, transform=Domain.TF, title="",
                 x_str="", x_format=FormatType.Lin_Mag, x_label="",
                 y_str="", y_format=FormatType.Lin_Mag, y_label="",
                 line_enable=False, line_style="-", line_size=2,
                 marker_enable=True, marker_style=".", marker_size=2,
                 meridian=(0, 0), options=None):
        super(PlotModel, self).__init__()
        self.type = type
        self.transform = transform
        self.title = title
        self.x_str, self.x_format, self.x_label = x_str, x_format, x_label
        self.y_str, self.y_format, self.y_label = y_str, y_format, y_label
        self.index_map = OrderedDict()
        self.line_enable, self.line_style, self.line_size = line_enable, line_style, line_size
        self.marker_enable, self.marker_style, self.marker_size = marker_enable, marker_style, marker_size
        self.meridian = meridian
        self.options = options
        self.__store = dict()
        self.update(dict())

    def __getitem__(self, key):
        return self.__store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.__store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.__store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)

    def __keytransform__(self, key):
        return key


class AxesModel(MutableMapping):

    def __init__(self, type=AxesType.Rectangular, autoscale=False, title="",
                 grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                 axis=(AxisType.Linear, AxisType.Linear), indep_axis=-1,
                 color_order=("blue", "green", "red", "violet", "cyan", "yellow", "magenta", "black")):
        super(AxesModel, self).__init__()
        self.type = type
        self.autoscale = autoscale
        self.title = title
        self.grid = grid
        self.gridspec = gridspec
        self.axis = axis
        self.indep_axis = indep_axis
        color_order = Settings().color_order if color_order is None else color_order
        color_map = Settings().color_map
        self.color_order = [color_map[color] for color in color_order]
        self.clear()
        self.__store = dict()
        self.update(dict())

    def __getitem__(self, key):
        return self.__store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.__store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.__store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)

    def __keytransform__(self, key):
        return key

    def clear(self):
        self.color_cycle = cycle(self.color_order)


class FigureModel(MutableMapping):

    def __init__(self, title="", gridspec=(1, 1)):
        super(FigureModel, self).__init__()
        self.title = title
        self.gridspec = gridspec
        self.__store = dict()
        self.update(dict())

    def __getitem__(self, key):
        return self.__store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.__store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.__store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.__store)

    def __len__(self):
        return len(self.__store)

    def __keytransform__(self, key):
        return key

    def data(self, dataset, axes_id, plot_id):
        axes_model = self[axes_id]
        plt_model = self[axes_id][plot_id]
        if len(plt_model.index_map) == 0:
            plt_model.index_map.clear()
            for index, (k, v) in enumerate(dataset.sweep_map.items()):
                plt_model.index_map[k] = slice(0, v.shape[index])
        index_filter = list(plt_model.index_map.values())
        zeros = np.zeros(dataset.shape, dtype=np.complex)
        x = (np.asarray(eval(plt_model.x_str, dataset._v_children)) + zeros)[index_filter]
        y = (np.asarray(eval(plt_model.y_str, dataset._v_children)) + zeros)[index_filter]
        # for interp_filter in plt_model.interp_filter.values():
        #     y = interp_filter(x, y)(x)
        if axes_model.type == AxesType.Rectangular:
            x = np.moveaxis(x, axes_model.indep_axis, 0).reshape(x.shape[axes_model.indep_axis], -1)
            y = np.moveaxis(y, axes_model.indep_axis, 0).reshape(y.shape[axes_model.indep_axis], -1)
        elif axes_model.type == AxesType.Polar:
            if plt_model.type in (PlotType.Line, PlotType.Scatter):
                xy = np.moveaxis(y, axes_model.indep_axis, 0).reshape(y.shape[axes_model.indep_axis], -1)
                x, y = np.angle(xy), np.abs(xy)
            else:
                x = np.moveaxis(x, axes_model.indep_axis, 0).reshape(x.shape[axes_model.indep_axis], -1)
                y = np.moveaxis(y, axes_model.indep_axis, 0).reshape(y.shape[axes_model.indep_axis], -1)
        elif axes_model.type == AxesType.Smith:
            if plt_model.type in (PlotType.Line, PlotType.Scatter):
                xy = np.moveaxis(y, axes_model.indep_axis, 0).reshape(y.shape[axes_model.indep_axis], -1)
                x, y = xy.real, xy.imag
            else:
                x = np.moveaxis(x, axes_model.indep_axis, 0).reshape(x.shape[axes_model.indep_axis], -1)
                y = np.moveaxis(y, axes_model.indep_axis, 0).reshape(y.shape[axes_model.indep_axis], -1)
        return x, y, options_map[plt_model.type]



