import unittest
import os
import logging
import pickle

import torch as th

from sknrf.settings import Settings
from sknrf.model.sequencer.sweep.frequency import FundLOSpanSweep, FundSSBSpanSweep, FundDSBSpanSweep, FundPhasorSpanSweep

root = os.sep.join((Settings().root, "model", "sequencer", "sweep", "complex"))
logger = logging.getLogger(__name__)


class TestFrequencySweep(unittest.TestCase):
    sweep_cls = FundLOSpanSweep
    sweep_kwargs = {"center": Settings().f0, "span": 1/Settings().t_step, "points": 3}

    @classmethod
    def setUpClass(cls):
        cls.filename = os.sep.join([Settings().data_root, "testdata", "saved_state.p"])
        cls.sweep = None

    def setUp(self):
        self.sweep = self.sweep_cls(**self.sweep_kwargs)

    def test_01_save(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        pickle.dump(self.sweep, open(self.filename, "wb"))
        self.assertTrue(os.path.exists(self.filename))

    def test_02_save_load(self):
        self.test_01_save()
        del self.sweep

        self.sweep = pickle.load(open(self.filename, "rb"))
        self.assertIsInstance(self.sweep, self.sweep_cls)

    def test_03_save_load_same_values(self):
        self.test_01_save()
        kwargs = {}
        for k, v in self.sweep_kwargs.items():
            kwargs[k] = getattr(self.sweep, k)
        del self.sweep

        self.sweep = pickle.load(open(self.filename, "rb"))
        for k, v in self.sweep_kwargs.items():
            self.assertTrue(kwargs[k] == getattr(self.sweep, k))

    def test_04_values(self):
        self.assertIsInstance(self.sweep.values(), th.Tensor)

    def tearDown(self):
        del self.sweep


class TestFundLOSpanSweep(TestFrequencySweep, unittest.TestCase):
    sweep_cls = FundLOSpanSweep
    sweep_kwargs = {"center": 0.0, "span": 1/Settings().t_step, "points": 3}


class TestFundSSBSpanSweep(TestFrequencySweep, unittest.TestCase):
    sweep_cls = FundSSBSpanSweep
    sweep_kwargs = {"center": 0.0, "span": 1/Settings().t_step, "points": 3}


class TestFundDSBSpanSweep(TestFrequencySweep, unittest.TestCase):
    sweep_cls = FundDSBSpanSweep
    sweep_kwargs = {"center": 0.0, "span": 1/Settings().t_step, "points": 3}


class TestFundPhasorSpanSweep(TestFrequencySweep, unittest.TestCase):
    sweep_cls = FundPhasorSpanSweep
    sweep_kwargs = {"center": 0.0, "span": 1/Settings().t_step, "points": 3}


def sweep_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestFundLOSpanSweep))
    test_suite.addTest(unittest.makeSuite(TestFundSSBSpanSweep))
    test_suite.addTest(unittest.makeSuite(TestFundDSBSpanSweep))
    test_suite.addTest(unittest.makeSuite(TestFundPhasorSpanSweep))
    return test_suite


if __name__ == '__main__':
    import sys

    from PySide2 import QtCore

    from sknrf.model.base import AbstractModel

    app = QtCore.QCoreApplication(sys.argv)
    AbstractModel.init()

    runner = unittest.TextTestRunner()
    runner.run(sweep_test_suite())
