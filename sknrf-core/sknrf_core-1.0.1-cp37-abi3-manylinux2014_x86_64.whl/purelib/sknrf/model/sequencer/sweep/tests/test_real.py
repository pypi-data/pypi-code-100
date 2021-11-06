import unittest
import os
import logging
import pickle
import math as mt

import torch as th
from numpy.testing import *

from sknrf.settings import Settings
from sknrf.model.sequencer.sweep.real import LinearSweep, SpanSweep, SubsetSweep, PowSweep, LogSweep
from sknrf.model.sequencer.sweep.real import INDEP_DIM

root = os.sep.join((Settings().root, "model", "sequencer", "sweep"))
logger = logging.getLogger(__name__)


class TestRealSweep(unittest.TestCase):
    sweep_cls = LinearSweep
    sweep_kwargs = {"start": 0.0, "stop": 1.0, "step": 1.0}

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


class TestLinearSweepStep(TestRealSweep, unittest.TestCase):
    sweep_cls = LinearSweep
    sweep_kwargs = {"start": 0.0, "stop": 1.0, "step": 1.0}


class TestLinearSweepPoints(TestRealSweep, unittest.TestCase):
    sweep_cls = LinearSweep
    sweep_kwargs = {"start": 0.0, "stop": 1.0, "points": 2}


class TestSpanSweepStep(TestRealSweep, unittest.TestCase):
    sweep_cls = SpanSweep
    sweep_kwargs = {"center": 0.0, "span": 0.0, "step": 1.0}


class TestSpanSweepPoints(TestRealSweep, unittest.TestCase):
    sweep_cls = SpanSweep
    sweep_kwargs = {"center": 0.0, "span": 0.0, "points": 1}


class TestSubsetSweepStep(TestRealSweep, unittest.TestCase):
    sweep_cls = SubsetSweep
    sweep_kwargs = {"dim": INDEP_DIM.TIME, "step": 1}


class TestSubsetSweepPoints(TestRealSweep, unittest.TestCase):
    sweep_cls = SubsetSweep
    sweep_kwargs = {"dim": INDEP_DIM.TIME, "points": 2}


class TestSubsetSweepFreq(TestRealSweep, unittest.TestCase):
    sweep_cls = SubsetSweep
    sweep_kwargs = {"dim": INDEP_DIM.FREQ, "points": 2}


class TestPowSweep(TestRealSweep, unittest.TestCase):
    sweep_cls = PowSweep
    sweep_kwargs = {"start": mt.sqrt(1.0e-3), "stop": mt.sqrt(1.0e-2), "points": 2, "power": 1}


class TestLogSweep(TestRealSweep, unittest.TestCase):
    sweep_cls = LogSweep
    sweep_kwargs = {"start": mt.sqrt(1.0e-3), "stop": mt.sqrt(1.0e-2), "points": 2}


def sweep_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestLinearSweepStep))
    test_suite.addTest(unittest.makeSuite(TestLinearSweepPoints))
    test_suite.addTest(unittest.makeSuite(TestSpanSweepStep))
    test_suite.addTest(unittest.makeSuite(TestSpanSweepPoints))
    test_suite.addTest(unittest.makeSuite(TestSubsetSweepStep))
    test_suite.addTest(unittest.makeSuite(TestPowSweep))
    test_suite.addTest(unittest.makeSuite(TestLogSweep))
    test_suite.addTest(unittest.makeSuite(TestLogSweep))
    return test_suite


if __name__ == '__main__':
    import sys

    from PySide import QtCore

    from sknrf.model.base import AbstractModel

    app = QtCore.QCoreApplication(sys.argv)
    AbstractModel.init()

    runner = unittest.TextTestRunner()
    runner.run(sweep_test_suite())
