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


class TestFFTransforms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.signal_ff = th.ones((Settings().t_points, Settings().f_points), dtype=si_dtype_map[SI.A])
        self.zeros_ff = th.full((Settings().t_points, Settings().f_points), 0.0, dtype=si_dtype_map[SI.A])

    def test_plot(self):
        pass

    def test_tf(self):
        signal_tf = ff.tf(self.signal_ff)
        assert_allclose(signal_tf.shape, (Settings().t_points, Settings().f_points))

    def test_ff_o_tf(self):
        signal_ff = tf.ff(ff.tf(self.signal_ff))
        assert_allclose(signal_ff, self.signal_ff)

    def test_ff_o_tf_bound_out(self):
        zeros_ff = tf.ff(ff.tf(self.zeros_ff))
        assert_allclose(zeros_ff, self.zeros_ff, atol=si_eps_map[SI.A])

    def test_ff(self):
        signal_ff = ff.ff(self.signal_ff)
        self.assertIs(signal_ff, self.signal_ff)

    def test_tt(self):
        signal_tt = ff.tt(self.signal_ff)
        assert_allclose(signal_tt.shape, (Settings().t_points, signal_tt.shape[-1]))

    def test_ff_o_tt(self):
        signal_ff = tt.ff(ff.tt(self.signal_ff))
        assert_allclose(signal_ff, self.signal_ff)

    def test_ff_o_tt_bound_out(self):
        zeros_ff = tt.ff(ff.tt(self.zeros_ff))
        assert_allclose(zeros_ff, self.zeros_ff, atol=si_eps_map[SI.A])

    def test_ft(self):
        signal_ft = ff.ft(self.signal_ff)
        assert_allclose(signal_ft.shape, (Settings().t_points, signal_ft.shape[-1]))

    def test_ff_o_ft(self):
        signal_ff = ft.ff(ff.ft(self.signal_ff))
        assert_allclose(signal_ff, self.signal_ff)

    def test_ff_o_ft_bound_out(self):
        zeros_ff = ft.ff(ff.ft(self.zeros_ff))
        assert_allclose(zeros_ff, self.zeros_ff, atol=si_eps_map[SI.A])

    def tearDown(self):
        pass
