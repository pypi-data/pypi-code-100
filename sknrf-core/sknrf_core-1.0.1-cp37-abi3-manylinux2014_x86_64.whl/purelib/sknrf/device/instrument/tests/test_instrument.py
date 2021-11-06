__author__ = 'dtbespal'
import abc
import unittest
from test.support import *


Device_Module = "sknrf.device.instrument.rfsource"
Device_Driver = "NoRFSource"
Address_Struct = {}
Port = 1


class TestAbstractInstrumentDefaultState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.device_module = import_module(Device_Module)
        cls.device_cls = cls.device_module.NoRFSource
        cls.device = cls.device_cls()
        # cls.device.preset()
        cls.device.corrected = False

    def test_port_number(self):
        self.assertIsInstance(self.device.port, int)
        self.assertTrue(self.device.port > 0)
