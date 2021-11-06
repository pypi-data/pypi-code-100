import os
import sys
import importlib
import unittest

import yaml
import torch as th
from numpy.testing import *

from sknrf.enums.runtime import SI, si_eps_map, si_dtype_map
from sknrf.enums.sequencer import Sweep, sid2b
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.instrument.rfsource.base import NoRFSource, NoRFSourcePulsed, NoRFSourceModulated
from sknrf.device.signal import tf
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestRFSourceCWNew(unittest.TestCase):
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
        cls.rfsource = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfsource = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.rfsource, NoRFSource):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFSource" % (self.rfsource.__class__.__name__,))
        AbstractDevice.__init__(self.rfsource, *self.args, **self.kwargs)
        self.rfsource.connect_handles()
        self.rfsource.__info__()
        self.rfsource.preset()

    def test_01_ap_min_bound(self):
        min_ = self.rfsource.info["_a_p"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.A])

    def test_02_ap_max_bound(self):
        max_ = self.rfsource.info["_a_p"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.A]).max)

    def test_03_get_ap(self):
        get_ = self.rfsource.a_p
        assert_array_equal(get_.shape, self.shape)

    def test_04_set_ap(self):
        set_ = self.rfsource.info["_a_p"].max*th.ones(self.shape, dtype=si_dtype_map[SI.A])
        self.rfsource.a_p = set_
        self.assertTrue(True)

    def test_05_set_get_ap(self):
        set_ = self.rfsource.info["_a_p"].max*th.ones(self.shape, dtype=si_dtype_map[SI.A])
        abs_tol = self.rfsource.info["_a_p"].abs_tol
        rel_tol = self.rfsource.info["_a_p"].rel_tol
        self.rfsource.a_p = set_
        get_ = self.rfsource.a_p.detach().numpy()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def test_06_set_get_ap_zeros(self):
        set_ = self.rfsource.info["_a_p"].max*th.ones(self.shape, dtype=si_dtype_map[SI.A])
        abs_tol = self.rfsource.info["_a_p"].abs_tol
        rel_tol = self.rfsource.info["_a_p"].rel_tol
        self.rfsource.a_p = th.zeros(self.shape, dtype=si_dtype_map[SI.A])
        self.rfsource.a_p = set_
        get_ = self.rfsource.a_p.detach().numpy()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def tearDown(self):
        self.rfsource.disconnect_handles()
        del self.rfsource


class TestRFSourcePulsedNew(unittest.TestCase):
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
        cls.rfsource = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfsource = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.rfsource, NoRFSourcePulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFSourcePulsed" % (self.rfsource.__class__.__name__,))
        AbstractDevice.__init__(self.rfsource, *self.args, **self.kwargs)
        self.rfsource.connect_handles()
        self.rfsource.__info__()
        self.rfsource.preset()

    def test_01_get_pulse_width(self):
        _ = self.rfsource.pulse_width
        self.assertTrue(True)

    def test_02_get_delay(self):
        _ = self.rfsource.delay
        self.assertTrue(True)

    def tearDown(self):
        self.rfsource.disconnect_handles()
        del self.rfsource


class TestRFSourceCWInit(unittest.TestCase):
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
        cls.rfsource = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfsource = self.class_(*self.args, **self.kwargs)
        self.args[0].set_stimulus(self.args[0].stimulus())
        if not isinstance(self.rfsource, NoRFSource):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFSource" % (self.rfsource.__class__.__name__,))

    def test_01_ap_set_get_min_tol(self):
        abs_tol = self.rfsource.info["_a_p"].abs_tol
        rel_tol = self.rfsource.info["_a_p"].rel_tol
        pk_set = self.rfsource.info["_a_p"].min * th.ones(self.rfsource.num_harmonics, dtype=si_dtype_map[SI.A])
        tf.set_pk(self.rfsource.a_p, pk_set)
        pk_get = tf.pk(self.rfsource.a_p).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_02_ap_set_get_max_tol(self):
        abs_tol = self.rfsource.info["_a_p"].abs_tol
        rel_tol = self.rfsource.info["_a_p"].rel_tol
        pk_set = self.rfsource.info["_a_p"].max * th.ones(self.rfsource.num_harmonics, dtype=si_dtype_map[SI.A])
        tf.set_pk(self.rfsource.a_p, pk_set)
        pk_get = tf.pk(self.rfsource.a_p).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_03_buffer_overwrite(self):
        error_model = self.rfsource._error_model
        port_index = self.rfsource.port
        _a_p_ = error_model._buffers[sid2b(Sweep.A_SET, port_index)][..., 1::]
        self.assertEqual(_a_p_.data_ptr(), self.rfsource._a_p_.data_ptr())

    def tearDown(self):
        self.rfsource.disconnect_handles()
        del self.rfsource


class TestRFSourcePulsedInit(unittest.TestCase):
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
        cls.rfsource = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfsource = self.class_(*self.args, **self.kwargs)
        self.args[0].set_stimulus(self.args[0].stimulus())
        if not isinstance(self.rfsource, NoRFSourcePulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFSourcePulsed" % (self.rfsource.__class__.__name__,))

    def test_01_set_delay_min_pulse_width_max(self):
        self.rfsource.delay = self.rfsource.info["delay"].min
        self.rfsource.pulse_width = self.rfsource.info["pulse_width"].max
        self.assertTrue(True)

    def test_02_set_pulse_width_min_delay_max(self):
        self.rfsource.pulse_width = self.rfsource.info["pulse_width"].min
        self.rfsource.delay = self.rfsource.info["delay"].max
        self.assertTrue(True)

    def test_03_set_get_pulse_width_delay(self):
        pulse_width_set = self.rfsource.info["pulse_width"].min
        delay_set = min(self.rfsource.info["delay"].max, self.rfsource.period - pulse_width_set)
        self.rfsource.pulse_width = pulse_width_set
        self.rfsource.delay = delay_set
        pulse_width_get = self.rfsource.pulse_width
        delay_get = self.rfsource.delay
        assert_allclose(pulse_width_get, pulse_width_set)
        assert_allclose(delay_get, delay_set)

    def test_04_get_pulse_ap(self):
        get_ = self.rfsource.a_p.detach().numpy()
        lower = get_[self.rfsource.time.flatten() < self.rfsource.delay, :]
        upper = get_[self.rfsource.time.flatten() > self.rfsource.delay + self.rfsource.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.A])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.A])

    def test_05_set_get_pulse_width_delay_ap(self):
        with th.no_grad():
            self.rfsource.a_p[...] = min(1.0, self.rfsource.info["a_p"].max)  # todo: Workaround for numerical stability issue
        self.rfsource.pulse_width = self.rfsource.info["pulse_width"].min
        self.rfsource.delay = self.rfsource.info["delay"].max
        get_ = self.rfsource.a_p.detach().numpy()
        lower = get_[self.rfsource.time.flatten() < self.rfsource.delay, :]
        upper = get_[self.rfsource.time.flatten() > self.rfsource.delay + self.rfsource.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.A]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.A]*2**1)

    def tearDown(self):
        self.rfsource.disconnect_handles()
        del self.rfsource


class TestRFSourceModulatedInit(unittest.TestCase):
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
        cls.rfsource = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfsource = self.class_(*self.args, **self.kwargs)
        self.args[0].set_stimulus(self.args[0].stimulus())
        if not isinstance(self.rfsource, NoRFSourceModulated):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFSourceModulated" % (self.rfsource.__class__.__name__,))

    def test_01_set_get_ap_iq(self):
        abs_tol = self.rfsource.info["_a_p"].abs_tol
        rel_tol = self.rfsource.info["_a_p"].rel_tol
        pk_set = self.rfsource.info["_a_p"].max
        iq = th.rand(self.shape, dtype=si_dtype_map[SI.A])  # + 1j*th.rand(self.shape, dtype=si_dtype_map[SI.A])
        iq = iq/th.max(iq.abs(), dim=-2)[0]
        tf.set_pk(self.rfsource.a_p, pk_set)
        tf.set_iq(self.rfsource.a_p, iq)
        get_ = self.rfsource.a_p.detach()
        assert_allclose(get_, pk_set*iq, rel_tol, abs_tol)

    def test_02_set_get_ap_zeros(self):
        abs_tol = self.rfsource.info["_a_p"].abs_tol
        rel_tol = self.rfsource.info["_a_p"].rel_tol
        pk_set = self.rfsource.info["_a_p"].max
        iq = th.zeros(self.shape, dtype=si_dtype_map[SI.A])
        tf.set_pk(self.rfsource.a_p, pk_set)
        tf.set_iq(self.rfsource.a_p, iq)
        pk_get = self.rfsource.a_p.detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def tearDown(self):
        self.rfsource.disconnect_handles()
        del self.rfsource


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestRFSourceCWNew))
    test_suite.addTest(unittest.makeSuite(TestRFSourcePulsedNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestRFSourceCWInit))
    test_suite.addTest(unittest.makeSuite(TestRFSourcePulsedInit))
    test_suite.addTest(unittest.makeSuite(TestRFSourceModulatedInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
