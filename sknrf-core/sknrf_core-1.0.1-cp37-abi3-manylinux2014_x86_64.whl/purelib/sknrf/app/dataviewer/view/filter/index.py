import logging
from collections import OrderedDict

import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import QSignalMapper
from PySide2.QtWidgets import QFrame
import matplotlib as mpl

from sknrf.app.dataviewer.view.filter.QIndexFrame import Ui_indexFrame
from sknrf.app.dataviewer.view.filter.widget import RealFilter, ComplexFilter

logger = logging.getLogger()


class IndexFrame(QFrame, Ui_indexFrame):

    def __init__(self, parent=None):
        super(IndexFrame, self).__init__(parent=parent)
        self.setupUi(self)

        self._parent = None
        self._filter_signal_mapper = QSignalMapper(self)
        self.dataset = None
        self._filter_frames = OrderedDict()
        self._x_value = None
        self._y_value = None
        self._model = OrderedDict()

    def connect_signals(self):
        self.markerToolButton.clicked.connect(self.toggle_markers)

    def disconnect_signals(self):
        self.markerToolButton.clicked.disconnect()

    def connect_filter_signals(self):
        self._filter_signal_mapper = QSignalMapper(self)
        for index, (k, v) in enumerate(self._filter_frames.items()):
            v.filter_changed.connect(self._filter_signal_mapper.map)
            self._filter_signal_mapper.setMapping(v, index)
        self._filter_signal_mapper.mapped.connect(self.set_filter)

    def disconnect_filter_signals(self):
        try:
            self._filter_signal_mapper.mapped.disconnect(self.set_filter)
            for index, (k, v) in enumerate(self._filter_frames.items()):
                v.filter_changed.disconnect(self._filter_signal_mapper.map)
        except RuntimeError:
            pass

    def gcf(self):
        return self._parent.gcf()

    def gca(self):
        return self._parent.gca()

    def sca(self, ax):
        self._parent.sca(ax)

    def gcp(self):
        return self._parent.gcp()

    def scp(self, artist):
        self._parent.scp(artist)

    @QtCore.Slot()
    def toggle_markers(self):
        if self.markerToolButton.isChecked():
            self.set_interactive_tool(self.markerToolButton)
            size = mpl.rcParams['lines.markersize']
        else:
            size = 0.0
        fig = self.gcf()
        if len(fig.axes) == 0:
            return
        ax = self.gca()
        for ln in ax.lines:
            ln.set_markersize(size)
        fig.canvas.draw()

    def set_interactive_tool(self, action):
        self.markerToolButton.setChecked(action == self.markerToolButton)

    def model(self):
        return self._model

    def set_model(self, model):
        """Update the filters widgets.
        """
        try:
            self.clear_filters()
            for index, (k, v) in enumerate(self.dataset.sweep_map.items()):
                if v is not self._x_value:
                    slice_ = [0] * v.ndim
                    slice_[index] = model[k]
                    if v.dtype == np.complex:
                        self._filter_frames[k] = ComplexFilter(k, v[slice_], parent=self.filtersToolbox)
                    else:
                        self._filter_frames[k] = RealFilter(k, v[slice_], parent=self.filtersToolbox)
                    self.filtersToolbox.addItem(self._filter_frames[k], k)
        finally:
            self._model = model
            self.connect_filter_signals()

    def clear_filters(self):
        self.disconnect_filter_signals()
        for index in reversed(range(self.filtersToolbox.count())):
            filter_ = self.filtersToolbox.widget(index)
            self.filtersToolbox.removeItem(index)
            filter_.deleteLater()
        self._filter_frames = OrderedDict()
        self._model = OrderedDict()

    @QtCore.Slot(int)
    def set_filter(self, index):
        """Set the indexed filter widget.

            Parameters
            ----------
            index : int
                    The index of the selected filter (The dimension of the dataset).
        """
        key = list(self._filter_frames.keys())[index]
        filter_frame = self._filter_frames[key]
        if isinstance(filter_frame, ComplexFilter):
            self._model[key] = filter_frame.ind
        else:
            self._model[key] = slice(filter_frame.lower_index(), filter_frame.upper_index() + 1, 1)
        self.update(plots=True)

    def update(self, plots=False):
        super(IndexFrame, self).update()
        self._parent.update(plots=plots)
