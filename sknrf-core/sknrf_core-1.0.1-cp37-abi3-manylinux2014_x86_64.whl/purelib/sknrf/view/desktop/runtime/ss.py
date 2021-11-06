import itertools
import logging

import torch as th
from PySide2 import QtCore
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QVBoxLayout, QSizePolicy
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection


from sknrf.device.signal import tf, ff
from sknrf.app.dataviewer.model import DatagroupModel
from sknrf.model.device import DevicesModel
from sknrf.app.dataviewer.model.figure import FigureModel, AxesModel, PlotModel
from sknrf.app.dataviewer.model.figure import AxesType, AxisType, PlotType, FormatType
from sknrf.settings import Settings
from sknrf.view.desktop.runtime.base import AbstractRuntimeView
from sknrf.app.dataviewer.view.figure import ContentFigure
from sknrf.utilities.rf import rU2dBU, dBU2rU, n2t, t2n
from sknrf.utilities.dsp import ind_grid, fm_grid


logger = logging.getLogger(__name__)

__author__ = 'dtbespal'


class SParameterView(QFrame):
    """Runtime status of a given port

    Runtime status of a port is presented as:
        * The multi-harmonic port impedance distribution.
        * The multi-harmonic peak incident power-wave (a_p), reflected power-wave (b_p), voltage (v), and current (i).

        Keyword Args:
            model (PortModel): A collection of all device objects connected to a given port.
            parent (QWidget): Parent GUI container.
    """

    def __init__(self, model, ports, parent=None):
        super(SParameterView, self).__init__(parent)
        self.vbl = QVBoxLayout(self)
        self.vbl.setContentsMargins(0, 0, 0, 0)
        self.ports = ports
        self.plots = [None]*len(self.ports)**2
        num_ports = len(self.ports)

        color_rgb = []
        for color in Settings().color_order:
            color_rgb.append(Settings().color_map[color])
        color_cycle = itertools.cycle(color_rgb)

        self.previewPlotWidget = ContentFigure(self)
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previewPlotWidget.sizePolicy().hasHeightForWidth())
        self.previewPlotWidget.setSizePolicy(sizePolicy)
        self.previewPlotWidget.setObjectName("previewPlotWidget")
        self.vbl.addWidget(self.previewPlotWidget)

        self._model = model
        ds = self._model.datagroup_model()[Settings().datagroup].dataset(Settings().dataset)
        fm_shape = [1] * len(ds.shape)
        fm_shape[-3] = ds.shape[-3]
        fm_index = th.arange(0, ds.shape[-3], 1, dtype=th.int64).reshape(fm_shape)
        freq = ds.sp_fund[...].gather(-3, fm_index)
        self._freq = fm_grid(freq.flatten())

        s = rU2dBU(ds.s[...])
        fig = self.previewPlotWidget.gcf()
        self.fig_model = FigureModel(1, gridspec=(1, 1))
        self.previewPlotWidget.gcf().clear()
        self.r_ax_model = AxesModel(type=AxesType.Rectangular, autoscale=True, title="Sxx",
                                    grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                                    axis=(AxisType.Linear, AxisType.Linear), indep_axis=-2)
        self.previewPlotWidget.add_axes(self.fig_model, "Sxx", self.r_ax_model, share_x=True)
        self.t_ax_model = AxesModel(type=AxesType.Rectangular, autoscale=True, title="Sxy",
                                    grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                                    axis=(AxisType.Linear, AxisType.Linear), indep_axis=-2)
        if num_ports > 1:
            self.previewPlotWidget.add_axes(self.fig_model, "Sxy", self.r_ax_model, share_x=True)

        legend_lines = list()
        legend_labels = list()
        self.plt_models = list()
        for src_index, src_port in enumerate(self.ports):
            for rcvr_index, rcvr_port in enumerate(self.ports):
                ax_model = self.r_ax_model if src_index == rcvr_index else self.t_ax_model

                plt_index = src_index*num_ports + rcvr_index
                plot_title = "S{:d}{:d}".format(rcvr_port, src_port)
                plt_model = PlotModel(type=PlotType.Line, transform="Frequency", title=plot_title,
                                      x_str="", x_format=FormatType.Re, x_label="Frequency [Hz]",
                                      y_str="", y_format=FormatType.Im, y_label="",
                                      line_enable=True, line_style="-", line_size=2,
                                      marker_enable=False, marker_style=".",
                                      meridian=(0, 0), options=None)
                self.plt_models.append(plt_model)

                x = t2n(self._freq.reshape(1, -1))
                y = s[:, rcvr_index, src_index].reshape(-1, x.shape[-1])
                line_color = next(color_cycle)
                options = {"colors": line_color}
                self.plots[plt_index] = self.previewPlotWidget.set_plot(self.fig_model, ax_model.title,
                                                                        ax_model, plt_model.title,
                                                                        plt_model, x, y, options)
                legend_lines.append(Line2D([0], [0], color=line_color, lw=4))
                legend_labels.append(plt_model.title)
                xlim = (x.min(), x.max())
                ylim = (-10, 0)
                ylabel = "Sxx [dB]" if src_index == rcvr_index else "Sxy [dB]"
                self.previewPlotWidget.update_axis(ax_model, xlabel="Freq", ylabel=ylabel, xlim=xlim, ylim=ylim)
        r_ax = fig.get_axes()[0]
        v_span = 0.05*num_ports
        r_ax.legend(legend_lines, legend_labels, bbox_to_anchor=(0.05, 1 - v_span, 0.9, v_span), loc=3, ncol=num_ports,
                    mode="expand", borderaxespad=0., bbox_transform=fig.transFigure)
        fig.tight_layout(pad=0, h_pad=0, w_pad=0, rect=(0, 0, 1, 1 - v_span))
        self.previewPlotWidget.update()

    def update(self):
        num_ports = len(self.ports)
        ds = self._model.datagroup_model()[Settings().datagroup].dataset(Settings().dataset)
        self._model.compute_sparameters(ds)
        s = rU2dBU(ds.s[...])
        fig = self.previewPlotWidget.gcf()
        legend_lines = list()
        legend_labels = list()
        for ax in fig.get_axes():
            ax.clear()
        for src_index, src_port in enumerate(self.ports):
            for rcvr_index, rcvr_port in enumerate(self.ports):
                ax_model = self.r_ax_model if src_index == rcvr_index else self.t_ax_model
                plt_index = src_index*num_ports + rcvr_index
                plt_model = self.plt_models[plt_index]
                plt = self.plots[plt_index]

                x = t2n(self._freq.reshape(1, -1))
                y = s[:, rcvr_index, src_index].reshape(-1, x.shape[-1])
                line_color = plt.get_color()
                options = {"colors": line_color}
                self.plots[plt_index] = self.previewPlotWidget.set_plot(self.fig_model, ax_model.title,
                                                                        ax_model, plt_model.title,
                                                                        plt_model, x, y, options)
                legend_lines.append(Line2D([0], [0], color=line_color, lw=4))
                legend_labels.append(plt_model.title)
                xlim = (x.min(), x.max())
                ylim = (-10, 0)
                ylabel = "Sxx [dB]" if src_index == rcvr_index else "Sxy [dB]"
                self.previewPlotWidget.update_axis(ax_model, xlabel="Freq", ylabel=ylabel, xlim=xlim, ylim=ylim)
        r_ax = fig.get_axes()[0]
        v_span = 0.05 * num_ports
        r_ax.legend(legend_lines, legend_labels, bbox_to_anchor=(0.05, 1 - v_span, 0.9, v_span), loc=3, ncol=num_ports,
                    mode="expand", borderaxespad=0., bbox_transform=fig.transFigure)
        self.previewPlotWidget.update()


class SmallSignalRuntimeView(AbstractRuntimeView):
    """The parent runtime window

    A runtime window that contains:
        * A ProgressUpdateView.
        * A RuntimePortView for each measurement port.

        Keyword Args:
            device_model (DevicesModel):  A reference to all connected device.
            datagroup_model (DatagroupModel): The Datagroup where measurements are being saved.
            parent (QWidget): Parent GUI container.
    """

    resume_request = QtCore.Signal()

    def __init__(self, parent=None):
        super(SmallSignalRuntimeView, self).__init__(parent)

    @QtCore.Slot(object)
    def initialize(self, model):
        self.sparameter_view = SParameterView(model, self.ss_stimulus_ports, parent=self.content_frame)
        self.hbl.addWidget(self.sparameter_view)
        super(SmallSignalRuntimeView, self).initialize(model)

    def update(self, model=None, batch_index=-1, sideview=False, value=False):
        all_ = not (sideview or value)

        if value or all_:
            self.sparameter_view.update()

        super(SmallSignalRuntimeView, self).update(model=model, batch_index=batch_index, sideview=sideview, value=value)

if __name__ == "__main__":
    pass
