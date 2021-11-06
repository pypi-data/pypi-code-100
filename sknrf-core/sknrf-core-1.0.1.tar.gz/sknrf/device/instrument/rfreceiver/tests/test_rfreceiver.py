import os
import sys
import importlib
import unittest

import yaml
import torch as th
from numpy.testing import *

from sknrf.enums.runtime import SI, si_eps_map, si_dtype_map
from sknrf.enums.device import Response, rid2b
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.instrument.rfreceiver.base import NoRFReceiver, NoRFReceiverPulsed, NoRFReceiverModulated
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestRFReceiverCWNew(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AbstractModel.init()
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.rfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfreceiver = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.rfreceiver, NoRFReceiver):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFReceiver" % (self.rfreceiver.__class__.__name__,))
        AbstractDevice.__init__(self.rfreceiver, *self.args, **self.kwargs)
        self.rfreceiver.connect_handles()
        self.rfreceiver.__info__()
        self.rfreceiver.preset()
        self.rfreceiver.on = True

    def test_01_ap_min_bound(self):
        min_ = self.rfreceiver.info["_a_p"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.A])

    def test_02_ap_max_bound(self):
        max_ = self.rfreceiver.info["_a_p"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.A]).max)

    def test_03_bp_min_bound(self):
        min_ = self.rfreceiver.info["_b_p"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.B])

    def test_04_bp_max_bound(self):
        max_ = self.rfreceiver.info["_b_p"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.B]).max)

    def test_05_trigger(self):
        self.rfreceiver.trigger()
        self.assertTrue(True)

    def test_06_trigger_measure(self):
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        self.assertTrue(True)

    def test_07_get_ap(self):
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        get_ = self.rfreceiver.a_p
        assert_array_equal(get_.shape, self.shape)

    def test_08_get_bp(self):
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        get_ = self.rfreceiver.b_p
        assert_array_equal(get_.shape, self.shape)

    def tearDown(self):
        self.rfreceiver.disconnect_handles()
        del self.rfreceiver


class TestRFReceiverPulsedNew(unittest.TestCase):
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
        cls.rfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfreceiver = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.rfreceiver, NoRFReceiverPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFReceiverPulsed" % (self.rfreceiver.__class__.__name__,))
        AbstractDevice.__init__(self.rfreceiver, *self.args, **self.kwargs)
        self.rfreceiver.connect_handles()
        self.rfreceiver.__info__()
        self.rfreceiver.preset()
        self.rfreceiver.on = True

    def test_01_get_pulse_width(self):
        _ = self.rfreceiver.pulse_width
        self.assertTrue(True)

    def test_02_get_delay(self):
        _ = self.rfreceiver.delay
        self.assertTrue(True)

    def test_03_set_delay_min_pulse_width_max(self):
        self.rfreceiver.delay = self.rfreceiver.info["delay"].min
        self.rfreceiver.pulse_width = self.rfreceiver.info["pulse_width"].max
        self.assertTrue(True)

    def test_04_set_pulse_width_min_delay_max(self):
        self.rfreceiver.pulse_width = self.rfreceiver.info["pulse_width"].min
        self.rfreceiver.delay = self.rfreceiver.info["delay"].max
        self.assertTrue(True)

    def test_05_set_get_pulse_width_delay(self):
        pulse_width_set = self.rfreceiver.info["pulse_width"].min
        delay_set = min(self.rfreceiver.info["delay"].max, self.rfreceiver.period)
        self.rfreceiver.pulse_width = pulse_width_set
        self.rfreceiver.delay = delay_set
        pulse_width_get = self.rfreceiver.pulse_width
        delay_get = self.rfreceiver.delay
        assert_allclose(pulse_width_get, pulse_width_set)
        assert_allclose(delay_get, delay_set)

    def tearDown(self):
        self.rfreceiver.disconnect_handles()
        del self.rfreceiver


class TestRFReceiverCWInit(unittest.TestCase):
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
        cls.rfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfreceiver = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.rfreceiver, NoRFReceiver):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFReceiver" % (self.rfreceiver.__class__.__name__,))
        self.rfreceiver.on = True

    def test_01_buffer_overwrite(self):
        error_model = self.rfreceiver._error_model
        port_index = self.rfreceiver.port
        _a_p_ = error_model._buffers[rid2b(Response.A_GET, port_index)][..., 1::]
        self.assertEqual(_a_p_.data_ptr(), self.rfreceiver._a_p_.data_ptr())
        _b_p_ = error_model._buffers[rid2b(Response.B_GET, port_index)][..., 1::]
        self.assertEqual(_b_p_.data_ptr(), self.rfreceiver._b_p_.data_ptr())

    def tearDown(self):
        self.rfreceiver.disconnect_handles()
        del self.rfreceiver


class TestRFReceiverPulsedInit(unittest.TestCase):
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
        cls.rfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfreceiver = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.rfreceiver, NoRFReceiverPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFReceiverPulsed" % (self.rfreceiver.__class__.__name__,))
        self.rfreceiver.on = True

    def test_01_get_pulse_a_p(self):
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        get_ = self.rfreceiver.a_p.detach().numpy()
        lower = get_[self.rfreceiver.time.flatten() < self.rfreceiver.delay, :]
        upper = get_[self.rfreceiver.time.flatten() > self.rfreceiver.delay + self.rfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.A]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.A]*2**1)

    def test_02_set_get_pulse_width_delay_a_p(self):
        self.rfreceiver.pulse_width = self.rfreceiver.info["pulse_width"].min
        self.rfreceiver.delay = self.rfreceiver.info["delay"].max
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        get_ = self.rfreceiver.a_p.detach().numpy()
        lower = get_[self.rfreceiver.time.flatten() < self.rfreceiver.delay, :]
        upper = get_[self.rfreceiver.time.flatten() > self.rfreceiver.delay + self.rfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.A]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.A]*2**1)

    def test_03_get_pulse_b_p(self):
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        get_ = self.rfreceiver.b_p.detach().numpy()
        lower = get_[self.rfreceiver.time.flatten() < self.rfreceiver.delay, :]
        upper = get_[self.rfreceiver.time.flatten() > self.rfreceiver.delay + self.rfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.B]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.B]*2**1)

    def test_04_set_get_pulse_width_delay_b_p(self):
        self.rfreceiver.pulse_width = self.rfreceiver.info["pulse_width"].min
        self.rfreceiver.delay = self.rfreceiver.info["delay"].max
        self.rfreceiver.trigger()
        self.rfreceiver.measure()
        get_ = self.rfreceiver.b_p.detach().numpy()
        lower = get_[self.rfreceiver.time.flatten() < self.rfreceiver.delay, :]
        upper = get_[self.rfreceiver.time.flatten() > self.rfreceiver.delay + self.rfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.B]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.B]*2**1)

    def tearDown(self):
        self.rfreceiver.disconnect_handles()
        del self.rfreceiver


class TestRFReceiverModulatedInit(unittest.TestCase):
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
        cls.rfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.rfreceiver = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.rfreceiver, NoRFReceiverModulated):
            self.tearDown()
            self.skipTest("%s: is not instance of NoRFReceiverModulated" % (self.rfreceiver.__class__.__name__,))

    def tearDown(self):
        self.rfreceiver.disconnect_handles()
        del self.rfreceiver


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestRFReceiverCWNew))
    test_suite.addTest(unittest.makeSuite(TestRFReceiverPulsedNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestRFReceiverCWInit))
    test_suite.addTest(unittest.makeSuite(TestRFReceiverPulsedInit))
    test_suite.addTest(unittest.makeSuite(TestRFReceiverModulatedInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
