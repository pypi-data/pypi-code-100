import os
import sys
import importlib
import unittest

import yaml
from sknrf.enums.device import Response, response_shape_map
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit, LogTestResult
from sknrf.device.dut.video.base import NoVideo
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestVideoNew(unittest.TestCase):
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
        cls.video = None
        cls.shape = response_shape_map[Response.VIDEO]

    def setUp(self):
        self.video = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.video, NoVideo):
            self.skipTest("%s: is not instance of NoVideo" % (self.video.__class__.__name__,))
        AbstractDevice.__init__(self.video, *self.args, **self.kwargs)
        self.video.connect_handles()
        self.video.__info__()
        self.video.preset()

    def tearDown(self):
        self.video.disconnect_handles()
        del self.video


class TestVideoInit(unittest.TestCase):
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
        cls.video = None
        cls.shape = response_shape_map[Response.VIDEO]

    def setUp(self):
        self.video = self.class_(*self.args, **self.kwargs)
        if not isinstance(self.video, NoVideo):
            self.skipTest("%s: is not instance of NoVideo" % (self.video.__class__.__name__,))

    def tearDown(self):
        self.video.disconnect_handles()
        del self.video


def driver_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestVideoNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestVideoInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())
