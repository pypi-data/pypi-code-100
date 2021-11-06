import sys
import os
import yaml

import importlib
import unittest

import numpy as np

from sknrf.enums.mipi import MIPI_READ_MODE, MIPI_WRITE_MODE, MIPI_ADDRESS_LIMIT
from sknrf.device.dut.mipi.client.base import NoMIPIClient
from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.device.tests.test_device import TestDeviceNew, TestDeviceInit
from sknrf.model.base import AbstractModel

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'


class TestMIPIClientNew(unittest.TestCase):
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
        cls.client = None

    def setUp(self):
        self.client = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.client, NoMIPIClient):
            self.skipTest("%s: is not instance of NoPM" % (self.client.__class__.__name__,))
        AbstractDevice.__init__(self.client, *self.args, **self.kwargs)
        self.client.connect_handles()
        self.client.__info__()
        self.client.preset()
        self.client.on = True

    def tearDown(self):
        self.client.disconnect_handles()
        del self.client


class TestMIPIClientInit(unittest.TestCase):
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
        cls.client = None

    def setUp(self):
        self.client = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.client, NoMIPIClient):
            self.skipTest("%s: is not instance of NoPM" % (self.client.__class__.__name__,))
        AbstractDevice.__init__(self.client, *self.args, **self.kwargs)
        self.client.connect_handles()
        self.client.__info__()
        self.client.preset()
        self.client.on = True

    def test_01_get_clk_rate(self):
        self.assertIsInstance(self.client._server.clk_rate, float)

    def test_02_set_clk_rate(self):
        self.client._server.clk_rate = self.client._server.clk_rate

    def tearDown(self):
        self.client.disconnect_handles()
        del self.client


class TestMIPIClientReadWriteSpecific(unittest.TestCase):
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
        cls.client = None

    def setUp(self):
        self.client = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.client, NoMIPIClient):
            self.skipTest("%s: is not instance of NoPM" % (self.client.__class__.__name__,))
        AbstractDevice.__init__(self.client, *self.args, **self.kwargs)
        self.client.connect_handles()
        self.client.__info__()
        self.client.preset()
        self.client.on = True

    def test_01_read_basic(self):
        self.client._server.read_mode = MIPI_READ_MODE.BASIC
        self.assertIsInstance(self.client._server.read(self.client.usid, 0x00), np.uint8)

    def test_02_read_extended(self):
        self.client._server.read_mode = MIPI_READ_MODE.EXTENDED
        self.assertIsInstance(self.client._server.read(self.client.usid, 0x00), np.uint32)

    def test_03_read_extended_long(self):
        self.client._server.read_mode = MIPI_READ_MODE.EXTENDED_LONG
        try:
            self.assertIsInstance(self.client._server.read(self.client.usid, 0x0000), np.uint64)
        except NotImplementedError:
            pass

    def test_04_write_reg0(self):
        self.client._server.write_mode = MIPI_WRITE_MODE.REG0
        self.client._server.write(self.client.usid, 0x00, 0x00)

    def test_05_write_basic(self):
        self.client._server.write_mode = MIPI_WRITE_MODE.BASIC
        self.client._server.write(self.client.usid, 0x00, 0x00)

    def test_06_write_extended(self):
        self.client._server.write_mode = MIPI_WRITE_MODE.EXTENDED
        self.client._server.write(self.client.usid, 0x00, 0x00000000)

    def test_07_write_extended_long(self):
        self.client._server.write_mode = MIPI_READ_MODE.EXTENDED_LONG
        try:
            self.client._server.write(self.client.usid, 0x00, 0x0000000000000000)
        except NotImplementedError:
            pass

    def tearDown(self):
        self.client.one = False
        self.client.disconnect_handles()
        del self.client


class TestMIPIClientReadWriteGeneric(unittest.TestCase):
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
        cls.client = None

    def setUp(self):
        self.client = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        if not isinstance(self.client, NoMIPIClient):
            self.skipTest("%s: is not instance of NoPM" % (self.client.__class__.__name__,))
        AbstractDevice.__init__(self.client, *self.args, **self.kwargs)
        self.client.connect_handles()
        self.client.__info__()
        self.client.preset()
        self.client.on = True

    def test_01_read_gneric_basic(self):
        self.client._server.read_mode = MIPI_READ_MODE.GENERIC
        self.assertIsInstance(self.client._server.read(self.client.usid, MIPI_ADDRESS_LIMIT.BASIC), np.uint8)

    def test_02_read_generic_extended(self):
        self.client._server.read_mode = MIPI_READ_MODE.GENERIC
        self.assertIsInstance(self.client._server.read(self.client.usid, MIPI_ADDRESS_LIMIT.EXTENDED), np.uint32)

    def test_03_read_generic_extended_long(self):
        self.client._server.read_mode = MIPI_READ_MODE.GENERIC
        try:
            self.assertIsInstance(self.client._server.read(self.client.usid, MIPI_ADDRESS_LIMIT.EXTENDED_LONG), np.uint64)
        except NotImplementedError:
            pass

    def test_04_write_reg0(self):
        self.client._server.write_mode = MIPI_WRITE_MODE.GENERIC
        self.client._server.write(self.client.usid, 0x00, 0x0)

    def test_05_write_generic_basic(self):
        self.client._server.write_mode = MIPI_WRITE_MODE.GENERIC
        self.client._server.write(self.client.usid, MIPI_ADDRESS_LIMIT.BASIC, 0x00)

    def test_06_write_generic_extended(self):
        self.client._server.write_mode = MIPI_WRITE_MODE.GENERIC
        try:
            self.client._server.write(self.client.usid, MIPI_ADDRESS_LIMIT.EXTENDED, 0x00000000)
        except NotImplementedError:
            pass

    def test_07_write_generic_extended_long(self):
        self.client._server.write_mode = MIPI_READ_MODE.GENERIC
        try:
            self.client._server.write(self.client.usid, MIPI_ADDRESS_LIMIT.EXTENDED_LONG, 0x0000000000000000)
        except NotImplementedError:
            pass

    def tearDown(self):
        self.client.disconnect_handles()
        del self.client


def driver_test_suite():
    test_suite = unittest.TestSuite()

    with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
        config = yaml.load(f, yaml.Loader)
        module = importlib.import_module(config["module"])
        class_ = getattr(module, config["class"])
    test_suite.addTest(unittest.makeSuite(TestDeviceNew))
    test_suite.addTest(unittest.makeSuite(TestMIPIClientNew))

    test_suite.addTest(unittest.makeSuite(TestDeviceInit))
    test_suite.addTest(unittest.makeSuite(TestMIPIClientInit))
    if class_ is not NoMIPIClient:
        test_suite.addTest(unittest.makeSuite(TestMIPIClientReadWriteSpecific))
        test_suite.addTest(unittest.makeSuite(TestMIPIClientReadWriteGeneric))
    return test_suite
