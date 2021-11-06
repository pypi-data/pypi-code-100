import unittest

import numpy as np
import torch as th
from numpy.testing import *

from sknrf.enums.runtime import Bound, SI, si_dtype_map, si_eps_map
from sknrf.settings import Settings
from sknrf.utilities.rf import viz2baz, baz2viz, g2z, z2g, g2vswr, vswr2g, a2v, v2a
from sknrf.utilities.rf import t2a, a2t, z2zp, zp2z, t2tp, tp2t, s2y, y2s, a2s, s2a, s2sp, sp2s, gin2gl, gl2gin
from sknrf.utilities.rf import s4t, t4s, t4tp, tp4t, t4a, a4t, det_minor


class TestRFSignalConversions(unittest.TestCase):

    def setUp(self):
        pass

    def test_viz2baz_o_baz2viz(self):
        b = th.rand((5, 1), dtype=si_dtype_map[SI.B])
        a = th.rand((5, 1), dtype=si_dtype_map[SI.A])
        z = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        b_new, a_new, z_new = viz2baz(*baz2viz(b, a, z))
        assert_allclose(b_new, b)
        assert_allclose(a_new, a)
        assert_allclose(z_new, z)

    def test_viz2baz_o_baz2viz_bound_off(self):
        Settings().bound = Bound.OFF
        b = th.full((5, 1), si_eps_map[SI.B], dtype=si_dtype_map[SI.B])
        a = th.full((5, 1), si_eps_map[SI.A], dtype=si_dtype_map[SI.A])
        z = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        z[0, :] = Settings().z0
        b_new, a_new, z_new = viz2baz(*baz2viz(b, a, z))
        assert_allclose(b_new, b, atol=si_eps_map[SI.B])
        assert_allclose(a_new, a, atol=si_eps_map[SI.A])
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_viz2baz_o_baz2viz_bound_in_ba(self):
        Settings().bound = Bound.IN
        b = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.B])
        a = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.A])
        z = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        b_new, a_new, z_new = viz2baz(*baz2viz(b, a, z))
        assert_allclose(b_new, b, atol=si_eps_map[SI.B])
        assert_allclose(a_new, a, atol=si_eps_map[SI.A])
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_viz2baz_o_baz2viz_bound_in_z(self):
        Settings().bound = Bound.IN
        b = th.full((5, 1), si_eps_map[SI.B], dtype=si_dtype_map[SI.B])
        a = th.full((5, 1), si_eps_map[SI.A], dtype=si_dtype_map[SI.A])
        z = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.Z])
        b_new, a_new, z_new = viz2baz(*baz2viz(b, a, z))
        assert_allclose(b_new, b, atol=si_eps_map[SI.B])
        assert_allclose(a_new, a, atol=si_eps_map[SI.A])
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_baz2viz_o_viz2baz(self):
        v = th.rand((5, 1), dtype=si_dtype_map[SI.V])
        i = th.rand((5, 1), dtype=si_dtype_map[SI.I])
        z = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        v_new, i_new, z_new = baz2viz(*viz2baz(v, i, z))
        assert_allclose(v_new, v)
        assert_allclose(i_new, i)
        assert_allclose(z_new, z)

    def test_baz2viz_o_viz2baz_bound_off(self):
        Settings().bound = Bound.OFF
        v = th.full((5, 1), si_eps_map[SI.V], dtype=si_dtype_map[SI.V])
        i = th.full((5, 1), si_eps_map[SI.I], dtype=si_dtype_map[SI.I])
        z = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        v_new, i_new, z_new = baz2viz(*viz2baz(v, i, z))
        assert_allclose(v_new, v, atol=si_eps_map[SI.V])
        assert_allclose(i_new, i, atol=si_eps_map[SI.I])
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_baz2viz_o_viz2baz_bound_in_vi(self):
        Settings().bound = Bound.IN
        v = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.V])
        i = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.I])
        z = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        v_new, i_new, z_new = baz2viz(*viz2baz(v, i, z))
        assert_allclose(v_new, v, atol=si_eps_map[SI.V])
        assert_allclose(i_new, i, atol=si_eps_map[SI.I])
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_baz2viz_o_viz2baz_bound_in_z(self):
        Settings().bound = Bound.IN
        v = th.full((5, 1), si_eps_map[SI.V], dtype=si_dtype_map[SI.V])
        i = th.full((5, 1), si_eps_map[SI.I], dtype=si_dtype_map[SI.I])
        z = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.Z])
        v_new, i_new, z_new = baz2viz(*viz2baz(v, i, z))
        assert_allclose(v_new, v, atol=si_eps_map[SI.V])
        assert_allclose(i_new, i, atol=si_eps_map[SI.I])
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_viz2baz_vs_v2a(self):
        v = th.rand((5, 1), dtype=si_dtype_map[SI.V])
        z = th.rand((5, 1), dtype=th.float64)
        i = v/z
        b, a, z_new = viz2baz(v, i, z)
        a2, z2 = v2a(v, z)
        assert_allclose(a2, a)
        assert_allclose(z2, z)

    def test_v2a_o_a2v(self):
        a = th.rand((5, 1), dtype=si_dtype_map[SI.V])
        z0 = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        a_new, _ = v2a(*a2v(a, z0=z0))
        assert_allclose(a_new, a)

    def test_v2a_o_a2v_bound_off(self):
        Settings().bound = Bound.OFF
        a = th.full((5, 1), si_eps_map[SI.A], dtype=si_dtype_map[SI.A])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        a_new, _ = v2a(*a2v(a, z0=z0))
        assert_allclose(a_new, a, atol=si_eps_map[SI.A])

    def test_v2a_o_a2v_bound_in_a(self):
        Settings().bound = Bound.IN
        a = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.A])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        a_new, _ = v2a(*a2v(a, z0=z0))
        assert_allclose(a_new, a, atol=si_eps_map[SI.A])

    def test_v2a_o_a2v_bound_in_z0(self):
        Settings().bound = Bound.IN
        a = th.full((5, 1), si_eps_map[SI.A], dtype=si_dtype_map[SI.A])
        z0 = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.Z])
        a_new, z_new = v2a(*a2v(a, z0=z0))
        assert_allclose(a_new, a, atol=si_eps_map[SI.A])
        assert_allclose(z_new, z0, atol=si_eps_map[SI.Z])

    def test_a2v_o_v2a(self):
        v = th.rand((5, 1), dtype=si_dtype_map[SI.V])
        z0 = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        v_new, _ = a2v(*v2a(v, z0=z0))
        assert_allclose(v_new, v)

    def test_a2v_o_v2a_bound_off(self):
        Settings().bound = Bound.OFF
        v = th.full((5, 1), si_eps_map[SI.V], dtype=si_dtype_map[SI.V])
        z0 = th.full((5, 1), si_eps_map[SI.Z], dtype=si_dtype_map[SI.Z])
        v_new, _ = a2v(*v2a(v, z0=z0))
        assert_allclose(v_new, v, atol=si_eps_map[SI.V])

    def test_a2v_o_v2a_bound_in_v(self):
        Settings().bound = Bound.IN
        v = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.V])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        v_new, _ = a2v(*v2a(v, z0=z0))
        assert_allclose(v_new, v, atol=si_eps_map[SI.V])

    def test_a2v_o_v2a_bound_in_z0(self):
        Settings().bound = Bound.IN
        v = th.full((5, 1), si_eps_map[SI.V], dtype=si_dtype_map[SI.V])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        v_new, z_new = a2v(*v2a(v, z0=z0))
        assert_allclose(v_new, v, atol=si_eps_map[SI.V])
        assert_allclose(z_new, z0, atol=si_eps_map[SI.Z])

    def test_baz2viz_vs_a2v(self):
        b = th.zeros((5, 1), dtype=si_dtype_map[SI.B])
        a = th.rand((5, 1), dtype=si_dtype_map[SI.A])
        z = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        v, i, z = baz2viz(b, a, z)
        v2, z2 = a2v(a, z)
        assert_allclose(v2, v)
        assert_allclose(z2, z)

    def test_z2g_o_g2z(self):
        g = th.rand((5, 1), dtype=si_dtype_map[SI.G])
        z0 = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        g_new, _ = z2g(*g2z(g, z0=z0))
        assert_allclose(g_new, g)

    def test_z2g_o_g2z_bound_off(self):
        Settings().bound = Bound.OFF
        g = th.full((5, 1), si_eps_map[SI.G], dtype=si_dtype_map[SI.G])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        g_new, _ = z2g(*g2z(g, z0=z0))
        assert_allclose(g_new, g, atol=si_eps_map[SI.G])

    def test_z2g_o_g2z_bound_in_g(self):
        Settings().bound = Bound.IN
        g = th.full((5, 1), 1.0, dtype=si_dtype_map[SI.G])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        g_new, _ = z2g(*g2z(g, z0=z0))
        assert_allclose(g_new, g, atol=si_eps_map[SI.G])

    def test_z2g_o_g2z_bound_in_z0(self):
        Settings().bound = Bound.IN
        g = th.full((5, 1), si_eps_map[SI.G], dtype=si_dtype_map[SI.G])
        z0 = th.full((5, 1), 0.0, dtype=si_dtype_map[SI.Z])
        g_new, _ = z2g(*g2z(g, z0=z0))
        assert_allclose(g_new, g, atol=si_eps_map[SI.G])

    def test_g2z_o_z2g(self):
        z = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        z0 = th.rand((5, 1), dtype=si_dtype_map[SI.Z])
        z_new, _ = g2z(*z2g(z, z0=z0))
        assert_allclose(z_new, z)

    def test_g2z_o_z2g_bound_off(self):
        Settings().bound = Bound.OFF
        z = th.full((5, 1), si_eps_map[SI.Z], dtype=si_dtype_map[SI.Z])
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        z_new, _ = g2z(*z2g(z, z0=z0))
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_g2z_o_z2g_bound_in_z(self):
        Settings().bound = Bound.IN
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        z = -z0
        z_new, _ = g2z(*z2g(z, z0=z0))
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

        Settings().bound = Bound.IN
        z0 = th.full((5, 1), Settings().z0, dtype=si_dtype_map[SI.Z])
        z = z0
        z_new, _ = g2z(*z2g(z, z0=z0))
        assert_allclose(z_new, z, atol=si_eps_map[SI.Z])

    def test_vswr2g_o_g2vswr_bound_in_g(self):
        Settings().bound = Bound.IN
        g = th.full((5, 1), 1.0, dtype=si_dtype_map[SI.G])
        g_new = vswr2g(g2vswr(g))
        assert_allclose(g_new, g, atol=si_eps_map[SI.G])

    def test_g2vswr_o_vswr2g(self):
        vswr = 1 + th.rand((5, 1), dtype=th.float64)
        vswr_new = g2vswr(vswr2g(vswr))
        assert_allclose(vswr_new, vswr)

    def test_g2vswr_o_vswr2g_bound_in_vswr(self):
        Settings().bound = Bound.IN
        vswr = th.full((5, 1), -1.0, dtype=si_dtype_map[SI.G])
        vswr_new = g2vswr(vswr2g(vswr))
        assert_allclose(vswr_new, vswr, atol=si_eps_map[SI.G])

        Settings().bound = Bound.IN
        vswr = th.full((5, 1), 1.0, dtype=si_dtype_map[SI.G])
        vswr_new = g2vswr(vswr2g(vswr))
        assert_allclose(vswr_new, vswr, atol=si_eps_map[SI.G])

    def tearDown(self):
        pass


class Test2PortConversions(unittest.TestCase):
    def setUp(self):
        pass

    def test_s2y_o_y2s(self):
        z0 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        y = th.rand((5, 2, 2), dtype=si_dtype_map[SI.Z])
        y_new = s2y(*y2s(y, z0))[0]
        assert_allclose(y_new, y)

    def test_y2s_o_s2y(self):
        z0 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        s = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        s_new = y2s(*s2y(s, z0))[0]
        assert_allclose(s_new, s)

    def test_s2a_o_a2s(self):
        a = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        a_new = s2a(a2s(a))
        assert_allclose(a_new, a)

    def test_a2s_o_s2a(self):
        s = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        s_new = a2s(s2a(s))
        assert_allclose(s_new, s)

    def test_s2sp_o_sp2s(self):
        z1 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z2 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        sp = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        sp_new = s2sp(*sp2s(sp, z1, z2))[0]
        assert_allclose(sp_new, sp)

    def test_sp2s_o_s2sp(self):
        z1 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z2 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        s = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        s_new = sp2s(*s2sp(s, z1, z2))[0]
        assert_allclose(s_new, s)

    def test_a2t(self):
        a = th.eye(2, dtype=si_dtype_map[SI.V]).reshape(1, 2, 2)
        t = a2t(a)[0]
        t_ref = th.eye(2, dtype=si_dtype_map[SI.V]).reshape(1, 2, 2)
        assert_allclose(t, t_ref)

    def test_t2a(self):
        t = th.eye(2, dtype=si_dtype_map[SI.B]).reshape(1, 2, 2)
        a = t2a(t)[0]
        a_ref = th.eye(2, dtype=si_dtype_map[SI.B]).reshape(1, 2, 2)
        assert_allclose(a, a_ref)

    def test_a2t_o_t2a(self):
        t = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        t_new = a2t(*t2a(t))[0]
        assert_allclose(t_new, t)

    def test_t2a_o_a2t(self):
        a = th.rand((5, 2, 2), dtype=si_dtype_map[SI.V])
        a_new = t2a(*a2t(a))[0]
        assert_allclose(a_new, a)

    def test_det_minor(self):
        s = th.rand((5, 4, 4), dtype=si_dtype_map[SI.B])
        det_ref = s[:, 0, 0]*s[:, 2, 1]*s[:, 3, 2] - s[:, 0, 0]*s[:, 2, 2]*s[:, 3, 1] - \
                  s[:, 0, 1]*s[:, 2, 0]*s[:, 3, 2] + s[:, 0, 1]*s[:, 2, 2]*s[:, 3, 0] + \
                  s[:, 0, 2]*s[:, 2, 0]*s[:, 3, 1] - s[:, 0, 2]*s[:, 2, 1]*s[:, 3, 0]
        det = det_minor(s, 1, 3)
        assert_allclose(det, det_ref)

    def test_tp2t_o_t2tp(self):
        z1 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z2 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        t = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        t_new = tp2t(*t2tp(t, z1, z2))[0]
        assert_allclose(t_new, t)

    def test_t2tp_o_tp2t(self):
        z1 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z2 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        tp = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        tp_new = t2tp(*tp2t(tp, z1, z2))[0]
        assert_allclose(tp_new, tp)

    def test_zp2z_o_z2zp(self):
        z = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        a = th.rand((5, 2, 2), dtype=si_dtype_map[SI.V])
        z_new = zp2z(z2zp(z, a), a)
        assert_allclose(z_new, z)

    def test_z2zp_o_zp2z(self):
        zp = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        a = th.rand((5, 2, 2), dtype=si_dtype_map[SI.V])
        zp_new = zp2z(z2zp(zp, a), a)
        assert_allclose(zp_new, zp)

    def test_gin2gl_o_gl2gin(self):
        gl = th.rand((5, 1, 1), dtype=si_dtype_map[SI.G])
        s = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        gl_new = gin2gl(*gl2gin(gl, s))[0]
        assert_allclose(gl_new, gl)

    def test_gl2gin_o_gin2gl(self):
        gin = th.rand((5, 1, 1), dtype=si_dtype_map[SI.G])
        s = th.rand((5, 2, 2), dtype=si_dtype_map[SI.B])
        g_in_new = gl2gin(*gin2gl(gin, s))[0]
        assert_allclose(g_in_new, gin)

    def tearDown(self):
        pass


class Test4PortConversions(unittest.TestCase):

    def setUp(self):
        pass

    def test_s4t(self):
        s = th.as_tensor([[
            [0., 0., 1., 0.],
            [0., 0., 0., 1.],
            [1., 0., 0., 0.],
            [0., 1., 0., 0.]
        ]])
        t = s4t(s)
        t_ref = th.eye(4).reshape(1, 4, 4)
        assert_allclose(t, t_ref)

    def test_t4s(self):
        t = th.eye(4, dtype=si_dtype_map[SI.B]).reshape(1, 4, 4)
        s = t4s(t)
        s_ref = th.as_tensor([[
            [0., 0., 1., 0.],
            [0., 0., 0., 1.],
            [1., 0., 0., 0.],
            [0., 1., 0., 0.]
        ]])
        assert_allclose(s, s_ref)

    def test_s4t_t4s(self):
        s = th.rand((5, 4, 4), dtype=si_dtype_map[SI.B])
        s_new = t4s(s4t(s))
        assert_allclose(s_new, s)

    def test_t4s_s4t(self):
        t = th.rand((5, 4, 4), dtype=si_dtype_map[SI.B])
        t_new = s4t(t4s(t))
        assert_allclose(t_new, t)

    def test_a4t(self):
        a = th.eye(4, dtype=si_dtype_map[SI.B]).reshape(1, 4, 4)
        t = a4t(a)[0]
        t_ref = th.eye(4, dtype=si_dtype_map[SI.B]).reshape(1, 4, 4)
        assert_allclose(t, t_ref)

    def test_t4a(self):
        t = th.eye(4, dtype=si_dtype_map[SI.B]).reshape(1, 4, 4)
        a = t4a(t)[0]
        a_ref = th.eye(4, dtype=si_dtype_map[SI.B]).reshape(1, 4, 4)
        assert_allclose(a, a_ref)

    def test_a4t_o_t4a(self):
        t = th.rand((5, 4, 4), dtype=si_dtype_map[SI.B])
        t_new = a4t(*t4a(t))[0]
        assert_allclose(t_new, t)

    def test_t4a_o_a4t(self):
        a = th.rand((5, 4, 4), dtype=si_dtype_map[SI.V])
        a_new = t4a(*a4t(a))[0]
        assert_allclose(a_new, a)

    def test_tp4t_o_t4tp(self):
        z1 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z2 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z3 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z4 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        t = th.rand((5, 4, 4), dtype=si_dtype_map[SI.B])
        t_new = tp4t(*t4tp(t, z1, z2, z3, z4))[0]
        assert_allclose(t_new, t)

    def test_t4tp_o_tp4t(self):
        z1 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z2 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z3 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        z4 = th.rand((5, 1, 1), dtype=si_dtype_map[SI.Z])
        tp = th.rand((5, 4, 4), dtype=si_dtype_map[SI.B])
        tp_new = t4tp(*tp4t(tp, z1, z2, z3, z4))[0]
        assert_allclose(tp_new, tp)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
