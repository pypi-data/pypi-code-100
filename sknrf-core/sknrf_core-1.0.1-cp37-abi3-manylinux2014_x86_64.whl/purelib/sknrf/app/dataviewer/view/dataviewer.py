import os
import logging
import webbrowser
import pickle
from collections import OrderedDict

import numpy as np
from numpy.core import defchararray as np_str
from PySide2.QtGui import QIcon
from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QDialog, QFileDialog, QWidget
from PySide2.QtWidgets import QSizePolicy
import matplotlib as mpl
from matplotlib.gridspec import GridSpec

from sknrf.settings import Settings
from sknrf.app.dataviewer.model.figure import PlotType
from sknrf.app.dataviewer.model.figure import FigureModel, AxesModel
from sknrf.app.dataviewer.view.QDataViewer import Ui_QDataViewer
from sknrf.app.dataviewer.view.QNewFigure import Ui_QNewFigureDialog
from sknrf.app.dataviewer.view.figure import ContentFigure

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NewFigureDialog(Ui_QNewFigureDialog, QDialog):

    def __init__(self, parent=None):
        super(NewFigureDialog, self).__init__(parent)
        self.setupUi(self)


class DataViewer(Ui_QDataViewer, QMainWindow):
    """Data Viewer for multi-dimensional datagroups.
        The data viewer can import the following formats:

        Examples
        --------
        * HDF Group HDF5
        * Mathworks MAT
        * Keysight MDIF
        * Touchstone SNP
        * Maury Microwaves SPL (Partial Support
        * Focus Microwaves LPC (Partial Support)
    """
    def __init__(self, parent=None):
        super(DataViewer, self).__init__(parent)
        self.setupUi(self)
        icon_path = os.path.join(mpl.rcParams['datapath'], 'images')
        self.actionSubplots.setIcon(QIcon(os.path.join(icon_path, 'subplots.png')))
        self.actionUndo.setIcon(QIcon(os.path.join(icon_path, 'back.png')))
        self.actionRedo.setIcon(QIcon(os.path.join(icon_path, 'forward.png')))
        # Right Align Measurement Buttons of Toolbar
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolBar.insertWidget(self.actionExport, empty)
        self._tab_map = OrderedDict()
        self._tab = None
        self.datagroupFrame._parent = self
        self.equationFrame._parent = self
        self.indexFrame._parent = self
        self.imageFrame._parent = self
        self.splitter.setSizes([1, 1000])

        self.connect_signals()
        self.set_model({})
        self.update()

    def connect_signals(self):
        self.actionNew.triggered.connect(self.add_tab)
        self.actionLoad.triggered.connect(self.load_tab)
        self.actionSave.triggered.connect(self.save_tab)

        self.actionExport.triggered.connect(self.save_figure)
        self.actionUndo.triggered.connect(self.undo_figure)
        self.actionRedo.triggered.connect(self.redo_figure)
        self.actionRefresh.triggered.connect(self.refresh_figure)
        self.actionSettings.triggered.connect(self.open_figure_settings)
        self.actionHelp.triggered.connect(self.open_documentation)
        self.actionClear.triggered.connect(self.clear_figure)

        self.contentTabWidget.currentChanged.connect(self.sct)
        self.contentTabWidget.tabCloseRequested.connect(self.remove_tab)

        self.datagroupFrame.connect_signals()
        self.datagroupFrame.datasetChanged.connect(self.set_dataset)
        self.equationFrame.axesChanged.connect(self.set_index)

    def disconnect_signals(self):
        self.actionNew.triggered.disconnect()
        self.actionLoad.triggered.disconnect()
        self.actionSave.triggered.disconnect()

        self.actionExport.triggered.disconnect()
        self.actionUndo.triggered.disconnect()
        self.actionRedo.triggered.disconnect()
        self.actionRefresh.triggered.disconnect()
        self.actionSettings.triggered.disconnect()
        self.actionHelp.triggered.disconnect()
        self.actionClear.triggered.disconnect()

        self.contentTabWidget.currentChanged.disconnect()
        self.contentTabWidget.tabCloseRequested.disconnect()

        self.datagroupFrame.disconnect_signals()
        self.datagroupFrame.datasetChanged.disconnect()
        self.equationFrame.axesChanged.disconnect()

    def connect_figure_signals(self):
        if self._tab:
            self.equationFrame.connect_signals()
            self.indexFrame.connect_signals()
            self.imageFrame.connect_signals()

            self._tab.connect_signals()
            self._tab.axesSelected.connect(self.equationFrame.set_axes)
            self._tab.addLegend.connect(self.set_legend)
            self._tab.removeLegend.connect(self.remove_legend)

    def disconnect_figure_signals(self):
        if self._tab:
            self.equationFrame.disconnect_signals()
            self.indexFrame.disconnect_signals()
            self.imageFrame.disconnect_signals()

            self._tab.disconnect_signals()
            self._tab.axesSelected.disconnect()
            self._tab.addLegend.disconnect()
            self._tab.removeLegend.disconnect()

    def model(self):
        return self._model

    def set_model(self, model):
        self.disconnect_signals()
        try:
            self._model = model
        finally:
            self.connect_signals()

    @QtCore.Slot()
    def save_figure(self):
        self.gctb().save_figure()

    @QtCore.Slot()
    def undo_figure(self):
        self.gctb().back()

    @QtCore.Slot()
    def redo_figure(self):
        self.gctb().forward()

    @QtCore.Slot()
    def refresh_figure(self):
        self.gctb().refresh()

    @QtCore.Slot()
    def open_figure_settings(self):
        self.gctb().configure_subplots()

    @QtCore.Slot()
    def clear_figure(self):
        self.gctb().clear_figure()
        self._model[self.gcf().get_gid()].clear()
        self.equationFrame.set_model(AxesModel())
        self.equationFrame.selectedAxesComboBox.clear()
        self.equationFrame.selectedAxesComboBox.addItem("< New Axes >")
        self.equationFrame.update()

    @QtCore.Slot()
    def open_documentation(self):
        webbrowser.open(os.pathsep.join((Settings().doc_root, "dataviewer.html")))

    @QtCore.Slot(object)
    def set_dataset(self, dataset):
        self.equationFrame.dataset = dataset
        self.equationFrame.set_equations()
        self.indexFrame.dataset = dataset
        self.indexFrame._x_value = None
        self.indexFrame._y_value = None

    @QtCore.Slot()
    def add_tab(self):
        base_name = "untitled"
        count = 0
        fig_id = base_name
        while fig_id in self._tab_map:
            count += 1
            fig_id = "%s%d" % (base_name, count)
        dialog = NewFigureDialog(self)
        if dialog.exec():
            fig_id, w, h = dialog.nameLineEdit.text(), dialog.widthGridSpinBox.value(), dialog.heightGridSpinBox.value()
            tab = ContentFigure(self, gridspec=GridSpec(h, w))
            fig_model = FigureModel(fig_id, gridspec=(h, w))
            self._model[fig_id] = fig_model
            tab.figure.set_gid(fig_id)
            index = self.contentTabWidget.addTab(tab, fig_id)
            self.contentTabWidget.setCurrentIndex(index)
        self.update()

    @QtCore.Slot(int)
    def remove_tab(self, index):
        self._model.pop(self.gcf().get_gid())
        self.contentTabWidget.removeTab(index)
        index = self.contentTabWidget.currentIndex()
        self.contentTabWidget.setCurrentIndex(index)
        self.update()

    @QtCore.Slot()
    def load_tab(self):
        filename = QFileDialog.getOpenFileName(self, 'Load Figure',
                                               os.sep.join((Settings().data_root, "figures")),
                                               "Figure (*.fig)",
                                               "figure.fig",
                                               QFileDialog.AnyFile)

        if len(filename[0]):
            if self.datagroupFrame._dataset is None:
                raise ValueError("Cannot load a figure without a selected dataset.")
            state = pickle.load(open(filename[0], "rb"))
            fig_id = state["name"]
            fig_model = state["model"]
            tab = ContentFigure(self, gridspec=GridSpec(*fig_model.gridspec))
            self._model[fig_id] = fig_model
            tab.figure.set_gid(fig_id)
            index = self.contentTabWidget.addTab(tab, fig_id)
            self.contentTabWidget.setCurrentIndex(index)
            self.indexFrame.clear_filters()
            for ax_id, ax_model in fig_model.items():
                self.equationFrame.set_model(fig_model[ax_id])
                for plt_id in ax_model.keys():
                    plt_model = fig_model[ax_id][plt_id]
                    self.set_plot(fig_model, ax_id, ax_model, plt_id, plt_model)
                    self.equationFrame.selectedAxesComboBox.addItem(ax_id)
            plt_model = self.equationFrame.gcp_model()
            self.equationFrame.set_x_format(plt_model.x_str, plt_model.transform)
            self.equationFrame.set_y_format(plt_model.y_str, plt_model.transform)
            self.set_index(self.equationFrame._x_value, self.equationFrame._y_value)

    @QtCore.Slot()
    def save_tab(self):
        filename = QFileDialog.getSaveFileName(self, 'Save Figure',
                                               os.sep.join((Settings().data_root, "figures")),
                                               "Figure (*.fig)",
                                               "figure.fig",
                                               QFileDialog.AnyFile)

        if len(filename[0]):
            state = {}
            state["name"] = self.gcf().get_gid()
            state["model"] = self._model[self.gcf().get_gid()]
            pickle.dump(state, open(filename[0], "wb"))

    def gct(self):
        return self._tab

    @QtCore.Slot(int)
    def sct(self, index):
        self.disconnect_figure_signals()
        if index == -1:
            self._tab = None
            return None
        self._tab = self.contentTabWidget.currentWidget()
        item_icon = self.equationFrame.selectedAxesComboBox.itemText(0)
        item_text = self.equationFrame.selectedAxesComboBox.itemText(0)
        item_data = self.equationFrame.selectedAxesComboBox.itemData(0)
        self.equationFrame.set_model(AxesModel())
        self.equationFrame.selectedAxesComboBox.clear()
        self.equationFrame.selectedAxesComboBox.addItem(item_icon, item_text, item_data)
        self.equationFrame._gridspec = self._model[self._tab.figure.get_gid()].gridspec
        self.equationFrame.set_axes(0)
        self.connect_figure_signals()

    def gcf(self):
        return self.gct().gcf()

    def gctb(self):
        return self.gct().gctb()

    def gca(self):
        return self.gct().gca()

    def sca(self, ax):
        self.gct().sca(ax)

    def gcp(self):
        return self.gct().gcp()

    def scp(self, artist):
        self.gct().scp(artist)

    def gcf_model(self):
        return self._model[self.gcf().get_gid()]

    @QtCore.Slot(np.ndarray, np.ndarray)
    def set_index(self, x_value, y_value):
        if not self.equationFrame.gca_model():
            self.indexFrame.clear_filters()
            return
        self.indexFrame._x_value = x_value
        self.indexFrame._y_value = y_value
        self.indexFrame.set_model(self.equationFrame.gcp_model().index_map)

    @QtCore.Slot()
    def set_plot(self, fig_model, ax_id, ax_model, plt_id, plt_model):
        """Update the plot.
        """
        dataset = self.datagroupFrame._dataset
        dataset = getattr(dataset._v_parent, "_".join(("", dataset._v_name, plt_model.transform)))
        x, y, options = fig_model.data(dataset, ax_id, plt_id)
        self.gct().set_plot(fig_model, ax_id, ax_model, plt_id, plt_model, x, y, options)

    def index_artist(self, artists):
        dataset = self.datagroupFrame._dataset
        fig = self.gcf()
        if len(fig.axes) == 0:
            return
        ax = self.gca()
        indep_axis = ax._indep_axis
        labels = np.array("")
        slice_ = [slice(None)]*len(dataset.shape)
        slice_[indep_axis] = slice(0, 1)
        for index, (k, v) in enumerate(dataset.sweep_map.items()):
            v = v[slice_]
            if index != indep_axis:
                prefix = r"%s:" % (k,) if labels.size == 1 else r", %s:" % (k,)
                if v.dtype == np.int:
                    v_str = np.asarray([r"%4d" % (v_,) for v_ in v.reshape(-1)]).reshape(v.shape)
                if v.dtype == np.float:
                    v_str = np.asarray([r"%-9.3g" % (v_.real,) for v_ in v.reshape(-1)]).reshape(v.shape)
                elif v.dtype == np.complex:
                    v_str = np.asarray([r"%-9.3g<%-9.3g" % (np.abs(v_), np.angle(v_, deg=True)) for v_ in v.reshape(-1)]).reshape(v.shape)
                labels = np_str.add(labels, np_str.add(prefix, v_str))
        labels = labels.reshape(-1)
        if ax._plot_type == PlotType.Line:
            ax._start_index, ax._stop_index = len(ax.get_lines()) - len(artists), len(ax.get_lines())
            for line, label in zip(artists, labels):
                line.set_label(str(label))

    @QtCore.Slot()
    def set_legend(self, ax, bbox_to_anchor):
        """Display the sorted legend in the position where the context menu was called.
        """
        h, l = ax.get_legend_handles_labels()
        if bbox_to_anchor is None:
            loc = 'center left'
            bbox_to_anchor = (1, 0.5)
        else:
            if not len(h):
                return
            try:
                meridian_index = h.index(ax._meridian)
            except (AttributeError, ValueError):
                meridian_index = -1
            else:
                del h[meridian_index]
                del l[meridian_index]
                del ax.lines[meridian_index]
                ax._meridian = None

            xy_axes = bbox_to_anchor
            xy_points = ax.transAxes.transform(bbox_to_anchor)
            xy_data = ax.transData.inverted().transform(xy_points)

            h, l = zip(*[(h, l) for h, l in zip(h, l) if h.get_visible()])
            h, l = zip(*[(h, l) for (h, l) in sorted(zip(h, l),
                                                     key=lambda pair: pair[0].get_ydata()[np.argmin(np.abs(pair[0].get_xdata() - xy_data[0]))],
                                                     reverse=True)])
            x_align = "right" if xy_axes[0] < 0.5 else "left"
            y_align = "lower" if xy_axes[1] < 0.5 else "upper"
            loc = " ".join((y_align, x_align))

            ylim = ax.get_ylim()
            ylow, yhigh = ylim[0] + (ylim[1] - ylim[0]) * 0.05, ylim[1] - (ylim[1] - ylim[0]) * 0.05
            ax._meridian = ax.plot([xy_data[0], xy_data[0]], [ylow, yhigh], color="black", linestyle=":",
                                   linewidth=3, label="annotation")[0]
        ax.legend(h, l, loc=loc, bbox_to_anchor=bbox_to_anchor)
        self.gcf().canvas.draw()

    def remove_legend(self, ax):
        if ax.legend_:
            ax.legend_.remove()
        if ax._meridian:
            ax._meridian.remove()
            ax._meridian = None
        self.gcf().canvas.draw()

    def update(self, datasets=False, index=False, equations=False, interpolation=False, plots=False):
        super(DataViewer, self).update()
        has_tab = self._tab is not None
        self.actionExport.setEnabled(has_tab)
        self.actionSubplots.setEnabled(has_tab)
        self.actionUndo.setEnabled(has_tab)
        self.actionRedo.setEnabled(has_tab)
        self.actionRefresh.setEnabled(has_tab)
        self.actionClear.setEnabled(has_tab)
        self.datagroupFrame.setEnabled(has_tab)
        self.equationFrame.setEnabled(has_tab)
        self.indexFrame.setEnabled(has_tab)
        self.imageFrame.setEnabled(has_tab)
        if datasets:
            self.datagroupFrame.update()
        if equations:
            self.equationFrame.update()
        if index:
            self.indexFrame.update()
        if interpolation:
            pass
        if plots:
            fig, fig_id, fig_model = self.gcf(), self.gcf().get_gid(), self.gcf_model()
            ax, ax_id, ax_model = self.gca(), self.gca().get_gid(), self.equationFrame.gca_model()
            plt, plt_id, plt_model = self.equationFrame.gcp(), self.equationFrame.gcp().get_gid(), self.equationFrame.gcp_model()
            dataset = self.datagroupFrame._dataset
            dataset = getattr(dataset._v_parent, "_".join(("", dataset._v_name, plt_model.transform)))
            x, y, options = fig_model.data(dataset, ax_id, plt_id)
            if plt_model.type == PlotType.Scatter:
                plt.set_offsets(x)
            elif plt_model.type == PlotType.Line:
                plt.set_xdata(x)
                plt.set_ydata(y)
            elif plt_model.type == PlotType.Contour:
                raise NotImplementedError()
            else:  # plt_model.type == PlotType.Contourf:
                raise NotImplementedError()
            fig.canvas.draw()


