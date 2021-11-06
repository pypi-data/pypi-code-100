import os
import sys
import importlib
import unittest

import yaml
import torch as th
from numpy.testing import *

from sknrf.enums.runtime import SI, si_eps_map, si_dtype_map
from sknrf.enums.device import Response, rid2b
from sknrf.enums.sequencer import Sweep, sid2b
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.instrument.lfztuner.base import NoLFZTuner, NoLFZTunerPulsed, NoLFZTunerModulated
from sknrf.device.signal import tf
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestLFZTunerCWNew(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AbstractModel.init()
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.lfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfztuner = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.lfztuner, NoLFZTuner):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFZTuner" % (self.lfztuner.__class__.__name__,))
        AbstractDevice.__init__(self.lfztuner, *self.args, **self.kwargs)
        self.lfztuner.connect_handles()
        self.lfztuner.__info__()
        self.lfztuner.preset()

    def test_01_z_set_min_bound(self):
        min_ = self.lfztuner.info["_z_set"].min
        self.assertGreater(min_, th.finfo(si_dtype_map[SI.Z]).min)

    def test_02_z_set_max_bound(self):
        max_ = self.lfztuner.info["_z_set"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.Z]).max)

    def test_03_get_z_set(self):
        get_ = self.lfztuner.z_set
        assert_array_equal(get_.shape, self.shape)
        assert_array_equal(get_.shape, self.shape)

    def test_04_set_z_set(self):
        set_ = self.lfztuner.info["_z_set"].max*th.ones(self.shape, dtype=si_dtype_map[SI.Z])
        self.lfztuner.z_set = set_
        self.assertTrue(True)

    def test_05_set_get_z_set(self):
        set_ = self.lfztuner.info["_z_set"].max*th.ones(self.shape, dtype=si_dtype_map[SI.Z])
        abs_tol = self.lfztuner.info["_z_set"].abs_tol
        rel_tol = self.lfztuner.info["_z_set"].rel_tol
        self.lfztuner.z_set = set_
        get_ = self.lfztuner.z_set.detach()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def test_06_set_get_z_set_zeros(self):
        set_ = self.lfztuner.info["_z_set"].max*th.ones(self.shape, dtype=si_dtype_map[SI.Z])
        abs_tol = self.lfztuner.info["_z_set"].abs_tol
        rel_tol = self.lfztuner.info["_z_set"].rel_tol
        self.lfztuner.z_set = th.zeros(self.shape, dtype=si_dtype_map[SI.Z])
        self.lfztuner.z_set = set_
        get_ = self.lfztuner.z_set.detach()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def test_07_trigger(self):
        self.lfztuner.trigger()
        self.assertTrue(True)

    def test_08_trigger_measure(self):
        self.lfztuner.trigger()
        self.lfztuner.measure()
        self.assertTrue(True)

    def test_09_z_min_bound(self):
        min_ = self.lfztuner.info["_z"].min
        self.assertGreater(min_, th.finfo(si_dtype_map[SI.Z]).min)

    def test_10_z_max_bound(self):
        max_ = self.lfztuner.info["_z"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.Z]).max)

    def test_10_get_z(self):
        self.lfztuner.trigger()
        self.lfztuner.measure()
        get_ = self.lfztuner.z
        assert_array_equal(get_.shape, self.shape)

    def tearDown(self):
        self.lfztuner.disconnect_handles()
        del self.lfztuner


class TestLFZTunerPulsedNew(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init()
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.lfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfztuner = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.lfztuner, NoLFZTunerPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFZTunerPulsed" % (self.lfztuner.__class__.__name__,))
        AbstractDevice.__init__(self.lfztuner, *self.args, **self.kwargs)
        self.lfztuner.connect_handles()
        self.lfztuner.__info__()
        self.lfztuner.preset()

    def test_01_get_pulse_width(self):
        _ = self.lfztuner.pulse_width
        self.assertTrue(True)

    def test_02_get_delay(self):
        _ = self.lfztuner.delay
        self.assertTrue(True)

    def tearDown(self):
        self.lfztuner.disconnect_handles()
        del self.lfztuner


class TestLFZTunerCWInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.lfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfztuner = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfztuner, NoLFZTuner):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFSource" % (self.lfztuner.__class__.__name__,))

    def test_01_z_set_set_get_min_tol(self):
        abs_tol = self.lfztuner.info["_z_set"].abs_tol
        rel_tol = self.lfztuner.info["_z_set"].rel_tol
        pk_set = self.lfztuner.info["_z_set"].min * th.ones(self.lfztuner.num_harmonics, dtype=si_dtype_map[SI.Z])
        tf.set_pk(self.lfztuner.z_set, pk_set)
        pk_get = tf.pk(self.lfztuner.z_set).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_02_z_set_set_get_max_tol(self):
        abs_tol = self.lfztuner.info["_z_set"].abs_tol
        rel_tol = self.lfztuner.info["_z_set"].rel_tol
        pk_set = self.lfztuner.info["_z_set"].max * th.ones(self.lfztuner.num_harmonics, dtype=si_dtype_map[SI.Z])
        tf.set_pk(self.lfztuner.z_set, pk_set)
        pk_get = tf.pk(self.lfztuner.z_set).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_03_buffer_overwrite(self):
        error_model = self.lfztuner._error_model
        port_index = self.lfztuner.port
        _z_set_ = error_model._buffers[sid2b(Sweep.Z_SET, port_index)][..., 0:1]
        self.assertEqual(_z_set_.data_ptr(), self.lfztuner._z_set_.data_ptr())
        _z_ = error_model._buffers[rid2b(Response.Z_GET, port_index)][..., 0:1]
        self.assertEqual(_z_.data_ptr(), self.lfztuner._z_.data_ptr())

    def tearDown(self):
        self.lfztuner.disconnect_handles()
        del self.lfztuner


class TestLFZTunerPulsedInit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init()
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.lfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfztuner = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfztuner, NoLFZTunerPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFZTunerPulsed" % (self.lfztuner.__class__.__name__,))

    def test_01_set_delay_min_pulse_width_max(self):
        self.lfztuner.delay = self.lfztuner.info["delay"].min
        self.lfztuner.pulse_width = self.lfztuner.info["pulse_width"].max
        self.assertTrue(True)

    def test_02_set_pulse_width_min_delay_max(self):
        self.lfztuner.pulse_width = self.lfztuner.info["pulse_width"].min
        self.lfztuner.delay = self.lfztuner.info["delay"].max
        self.assertTrue(True)

    def test_03_get_pulse_z_set(self):
        get_ = self.lfztuner.z_set.detach().numpy()
        lower = get_[self.lfztuner.time.flatten() < self.lfztuner.delay, :]
        upper = get_[self.lfztuner.time.flatten() > self.lfztuner.delay + self.lfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.Z])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.Z])

    def test_04_set_get_pulse_width_delay_z_set(self):
        self.lfztuner.pulse_width = self.lfztuner.info["pulse_width"].min
        self.lfztuner.delay = self.lfztuner.info["delay"].max
        get_ = self.lfztuner.z_set.detach().numpy()
        lower = get_[self.lfztuner.time.flatten() < self.lfztuner.delay, :]
        upper = get_[self.lfztuner.time.flatten() > self.lfztuner.delay + self.lfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.Z])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.Z])

    def test_05_get_pulse_z(self):
        self.lfztuner.trigger()
        self.lfztuner.measure()
        get_ = self.lfztuner.z.detach().numpy()
        lower = get_[self.lfztuner.time.flatten() < self.lfztuner.delay, :]
        upper = get_[self.lfztuner.time.flatten() > self.lfztuner.delay + self.lfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.Z])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.Z])

    def test_06_set_get_pulse_width_delay_z(self):
        self.lfztuner.pulse_width = self.lfztuner.info["pulse_width"].min
        self.lfztuner.delay = self.lfztuner.info["delay"].max
        self.lfztuner.trigger()
        self.lfztuner.measure()
        get_ = self.lfztuner.z.detach().numpy()
        lower = get_[self.lfztuner.time.flatten() < self.lfztuner.delay, :]
        upper = get_[self.lfztuner.time.flatten() > self.lfztuner.delay + self.lfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.Z])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.Z])

    def tearDown(self):
        self.lfztuner.disconnect_handles()
        del self.lfztuner


class TestLFZTunerModulatedInit(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        AbstractModel.init()
        if sys.platform == "win32": pythoncom.CoInitialize()
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.lfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfztuner = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfztuner, NoLFZTunerModulated):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFZTunerModulated" % (self.lfztuner.__class__.__name__,))

    def test_01_set_get_z_set_iq(self):
        abs_tol = self.lfztuner.info["_z_set"].abs_tol
        rel_tol = self.lfztuner.info["_z_set"].rel_tol
        pk_set = self.lfztuner.info["_z_set"].max
        iq = th.rand(self.shape, dtype=si_dtype_map[SI.Z])  # + 1j*th.rand(self.shape, dtype=si_dtype_map[SI.Z])
        iq = iq / th.max(iq.abs(), dim=-2)[0]
        tf.set_pk(self.lfztuner.z_set, pk_set)
        tf.set_iq(self.lfztuner.z_set, iq)
        get_ = self.lfztuner.z_set.detach()
        assert_allclose(get_, pk_set*iq, abs_tol, rel_tol)

    def test_02_set_get_z_set_zeros(self):
        abs_tol = self.lfztuner.info["_z_set"].abs_tol
        rel_tol = self.lfztuner.info["_z_set"].rel_tol
        pk_set = self.lfztuner.info["_z_set"].max
        iq = th.zeros(self.shape, dtype=si_dtype_map[SI.Z])
        tf.set_pk(self.lfztuner.z_set, pk_set)
        tf.set_iq(self.lfztuner.z_set, iq)
        self.lfztuner.trigger()
        self.lfztuner.measure()
        get_ = self.lfztuner.z_set.detach()
        assert_allclose(get_, pk_set, abs_tol, rel_tol)

    def tearDown(self):
        self.lfztuner.disconnect_handles()
        del self.lfztuner


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestLFZTunerCWNew))
    test_suite.addTest(unittest.makeSuite(TestLFZTunerPulsedNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestLFZTunerCWInit))
    test_suite.addTest(unittest.makeSuite(TestLFZTunerPulsedInit))
    test_suite.addTest(unittest.makeSuite(TestLFZTunerModulatedInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
