import math as mt
import numpy as np
import torch as th
from torch.nn import functional as F
from scipy.ndimage import fourier_shift
from scipy.signal import hilbert
from scipy.interpolate import griddata
from scipy.interpolate import interp1d

from sknrf.settings import Settings
from sknrf.device.signal import tf, ff
from sknrf.utilities.rf import n2t, t2n, real, imag


def val2bits(val):
    nbits = 0
    while val:
        val = val >> 1
        nbits += 1
    return nbits


def nbits2sqnr(nbits):
    """Convert the number of bits in a DAC/ADC to Signal-to-Quantization Noise Ratio in rU"""
    return 1/(1.5*2**nbits)


def load_iq_txt(i_filename, q_filename, t_points):
    iq_array = np.loadtxt(i_filename, delimiter='\r\n', dtype=np.complex) \
               + 1j*np.loadtxt(q_filename, delimiter='\r\n', dtype=np.complex)
    if t_points <= iq_array.size:
        iq_array = iq_array[0:t_points]
    else:
        iq_array = np.append(np.tile(iq_array, (int(np.floor(t_points / iq_array.size)),)),
                                     iq_array[0:np.mod(t_points, iq_array.size)])
    return n2t(iq_array.reshape(1, -1))


def save_iq_txt(iq_array, i_filename, q_filename):
    np.savetxt(i_filename, t2n(iq_array)[0, :].real, delimiter='\r\n')
    np.savetxt(q_filename, t2n(iq_array)[0, :].imag, delimiter='\r\n')


def resample_f(X, num, axis=0):
    """
    Resample `X` to `num` samples using Fourier method along the given axis.

    The resampled signal starts at the same value as `x` but is sampled
    with a spacing of ``len(x) / num * (spacing of x)``.  Because a
    Fourier method is used, the signal is assumed to be periodic.

    Parameters
    ----------
    x : array_like
        The data to be resampled.
    num : int
        The number of samples in the resampled signal.
    axis : int, optional
        The axis of `x` that is resampled.  Default is 0.

    Returns
    -------
    resampled_X

    See also
    --------
    decimate : Downsample the signal after applying an FIR or IIR filter.
    resample_poly : Resample using polyphase filtering and an FIR filter.
    """

    Nx = X.shape[axis]
    sl = [slice(None)]*X.dim()
    newshape = list(X.shape)
    newshape[axis] = num
    N = min(num, Nx)
    Y = th.zeros(newshape, dtype=X.dtype)
    sl[axis] = slice(0, (N + 1) // 2)
    Y[sl] = X[sl]
    sl[axis] = slice(-(N - 1) // 2, None)
    Y[sl] = X[sl]*(float(num) / float(Nx))
    return Y


def sinc(iq):
    t_step = Settings().t_step
    freq_m = th.linspace(-1 / (2 * t_step), 1 / (2 * t_step), Settings().t_points, dtype=iq.dtype).reshape(1, -1, 1) + \
             th.zeros_like(iq, dtype=iq.dtype)
    x = t_step * mt.pi * freq_m
    x[x.abs() < 1e-100] = 1e-100
    return th.abs(th.sin(x)/x)


def iq_delay(iq, tau):
    iq_list = []
    axis = -2
    tau_det = tau.detach()
    tau_step = tau_det[1] - tau_det[0]
    upsample_factor = int(th.ceil(Settings().t_step/tau_step).item())
    max_shift = int(th.ceil(tau_det.abs().max()/Settings().t_step).item())
    pad_width = (0, 0, max_shift, max_shift)
    signal_tf = F.pad(iq, pad_width, mode='constant', value=0.0)
    signal_ff = tf.ff(signal_tf)
    signal_ff = resample_f(signal_ff, upsample_factor*signal_ff.shape[axis], axis=axis)
    sweep_values = (tau/tau_step).type(th.int)
    for shift in sweep_values:
        iq_list.append(n2t(fourier_shift(t2n(signal_ff), int(t2n(shift).real), axis=axis)))
    signal_ff = th.stack(iq_list, dim=0)
    signal_ff = resample_f(signal_ff, Settings().t_points, axis=axis)
    iq_ = ff.tf(signal_ff)
    return iq_


def iq_phase(iq, phase):
    return iq_delay(iq, phase)


def sample_filter(iq, filter_, keepdims=False):
    t = Settings().time.reshape(1, -1, 1)
    if t.shape[-2] % 2:  # odd
        IQ = tf.ff(iq)
        IQ = IQ*filter_
        IQ = th.sum(IQ, -3, keepdims=True) if keepdims else IQ
        iq_ = ff.tf(IQ)
    else:  # t.size % 2 == 0: # even
        raise NotImplementedError("Time points and Fund points must be odd.")
    return iq_


def ind_grid(fm):
    t_step = Settings().t_step
    t_points = Settings().t_points
    fm = fm.reshape(-1)
    fm_grid = t2n(th.linspace(-1 / (2 * t_step), 1 / (2 * t_step), t_points))
    ind_grid = t2n(th.linspace(0, t_points - 1, t_points, dtype=th.int64))
    ind = n2t(interp1d(fm_grid, ind_grid, kind="nearest")(fm)).to(dtype=th.long)
    ind = ind.reshape(-1, 1)
    return ind


def fm_grid(fm):
    t_step = Settings().t_step
    t_points = Settings().t_points
    fm = fm.reshape(-1)
    fm_grid = t2n(th.linspace(-1 / (2 * t_step), 1 / (2 * t_step), t_points))
    fm = n2t(interp1d(fm_grid, fm_grid, kind="nearest")(fm))
    fm = fm.reshape(-1, 1, 1)
    return fm


def fund_phasor(iq, fm, level=False, keepdims=False):
    """Synthesize a phasor frequency sweep.

    Sweeps positive and negative frequencies individually (one-tone) using:

    .. math::

    iq = exp^{j2 \pi f_m t}

    Parameters
    ----------
    iq : Tensor
        IQ waveform of shape (1, t_points, f_points).
    fm : Tensor
        Fundamental frequency sweep of shape (fm_points).
    level:
        Level the frequency sweep with a 1/sinc(t) filter.
    keepdims:
        Keep the full dimensionality of the sweep.

    Returns
    -------
    iq : Tensor
        IQ waveform of shape (fm_points, t_points, f_points).
    """

    t = Settings().time
    fm = fm_grid(fm)
    e = th.exp(1j*(2*mt.pi*fm*t - mt.pi/2))
    iq_ = e

    if level:
        sinc_t = sinc(iq_)
        return sample_filter(iq_, 1 / sinc_t, keepdims=keepdims)
    else:
        return iq_


def fund_dsb(iq, fm, level=False, keepdims=False):
    """Synthesize a Double-Sideband (DSB) frequency sweep.

    Sweeps positive and negative frequencies simultaneously (two-tone) using:

    .. math::

    iq = sin\( 2 \pi f_m t \)

    Parameters
    ----------
    iq : Tensor
        IQ waveform of shape (1, t_points, f_points).
    fm : Tensor
        Fundamental frequency sweep of shape (fm_points).
    level:
        Level the frequency sweep with a 1/sinc(t) filter.
    keepdims:
        Keep the full dimensionality of the sweep.

    Returns
    -------
    iq : Tensor
        IQ waveform of shape (fm_points, t_points, f_points).
    """
    t = Settings().time
    fm = fm_grid(fm)
    s = th.sin(2*mt.pi*fm*t)
    iq_ = s

    if level:
        sinc_t = sinc(iq_)
        sinc_t[1:-1, :, :] /= 2
        return sample_filter(iq_, 1 / sinc_t, keepdims=keepdims)
    else:
        return iq_


def fund_ssb(iq, fm, level=False, keepdims=False):
    """Synthesize a Single-Sideband (SSB) frequency sweep.

    Sweeps positive and negative frequencies independently (one-tone), using:

    .. math::

    iq = sin\( 2 \pi f_m t \)

    Parameters
    ----------
    iq : Tensor
        IQ waveform of shape (1, t_points, f_points).
    fm : Tensor
        Fundamental frequency sweep of shape (fm_points).
    level:
        Level the frequency sweep with a 1/sinc(t) filter.
    keepdims:
        Keep the full dimensionality of the sweep.

    Returns
    -------
    iq : Tensor
        IQ waveform of shape (fm_points, t_points, f_points).
    """
    t = Settings().time
    fm = fm_grid(fm)
    s = th.sin(2 * mt.pi * fm * t)
    sa = n2t(hilbert(t2n(s), axis=-2).imag)
    iq_ = s + th.sign(fm)*1j*sa

    if level:
        sinc_t = sinc(iq_)
        return sample_filter(iq_, 1 / sinc_t, keepdims=keepdims)
    else:
        return iq_
