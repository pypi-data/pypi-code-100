import torch as th
from torch import fft

from sknrf.enums.runtime import SI, si_dtype_map, Bound
from sknrf.settings import Settings

def fund():
    t_old = Settings().time
    t_start, t_stop, t_step = t_old[0], t_old[-1], t_old[1] - t_old[0]
    fm_start, fm_stop, fm_step = -1 / (2 * t_step), 1 / (2 * t_step), 1 / (t_stop - t_start)
    fm_points = th.round((fm_stop - fm_start) / fm_step + 1)
    fund_ = th.linspace(int(fm_start), int(fm_stop), int(fm_points), dtype=si_dtype_map[SI.F])
    return fund_


def freq(harm=slice(None, None, None)):
    fund_ = fund()
    freq = (fund_ + Settings().freq[harm].reshape(-1, 1)).flatten()
    return freq


def aclr(ts):
    raise NotImplementedError()


def evm(ts):
    raise NotImplementedError()


def tf(ff_):
    fund_axis, freq_axis = -2, -1
    nfft = ff_.shape[fund_axis]

    tf_ = fft.ifftshift(ff_, dim=fund_axis)
    tf_ = tf_.transpose(fund_axis, freq_axis)
    tf_ = fft.ifft(tf_, dim=freq_axis)*nfft
    tf_ = tf_.transpose(freq_axis, fund_axis)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(tf_.dtype).eps
        tf_[0, :] = tf_[0, :]/nfft if th.all(tf_[0, :].abs() < eps*nfft) and th.all(tf_[1:, :].abs() < eps) else tf_[0, :]
    return tf_


def ff(ff_):
    return ff_


def tt(ff_):
    tt_ = ft(tf(ff_))
    return tt_


def ft(ff_):
    freq_axis = -1
    cycles, points = 2, 25
    num_harmonics = ff_.shape[freq_axis]
    nfft = points * num_harmonics
    shape = list(ff_.shape)
    shape[freq_axis] = nfft - num_harmonics

    ft_ = th.cat((ff_, th.zeros(shape, dtype=ff_.dtype)), dim=freq_axis)
    ft_ = fft.ifft(ft_, dim=freq_axis)*nfft
    ft_ = th.cat((ft_,) * cycles, dim=freq_axis)

    if Settings().bound & Bound.OUT:
        eps = th.finfo(ft_.dtype).eps
        ft_[:, 0] = ft_[:, 0]/nfft if th.all(ft_[:, 0].abs() < eps*nfft) and th.all(ft_[:, 1:].abs() < eps) else ft_[:, 0]
    return ft_
