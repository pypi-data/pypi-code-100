import torch as th
from torch import fft

from sknrf.settings import Settings
from sknrf.enums.runtime import Bound


def tf(tt_):
    ctime_axis = -1
    cycles, points = 2, 25
    num_harmonics = tt_.shape[ctime_axis]//(cycles*points)
    nfft = points*num_harmonics

    tf_ = tt_.narrow(ctime_axis, 0, nfft)
    tf_ = fft.fft(tf_, dim=ctime_axis)/nfft
    tf_ = tf_.narrow(ctime_axis, 0, num_harmonics)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(tf_.dtype).eps
        tf_[:, 0] = tf_[:, 0]**2 if th.all(tf_[0, :].abs() < eps) and th.all(tf_[:, 1:].abs() < eps) else tf_[:, 0]
    return tf_


def ff(tt_):
    return tf(ft(tt_))


def tt(tt_):
    return tt_


def ft(tt_):
    time_axis, freq_axis = -2, -1
    nfft = tt_.shape[time_axis]

    ft_ = tt_.transpose(time_axis, freq_axis)
    ft_ = fft.fft(ft_, dim=freq_axis)/nfft
    ft_ = ft_.transpose(freq_axis, time_axis)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(ft_.dtype).eps
        ft_[0, :] = ft_[0, :]**2 if th.all(ft_[0, :].abs() < eps) and th.all(ft_[1:, :].abs() < eps) else ft_[0, :]
    ft_ = fft.fftshift(ft_, dim=time_axis)
    return ft_
