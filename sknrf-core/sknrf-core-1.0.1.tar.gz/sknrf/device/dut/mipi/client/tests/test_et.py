import sys
import importlib
import inspect
import unittest

import math as mt

from sknrf.device import AbstractDevice
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.tests.test_device import LogTestResult
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit
from sknrf.device.dut.mipi.client.tests.test_client import TestMIPIClientNew
from sknrf.device.dut.mipi.client.tests.test_client import TestMIPIClientInit
from sknrf.device.dut.mipi.client.tests.test_client import TestMIPIClientReadWriteSpecific, TestMIPIClientReadWriteGeneric

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestEtNew(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pythoncom.CoInitialize()
        from sknrf.device.tests.test_device import device_module, device_driver
        cls.device_module = importlib.import_module(device_module)
        cls.device_cls = getattr(cls.device_module, device_driver)
        cls.et = None

    def setUp(self):
        from sknrf.device.tests.test_device import positional_args, keyword_args
        self.et = self.device_cls.__new__(self.device_cls, *positional_args, **keyword_args)
        AbstractDevice.__init__(self.et, *positional_args, **keyword_args)
        self.et.connect_handles()
        self.et.__info__()
        self.et.preset()
        self.et.on = True

    def test_01_v_max_finite_limits(self):
        _min = self.et.info["v_max"].min
        _max = self.et.info["v_max"].max
        self.assertTrue(mt.isfinite(_min), "Finite minimum limit not defined for property: v_max")
        self.assertTrue(mt.isfinite(_max), "Finite maximum limit not defined for property: v_max")

    def test_02_v_min_finite_limits(self):
        _min = self.et.info["v_min"].min
        _max = self.et.info["v_min"].max
        self.assertTrue(mt.isfinite(_min), "Finite minimum limit not defined for property: v_min")
        self.assertTrue(mt.isfinite(_max), "Finite maximum limit not defined for property: v_min")

    def test_03_et_gain_finite_limits(self):
        _min = self.et.info["et_gain"].min
        _max = self.et.info["et_gain"].max
        self.assertTrue(mt.isfinite(_min), "Finite minimum limit not defined for property: et_gain")
        self.assertTrue(mt.isfinite(_max), "Finite maximum limit not defined for property: et_gain")

    def test_04_et_offset_finite_limits(self):
        _min = self.et.info["et_offset"].min
        _max = self.et.info["et_offset"].max
        self.assertTrue(mt.isfinite(_min), "Finite minimum limit not defined for property: et_offset")
        self.assertTrue(mt.isfinite(_max), "Finite maximum limit not defined for property: et_offset")

    def test_05_et_cm_finite_limits(self):
        _min = self.et.info["et_cm"].min
        _max = self.et.info["et_cm"].max
        self.assertTrue(mt.isfinite(_min), "Finite minimum limit not defined for property: et_cm")
        self.assertTrue(mt.isfinite(_max), "Finite maximum limit not defined for property: et_cm")

    def tearDown(self):
        self.et.disconnect_handles()
        del self.et


class TestETInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pythoncom.CoInitialize()
        from sknrf.device.tests.test_device import device_module, device_driver
        cls.device_module = importlib.import_module(device_module)
        cls.device_cls = getattr(cls.device_module, device_driver)
        cls.et = None

    def setUp(self):
        from sknrf.device.tests.test_device import positional_args, keyword_args
        self.et = self.device_cls(*positional_args, **keyword_args)
        self.et.on = True

    def test_01_et_mode_sleep(self):
        self.et.on = False
        self.et.et_mode = self.device_module.ET_MOD_MODE.SLEEP
        self.assertTrue(self.et.et_mode == self.device_module.ET_MOD_MODE.SLEEP, "Envelope Tracker did not enter sleep mode")

    def test_02_et_mode_standby(self):
        self.et.et_mode = self.device_module.ET_MOD_MODE.STANDBY
        self.assertTrue(self.et.et_mode == self.device_module.ET_MOD_MODE.STANDBY, "Envelope Tracker did not enter standby mode")

    def test_04_et_mode_apt(self):
        self.et.et_mode = self.device_module.ET_MOD_MODE.APT
        self.assertTrue(self.et.et_mode == self.device_module.ET_MOD_MODE.APT, "Envelope Tracker did not enter APT mode")

    def test_05_et_mode_et(self):
        self.et.et_mode = self.device_module.ET_MOD_MODE.ET
        self.assertTrue(self.et.et_mode == self.device_module.ET_MOD_MODE.ET, "Envelope Tracker did not enter ET mode")

    def test_06_v_max_greater_than_v_min(self):
        self.assertTrue(self.et.v_max > self.et.v_min)

    def tearDown(self):
        self.et.disconnect_handles()
        del self.et


def driver_test_suite():
    from sknrf.device.tests.test_device import device_module, device_driver
    test_suite = unittest.TestSuite()

    device_module_ = importlib.import_module(device_module)
    device_class = getattr(device_module_, device_driver)
    base_classes = inspect.getmro(device_class)

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    if NoMIPIClient in base_classes:
        test_suite.addTest(unittest.makeSuite(TestMIPIClientNew))
    # if NoET in base_classes:
    #     test_suite.addTest(unittest.makeSuite(TestEtNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestMIPIClientInit))
    test_suite.addTest(unittest.makeSuite(TestMIPIClientReadWriteSpecific))
    test_suite.addTest(unittest.makeSuite(TestMIPIClientReadWriteGeneric))
    # if NoET in base_classes:
    #     test_suite.addTest(unittest.makeSuite(TestETInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())