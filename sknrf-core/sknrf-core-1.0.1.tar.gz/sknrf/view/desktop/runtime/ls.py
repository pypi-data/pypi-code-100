import os
import itertools
from collections import OrderedDict
import logging

import matplotlib.pyplot as plt
import numpy as np
import torch as th
import torch.nn.functional as F
from PySide2 import QtCore
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import QFrame, QLabel, QProgressBar
from PySide2.QtWidgets import QGridLayout
from PySide2.QtQuickWidgets import QQuickWidget

from sknrf.app.dataviewer.model import DatagroupModel
from sknrf.model.device import DevicesModel
from sknrf.app.dataviewer.model.figure import FigureModel, AxesModel, PlotModel
from sknrf.app.dataviewer.model.figure import AxesType, AxisType, PlotType, FormatType
from sknrf.settings import Settings
from sknrf.device.signal import tf
from sknrf.enums.runtime import RuntimeState
from sknrf.view.desktop.runtime.base import AbstractRuntimeView
from sknrf.view.desktop.runtime.QRuntimePortFrame import Ui_runtimePortFrame
from sknrf.utilities.numeric import Scale
from sknrf.utilities.rf import rU2dBU

logger = logging.getLogger(__name__)

__author__ = 'dtbespal'

meter_bg_style = "QProgressBar {border: 1px solid black; text-align: top; padding: 1px;" \
                 "border-bottom-right-radius: 7px; border-bottom-left-radius: 7px; " \
                 "background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, " \
                 "stop: 0 #ffffff, stop: 0.4999 #eeeeee, stop: 0.5 #eeeeee, stop: 1.0 #gggggg);}"

meter_fg_style = "QProgressBar::chunk {border-bottom-right-radius: 7px; border-bottom-left-radius: 7px;" \
                 "border: 1px solid black;" \
                 "background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, " \
                 "stop: 0 #ffffff, stop: 0.25 #gggggg, stop: 0.26 #gggggg, stop: 1 #gggggg);}"


def scale(x, x_min, x_max, y_min=0, y_max=100):
    return (x - x_min)/(x_max - x_min)*(y_max - y_min) + y_min


class RuntimePortView(QFrame, Ui_runtimePortFrame):
    """Runtime status of a given port

    Runtime status of a port is presented as:
        * The multi-harmonic port impedance distribution.
        * The multi-harmonic peak incident power-wave (a_p), reflected power-wave (b_p), voltage (v), and current (i).

        Keyword Args:
            model (PortModel): A collection of all device objects connected to a given port.
            parent (QWidget): Parent GUI container.
    """

    def __init__(self, model=None, label="Port", parent=None):
        super(RuntimePortView, self).__init__(parent)
        self.setupUi(self)
        self.gbl = self.meterFrame.layout()

        color_rgb = []
        for color in Settings().color_order:
            color_rgb.append(Settings().color_map[color])
        self._gamma_color_order = color_rgb
        self._gamma_marker_order = Settings().marker_order
        self._gamma_marker_size = plt.rcParams['lines.markersize'] ** 2
        num_harmonics = Settings().num_harmonics
        self.model = model
        self.portLabel.setText(label)
        gamma = tf.avg(self.model.rfztuner.gamma)
        gamma_color_cycle = itertools.cycle(self._gamma_color_order)
        gamma_marker_cycle = itertools.cycle(self._gamma_marker_order)
        gamma_marker_size = self._gamma_marker_size

        self.fig_model = FigureModel(1, gridspec=(1, 1))
        self.previewPlotWidget.gcf().clear()
        ax_model = AxesModel(type=AxesType.Smith, autoscale=True, title="",
                             grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                             axis=(AxisType.Linear, AxisType.Linear), indep_axis=-2)
        self.previewPlotWidget.add_axes(self.fig_model, "impedance", ax_model)
        self.z_plot = [None]*num_harmonics
        for index in range(num_harmonics):
            plt_model = PlotModel(type=PlotType.Scatter, transform="Frequency", title="",
                                  x_str="", x_format=FormatType.Re, x_label="",
                                  y_str="", y_format=FormatType.Im, y_label="",
                                  line_enable=False, line_style="", line_size=2,
                                  marker_enable=True,
                                  marker_style=next(gamma_marker_cycle), marker_size=gamma_marker_size,
                                  meridian=(0, 0), options=None)
            x = gamma[index]
            y = gamma[index]
            options = {"picker": 5, "c": next(gamma_color_cycle)}
            self.z_plot[index] = self.previewPlotWidget.set_plot(self.fig_model, "impedance", ax_model, "plot", plt_model, x, y, options)
        self.previewPlotWidget.update()

        self.v_meters, self.v_limits = self.add_meter_group(model.lfreceiver.v, model.lfreceiver.info["v"], 0, 0, offset=0)
        self.i_meters, self.i_limits = self.add_meter_group(model.lfreceiver.i, model.lfreceiver.info["i"], 1, 0, offset=0)
        self.ap_meters, self.ap_limits = self.add_meter_group(model.rfreceiver.a_p, model.rfreceiver.info["a_p"], 2, 0, offset=1)
        self.bp_meters, self.bp_limits = self.add_meter_group(model.rfreceiver.a_p, model.rfreceiver.info["b_p"], 2+num_harmonics, 0, offset=1)

    def add_meter_group(self, signal, signal_info, y, x, offset=0):
        root = os.path.dirname(os.path.realpath(Settings().root))
        dirname = os.sep.join((root, "sknrf", "view", "desktop", "runtime"))
        filename = QUrl.fromLocalFile(os.sep.join((dirname, "src", "RFGauge.qml")))
        num_harmonics = signal.shape[-1]
        meters = [None]*num_harmonics
        limits = list(np.squeeze(signal_info.max)*np.ones(num_harmonics, np.float))
        for index in range(num_harmonics):
            meters[index] = QQuickWidget(self.meterFrame)
            meters[index].setResizeMode(QQuickWidget.SizeRootObjectToView)
            meters[index].setSource(QUrl(filename))
            meters[index].rootObject().setProperty("name", "%s%d" % (signal_info.label, index + offset))
            self.gbl.addWidget(meters[index], y+index, x, 1, 1)
        return meters, limits

    def closeEvent(self, event):
        meters = self.v_meters + self.i_meters + self.ap_meters + self.bp_meters
        for meter in meters:
            meter.deleteLater()
            del meter

    def update(self):
        v = np.abs(tf.pk(self.model.lfreceiver.v.detach()))
        i = np.abs(tf.pk(self.model.lfreceiver.i.detach()))
        a_p = np.abs(tf.pk(self.model.rfreceiver.a_p.detach()))
        b_p = np.abs(tf.pk(self.model.rfreceiver.b_p.detach()))
        gamma = tf.avg(self.model.rfztuner.gamma.detach()).reshape(-1, 1)
        # gamma.dtype = np.float
        # gamma = gamma.reshape((-1, 2))
        gamma = F.pad(input=gamma, pad=(0, 1, 0, 0), mode='constant', value=0)
        index = 0
        self.v_meters[index].rootObject().setProperty("value", float(rU2dBU(v[index]/self.v_limits[index])))
        self.i_meters[index].rootObject().setProperty("value", float(rU2dBU(i[index]/self.i_limits[index])))
        for index in range(1):
            self.ap_meters[index].rootObject().setProperty("value", float(rU2dBU(a_p[index]/self.ap_limits[index])))
            self.bp_meters[index].rootObject().setProperty("value", float(rU2dBU(b_p[index]/self.bp_limits[index])))
            # self.z_plot[index].set_offsets(gamma[index].transpose())
            self.z_plot[index].set_offsets(gamma[index, :])
        self.previewPlotWidget.canvas.draw()


class LargeSignalRuntimeView(AbstractRuntimeView):
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
        super(LargeSignalRuntimeView, self).__init__(parent)

    @QtCore.Slot(object)
    def initialize(self, model):
        self.port_frames = [None] * len(model.ports)
        for port_index, port_num in enumerate(model.ports):
            self.port_frames[port_index] = RuntimePortView(model.device_model().ports[port_num],
                                                           label="Port " + str(port_num),
                                                           parent=self.content_frame)
            self.hbl.addWidget(self.port_frames[port_index])
        super(LargeSignalRuntimeView, self).initialize(model)

    def closeEvent(self, event):
        if Settings().runtime_state != RuntimeState.STOPPED:
            Settings().runtime_state = RuntimeState.STOPPED
            event.ignore()
            return
        for port_frame in reversed(self.port_frames):
            port_frame.closeEvent(event)
        super(AbstractRuntimeView, self).closeEvent(event)

    def update(self, model=None, batch_index=-1, sideview=False, value=False):
        all_ = not (sideview or value)

        if value or all_:
            for port_frame in self.port_frames:
                port_frame.update()

        super(LargeSignalRuntimeView, self).update(model=model, batch_index=batch_index, sideview=sideview, value=value)


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QApplication

    from sknrf.model.base import AbstractModel
    from sknrf.model.sequencer.measure import Measure

    dg_dir = os.sep.join((Settings().data_root, "datagroups"))
    pdmv = (Settings().num_ports, Settings().num_duts, Settings().num_mipi, Settings().num_video)
    Settings().datagroup = dg = "ls"
    Settings().dataset = ds = "Single"
    AbstractModel.set_device_model(DevicesModel(*pdmv))
    AbstractModel.set_datagroup_model({dg: DatagroupModel(os.sep.join((dg_dir, dg + ".h5")), mode="w")})
    dg_model = AbstractModel.datagroup_model()
    dg_model[dg].add(ds)

    measure = Measure()
    measure.background = True
    app = QApplication(sys.argv)
    form = LargeSignalRuntimeView()
    form.initialize(measure)
    form.showMaximized()
    form.update()
    sys.exit(app.exec_())
