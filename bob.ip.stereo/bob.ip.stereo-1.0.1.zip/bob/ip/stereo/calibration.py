#!/usr/bin/env python3

"""Calibration script computing intrinsic and extrinsic parameters of cameras from capture files.

This script performs the following steps: 
1. For all capture files specified in the configuration json, detect the pattern points (first on the image, if failed
processes the image (grey-closing, thresholding) and tries again)
2. Using the frames were the pattern points were detected in step 1: estimate the intrinsic parameters for each stream 
(camera) in the capture files.
3. Againg using the pattern points detected in step 1, the extrinsic parameters of the cameras are estimated with 
respect to the reference.
4. The camera poses are displayed, and the results are saved to a json file.
"""

import argparse
import os
import json
import warnings

import numpy as np
from scipy.ndimage.morphology import grey_closing
import pandas as pd
import cv2
from matplotlib import pyplot as plt

from bob.io.stream import Stream, StreamFile
from bob.io.image import bob_to_opencvbgr


def preprocess_image(image, closing_size=15, threshold=201, verbosity=None):
    """Image processing to improve pattern detection for calibration.

    Performs grey closing and adaptative threshold to enhance pattern visibility in calibration image.

    Parameters
    ----------
    image : :obj:`numpy.ndarray`
        Calibration image. (uint16)
    closing_size : int
        Grey closing size, by default 15.
    threshold : int
        Adaptative threshold passed to opencv adaptativeThreshold, by default 201.

    Returns
    -------
    image : :obj:`numpy.ndarray`
        Processed image. (uint8)
    """

    prep_image = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, threshold, 1
    ).astype(np.uint8)
    prep_image = grey_closing(prep_image, closing_size)

    if verbosity is not None and verbosity > 2:
        draw_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        draw_prep_image = cv2.cvtColor(prep_image, cv2.COLOR_GRAY2BGR)
        plt.imshow(draw_image, cmap="gray", vmin=0, vmax=255)
        plt.show()
        plt.imshow(draw_prep_image, cmap="gray", vmin=0, vmax=255)
        plt.show()
    return prep_image


def detect_chessboard_corners(image, pattern_size, verbosity):
    """Detect the chessboard pattern corners in a calibration image.

    This function returns the coordinates of the corners in between the chessboard squares, in the coordinate system of
    the image pixels.
    With a chessboard pattern, either all corners are found, or the detection fails and None is returned.

    Parameters
    ----------
    image : :obj:`numpy.ndarray`
        Calibration image. (uint8)
    pattern_size : tuple(int, int)
        Number of rows, columns in the pattern. These are the number of corners in between the board squares, so it is 1
        less than the actual number of squares in a row/column.
    verbosity : int
        If verbosity is strictly superior to 2, the detected chessboard will be plotted on the image.

    Returns
    -------
    im_points : :obj:`numpy.ndarray`
        Array of the detected corner coordinates in the image.
    """

    ret, corners = cv2.findChessboardCorners(image, pattern_size, 0)
    im_points = None
    if ret:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 300, 0.0001)
        im_points = cv2.cornerSubPix(image, corners, (11, 11), (-1, -1), criteria)
    if verbosity > 2:
        draw_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        draw_image = cv2.drawChessboardCorners(draw_image, pattern_size, im_points, True)
        plt.imshow(draw_image, cmap="gray", vmin=0, vmax=255)
        plt.show()

    return im_points


def detect_charuco_corners(image, charuco_board, verbosity):
    """Detects charuco patterns corners in a calibration image.

    This function returns the coordinates of the corners in between the charuco board squares, in the coordinate system
    of the image pixels.
    The charuco detection method is able to detect individual charuco symbol in the pattern, therefore the detection
    doesn't necessarilly return a subset of the points if not all pattern symbol are detected. In order to know which
    symbol was detected, the function also returns the identifiers of the detected points.

    Note: This function detects the charuco pattern inside the board squares, therefore the pattern size of the board
    (#rows, #cols) corresponds to the number of squares, not the number of corners in between squares.

    Parameters
    ----------
    image : :obj:`numpy.ndarray`
        Calibration image (grayscale, uint8)
    charuco_board : :obj:`cv2.aruco_CharucoBoard`
        Dictionary like structure defining the charuco patterns.
    verbosity : int
        If verbosity is strictly superior to 2, the detected pattersn will be plotted on the image.

    Returns
    -------
    im_points : :obj:`numpy.ndarray`
        Array of the detected corners coordinates in the image. Shape: (#detected_pattern, 1, 2)
    ids : :obj:`numpy.ndarray`
        Identifiers of the detected patterns. Shape: (#detected_pattern, 1)
    """

    im_points, ids = None, None
    markers, ids, rejected_points = cv2.aruco.detectMarkers(image, charuco_board.dictionary)

    if ids is not None:
        if len(ids) < 3:
            ids = None
            markers = None
        else:
            _, im_points, ids = cv2.aruco.interpolateCornersCharuco(markers, ids, image, charuco_board)

    if verbosity > 2:
        draw_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        draw_image = cv2.aruco.drawDetectedCornersCharuco(draw_image, im_points, ids)
        plt.imshow(draw_image, cmap="gray", vmin=0, vmax=255)
        plt.show()

    return im_points, ids


def detect_patterns(
    directory_path, data_config_path, pattern_type, pattern_size, params, charuco_board=None, verbosity=0
):
    """Detects chessboard or charuco patterns in the capture files.

    For all files in the calibration parameters (json loaded in `params`), this function detects the pattern and returns
    the pattern points coordinates for each stream in the files. The results (image points and IDs for charuco) are
    stored in a DataFrame. This function also returns a dictionary with the image shape per camera, which is used to
    initialize the camera intrinsic matrices.

    If the pattern is a chessboard, the same number of corners are found for all detected pattern. For charuco board,
    the detection can find a subset of the symbol present on the pattern, so the number not always the same. The ID of
    the detected symbol is then required to estimate the camera parameters.

    The pattern points dataframe has the following structure:

                     cameraXXX cameraYYY cameraZZZ

    fileAA:frameAA    ptr_pts   ptr_pts   ptr_pts
    fileBB:frameBB    ptr_pts   ptr_pts   ptr_pts
    fileCC:frameCC    ptr_pts   ptr_pts   ptr_pts

    Notes
    -----
        Color images (in bob's format) are first converted to opencv's grayscale format

        The detection is first run on the raw images. If it fails, it is tried on the pre-processed images.

    Parameters
    ----------
    directory_path : str
        Path to the directory containing the calibration data.
    data_config_path : str
        Path to the json file describing the data (names, shape, ...).
    pattern_type : str
        "charuco" or "chessboard": Type of pattern to detect.
    pattern_size : :obj:`tuple` of int
        Number of rows, number of columns in the pattern.
    params : dict
        Calibration parameters (image processing parameters, etc...)
    charuco_board : :obj:`cv2.aruco_CharucoBoard`
        Dictionary like structure defining the charuco pattern, by default None. Required if pattern_type is "charuco".
    verbosity : int
        Verbosity level, higher for more output, by default 0.

    Returns
    -------
    pattern_points : :obj:`pandas.DataFrame`
        Dataframe containing the detected patterns points in the data.
    image_size : dict
        Shape of the image for each stream in the data, which is required to initialize the camera parameters
        estimations.

    Raises
    ------
    ValueError
        If the charuco board is not specified when the pattern_type is "charuco"
    ValueError
        If the streams in the data files do not have the same number of frames.
    ValueError
        If the specified list of frames length doesn't match the number of calibration files .
    ValueError
        If the specified pattern type is not supported. (Only "chessboard" and "charuco" supported.)
    """

    if charuco_board is None and pattern_type == "charuco":
        raise ValueError("Charuco board not specified.")

    frames_dict = params["frames_list"]
    files = [os.path.join(directory_path, file) for file in frames_dict.keys()]
    frames = list(v for v in frames_dict.values())
    threshold = params["threshold"]
    closing_size = params["closing_size"]

    capture_dict = {}
    image_size = {}

    for file_idx, capture in enumerate(files):
        f = StreamFile(capture, data_config_path)

        streams = [Stream(stream, f) for stream in f.get_available_streams()]

        # Prepare dictionary to store the detection results for each camera in the data file.
        for stream in streams:
            if stream.name not in capture_dict.keys():
                capture_dict[stream.name] = {}

        # Get the indices of frames to use in data files
        if frames is None:  # take all frames
            frame_idx = range(streams[0].shape[0])
        elif isinstance(frames, list):  #
            if len(frames) != len(files):
                raise ValueError("List of frames to use does not match number of data files.")
            frame_idx = frames[file_idx]
            if isinstance(frame_idx, int):
                frame_idx = [frame_idx]

        for stream in streams:
            for frame in frame_idx:
                # Transform image to opencv's grayscale format
                image = stream.normalize()[frame]
                if image.shape[0] == 3:  # color image in bob's format -> opencv's grayscale
                    image = bob_to_opencvbgr(image)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                image = image.squeeze()  # grayscale images have channel dim of 1.

                # Normalization
                prep_image = preprocess_image(image, closing_size, threshold, verbosity)
                image_size[stream.name] = image.shape
                capture_name = capture + ":" + str(frame)

                # if detection fails, pattern_points are set to None
                if pattern_type == "chessboard":
                    ptrn_pts = detect_chessboard_corners(prep_image, pattern_size, verbosity)
                    capture_dict[stream.name][capture_name] = ptrn_pts
                    if ptrn_pts is not None:
                        print("Capture {} / stream : {} : Detect chessboard corners.".format(capture_name, stream.name))
                    else:
                        print(
                            "Capture {} / stream : {} : Failed to detect chessboard corners.".format(
                                capture_name, stream.name
                            )
                        )

                elif pattern_type == "charuco":
                    ptrn_pts, ids = detect_charuco_corners(prep_image, charuco_board, verbosity)
                    if ids is not None:
                        capture_dict[stream.name][capture_name] = (ids, ptrn_pts)
                        print("Capture {} / stream : {} : Detect charuco corners.".format(capture_name, stream.name))
                    else:
                        print(
                            "Capture {} / stream : {} : Failed to detect charuco corners.".format(
                                capture_name, stream.name
                            )
                        )
                        capture_dict[stream.name][capture_name] = None
                else:
                    raise ValueError("Invalid pattern type: " + pattern_type)

    pattern_points = pd.DataFrame(capture_dict)
    return pattern_points, image_size


def create_3Dpoints(pattern_size, square_size):
    """Returns the 3D coordinates of a board corners, in the coordinate system of the calibration pattern.

    With a pattern size (X,Y) or (rows, cols), the order of the corners iterate along X first, before Y.
    The 3D object points are created as that: (0,0,0), ..., (X-1,0,0), (0,1,0), ... , (X-1,Y-1,0).
    The 3rd coordinates is always 0, since all the points are in the plane of the board.
    Warning: for a charuco board with a pattern size (X,Y) is not equivalent a pattern (Y,X) rotated of +/- 90 degrees,
    but has different aruco markers on its board.

    The coordinates are then scaled by the size of square in the pattern, to use metric distances. (This scale is
    reported to the translaltion distance between the cameras in the extrinsinc parameters estimation)

    Parameters
    ----------
    pattern_size : :obj:`tuple` of int
        Number of rows, number of columns in the pattern. These are the number of corners in between the pattern
        squares, which is 1 less than the number of squares.
    square_size : float
        Width (or height) of a square in the pattern. The unit of this distance (eg, mm) will be the unit of distance
        in the calibration results.

    Returns
    -------
    object_points : :obj:`numpy.ndarray`
        Coordinates of the pattern corners, with respect to the board.
    """

    rows, cols = pattern_size
    object_points = np.zeros((rows * cols, 3), np.float32)
    for i in range(0, cols):
        for j in range(0, rows):
            object_points[i * rows + j] = [j, i, 0]

    object_points *= square_size
    return object_points


def get_valid_frames_for_intrinsic_calibration(detection_df, camera, pattern_type):
    """Filters the detection df to keep only the frames that allow to estimate the intrinsic parameters of `camera`.

    A frame in the calibration file has images for multiple streams. However, it is possible that the pattern was not
    detected for a stream in a frame. This function filters out the frames for which the pattern was not detected for
    the `camera` stream, returning only valid frames for the intrinsic parameter estimation of `camera`.

    Parameters
    ----------
    detection_df : :obj:`pandas.DataFrame`
        DataFrame to filter, containing the detected points coordinates (and ID if charuco pattern) for all frames in
        all calibration files.
    camera : str
        Camera which intrinsic parameters will be estimated.
    pattern_type : str
        "chessbord" or "charuco": type of pattern.

    Returns
    -------
    detection_df : :obj:`pandas.DataFrame`
        Filtered dataframe with only valid frames for intrinsic parameter estimation of `camera`.
    """

    # Drop the frames where the pattern was not detected at all.
    detection_df = detection_df[~detection_df[camera].isnull()][camera]

    # When using a charuco board, only a subset of the pattern symbol can be detected. We filter the frames where less
    # than 4 corners were detected, because at least 4 are required for intrinsic parameter estimation.
    index_to_delete = []
    if pattern_type == "charuco":
        for capture_id, capture in detection_df.iteritems():
            corners_num = capture[0].shape[0]
            if corners_num < 4:
                index_to_delete.append(capture_id)
    detection_df = detection_df.drop(index_to_delete, axis=0)
    return detection_df


def format_calibration_points_from_df(df, object_points, pattern_type):
    """Format the detected pattern points in df and objects points in appropriate format for parameter estimation.

    This is a utility function to take the image points in `df`, the corresponding 3D points in `object_points`
    and output them in the format required by opencv's camera parameters estimation functions.
    `df` contains the image points (calibration points in the coordinate system of the image pixels), and
    `object_points` the pattern points in the coordinate system of the pattern. If a chessboard pattern is used, this
    function simply return the points as separate arrays. If a charuco board is used, the function also selects the
    object points corresponding to the detected image points.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe containing the detected image points to use for calibration of a camera. Index is the capture filename
        and frame, values are the image points coordinates. (if a charuco pattern is used), the values a tuple of the
        images points ids and coordinates
    object_points : numpy.ndarray
        3D coordinates of the pattern points, in the coordinate system of the pattern. shape: (#points, 3)
    pattern_type : str
        "chessboard" or "charuco". Type of the pattern used for calibration.

    Returns
    -------
    im_pts: : list
        Images points list. The length of the list is the number of capture files. Each element in the list is an array
        of detected image points for this file. shape: (#points, 1, 2)
    obj_pts : list
        Object points list. The object points are the coordinates, in the coordinate system of the pattern, of the
        detected image points.
    ids : list
        list of the points ids. If chessboard, the list is empty (the points don't have an id).
    """

    obj_pts, im_pts, ids = [], [], []
    for capture_id, capture in df.iteritems():
        if pattern_type == "charuco":
            ids.append(capture[0])  # ids of the points
            im_pts.append(capture[1])  # coordinates of the points
        else:
            im_pts.append(capture)

    # If charuco board, mask all 3D points in the board not detected in the ids for each frame
    if pattern_type == "charuco":
        for frame in range(0, len(im_pts)):
            list_id = ids[frame]  # get the ids of the detected image points
            obj_pts.append(
                object_points[list_id, :]
            )  # select only the object points corresponding to detected image points.
    else:
        obj_pts = [object_points for _ in range(0, len(im_pts))]  # if chessboard, take them all

    return im_pts, obj_pts, ids


def compute_intrinsics(im_pts, image_size, params, obj_pts=None, ids=None, charuco_board=None):
    """Estimates intrinsic parameters of a camera

    This function is basically a wrapper of opencv's calibration function `calibrateCameraCharuco` or `calibrateCamera`.
    For more details on the format or meaning of the return values, please consult opencv's documentation, eg:
    https://docs.opencv.org/4.5.0/d9/d0c/group__calib3d.html#ga3207604e4b1a1758aa66acb6ed5aa65d
    https://docs.opencv.org/4.5.0/d9/d6a/group__aruco.html#ga54cf81c2e39119a84101258338aa7383


    Parameters
    ----------
    im_pts : list
        Coordinates of the detected pattern corners, in the image pixels coordinate system. Length of the list is the
        number of calibration capture files. Each element is an array of image points coordinates
        (shape: (#points, 1, 2))
    image_size : dict
        Shape of the images of the camera which parameters are computed.
    params : dict
        Parameters for the intrisinc parameters estimation algorithms. These are the parameters in the "intrinsics"
        field of the config passed to this script.
    obj_pts : list
        List of detected pattern points, in the coordinate system of the pattern, by default None. This is required if
        the pattern used was a chessboard pattern, but is not necessary for charuco patterns: the charuco calibration
        function builds the object points coordinates using the detected points ids (For a given size, a pattern always
        has the same points in the same place).
    ids : list
        Ids of the image points, by default None. This is only required with a charuco pattern.
    charuco_board : :obj:`cv2.aruco_CharucoBoard`
        Dictionary like structure defining the charuco pattern, by default None. Required if pattern_type is "charuco".

    Returns
    -------
    reprojection_error : float
        Reprojection error
    cam_mat : :obj:`numpy.ndarray`
        opencv 3x3 camera matrix: [[fx, 0,  cx]]
                                   [0,  fy, cy]
                                   [0,  0,  1 ]]
    dist_coefs : :obj:`numpy.ndarray`
        Opencv's distortion coefficients (length depends on the pattern type and estimation algorithm parameters)
    """

    # set the flags and parameters to pass to opencv's functions
    flags = 0
    cam_m, dist_coefs = None, None
    if params["use_intrinsic_guess"]:
        flags += cv2.CALIB_USE_INTRINSIC_GUESS
        fx, fy = params["intrinsics_guess"]["f"]
        cx, cy = params["intrinsics_guess"]["center_point"]
        dist_coefs = np.array(params["intrinsics_guess"]["dist_coefs"])
        cam_m = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1],])
    if params["fix_aspect_ratio"]:
        flags += cv2.CALIB_FIX_ASPECT_RATIO
    if params["fix_center_point"]:
        flags += cv2.CALIB_FIX_PRINCIPAL_POINT
    if params["fix_focal_length"]:
        flags += cv2.CALIB_FIX_FOCAL_LENGTH
    if params["zero_tang_dist"]:
        flags += cv2.CALIB_ZERO_TANGENT_DIST

    image_size = (image_size[1], image_size[0])
    if not isinstance(im_pts, list):
        im_pts = [im_pts]

    if charuco_board is not None:  # Using a charuco pattern
        if not isinstance(ids, list):
            ids = [ids]
        reprojection_error, cam_mat, dist_coefs, r, t = cv2.aruco.calibrateCameraCharuco(
            im_pts, ids, charuco_board, image_size, cam_m, dist_coefs, flags=flags
        )

    else:
        if not isinstance(obj_pts, list):
            obj_pts = [obj_pts]
        reprojection_error, cam_mat, dist_coefs, r, t = cv2.calibrateCamera(
            obj_pts, im_pts, image_size, cam_m, dist_coefs, flags=flags
        )
    return reprojection_error, cam_mat, dist_coefs


def get_valid_frames_for_extrinsic_calibration(detection_df, camera_1, camera_2, pattern_type):
    """Select the frames in which enough pattern points were detected to estimate extrinsic parameters between 2 cameras

    If a chessboard pattern is used, the detection either find all points, or none, so it just selects frames where the
    detection was successful for both camera.
    For charuco pattern, the detection can detect a subset of the pattern points. In this case, selects the frames wit
    enough matching points (ie with id) detected in both cameras.

    Parameters
    ----------
    detection_df : :obj:`pandas.DataFrame`
        DataFrame to filter, containing the detected points coordinates (and ID if charuco pattern) for all frames in
        all calibration files.
    camera_1 : str
        First camera which extrinsic parameters will be estimated.
    camera_2 : str
        Second camera which extrinsic parameters will be estimated.
    pattern_type : str
        "chessboard" or "charuco": type of pattern.

    Returns
    -------
    detection_df : :obj:`pandas.DataFrame`
        Filtered dataframe with only valid frames for extrinsic parameter estimation between `camera_1` and `camera_2`.
    """

    # subselect only the 2 cameras
    detection_df = detection_df.loc[:, [camera_1, camera_2]]
    # drop any row where pattern points were not detected for a camera
    detection_df = detection_df[(~detection_df[camera_1].isnull()) & (~detection_df[camera_2].isnull())]

    # If charuco board, pattern points are not necessary all detected. We need to remove those detected in one camera
    # but not the other.
    index_to_delete = []
    if pattern_type == "charuco":
        for capture_id, capture in detection_df.iterrows():
            # capture[cam][0] are the pattern ids, capture[cam][1] are the pattern coordinates
            # ids of pattern points in camera 1 also in camera 2
            mask_camera_1 = np.in1d(capture[camera_1][0], capture[camera_2][0])
            # ids of pattern points in camera 2 also in camera 1
            mask_camera_2 = np.in1d(capture[camera_2][0], capture[camera_1][0])
            if np.count_nonzero(mask_camera_1) < 4 or np.count_nonzero(mask_camera_2) < 4:
                # Not enough matching pattern points were detected, remove this capture from the df.
                index_to_delete.append(capture_id)
            else:
                # select the pattern points that were detected for both cameras
                capture[camera_1] = (capture[camera_1][0][mask_camera_1], capture[camera_1][1][mask_camera_1])
                capture[camera_2] = (capture[camera_2][0][mask_camera_2], capture[camera_2][1][mask_camera_2])
    detection_df = detection_df.drop(index_to_delete, axis=0)
    return detection_df


def compute_relative_extrinsics(obj_pts, im_pts1, cam_m1, dist_1, im_pts2, cam_m2, dist_2, image_size=None):
    """Compute extrinsic parameters of camera 1 with respect to camera 2.

    This function is basically a wrapper around opencv's stereoCalibrate function. For more information on the output
    values and signification, please refer to opencv's documentation, eg:
    https://docs.opencv.org/4.5.0/d9/d0c/group__calib3d.html#ga91018d80e2a93ade37539f01e6f07de5

    Parameters
    ----------
    obj_pts : list
        Object points list: Coordinates of the detected pattern points in the coordinate system of the pattern
    im_pts1 : list
        Image points of camera 1: the coordinates of the pattern points in the coordinate system of the camera 1 pixels.
        Each element of the list is a numpy array with shape (#points, 1, 2)
    cam_m1 : :obj:`numpy.ndarray`
        Camera matrix of camera 1.
    dist_1 : :obj:`numpy.ndarray`
        Distortion coefficients of camera 1.
    im_pts2 : :obj:`numpy.ndarray`
        Image points of camera 2: the coordinates of the pattern points in the coordinate system of the camera 2 pixels.
        Each element of the list is a numpy array with shape (#points, 1, 2)
    cam_m2 : :obj:`numpy.ndarray`
        Camera matrix of camera 2.
    dist_2 : :obj:`numpy.ndarray`
        Distortion coefficients of camera 2.
    image_size : tuple
        Shaped of the image used only to initialize the camera intrinsic matrices, by default None.

    Returns
    -------
    reprojection_error : float
        Reprojection error
    R : :obj:`numpy.ndarray`
        Relative rotation matrix of camera 1 with respect to camera 2. shape: (3, 3)
    T : :obj:`numpy.ndarray`
        Relative translation of camera 1 with respect to camera 2. shape: (3, 1)
    """

    R, T, E, F = None, None, None, None
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 1000, 1e-5)
    flags = cv2.CALIB_FIX_INTRINSIC
    # In cv2.stereoCalibrate, image_size is used to initialize the intrinsics matrix. As the intrinsics are
    # already computed, the flags can be set to cv2.CALIB_FIX_INTRINSIC
    (reprojection_error, _, _, _, _, R, T, E, F) = cv2.stereoCalibrate(
        obj_pts,
        im_pts1,
        im_pts2,
        cam_m1,
        dist_1,
        cam_m2,
        dist_2,
        image_size,
        R,
        T,
        E,
        F,
        flags=flags,
        criteria=criteria,
    )

    if R is None or T is None:
        print("WARNING: No target pair was detected in the same capture")
    return reprojection_error, R, T


# only for debugging
def display_df(df):
    for i, col in df.iteritems():
        print(i)
        if isinstance(col, pd.Series):
            for j, v in col.iteritems():
                if isinstance(v, tuple) and v[0] is not None and v[1] is not None:
                    print(j, v[0].shape, v[1].shape)
                elif v is None:
                    print(j, v)
                else:
                    print(j, v.shape)
        else:
            if isinstance(col, tuple) and col[0] is not None and col[1] is not None:
                print(col[0].shape, col[1].shape)
            elif col is None:
                print(col)
            else:
                print(col.shape)


def display_cameras_poses(camera_poses, ax_limits):
    """Plot the camera poses.

    Parameters
    ----------
    camera_poses : dict
        Camera poses: joint rotation-translation matrix H = [R|T] of the camera with respect to the reference.
    ax_limits : dict
        Limit values for the (matplotlib) axes of the plot. Defined in the "display" section of the configuration file.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(ax_limits["axe_x"])
    ax.set_ylim(ax_limits["axe_y"])
    ax.set_zlim(ax_limits["axe_z"])
    ax.set_xlabel("$X$")
    ax.set_ylabel("$Y$")
    ax.set_zlabel("$Z$")
    ax.view_init(elev=135, azim=90)
    for camera, H in camera_poses.items():
        R = H[0:3, 0:3]
        p = H[0:3, 3]
        rx = R[:, 0]
        ry = R[:, 1]
        rz = R[:, 2]
        x = p + rx * 5
        y = p + ry * 5
        z = p + rz * 5
        # ax.set_aspect('equal')
        ax.plot([p[0], x[0]], [p[1], x[1]], [p[2], x[2]], c="r", linestyle="solid")
        ax.plot([p[0], y[0]], [p[1], y[1]], [p[2], y[2]], c="g", linestyle="solid")
        ax.plot([p[0], z[0]], [p[1], z[1]], [p[2], z[2]], c="b", linestyle="solid")
        ax.text(p[0], p[1], p[2] - 3, camera)
    plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c", "--config", type=str, help="An absolute path to the JSON file containing the calibration configuration."
    )
    parser.add_argument("-i", "--intrinsics-only", type=bool, default=False, help="Compute intrinsics only.")
    parser.add_argument(
        "-r",
        "--reference",
        type=str,
        required=True,
        help="Stream name in the data files of camera to use as reference.",
    )
    parser.add_argument("-o", "--output_file", type=str, default=None, help="Output calibration JSON file.")
    parser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="Output verbosity: -v output calibration result, -vv output the dataframe, \
                             -vvv plots the target detection.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    # load calibration config
    with open(args.config) as f:
        config = json.load(f)

    capture_dir_path = config["capture_directory"]
    data_config_path = config["stream_config"]

    pattern_type = config["pattern_type"]
    square_size = config["square_size"]
    verbosity = args.verbosity
    intrinsics_only = args.intrinsics_only
    if pattern_type == "charuco":
        pattern_size = (config["pattern_rows"], config["pattern_columns"])
    if pattern_type == "chessboard":
        # The chessboard detection counts the number of corners in between the chessboard squares, which is 1 less than
        # the number of squares in a line or column.
        # The points detection of charuco counts the number of squares, so we don't need to change it.
        pattern_size = (config["pattern_rows"] - 1, config["pattern_columns"] - 1)

    charuco_board = None
    if pattern_type == "charuco":
        dict_type = cv2.aruco.DICT_4X4_1000
        aruco_dict = cv2.aruco.getPredefinedDictionary(dict_type)
        # Marker size : (b.e. 4x4 -> length of the 4 squares in the markers, not the black/white boarder)
        marker_size = config["marker_size"]
        charuco_board = cv2.aruco.CharucoBoard_create(
            pattern_size[0], pattern_size[1], square_size, marker_size, aruco_dict
        )

    # Run the pattern detection in all specified files in the calibration configuration.
    pts, image_data = detect_patterns(
        capture_dir_path,
        data_config_path,
        pattern_type,
        pattern_size,
        charuco_board=charuco_board,
        params=config,
        verbosity=verbosity,
    )

    # Create 3D object points of the pattern corners, in the coordinate system of the calibration pattern
    if pattern_type == "charuco":
        # The intrinsic parameter estimations functions from opencv use the number of corners between the pattern
        # (charuco or chessboard) squares. The pattern detection however uses the number of squares, which is one more,
        # so we need to reduce the pattern size by one.
        pattern_size = (pattern_size[0] - 1, pattern_size[1] - 1)
    object_points = create_3Dpoints(pattern_size, square_size)

    # Set print options for debuging
    np.set_printoptions(formatter={"float": lambda x: "{0:0.3f}".format(x)})

    # First all dataframe must be set and intrinsics computed for each camera
    stream = [k for k in image_data.keys()]
    calibration = dict.fromkeys(stream)  # To store the calibration results for each camera
    for idx, camera in enumerate(stream):
        image_size = image_data[camera]
        df_intrinsics = get_valid_frames_for_intrinsic_calibration(pts, camera, pattern_type)
        if df_intrinsics.empty:
            print("{} dataframe is emtpy, this camera will not be calibrated.".format(camera))
            continue

        if verbosity > 1:
            print("\n=== Intrinsics {} dataframe ===".format(camera))
            display_df(df_intrinsics)
        calibration[camera] = {}
        im_pts, obj_pts, ids = format_calibration_points_from_df(df_intrinsics, object_points, pattern_type)
        if pattern_type == "charuco":
            err, cam_mat, dist_coefs = compute_intrinsics(
                im_pts, image_size, ids=ids, charuco_board=charuco_board, params=config["intrinsics"]
            )
        else:
            err, cam_mat, dist_coefs = compute_intrinsics(
                im_pts, image_size, obj_pts=obj_pts, params=config["intrinsics"]
            )
        calibration[camera]["camera_matrix"] = cam_mat
        calibration[camera]["distortion_coefs"] = dist_coefs
        if verbosity > 0:
            print("\n=== Intrinsics {} ===".format(camera))
            print("Camera matrix \n {} \n Distortion coeffs \n {} \n".format(cam_mat, dist_coefs))
            print("Reprojection error \n {}\n".format(err))

    reference = args.reference
    if intrinsics_only:
        return
    if reference not in stream:
        raise ValueError("Reference camera " + reference + " is not in the available streams " + str(stream))

    # Get the frames that can be used for extrinsic parameters estimation
    if not intrinsics_only:
        for idx, camera in enumerate(stream):
            for camera_2 in stream:
                if camera_2 == camera:
                    continue
                df_extrinsics = get_valid_frames_for_extrinsic_calibration(pts, camera, camera_2, pattern_type)
                calibration[camera]["df_extrinsics_{}".format(camera_2)] = df_extrinsics
                if verbosity > 1:
                    print("\n=== Extrinsics {}-{} dataframe ===".format(camera, camera_2))
                    display_df(df_extrinsics)

    # Then the extrinsics between the cameras with respect to the reference are computed
    stream = [k for k, v in calibration.items() if v is not None]
    for idx, camera in enumerate(stream):
        image_size = image_data[camera]

        if not "df_extrinsics_{}".format(reference) in calibration[camera].keys():
            if reference != camera:
                warnings.warn(
                    "Can not perform extrinsic parameters estimation for cameras "
                    + camera
                    + " and "
                    + reference
                    + ", because no frames provided enough detected pattern points."
                )
            continue
        df = calibration[camera]["df_extrinsics_{}".format(reference)]
        cam_mat1 = calibration[camera]["camera_matrix"]
        cam_mat2 = calibration[reference]["camera_matrix"]
        dist_coefs1 = calibration[camera]["distortion_coefs"]
        dist_coefs2 = calibration[reference]["distortion_coefs"]
        im_pts1, obj_pts, ids = format_calibration_points_from_df(df[camera], object_points, pattern_type)
        im_pts2, obj_pts2, ids2 = format_calibration_points_from_df(df[reference], object_points, pattern_type)
        err, R, T = compute_relative_extrinsics(obj_pts, im_pts2, cam_mat2, dist_coefs2, im_pts1, cam_mat1, dist_coefs1)
        # Build the camera poses H: combination of R and T.
        H = np.eye(4)
        H[0:3, 0:3] = R
        H[0:3, 3] = T.squeeze()  # T shape is (3, 1), doesn't broadcast to (3,) without squeeze
        calibration[camera]["extrinsics_{}".format(reference)] = H
        calibration[camera]["relative_rotation"] = R
        calibration[camera]["relative_translation"] = T
        if verbosity > 0:
            print("\n=== Extrinsics {}-{} ===".format(camera, reference))
            print("Rotation \n {} \nTranslation \n {} \n".format(R, T.T))
            print("Reprojection error \n {}\n".format(err))

    # add extrinsic parameters for reference camera so it is written in config
    calibration[reference]["relative_rotation"] = np.eye(3)
    calibration[reference]["relative_translation"] = np.zeros(shape=(3,))

    # Write results in format of calibration file
    if args.output_file is not None:
        data = {}
        for camera in stream:
            # As all value are ndarray, tolist() is used to serialized the values
            data[camera] = {
                k: v.tolist() for k, v in calibration[camera].items() if "df_" not in k and "extrinsics_" not in k
            }
            data[camera]["markers"] = None  # markers should be computed with linear calibration
            data[camera]["reference"] = reference
        with open(args.output_file, "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
        print("{} written.".format(args.output_file))

    poses = {}
    for camera in stream:
        if camera == reference:
            poses[reference] = np.eye(4)
        else:
            poses[camera] = calibration[camera]["extrinsics_{}".format(reference)]
    display_cameras_poses(poses, config["display"])


if __name__ == "__main__":
    main()
