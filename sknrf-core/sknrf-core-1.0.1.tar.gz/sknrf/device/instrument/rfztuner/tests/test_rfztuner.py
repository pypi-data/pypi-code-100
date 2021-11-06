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
from sknrf.device.instrument.rfztuner.base import NoRFZTuner, NoRFZTunerPulsed, NoRFZTunerModulated
from sknrf.device.signal import tf
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestRFZTunerCWNew(unittest.TestCase):
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
        cls.rfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfztuner = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.rfztuner, NoRFZTuner):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFZTuner" % (self.rfztuner.__class__.__name__,))
        AbstractDevice.__init__(self.rfztuner, *self.args, **self.kwargs)
        self.rfztuner.connect_handles()
        self.rfztuner.__info__()
        self.rfztuner.preset()

    def test_01_gamma_set_min_bound(self):
        min_ = self.rfztuner.info["_gamma_set"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.G])

    def test_02_gamma_set_max_bound(self):
        max_ = self.rfztuner.info["_gamma_set"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.G]).max)

    def test_02_get_gamma_set(self):
        get_ = self.rfztuner.gamma_set
        assert_array_equal(get_.shape, self.shape)

    def test_03_set_gamma_set(self):
        set_ = self.rfztuner.info["_gamma_set"].max*th.ones(self.shape, dtype=si_dtype_map[SI.G])
        self.rfztuner.gamma_set = set_
        self.assertTrue(True)

    def test_04_set_get_gamma_set(self):
        set_ = self.rfztuner.info["_gamma_set"].max*th.ones(self.shape, dtype=si_dtype_map[SI.G])
        abs_tol = self.rfztuner.info["_gamma_set"].abs_tol
        rel_tol = self.rfztuner.info["_gamma_set"].rel_tol
        self.rfztuner.gamma_set = set_
        get_ = self.rfztuner.gamma_set.detach()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def test_05_set_get_gamma_set_zeros(self):
        set_ = self.rfztuner.info["_gamma_set"].max*th.ones(self.shape, dtype=si_dtype_map[SI.G])
        abs_tol = self.rfztuner.info["_gamma_set"].abs_tol
        rel_tol = self.rfztuner.info["_gamma_set"].rel_tol
        self.rfztuner.gamma_set = th.zeros(self.shape, dtype=si_dtype_map[SI.G])
        self.rfztuner.gamma_set = set_
        get_ = self.rfztuner.gamma_set.detach()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def test_06_trigger(self):
        self.rfztuner.trigger()
        self.assertTrue(True)

    def test_07_trigger_measure(self):
        self.rfztuner.trigger()
        self.rfztuner.measure()
        self.assertTrue(True)

    def test_08_gamma_min_bound(self):
        min_ = self.rfztuner.info["_gamma"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.G])

    def test_09_gamma_max_bound(self):
        max_ = self.rfztuner.info["_gamma"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.G]).max)

    def test_10_get_gamma(self):
        self.rfztuner.trigger()
        self.rfztuner.measure()
        get_ = self.rfztuner.gamma
        assert_array_equal(get_.shape, self.shape)

    def tearDown(self):
        self.rfztuner.disconnect_handles()
        del self.rfztuner


class TestRFZTunerPulsedNew(unittest.TestCase):
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
        cls.rfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfztuner = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.rfztuner, NoRFZTunerPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFZTunerPulsed" % (self.rfztuner.__class__.__name__,))
        AbstractDevice.__init__(self.rfztuner, *self.args, **self.kwargs)
        self.rfztuner.connect_handles()
        self.rfztuner.__info__()
        self.rfztuner.preset()

    def test_01_get_pulse_width(self):
        _ = self.rfztuner.pulse_width
        self.assertTrue(True)

    def test_02_get_delay(self):
        _ = self.rfztuner.delay
        self.assertTrue(True)

    def tearDown(self):
        self.rfztuner.disconnect_handles()
        del self.rfztuner


class TestRFZTunerCWInit(unittest.TestCase):
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
        cls.rfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfztuner = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.rfztuner, NoRFZTuner):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFZTuner" % (self.rfztuner.__class__.__name__,))

    def test_01_gamma_set_set_get_min_tol(self):
        abs_tol = self.rfztuner.info["_gamma_set"].abs_tol
        rel_tol = self.rfztuner.info["_gamma_set"].rel_tol
        pk_set = self.rfztuner.info["_gamma_set"].min * th.ones(self.rfztuner.num_harmonics, dtype=si_dtype_map[SI.G])
        tf.set_pk(self.rfztuner.gamma_set, pk_set)
        pk_get = tf.pk(self.rfztuner.gamma_set).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_02_gamma_set_set_get_max_tol(self):
        abs_tol = self.rfztuner.info["_gamma_set"].abs_tol
        rel_tol = self.rfztuner.info["_gamma_set"].rel_tol
        pk_set = self.rfztuner.info["_gamma_set"].max * th.ones(self.rfztuner.num_harmonics, dtype=si_dtype_map[SI.G])
        tf.set_pk(self.rfztuner.gamma_set, pk_set)
        pk_get = tf.pk(self.rfztuner.gamma_set).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_03_buffer_overwrite(self):
        error_model = self.rfztuner._error_model
        port_index = self.rfztuner.port
        _gamma_set_ = error_model._buffers[sid2b(Sweep.G_SET, port_index)][..., 1::]
        self.assertEqual(_gamma_set_.data_ptr(), self.rfztuner._gamma_set_.data_ptr())
        _gamma_ = error_model._buffers[rid2b(Response.G_GET, port_index)][..., 1::]
        self.assertEqual(_gamma_.data_ptr(), self.rfztuner._gamma_.data_ptr())

    def tearDown(self):
        self.rfztuner.disconnect_handles()
        del self.rfztuner


class TestRFZTunerPulsedInit(unittest.TestCase):
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
        cls.rfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfztuner = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.rfztuner, NoRFZTunerPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFZTunerPulsed" % (self.rfztuner.__class__.__name__,))

    def test_01_set_delay_min_pulse_width_max(self):
        self.rfztuner.delay = self.rfztuner.info["delay"].min
        self.rfztuner.pulse_width = self.rfztuner.info["pulse_width"].max
        self.assertTrue(True)

    def test_02_set_pulse_width_min_delay_max(self):
        self.rfztuner.pulse_width = self.rfztuner.info["pulse_width"].min
        self.rfztuner.delay = self.rfztuner.info["delay"].max
        self.assertTrue(True)

    def test_03_get_pulse_gamma_set(self):
        get_ = self.rfztuner.gamma_set.detach().numpy()
        lower = get_[self.rfztuner.time.flatten() < self.rfztuner.delay, :]
        upper = get_[self.rfztuner.time.flatten() > self.rfztuner.delay + self.rfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.G])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.G])

    def test_04_set_get_pulse_width_delay_gamma_set(self):
        self.rfztuner.pulse_width = self.rfztuner.info["pulse_width"].min
        self.rfztuner.delay = self.rfztuner.info["delay"].max
        get_ = self.rfztuner.gamma_set.detach().numpy()
        lower = get_[self.rfztuner.time.flatten() < self.rfztuner.delay, :]
        upper = get_[self.rfztuner.time.flatten() > self.rfztuner.delay + self.rfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.G])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.G])

    def test_05_get_pulse_gamma(self):
        self.rfztuner.trigger()
        self.rfztuner.measure()
        get_ = self.rfztuner.gamma.detach().numpy()
        lower = get_[self.rfztuner.time.flatten() < self.rfztuner.delay, :]
        upper = get_[self.rfztuner.time.flatten() > self.rfztuner.delay + self.rfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.G])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.G])

    def test_06_set_get_pulse_width_delay_gamma(self):
        self.rfztuner.pulse_width = self.rfztuner.info["pulse_width"].min
        self.rfztuner.delay = self.rfztuner.info["delay"].max
        self.rfztuner.trigger()
        self.rfztuner.measure()
        get_ = self.rfztuner.gamma.detach().numpy()
        lower = get_[self.rfztuner.time.flatten() < self.rfztuner.delay, :]
        upper = get_[self.rfztuner.time.flatten() > self.rfztuner.delay + self.rfztuner.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.G])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.G])

    def tearDown(self):
        self.rfztuner.disconnect_handles()
        del self.rfztuner


class TestRFZTunerModulatedInit(unittest.TestCase):
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
        cls.rfztuner = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfztuner = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.rfztuner, NoRFZTunerModulated):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFZTunerModulated" % (self.rfztuner.__class__.__name__,))

    def test_01_set_get_gamma_set_iq(self):
        abs_tol = self.rfztuner.info["_gamma_set"].abs_tol
        rel_tol = self.rfztuner.info["_gamma_set"].rel_tol
        pk_set = self.rfztuner.info["_gamma_set"].max
        iq = th.rand(self.shape, dtype=si_dtype_map[SI.G])  # + 1j*th.rand(self.shape, dtype=si_dtype_map[SI.G])
        iq = iq / th.max(iq.abs(), dim=-2)[0]
        tf.set_pk(self.rfztuner.gamma_set, pk_set)
        tf.set_iq(self.rfztuner.gamma_set, iq)
        get_ = self.rfztuner.gamma_set.detach()
        assert_allclose(get_, pk_set*iq, abs_tol, rel_tol)

    def test_02_set_get_gamma_set_zeros(self):
        abs_tol = self.rfztuner.info["_gamma_set"].abs_tol
        rel_tol = self.rfztuner.info["_gamma_set"].rel_tol
        pk_set = self.rfztuner.info["_gamma_set"].max
        iq = th.zeros(self.shape, dtype=si_dtype_map[SI.Z])
        tf.set_pk(self.rfztuner.gamma_set, pk_set)
        tf.set_iq(self.rfztuner.gamma_set, iq)
        get_ = self.rfztuner.gamma_set.detach()
        assert_allclose(get_, pk_set, abs_tol, rel_tol)

    def tearDown(self):
        self.rfztuner.disconnect_handles()
        del self.rfztuner


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestRFZTunerCWNew))
    test_suite.addTest(unittest.makeSuite(TestRFZTunerPulsedNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestRFZTunerCWInit))
    test_suite.addTest(unittest.makeSuite(TestRFZTunerPulsedInit))
    test_suite.addTest(unittest.makeSuite(TestRFZTunerModulatedInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
