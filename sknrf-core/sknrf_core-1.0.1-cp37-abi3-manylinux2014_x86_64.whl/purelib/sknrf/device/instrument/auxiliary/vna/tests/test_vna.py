import os
import sys
import importlib
import unittest

import yaml
from sknrf.enums.device import Response, response_shape_map
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.instrument.auxiliary.vna.base import NoVNA
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestVNANew(unittest.TestCase):
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
        cls.vna = None
        cls.shape = response_shape_map[Response.SP]

    def setUp(self):
        self.vna = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.vna, NoVNA):
            self.skipTest("%s: is not instance of NoPM" % (self.vna.__class__.__name__,))
        AbstractDevice.__init__(self.vna, *self.args, **self.kwargs)
        self.vna.connect_handles()
        self.vna.__info__()
        self.vna.preset()

    def tearDown(self):
        self.vna.disconnect_handles()
        del self.vna


class TestVNAInit(unittest.TestCase):
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
        cls.vna = None
        cls.shape = response_shape_map[Response.SP]

    def setUp(self):
        self.vna = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.vna, NoVNA):
            self.skipTest("%s: is not instance of NoPM" % (self.vna.__class__.__name__,))

    def tearDown(self):
        self.vna.disconnect_handles()
        del self.vna


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestVNANew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestVNAInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
