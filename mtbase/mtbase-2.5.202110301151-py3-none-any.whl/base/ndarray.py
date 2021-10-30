'''Useful functions dealing with numpy array.'''


import numpy as np


__all__ = ['ndarray_repr', 'SparseNdarray']


def ndarray_repr(a):
    '''Gets a one-line representation string for a numpy array.

    Parameters
    ----------
    a : numpy.ndarray
        input numpy array

    Returns
    -------
    str
        a short representation string for the array
    '''
    if not isinstance(a, np.ndarray):
        raise TypeError("An ndarray expected. Got '{}'.".format(type(a)))

    if a.size > 20:
        return "ndarray(shape={}, dtype={}, min={}, max={}, mean={}, std={})".format(a.shape, a.dtype, a.min(), a.max(), a.mean(), a.std())

    return "ndarray({}, dtype={})".format(repr(a.tolist()), a.dtype)


class SparseNdarray:
    '''A sparse ndarray, following TensorFlow's convention.

    Attributes
    ----------
    values : numpy.ndarray
        A 1D ndarray with shape (N,) containing all nonzero values. The dtype of 'values' specifies
        the dtype of the sparse ndarray.
    indices : numpy.ndarray
        A 2D ndarray with shape (N, rank), containing the indices of the nonzero values.
    dense_shape : tuple
        An integer tuple with 'rank' elements, specifying the shape of the ndarray.
    '''

    def __init__(self, values: np.ndarray, indices: np.ndarray, dense_shape: tuple):
        self.values = values
        self.indices = indices
        self.dense_shape = dense_shape

    def __repr__(self):
        return "SparseNdarray(dense_shape=%r, dtype=%r, len(indices)=%r)" % (self.dense_shape, self.values.dtype, len(self.indices))
