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


class TestFTTransforms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        cycles, points = 2, 25
        self.signal_ft = th.ones((Settings().t_points, Settings().f_points*points*cycles), dtype=si_dtype_map[SI.A])
        self.zeros_ft = th.full((Settings().t_points, Settings().f_points*points*cycles), 0.0, dtype=si_dtype_map[SI.A])

    def test_plot(self):
        pass

    def test_tf(self):
        signal_tf = ft.tf(self.signal_ft)
        assert_allclose(signal_tf.shape, (Settings().t_points, Settings().f_points))

    def test_ft_o_tf(self):
        signal_ft = tf.ft(ft.tf(self.signal_ft))
        assert_allclose(signal_ft, self.signal_ft)

    def test_ft_o_tf_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_ft = tf.ft(ft.tf(self.zeros_ft))
        assert_allclose(zeros_ft, self.zeros_ft, atol=si_eps_map[SI.A])

    def test_ff(self):
        signal_ff = ft.ff(self.signal_ft)
        assert_allclose(signal_ff.shape, (Settings().t_points, Settings().f_points))

    def test_ft_o_ff(self):
        signal_ff = ff.ft(ft.ff(self.signal_ft))
        assert_allclose(signal_ff, self.signal_ft)

    def test_ft_o_ff_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_ft = ff.ft(ft.ff(self.zeros_ft))
        assert_allclose(zeros_ft, self.zeros_ft, atol=si_eps_map[SI.A])

    def test_tt(self):
        signal_tt = ft.tt(self.signal_ft)
        assert_allclose(signal_tt.shape, (Settings().t_points, signal_tt.shape[-1]))

    def test_ft_o_tt(self):
        signal_ft = tt.ft(ft.tt(self.signal_ft))
        assert_allclose(signal_ft, self.signal_ft)

    def test_ft_o_tt_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_ft = tt.ft(ft.tt(self.zeros_ft))
        assert_allclose(zeros_ft, self.zeros_ft, atol=si_eps_map[SI.A])

    def test_ft(self):
        signal_ft = ft.ft(self.signal_ft)
        self.assertIs(signal_ft, self.signal_ft)

    def tearDown(self):
        pass
