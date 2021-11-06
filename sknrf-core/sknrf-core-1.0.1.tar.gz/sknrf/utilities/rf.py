"""RF Specific Utility Functions
"""

import cmath as ct
import numpy as np
import torch as th
from skrf import network

from sknrf.enums.runtime import SI, si_eps_map
from sknrf.settings import Settings
from sknrf.enums.runtime import Bound


__author__ = 'dtbespal'


def n2t(n):
    """Converts numpy tensor to pytorch tensor
    """
    return th.as_tensor(n)


def t2n(t):
    """Converts pytorch tensor to numpy tensor
    """
    return t.detach().numpy().astype(np.complex128) if t.is_complex() else t.detach().numpy().astype(np.float64)


def real(re_im):
    """Returns real component of a pytorch tensor
    """
    return re_im.real if re_im.is_complex() else re_im


def imag(re_im):
    """Returns imaginary component of a pytorch tensor
    """
    return re_im.imag if re_im.is_complex() else re_im


def rW2dBW(rW):
    """Converts value in base linear units, such as V, A, rW, to decibels (dB), such as dBV, dBA, dBW.

    Parameters
    ----------
    rW : float
        value in base linear units

    Returns
    -------
    dBW : float
        value in decibels (dB)

    .. math::

       dBW  & = & 20 log10(abs(rW))

    >>> rW2dBW(10)
    10.0
    >>> rW2dBW(0)
    Traceback (most recent call last):
    ...
    ValueError: math domain error
    """
    try:
        result = 20 * th.log10(th.abs(rW))
    except TypeError:
        result = 20 * np.log10(np.abs(rW))
    return result


def rW2dBm(rW):
    """Converts value in base linear units, such as V, A, rW, to milli-decibels (dBm), such as dBmV, dBmA, dBmrW

    Parameters
    ----------
    rW : float
        value in base linear units

    Returns
    -------
    dBm : float
        value in milli-decibels (dBm)

    .. math::

       dBm  & = & rW2dBW(rW) + 30
    """
    return rW2dBW(rW) + 30


def dBW2rW(dBW):
    """Converts value in decibels (dB), such as dBV, dBA, dBW to base linear units, such as V, A, rW.

    Parameters
    ----------
    dBW : float
        value in decibels (dB)

    Returns
    -------
    rW : float
        value in base linear units

    .. math::

       rW  & = & 10^{dBW/20}

    """
    return 10**(dBW/20)


def dBm2rW(dBm):
    """Converts value in milli-decibels (dBm), such as dBmV, dBmA, dBmrW to base linear units, such as V, A, rW

    Parameters
    ----------
    dBW : float
        value in decibels (dB)

    Returns
    -------
    rW : float
        value in base linear units

    .. math::

       rW  & = & dBW2rW(dBm - 30)
    """
    return dBW2rW(dBm-30)


def angle_deg(re_im):
    result = th.angle(re_im)*180/np.pi
    return result


def angle(re_im):
    result = th.angle(re_im)
    return result


def poynting(tf):
    time_axis = -2
    indices = tf.abs().max(time_axis)[1].unsqueeze(time_axis)
    poynting_angle = th.angle(th.gather(tf, time_axis, indices))
    poynting_vec = th.exp(1j * poynting_angle)
    return poynting_vec.flatten()


def a2v(a, z0=50.0):
    """ Gonzalez 1.7.13 using the explanation in 1.7.18

    Parameters
    ----------
    a : Tensor
        Port Incident power-wave.
    z0 : Tensor
        Reference Impedance.

    Returns
    -------
    Tuple
        (v, z0): v+ or the port voltage when conjugate matched, and reference impedance.
    """
    z0 = z0_ = th.as_tensor(z0, dtype=a.dtype)
    if Settings().bound & Bound.IN:
        a_min = th.as_tensor(th.finfo(a.dtype).eps, dtype=a.dtype)
        z0_min = th.as_tensor(th.finfo(z0.dtype).eps, dtype=z0.dtype)
        a = th.where(a.abs() < a_min.abs(), a_min, a)
        a = th.where(z0.abs() < z0_min.abs(), a*th.sqrt(z0_min)/z0_min, a)
        z0_ = th.where(z0.abs() < z0_min.abs(), z0_min, z0)
    return z0_.conj()/th.sqrt(real(z0_))*a, z0


def v2a(v, z0=50.0):
    """ Gonzalez 1.7.13 using the explanation in 1.7.18

    Parameters
    ----------
    v : Tensor
        Port Voltage.
    z0 : Tensor
        Reference Impedance.

    Returns
    -------
    Tuple
        (a, z0): the port incident power-wave, and reference impedance.
    """
    z0 = z0_ = th.as_tensor(z0, dtype=v.dtype)
    if Settings().bound & Bound.IN:
        v_min = th.as_tensor(th.finfo(v.dtype).eps, dtype=v.dtype)
        z0_min = th.as_tensor(th.finfo(z0.dtype).eps, dtype=z0.dtype)
        v = th.where(v.abs() < v_min.abs(), v_min, v)
        v = th.where(z0.abs() < z0_min.abs(), v*z0_min/th.sqrt(z0_min), v)
        z0_ = th.where(z0.abs() < z0_min.abs(), z0_min, z0)
    return th.sqrt(real(z0_))/z0_.conj()*v, z0


def baz2viz(b, a, z0=50.0):
    """ Gonzalez 1.7.9 and 1.7.10

    Parameters
    ----------
    b : Tensor
         Port Reflected power-wave.
    a : Tensor
        Port Incident power-wave.
    z0 : Tensor
        Reference Impedance.

    Returns
    -------
    Tuple
        (v, i, z0): The port voltage, current, and reference impedance.
    """
    z0 = z0_ = th.as_tensor(z0, dtype=b.dtype)
    if Settings().bound & Bound.IN:
        b_min = th.as_tensor(th.finfo(b.dtype).eps, dtype=b.dtype)
        a_min = th.as_tensor(th.finfo(a.dtype).eps, dtype=a.dtype)
        z0_min = th.as_tensor(th.finfo(z0.dtype).eps, dtype=z0.dtype)
        b = th.where(b.abs() < b_min.abs(), b_min, b)
        a = th.where(a.abs() < a_min.abs(), a_min, a)
        z0_ = th.where(z0.abs() < z0_min.abs(), z0_min, z0)
    m = 1 / th.sqrt(real(z0_))
    v, i, z0 = m * (z0_.conj() * a + z0_ * b), m * (a - b), z0
    if Settings().bound & Bound.IN:
        v = th.where(z0.abs() < z0_min.abs(), v*th.sqrt(z0_min)/z0_min, v)
        i = th.where(z0.abs() < z0_min.abs(), i*th.sqrt(z0_min), i)
    return v, i, z0


def viz2baz(v, i, z0=50.0):
    """ Gonzalez 1.7.1 and 1.7.2

    .. math::
       :nowrap:

        \begin{eqnarray}
            B_p & = & \\frac{1}{2 \\sqrt{ \\Re Z_p }} \\left( V - Z_p^*I \\right) \\\\
            A_p & = & \\frac{1}{2 \\sqrt{ \\Re Z_p }} \\left( V + Z_pI \\right) \\\\
            \\Gamma_p & = & \\frac{Z_p - Z_0}{Z_p + Z_0} \\\\
        \end{eqnarray}

    Parameters
    ----------
    v : Tensor
         Port Voltage.
    i : Tensor
        Port Current.
    z0 : Tensor
        Reference Impedance.

    Returns
    -------
    Tuple
        (v, i, z0): The port reflected power-wave, incident power-wave, and reference impedance.
    """
    z0 = z0_ = th.as_tensor(z0, dtype=v.dtype)
    if Settings().bound & Bound.IN:
        v_min = th.as_tensor(th.finfo(v.dtype).eps, dtype=v.dtype)
        i_min = th.as_tensor(th.finfo(i.dtype).eps, dtype=i.dtype)
        z0_min = th.as_tensor(th.finfo(z0.dtype).eps, dtype=z0.dtype)
        v = th.where(v.abs() < v_min.abs(), v_min, v)
        v = th.where(z0.abs() < z0_min.abs(), v*th.sqrt(z0_min), v)
        i = th.where(i.abs() < i_min.abs(), i_min, i)
        i = th.where(z0.abs() < z0_min.abs(), i*th.sqrt(z0_min)/z0_min, i)
        z0_ = th.where(z0.abs() < z0_min.abs(), z0_min, z0)
    m = 1 / (2 * th.sqrt(real(z0_)))
    return m * (v - z0_.conj()*i), m * (v + z0_*i), z0


def g2vswr(g):
    """ Gonzalez 1.3.44


    Parameters
    ----------
    g : Tensor
        Reflection Coefficient.

    Returns
    -------
    Tensor
        The VSWR.
    """
    g_abs = g.abs()
    if Settings().bound & Bound.IN:
        g_abs = th.where(g_abs == 1.0, g_abs - th.finfo(g_abs.dtype).eps, g_abs)
    return (1 + g_abs)/(1 - g_abs)


def vswr2g(vswr):
    """ Gonzalez 1.3.44


    Parameters
    ----------
    vswr : Tensor
        Voltage Standing Wave Ratio (VSWR).

    Returns
    -------
    Tensor
        The Reflection coefficient.
    """
    if Settings().bound & Bound.IN:
        vswr = th.where(vswr == -1.0, vswr + th.finfo(vswr.dtype).eps, vswr)
        vswr = th.where(vswr == 1.0, vswr - th.finfo(vswr.dtype).eps, vswr)
    return (vswr - 1)/(vswr + 1)


def z2g(z, z0=50.0):
    """ Gonzalez 1.3.39

    .. math::
       :nowrap:

        \begin{eqnarray}
            \\Gamma_p & = & \\frac{Z_p - Z_0}{Z_p + Z_0} \\\\
        \end{eqnarray}

    Parameters
    ----------
    z : Tensor
         Port Impedance.
    z0 : Tensor
        Reference Impedance.

    Returns
    -------
    Tuple
        (g, z0): The reflection coefficient, and reference impedance.
    """
    z0 = th.as_tensor(z0, dtype=z.dtype)
    if Settings().bound & Bound.IN:
        z = th.where(z == -z0, z + z0*th.finfo(z.dtype).eps, z)
        z = th.where(z == z0, z - z0*th.finfo(z.dtype).eps, z)
    return (z - z0)/(z + z0), z0


def g2z(g, z0=50.0):
    """ Gonzalez 1.3.39


    Parameters
    ----------
    g : Tensor
        Reflection Coefficient.
    z0 : Tensor
        Reference Impedance.

    Returns
    -------
    Tuple
        (z, z0): The port impedance, and reference impedance.
    """
    if Settings().bound & Bound.IN:
        z0_min = th.as_tensor(th.finfo(z0.dtype).eps, dtype=z0.dtype)
        g_abs = g.abs()
        g = th.where(g_abs == 1.0, g - th.finfo(g.dtype).eps, g)
        z0 = th.where(z0.abs() < z0_min.abs(), z0_min, z0)
    return z0*(1 + g)/(-g + 1), z0   # todo: fix rsub backpropagation for complex numbers z0*(1 + g)/(1 - g)


def s2y(s, z0=50):
    z0 = th.as_tensor(z0, dtype=s.dtype).flatten()
    s11 = s[..., 0, 0]
    s12 = s[..., 0, 1]
    s21 = s[..., 1, 0]
    s22 = s[..., 1, 1]
    y = th.empty_like(s)
    d = ((1+s11)*(1+s22)-s12*s21)*z0+si_eps_map[SI.B]
    y[..., 0, 0] = ((1-s11)*(1+s22)+s12*s21)/d
    y[..., 0, 1] = (-2*s12)/d
    y[..., 1, 0] = (-2*s21)/d
    y[..., 1, 1] = ((1+s11)*(1-s22)+s12*s21)/d
    return y, z0


def y2s(y, z0=50):
    z0 = th.as_tensor(z0, dtype=y.dtype).flatten()
    y11 = y[..., 0, 0]
    y12 = y[..., 0, 1]
    y21 = y[..., 1, 0]
    y22 = y[..., 1, 1]
    y0 = 1/z0
    s = th.empty_like(y)
    d = (y11 + y0)*(y22 + y0) - y12*y21+si_eps_map[SI.Z]
    s[..., 0, 0] = ((y0 - y11)*(y0 + y22) + y12*y21)/d
    s[..., 0, 1] = (-2*y12*y0)/d
    s[..., 1, 1] = ((y0 + y11)*(y0 - y22) + y12*y21)/d
    s[..., 1, 0] = (-2*y21*y0)/d
    return s, z0


def s2a(s, z0=50):
    z0 = th.as_tensor(z0, dtype=s.dtype).flatten()
    return t2a(n2t(network.s2t(t2n(s))), z0=z0)[0]


def a2s(a, z0=50):
    z0 = th.as_tensor(z0, dtype=a.dtype).flatten()
    return n2t(network.t2s(t2n(a2t(a, z0=z0)[0])))


def t2a(t, z0=50.):
    z0 = th.as_tensor(z0, dtype=t.dtype).flatten()
    t11, t12 = t[..., 0, 0], t[..., 0, 1]
    t21, t22 = t[..., 1, 0], t[..., 1, 1]
    a = th.empty_like(t)
    conj = th.conj
    a[..., 0, 0] = t11*z0 + t12*z0 + t21*conj(z0) + t22*conj(z0)
    a[..., 0, 1] = -z0*(t11*z0 + t21*conj(z0)) + (t12*z0 + t22*conj(z0))*conj(z0)
    a[..., 1, 0] = -t11 - t12 + t21 + t22
    a[..., 1, 1] = z0*(t11 - t21) - (t12 - t22)*conj(z0)
    a = a/(2*real(z0))
    return a, z0


def a2t(a, z0=50.):
    z0 = th.as_tensor(z0, dtype=a.dtype).flatten()
    a11, a12 = a[..., 0, 0], a[..., 0, 1]
    a21, a22 = a[..., 1, 0], a[..., 1, 1]
    t = th.empty_like(a)
    conj = th.conj
    t[..., 0, 0] = -a12 + a22*conj(z0) + (a11 - a21*conj(z0))*conj(z0)
    t[..., 0, 1] = a12 - a22*conj(z0) + z0*(a11 - a21*conj(z0))
    t[..., 1, 0] = -a12 - a22*z0 + (a11 + a21*z0)*conj(z0)
    t[..., 1, 1] = a12 + a22*z0 + z0*(a11 + a21*z0)
    t = t/(2*real(z0))
    return t, z0


def s2sp(s, z1=50., z2=50., z0=50.):
    z0 = th.as_tensor(z0, dtype=s.dtype).flatten()
    z1 = th.as_tensor(z1, dtype=s.dtype).flatten()
    z2 = th.as_tensor(z2, dtype=s.dtype).flatten()
    g1 = z2g(z1, z0=z0)[0]
    g2 = z2g(z2, z0=z0)[0]
    s11 = s[..., 0, 0]
    s12 = s[..., 0, 1]
    s21 = s[..., 1, 0]
    s22 = s[..., 1, 1]
    d = (1-g1*s11)*(1-s22*g2) - s21*s12*g2*g1
    sp = th.empty_like(s)
    conj = th.conj
    sp[..., 0, 0] = (1-g1)/(1-conj(g1))*((1-g2*s22)*(s11-conj(g1)) + s12*s21*g2)/d
    sp[..., 1, 1] = (1-g2)/(1-conj(g2))*((1-g1*s11)*(s22-conj(g2)) + s12*s21*g1)/d
    sp[..., 0, 1] = (1-g2)/abs(1-g2)*abs(1-g1)/(1-conj(g1))*(s12*th.sqrt((1-abs(g1)**2)*(1-abs(g2)**2)))/d
    sp[..., 1, 0] = (1-g1)/abs(1-g1)*abs(1-g2)/(1-conj(g2))*(s21*th.sqrt((1-abs(g1)**2)*(1-abs(g2)**2)))/d
    return sp, z1, z2, z0


def sp2s(sp, z1, z2, z0=50.):
    z0 = th.as_tensor(z0, dtype=sp.dtype).flatten()
    z1 = th.as_tensor(z1, dtype=sp.dtype).flatten()
    z2 = th.as_tensor(z2, dtype=sp.dtype).flatten()
    conj = th.conj
    z1_ = g2z((50 - z1) / (50 + conj(z1)), z0=z0)[0]
    z2_ = g2z((50 - z2) / (50 + conj(z2)), z0=z0)[0]
    return s2sp(sp, z1_, z2_)[0], z1, z2, z0


def t2tp(t, z1=50., z2=50., z0=50.):
    z0 = th.as_tensor(z0, dtype=t.dtype).flatten()
    z1 = th.as_tensor(z1, dtype=t.dtype).flatten()
    z2 = th.as_tensor(z2, dtype=t.dtype).flatten()
    t11, t12 = t[..., 0, 0], t[..., 0, 1]
    t21, t22 = t[..., 1, 0], t[..., 1, 1]
    tp = th.empty_like(t)
    conj = th.conj
    tp[..., 0, 0] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z2))**0.5*(-(z0 - z2)*(t12*z0 + t12*conj(z1) + t22*z0 - t22*conj(z1)) + (z0 + z2)*(t11*z0 + t11*conj(z1) + t21*z0 - t21*conj(z1)))/(2*z0*(z2 + conj(z2)))
    tp[..., 0, 1] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z2))**0.5*(-(z0 - conj(z2))*(t11*z0 + t11*conj(z1) + t21*z0 - t21*conj(z1)) + (z0 + conj(z2))*(t12*z0 + t12*conj(z1) + t22*z0 - t22*conj(z1)))/(2*z0*(z2 + conj(z2)))
    tp[..., 1, 0] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z2))**0.5*(-(z0 - z2)*(t12*z0 - t12*z1 + t22*z0 + t22*z1) + (z0 + z2)*(t11*z0 - t11*z1 + t21*z0 + t21*z1))/(2*z0*(z2 + conj(z2)))
    tp[..., 1, 1] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z2))**0.5*(-(z0 - conj(z2))*(t11*z0 - t11*z1 + t21*z0 + t21*z1) + (z0 + conj(z2))*(t12*z0 - t12*z1 + t22*z0 + t22*z1))/(2*z0*(z2 + conj(z2)))
    return tp, z1, z2, z0


def tp2t(tp, z1=50., z2=50., z0=50.):
    z0 = th.as_tensor(z0, dtype=tp.dtype).flatten()
    z1 = th.as_tensor(z1, dtype=tp.dtype).flatten()
    z2 = th.as_tensor(z2, dtype=tp.dtype).flatten()
    tp11, tp12 = tp[..., 0, 0], tp[..., 0, 1]
    tp21, tp22 = tp[..., 1, 0], tp[..., 1, 1]
    t = th.empty_like(tp)
    conj = th.conj
    t[..., 0, 0] = (real(z0)*real(z1))**0.5*(real(z0)*real(z2))**(-0.5)*((z0 + z1)*(tp11*z0 + tp11*conj(z2) + tp12*z0 - tp12*z2) - (z0 - conj(z1))*(tp21*z0 + tp21*conj(z2) + tp22*z0 - tp22*z2))/(2*z0*(z1 + conj(z1)))
    t[..., 0, 1] = (real(z0)*real(z1))**0.5*(real(z0)*real(z2))**(-0.5)*((z0 + z1)*(tp11*z0 - tp11*conj(z2) + tp12*z0 + tp12*z2) - (z0 - conj(z1))*(tp21*z0 - tp21*conj(z2) + tp22*z0 + tp22*z2))/(2*z0*(z1 + conj(z1)))
    t[..., 1, 0] = (real(z0)*real(z1))**0.5*(real(z0)*real(z2))**(-0.5)*(-(z0 - z1)*(tp11*z0 + tp11*conj(z2) + tp12*z0 - tp12*z2) + (z0 + conj(z1))*(tp21*z0 + tp21*conj(z2) + tp22*z0 - tp22*z2))/(2*z0*(z1 + conj(z1)))
    t[..., 1, 1] = (real(z0)*real(z1))**0.5*(real(z0)*real(z2))**(-0.5)*(-(z0 - z1)*(tp11*z0 - tp11*conj(z2) + tp12*z0 + tp12*z2) + (z0 + conj(z1))*(tp21*z0 - tp21*conj(z2) + tp22*z0 + tp22*z2))/(2*z0*(z1 + conj(z1)))
    return t, z1, z2, z0


def z2zp(z, a):
    shape = z.shape
    z = z.flatten()
    a11, a12 = a[..., 0, 0], a[..., 0, 1]
    a21, a22 = a[..., 1, 0], a[..., 1, 1]
    zp = (a12 + a22*z)/(a11 + a21*z)
    zp = zp.reshape(shape)
    return zp


def zp2z(zp, a):
    shape = zp.shape
    zp = zp.flatten()
    a11, a12 = a[..., 0, 0], a[..., 0, 1]
    a21, a22 = a[..., 1, 0], a[..., 1, 1]
    z = (-a11*zp + a12)/(a21*zp - a22)
    z = z.reshape(shape)
    return z


def gl2gin(gl, s):
    shape = gl.shape
    gl = gl.flatten()
    s11, s12 = s[..., 0, 0], s[..., 0, 1]
    s21, s22 = s[..., 1, 0], s[..., 1, 1]
    gin = s11 + s12*gl*s21/(1 - s22*gl)
    gin = gin.reshape(shape)
    return gin, s


def gin2gl(gin, s):
    shape = gin.shape
    gin = gin.flatten()
    s11, s12 = s[..., 0, 0], s[..., 0, 1]
    s21, s22 = s[..., 1, 0], s[..., 1, 1]
    gl = (gin - s11)/(gin*s22 - s11*s22 + s12*s21)
    gl = gl.reshape(shape)
    return gl, s


def s4t(s):
    M = det_minor
    s11, s12, s13, s14 = s[..., 0, 0], s[..., 0, 1], s[..., 0, 2], s[..., 0, 3]
    s21, s22, s23, s24 = s[..., 1, 0], s[..., 1, 1], s[..., 1, 2], s[..., 1, 3]
    s31, s32, s33, s34 = s[..., 2, 0], s[..., 2, 1], s[..., 2, 2], s[..., 2, 3]
    s41, s42, s43, s44 = s[..., 3, 0], s[..., 3, 1], s[..., 3, 2], s[..., 3, 3]
    t = th.empty_like(s)
    t[..., 0, 0] = M(s, 1, 3)/(s31*s42 - s32*s41)
    t[..., 0, 1] = (s11*s42 - s12*s41)/(s31*s42 - s32*s41)
    t[..., 0, 2] = M(s, 1, 2)/(s31*s42 - s32*s41)
    t[..., 0, 3] = (-s11*s32 + s12*s31)/(s31*s42 - s32*s41)
    t[..., 1, 0] = (s32*s43 - s33*s42)/(s31*s42 - s32*s41)
    t[..., 1, 1] = s42/(s31*s42 - s32*s41)
    t[..., 1, 2] = (s32*s44 - s34*s42)/(s31*s42 - s32*s41)
    t[..., 1, 3] = -s32/(s31*s42 - s32*s41)
    t[..., 2, 0] = M(s, 0, 3)/(s31*s42 - s32*s41)
    t[..., 2, 1] = (s21*s42 - s22*s41)/(s31*s42 - s32*s41)
    t[..., 2, 2] = M(s, 0, 2)/(s31*s42 - s32*s41)
    t[..., 2, 3] = (-s21*s32 + s22*s31)/(s31*s42 - s32*s41)
    t[..., 3, 0] = (-s31*s43 + s33*s41)/(s31*s42 - s32*s41)
    t[..., 3, 1] = -s41/(s31*s42 - s32*s41)
    t[..., 3, 2] = (-s31*s44 + s34*s41)/(s31*s42 - s32*s41)
    t[..., 3, 3] = s31/(s31*s42 - s32*s41)
    return t


def t4s(t):
    M = det_minor
    t11, t12, t13, t14 = t[..., 0, 0], t[..., 0, 1], t[..., 0, 2], t[..., 0, 3]
    t21, t22, t23, t24 = t[..., 1, 0], t[..., 1, 1], t[..., 1, 2], t[..., 1, 3]
    t31, t32, t33, t34 = t[..., 2, 0], t[..., 2, 1], t[..., 2, 2], t[..., 2, 3]
    t41, t42, t43, t44 = t[..., 3, 0], t[..., 3, 1], t[..., 3, 2], t[..., 3, 3]
    s = th.empty_like(t)
    s[..., 0, 0] = (t12*t44 - t14*t42)/(t22*t44 - t24*t42)
    s[..., 0, 1] = (-t12*t24 + t14*t22)/(t22*t44 - t24*t42)
    s[..., 0, 2] = M(t, 2, 2)/(t22*t44 - t24*t42)
    s[..., 0, 3] = -M(t, 2, 0)/(t22*t44 - t24*t42)
    s[..., 1, 0] = (t32*t44 - t34*t42)/(t22*t44 - t24*t42)
    s[..., 1, 1] = (t22*t34 - t24*t32)/(t22*t44 - t24*t42)
    s[..., 1, 2] = -M(t, 0, 2)/(t22*t44 - t24*t42)
    s[..., 1, 3] = M(t, 0, 0)/(t22*t44 - t24*t42)
    s[..., 2, 0] = t44/(t22*t44 - t24*t42)
    s[..., 2, 1] = -t24/(t22*t44 - t24*t42)
    s[..., 2, 2] = (-t21*t44 + t24*t41)/(t22*t44 - t24*t42)
    s[..., 2, 3] = (-t23*t44 + t24*t43)/(t22*t44 - t24*t42)
    s[..., 3, 0] = -t42/(t22*t44 - t24*t42)
    s[..., 3, 1] = t22/(t22*t44 - t24*t42)
    s[..., 3, 2] = (t21*t42 - t22*t41)/(t22*t44 - t24*t42)
    s[..., 3, 3] = (-t22*t43 + t23*t42)/(t22*t44 - t24*t42)
    return s


def det_minor(arr, i, j):
    # determinant with ith row, jth column removed
    return th.det(arr[...,
                  th.cat((th.arange(i), th.arange(i+1, arr.shape[-2]))).reshape(-1, 1),
                  th.cat((th.arange(j), th.arange(j+1, arr.shape[-1])))
                  ])


def t4a(t, z0=50.):
    z0 = th.as_tensor(z0, dtype=t.dtype)
    conj = th.conj
    t11, t12, t13, t14 = t[..., 0, 0], t[..., 0, 1], t[..., 0, 2], t[..., 0, 3]
    t21, t22, t23, t24 = t[..., 1, 0], t[..., 1, 1], t[..., 1, 2], t[..., 1, 3]
    t31, t32, t33, t34 = t[..., 2, 0], t[..., 2, 1], t[..., 2, 2], t[..., 2, 3]
    t41, t42, t43, t44 = t[..., 3, 0], t[..., 3, 1], t[..., 3, 2], t[..., 3, 3]
    a = th.empty_like(t)
    a[..., 0, 0] = t11*z0 + t12*z0 + t21*conj(z0) + t22*conj(z0)
    a[..., 0, 1] = -z0*(t11*z0 + t21*conj(z0)) + (t12*z0 + t22*conj(z0))*conj(z0)
    a[..., 0, 2] = t13*z0 + t14*z0 + t23*conj(z0) + t24*conj(z0)
    a[..., 0, 3] = -z0*(t13*z0 + t23*conj(z0)) + (t14*z0 + t24*conj(z0))*conj(z0)
    a[..., 1, 0] = -t11 - t12 + t21 + t22
    a[..., 1, 1] = z0*(t11 - t21) - (t12 - t22)*conj(z0)
    a[..., 1, 2] = -t13 - t14 + t23 + t24
    a[..., 1, 3] = z0*(t13 - t23) - (t14 - t24)*conj(z0)
    a[..., 2, 0] = t31*z0 + t32*z0 + t41*conj(z0) + t42*conj(z0)
    a[..., 2, 1] = -z0*(t31*z0 + t41*conj(z0)) + (t32*z0 + t42*conj(z0))*conj(z0)
    a[..., 2, 2] = t33*z0 + t34*z0 + t43*conj(z0) + t44*conj(z0)
    a[..., 2, 3] = -z0*(t33*z0 + t43*conj(z0)) + (t34*z0 + t44*conj(z0))*conj(z0)
    a[..., 3, 0] = -t31 - t32 + t41 + t42
    a[..., 3, 1] = z0*(t31 - t41) - (t32 - t42)*conj(z0)
    a[..., 3, 2] = -t33 - t34 + t43 + t44
    a[..., 3, 3] = z0*(t33 - t43) - (t34 - t44)*conj(z0)
    a = a/(2*real(z0))
    return a, z0


def a4t(a, z0=50.):
    z0 = th.as_tensor(z0, dtype=a.dtype)
    conj = th.conj
    a11, a12, a13, a14 = a[..., 0, 0], a[..., 0, 1], a[..., 0, 2], a[..., 0, 3]
    a21, a22, a23, a24 = a[..., 1, 0], a[..., 1, 1], a[..., 1, 2], a[..., 1, 3]
    a31, a32, a33, a34 = a[..., 2, 0], a[..., 2, 1], a[..., 2, 2], a[..., 2, 3]
    a41, a42, a43, a44 = a[..., 3, 0], a[..., 3, 1], a[..., 3, 2], a[..., 3, 3]
    t = th.empty_like(a)
    t[..., 0, 0] = -a12 + a22*conj(z0) + (a11 - a21*conj(z0))*conj(z0)
    t[..., 0, 1] = a12 - a22*conj(z0) + z0*(a11 - a21*conj(z0))
    t[..., 0, 2] = -a14 + a24*conj(z0) + (a13 - a23*conj(z0))*conj(z0)
    t[..., 0, 3] = a14 - a24*conj(z0) + z0*(a13 - a23*conj(z0))
    t[..., 1, 0] = -a12 - a22*z0 + (a11 + a21*z0)*conj(z0)
    t[..., 1, 1] = a12 + a22*z0 + z0*(a11 + a21*z0)
    t[..., 1, 2] = -a14 - a24*z0 + (a13 + a23*z0)*conj(z0)
    t[..., 1, 3] = a14 + a24*z0 + z0*(a13 + a23*z0)
    t[..., 2, 0] = -a32 + a42*conj(z0) + (a31 - a41*conj(z0))*conj(z0)
    t[..., 2, 1] = a32 - a42*conj(z0) + z0*(a31 - a41*conj(z0))
    t[..., 2, 2] = -a34 + a44*conj(z0) + (a33 - a43*conj(z0))*conj(z0)
    t[..., 2, 3] = a34 - a44*conj(z0) + z0*(a33 - a43*conj(z0))
    t[..., 3, 0] = -a32 - a42*z0 + (a31 + a41*z0)*conj(z0)
    t[..., 3, 1] = a32 + a42*z0 + z0*(a31 + a41*z0)
    t[..., 3, 2] = -a34 - a44*z0 + (a33 + a43*z0)*conj(z0)
    t[..., 3, 3] = a34 + a44*z0 + z0*(a33 + a43*z0)
    t = t/(2*real(z0))
    return t, z0


def t4tp(t, z1=50., z2=50., z3=50., z4=50., z0=50.):
    z0 = th.as_tensor(z0, dtype=t.dtype).flatten()
    z1 = th.as_tensor(z1, dtype=t.dtype).flatten()
    z2 = th.as_tensor(z2, dtype=t.dtype).flatten()
    z3 = th.as_tensor(z3, dtype=t.dtype).flatten()
    z4 = th.as_tensor(z4, dtype=t.dtype).flatten()
    conj = th.conj
    t11, t12, t13, t14 = t[..., 0, 0], t[..., 0, 1], t[..., 0, 2], t[..., 0, 3]
    t21, t22, t23, t24 = t[..., 1, 0], t[..., 1, 1], t[..., 1, 2], t[..., 1, 3]
    t31, t32, t33, t34 = t[..., 2, 0], t[..., 2, 1], t[..., 2, 2], t[..., 2, 3]
    t41, t42, t43, t44 = t[..., 3, 0], t[..., 3, 1], t[..., 3, 2], t[..., 3, 3]
    tp = th.empty_like(t)
    tp[..., 0, 0] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - z3)*(t12*z0 + t12*conj(z1) + t22*z0 - t22*conj(z1)) + (z0 + z3)*(t11*z0 + t11*conj(z1) + t21*z0 - t21*conj(z1)))/(2*z0*(z3 + conj(z3)))
    tp[..., 0, 1] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - conj(z3))*(t11*z0 + t11*conj(z1) + t21*z0 - t21*conj(z1)) + (z0 + conj(z3))*(t12*z0 + t12*conj(z1) + t22*z0 - t22*conj(z1)))/(2*z0*(z3 + conj(z3)))
    tp[..., 0, 2] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - z4)*(t14*z0 + t14*conj(z1) + t24*z0 - t24*conj(z1)) + (z0 + z4)*(t13*z0 + t13*conj(z1) + t23*z0 - t23*conj(z1)))/(2*z0*(z4 + conj(z4)))
    tp[..., 0, 3] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - conj(z4))*(t13*z0 + t13*conj(z1) + t23*z0 - t23*conj(z1)) + (z0 + conj(z4))*(t14*z0 + t14*conj(z1) + t24*z0 - t24*conj(z1)))/(2*z0*(z4 + conj(z4)))
    tp[..., 1, 0] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - z3)*(t12*z0 - t12*z1 + t22*z0 + t22*z1) + (z0 + z3)*(t11*z0 - t11*z1 + t21*z0 + t21*z1))/(2*z0*(z3 + conj(z3)))
    tp[..., 1, 1] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - conj(z3))*(t11*z0 - t11*z1 + t21*z0 + t21*z1) + (z0 + conj(z3))*(t12*z0 - t12*z1 + t22*z0 + t22*z1))/(2*z0*(z3 + conj(z3)))
    tp[..., 1, 2] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - z4)*(t14*z0 - t14*z1 + t24*z0 + t24*z1) + (z0 + z4)*(t13*z0 - t13*z1 + t23*z0 + t23*z1))/(2*z0*(z4 + conj(z4)))
    tp[..., 1, 3] = (real(z0)*real(z1))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - conj(z4))*(t13*z0 - t13*z1 + t23*z0 + t23*z1) + (z0 + conj(z4))*(t14*z0 - t14*z1 + t24*z0 + t24*z1))/(2*z0*(z4 + conj(z4)))
    tp[..., 2, 0] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - z3)*(t32*z0 + t32*conj(z2) + t42*z0 - t42*conj(z2)) + (z0 + z3)*(t31*z0 + t31*conj(z2) + t41*z0 - t41*conj(z2)))/(2*z0*(z3 + conj(z3)))
    tp[..., 2, 1] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - conj(z3))*(t31*z0 + t31*conj(z2) + t41*z0 - t41*conj(z2)) + (z0 + conj(z3))*(t32*z0 + t32*conj(z2) + t42*z0 - t42*conj(z2)))/(2*z0*(z3 + conj(z3)))
    tp[..., 2, 2] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - z4)*(t34*z0 + t34*conj(z2) + t44*z0 - t44*conj(z2)) + (z0 + z4)*(t33*z0 + t33*conj(z2) + t43*z0 - t43*conj(z2)))/(2*z0*(z4 + conj(z4)))
    tp[..., 2, 3] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - conj(z4))*(t33*z0 + t33*conj(z2) + t43*z0 - t43*conj(z2)) + (z0 + conj(z4))*(t34*z0 + t34*conj(z2) + t44*z0 - t44*conj(z2)))/(2*z0*(z4 + conj(z4)))
    tp[..., 3, 0] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - z3)*(t32*z0 - t32*z2 + t42*z0 + t42*z2) + (z0 + z3)*(t31*z0 - t31*z2 + t41*z0 + t41*z2))/(2*z0*(z3 + conj(z3)))
    tp[..., 3, 1] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z3))**0.5*(-(z0 - conj(z3))*(t31*z0 - t31*z2 + t41*z0 + t41*z2) + (z0 + conj(z3))*(t32*z0 - t32*z2 + t42*z0 + t42*z2))/(2*z0*(z3 + conj(z3)))
    tp[..., 3, 2] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - z4)*(t34*z0 - t34*z2 + t44*z0 + t44*z2) + (z0 + z4)*(t33*z0 - t33*z2 + t43*z0 + t43*z2))/(2*z0*(z4 + conj(z4)))
    tp[..., 3, 3] = (real(z0)*real(z2))**(-0.5)*(real(z0)*real(z4))**0.5*(-(z0 - conj(z4))*(t33*z0 - t33*z2 + t43*z0 + t43*z2) + (z0 + conj(z4))*(t34*z0 - t34*z2 + t44*z0 + t44*z2))/(2*z0*(z4 + conj(z4)))
    return tp, z1, z2, z3, z4, z0


def tp4t(tp, z1=50., z2=50., z3=50., z4=50., z0=50.):
    z0 = th.as_tensor(z0, dtype=tp.dtype).flatten()
    z1 = th.as_tensor(z1, dtype=tp.dtype).flatten()
    z2 = th.as_tensor(z2, dtype=tp.dtype).flatten()
    z3 = th.as_tensor(z3, dtype=tp.dtype).flatten()
    z4 = th.as_tensor(z4, dtype=tp.dtype).flatten()
    conj = th.conj
    tp11, tp12, tp13, tp14 = tp[..., 0, 0], tp[..., 0, 1], tp[..., 0, 2], tp[..., 0, 3]
    tp21, tp22, tp23, tp24 = tp[..., 1, 0], tp[..., 1, 1], tp[..., 1, 2], tp[..., 1, 3]
    tp31, tp32, tp33, tp34 = tp[..., 2, 0], tp[..., 2, 1], tp[..., 2, 2], tp[..., 2, 3]
    tp41, tp42, tp43, tp44 = tp[..., 3, 0], tp[..., 3, 1], tp[..., 3, 2], tp[..., 3, 3]
    t = th.empty_like(tp)
    t[..., 0, 0] = (real(z0)*real(z1))**0.5*(real(z0)*real(z3))**(-0.5)*((z0 + z1)*(tp11*z0 + tp11*conj(z3) + tp12*z0 - tp12*z3) - (z0 - conj(z1))*(tp21*z0 + tp21*conj(z3) + tp22*z0 - tp22*z3))/(2*z0*(z1 + conj(z1)))
    t[..., 0, 1] = (real(z0)*real(z1))**0.5*(real(z0)*real(z3))**(-0.5)*((z0 + z1)*(tp11*z0 - tp11*conj(z3) + tp12*z0 + tp12*z3) - (z0 - conj(z1))*(tp21*z0 - tp21*conj(z3) + tp22*z0 + tp22*z3))/(2*z0*(z1 + conj(z1)))
    t[..., 0, 2] = (real(z0)*real(z1))**0.5*(real(z0)*real(z4))**(-0.5)*((z0 + z1)*(tp13*z0 + tp13*conj(z4) + tp14*z0 - tp14*z4) - (z0 - conj(z1))*(tp23*z0 + tp23*conj(z4) + tp24*z0 - tp24*z4))/(2*z0*(z1 + conj(z1)))
    t[..., 0, 3] = (real(z0)*real(z1))**0.5*(real(z0)*real(z4))**(-0.5)*((z0 + z1)*(tp13*z0 - tp13*conj(z4) + tp14*z0 + tp14*z4) - (z0 - conj(z1))*(tp23*z0 - tp23*conj(z4) + tp24*z0 + tp24*z4))/(2*z0*(z1 + conj(z1)))
    t[..., 1, 0] = (real(z0)*real(z1))**0.5*(real(z0)*real(z3))**(-0.5)*(-(z0 - z1)*(tp11*z0 + tp11*conj(z3) + tp12*z0 - tp12*z3) + (z0 + conj(z1))*(tp21*z0 + tp21*conj(z3) + tp22*z0 - tp22*z3))/(2*z0*(z1 + conj(z1)))
    t[..., 1, 1] = (real(z0)*real(z1))**0.5*(real(z0)*real(z3))**(-0.5)*(-(z0 - z1)*(tp11*z0 - tp11*conj(z3) + tp12*z0 + tp12*z3) + (z0 + conj(z1))*(tp21*z0 - tp21*conj(z3) + tp22*z0 + tp22*z3))/(2*z0*(z1 + conj(z1)))
    t[..., 1, 2] = (real(z0)*real(z1))**0.5*(real(z0)*real(z4))**(-0.5)*(-(z0 - z1)*(tp13*z0 + tp13*conj(z4) + tp14*z0 - tp14*z4) + (z0 + conj(z1))*(tp23*z0 + tp23*conj(z4) + tp24*z0 - tp24*z4))/(2*z0*(z1 + conj(z1)))
    t[..., 1, 3] = (real(z0)*real(z1))**0.5*(real(z0)*real(z4))**(-0.5)*(-(z0 - z1)*(tp13*z0 - tp13*conj(z4) + tp14*z0 + tp14*z4) + (z0 + conj(z1))*(tp23*z0 - tp23*conj(z4) + tp24*z0 + tp24*z4))/(2*z0*(z1 + conj(z1)))
    t[..., 2, 0] = (real(z0)*real(z2))**0.5*(real(z0)*real(z3))**(-0.5)*((z0 + z2)*(tp31*z0 + tp31*conj(z3) + tp32*z0 - tp32*z3) - (z0 - conj(z2))*(tp41*z0 + tp41*conj(z3) + tp42*z0 - tp42*z3))/(2*z0*(z2 + conj(z2)))
    t[..., 2, 1] = (real(z0)*real(z2))**0.5*(real(z0)*real(z3))**(-0.5)*((z0 + z2)*(tp31*z0 - tp31*conj(z3) + tp32*z0 + tp32*z3) - (z0 - conj(z2))*(tp41*z0 - tp41*conj(z3) + tp42*z0 + tp42*z3))/(2*z0*(z2 + conj(z2)))
    t[..., 2, 2] = (real(z0)*real(z2))**0.5*(real(z0)*real(z4))**(-0.5)*((z0 + z2)*(tp33*z0 + tp33*conj(z4) + tp34*z0 - tp34*z4) - (z0 - conj(z2))*(tp43*z0 + tp43*conj(z4) + tp44*z0 - tp44*z4))/(2*z0*(z2 + conj(z2)))
    t[..., 2, 3] = (real(z0)*real(z2))**0.5*(real(z0)*real(z4))**(-0.5)*((z0 + z2)*(tp33*z0 - tp33*conj(z4) + tp34*z0 + tp34*z4) - (z0 - conj(z2))*(tp43*z0 - tp43*conj(z4) + tp44*z0 + tp44*z4))/(2*z0*(z2 + conj(z2)))
    t[..., 3, 0] = (real(z0)*real(z2))**0.5*(real(z0)*real(z3))**(-0.5)*(-(z0 - z2)*(tp31*z0 + tp31*conj(z3) + tp32*z0 - tp32*z3) + (z0 + conj(z2))*(tp41*z0 + tp41*conj(z3) + tp42*z0 - tp42*z3))/(2*z0*(z2 + conj(z2)))
    t[..., 3, 1] = (real(z0)*real(z2))**0.5*(real(z0)*real(z3))**(-0.5)*(-(z0 - z2)*(tp31*z0 - tp31*conj(z3) + tp32*z0 + tp32*z3) + (z0 + conj(z2))*(tp41*z0 - tp41*conj(z3) + tp42*z0 + tp42*z3))/(2*z0*(z2 + conj(z2)))
    t[..., 3, 2] = (real(z0)*real(z2))**0.5*(real(z0)*real(z4))**(-0.5)*(-(z0 - z2)*(tp33*z0 + tp33*conj(z4) + tp34*z0 - tp34*z4) + (z0 + conj(z2))*(tp43*z0 + tp43*conj(z4) + tp44*z0 - tp44*z4))/(2*z0*(z2 + conj(z2)))
    t[..., 3, 3] = (real(z0)*real(z2))**0.5*(real(z0)*real(z4))**(-0.5)*(-(z0 - z2)*(tp33*z0 - tp33*conj(z4) + tp34*z0 + tp34*z4) + (z0 + conj(z2))*(tp43*z0 - tp43*conj(z4) + tp44*z0 + tp44*z4))/(2*z0*(z2 + conj(z2)))
    return t, z1, z2, z3, z4, z0


rU2dBU = rW2dBW
dBU2rU = dBW2rW
