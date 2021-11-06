import sys
import importlib
import inspect
import unittest


from sknrf.device import AbstractDevice
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.tests.test_device import LogTestResult
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit
from sknrf.device.dut.mipi.client.tests.test_client import TestMIPIClientNew
from sknrf.device.dut.mipi.client.tests.test_client import TestMIPIClientInit
from sknrf.device.dut.mipi.client.tests.test_client import TestMIPIClientReadWriteSpecific, TestMIPIClientReadWriteGeneric

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestRFFENew(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pythoncom.CoInitialize()
        from sknrf.device.tests.test_device import device_module, device_driver
        cls.device_module = importlib.import_module(device_module)
        cls.device_cls = getattr(cls.device_module, device_driver)
        cls.mipi = None

    def setUp(self):
        from sknrf.device.tests.test_device import positional_args, keyword_args
        self.mipi = self.device_cls.__new__(self.device_cls, *positional_args, **keyword_args)
        AbstractDevice.__init__(self.mipi, *positional_args, **keyword_args)
        self.mipi.connect_handles()
        self.mipi.__info__()
        self.mipi.preset()
        self.mipi.on = True

    def tearDown(self):
        self.mipi.disconnect_handles()
        del self.mipi


class TestRFFEInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pythoncom.CoInitialize()
        from sknrf.device.tests.test_device import device_module, device_driver
        cls.device_module = importlib.import_module(device_module)
        cls.device_cls = getattr(cls.device_module, device_driver)
        cls.mipi = None

    def setUp(self):
        from sknrf.device.tests.test_device import positional_args, keyword_args
        self.mipi = self.device_cls(*positional_args, **keyword_args)
        self.mipi.on = True

    def tearDown(self):
        self.mipi.disconnect_handles()
        del self.mipi


def driver_test_suite():
    from sknrf.device.tests.test_device import device_module, device_driver
    test_suite = unittest.TestSuite()

    device_module_ = importlib.import_module(device_module)
    device_class = getattr(device_module_, device_driver)
    base_classes = inspect.getmro(device_class)

    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    if NoMIPIClient in base_classes:
        test_suite.addTest(unittest.makeSuite(TestMIPIClientNew))
    if NoRFFE in base_classes:
        test_suite.addTest(unittest.makeSuite(TestRFFENew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    if NoRFFE in base_classes:
        test_suite.addTest(unittest.makeSuite(TestMIPIClientInit))
        test_suite.addTest(unittest.makeSuite(TestMIPIClientReadWriteSpecific))
        test_suite.addTest(unittest.makeSuite(TestMIPIClientReadWriteGeneric))
    if NoRFFE in base_classes:
        test_suite.addTest(unittest.makeSuite(TestRFFEInit))
    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.resultclass = LogTestResult
    runner.run(driver_test_suite())