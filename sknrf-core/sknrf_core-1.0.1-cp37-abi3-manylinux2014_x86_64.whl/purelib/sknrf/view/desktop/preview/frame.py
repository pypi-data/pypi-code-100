import sys
import abc
import itertools
from collections import OrderedDict

import tables as tb
import torch as th
import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QFrame, QLabel, QCheckBox, QComboBox, QSpinBox
from PySide2.QtWidgets import QAbstractItemView, QListWidgetItem, QSpacerItem, QSizePolicy, QHBoxLayout
import matplotlib as mpl

from sknrf.enums.signal import transform_map, transform_label_map, transform_icon_map, transform_xlabel_map
from sknrf.settings import Settings
from sknrf.utilities.rf import t2n
from sknrf.model.sequencer.sweep.base import AbstractSweep
from sknrf.app.dataviewer.model.dataset import preview_plot, WCArray
from sknrf.app.dataviewer.model.figure import FigureModel, AxesModel, PlotModel
from sknrf.app.dataviewer.model.figure import AxesType, AxisType, PlotType, FormatType, format_map
from sknrf.widget.propertybrowser.view.helper import DISPLAY, model_generator, get_attr
from sknrf.app.dataviewer.view.figure import ToolbarMenus
from sknrf.app.dataviewer.view.filter.widget import RealFilter
from sknrf.view.desktop.preview.QPreviewPlotFrame import Ui_previewPlotFrame
from sknrf.view.desktop.sequencer.sweep import SweepSliderWidget
from sknrf.view.desktop.sequencer.widgets import SequencerState

from sknrf.widget.propertybrowser.view import Domain

from sknrf.utilities import rf
from sknrf.utilities.numeric import PkAvg, Format
from sknrf.icons import blue_32_rc
from sknrf.icons import green_32_rc
from sknrf.icons import cyan_32_rc
from sknrf.icons import orange_32_rc
from sknrf.icons import magenta_32_rc
from sknrf.icons import red_32_rc
from sknrf.icons import violet_32_rc
from sknrf.icons import yellow_32_rc

__author__ = 'dtbespal'


class AbstractPreviewFrame(QFrame, Ui_previewPlotFrame):

    setting_changed = QtCore.Signal()

    def __init__(self, parent=None, model=None):
        super(AbstractPreviewFrame, self).__init__(parent=parent)
        self.setupUi(self)
        self.fig_model = FigureModel(1, gridspec=(1, 1))
        self.get_func = getattr
        self.format_map = format_map
        self._color_map = {}

        self.formatComboBox.clear()
        for key in self.format_map.keys():
            self.formatComboBox.addItem(str(key).replace("FormatType.", ""))
        self._item_type = object
        self._model = None

    def connect_signals(self):
        self.itemListWidget.itemClicked.connect(self.select_items)
        self.axesComboBox.currentIndexChanged[str].connect(self.set_axes)
        self.formatComboBox.currentIndexChanged[str].connect(self.set_format)

    def disconnect_signals(self):
        self.itemListWidget.itemClicked.disconnect()
        self.axesComboBox.currentIndexChanged[str].disconnect()
        self.formatComboBox.currentIndexChanged[str].disconnect()

    def clear(self):
        self.itemListWidget.clear()
        self._model.clear()

    def model(self):
        return self._model

    def set_model(self, model, display=DISPLAY.READ):
        self.disconnect_signals()
        selected_items_names = []
        for item in self.itemListWidget.selectedItems():
            selected_items_names.append(item.text())
        self.itemListWidget.clear()
        self._color_map.clear()
        color_cycle = itertools.cycle(Settings().color_order)

        generator = model_generator(model, display=display)
        for attribute in generator:
            items = get_attr(model, attribute)
            if isinstance(items, self._item_type):
                next_color = next(color_cycle)
                self._color_map[attribute] = Settings().color_map[next_color]
                icon = QIcon()
                icon.addFile(":/PNG/" + next_color + "/32/form_oval.png", QSize(), QIcon.Normal, QIcon.Off)
                new_item = QListWidgetItem(icon, attribute)
                self.itemListWidget.addItem(new_item)
                new_item.setSelected(attribute in selected_items_names)
        self._model = model
        self.select_items()
        self.connect_signals()

    @abc.abstractmethod
    def select_items(self):
        pass

    @abc.abstractmethod
    def update(self, **kwargs):
        pass

    def set_axes(self, axes):
        if axes == "Rectangular":
            self.formatComboBox.setEnabled(True)
        else:
            self.formatComboBox.setEnabled(False)
            self.formatComboBox.setCurrentIndex(0)
        self.update(plot=True)

    def set_format(self, _):
        self.update(plot=True)

    def no_format(self, value):
        return value


class AuxiliarySignalPreviewFrame(AbstractPreviewFrame):
    setting_changed = QtCore.Signal()

    def __init__(self, parent=None, model=None):
        super(AuxiliarySignalPreviewFrame, self).__init__(parent=parent)
        toolbar_menues = ToolbarMenus.STATE | ToolbarMenus.SCALE | ToolbarMenus.AXES
        self.previewPlot.add_toolbar(toolbar_menus=toolbar_menues)
        self.connect_signals()
        self._item_type = np.ndarray
        if model is not None:
            self.set_model(model)

    def connect_signals(self):
        super(AuxiliarySignalPreviewFrame, self).connect_signals()

    def disconnect_signals(self):
        super(AuxiliarySignalPreviewFrame, self).disconnect_signals()

    def set_model(self, model, display=DISPLAY.PUBLIC):
        super(AuxiliarySignalPreviewFrame, self).set_model(model, display=display)

    def select_items(self):
        self.update(plot=True)

    @abc.abstractmethod
    def update(self, plot=False, **kwargs):
        super(AuxiliarySignalPreviewFrame, self).update()
        all_ = not (plot)

        self.previewPlot.gcf().clear()
        axes_type = AxesType(self.axesComboBox.currentIndex())
        ax_model = AxesModel(type=axes_type, autoscale=False, title="",
                             grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                             axis=(AxisType.Linear, AxisType.Linear), indep_axis=-2)
        self.previewPlot.add_axes(self.fig_model, "auxiliary", ax_model)

        selected_items = self.itemListWidget.selectedItems()
        if not selected_items:
            self.previewPlot.canvas.draw()
            return

        if plot or all_:
            if self.formatComboBox.isVisible():
                format_ = self.format_map[FormatType(self.formatComboBox.currentIndex())]
            else:
                format_ = format_map[FormatType.Re]
            transform = transform_map[Domain.FF]
            xlabel = transform_xlabel_map[Domain.FF]
            plt_model = PlotModel(type=PlotType.Line, transform=transform, title="",
                                  x_str="", x_format=FormatType.Re, x_label=xlabel,
                                  y_str="", y_format=format_, y_label="",
                                  line_enable=True, line_style="", line_size=2,
                                  marker_enable=False, marker_style=".", marker_size=2,
                                  meridian=(0, 0), options=None)
            self.previewPlot.add_plot(self.fig_model, "auxiliary", ax_model, "plot", plt_model)
            freq = self._model.freq
            x_min, x_max = -2e-100, 2e-100
            y_min, y_max = -2e-100, 2e-100
            for item in selected_items:
                plot_signal = self.get_func(self._model, item.text()).transpose()
                options = {"colors": self._color_map[item.text()]}
                if axes_type == AxesType.Rectangular:
                    plot_signal = format_(plot_signal)
                    x = freq.reshape(1, -1)
                    y = np.asarray(plot_signal).transpose()[:, 0:freq.size]
                    xlabel = plt_model.x_label
                    x_min, x_max = freq.min(), freq.max()
                elif axes_type == AxesType.Polar:
                    x = np.angle(np.asarray(plot_signal)).transpose()[:, 0:freq.size]
                    y = np.abs(np.asarray(plot_signal)).transpose()[:, 0:freq.size]
                    xlabel = ""
                else:
                    x = np.real(np.asarray(plot_signal)).transpose()[:, 0:freq.size]
                    y = np.imag(np.asarray(plot_signal)).transpose()[:, 0:freq.size]
                    xlabel = ""
                self.previewPlot.set_plot(self.fig_model, "auxiliary", ax_model, "plot", plt_model, x, y, options)
                x_min, x_max = np.minimum(x_min, np.nanmin(x)), np.maximum(x_max, np.nanmax(x))
                y_min, y_max = np.minimum(y_min, np.nanmin(y)), np.maximum(y_max, np.nanmax(y))
            self.previewPlot.update_axis(xlabel=xlabel, xlim=(x_min, x_max), ylim=(y_min, y_max))
            self.previewPlot.update()


class SignalPreviewFrame(AbstractPreviewFrame):

    def __init__(self, parent=None, model=None):
        super(SignalPreviewFrame, self).__init__(parent=parent)
        toolbar_menues = ToolbarMenus.STATE | ToolbarMenus.SCALE | ToolbarMenus.AXES
        self.previewPlot.add_toolbar(toolbar_menus=toolbar_menues)
        self.itemListLabel.setText("Signals:")
        self.itemListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.transformLabel = QLabel("Transform:")
        self.transformComboBox = QComboBox(parent=self.scrollArea)

        layout = self.defaultGridLayout.layout()
        layout.addWidget(self.transformLabel, 2, 0, 1, 1)
        layout.addWidget(self.transformComboBox, 2, 1, 1, 1)

        self.transform_map = OrderedDict()
        self.filter_widget_map = OrderedDict()
        self._current_filter = None

        self.connect_signals()
        self._item_type = th.Tensor
        if model is not None:
            self.set_model(model)

    def connect_signals(self):
        super(SignalPreviewFrame, self).connect_signals()
        self.transformComboBox.currentIndexChanged[str].connect(self.set_transform)
        for filter_widget in self.filter_widget_map.values():
            filter_widget.filter_changed.connect(self.set_filter)

    def disconnect_signals(self):
        super(SignalPreviewFrame, self).disconnect_signals()
        self.transformComboBox.currentIndexChanged[str].disconnect()
        for filter_widget in self.filter_widget_map.values():
            filter_widget.filter_changed.disconnect()

    def model(self):
        return self._model

    def set_model(self, model, display=DISPLAY.PUBLIC):
        super(SignalPreviewFrame, self).set_model(model, display=display)
        self.disconnect_signals()
        self.set_transforms_list(list(transform_map.keys()))
        self.connect_signals()

    def select_items(self):
        self.add_filter("freq", self._model.freq)
        self.add_filter("time", self._model.time)
        self.update(plot=True)

    def set_transform(self, transform):
        transform_type = list(transform_label_map.keys())[self.transformComboBox.currentIndex()]
        if transform_type == Domain.TF:
            self.replace_filter(0, "freq", self._model.freq[...])
            self.replace_filter(1, "time", self._model.time[...])
        elif transform_type == Domain.FF:
            self.replace_filter(0, "freq", self._model.freq[...])
            self.replace_filter(1, "freq_m", self._model.freq_m[...])
        elif transform_type == Domain.FT:
            self.replace_filter(0, "time_c", self._model.time_c[...])
            self.replace_filter(1, "freq_m", self._model.freq_m[...])
        elif transform_type == Domain.TT:
            self.replace_filter(0, "time_c", self._model.time_c[...])
            self.replace_filter(1, "time", self._model.time[...])
        self.update(filters=True, plot=True)

    def add_filter(self, name, value):
        if name in self.filter_widget_map.keys():
            pass
        else:
            filter_widget = RealFilter(name, value, parent=self.scrollArea)
            filter_widget.filter_changed.connect(self.set_filter)
            layout = self.customGridLayout.layout()
            layout.addWidget(filter_widget, layout.rowCount(), 0, 1, 1)
            self.filter_widget_map[name] = filter_widget

    def replace_filter(self, index, name, value):
        old_name = list(self.filter_widget_map.keys())[index]
        filter_widget = RealFilter(name, value, parent=self.scrollArea)
        filter_widget.filter_changed.connect(self.set_filter)
        layout = self.customGridLayout.layout()
        widget = self.filter_widget_map.pop(old_name)
        layout.removeWidget(widget)
        widget.deleteLater()
        layout.addWidget(filter_widget, index, 0, 1, 1)
        self.filter_widget_map[name] = filter_widget
        keys = list(self.filter_widget_map.keys())
        for ind, k in enumerate(keys[:-1]):
            if ind >= index:
                self.filter_widget_map.move_to_end(k)

    def clear(self):
        self.clear_filters()
        self.itemListWidget.clear()

    def clear_filters(self):
        for widget in self.filter_widget_map.values():
            widget.deleteLater()
        self.filter_widget_map = OrderedDict()

    def set_filter(self):
        selected_items = self.itemListWidget.selectedItems()
        if selected_items:
            self.update()
            self.setting_changed.emit()

    def set_transforms_list(self, transforms_list):
        self.transformComboBox.clear()
        for key in transforms_list:
            icon = QIcon()
            icon.addFile(transform_icon_map[key], QSize(), QIcon.Normal, QIcon.Off)
            label = transform_label_map[key]
            self.transform_map[key] = transform_label_map[key]
            self.transformComboBox.addItem(label, key)

    def update(self, filters=False, plot=False):
        super(SignalPreviewFrame, self).update()
        all_ = not (filters or plot)

        if filters or all_:
            pass

        if plot or all_:
            axes_type = AxesType(self.axesComboBox.currentIndex())
            format_type = FormatType(self.formatComboBox.currentIndex())
            format_type = format_type if self.formatComboBox.isVisible() else FormatType.Re
            transform_type = list(transform_map.keys())[self.transformComboBox.currentIndex()]
            selected_items = [item.text() for item in self.itemListWidget.selectedItems()]
            filters = [(v.lower_index(), v.upper_index()) for v in self.filter_widget_map.values()]
            self.previewPlot.gcf().clear()
            yaxis_type = AxisType.LinearLog if format_type in [FormatType.dB, FormatType.dBm] else AxisType.Linear
            x_label = transform_xlabel_map[transform_type]
            ax_model = AxesModel(type=axes_type, autoscale=True, title="",
                                 grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                                 axis=(AxisType.Linear, yaxis_type), indep_axis=-2)
            self.previewPlot.add_axes(self.fig_model, "signal", ax_model)
            if not selected_items:
                self.previewPlot.canvas.draw()
                return
            x_min, x_max = np.nan, np.nan
            y_min, y_max = np.nan, np.nan
            for item in selected_items:
                x_label = transform_xlabel_map[transform_type]
                options_map = {"colors": self._color_map[item]}
                plt_model = PlotModel(type=PlotType.Line, transform=transform_type, title="",
                                      x_str="", x_format=FormatType.Re, x_label=x_label,
                                      y_str="", y_format=format_type, y_label="",
                                      line_enable=True, line_style="", line_size=2,
                                      marker_enable=False, marker_style=".", marker_size=2,
                                      meridian=(0, 0), options=None)
                self.previewPlot.add_plot(self.fig_model, "signal", ax_model, "plot", plt_model)
                plot_data = preview_plot(self._model, self.get_func, item, filters,
                                         ax_model, plt_model,
                                         transform_type, options_map)
                ax_model, plt_model, x, y, options_map = plot_data
                self.previewPlot.set_plot(self.fig_model, "signal", ax_model, "plot", plt_model,
                                          np.asarray(x), np.asarray(y), options_map)
                x_min, x_max = np.nanmin([x_min, np.nanmin(x)]), np.nanmax([x_max, np.nanmax(x)])
                y_min, y_max = np.nanmin([y_min, np.nanmin(y)]), np.nanmax([y_max, np.nanmax(y)])
            self.previewPlot.update_axis(ax_model, xlabel=x_label, xlim=(x_min, x_max), ylim=(y_min, y_max))
            self.previewPlot.update()


class DatasetPreviewFrame(SignalPreviewFrame):

    def __init__(self, parent=None, model=None):
        super().__init__(parent=parent, model=None)
        self._item_type = WCArray
        if model:
            self.set_model(model)

    def select_items(self):
        sweep_map = self._model.sweep_map
        for index, (k, v) in enumerate(sweep_map.items()):
            indices = [0]*len(sweep_map)
            indices[-index - 1] = Ellipsis
            self.add_filter(k, t2n(v[indices].abs()))
        self.update(plot=True)


class SweepPreviewFrame(AbstractPreviewFrame):

    def __init__(self, parent=None, model=None):
        super(SweepPreviewFrame, self).__init__(parent=parent)
        toolbar_menues = ToolbarMenus.STATE | ToolbarMenus.SCALE | ToolbarMenus.MARKUP | ToolbarMenus.AXES
        self.previewPlot.add_toolbar(toolbar_menus=toolbar_menues)
        self.itemListLabel.setText("Sweeps:")
        self.itemListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setting_widget_map = OrderedDict()

        self.connect_signals()
        self._item_type = AbstractSweep
        if model is not None:
            self.set_model(model)

    def connect_signals(self):
        super(SweepPreviewFrame, self).connect_signals()
        for setting_widget in self.setting_widget_map.values():
            setting_widget.slider.valueChanged.connect(self.set_setting)

    def disconnect_signals(self):
        super(SweepPreviewFrame, self).disconnect_signals()
        for setting_widget in self.setting_widget_map.values():
            setting_widget.slider.valueChanged.disconnect(self.set_setting)

    def select_items(self):
        self.clear_settings()
        for item in self.itemListWidget.selectedItems():
            sweep = self._model[item.text()]
            for info in sweep.info.values():
                if info.check and info.max < 1e99:
                    self.add_setting(info.name, getattr(sweep, info.name), info)
        self.update(plot=True)

    def add_setting(self, name, value, info):
        setting_widget = SweepSliderWidget(name, value, info, parent=self.scrollArea)
        setting_widget.slider.valueChanged.connect(self.set_setting)
        layout = self.customGridLayout.layout()
        layout.addWidget(setting_widget)
        self.setting_widget_map[name] = setting_widget

    def clear(self):
        self.clear_settings()
        super(SweepPreviewFrame, self).clear()

    def clear_settings(self):
        layout = self.customGridLayout.layout()
        for widget_name, widget in self.setting_widget_map.items():
            layout.removeWidget(widget)
            widget.deleteLater()
        self.setting_widget_map = OrderedDict()

    def set_setting(self):
        selected_items = self.itemListWidget.selectedItems()
        if selected_items:
            sweep = self._model[selected_items[0].text()]
            setting_widget = self.sender().parent()
            setattr(sweep, setting_widget.name_label.text(), setting_widget.value())
            self.update(plot=True)
            old_variable_name = SequencerState.variable_name
            old_variable = SequencerState.variable
            SequencerState.variable_name = selected_items[0].text()
            SequencerState.variable = sweep
            self.setting_changed.emit()
            SequencerState.variable_name = old_variable_name
            SequencerState.variable = old_variable

    def update(self, settings=False, plot=False):
        super(SweepPreviewFrame, self).update()
        all_ = not (settings or plot)

        self.previewPlot.gcf().clear()
        axes_type = AxesType(self.axesComboBox.currentIndex())
        ax_model = AxesModel(type=axes_type, autoscale=False, title="",
                             grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                             axis=(AxisType.Linear, AxisType.Linear), indep_axis=-2)
        self.previewPlot.add_axes(self.fig_model, "sweep", ax_model)

        selected_items = self.itemListWidget.selectedItems()
        if not selected_items:
            self.previewPlot.canvas.draw()
            return

        sweep = self._model[selected_items[0].text()]
        if settings or all_:
            for setting_name, setting in self.setting_widget_map.items():
                setting.update(getattr(sweep, setting_name), sweep.info[setting_name])

        if plot or all_:
            if self.formatComboBox.isVisible():
                format_ = self.format_map[FormatType(self.formatComboBox.currentIndex())]
            else:
                format_ = format_map[FormatType.Re]
            marker_size = mpl.rcParams['lines.markersize']**2
            plt_model = PlotModel(type=PlotType.Scatter, transform="Envelope", title="",
                                  x_str="", x_format=FormatType.Re, x_label="",
                                  y_str="", y_format=format_, y_label="",
                                  line_enable=False, line_style="", line_size=2,
                                  marker_enable=True, marker_style="x", marker_size=marker_size,
                                  meridian=(0, 0), options=None)
            self.previewPlot.add_plot(self.fig_model, "sweep", ax_model, "plot", plt_model)
            options = {"c": self._color_map[selected_items[0].text()]}
            values = sweep.values()
            x_min, x_max = -2e-100, 2e-100
            y_min, y_max = -2e-100, 2e-100
            if axes_type == AxesType.Rectangular:
                x = np.real(t2n(values)).transpose()
                y = np.imag(t2n(values)).transpose()
                xlabel = ""
            elif axes_type == AxesType.Polar:
                x = np.angle(t2n(values)).transpose()
                y = np.abs(t2n(values)).transpose()
                xlabel = ""
            else:
                x = np.real(t2n(values)).transpose()
                y = np.imag(t2n(values)).transpose()
                xlabel = ""
            self.previewPlot.set_plot(self.fig_model, "sweep", ax_model, "plot", plt_model, x, y, options)
            x_min, x_max = np.minimum(x_min, np.nanmin(x)), np.maximum(x_max, np.nanmax(x))
            y_min, y_max = np.minimum(y_min, np.nanmin(y)), np.maximum(y_max, np.nanmax(y))
            self.previewPlot.update_axis(ax_model, xlabel=xlabel, xlim=(x_min, x_max), ylim=(y_min, y_max))
            self.previewPlot.update()


if __name__ == "__main__":
    from sknrf.model.sequencer.sweep import real, frequency, complex

    app = QApplication(sys.argv)

    # form = SignalPreviewFrame()
    # indep_map = signal.IndepDict((("freq", Settings().freq), ("time", Settings().time)))
    # signal1 = signal.EnvelopeSignal(np.zeros(indep_map.shape, dtype=np.complex128), indep_map)
    # signal2 = signal.EnvelopeSignal(np.zeros(indep_map.shape, dtype=np.complex128), indep_map)
    # model = PreviewModel()
    # model['signal1'] = signal1
    # model['signal2'] = signal2

    form = SweepPreviewFrame()
    model = {}
    model['linear_sweep'] = real.LinearSweep()
    model['span_sweep'] = real.SpanSweep()
    model['subset_sweep'] = real.SubsetSweep()
    model['log_sweep'] = real.LogSweep()
    model['pow_sweep'] = real.PowSweep()

    model["fm_lo_span_sweep"] = frequency.FundLOSpanSweep()
    model["fm_phasor_span_sweep"] = frequency.FundPhasorSpanSweep()
    model["fm_dsb_span_sweep"] = frequency.FundDSBSpanSweep()
    model["fm_ssb_span_sweep"] = frequency.FundSSBSpanSweep()

    model['rectangular'] = complex.RectangularSweep()
    model['polar'] = complex.PolarSweep()
    model['rectangular_uniform'] = complex.RectangularUniformSweep()
    model['polar_uniform'] = complex.PolarUniformSweep()
    model['rectangular_random'] = complex.RectangularRandomSweep()
    model['polar_random'] = complex.PolarRandomSweep()

    form.set_model(model)
    form.showMaximized()
    app.exec_()