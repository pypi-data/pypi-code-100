import os
import sys
import importlib
import unittest

import yaml
from sknrf.enums.device import Response, response_shape_map
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.dut.base import NoDUT
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestDUTNew(unittest.TestCase):
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
        cls.dut = None

    def setUp(self):
        self.dut = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.dut, NoDUT):
            self.skipTest("%s: is not instance of NoDUT" % (self.dut.__class__.__name__,))
        AbstractDevice.__init__(self.dut, *self.args, **self.kwargs)
        self.dut.connect_handles()
        self.dut.__info__()
        self.dut.preset()

    def tearDown(self):
        self.dut.disconnect_handles()
        del self.dut


class TestDUTInit(unittest.TestCase):
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
        cls.dut = None

    def setUp(self):
        self.dut = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.dut, NoDUT):
            self.skipTest("%s: is not instance of NoDUT" % (self.dut.__class__.__name__,))

    def tearDown(self):
        self.dut.disconnect_handles()
        del self.dut


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDUTNew))

    test_suite.addTest(unittest.makeSuite(TestDUTInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
