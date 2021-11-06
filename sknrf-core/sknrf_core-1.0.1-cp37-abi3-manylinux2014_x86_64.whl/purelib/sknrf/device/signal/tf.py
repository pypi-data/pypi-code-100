import numpy as np
import torch as th
from torch import fft

from sknrf.settings import Settings
from sknrf.enums.runtime import Bound


def delta(shape, eps, out=None, dtype=th.complex128, layout=th.strided, device=None, requires_grad=False):
    delta = th.full(shape, eps, out=out, dtype=dtype, device=device, layout=layout, requires_grad=requires_grad)
    delta[0::Settings().t_points, :] *= Settings().t_points
    return delta


def delta_like(ts, eps, out=None, dtype=None, layout=th.strided, device=None, requires_grad=False):
    dtype = ts.dtype if dtype is None else dtype
    layout = ts.layout if layout is None else layout
    device = ts.device if device is None else device
    requires_grad = ts.requires_grad if requires_grad is None else requires_grad
    return delta(ts.shape, eps, out=out, dtype=dtype, layout=layout, device=device, requires_grad=requires_grad)


def pk(ts):
    """The peak amplitude of the signal over the time dimension.
    """
    time_axis = -2
    pk_ = ts.abs().max(time_axis)[0]
    return pk_


def set_pk(ts, pk_):
    """Set the peak amplitude of the signal over the time dimension.
    """
    time_axis = -2
    with th.no_grad():
        pk_ = th.as_tensor(pk_, dtype=ts.dtype) + th.zeros_like(ts)
        eps = th.as_tensor(th.finfo(ts.dtype).eps, dtype=ts.dtype)
        pk_ = th.where(pk_.abs() < eps.abs(), eps, pk_)

        ts[...] = pk_ * iq(ts)


def avg(ts, rms=True):
    """The average amplitude of the signal over the time dimension.
    """
    time_axis = -2
    if rms:
        avg_ = th.sqrt((ts * ts.conj()).mean(time_axis))
    else:
        avg_ = ts.abs().mean(time_axis)
    return avg_


def set_avg(ts, avg_, rms=True):
    """Set the average amplitude of the signal over the time dimension.
    """
    avg_ = th.as_tensor(avg_, dtype=ts.dtype) + th.zeros_like(ts)
    eps = th.as_tensor(th.finfo(ts.dtype).eps/Settings().t_points, dtype=ts.dtype)
    avg_ = th.where(avg_.abs() < eps.abs(), eps, avg_)

    set_pk(ts, avg_*par(ts, rms=rms))


def par(ts, rms=True):
    """The average peak-to-average ratio (PAR) of the signal over the time dimension.
    """
    par_ = pk(ts)/avg(ts, rms=rms)
    return par_


def iq(ts):
    """The normalized IQ of the signal over the time dimension.
    """
    time_axis = -2
    iq_ = ts/pk(ts).unsqueeze(time_axis)
    return iq_


def set_iq(ts, iq_):
    """Set the normalized IQ of the signal over the time sweep.
    """
    time_axis = -2
    with th.no_grad():
        iq_ = th.as_tensor(iq_, dtype=ts.dtype) + th.zeros_like(ts)
        eps = th.as_tensor(th.finfo(ts.dtype).eps, dtype=ts.dtype)
        iq_ = th.where(iq_.abs() < eps.abs(), eps, iq_)

        iq_max = pk(iq_)
        iq_norm = iq_/iq_max.unsqueeze(time_axis)
        ts[...] = pk(ts).unsqueeze(time_axis)*iq_norm


def tf(tf_):
    return tf_


def ff(tf_):
    time_axis, freq_axis = -2, -1
    nfft = tf_.shape[time_axis]

    ff_ = tf_.transpose(time_axis, freq_axis)
    ff_ = fft.fft(ff_, dim=freq_axis)/nfft
    ff_ = ff_.transpose(freq_axis, time_axis)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(ff_.dtype).eps
        ff_[0, :] = ff_[0, :]**2 if th.all(ff_[0, :].abs() < eps) and th.all(ff_[1:, :].abs() < eps) else ff_[0, :]
    ff_ = fft.fftshift(ff_, dim=time_axis)
    return ff_


def tt(tf_):
    freq_axis = -1
    cycles, points = 2, 25
    num_harmonics = tf_.shape[freq_axis]
    nfft = points*num_harmonics
    shape = list(tf_.shape)
    shape[freq_axis] = nfft - num_harmonics

    tt_ = th.cat((tf_, th.zeros(shape, dtype=tf_.dtype)), dim=freq_axis)
    tt_ = fft.ifft(tt_, dim=freq_axis)*nfft
    tt_ = th.cat((tt_,)*cycles, dim=freq_axis)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(tt_.dtype).eps
        tt_[:, 0] = tt_[:, 0]/nfft if th.all(tt_[:, 0] == eps*nfft) and th.all(tt_[:, 1:].abs() < eps) else tt_[:, 0]
    return tt_


def ft(tf_):
    ft_ = tt(ff(tf_))
    return ft_
