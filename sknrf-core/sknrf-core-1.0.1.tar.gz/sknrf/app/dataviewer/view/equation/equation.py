import os
import logging

from PySide2 import QtCore
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QFrame
import matplotlib as mpl
from matplotlib.lines import lineStyles
from matplotlib.markers import MarkerStyle

from sknrf.enums.signal import transform_map, transform_label_map, transform_icon_map
from sknrf.device import signal
from sknrf.app.dataviewer.model.equation import EquationTableModel
from sknrf.app.dataviewer.model.figure import AxesType, PlotType, AxisType, FormatType
from sknrf.app.dataviewer.model.figure import AxesModel, PlotModel
from sknrf.app.dataviewer.view.equation.QEquationFrame import Ui_equationFrame
from sknrf.utilities.numeric import PkAvg, Format
from sknrf.utilities import rf
from sknrf.icons import blue_32_rc, green_32_rc, cyan_32_rc, orange_32_rc, red_32_rc, violet_32_rc, yellow_32_rc

import numpy as np
import scipy as sp
from scipy import constants as const
import skrf

logger = logging.getLogger()


class EquationFrame(QFrame, Ui_equationFrame):

    axesChanged = QtCore.Signal(object, object)

    def __init__(self, parent=None):
        super(EquationFrame, self).__init__(parent=parent)
        self.setupUi(self)
        icon_path = os.path.join(mpl.rcParams['datapath'], 'images')
        self.panToolButton.setIcon(QIcon(os.path.join(icon_path, 'move.png')))
        self.zoomToolButton.setIcon(QIcon(os.path.join(icon_path, 'zoom_to_rect.png')))
        self.homeToolButton.setIcon(QIcon(os.path.join(icon_path, 'home.png')))
        self.settingsToolButton.setIcon(QIcon(os.path.join(icon_path, 'qt4_editor_options.png')))
        self.axesComboBox.clear()
        for axes_type in AxesType:
            self.axesComboBox.addItem(axes_type.name, axes_type.value)
        self.xAxisComboBox.clear()
        self.yAxisComboBox.clear()
        for axis_type in AxisType:
            self.xAxisComboBox.addItem(axis_type.name, axis_type.value)
            self.yAxisComboBox.addItem(axis_type.name, axis_type.value)
        self.plotComboBox.clear()
        for plot_type in PlotType:
            self.plotComboBox.addItem(plot_type.name, plot_type.value)
        self.xFormatComboBox.clear()
        self.yFormatComboBox.clear()
        for format_type in FormatType:
            self.xFormatComboBox.addItem(format_type.name, format_type.value)
            self.yFormatComboBox.addItem(format_type.name, format_type.value)
        self.lineStyleComboBox.clear()
        for line_style in lineStyles.keys():
            self.lineStyleComboBox.addItem(line_style)
        self.markerStyleComboBox.clear()
        for marker_style in MarkerStyle.filled_markers:
            self.markerStyleComboBox.addItem(marker_style)

        self._parent = None
        self.dataset = None
        self._model = AxesModel()
        self._gridspec = (1, 1)
        self.set_transforms_list(list(transform_map.keys()))
        self.transform = "Envelope"
        self._indep_axis = 0
        self._x_model = EquationTableModel({}, parent=self)
        self._x_value = None
        self._y_model = EquationTableModel({}, parent=self)
        self._y_value = None

    def connect_signals(self):
        self.panToolButton.clicked.connect(self.pan_axes)
        self.zoomToolButton.clicked.connect(self.crop_axes)
        self.homeToolButton.clicked.connect(self.auto_scale_axes)
        self.settingsToolButton.clicked.connect(self.open_axes_settings)
        self.clearToolButton.clicked.connect(self.remove_axes)

        self.selectedAxesComboBox.currentIndexChanged.connect(self.set_axes)
        self.xShareAxisCheckBox.stateChanged.connect(self.update)
        self.xOriginSpinBox.valueChanged.connect(self.update)
        self.xSpanSpinBox.valueChanged.connect(self.update)
        self.yShareAxisCheckBox.stateChanged.connect(self.update)
        self.yOriginSpinBox.valueChanged.connect(self.update)
        self.ySpanSpinBox.valueChanged.connect(self.update)

        self.transformComboBox.currentIndexChanged.connect(self.set_transform)
        self._x_model.dataChanged.connect(self.set_x_equation)
        self.xTableView.clicked.connect(self.set_x_equation)
        self._y_model.dataChanged.connect(self.set_y_equation)
        self.yTableView.clicked.connect(self.set_y_equation)
        # self.selectedPlotComboBox.currentIndexChanged.connect(self.set_plot)
        self.plotPushButton.clicked.connect(self.add_axes)

    def disconnect_signals(self):
        self.panToolButton.clicked.disconnect()
        self.zoomToolButton.clicked.disconnect()
        self.homeToolButton.clicked.disconnect()
        self.settingsToolButton.clicked.disconnect()
        self.clearToolButton.clicked.disconnect()

        self.selectedAxesComboBox.currentIndexChanged.disconnect()
        self.xShareAxisCheckBox.stateChanged.disconnect()
        self.xOriginSpinBox.valueChanged.disconnect()
        self.xSpanSpinBox.valueChanged.disconnect()
        self.yShareAxisCheckBox.stateChanged.disconnect()
        self.yOriginSpinBox.valueChanged.disconnect()
        self.ySpanSpinBox.valueChanged.disconnect()

        self.transformComboBox.currentIndexChanged.disconnect()
        self._x_model.dataChanged.disconnect()
        self.xTableView.clicked.disconnect()
        self._y_model.dataChanged.disconnect()
        self.yTableView.clicked.disconnect()
        # self.selectedPlotComboBox.currentIndexChanged.disconnect()
        self.plotPushButton.clicked.disconnect()

    def set_transforms_list(self, transforms_list):
        self.transformComboBox.clear()
        for key in transforms_list:
            icon = QIcon()
            icon.addFile(transform_icon_map[key], QtCore.QSize(), QIcon.Normal, QIcon.Off)
            label = transform_label_map[key]
            self.transformComboBox.addItem(label, key)

    def set_equations(self):
        """Update the equation tables.
        """
        self.setDisabled(self.dataset is None)
        if self.isEnabled():
            self.disconnect_signals()
            ds = getattr(self.dataset._v_parent, "_".join(("", self.dataset._v_name, self.transform)))
            self._x_model.blockSignals(True)
            self._x_model = EquationTableModel(ds.sweep_map, parent=self)
            self.xTableView.setModel(self._x_model)
            self._y_model.blockSignals(True)
            self._y_model = EquationTableModel(ds._v_children, parent=self)
            self.yTableView.setModel(self._y_model)
            self.connect_signals()

    @QtCore.Slot()
    def auto_scale_axes(self):
        self._parent.gctb().home()

    @QtCore.Slot()
    def pan_axes(self, checked=False):
        if self.panToolButton.isChecked():
            self.set_interactive_tool(self.panToolButton)
        self._parent.gctb().pan()

    @QtCore.Slot()
    def crop_axes(self, checked=False):
        if self.zoomToolButton.isChecked():
            self.set_interactive_tool(self.zoomToolButton)
        self._parent.gctb().zoom()

    @QtCore.Slot()
    def open_axes_settings(self):
        self._parent.gctb().edit_parameters()

    def set_model(self, model):
        self._model = model

    def gct(self):
        return self._parent.gct()

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

    def gca_model(self):
        return self._model

    def gcp_model(self):
        return self._model[self.gcp().get_gid()]

    def set_interactive_tool(self, action):
        self.panToolButton.setChecked(action == self.panToolButton)
        self.zoomToolButton.setChecked(action == self.zoomToolButton)

    @QtCore.Slot(int)
    def set_transform(self, _):
        self.transform = self.transformComboBox.currentText()
        self.set_equations()

    @QtCore.Slot(QtCore.QModelIndex, QtCore.QModelIndex)
    def set_x_equation(self, topLeft=None, bottomRight=None):
        """Set the selected equation in the equation table.
        """
        self.xTableView.model().set_selected(topLeft)
        self._indep_axis, x_str, _, _, _ = self.xTableView.model().selected()
        self.set_x_format(x_str)

    @QtCore.Slot()
    def set_x_format(self, equation="", transform=""):
        equation = self.xStrLineEdit.text() if len(equation) == 0 else equation
        transform = self.transform if len(transform) == 0 else transform
        ds = getattr(self.dataset._v_parent, "_".join(("", self.dataset._v_name, transform)))
        try:
            self._x_value = eval(equation, globals(), ds._v_children)[...]
        except ValueError as e:
            logger("Syntax Error in X Equation")
            raise e
        else:
            self.xStrLineEdit.setText(equation)

    @QtCore.Slot(QtCore.QModelIndex, QtCore.QModelIndex)
    def set_y_equation(self, topLeft=None, bottomRight=None):
        self.yTableView.model().set_selected(topLeft)
        _, y_str, _, _, _ = self.yTableView.model().selected()
        self.set_y_format(y_str)

    @QtCore.Slot()
    def set_y_format(self, equation="", transform=""):
        equation = self.xStrLineEdit.text() if len(equation) == 0 else equation
        transform = self.transform if len(transform) == 0 else transform
        ds = getattr(self.dataset._v_parent, "_".join(("", self.dataset._v_name, transform)))
        try:
            self._y_value = eval(equation, globals(), ds._v_children)[...]
        except ValueError as e:
            logger("Syntax Error in Y Equation")
            raise e
        else:
            self.yStrLineEdit.setText(equation)

    @QtCore.Slot()
    def add_axes(self):
        tab = self.gct()
        fig = self.gcf()
        fig_model = self._parent.gcf_model()
        ax = None
        grid = (self.majorGridCheckBox.isChecked(), self.minorGridCheckBox.isChecked())
        gridspec = (slice(self.yOriginSpinBox.value(), self.yOriginSpinBox.value() + self.ySpanSpinBox.value(), None),
                    slice(self.xOriginSpinBox.value(), self.xOriginSpinBox.value() + self.xSpanSpinBox.value(), None))
        axis = (AxisType(self.xAxisComboBox.currentIndex()), AxisType(self.xAxisComboBox.currentIndex()))
        ax_model = AxesModel(type=AxesType(self.axesComboBox.currentIndex()), title=self.axesTitleLineEdit.text(),
                             grid=grid, gridspec=gridspec,
                             axis=axis, indep_axis=self._indep_axis)
        share_x = bool(len(fig.axes) and self.xShareAxisCheckBox.isChecked())
        share_y = bool(len(fig.axes) and self.yShareAxisCheckBox.isChecked())
        ax_id = "<anonymous {} (id: {:#x})>".format(type(ax).__name__, id(ax))

        tab.add_axes(fig_model, ax_id, ax_model, share_x, share_y)
        ax = self.gca()
        self._model = ax_model
        plt_id, plt_model = self.add_plot(fig_model, ax_id, ax_model)
        self._parent.set_plot(fig_model, ax_id, ax_model, plt_id, plt_model)
        tab.set_grid(ax, *self.gca_model().grid)

        index = self.selectedAxesComboBox.count()
        name = (ax.get_title() or " - ".join(filter(None, [ax.get_xlabel(), ax.get_ylabel()])) or ax_id)
        if self.selectedAxesComboBox.findText(name) < 0:
            self.selectedAxesComboBox.addItem(name)
        self.selectedAxesComboBox.setCurrentIndex(index)

    @QtCore.Slot(int)
    def set_axes(self, index):
        tab = self.gct()
        tab.set_axes(index)
        self.axesChanged.emit(self._x_value, self._y_value)
        self.update()
        self.gcf().canvas.draw()

    @QtCore.Slot()
    def remove_axes(self):
        index = self.selectedAxesComboBox.currentIndex()
        self.gct().remove_axes(index)
        if index > 0:
            self.selectedAxesComboBox.removeItem(index)
            del self._parent.gcf_model()[self.gca().get_gid()]
            self.set_axes(0)

    def add_plot(self, fig_model, ax_id, ax_model):
        x_format = FormatType(self.xFormatComboBox.currentIndex())
        y_format = FormatType(self.yFormatComboBox.currentIndex())
        plt_model = PlotModel(transform=self.transformComboBox.currentText(),
                              x_str=self.xStrLineEdit.text(), x_format=x_format, x_label=self.xStrLineEdit.text(),
                              y_str=self.yStrLineEdit.text(), y_format=y_format, y_label=self.yStrLineEdit.text(),
                              line_enable=self.lineCheckBox.isChecked(), line_style=self.lineStyleComboBox.currentText(), line_size=self.lineSizeSpinBox.value(),
                              marker_enable=self.markerCheckBox.isChecked(), marker_style=self.markerStyleComboBox.currentText(), marker_size=self.markerSizeSpinBox.value(),
                              options=eval("{%s}" % self.optionsLineEdit.text()))
        plt_id = "%s vs. %s" % (plt_model.y_str, plt_model.x_str)
        self.gct().add_plot(fig_model, ax_id, ax_model, plt_id, plt_model)
        return plt_id, plt_model

    def update(self, index=False, interpolation=False, plots=False):
        super(EquationFrame, self).update()

        ind = self.selectedAxesComboBox.currentIndex()
        ax_model = self.gca_model()
        num_rows, num_cols = self._gridspec
        y_slice, x_slice = ax_model.gridspec
        x_span = max((1, min((num_cols - x_slice.start, x_slice.stop - x_slice.start))))
        y_span = max((1, min((num_rows - y_slice.start, y_slice.stop - y_slice.start))))
        self.xOriginSpinBox.setMaximum(num_cols - x_span)
        self.yOriginSpinBox.setMaximum(num_rows - y_span)
        self.xSpanSpinBox.setMaximum(num_cols - self.xOriginSpinBox.value())
        self.ySpanSpinBox.setMaximum(num_rows - self.yOriginSpinBox.value())
        if ind > 0:
            self.selectedAxesComboBox.setCurrentIndex(ind)
            self.axesComboBox.setCurrentIndex(AxesType(ax_model.type).value)
            self.axesTitleLineEdit.setText(ax_model.title)
            self.majorGridCheckBox.setChecked(ax_model.grid[0]), self.minorGridCheckBox.setChecked(ax_model.grid[1])
            self.xOriginSpinBox.setValue(x_slice.start)
            self.xSpanSpinBox.setValue(x_slice.stop)
            self.xAxisComboBox.setCurrentIndex(AxisType(ax_model.axis[0]).value)
            self.yOriginSpinBox.setValue(y_slice.start)
            self.ySpanSpinBox.setValue(y_slice.stop)
            self.yAxisComboBox.setCurrentIndex(AxisType(ax_model.axis[1]).value)

            plt_model = self.gcp_model()
            self.plotComboBox.setCurrentIndex(PlotType(plt_model.type).value)
            self.xStrLineEdit.setText(plt_model.x_str)
            self.xFormatComboBox.setCurrentIndex(FormatType(plt_model.x_format).value)
            self.yStrLineEdit.setText(plt_model.y_str)
            self.yFormatComboBox.setCurrentIndex(FormatType(plt_model.y_format).value)
            self.lineCheckBox.setChecked(plt_model.line_enable)
            self.lineStyleComboBox.setCurrentIndex(list(lineStyles.keys()).index(plt_model.line_style))
            self.lineSizeSpinBox.setValue(plt_model.line_size)
            self.markerCheckBox.setChecked(plt_model.line_enable)
            self.markerStyleComboBox.setCurrentIndex(MarkerStyle.filled_markers.index(plt_model.marker_style))
            self.markerSizeSpinBox.setValue(plt_model.marker_size)
            self.optionsLineEdit.setText(str(plt_model.options).strip("{}"))

        self.axesComboBox.setEnabled(not ind)
        self.axesTitleLineEdit.setEnabled(not ind)
        self.majorGridCheckBox.setEnabled(not ind), self.minorGridCheckBox.setEnabled(not ind)
        self.xShareAxisCheckBox.setEnabled(not ind)
        x_shared = self.xShareAxisCheckBox.isChecked()
        self.xOriginSpinBox.setEnabled(not ind and not x_shared), self.xSpanSpinBox.setEnabled(not ind and not x_shared)
        self.xAxisComboBox.setEnabled(not ind and not x_shared)
        self.yShareAxisCheckBox.setEnabled(not ind)
        y_shared = self.yShareAxisCheckBox.isChecked()
        self.yOriginSpinBox.setEnabled(not ind and not y_shared), self.ySpanSpinBox.setEnabled(not ind and not y_shared)
        self.yAxisComboBox.setEnabled(not ind and not y_shared)

        self.selectedPlotComboBox.setEnabled(False)
        self._parent.update(batch_index=index, interpolation=interpolation, plots=plots)
