import numpy as np
import scipy as sp

def fft(a, method='dft', positive_freq_only=False):
    """
    Compute the one-dimensional discrete Fourier Transform. The data is assumed to be
    uniformly/evenly sampled (so the sample interval is not used in the transform process),
    if not, please refer to the Nonequispaced Fast Fourier Transforms (NFFT) project (https://github.com/jakevdp/nfft).

    This function computes the one-dimensional n-point discrete Fourier
    Transform (DFT) with the efficient lower than the Fast Fourier Transform (FFT) algorithm.
    Use Numpy or Scipy if need true FFT with higher calculation efficiency.

    Parameters
    ----------
        a : array_like
            Input array, can be complex.
        method : {'dft', 'numpy', 'scipy'}, optional
        positive_freq_only : bool
            If only output the results corresponding to positive frequency values.

    Returns
    -------
        out : complex ndarray

    Notes
    -----
        FFT (Fast Fourier Transform) refers to a way the discrete Fourier
        Transform (DFT) can be calculated efficiently, by using symmetries in the
        calculated terms. The symmetry is highest when `n` is a power of 2, and
        the transform is therefore most efficient for these sizes.

        The values in the result follow so-called “standard” order: If A = fft(a, n),
        then A[0] contains the zero-frequency term (the sum of the signal), which is
        always purely real for real inputs. Then A[1:n/2] contains the positive-frequency
        terms, and A[n/2+1:] contains the negative-frequency terms, in order of
        decreasingly negative frequency. For an even number of input points, A[n/2]
        represents both positive and negative Nyquist frequency, and is also purely
        real for real input. For an odd number of input points, A[(n-1)/2] contains
        the largest positive frequency, while A[(n+1)/2] contains the largest negative
        frequency. The routine np.fft.fftfreq(n) returns an array giving the frequencies
        of corresponding elements in the output. The routine np.fft.fftshift(A) shifts
        transforms and their frequencies to put the zero-frequency components in the
        middle, and np.fft.ifftshift(A) undoes that shift. # ref [1].

        When the input a is a time-domain signal and A = fft(a), np.abs(A) is its
        amplitude spectrum and np.abs(A)**2 is its power spectrum.
        The phase spectrum is obtained by np.angle(A).

    References
    ----------
        [1] https://numpy.org/doc/stable/reference/routines.fft.html
        [2] https://numpy.org/doc/stable/reference/generated/numpy.fft.fft.html
        [3] https://jakevdp.github.io/blog/2013/08/28/understanding-the-fft/
        [4] https://rosettacode.org/wiki/Fast_Fourier_transform

    """
    if not isinstance(positive_freq_only, bool):
        raise ValueError("positive_freq_only should be an bool")

    a = np.asarray(a)
    N_pos = ((len(a)-1)//2)+1 # number of total sampling points corresponding to positive frequency values

    def is_power_of_two(x):
        """
        Function to check if x is power of 2
        If x & (x-1) == 0 return True else return False
        """
        if x < 1:
            return False
        elif (x & (x-1)):
            return False
        else:
            return True

    def dft(a):
        """
        My own DFT solver, intuitive but not efficient
        """
        N = len(a)
        A = np.empty(N, complex)
        for k in range(0,N):
            summ = complex(0.0,0.0)
            for n in range(0,N):
                summ += a[n]*(np.cos(2.0*np.pi*k*n/N)-1j*np.sin(2.0*np.pi*k*n/N))
            A[k] = round(summ.real,8)+round(summ.imag,8)*1j # set calculation precision

        return A
    
    def dft_faster(a):
        """
        Ref: https://rosettacode.org/wiki/Fast_Fourier_transform
        """
        N = len(a)
        A = np.empty(N, complex)
        n = np.arange(N)
        k = n.reshape(N,1)
        M = np.exp(-2j*np.pi*k*n/N)
        prod = np.dot(M, a)
        for k in range(N):
            A[k] = round(prod[k].real,8)+round(prod[k].imag,8)*1j # set calculation precision

        return A

    def naive_fourier_transform(a):
        """
        Naive implementation of the DFT equation.
        Ref: https://nbviewer.org/github/spatialaudio/communication-acoustics-exercises/blob/master/dft-solutions.ipynb
        The input must be a one-dimensional array.
        WARNING: this implementation is extremely inefficient, but it is still faster than my dft()
        """
        N = len(a)
        n = np.arange(N)

        return np.array([np.sum(a*np.exp(-1j*2*np.pi*k*n/N)) for k in range(N)])

    def fft_raw(a): # Cooley–Tukey FFT (https://rosettacode.org/wiki/Fast_Fourier_transform)
        N = len(a)
        if N <= 2:
            return dft(a)
        if not is_power_of_two(N): # N must be a even number, and FFT is fastest when N is the power of 2 (i.e. N = 2^n)
            return dft(a)
        A = np.empty(N, complex)
        A_even = fft_raw(a[0::2])
        A_odd = fft_raw(a[1::2])
        for k in range(N//2):
            expo = np.exp(-2j*np.pi*k/N)
            A[k] = A_even[k]+expo*A_odd[k]
            A[k+N//2] = A_even[k]-expo*A_odd[k]

        return A

    if method == 'dft':
        A = dft(a)
        #A = naive_fourier_transform(a)
        if positive_freq_only:
            return A[:N_pos]
        return A

    elif method == 'dft_faster':
        A = dft_faster(a)
        if positive_freq_only:
            return A[:N_pos]
        return A

    elif method == 'fft':
        A = fft_raw(a)
        if positive_freq_only:
            return A[:N_pos]
        return A

    elif method == 'numpy':
        if positive_freq_only:
            return np.fft.fft(a)[:N_pos]
        return np.fft.fft(a)

    elif method == 'scipy':
        if positive_freq_only:
            return sp.fft.fft(a)[:N_pos]
        return sp.fft.fft(a)

    raise ValueError(f"Invalid method value '{method}'; should be 'dft', 'numpy' or 'scipy'.")

def fftfreq(n, d=1.0, method='dft', positive_freq_only=False):
    """
    Return the Discrete Fourier Transform sample frequencies.

    The returned float array `f` contains the frequency bin centers in cycles
    per unit of the sample spacing (with zero at the start). For instance, if
    the sample spacing is in seconds, then the frequency unit is cycles/second.

    Given a window length `n` and a sample spacing `d`::
      f = [0, 1, ...,   n/2-1,     -n/2, ..., -1] / (d*n)  if n is even
      f = [0, 1, ..., (n-1)/2, -(n-1)/2, ..., -1] / (d*n)  if n is odd

    Parameters
    ----------
        n : int
            Window length.
        d : scalar, optional
            Sample interval (inverse of the sampling rate). Defaults to 1.0.
        method : {'dft', 'numpy', 'scipy'}, optional
        positive_freq_only : bool
            If only output the results corresponding to positive frequency values.

    Returns
    -------
        f : ndarray
            Array of length `n` containing the sample frequencies.

    References
    ----------
        [1] https://numpy.org/doc/stable/reference/generated/numpy.fft.fftfreq.html

    Examples
    --------
        >>> signal = np.array([-2, 8, 6, 4, 1, 0, 3, 5], dtype=float)
        >>> fourier = fft.fft(signal)
        >>> n = signal.size
        >>> timestep = 0.1
        >>> freq = fft.fftfreq(n, d=timestep)
        >>> freq
        array([ 0., 1.25, 2.5, 3.75, -5, -3.75, -2.5, -1.25])

    """
    if not isinstance(n, int):
	    raise ValueError("n should be an integer")

    if not isinstance(positive_freq_only, bool):
        raise ValueError("positive_freq_only should be an bool")

    N = n # number of total sampling points
    N_pos = ((N-1)//2)+1 # number of total sampling points corresponding to positive frequency values

    sampling_interval = d # sampling interval of the data points, if data is time series then unit is [sec]
    sampling_rate = 1.0/sampling_interval

    T = N*sampling_interval # physical duration of the data series, if data is time series then unit is [sec]
    freq_interval = 1.0/T # frequency resolution (frequency interval), = 1.0/(n*d) = sampling_rate/N

    if method == 'dft':
        if positive_freq_only:
            sampling_point_num = np.arange(0, N_pos, dtype=int)
        else:
            sampling_point_num = np.empty(N, int) # return a new array of given shape and type, without initializing entries.

            p1 = np.arange(0, N_pos, dtype=int)
            sampling_point_num[:N_pos] = p1

            p2 = np.arange(-(N//2), 0, dtype=int)
            sampling_point_num[N_pos:] = p2

        return sampling_point_num*freq_interval

    elif method == 'numpy':
        if positive_freq_only:
            return np.fft.fftfreq(n, d)[:N_pos]
        return np.fft.fftfreq(n, d)

    elif method == 'scipy':
        if positive_freq_only:
            return sp.fft.fftfreq(n, d)[:N_pos]
        return sp.fft.fftfreq(n, d)

    raise ValueError(f"Invalid method value '{method}; should be 'dft', 'numpy' or 'scipy'.")

def ifft(a, method='dft'):
    """
    Compute the one-dimensional inverse discrete Fourier Transform.

    This function computes the inverse of the one-dimensional *n*-point
    discrete Fourier transform computed by `fft`. In other words,
    ``ifft(fft(a)) == a`` to within numerical accuracy.
    For a general description of the algorithm and definitions,
    see `numpy.fft`.

    The input should be ordered in the same way as is returned by `fft`,
    i.e.,
    * ``a[0]`` should contain the zero frequency term,
    * ``a[1:n//2]`` should contain the positive-frequency terms,
    * ``a[n//2 + 1:]`` should contain the negative-frequency terms, in
      increasing order starting from the most negative frequency.

    For an even number of input points, ``A[n//2]`` represents the sum of
    the values at the positive and negative Nyquist frequencies, as the two
    are aliased together. See `numpy.fft` for details.

    Parameters
    ----------
        a : array_like
            Input array, can be complex.
        method : {'dft', 'numpy', 'scipy'}, optional

    Returns
    -------
        out : complex ndarray

    Notes
    -----
        FFT (Fast Fourier Transform) refers to a way the discrete Fourier
        Transform (DFT) can be calculated efficiently, by using symmetries in the
        calculated terms. The symmetry is highest when `n` is a power of 2, and
        the transform is therefore most efficient for these sizes.

    References
    ----------
        [1] https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft.html

    """
    a = np.asarray(a)
    N = len(a)

    if method == 'dft':
        A = np.empty(N, complex)
        for k in range(0,N):
            summ = 0
            for n in range(0,N):
                summ += a[n]*(np.cos(2.0*np.pi*k*n/N)+1j*np.sin(2.0*np.pi*k*n/N))
            A[k] = ((round(summ.real, 8)+0.0) + (round(summ.imag, 8)+0.0)*1j)/N # set calculation precision

        return A

    elif method == 'numpy':
        return np.fft.ifft(a)

    elif method == 'scipy':
        return sp.fft.ifft(a)

    raise ValueError(f"Invalid method value '{method}'; should be 'dft', 'numpy' or 'scipy'.")