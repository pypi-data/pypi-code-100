import numpy as np
from acous import fft

def periodogram(a, fs=1.0, scaling='density'):
    """
    Estimate power spectral density using a periodogram of one-dimensional real value series.

    Parameters
    ----------
        a : array_like
            Input array, should be real input.
        fs : float, optional
            Sampling frequency of the time series. Defaults to 1.0.
        scaling : { 'density', 'spectrum' }, optional
            Selects between computing the power spectral density ('density')
            where `Pxx` has units of V**2/Hz (electric signal) or P**2/Hz (acoustic signal)
            and computing the power spectrum ('spectrum') where `Pxx` has units of V**2,
            if `x` is measured in V and `fs` is measured in Hz. Defaults to 'density'.

    Returns
    -------
        f : ndarray
            Array of length [0, Fs/2] = [0, 1/(2*d)] containing the postive frequencies.
        |Pxx| : ndarray
            Single-sided power spectral density (absolute value)

    Notes
    -----
        Sxx : ndarray
            Double-sided power spectral density

            if scaling == 'density' # ref [1]
                Sxx = (1/(fs*N))*(|A|^2)
            if scaling == 'spectrum' # ref [2] (1/N)*(|A|^2) but here we refer scipy and powerflow
                Sxx = (1/(N*N))*(|A|^2)
            in which fs is sampling frequency, dt is sampling interval, and fs = 1/dt with dt = d is the samping interval
            N is the number of total sampling points, and |A| = abs(fft(a)) = A*conjugate(A)

        We need to redefine the frequency of the fft() according to the following reason:
        The values in the result follow so-called “standard” order: If A = fft(a, n),
        then A[0] contains the zero-frequency term (the sum of the signal), which is
        always purely real for real inputs. Then A[1:n/2] contains the positive-frequency
        terms, and A[n/2+1:] contains the negative-frequency terms, in order of
        decreasingly negative frequency. For an even number of input points, A[n/2]
        represents both positive and negative Nyquist frequency, and is also purely
        real for real input. For an odd number of input points, A[(n-1)/2] contains
        the largest positive frequency, while A[(n+1)/2] contains the largest negative
        frequency. # ref [3]

        So here, for an even number of input points, we add A[n/2] and the Nyquist frequency.

    References
    ----------
        [1] The class of EAE298 by Prof. Seongkyu Lee at University of California, Davis
        [2] Michael Cerna, Audrey Harvey. The fundamentals of FFT-based signal analysis and measurement.
            Application Note 041, National Instruments, 2000.
        [3] https://numpy.org/doc/stable/reference/routines.fft.html

    """

    a = np.asarray(a, dtype='float') # make sure input array contains no complex numbers
    N = len(a)

    A = fft.fft(a, 'scipy')

    if scaling == 'density':
        scale = 1.0/(fs*N)
    elif scaling == 'spectrum':
        scale = 1.0/(N*N)
    else:
        raise ValueError(f"Unknown scaling value '{scaling}'; should be 'density' or 'spectrum'.")

    Sxx = scale*(A*np.conjugate(A))

    if N%2 == 0:
        N_pos = N//2
        f = (fs/N)*np.arange(0, N_pos+1, dtype=int)
        Pxx = np.empty(N_pos+1, complex)

        Pxx[0] = Sxx[0] # the DC value at 0 [Hz] is usually discarded in scipy and PowerFLOW
        Pxx[1:N_pos] = 2.0*Sxx[1:N_pos]
        Pxx[N_pos] = Sxx[N_pos]
    
    else:
        N_pos = (N+1)//2
        f = (fs/N)*np.arange(0, N_pos, dtype=int)
        Pxx = np.empty(N_pos, complex)

        Pxx[0] = Sxx[0]
        Pxx[1:N_pos] = 2.0*Sxx[1:N_pos]

    return f, np.abs(Pxx)