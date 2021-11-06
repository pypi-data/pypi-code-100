import unittest
import os

from sknrf.settings import Settings
from sknrf.enums.sequencer import Sweep

from sknrf.model.base import AbstractModel
from sknrf.device.instrument.lfsource import NoLFSource
from sknrf.device.instrument.rfsource import NoRFSource
from sknrf.model.sequencer.measure import Measure
from sknrf.model.sequencer.sweep.real import LinearSweep
from sknrf.utilities.numeric import Domain

from sknrf.app.dataviewer.model.figure import AxesType, AxisType, PlotType, FormatType
from sknrf.app.dataviewer.model.dataset import preview_plot
from sknrf.app.dataviewer.model.figure import AxesModel, PlotModel

__author__ = 'dtbespal'


class TestDatasetPreviewPlot(unittest.TestCase):

    def parent_object(self):
        dg = AbstractModel.datagroup_model()[Settings().datagroup]
        ds = dg.dataset(Settings().dataset)
        return ds

    def attribute(self):
        return "a_1"

    @classmethod
    def setUpClass(cls):
        AbstractModel.init_test(cls.__name__)
        Settings().datagroup = "TestDatasetPreviewPlot"

    def setUp(self):
        default_axes_type = AxesType.Rectangular
        default_format_type = FormatType.Lin_Mag
        marker_size = 2
        self.ax_model = AxesModel(type=default_axes_type, autoscale=False, title="",
                                  grid=(True, True), gridspec=(slice(0, 1, None), slice(0, 1, None)),
                                  axis=(AxisType.Linear, AxisType.Linear), indep_axis=-2)
        self.plt_model = PlotModel(type=PlotType.Scatter, transform="Envelope", title="",
                                   x_str="", x_format=FormatType.Re, x_label="",
                                   y_str="", y_format=default_format_type, y_label="",
                                   line_enable=False, line_style="", line_size=2,
                                   marker_enable=True, marker_style="x", marker_size=marker_size,
                                   meridian=(0, 0), options=None)
        self.options_map = {}
        self.measure = Measure()
        self.measure.background = True
        self.sweep1 = LinearSweep(False, 0.0, 5.0, 1.0, 0)
        self.measure.add_sweep(Sweep.V_SET, 1, 0, self.sweep1)

    def test_rectangular_tf(self):
        Settings().dataset = "test_rectangular_tf"
        self.measure.swept_measurement((), {})
        axes_type, format_type, transform_type = AxesType.Rectangular, FormatType.Lin_Mag, Domain.TF
        self.ax_model.type = axes_type
        self.plt_model.y_format = format_type

        ds = self.parent_object()
        plot_data = preview_plot(ds, getattr, self.attribute(), [],
                                 self.ax_model, self.plt_model, transform_type, self.options_map)
        ax_model, plt_model, x, y, options_map = plot_data
        self.assertEqual(x.shape[-1], y.shape[-1])

    def test_rectangular_ff(self):
        Settings().dataset = "test_rectangular_ff"
        self.measure.swept_measurement((), {})
        axes_type, format_type, transform_type = AxesType.Rectangular, FormatType.Lin_Mag, Domain.FF
        self.ax_model.type = axes_type
        self.plt_model.y_format = format_type

        ds = self.parent_object()
        plot_data = preview_plot(ds, getattr, self.attribute(), [],
                                 self.ax_model, self.plt_model, transform_type, self.options_map)
        ax_model, plt_model, x, y, options_map = plot_data
        self.assertEqual(x.shape[-1], y.shape[-1])

    def test_rectangular_ft(self):
        Settings().dataset = "test_rectangular_ft"
        self.measure.swept_measurement((), {})
        axes_type, format_type, transform_type = AxesType.Rectangular, FormatType.Lin_Mag, Domain.FT
        self.ax_model.type = axes_type
        self.plt_model.y_format = format_type

        ds = self.parent_object()
        plot_data = preview_plot(ds, getattr, self.attribute(), [],
                                 self.ax_model, self.plt_model, transform_type, self.options_map)
        ax_model, plt_model, x, y, options_map = plot_data
        self.assertEqual(x.shape[-1], y.shape[-1])

    def test_rectangular_tt(self):
        Settings().dataset = "test_rectangular_tt"
        self.measure.swept_measurement((), {})
        axes_type, format_type, transform_type = AxesType.Rectangular, FormatType.Lin_Mag, Domain.TT
        self.ax_model.type = axes_type
        self.plt_model.y_format = format_type

        ds = self.parent_object()
        plot_data = preview_plot(ds, getattr, self.attribute(), [],
                                 self.ax_model, self.plt_model, transform_type, self.options_map)
        ax_model, plt_model, x, y, options_map = plot_data
        self.assertEqual(x.shape[-1], y.shape[-1])

    def test_polar_tf(self):
        Settings().dataset = "test_polar_tf"
        self.measure.swept_measurement((), {})
        axes_type, format_type, transform_type = AxesType.Polar, FormatType.Lin_Mag, Domain.TF
        self.ax_model.type = axes_type
        self.plt_model.y_format = format_type

        ds = self.parent_object()
        plot_data = preview_plot(ds, getattr, self.attribute(), [],
                                 self.ax_model, self.plt_model, transform_type, self.options_map)
        ax_model, plt_model, x, y, options_map = plot_data
        self.assertEqual(x.shape[-1], y.shape[-1])

    def test_smith_tf(self):
        Settings().dataset = "test_polar_tf"
        self.measure.swept_measurement((), {})
        axes_type, format_type, transform_type = AxesType.Smith, FormatType.Lin_Mag, Domain.TF
        self.ax_model.type = axes_type
        self.plt_model.y_format = format_type

        ds = self.parent_object()
        plot_data = preview_plot(ds, getattr, self.attribute(), [],
                                 self.ax_model, self.plt_model, transform_type, self.options_map)
        ax_model, plt_model, x, y, options_map = plot_data
        self.assertEqual(x.shape[-1], y.shape[-1])


class TestLFPreviewPlot(TestDatasetPreviewPlot):

    def parent_object(self):
        obj = NoLFSource(AbstractModel.device_model(), 1)
        return obj

    def attribute(self):
        return "v"


class TestRFPreviewPlot(TestDatasetPreviewPlot):

    def parent_object(self):
        obj = NoRFSource(AbstractModel.device_model(), 1)
        return obj

    def attribute(self):
        return "a_p"
