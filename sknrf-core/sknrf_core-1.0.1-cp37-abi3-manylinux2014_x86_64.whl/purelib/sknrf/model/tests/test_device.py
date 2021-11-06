import sys
import unittest
import os
import pickle

from numpy.testing import *
import torch as th

from sknrf.enums.runtime import Bound, SI, si_eps_map
from sknrf.enums.device import Response, response_fill_map
from sknrf.enums.mipi import MIPI_READ_MODE, MIPI_WRITE_MODE, MIPI_ADDRESS_LIMIT
from sknrf.enums.sequencer import Sweep, sweep_fill_map
from sknrf.enums.modulation import POWER_CLASS, CA, DF_OOB
from sknrf.settings import Settings
from sknrf.model.device import DevicesModel
from sknrf.device.signal.tf import delta_like
from sknrf.model.base import AbstractModel
from sknrf.device.instrument.lfsource.base import NoLFSource, NoLFSourcePulsed, NoLFSourceModulated
from sknrf.device.instrument.lfreceiver.base import NoLFReceiver, NoLFReceiverPulsed, NoLFReceiverModulated, FromLFSource
from sknrf.device.instrument.lfztuner.base import NoLFZTuner, NoLFZTunerPulsed, NoLFZTunerModulated
from sknrf.device.instrument.rfsource.base import NoRFSource, NoRFSourcePulsed, NoRFSourceModulated
from sknrf.device.instrument.rfreceiver.base import NoRFReceiver, NoRFReceiverPulsed, NoRFReceiverModulated, FromRFSource
from sknrf.device.instrument.rfztuner.base import NoRFZTuner, NoRFZTunerPulsed, NoRFZTunerModulated
from sknrf.device.dut.base import NoDUT
from sknrf.device.dut.mipi.server.base import NoMIPIServer
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.dut.video.base import NoVideo
from sknrf.device.instrument.auxiliary.pm.base import NoPM
from sknrf.device.instrument.auxiliary.sa.base import NoSA
from sknrf.device.instrument.auxiliary.vna.base import NoVNA
from sknrf.app.dataviewer.model.dataset import IQFile
from sknrf.utilities.rf import a2v, v2a

if sys.platform == "win32": import pythoncom


__author__ = 'dtbespal'

root = os.sep.join((Settings().root, "model", "sequencer", "tests"))
dirname = os.sep.join((Settings().data_root, "testdata"))


class TestDeviceSaveLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pdmv = Settings().num_ports, Settings().num_duts, Settings().num_mipi, Settings().num_video
        AbstractModel.set_device_model(DevicesModel(*pdmv))

    def setUp(self):
        pass

    def test_save(self):
        filename = os.sep.join((dirname, "saved_state.p"))
        with open(filename, "wb") as file_id:
            pickle.dump(Settings(), file_id)
            pickle.dump(AbstractModel.device_model(), file_id)

    def test_save_pulsed(self):
        filename = os.sep.join((dirname, "saved_state.p"))
        error_model = AbstractModel.device_model()
        [NoLFSourcePulsed(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoLFReceiverPulsed(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoLFZTunerPulsed(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFSourcePulsed(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFReceiverPulsed(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFZTunerPulsed(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        with open(filename, "wb") as file_id:
            pickle.dump(Settings(), file_id)
            pickle.dump(AbstractModel.device_model(), file_id)

    def test_save_modulated(self):
        filename = os.sep.join((dirname, "saved_state.p"))
        error_model = AbstractModel.device_model()
        [NoLFSourceModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoLFReceiverModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoLFZTunerModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFSourceModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFReceiverModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFZTunerModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        with open(filename, "wb") as file_id:
            pickle.dump(Settings(), file_id)
            pickle.dump(AbstractModel.device_model(), file_id)

    def test_save_modulated_from_source(self):
        filename = os.sep.join((dirname, "saved_state.p"))
        error_model = AbstractModel.device_model()
        [NoLFSourceModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [FromLFSource(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoLFZTunerModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFSourceModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [FromRFSource(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        [NoRFZTunerModulated(error_model, port_index) for port_index in range(0, Settings().num_ports+1)]
        with open(filename, "wb") as file_id:
            pickle.dump(Settings(), file_id)
            pickle.dump(AbstractModel.device_model(), file_id)

    def test_load(self):
        self.test_save()
        filename = os.sep.join((dirname, "saved_state.p"))
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(filename, "rb") as file_id:
            Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))
            AbstractModel.device_model().disconnect_handles()
            AbstractModel.set_device_model(pickle.load(file_id))

    def test_load_pulsed(self):
        self.test_save_pulsed()
        filename = os.sep.join((dirname, "saved_state.p"))
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(filename, "rb") as file_id:
            Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))
            AbstractModel.device_model().disconnect_handles()
            AbstractModel.set_device_model(pickle.load(file_id))

    def test_load_modulated(self):
        self.test_save_modulated()
        filename = os.sep.join((dirname, "saved_state.p"))
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(filename, "rb") as file_id:
            Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))
            AbstractModel.device_model().disconnect_handles()
            AbstractModel.set_device_model(pickle.load(file_id))

    def test_load_modulated_from_source(self):
        self.test_save_modulated_from_source()
        filename = os.sep.join((dirname, "saved_state.p"))
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(filename, "rb") as file_id:
            Settings().__setstate__(pickle.load(file_id).__getstate__(state={}))
            AbstractModel.device_model().disconnect_handles()
            AbstractModel.set_device_model(pickle.load(file_id))

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()


class TestDeviceConnections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pdmv = Settings().num_ports, Settings().num_duts, Settings().num_mipi, Settings().num_video
        AbstractModel.set_device_model(DevicesModel(*pdmv))
        self.error_model = AbstractModel.device_model()
        Settings().bound = Bound.OFF
        self.iq_file = IQFile(os.sep.join((Settings().data_root, "signals", "CW.h5")))

    def test_lfsource(self):
        old_device = self.error_model.ports[0].lfsource
        device = NoLFSource(self.error_model, 0)
        new_device = self.error_model.ports[0].lfsource
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, 0.0)
        assert_allclose(device.num_harmonics, 1)
        assert_allclose(device.freq, Settings().freq[0:1])
        assert_allclose(device.time, Settings().time)
        a_get = device.a_p.detach()
        assert_allclose(device._v, sweep_fill_map[Sweep.V_SET], atol=si_eps_map[SI.V])
        assert_allclose(device.v.detach(), sweep_fill_map[Sweep.V_SET], atol=si_eps_map[SI.V])
        assert_allclose(a_get, v2a(th.as_tensor(sweep_fill_map[Sweep.V_SET]))[0], atol=si_eps_map[SI.A])
        device.a_p = a_get
        assert_allclose(device.a_p.detach(), a_get, atol=si_eps_map[SI.A])

    def test_lfsource_pulsed(self):
        old_device = self.error_model.ports[0].lfsource
        device = NoLFSourcePulsed(self.error_model, 0)
        new_device = self.error_model.ports[0].lfsource
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.pulse_width = Settings().t_fall - Settings().t_rise
        device.delay = Settings().t_rise
        a_get = device.a_p.detach()
        assert_allclose(device._v, sweep_fill_map[Sweep.V_SET], atol=si_eps_map[SI.V])
        assert_allclose(device.v.detach(), sweep_fill_map[Sweep.V_SET], atol=si_eps_map[SI.V])
        assert_allclose(a_get, v2a(th.as_tensor(sweep_fill_map[Sweep.V_SET]))[0], atol=si_eps_map[SI.A])
        device.a_p = a_get
        assert_allclose(device.a_p.detach(), a_get, atol=si_eps_map[SI.A])

    def test_lfsource_modulated(self):
        old_device = self.error_model.ports[0].lfsource
        device = NoLFSourceModulated(self.error_model, 0)
        new_device = self.error_model.ports[0].lfsource
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.iq_files = [self.iq_file]*device.num_harmonics
        a_get = device.a_p.detach()
        assert_allclose(device._v, sweep_fill_map[Sweep.V_SET], atol=si_eps_map[SI.V])
        assert_allclose(device.v.detach(), sweep_fill_map[Sweep.V_SET], atol=si_eps_map[SI.V])
        assert_allclose(a_get, v2a(th.as_tensor(sweep_fill_map[Sweep.V_SET]))[0], atol=si_eps_map[SI.A])
        device.a_p = a_get
        assert_allclose(device.a_p.detach(), a_get, atol=si_eps_map[SI.A])

    def test_lfreceiver(self):
        old_device = self.error_model.ports[0].lfreceiver
        device = NoLFReceiver(self.error_model, 0)
        new_device = self.error_model.ports[0].lfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, 0.0)
        assert_allclose(device.num_harmonics, 1)
        assert_allclose(device.freq, Settings().freq[0:1])
        assert_allclose(device.time, Settings().time)
        assert_allclose(device._v, response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device._i, response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])
        assert_allclose(device.v.detach(), response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device.i.detach(), response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])

    def test_lfreceiver_pulsed(self):
        old_device = self.error_model.ports[0].lfreceiver
        device = NoLFReceiverPulsed(self.error_model, 0)
        new_device = self.error_model.ports[0].lfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.pulse_width = Settings().t_fall - Settings().t_rise
        device.delay = Settings().t_rise
        assert_allclose(device._v, response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device._i, response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])
        assert_allclose(device.v.detach(), response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device.i.detach(), response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])

    def test_lfreceiver_modulated(self):
        old_device = self.error_model.ports[0].lfreceiver
        device = NoLFReceiverModulated(self.error_model, 0)
        new_device = self.error_model.ports[0].lfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device._v, response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device._i, response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])
        assert_allclose(device.v.detach(), response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device.i.detach(), response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])

    def test_lfreceiver_from_lfsource(self):
        old_device = self.error_model.ports[0].lfreceiver
        device = FromLFSource(self.error_model, 0)
        new_device = self.error_model.ports[0].lfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, 0.0)
        assert_allclose(device.num_harmonics, 1)
        assert_allclose(device.freq, Settings().freq[0:1])
        assert_allclose(device.time, Settings().time)
        assert_allclose(device._v, response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device._i, response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])
        assert_allclose(device.v.detach(), response_fill_map[Response.V_GET], atol=si_eps_map[SI.V])
        assert_allclose(device.i.detach(), response_fill_map[Response.I_GET], atol=si_eps_map[SI.I])

    def test_lfztuner(self):
        old_device = self.error_model.ports[0].lfztuner
        device = NoLFZTuner(self.error_model, 0)
        new_device = self.error_model.ports[0].lfztuner
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, 0.0)
        assert_allclose(device.num_harmonics, 1)
        assert_allclose(device.freq, Settings().freq[0:1])
        assert_allclose(device.time, Settings().time)
        z_get = delta_like(device._z, response_fill_map[Response.Z_GET])
        z_set = delta_like(device._z_set, sweep_fill_map[Sweep.Z_SET])
        assert_allclose(device._z, z_get, atol=si_eps_map[SI.Z])
        assert_allclose(device.z.detach(), z_get, atol=si_eps_map[SI.Z])
        assert_allclose(device._z_set, z_set, atol=si_eps_map[SI.Z])
        assert_allclose(device.z_set.detach(), z_set, atol=si_eps_map[SI.Z])

    def test_lfztuner_pulsed(self):
        old_device = self.error_model.ports[0].lfztuner
        device = NoLFZTunerPulsed(self.error_model, 0)
        new_device = self.error_model.ports[0].lfztuner
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.pulse_width = Settings().t_fall - Settings().t_rise
        device.delay = Settings().t_rise
        z_get = delta_like(device._z, response_fill_map[Response.Z_GET])
        z_set = delta_like(device._z_set, sweep_fill_map[Sweep.Z_SET])
        assert_allclose(device._z, z_get, atol=si_eps_map[SI.Z])
        assert_allclose(device.z.detach(), z_get, atol=si_eps_map[SI.Z])
        assert_allclose(device._z_set, z_set, atol=si_eps_map[SI.Z])
        assert_allclose(device.z_set.detach(), z_set, atol=si_eps_map[SI.Z])

    def test_lfztuner_modulated(self):
        old_device = self.error_model.ports[0].lfztuner
        device = NoLFZTunerModulated(self.error_model, 0)
        new_device = self.error_model.ports[0].lfztuner
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.iq_files = [self.iq_file]*device.num_harmonics
        z_get = delta_like(device._z, response_fill_map[Response.Z_GET])
        z_set = device._z_set
        assert_allclose(device._z, z_get, atol=si_eps_map[SI.Z])
        assert_allclose(device.z.detach(), z_get, atol=si_eps_map[SI.Z])
        assert_allclose(device._z_set, z_set, atol=si_eps_map[SI.Z])
        assert_allclose(device.z_set.detach(), z_set, atol=si_eps_map[SI.Z])

    def test_rfsource(self):
        old_device = self.error_model.ports[0].rfsource
        device = NoRFSource(self.error_model, 0)
        new_device = self.error_model.ports[0].rfsource
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, Settings().f0)
        assert_allclose(device.num_harmonics, Settings().num_harmonics)
        assert_allclose(device.freq, Settings().freq[1::])
        assert_allclose(device.time, Settings().time)
        v_get = device.v_s.detach()
        assert_allclose(device._a_p, sweep_fill_map[Sweep.A_SET], atol=si_eps_map[SI.A])
        assert_allclose(device.a_p.detach(), sweep_fill_map[Sweep.A_SET], atol=si_eps_map[SI.A])
        assert_allclose(v_get, a2v(th.as_tensor(sweep_fill_map[Sweep.A_SET]))[0], atol=si_eps_map[SI.V])
        device.v_s = v_get
        assert_allclose(device.v_s.detach(), v_get, atol=si_eps_map[SI.V])

    def test_rfsource_pulsed(self):
        old_device = self.error_model.ports[0].rfsource
        device = NoRFSourcePulsed(self.error_model, 0)
        new_device = self.error_model.ports[0].rfsource
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.pulse_width = Settings().t_fall - Settings().t_rise
        device.delay = Settings().t_rise
        v_get = device.v_s.detach()
        assert_allclose(device._a_p, sweep_fill_map[Sweep.A_SET], atol=si_eps_map[SI.A])
        assert_allclose(device.a_p.detach(), sweep_fill_map[Sweep.A_SET], atol=si_eps_map[SI.A])
        assert_allclose(v_get, a2v(th.as_tensor(sweep_fill_map[Sweep.A_SET]))[0], atol=si_eps_map[SI.V])
        device.v_s = v_get
        assert_allclose(device.v_s.detach(), v_get, atol=si_eps_map[SI.V])

    def test_rfsource_modulated(self):
        old_device = self.error_model.ports[0].rfsource
        device = NoRFSourceModulated(self.error_model, 0)
        new_device = self.error_model.ports[0].rfsource
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.iq_files = [self.iq_file]*device.num_harmonics
        v_get = device.v_s.detach()
        assert_allclose(device._a_p, sweep_fill_map[Sweep.A_SET], atol=si_eps_map[SI.A])
        assert_allclose(device.a_p.detach(), sweep_fill_map[Sweep.A_SET], atol=si_eps_map[SI.A])
        assert_allclose(v_get, a2v(th.as_tensor(sweep_fill_map[Sweep.A_SET]))[0], atol=si_eps_map[SI.V])
        device.v_s = v_get
        assert_allclose(device.v_s.detach(), v_get, atol=si_eps_map[SI.V])

    def test_rfreceiver(self):
        old_device = self.error_model.ports[0].rfreceiver
        device = NoRFReceiver(self.error_model, 0)
        new_device = self.error_model.ports[0].rfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, Settings().f0)
        assert_allclose(device.num_harmonics, Settings().num_harmonics)
        assert_allclose(device.freq, Settings().freq[1::])
        assert_allclose(device.time, Settings().time)
        assert_allclose(device._b_p, response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device._a_p, response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])
        assert_allclose(device.b_p.detach(), response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device.a_p.detach(), response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])

    def test_rfreceiver_pulsed(self):
        old_device = self.error_model.ports[0].rfreceiver
        device = NoRFReceiverPulsed(self.error_model, 0)
        new_device = self.error_model.ports[0].rfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.pulse_width = Settings().t_fall - Settings().t_rise
        device.delay = Settings().t_rise
        assert_allclose(device._b_p, response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device._a_p, response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])
        assert_allclose(device.b_p.detach(), response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device.a_p.detach(), response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])

    def test_rfreceiver_modulated(self):
        old_device = self.error_model.ports[0].rfreceiver
        device = NoRFReceiverModulated(self.error_model, 0)
        new_device = self.error_model.ports[0].rfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device._b_p, response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device._a_p, response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])
        assert_allclose(device.b_p.detach(), response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device.a_p.detach(), response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])

    def test_rfreceiver_from_rfsource(self):
        old_device = self.error_model.ports[0].rfreceiver
        device = FromRFSource(self.error_model, 0)
        new_device = self.error_model.ports[0].rfreceiver
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, Settings().f0)
        assert_allclose(device.num_harmonics, Settings().num_harmonics)
        assert_allclose(device.freq, Settings().freq[1::])
        assert_allclose(device.time, Settings().time)
        assert_allclose(device._b_p, response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device._a_p, response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])
        assert_allclose(device.b_p.detach(), response_fill_map[Response.B_GET], atol=si_eps_map[SI.B])
        assert_allclose(device.a_p.detach(), response_fill_map[Response.A_GET], atol=si_eps_map[SI.A])

    def test_rfztuner(self):
        old_device = self.error_model.ports[0].rfztuner
        device = NoRFZTuner(self.error_model, 0)
        new_device = self.error_model.ports[0].rfztuner
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.f0, Settings().f0)
        assert_allclose(device.num_harmonics, Settings().num_harmonics)
        assert_allclose(device.freq, Settings().freq[1::])
        assert_allclose(device.time, Settings().time)
        g_get = delta_like(device._gamma, response_fill_map[Response.G_GET])
        g_set = delta_like(device._gamma_set, sweep_fill_map[Sweep.G_SET])
        assert_allclose(device._gamma, g_get, atol=si_eps_map[SI.G])
        assert_allclose(device.gamma.detach(), g_get, atol=si_eps_map[SI.G])
        assert_allclose(device._gamma_set, g_set, atol=si_eps_map[SI.G])
        assert_allclose(device.gamma_set.detach(), g_set, atol=si_eps_map[SI.G])

    def test_rfztuner_pulsed(self):
        old_device = self.error_model.ports[0].rfztuner
        device = NoRFZTunerPulsed(self.error_model, 0)
        new_device = self.error_model.ports[0].rfztuner
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.pulse_width = Settings().t_fall - Settings().t_rise
        device.delay = Settings().t_rise
        g_get = delta_like(device._gamma, response_fill_map[Response.G_GET])
        g_set = delta_like(device._gamma_set, sweep_fill_map[Sweep.G_SET])
        assert_allclose(device._gamma, g_get, atol=si_eps_map[SI.G])
        assert_allclose(device.gamma.detach(), g_get, atol=si_eps_map[SI.G])
        assert_allclose(device._gamma_set, g_set, atol=si_eps_map[SI.G])
        assert_allclose(device.gamma_set.detach(), g_set, atol=si_eps_map[SI.G])

    def test_rfztuner_modulated(self):
        old_device = self.error_model.ports[0].rfztuner
        device = NoRFZTunerModulated(self.error_model, 0)
        new_device = self.error_model.ports[0].rfztuner
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.iq_files = [self.iq_file]*device.num_harmonics
        g_get = delta_like(device._gamma, response_fill_map[Response.G_GET])
        g_set = device._gamma_set
        assert_allclose(device._gamma, g_get, atol=si_eps_map[SI.G])
        assert_allclose(device.gamma.detach(), g_get, atol=si_eps_map[SI.G])
        assert_allclose(device._gamma_set, g_set, atol=si_eps_map[SI.G])
        assert_allclose(device.gamma_set.detach(), g_set, atol=si_eps_map[SI.G])

    def test_dut(self):
        old_device = self.error_model.duts[0]
        device = NoDUT(self.error_model, 0)
        new_device = self.error_model.duts[0]
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)

    def test_dut_mipi_server(self):
        old_device = self.error_model.duts[0].mipi_server
        device = NoMIPIServer(self.error_model, 0)
        new_device = self.error_model.duts[0].mipi_server
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        device.read_mode = MIPI_READ_MODE.BASIC
        self.assertRaises(NotImplementedError, device.read, *(0, 0x00))
        device.read_mode = MIPI_READ_MODE.EXTENDED
        self.assertRaises(NotImplementedError, device.read, *(0, 0x00))
        device.read_mode = MIPI_READ_MODE.EXTENDED_LONG
        self.assertRaises(NotImplementedError, device.read, *(0, 0x00))
        device.read_mode = MIPI_READ_MODE.GENERIC
        self.assertRaises(NotImplementedError, device.read, *(0, MIPI_ADDRESS_LIMIT.BASIC))
        self.assertRaises(NotImplementedError, device.read, *(0, MIPI_ADDRESS_LIMIT.EXTENDED))
        self.assertRaises(NotImplementedError, device.read, *(0, MIPI_ADDRESS_LIMIT.EXTENDED_LONG))
        device.write_mode = MIPI_WRITE_MODE.REG0
        self.assertRaises(NotImplementedError, device.write, *(0, 0x00, 0x00))
        device.write_mode = MIPI_WRITE_MODE.BASIC
        self.assertRaises(NotImplementedError, device.write, *(0, 0x00, 0x00))
        device.write_mode = MIPI_WRITE_MODE.EXTENDED
        self.assertRaises(NotImplementedError, device.write, *(0, 0x00, 0x00))
        device.write_mode = MIPI_WRITE_MODE.EXTENDED_LONG
        self.assertRaises(NotImplementedError, device.write, *(0, 0x00, 0x00))
        device.write_mode = MIPI_WRITE_MODE.GENERIC
        self.assertRaises(NotImplementedError, device.write, *(0, MIPI_ADDRESS_LIMIT.REG0, 0x00))
        self.assertRaises(NotImplementedError, device.write, *(0, MIPI_ADDRESS_LIMIT.BASIC, 0x00))
        self.assertRaises(NotImplementedError, device.write, *(0, MIPI_ADDRESS_LIMIT.EXTENDED, 0x00))
        self.assertRaises(NotImplementedError, device.write, *(0, MIPI_ADDRESS_LIMIT.EXTENDED_LONG, 0x00))

    def test_dut_mipi_client(self):
        old_device = self.error_model.duts[0].mipi[0]
        device = NoMIPIClient(self.error_model, 0, mipi=0)
        new_device = self.error_model.duts[0].mipi[0]
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)

    def test_dut_video(self):
        old_device = self.error_model.duts[0].video[0]
        device = NoVideo(self.error_model, 0, video=0)
        new_device = self.error_model.duts[0].video[0]
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.video.detach(), response_fill_map[Response.VIDEO], atol=response_fill_map[Response.VIDEO])

    def test_aux_pm(self):
        old_device = self.error_model.aux[0]
        device = NoPM(self.error_model, 2)
        new_device = self.error_model.aux[0]
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.p.detach(), response_fill_map[Response.P], atol=response_fill_map[Response.P])

    def test_aux_sa(self):
        old_device = self.error_model.aux[1]
        device = NoSA(self.error_model, 2)
        new_device = self.error_model.aux[1]
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.psd.detach(), response_fill_map[Response.PSD], atol=response_fill_map[Response.PSD])

    def test_aux_vna(self):
        old_device = self.error_model.aux[2]
        device = NoVNA(self.error_model, 2)
        new_device = self.error_model.aux[2]
        self.assertIsNot(device, old_device)
        self.assertIs(device, new_device)
        assert_allclose(device.sp.detach(), response_fill_map[Response.SP], atol=response_fill_map[Response.SP])

    def tearDown(self):
        for datagroup in AbstractModel.datagroup_model().values():
            datagroup.close()

    @classmethod
    def tearDownClass(cls):
        pass
