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
from sknrf.device.instrument.lfreceiver.base import NoLFReceiver, NoLFReceiverPulsed, NoLFReceiverModulated
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestLFReceiverCWNew(unittest.TestCase):
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
        cls.lfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfreceiver = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.lfreceiver, NoLFReceiver):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFReceiver" % (self.lfreceiver.__class__.__name__,))
        AbstractDevice.__init__(self.lfreceiver, *self.args, **self.kwargs)
        self.lfreceiver.connect_handles()
        self.lfreceiver.__info__()
        self.lfreceiver.preset()
        self.lfreceiver.on = True

    def test_01_v_min_bound(self):
        min_ = self.lfreceiver.info["_v"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.V])

    def test_02_v_max_bound(self):
        max_ = self.lfreceiver.info["_v"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.V]).max)

    def test_03_i_min_bound(self):
        min_ = self.lfreceiver.info["_i"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.I])

    def test_04_i_max_bound(self):
        max_ = self.lfreceiver.info["_i"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.I]).max)

    def test_05_trigger(self):
        self.lfreceiver.trigger()
        self.assertTrue(True)

    def test_06_trigger_measure(self):
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        self.assertTrue(True)

    def test_07_get_v(self):
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        get_ = self.lfreceiver.v
        assert_array_equal(get_.shape, self.shape)

    def test_08_get_i(self):
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        get_ = self.lfreceiver.i
        assert_array_equal(get_.shape, self.shape)

    def tearDown(self):
        self.lfreceiver.disconnect_handles()
        del self.lfreceiver


class TestLFReceiverPulsedNew(unittest.TestCase):
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
        cls.lfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfreceiver = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.lfreceiver, NoLFReceiverPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFReceiverPulsed" % (self.lfreceiver.__class__.__name__,))
        AbstractDevice.__init__(self.lfreceiver, *self.args, **self.kwargs)
        self.lfreceiver.connect_handles()
        self.lfreceiver.__info__()
        self.lfreceiver.preset()
        self.lfreceiver.on = True

    def test_01_get_pulse_width(self):
        _ = self.lfreceiver.pulse_width
        self.assertTrue(True)

    def test_02_get_delay(self):
        _ = self.lfreceiver.delay
        self.assertTrue(True)

    def test_03_set_delay_min_pulse_width_max(self):
        self.lfreceiver.delay = self.lfreceiver.info["delay"].min
        self.lfreceiver.pulse_width = self.lfreceiver.info["pulse_width"].max
        self.assertTrue(True)

    def test_04_set_pulse_width_min_delay_max(self):
        self.lfreceiver.pulse_width = self.lfreceiver.info["pulse_width"].min
        self.lfreceiver.delay = self.lfreceiver.info["delay"].max
        self.assertTrue(True)

    def test_05_set_get_pulse_width_delay(self):
        pulse_width_set = self.lfreceiver.info["pulse_width"].min
        delay_set = min(self.lfreceiver.info["delay"].max, self.lfreceiver.period) - pulse_width_set
        self.lfreceiver.pulse_width = pulse_width_set
        self.lfreceiver.delay = delay_set
        pulse_width_get = self.lfreceiver.pulse_width
        delay_get = self.lfreceiver.delay
        assert_allclose(pulse_width_get, pulse_width_set)
        assert_allclose(delay_get, delay_set)

    def tearDown(self):
        self.lfreceiver.disconnect_handles()
        del self.lfreceiver


class TestLFReceiverCWInit(unittest.TestCase):
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
        cls.lfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfreceiver = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfreceiver, NoLFReceiver):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFReceiver" % (self.lfreceiver.__class__.__name__,))
        self.lfreceiver.on = True

    def test_01_buffer_overwrite(self):
        error_model = self.lfreceiver._error_model
        port_index = self.lfreceiver.port
        _v_ = error_model._buffers[rid2b(Response.V_GET, port_index)][..., 0:1]
        self.assertEqual(_v_.data_ptr(), self.lfreceiver._v_.data_ptr())
        _i_ = error_model._buffers[rid2b(Response.I_GET, port_index)][..., 0:1]
        self.assertEqual(_i_.data_ptr(), self.lfreceiver._i_.data_ptr())

    def tearDown(self):
        self.lfreceiver.disconnect_handles()
        del self.lfreceiver


class TestLFReceiverPulsedInit(unittest.TestCase):
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
        cls.lfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfreceiver = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfreceiver, NoLFReceiverPulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFReceiverPulsed" % (self.lfreceiver.__class__.__name__,))
        self.lfreceiver.on = True

    def test_01_get_pulse_v(self):
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        get_ = self.lfreceiver.v.detach().numpy()
        lower = get_[self.lfreceiver.time.flatten() < self.lfreceiver.delay, :]
        upper = get_[self.lfreceiver.time.flatten() > self.lfreceiver.delay + self.lfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.V]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.V]*2**1)

    def test_02_set_get_pulse_width_delay_v(self):
        self.lfreceiver.pulse_width = self.lfreceiver.info["pulse_width"].min
        self.lfreceiver.delay = self.lfreceiver.info["delay"].max
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        get_ = self.lfreceiver.v.detach().numpy()
        lower = get_[self.lfreceiver.time.flatten() < self.lfreceiver.delay, :]
        upper = get_[self.lfreceiver.time.flatten() > self.lfreceiver.delay + self.lfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.V]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.V]*2**1)

    def test_03_get_pulse_i(self):
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        get_ = self.lfreceiver.i.detach().numpy()
        lower = get_[self.lfreceiver.time.flatten() < self.lfreceiver.delay, :]
        upper = get_[self.lfreceiver.time.flatten() > self.lfreceiver.delay + self.lfreceiver.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.I]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.I]*2**1)

    def test_04_set_get_pulse_width_delay_i(self):
        self.lfreceiver.pulse_width = self.lfreceiver.info["pulse_width"].min
        self.lfreceiver.delay = self.lfreceiver.info["delay"].max
        self.lfreceiver.trigger()
        self.lfreceiver.measure()
        get_ = self.lfreceiver.i.detach().numpy()
        lower = get_[self.lfreceiver.time.flatten() < self.lfreceiver.delay]
        upper = get_[self.lfreceiver.time.flatten() > self.lfreceiver.delay + self.lfreceiver.pulse_width]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.I]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.I]*2**1)

    def tearDown(self):
        self.lfreceiver.disconnect_handles()
        del self.lfreceiver


class TestLFReceiverModulatedInit(unittest.TestCase):
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
        cls.lfreceiver = None
        cls.shape = (Settings().t_points, Settings().num_harmonics)

    def setUp(self):
        self.lfreceiver = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfreceiver, NoLFReceiverModulated):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFReceiverModulated" % (self.lfreceiver.__class__.__name__,))

    def tearDown(self):
        self.lfreceiver.disconnect_handles()
        del self.lfreceiver


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestLFReceiverCWNew))
    test_suite.addTest(unittest.makeSuite(TestLFReceiverPulsedNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestLFReceiverCWInit))
    test_suite.addTest(unittest.makeSuite(TestLFReceiverPulsedInit))
    test_suite.addTest(unittest.makeSuite(TestLFReceiverModulatedInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
