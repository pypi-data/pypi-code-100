import os
import sys
import importlib
import unittest

import yaml
import torch as th
from numpy.testing import *

from sknrf.enums.runtime import SI, si_eps_map, si_dtype_map
from sknrf.enums.sequencer import Sweep, sid2b
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.instrument.lfsource.base import NoLFSource, NoLFSourcePulsed, NoLFSourceModulated
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.signal import tf
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestLFSourceCWNew(unittest.TestCase):
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
        cls.lfsource = None
        cls.shape = (Settings().t_points, 1)

    def setUp(self):
        self.lfsource = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.lfsource, NoLFSource):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFSource" % (self.lfsource.__class__.__name__,))
        AbstractDevice.__init__(self.lfsource, *self.args, **self.kwargs)
        self.lfsource.connect_handles()
        self.lfsource.__info__()
        self.lfsource.preset()

    def test_01_v_min_bound(self):
        min_ = self.lfsource.info["_v"].min
        self.assertGreaterEqual(min_, si_eps_map[SI.V])

    def test_02_v_max_bound(self):
        max_ = self.lfsource.info["_v"].max
        self.assertLess(max_, th.finfo(si_dtype_map[SI.V]).max)

    def test_03_get_v(self):
        get_ = self.lfsource.v
        assert_array_equal(get_.shape, self.shape)

    def test_04_set_v(self):
        set_ = self.lfsource.info["_v"].max*th.ones(self.shape, dtype=si_dtype_map[SI.V])
        self.lfsource.v = set_
        self.assertTrue(True)

    def test_05_set_get_v(self):
        set_ = self.lfsource.info["_v"].max * th.ones(self.shape, dtype=si_dtype_map[SI.V])
        abs_tol = self.lfsource.info["_v"].abs_tol
        rel_tol = self.lfsource.info["_v"].rel_tol
        self.lfsource.v = set_
        get_ = self.lfsource.v.detach()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def test_06_set_get_v_zeros(self):
        set_ = self.lfsource.info["_v"].max * th.ones(self.shape, dtype=si_dtype_map[SI.V])
        abs_tol = self.lfsource.info["_v"].abs_tol
        rel_tol = self.lfsource.info["_v"].rel_tol
        self.lfsource.v = th.zeros(self.shape, dtype=si_dtype_map[SI.V])
        self.lfsource.v = set_
        get_ = self.lfsource.v.detach()
        assert_allclose(get_, set_, rel_tol, abs_tol)

    def tearDown(self):
        self.lfsource.disconnect_handles()
        del self.lfsource


class TestLFSourcePulsedNew(unittest.TestCase):
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
        cls.lfsource = None
        cls.shape = (Settings().t_points, 1)

    def setUp(self):
        self.lfsource = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.lfsource, NoLFSourcePulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of LFSourcePulsed" % (self.lfsource.__class__.__name__,))
        AbstractDevice.__init__(self.lfsource, *self.args, **self.kwargs)
        self.lfsource.connect_handles()
        self.lfsource.__info__()
        self.lfsource.preset()

    def test_01_get_pulse_width(self):
        _ = self.lfsource.pulse_width
        self.assertTrue(True)

    def test_02_get_delay(self):
        _ = self.lfsource.delay
        self.assertTrue(True)

    def tearDown(self):
        self.lfsource.disconnect_handles()
        del self.lfsource


class TestLFSourceCWInit(unittest.TestCase):
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
        cls.lfsource = None
        cls.shape = (Settings().t_points, 1)

    def setUp(self):
        self.lfsource = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfsource, NoLFSource):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFSource" % (self.lfsource.__class__.__name__,))

    def test_01_v_set_get_min_tol(self):
        abs_tol = self.lfsource.info["_v"].abs_tol
        rel_tol = self.lfsource.info["_v"].rel_tol
        pk_set = self.lfsource.info["_v"].min * th.ones(self.lfsource.num_harmonics, dtype=si_dtype_map[SI.V])
        tf.set_pk(self.lfsource.v, pk_set)
        pk_get = tf.pk(self.lfsource.v).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_02_v_set_get_max_tol(self):
        abs_tol = self.lfsource.info["_v"].abs_tol
        rel_tol = self.lfsource.info["_v"].rel_tol
        pk_set = self.lfsource.info["_v"].max * th.ones(self.lfsource.num_harmonics, dtype=si_dtype_map[SI.V])
        tf.set_pk(self.lfsource.v, pk_set)
        pk_get = tf.pk(self.lfsource.v).detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def test_03_buffer_overwrite(self):
        device_model = self.lfsource._error_model
        port_index = self.lfsource.port
        _v_ = device_model._buffers[sid2b(Sweep.V_SET, port_index)][..., 0:1]
        self.assertEqual(_v_.data_ptr(), self.lfsource._v_.data_ptr())

    def tearDown(self):
        self.lfsource.disconnect_handles()
        del self.lfsource


class TestLFSourcePulsedInit(unittest.TestCase):
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
        cls.lfsource = None
        cls.shape = (Settings().t_points, 1)

    def setUp(self):
        self.lfsource = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfsource, NoLFSourcePulsed):
            self.tearDown()
            self.skipTest("%s: is not instance of LFSourcePulsed" % (self.lfsource.__class__.__name__,))

    def test_01_set_delay_min_pulse_width_max(self):
        self.lfsource.delay = self.lfsource.info["delay"].min
        self.lfsource.pulse_width = self.lfsource.info["pulse_width"].max
        self.assertTrue(True)

    def test_02_set_pulse_width_min_delay_max(self):
        self.lfsource.pulse_width = self.lfsource.info["pulse_width"].min
        self.lfsource.delay = self.lfsource.info["delay"].max
        self.assertTrue(True)

    def test_03_set_get_pulse_width_delay(self):
        pulse_width_set = self.lfsource.info["pulse_width"].min
        delay_set = min(self.lfsource.info["delay"].max, self.lfsource.period - pulse_width_set)
        self.lfsource.pulse_width = pulse_width_set
        self.lfsource.delay = delay_set
        pulse_width_get = self.lfsource.pulse_width
        delay_get = self.lfsource.delay
        assert_allclose(pulse_width_get, pulse_width_set)
        assert_allclose(delay_get, delay_set)

    def test_04_get_pulse_v(self):
        get_ = self.lfsource.v.detach().numpy()
        lower = get_[self.lfsource.time.flatten() < self.lfsource.delay, :]
        upper = get_[self.lfsource.time.flatten() > self.lfsource.delay + self.lfsource.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.V])
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.V])

    def test_05_set_get_pulse_width_delay_v(self):
        with th.no_grad():
            self.lfsource.v[...] = min(1.0, self.lfsource.info["v"].max)  # todo: Workaround for numerical stability issue
        self.lfsource.pulse_width = self.lfsource.info["pulse_width"].min
        self.lfsource.delay = self.lfsource.info["delay"].max
        get_ = self.lfsource.v.detach().numpy()
        lower = get_[self.lfsource.time.flatten() < self.lfsource.delay, :]
        upper = get_[self.lfsource.time.flatten() > self.lfsource.delay + self.lfsource.pulse_width, :]
        assert_allclose(lower, 0.0, atol=si_eps_map[SI.V]*2**1)
        assert_allclose(upper, 0.0, atol=si_eps_map[SI.V]*2**1)

    def tearDown(self):
        self.lfsource.disconnect_handles()
        del self.lfsource


class TestLFSourceModulatedInit(unittest.TestCase):
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
        cls.lfsource = None
        cls.shape = (Settings().t_points, 1)

    def setUp(self):
        self.lfsource = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.lfsource, NoLFSourceModulated):
            self.tearDown()
            self.skipTest("%s: is not instance of NoLFSourceModulated" % (self.lfsource.__class__.__name__,))

    def test_01_set_get_v_iq(self):
        abs_tol = self.lfsource.info["_v"].abs_tol
        rel_tol = self.lfsource.info["_v"].rel_tol
        pk_set = self.lfsource.info["_v"].max
        iq = th.rand(self.shape, dtype=si_dtype_map[SI.V])
        iq = iq/th.max(iq.abs(), dim=-2)[0]
        tf.set_pk(self.lfsource.v, pk_set)
        tf.set_iq(self.lfsource.v, iq)
        get_ = self.lfsource.v.detach()
        assert_allclose(get_, pk_set*iq, rel_tol, abs_tol)

    def test_02_set_get_v_zeros(self):
        abs_tol = self.lfsource.info["_v"].abs_tol
        rel_tol = self.lfsource.info["_v"].rel_tol
        pk_set = self.lfsource.info["_v"].max
        iq = th.zeros(self.shape, dtype=si_dtype_map[SI.V])
        tf.set_pk(self.lfsource.v, pk_set)
        tf.set_iq(self.lfsource.v, iq)
        pk_get = self.lfsource.v.detach()
        assert_allclose(pk_get, pk_set, rel_tol, abs_tol)

    def tearDown(self):
        self.lfsource.disconnect_handles()
        del self.lfsource


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestLFSourceCWNew))
    test_suite.addTest(unittest.makeSuite(TestLFSourcePulsedNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestLFSourceCWInit))
    test_suite.addTest(unittest.makeSuite(TestLFSourcePulsedInit))
    test_suite.addTest(unittest.makeSuite(TestLFSourceModulatedInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
