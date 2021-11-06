import torch as th
from torch import fft

from sknrf.settings import Settings
from sknrf.enums.runtime import Bound


def tf(ft_):
    tf_ = ff(tt(ft_))
    return tf_


def ff(ft_):
    ctime_axis = -1
    cycles, points = 2, 25
    num_harmonics = ft_.shape[ctime_axis] // (cycles * points)
    nfft = points * num_harmonics

    ff_ = ft_.narrow(ctime_axis, 0, nfft)
    ff_ = fft.fft(ff_, dim=ctime_axis)/nfft
    ff_ = ff_.narrow(ctime_axis, 0, num_harmonics)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(ff_.dtype).eps
        ff_[:, 0] = ff_[:, 0]**2 if th.all(ff_[:, 0].abs() < eps) and th.all(ff_[:, 1:].abs() < eps) else ff_[:, 0]
    return ff_


def tt(ft_):
    fund_axis, freq_axis = -2, -1
    nfft = ft_.shape[fund_axis]

    tt_ = fft.ifftshift(ft_, dim=fund_axis)
    tt_ = tt_.transpose(fund_axis, freq_axis)
    tt_ = fft.ifft(tt_, dim=freq_axis)*nfft
    tt_ = tt_.transpose(freq_axis, fund_axis)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(tt_.dtype).eps
        tt_[0, :] = tt_[0, :]/nfft if th.all(tt_[0, :].abs() < eps*nfft) and th.all(tt_[1:, :].abs() < eps) else tt_[0, :]
    return tt_


def ft(ft_):
    return ft_
