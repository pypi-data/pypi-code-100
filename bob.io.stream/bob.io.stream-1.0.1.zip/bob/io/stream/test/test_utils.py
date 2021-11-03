#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
Test Units of utils functions.
"""
# ==============================================================================
import numpy as np

from bob.io.image import load

from bob.io.stream.utils import get_axis_size, get_index_list, rotate_data

# ==============================================================================

def test_rotate_data():
    """Unit tests for :func:`~bob.io.stream.utils.rotate_data`."""

    # 2D
    test_array = np.array([[1, 2], [3, 4]])
    assert np.array_equal(rotate_data(test_array, 90), np.array([[3, 1], [4, 2]]))
    assert np.array_equal(rotate_data(test_array, 180), np.array([[2, 1], [4, 3]]))
    assert np.array_equal(rotate_data(test_array, -90), np.array([[2, 4], [1, 3]]))
    assert np.array_equal(rotate_data(test_array, 270), np.array([[2, 4], [1, 3]]))
    assert np.array_equal(rotate_data(test_array, 0), test_array)

    # 3D
    test_array = np.arange(12).reshape(2, 3, 2)
    assert np.array_equal(rotate_data(test_array, 90), np.array([[[4, 2, 0], [5, 3, 1]], [[10, 8, 6], [11, 9, 7]]]))
    assert np.array_equal(
        rotate_data(test_array, 180), np.array([[[1, 0], [3, 2], [5, 4]], [[7, 6], [9, 8], [11, 10]]])
    )
    assert np.array_equal(rotate_data(test_array, -90), np.array([[[1, 3, 5], [0, 2, 4]], [[7, 9, 11], [6, 8, 10]]]))
    assert np.array_equal(rotate_data(test_array, 270), np.array([[[1, 3, 5], [0, 2, 4]], [[7, 9, 11], [6, 8, 10]]]))
    assert np.array_equal(rotate_data(test_array, 0), test_array)


def test_get_axis_size():
    """Unit tests for :func:`~bob.io.stream.utils.get_axis_size`."""

    test_array = np.arange(15000).reshape(10, 3, 50, 10)

    assert test_array[:].shape[0] == get_axis_size(test_array.shape, 0, None)
    assert 1 == get_axis_size(test_array.shape, 0, 0)
    assert test_array[::3].shape[0] == get_axis_size(test_array.shape, 0, slice(None, None, 3))
    assert test_array[3::3].shape[0] == get_axis_size(test_array.shape, 0, slice(3, None, 3))
    assert test_array[3:9:3].shape[0] == get_axis_size(test_array.shape, 0, slice(3, 9, 3))
    assert test_array[9:3].shape[0] == get_axis_size(test_array.shape, 0, slice(9, 3, None))
    assert test_array[-6:-3:2].shape[0] == get_axis_size(test_array.shape, 0, slice(-6, -3, 2))
    assert test_array[-3:-6:2].shape[0] == get_axis_size(test_array.shape, 0, slice(-3, -6, 2))
    assert test_array[3:12].shape[0] == get_axis_size(test_array.shape, 0, slice(3, 12, None))
    assert test_array[3:12].shape[0] == get_axis_size(test_array.shape, 0, slice(3, 12, None))
    assert test_array[:, :, 3:12, :].shape[2] == get_axis_size(test_array.shape, 2, slice(3, 12, None))
    assert test_array[:, :, -24:-1:5, :].shape[2] == get_axis_size(test_array.shape, 2, slice(-24, -1, 5))
    assert test_array[:, :, 3:12:4, :].shape[2] == get_axis_size(test_array.shape, 2, slice(3, 12, 4))
    assert test_array[:, :, :, 3:37:3].shape[3] == get_axis_size(test_array.shape, 3, slice(3, 37, 3))
    assert test_array[:, :, :, -16::3].shape[3] == get_axis_size(test_array.shape, 3, slice(-16, None, 3))
    assert test_array[:, :, :, -16:-16:3].shape[3] == get_axis_size(test_array.shape, 3, slice(-16, -16, 3))


def test_get_index_list():
    """Unit tests for :func:`~bob.io.stream.utils.get_index_list`."""

    test_array = np.arange(15000).reshape(10, 3, 50, 10)

    assert np.array_equal(test_array[:], test_array[get_index_list(None, test_array.shape[0])])
    assert [3] == get_index_list(3, test_array.shape[0])
    assert [2], get_index_list(2, test_array.shape[1])
    assert np.array_equal(
        test_array[..., 2:6], test_array[..., get_index_list(slice(2, 6, None), test_array.shape[-1])]
    )
    assert np.array_equal(test_array[..., 2:9:3], test_array[..., get_index_list(slice(2, 9, 3), test_array.shape[-1])])
    assert np.array_equal(
        test_array[..., -8:-2], test_array[..., get_index_list(slice(-8, -2, None), test_array.shape[-1])]
    )
    assert np.array_equal(
        test_array[..., 12:14], test_array[..., get_index_list(slice(12, 14, None), test_array.shape[-1])]
    )
    assert np.array_equal(
        test_array[..., -2:-3], test_array[..., get_index_list(slice(-2, -3, None), test_array.shape[-1])]
    )
    assert np.array_equal(
        test_array[..., -9:-3:-2], test_array[..., get_index_list(slice(-9, -3, -2), test_array.shape[-1])]
    )
    assert np.array_equal(
        test_array[..., -12:-10:-2], test_array[..., get_index_list(slice(-12, -10, -2), test_array.shape[-1])]
    )
    assert np.array_equal(test_array[..., [1, 2, 3]], test_array[..., get_index_list([1, 2, 3], test_array.shape[-1])])

