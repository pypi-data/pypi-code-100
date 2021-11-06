import os
import sys
import importlib
import unittest

import yaml
from sknrf.enums.device import Response, response_shape_map
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.instrument.auxiliary.pm.base import NoPM
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestPMNew(unittest.TestCase):
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
        cls.pm = None
        cls.shape = response_shape_map[Response.P]

    def setUp(self):
        self.pm = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.pm, NoPM):
            self.skipTest("%s: is not instance of NoPM" % (self.pm.__class__.__name__,))
        AbstractDevice.__init__(self.pm, *self.args, **self.kwargs)
        self.pm.connect_handles()
        self.pm.__info__()
        self.pm.preset()

    def tearDown(self):
        self.pm.disconnect_handles()
        del self.pm


class TestPMInit(unittest.TestCase):
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
        cls.pm = None
        cls.shape = response_shape_map[Response.P]

    def setUp(self):
        self.pm = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.pm, NoPM):
            self.skipTest("%s: is not instance of NoPM" % (self.pm.__class__.__name__,))

    def tearDown(self):
        self.pm.disconnect_handles()
        del self.pm


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestPMNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestPMInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
