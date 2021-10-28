from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from wisdom.errors import FilterError
from wisdom.utils import *
from wisdom.preprocessing.filter import Filter

response_types = ['lowpass', 'highpass', 'bandpass', 'bandstop']
length_factors = dict(rectangular=0.9, hamming=3.3, hanning=3.1, blackman=5.5, kaiser=-1)
f_types = ['butter', 'cheby1', 'cheby2', 'ellip', 'bessel']


def create_firwin_filter(response_type=None, window='hamming', sfreq=SAMPLING_FREQUENCY, f_cutoff=None, order=None,
                         width=None):
    f_cutoff = np.array(f_cutoff)
    # normalise frequencies, nyq = 1
    f_cutoff = (f_cutoff / sfreq) * 2

    # filter_order
    numtaps = order + 1
    # choose whether kaiser window or not.
    if width is None and window in length_factors.keys():
        if window == 'kaiser':
            raise FilterError("The width attribute is missing, can't design a Kaiser window.")
        transition = length_factors[window] / numtaps * 2
    elif width is None and window not in length_factors.keys():
        transition = 0
    else:
        width = width / sfreq * 2
        transition = width
        atten = signal.kaiser_atten(numtaps, width)
        beta = signal.kaiser_beta(atten)
        window = ('kaiser', beta)
    info = {'window': window,
            'order': order}

    if response_type in response_types:
        if response_type == 'lowpass':
            if f_cutoff.size != 1:
                raise FilterError("Only one cutoff frequency is required for a lowpass filter.")
            f_pass = f_cutoff - (transition / 2)
            f_stop = f_cutoff + (transition / 2)
            pass_zero = True
            bands = {'passband': f"0 - {f_pass * sfreq / 2} Hz",
                     'transition band': f"{f_pass * sfreq / 2} - {f_stop * sfreq / 2} Hz",
                     "stopband": f"{f_stop * sfreq / 2} - {1 * sfreq / 2} Hz"}
        elif response_type == 'highpass':
            if f_cutoff.size != 1:
                raise FilterError("Only one cutoff frequency is required for a highpass filter.")
            f_pass = f_cutoff + (transition / 2)
            f_stop = f_cutoff - (transition / 2)
            pass_zero = False
            bands = {'stopband': f"0 - {f_stop * sfreq / 2} Hz",
                     'transition band': f"{f_stop * sfreq / 2} - {f_pass * sfreq / 2} Hz",
                     "passband": f"{f_pass * sfreq / 2} - {1 * sfreq / 2} Hz"}
        elif response_type == 'bandpass':
            if f_cutoff.size != 2:
                raise FilterError("Two cutoff frequencies are required for a bandpass filter.")
            f_pass_1 = f_cutoff[0] + (transition / 2)
            f_stop_1 = f_cutoff[0] - (transition / 2)
            f_pass_2 = f_cutoff[1] - (transition / 2)
            f_stop_2 = f_cutoff[1] + (transition / 2)
            pass_zero = False
            bands = {"stopband 1": f"0 - {f_stop_1 * sfreq / 2} Hz",
                     "transition band 1": f"{f_stop_1 * sfreq / 2} - {f_pass_1 * sfreq / 2} Hz",
                     "passband": f"{f_pass_1 * sfreq / 2} - {f_pass_2 * sfreq / 2} Hz",
                     "transition band 2": f"{f_pass_2 * sfreq / 2} - {f_stop_2 * sfreq / 2} Hz",
                     "stopband 2": f"{f_stop_2 * sfreq / 2} - {1 * sfreq / 2} Hz"}
        elif response_type == 'bandstop':
            if f_cutoff.size != 2:
                raise FilterError("Two cutoff frequencies are required for a bandstop filter.")
            f_pass_1 = f_cutoff[0] - (transition / 2)
            f_stop_1 = f_cutoff[0] + (transition / 2)
            f_pass_2 = f_cutoff[1] + (transition / 2)
            f_stop_2 = f_cutoff[1] - (transition / 2)
            pass_zero = True
            bands = {"passband 1": f"0 - {f_pass_1 * sfreq / 2} Hz",
                     "transition band 1": f"{f_pass_1 * sfreq / 2} - {f_stop_1 * sfreq / 2} Hz",
                     "stopband": f"{f_stop_1 * sfreq / 2} - {f_stop_2 * sfreq / 2} Hz",
                     "transition band 2": f"{f_stop_2 * sfreq / 2} - {f_pass_2 * sfreq / 2} Hz",
                     "passband 2": f"{f_pass_2 * sfreq / 2} - {1 * sfreq / 2} Hz"}
    else:
        raise FilterError("Not a valid response type.")

    b = signal.firwin(numtaps, f_cutoff, window=window, pass_zero=pass_zero, fs=2)
    init_state = signal.lfilter_zi(b, 1.0)
    init_state = np.transpose(np.tile(init_state, (16, 1)), axes=(1, 0))
    coeffs = (b, 1.0)

    out = Filter(filter_type='FIR - WINDOW', response_type=response_type, cutoff_freqs=f_cutoff * sfreq / 2,
                 bands=bands, filter_coeffs=coeffs, info=info, initial_state=init_state)
    return out


def create_iir_filter_wc(response_type=None, ftype='butter', order=None, wc=None, rp=None, rs=None,
                         sfreq=SAMPLING_FREQUENCY):
    if ftype not in f_types:
        raise FilterError("Not a valid option for IIR Filter Design.")
    if response_type not in response_types:
        raise FilterError("Not a valid response type.")

    coeffs = signal.iirfilter(N=order, Wn=wc, rp=rp, rs=rs, btype=response_type, analog=False, ftype=ftype, output='sos',
                              fs=sfreq)
    init_state = signal.sosfilt_zi(coeffs)
    init_state = np.transpose(np.tile(init_state, (16, 1, 1)), axes=(1, 2, 0))
    bands = {"sts": "NOT IMPLEMENTED"}
    if ftype in ['cheby1', 'cheby2', 'ellip']:
        info = {"Filter Type": ftype,
                "Order": order,
                "Passband Ripple": rp,
                "Stopband Attenuation": rs}
    else:
        info = {"Filter Type": ftype,
                "Order": order}

    out = Filter(filter_type='IIR', response_type=response_type, cutoff_freqs=wc,
                 bands=bands, filter_coeffs=coeffs, info=info, initial_state=init_state)

    return out


def notch_filter(cutoff_freq=None, quality_factor=None, sfreq=SAMPLING_FREQUENCY):
    b, a = signal.iirnotch(cutoff_freq, Q=quality_factor, fs=sfreq)
    init_state = signal.lfilter_zi(b, a)
    init_state = np.transpose(np.tile(init_state, (16, 1)), axes=(1, 0))

    bw = cutoff_freq / quality_factor
    bands = {"bandwidth": bw}

    out = Filter(filter_type='IIR - NOTCH', response_type='Notch ', cutoff_freqs=cutoff_freq, bands=bands,
                 filter_coeffs=(b, a), info=None, initial_state=init_state)
    return out


def apply_filters(data, filters_obj):
    out = np.array(data)
    counters = out[:, 16]
    counters = counters.reshape((1000, 1))
    out = out[:, :16]

    for f in filters_obj.filters:
        out, final_z = signal.sosfilt(f.filter_coeffs, out, axis=0, zi=f.init_state)
        f.init_state = final_z
    out = np.hstack((out, counters))
    return out
