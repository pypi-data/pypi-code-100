import unittest
import os
import logging
import pickle

import torch as th

from sknrf.settings import Settings
from sknrf.model.sequencer.sweep.complex import RectangularSweep, RectangularRandomSweep, RectangularUniformSweep
from sknrf.model.sequencer.sweep.complex import PolarSweep, PolarRandomSweep, PolarUniformSweep
from sknrf.model.sequencer._shape import SHAPE

root = os.sep.join((Settings().root, "model", "sequencer", "sweep", "complex"))
logger = logging.getLogger(__name__)


class TestComplexSweep(unittest.TestCase):
    sweep_cls = RectangularSweep
    sweep_kwargs = {"real_start": -0.707, "real_stop": 0.707,
                    "imag_start": -0.707, "imag_stop": 0.707,
                    "real_step": 1.414, "real_points": 0, "imag_step": 1.414, "imag_points": 0}

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


class TestRectangularSweepStep(TestComplexSweep, unittest.TestCase):
    sweep_cls = RectangularSweep
    sweep_kwargs = {"real_start": -0.707, "real_stop": 0.707,
                    "imag_start": -0.707, "imag_stop": 0.707,
                    "real_step": 1.414, "imag_step": 1.414}


class TestRectangularSweepPoints(TestComplexSweep, unittest.TestCase):
    sweep_cls = RectangularSweep
    sweep_kwargs = {"real_start": -0.707, "real_stop": 0.707,
                    "imag_start": -0.707, "imag_stop": 0.707,
                    "real_points": 2, "imag_points": 2}


class TestPolarSweepStep(TestComplexSweep, unittest.TestCase):
    sweep_cls = PolarSweep
    sweep_kwargs = {"abs_start": 0.0, "abs_stop": 1.0,
                    "angle_start": -180.0, "angle_stop": 180.0,
                    "abs_step": 1.0, "angle_step": 60.0}


class TestPolarSweepPoints(TestComplexSweep, unittest.TestCase):
    sweep_cls = PolarSweep
    sweep_kwargs = {"abs_start": 0.0, "abs_stop": 1.0,
                    "angle_start": -180.0, "angle_stop": 180.0,
                    "abs_points": 2, "angle_points": 2}


class TestRectangularUniformSweep(TestComplexSweep, unittest.TestCase):
    sweep_cls = RectangularUniformSweep
    sweep_kwargs = {"shape": SHAPE.TRIANGLE, "real_start": -0.5, "real_stop": 0.5,
                    "imag_start": -0.707, "imag_stop": 0.707, "step": 1.414}


class TestRectangularUniformSweepSwapped(TestComplexSweep, unittest.TestCase):
    sweep_cls = RectangularUniformSweep
    sweep_kwargs = {"shape": SHAPE.TRIANGLE, "real_start": -0.707, "real_stop": 0.707,
                    "imag_start": -0.5, "imag_stop": 0.5, "step": 1.414}


class TestRectangularUniformSweepNoVertices(TestComplexSweep, unittest.TestCase):
    sweep_cls = RectangularUniformSweep
    sweep_kwargs = {"shape": SHAPE.TRIANGLE, "real_start": -0.707, "real_stop": 0.707,
                    "imag_start": -0.5, "imag_stop": 0.5, "step": 100.0}


class TestPolarUniformSweep(TestComplexSweep, unittest.TestCase):
    sweep_cls = PolarUniformSweep
    sweep_kwargs = {"shape": SHAPE.TRIANGLE, "abs_start": 0.0, "abs_stop": 1.0, "step": 1.0}


class TestPolarUniformNoVertices(TestComplexSweep, unittest.TestCase):
    sweep_cls = PolarUniformSweep
    sweep_kwargs = {"shape": SHAPE.TRIANGLE, "abs_start": 0.0, "abs_stop": 1.0, "step": 100.0}


class TestRectangularRandomSweep(TestComplexSweep, unittest.TestCase):
    sweep_cls = RectangularRandomSweep
    sweep_kwargs = {"real_start": -0.707, "real_stop": 0.707,
                    "imag_start": -0.707, "imag_stop": 0.707,
                    "points": 2}

    def test_05_set_properties(self):
        self.sweep.real_start = -0.5
        self.sweep.real_stop = 0.5
        self.sweep.imag_start = -0.5
        self.sweep.imag_stop = 0.5
        self.sweep.points = 4


class TestPolarRandomSweep(TestComplexSweep, unittest.TestCase):
    sweep_cls = PolarRandomSweep
    sweep_kwargs = {"abs_start": 0.0, "abs_stop": 1.0, "points": 2}

    def test_05_set_properties(self):
        self.sweep.abs_start = 0.25
        self.sweep.abs_stop = 0.75
        self.sweep.points = 4


def sweep_test_suite():
    test_suite = unittest.TestSuite()

    test_suite.addTest(unittest.makeSuite(TestRectangularSweepStep))
    test_suite.addTest(unittest.makeSuite(TestRectangularSweepPoints))
    test_suite.addTest(unittest.makeSuite(TestRectangularRandomSweep))
    test_suite.addTest(unittest.makeSuite(TestRectangularUniformSweep))
    test_suite.addTest(unittest.makeSuite(TestRectangularUniformSweepSwapped))
    test_suite.addTest(unittest.makeSuite(TestPolarSweepStep))
    test_suite.addTest(unittest.makeSuite(TestPolarSweepPoints))
    test_suite.addTest(unittest.makeSuite(TestPolarRandomSweep))
    test_suite.addTest(unittest.makeSuite(TestPolarUniformSweep))
    return test_suite


if __name__ == '__main__':
    import sys

    from PySide import QtCore

    from sknrf.model.base import AbstractModel

    app = QtCore.QCoreApplication(sys.argv)
    AbstractModel.init()

    runner = unittest.TextTestRunner()
    runner.run(sweep_test_suite())
