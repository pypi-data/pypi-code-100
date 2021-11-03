#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
Test Units
"""
# ==============================================================================
import os

import numpy as np

from bob.io.base import load, HDF5File
from pkg_resources import resource_filename

from bob.io.stream import StreamFile, Stream

# ==============================================================================


def resource_path(relative_path, package="bob.io.stream"):
    """Wrapper around pkg_resources to get the paths.

    Args:
        package (str): package name
        relative_path (str): Location of the resource in the package
    """

    return resource_filename(package, relative_path)


def test_stream_write():
    """Test writing and reading back a file through Stream and StreamFile."""

    test_data = [
        np.arange(5 * 3 * 40 * 52, dtype=np.int16).reshape((5, 3, 40, 52)),
        np.arange(5 * 1 * 5 * 5, dtype=np.int8).reshape((5, 1, 5, 5)),
        np.arange(1 * 1 * 500 * 400).astype(np.float).reshape((1, 1, 500, 400)),
        np.arange(12 * 52).astype(np.float64).reshape((12, 52)),
    ]

    test_timestamps = [
        np.linspace(0, 20*test_data[0].shape[0], test_data[0].shape[0]),
        np.linspace(10, 10*test_data[1].shape[0], test_data[1].shape[0]),
        np.linspace(100, 200*test_data[2].shape[0], test_data[2].shape[0]),
        np.linspace(5, 6*test_data[3].shape[0], test_data[3].shape[0]),
    ]

    for a_test_data, a_test_timestamps in zip(test_data, test_timestamps):
        with StreamFile(resource_path("test/data/save_test.h5"), mode="w") as output_file:
            stream = Stream("test_data")
            save_filter = stream.save(output_file)
            for i in range(a_test_data.shape[0]):
                stream.put(a_test_data[i], a_test_timestamps[i])

        with StreamFile(resource_path("test/data/save_test.h5"), mode="r") as input_file:
            stream = Stream("test_data", input_file)
            data = stream.load()
            timestamps = input_file.get_stream_timestamps("test_data")
            if np.isscalar(timestamps): # if there is only 1 frame, timestamps are returned as a scalar
                timestamps = np.array([timestamps])

        assert np.array_equal(data, a_test_data)
        assert data.dtype == a_test_data.dtype
        assert np.array_equal(timestamps, a_test_timestamps)

    os.remove(resource_path("test/data/save_test.h5"))


def test_stream():
    """Test some functionality of the stream class: shape, ndim, slicing (view), etc..."""

    # create data sets
    data_shape = (10, 3, 40, 30)  # #frames, #channels, with, height
    data_a = np.random.random_sample(data_shape)
    data_b = np.random.random_integers(5000, size=data_shape)

    # create data file
    f = HDF5File(resource_path("test/data/stream_test.h5"), "w")
    f.set("data_a", data_a)
    f.set("data_b", data_b)
    del f

    # Streams attributes when config is specified
    f = StreamFile(resource_path("test/data/input_example.h5"), resource_path("config/idiap_face_streams.json"))
    color = Stream("color", f)
    assert color.shape == (1, 3, 1920, 1200)
    assert color.timestamps[0] == 46399548

    # Streams attributes when not specified.
    f = StreamFile(resource_path("test/data/stream_test.h5"))
    stream_a = Stream("data_a", f)
    stream_b = Stream("data_b", f)
    assert stream_a.shape == data_a.shape
    assert stream_b.shape == data_b.shape
    assert stream_a.timestamps == None
    assert stream_b.timestamps == None

    # Test loading entire datasets
    ld_a = stream_a.load()
    ld_b = stream_b.load()
    assert ld_a.shape == data_a.shape
    assert ld_b.shape == data_b.shape
    assert np.array_equal(ld_a, data_a)
    assert np.array_equal(ld_b, data_b)

    # Test slicing over the first dimension
    test_slices = [
        slice(None, None, None),
        slice(5, None, None),
        slice(None, 3, None),
        slice(None, None, 3),
        slice(1, 10, 3),
        slice(9, 0, -3),
        slice(-5, -1, None),
        slice(10, 0, -3),
    ]

    for a_slice in test_slices:
        gt_slice = data_a[a_slice]
        s_slice = stream_a[a_slice].load()
        s_l_slice = stream_a.load(a_slice)
        assert np.array_equal(s_slice, gt_slice), "Slice " + str(a_slice) + " assertation failed."
        assert np.array_equal(s_l_slice, gt_slice), "Slice " + str(a_slice) + " assertation failed."

    # test slicing over other dimensions:
    test_indices = [
        (slice(None, None, None), 1),
        (slice(None, None, None), slice(None, None, None), slice(1, 2, 3), slice(4, 5, 6)),
        (slice(None, None, None), slice(None, None, None), slice(-1, -6, -3), slice(-4, 5, -6)),
    ]

    for index in test_indices:
        gt_slice = data_a[index]
        s_slice = stream_a[index]
        assert s_slice.shape == gt_slice.shape, "index " + str(index) + " shape assertation failed."
        assert s_slice.ndim == gt_slice.ndim, "index " + str(index) + " ndim assertation failed."
        assert np.array_equal(s_slice.load(), gt_slice), "index " + str(index) + " equality assertation failed."

    os.remove(resource_path("test/data/stream_test.h5"))


def test_filters():
    """Test that a few filters provide a similar result to saved groundtruth."""

    # load groundtruth for images
    gt_swir_940_dark_subtract = load(resource_path("test/data/swir_940_dark_subtract.png"))
    gt_colormap_gray = load(resource_path("test/data/gt_colormap_gray.png"))
    gt_colormap_bone = load(resource_path("test/data/gt_colormap_bone.png"))
    gt_thermal_clean = load(resource_path("test/data/gt_thermal_clean.png"))
    gt_swir_norm = load(resource_path("test/data/gt_swir_norm.png"))

    f = StreamFile(resource_path("test/data/input_example.h5"), resource_path("config/idiap_face_streams.json"))

    # define stream
    color = Stream("color", f)
    nir_left = Stream("nir_left_stereo")  # set source later
    swir_dark = Stream("swir", f)
    swir_940 = Stream("swir_940nm", f)
    swir_1050 = Stream("swir_1050nm", f)
    swir_1300 = Stream("swir_1300nm", f)
    swir_1550 = Stream("swir_1550nm", f)
    thermal = Stream("thermal", f)

    nir_left.set_source(f)

    # astype
    nir_left_unit16 = nir_left.astype(dtype=np.int16)
    assert np.array_equal(nir_left_unit16[0], nir_left[0].astype(np.int16))

    # adjust
    nir_left = nir_left.adjust(color)
    assert swir_1050.timestamps.shape != color.timestamps.shape
    assert np.allclose(swir_1050.adjust(color).timestamps, color.timestamps)

    # User defined operations through "filter": eg clipping values bellow average
    test_func = lambda data: np.where(data > data.mean(), data - data.mean(), data.mean())
    user_filter = color.filter(process_frame=test_func)
    assert np.array_equal(user_filter[0], test_func(color[0]))

    # select
    assert np.array_equal(color[0][1], color.select(channel=1)[0][0])

    # colormap
    assert np.allclose(thermal.colormap(colormap="gray")[0], gt_colormap_gray)
    assert np.allclose(thermal.colormap(colormap="bone")[0], gt_colormap_bone)

    # clean
    assert np.allclose(thermal.clean()[0], gt_thermal_clean)

    # stack and norm
    swir_norm = swir_1550.normalize().stack(swir_1300.normalize()).stack(swir_1550.normalize())
    assert np.allclose(swir_norm[0], gt_swir_norm)

    # subtract
    swir_dark = swir_dark.adjust(color)
    swir_940 = swir_940.adjust(color).subtract(swir_dark)
    assert np.array_equal(swir_940[0][0], gt_swir_940_dark_subtract)
