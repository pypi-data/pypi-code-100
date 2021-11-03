import numpy as np


def rotate_data(data, angle):
    """Rotate the `data` array by `angle`, where `angle` is a multiple of a square angle.

    `data` must at least have 2 dimension. If it has more, the rotation operates on the last dimensions.

    Parameters
    ----------
    data : :obj:`numpy.ndarray`
        Array to rotate.
    angle : int
        Angle by which to rotate `data`.

    Returns
    -------
    :obj:`numpy.ndarray`
        Rotated array.

    Raises
    ------
    ValueError
        If `angle` is not a supported multiple of a square angle.
    """
    if angle not in (-90, 0, 90, 180, 270):
        raise ValueError("angle must be a multiple of a square angle. Accepted values: -90, 0, 90, 180, 270.")
    if angle == 0:
        pass
    elif angle == 90:
        data = data.swapaxes(-2, -1)[..., ::-1]
    elif angle == 180:
        data = data[..., ::-1]
    elif angle in (-90, 270):
        data = data.swapaxes(-2, -1)[..., ::-1, :]
    return data


def get_index_list(index, size):
    """From an indexing value of type int, slice, list or None, generates the equivalent list of indices in a 1d array.

    Parameters
    ----------
    index : int or slice or list or None
        Indexing value in an array. Eg: 2 for array[2], slice(None, None, 2) for array[::2], ...
        Only 1d index are supported.
    size : int
        Size of the array that is indexed.

    Returns
    -------
    list of int
        Equivalent list of indices to `index`.

    Raises
    ------
    ValueError
        If `index` is not of a supported type.
    """
    # None index is equivalent to [:] i.e. slice(None, None, None)
    if index is None:
        index = slice(None, None, None)
    # frame index transform to list
    if isinstance(index, int):
        indices = [index]
    # slice transform to list
    elif isinstance(index, slice):
        # start value: handle None and negative
        if index.start is not None:
            if index.start < 0:
                start = size + index.start
            else:
                start = index.start
            # boundary case
            if start >= size:
                start = size - 1
        else:
            start = 0
        # stop value: handle None and negative
        if index.stop is not None:
            if index.stop < 0:
                stop = size + index.stop
            else:
                stop = index.stop
            # boundary case
            if stop >= size:
                stop = size - 1
        else:
            stop = size
        # step value: handle None
        if index.step is not None:
            step = index.step
        else:
            step = 1
        # generate list
        indices = list(range(start, stop, step))
    # pass lists thru
    elif isinstance(index, list):
        indices = index
    else:
        raise ValueError("index can only be None, int, slice or list, but got " + str(type(index)))
    return indices


def get_axis_size(shape, axis, indices=None):
    """Given the `shape` of an array, returns the dimension along `axis` of that array after `indices` are taken into 
    the array along `axis`.

    Parameters
    ----------
    shape : tuple of int
        Shape of an array.
    axis : int
        Axis on which `indices` operate.
    indices : int or slice or None
        The indices taken in an array with shape `shape`, on axis `axis`, by default None

    Returns
    -------
    int
        Size of an array along `axis` after `indices` are taken.

    Raises
    ------
    ValueError
        If `indices` does not have a supported type.

    Examples
    --------
    This function is used to know the size of an array after slicing into it, which is usefull when the actual slicing 
    operation is delayed as sometimes in the `~bob.io.stream.Stream` class.

    >>> a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> a[...,1:].shape[1]
    2
    >>> get_axis_size(a.shape, 1, slice(1, None, None))
    2
    """
    if indices is None:
        return shape[axis]
    else:
        if isinstance(indices, int):
            return 1
        elif isinstance(indices, slice):
            return len(range(*indices.indices(shape[axis])))
        else:
            raise ValueError("`indices` can only be None, int or slice, but got " + str(type(indices)))


class StreamArray:
    """Class to associate data to a :class:`~bob.io.stream.Stream`, for instance bounding boxes to a video stream.

    This class allows to set the value of the data array (eg the bounding box at some or each frame of a stream) without
    having to care about the shape of the stream.
    If the data is not initialized, it will return None.
    """

    def __init__(self, stream):
        """Set link to stream to access its shape.

        Parameters
        ----------
        stream : :obj:`~bob.io.stream.Stream`
            The stream to which this array of data is associated.
        """
        self.__stream = stream
        self.__data = None

    def __getitem__(self, index):
        # no value is array not initialised
        if self.__data is None:
            return None
        else:
            return self.__data[index]

    def __setitem__(self, index, data):
        # initialise array if needed
        if self.__data is None:
            self.__data = [None for i in range(self.__stream.shape[0])]
        assert len(self.__data) == self.__stream.shape[0]
        self.__data[index] = data
