#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""
Test Units
"""
# ==============================================================================
from bob.ip.stereo.stereo import stereo_match, reproject_image, StereoParameters
from bob.ip.stereo.camera import load_camera_config, CameraPair

from bob.io.stream import Stream, StreamFile
from bob.io.image import load

from pkg_resources import resource_filename

import numpy as np
import cv2

# ==============================================================================


def resource_path(relative_path, package="bob.ip.stereo"):
    """Wrapper around pkg_resources to get the paths.

    Args:
        package (str): package name
        relative_path (str): Location of the resource in the package
    """

    return resource_filename(package, relative_path)


# ==============================================================================
# Image distances functions


def sum_of_squared_absolute_difference(array1, array2):
    """Sum the squared absolute difference between the input arrays.
    """

    return np.sum((np.abs(array1.astype(np.float64)) - np.abs(array2.astype(np.float64))) ** 2)


def euclidian_distance(array1, array2):
    """Euclidian distance between the 2 input arrays (2 norm of the difference)
    """

    return np.sqrt(np.sum(np.square(array1.astype(np.float64) - array2.astype(np.float64))))


def manhattan_distance(array1, array2):
    """Manhattan (or city block) distance between 2 inputs
    """

    return np.sum(np.abs(array1.astype(np.float64) - array2.astype(np.float64)))


def canberra_distance(array1, array2):
    """Camberra distance between the 2 inputs
    """

    return np.sum(
        np.abs(array1.astype(np.float64) - array2.astype(np.float64))
        / (np.abs(array1.astype(np.float64)) + np.abs(array2.astype(np.float64) + 1.0))
    )


# ==============================================================================
# Image distance aggregate function


def is_close_enough(image1, image2):
    """Checks if the 2 inputs are close enough to pass the test, using different metrics.

    The test is considered passed if the difference between the inputs is not more than the a small value for each 
    pixel on average.
    Eg: the first test is considered passed if "distance(image1, image2) < distance(image1, image1 + epsilon)"

    The images are expected to be in unsigned int format (so positive).

    """

    assert image1.shape == image2.shape

    nb_elements = np.prod(image1.shape)

    epsilon = 0.5  # allowed average difference between image

    return (
        sum_of_squared_absolute_difference(image1, image2) < epsilon * nb_elements
        and euclidian_distance(image1, image2) < (epsilon ** 2) * nb_elements
        and manhattan_distance(image1, image2) < epsilon * nb_elements
        and canberra_distance(image1, image2) < epsilon * nb_elements / (np.mean(image1) + np.mean(image2))
    )


def test_stereo_mapping_and_project():
    """
    Test that an image projected onto the left camera of a camera pair is close
    enough to groundtruth result.

    """

    # Load test images
    left_image = np.expand_dims(load(resource_path("test/data/nir_left_stereo.png")), 0)
    right_image = np.expand_dims(load(resource_path("test/data/nir_right_stereo.png")), 0)
    color_image = load(resource_path("test/data/color.png"))

    # load landmarks and bounding box
    landmarks = np.load(resource_path("test/data/landmarks.npy"))
    bounding_box = np.load(resource_path("test/data/bounding_box.npy"))

    # Load camera configurations
    nir_left_stereo = load_camera_config(resource_path("config/idiap_face_calibration.json"), "nir_left")
    nir_right_stereo = load_camera_config(resource_path("config/idiap_face_calibration.json"), "nir_right")
    color = load_camera_config(resource_path("config/idiap_face_calibration.json"), "color")
    camera_pair = CameraPair(nir_left_stereo, nir_right_stereo)

    stereo_parameters = StereoParameters()
    stereo_parameters.erode = True  # remove small features
    stereo_parameters.inpaint = True  # fill holes

    # Create 3D image
    map_3d = stereo_match(left_image, right_image, camera_pair, stereo_parameters)

    # project color image on left camera (rectified)
    projected_image = reproject_image(color_image, map_3d, color, camera_pair, bounding_box, landmarks)

    # Compare to saved values
    groundtruth_color_image = np.load(resource_path("test/data/projected_image.npy"))
    groundtruth_map_3d = np.load(resource_path("test/data/map_3d.npy"))
    groundtruth_landmarks = np.load(resource_path("test/data/projected_landmarks.npy"))
    groundtruth_bounding_box = np.load((resource_path("test/data/projected_bounding_box.npy")))

    assert groundtruth_color_image.shape == projected_image.shape
    assert groundtruth_map_3d.shape == map_3d.shape

    assert is_close_enough(groundtruth_color_image, projected_image)
    assert is_close_enough(groundtruth_map_3d, map_3d)

    assert np.array_equal(bounding_box, groundtruth_bounding_box)
    assert np.allclose(landmarks, groundtruth_landmarks)


def test_stereo_filters():
    """Test the stereo :obj:`~bob.io.stream.StreamFilter`."""

    gt_color = load(resource_path("test/data/reprojection_color.png"))
    gt_depth = load(resource_path("test/data/reprojection_depth.png"))
    gt_warp_thermal = load(resource_path("test/data/warp_thermal.png"))
    gt_warp_swir = load(resource_path("test/data/warp_swir_norm.png"))

    landmarks = np.load(resource_path("test/data/stream_landmarks.npy"))
    bounding_box = np.load(resource_path("test/data/stream_bounding_box.npy"))
    gt_landmarks = np.load(resource_path("test/data/stream_projected_landmarks.npy"))
    gt_bounding_box = np.load(resource_path("test/data/stream_projected_bounding_box.npy"))

    f = StreamFile(
        resource_path("test/data/input_example.h5", "bob.io.stream"),
        resource_path("config/idiap_face_streams.json", "bob.io.stream"),
    )
    f.set_camera_configs(resource_path("config/idiap_face_calibration.json"))

    # stream for stereo and projection tests
    color = Stream("color", f)
    nir_left = Stream("nir_left_stereo", f).adjust(color)
    nir_right = Stream("nir_right_stereo", f).adjust(color)
    # streams for stack, normalize and warp tests
    swir_1300 = Stream("swir_1300nm", f)
    swir_1550 = Stream("swir_1550nm", f)
    thermal = Stream("thermal", f)

    # reproject operations
    map_3d = nir_left.stereo(nir_right)
    depth = map_3d.select(channel=2).colormap(colormap="jet")
    rep_color = color.reproject(nir_left, nir_right, map_3d)

    # warp operations
    swir_norm = swir_1550.normalize().stack(swir_1300.normalize()).stack(swir_1550.normalize())
    warp_swir_norm = swir_norm.warp(color)
    warp_thermal = thermal.normalize().warp(color)

    # landmarks and bounding box
    color.bounding_box[0] = bounding_box
    color.image_points[0] = landmarks

    # Compare stereo and projection results
    assert gt_depth.shape == depth[0].shape  # groundtruth correspond to first frame of stream
    assert gt_color.shape == rep_color[0].shape

    assert is_close_enough(gt_depth, depth[0])
    assert is_close_enough(gt_color, rep_color[0])

    assert np.array_equal(rep_color.bounding_box[0], gt_bounding_box)
    assert np.allclose(rep_color.image_points[0], gt_landmarks)

    # Compare warp results
    assert is_close_enough(warp_swir_norm[0][0], gt_warp_swir)
    assert is_close_enough(warp_thermal[0][0], gt_warp_thermal)
