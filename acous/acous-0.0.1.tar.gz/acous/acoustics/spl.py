import numpy as np
from acous import fft

P_REF = 2.0e-5 # reference sound pressure based on the auditory threshold, [Pa]

def from_pressure_to_spl(p, pref=P_REF):
    """
    Calculate sound pressure level from sound pressure.

    Parameters
    ----------
        p : array_like
            Sound pressure or root mean square of sound pressure, [Pa]
        pref : scalar, optional
            Reference sound pressure, [Pa]

    Returns
    -------
        out : ndarray
            Sound pressure level, [dB]

    """
    p = np.asarray(p, dtype='float') # convert the input to an array

    return 20.0*np.log10(p/pref)

def from_spl_to_pressure(s, pref=P_REF):
    """
    Calculate sound pressure from sound pressure level.

    Parameters
    ----------
        s : array_like
            Sound pressure level, [dB]
        pref : scalar, optional
            Reference sound pressure, [dB]

    Returns
    -------
        out : ndarray
            Root mean square of sound pressure, [Pa]

    """
    s = np.asarray(s, dtype='float')

    return pref*np.power(10,s/20.0)

def cal_root_sum_square(p):
    """
    Calculate root sum square value from a sound pressure series

    Parameters
    ----------
        p : array_like
            Sound pressure or root mean square of sound pressure, [Pa]

    Returns
    -------
        out : scalar
            Root sum square of sound pressure, [Pa]

    """
    p = np.asarray(p, dtype='float')

    return np.sqrt(np.sum(np.square(p)))

def from_spl_to_oaspl(s, pref=P_REF):
    """
    Calculate overall sound pressure level from sound pressure level.

    Parameters
        s : array_like
            Sound pressure level, [dB]
        pref: scalar, optional
            Reference sound pressure, [dB]
    Returns
        out : scalar
            Overall sound pressure level, [Pa]

    """
    s = np.asarray(s, dtype='float')
    p = from_spl_to_pressure(s,pref)
    prss = cal_root_sum_square(p)

    return from_pressure_to_spl(prss,pref)

if __name__ == "__main__":
    pressure_rms = [20*1.123,200]
    spl = from_pressure_to_spl(pressure_rms)
    print(f'sound pressure level: {spl}')

    pressure = from_spl_to_pressure(spl)
    print(f'sound pressure: {pressure}')