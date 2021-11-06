import unittest
import os
import pickle
import copy

import math as mt
import numpy as np
import torch as th
import torch.multiprocessing as mp
from numpy.testing import *

from sknrf.settings import Settings
from sknrf.enums.runtime import Bound, SI, si_dtype_map, si_eps_map
from sknrf.device.signal import tf, ff, ft, tt

root = os.sep.join((Settings().root, "device", "signal", "tests"))
dirname = os.sep.join((Settings().data_root, "testdata"))


class TestTFTransforms(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.signal_tf = th.ones((Settings().t_points, Settings().f_points), dtype=si_dtype_map[SI.A])
        self.zeros_tf = th.full((Settings().t_points, Settings().f_points), 0.0, dtype=si_dtype_map[SI.A])

    def test_plot(self):
        pass

    def test_tf(self):
        signal_tf = tf.tf(self.signal_tf)
        self.assertIs(signal_tf, self.signal_tf)

    def test_ff(self):
        signal_tf = tf.ff(self.signal_tf)
        assert_allclose(signal_tf.shape, (Settings().t_points, Settings().f_points))

    def test_tf_o_ff(self):
        signal_tf = ff.tf(tf.ff(self.signal_tf))
        assert_allclose(signal_tf, self.signal_tf)

    def test_tf_o_ff_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_tf = ff.tf(tf.ff(self.zeros_tf))
        assert_allclose(zeros_tf, self.zeros_tf, atol=si_eps_map[SI.A])

    def test_tt(self):
        signal_tt = tf.tt(self.signal_tf)
        assert_allclose(signal_tt.shape, (Settings().t_points, signal_tt.shape[-1]))

    def test_tf_o_tt(self):
        signal_tf = tt.tf(tf.tt(self.signal_tf))
        assert_allclose(signal_tf, self.signal_tf)

    def test_tf_o_tt_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_tf = tt.tf(tf.tt(self.zeros_tf))
        assert_allclose(zeros_tf, self.zeros_tf, atol=si_eps_map[SI.A])

    def test_ft(self):
        signal_ft = tf.ft(self.signal_tf)
        assert_allclose(signal_ft.shape, (Settings().t_points, signal_ft.shape[-1]))

    def test_tf_o_ft(self):
        signal_tf = ft.tf(tf.ft(self.signal_tf))
        assert_allclose(signal_tf, self.signal_tf)

    def test_tf_o_ft_bound_out(self):
        Settings.bound = Bound.OUT
        zeros_tf = ft.tf(tf.ft(self.zeros_tf))
        assert_allclose(zeros_tf, self.zeros_tf, atol=si_eps_map[SI.A])

    def tearDown(self):
        pass


class TestTFZeros(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        dtype = si_dtype_map[SI.B]
        self.min = th.tensor(th.finfo(dtype).eps, dtype=dtype)
        self.signal_tf = th.full((Settings().t_points, Settings().f_points), self.min, dtype=dtype)

    def test_non_zero(self):
        assert_allclose(tf.pk(self.signal_tf), self.min)
        assert_allclose(tf.avg(self.signal_tf), self.min)
        assert_allclose(tf.iq(self.signal_tf), 1.0)
        assert_allclose(tf.par(self.signal_tf), 1.0)

    def tearDown(self):
        pass


class TestTFModulation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        iq = th.as_tensor([1.0000 + 0.0000j, 0.0000 + 0.0000j, 0.0000 + 1.0000j, 0.7071 + 0.7071j]).reshape(-1, 1)
        num_reps = int(mt.ceil(Settings().t_points / iq.shape[-2]))
        cls.iq = iq.repeat((num_reps, Settings().f_points))[:Settings().t_points, :]

    def setUp(self):
        pass

    def test_cw(self):
        par = 1
        signal_tf = th.full((Settings().t_points, Settings().f_points), 1.24, dtype=si_dtype_map[SI.B])
        assert_allclose(tf.pk(signal_tf), 1.24)
        assert_allclose(tf.avg(signal_tf), tf.pk(signal_tf)/par)
        assert_allclose(tf.par(signal_tf), 1.0)

    def test_pulse_modulated(self):
        start, end = int(mt.floor(Settings().t_points/2)), int(mt.ceil(Settings().t_points/2))
        par = mt.sqrt(Settings().t_points/end)
        f_points = Settings().f_points
        signal_tf = th.cat((th.zeros((start, f_points)), th.full((end, f_points), 1.24)), dim=-2)
        signal_tf = th.as_tensor(signal_tf)
        assert_allclose(tf.pk(signal_tf), 1.24)
        assert_allclose(tf.avg(signal_tf), tf.pk(signal_tf)/par)
        assert_allclose(tf.par(signal_tf), par)

    def test_iq_modulated(self):
        signal_tf = th.as_tensor(1.24*self.iq.real)
        par = th.max(self.iq.real)/th.sqrt(th.mean(self.iq.real*th.conj(self.iq.real)))
        assert_allclose(tf.pk(signal_tf), abs(1.24))
        assert_allclose(tf.avg(signal_tf), tf.pk(signal_tf)/par)
        assert_allclose(tf.par(signal_tf), par)

    def test_iq_modulated_set_pk(self):
        f_points = Settings().f_points
        signal_tf = th.as_tensor(1.24 * self.iq.real)
        old_pk = tf.pk(signal_tf)
        old_par = tf.par(signal_tf)
        tf.set_pk(signal_tf, th.ones((f_points,)))
        self.assertIsInstance(signal_tf, th.Tensor)
        assert_allclose(tf.par(signal_tf), old_par)
        self.assertFalse(th.any(tf.pk(signal_tf) == old_pk))

    def test_iq_modulated_set_avg_rms(self):
        f_points = Settings().f_points
        signal_tf = th.as_tensor(1.24 * self.iq.real)
        old_avg = tf.avg(signal_tf)
        old_par = tf.par(signal_tf)
        tf.set_avg(signal_tf, th.ones((f_points,)))
        self.assertIsInstance(signal_tf, th.Tensor)
        assert_allclose(tf.par(signal_tf), old_par)
        self.assertFalse(th.any(tf.avg(signal_tf) == old_avg))

    def test_iq_modulated_set_avg_mean(self):
        f_points = Settings().f_points
        signal_tf = th.as_tensor(1.24 * self.iq.real)
        old_avg = tf.avg(signal_tf, rms=False)
        old_par = tf.par(signal_tf, rms=False)
        tf.set_avg(signal_tf, th.ones((f_points,)), rms=False)
        self.assertIsInstance(signal_tf, th.Tensor)
        assert_allclose(tf.par(signal_tf, rms=False), old_par)
        self.assertFalse(th.any(tf.avg(signal_tf, rms=False) == old_avg))

    def test_iq_modulated_set_iq(self):
        signal_tf = th.as_tensor(1.24 * self.iq.real)
        old_pk = tf.pk(signal_tf)
        old_par = tf.par(signal_tf)
        tf.set_iq(signal_tf, th.ones_like(signal_tf))
        self.assertIsInstance(signal_tf, th.Tensor)
        assert_allclose(tf.pk(signal_tf), old_pk)
        self.assertFalse(th.any(tf.par(signal_tf) == old_par))

    def tearDown(self):
        pass
