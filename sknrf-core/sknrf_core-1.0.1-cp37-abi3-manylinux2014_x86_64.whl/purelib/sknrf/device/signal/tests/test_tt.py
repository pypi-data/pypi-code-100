import unittest
import os
import pickle
import copy

import torch as th
import torch.multiprocessing as mp
from numpy.testing import *

from sknrf.settings import Settings
from sknrf.enums.runtime import Bound, SI, si_dtype_map, si_eps_map
from sknrf.device.signal import tf, ff, ft, tt

root = os.sep.join((Settings().root, "device", "signal", "tests"))
dirname = os.sep.join((Settings().data_root, "testdata"))


class TestTTTransforms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        cycles, points = 2, 25
        self.signal_tt = th.ones((Settings().t_points, Settings().f_points*points*cycles), dtype=si_dtype_map[SI.A])
        self.zeros_tt = th.full((Settings().t_points, Settings().f_points*points*cycles), 0.0, dtype=si_dtype_map[SI.A])

    def test_plot(self):
        pass

    def test_tf(self):
        signal_tf = tt.tf(self.signal_tt)
        assert_allclose(signal_tf.shape, (Settings().t_points, Settings().f_points))

    def test_tt_o_tf(self):
        signal_tt = tf.tt(tt.tf(self.signal_tt))
        assert_allclose(signal_tt, self.signal_tt)

    def test_tt_o_tf_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_tt = tf.tt(tt.tf(self.zeros_tt))
        assert_allclose(zeros_tt, self.zeros_tt, atol=si_eps_map[SI.A])

    def test_ff(self):
        signal_ff = tt.ff(self.signal_tt)
        assert_allclose(signal_ff.shape, (Settings().t_points, Settings().f_points))

    def test_tt_o_ff(self):
        signal_tt = ff.tt(tt.ff(self.signal_tt))
        assert_allclose(signal_tt, self.signal_tt)

    def test_tt_o_ff_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_tt = ff.tt(tt.ff(self.zeros_tt))
        assert_allclose(zeros_tt, self.zeros_tt, atol=si_eps_map[SI.A])

    def test_tt(self):
        signal_tt = tt.tt(self.signal_tt)
        self.assertIs(signal_tt, self.signal_tt)

    def test_ft(self):
        signal_ft = tt.ft(self.signal_tt)
        assert_allclose(signal_ft.shape, (Settings().t_points, signal_ft.shape[-1]))

    def test_tt_o_ft(self):
        signal_tt = ft.tt(tt.ft(self.signal_tt))
        assert_allclose(signal_tt, self.signal_tt)

    def test_tt_o_ft_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_tt = ft.tt(tt.ft(self.zeros_tt))
        assert_allclose(zeros_tt, self.zeros_tt, atol=si_eps_map[SI.A])

    def tearDown(self):
        pass
