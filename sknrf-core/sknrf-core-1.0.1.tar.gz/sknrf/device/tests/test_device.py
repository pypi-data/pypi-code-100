import sys
import os
import unittest
import importlib
import pickle
import logging
import traceback
import re

import yaml
import torch as th

from sknrf.device.base import AbstractDevice
from sknrf.settings import Settings
from sknrf.model.base import AbstractModel
from sknrf.utilities.numeric import AttributeInfo

if sys.platform == "win32": import pythoncom

__author__ = 'dtbespal'

logger = logging.getLogger(__name__)


class TestDeviceNew(unittest.TestCase):
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
        cls.device = None

    def setUp(self):
        self.device = self.class_.__new__(self.class_, *self.args, **self.kwargs)
        AbstractDevice.__init__(self.device, *self.args, **self.kwargs)
        self.initialized = False

    def test_01_buffer_zero_pre_check(self):
        error_model = self.device._error_model
        for k, v in error_model._buffers.items():
            self.assertFalse(th.any(th.isnan(v)), "buffer: %s, contains zero during pre_check" % (k,))

    def test_02_parameter_zero_pre_check(self):
        error_model = self.device._error_model
        for k, v in error_model._parameters.items():
            self.assertFalse(th.any(th.isnan(v)), "parameter: %s, contains zero during pre_check" % (k,))

    def test_03_buffer_nan_pre_check(self):
        error_model = self.device._error_model
        for k, v in error_model._buffers.items():
            self.assertFalse(th.any(th.isnan(v)), "buffer: %s, contains nan during pre_check" % (k,))

    def test_04_parameter_nan_pre_check(self):
        error_model = self.device._error_model
        for k, v in error_model._parameters.items():
            self.assertFalse(th.any(th.isnan(v)), "parameter: %s, contains nan during pre_check" % (k,))

    def test_05_connect_handles(self):
        self.device.connect_handles()
        for k, v in self.device.handles.items():
            self.assertTrue(self.device.unique_handle(v),
                "Connection to %s is not unique, cannot preset. This test is not independent of other connected devices." % (k,))

    def test_06_preset(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()

    def test_07_get_freq(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        self.assertTrue(set(self.device.freq.tolist()) <= set(Settings().freq.tolist()))

    def test_08_get_time(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        self.assertIs(self.device.time, Settings().time)

    def test_09_float_finite_tol(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        public_properties = {k: v for (k, v) in self.device.info.items() if k[0] != "_"}
        for k, info in public_properties.items():
            abs_tol = th.as_tensor(self.device.info[k].abs_tol)
            self.assertTrue(th.isfinite(abs_tol), "Finite absolute tolerance not defined for property: %s" % str(k))
            rel_tol = th.as_tensor(self.device.info[k].rel_tol)
            self.assertTrue(th.isfinite(rel_tol), "Finite relative tolerance not defined for property: %s" % str(k))

    def test_10_get_on(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        _ = self.device.on
        self.assertTrue(True)

    def test_11_set_on(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        self.device.on = True
        self.device.on = False
        self.assertTrue(True)

    def test_12_set_get_on(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        self.device.on = True
        self.assertTrue(self.device.on)
        self.device.on = False
        self.assertFalse(self.device.on)

    def test_13_initialized_false(self):
        self.device.connect_handles()
        self.device.__info__()
        self.device.preset()
        self.assertFalse(self.device.initialized)

    def tearDown(self):
        self.device.disconnect_handles()
        del self.device


class TestDeviceInit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        AbstractModel.init()
        if sys.platform == "win32": pythoncom.CoInitialize()
        cls.filename = os.sep.join([Settings().data_root, "testdata", "saved_state.p"])
        with open(os.sep.join((Settings().data_root, "testdata", "test_device.yml")), 'r') as f:
            config = yaml.load(f, yaml.Loader)
            cls.module = importlib.import_module(config["module"])
            cls.class_ = getattr(cls.module, config["class"])
            cls.args = [AbstractModel.device_model()] + config["args"]
            cls.kwargs = config["kwargs"]
        cls.device = None

    def setUp(self):
        self.device = self.class_(*self.args, **self.kwargs)

    def test_01_getstate(self):
        state = self.device.__getstate__()
        self.assertIsInstance(state, dict)

    def test_02_setstate(self):
        state = self.device.__getstate__()
        self.device.disconnect_handles()
        self.device.__setstate__(state)
        self.assertTrue(self.device.initialized, True)

    def test_03_save(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        pickle.dump(self.device, open(self.filename, "wb"))
        self.assertTrue(os.path.exists(self.filename))

    def test_04_save_load(self):
        self.test_03_save()
        self.device.disconnect_handles()
        del self.device

        self.device = pickle.load(open(self.filename, "rb"))
        self.assertIsInstance(self.device, self.class_)

    def test_05_properties_not_none(self):
        attribute_dict = self.device.__dict__.copy()
        attribute_dict.update(self.device.__class__.__dict__)
        base_classes = self.device.__class__.__bases__
        attribute_dict = AttributeInfo.search_base_dict(attribute_dict, base_classes)
        public_properties = {k: v for (k, v) in attribute_dict.items() if k[0] != "_" and isinstance(v, property) and v.fget}
        for k, v in public_properties.items():
            self.assertIsNotNone(getattr(self.device, k), "NULL value detected for property: %s" % str(k))

    def test_06_save_load_properties_not_none(self):
        self.test_03_save()
        self.device.disconnect_handles()
        del self.device

        self.device = pickle.load(open(self.filename, "rb"))
        attribute_dict = self.device.__dict__.copy()
        attribute_dict.update(self.device.__class__.__dict__)
        base_classes = self.device.__class__.__bases__
        attribute_dict = AttributeInfo.search_base_dict(attribute_dict, base_classes)
        public_properties = {k: v for (k, v) in attribute_dict.items() if k[0] != "_" and isinstance(v, property) and v.fget}
        for k, v in public_properties.items():
            self.assertIsNotNone(getattr(self.device, k), "NULL value detected for property: %s" % str(k))

    def test_07_buffer_nan_zero_check(self):
        error_model = self.device._error_model
        for k, v in error_model._buffers.items():
            self.assertFalse(th.any(th.isnan(v)), "buffer: %s, contains zero during pre_check" % (k,))

    def test_08_parameter_zero_post_check(self):
        error_model = self.device._error_model
        for k, v in error_model._parameters.items():
            self.assertFalse(th.any(th.isnan(v)), "parameter: %s, contains zero during pre_check" % (k,))

    def test_09_buffer_nan_post_check(self):
        error_model = self.device._error_model
        for k, v in error_model._buffers.items():
            self.assertFalse(th.any(th.isnan(v)), "buffer: %s, contains nan during pre_check" % (k,))

    def test_10_parameter_nan_post_check(self):
        error_model = self.device._error_model
        for k, v in error_model._parameters.items():
            self.assertFalse(th.any(th.isnan(v)), "parameter: %s, contains nan during pre_check" % (k,))

    def tearDown(self):
        self.device.disconnect_handles()
        del self.device


class LogTestResult(unittest.TextTestResult):

    @classmethod
    def format_log(cls, test_name, result, message=""):
        if len(message) == 0:
            return "- %s -- %s" % (test_name, result)
        else:
            return "- %s -- %s\n%s" % (test_name, result, message)

    def addError(self, test, err):
        logger.critical(LogTestResult.format_log(str(test), "ERROR", "".join(traceback.format_exception(*err))))
        super(LogTestResult, self).addError(test, err)

    def addFailure(self, test, err):
        logger.error(LogTestResult.format_log(str(test), "FAIL", "".join(traceback.format_exception(*err))))
        super(LogTestResult, self).addFailure(test, err)

    def addSuccess(self, test):
        logger.info(LogTestResult.format_log(str(test), "PASS"))
        super(LogTestResult, self).addSuccess(test)

    def addSkip(self, test, reason):
        logger.debug(LogTestResult.format_log(str(test), "SKIP", reason))
        super(LogTestResult, self).addSkip(test, reason)

    def addExpectedFailure(self, test, err):
        logger.error(LogTestResult.format_log(str(test), "EXPECTED_FAIL", "".join(traceback.format_exception(*err))))
        super(LogTestResult, self).addExpectedFailure(test, err)

    def addUnexpectedSuccess(self, test):
        logger.error(LogTestResult.format_log(str(test), "EXPECTED_PASS"))
        super(LogTestResult, self).addUnexpectedSuccess(test)
