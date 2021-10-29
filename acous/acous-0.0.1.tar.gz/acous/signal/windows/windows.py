import numpy as np

def hanning(M):
    """
    Return the Hanning window.

    Parameters
    ----------
        M : int
            Number of points in the output window.
            If zero or less, an empty array is returned.

    Returns
    -------
        out : ndarray, shape(M,)
            The window, with the maximum value normalized to one 
            (this maximum value `one` appears only if `M` is odd).

    References
    ----------
        [1] https://numpy.org/doc/stable/reference/generated/numpy.hanning.html
        [2] https://en.wikipedia.org/wiki/Window_function

    """
    if M < 1:
        return np.array([])
    if M == 1:
        return np.ones(1, dtype=float)
    n = np.arange(0,M,1)

    return 0.5-0.5*np.cos(2*np.pi*n/(M-1)) #return np.square(np.sin(np.pi*n/(M-1)))