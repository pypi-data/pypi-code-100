#!/usr/bin/env python
#
# Copyright (c) 2021 Idiap Research Institute, https://www.idiap.ch/
#

"""Calibration script to find markers in each stream image and output a calibration usefull for linear transformation (warp).

This scripts performs the following steps:
1 Load the configuration JSON for the calibration
2 Load capture file (hdf5) with the captures of a chessboard for each camera.
3 Find the chessboards corners and keep the 4 internal corners as markers coordinates.
  If this fails, the capture is displayed to the user, which should click on the corners with the mouse.
  The mouse coordinates are recorded for the markers coordinates (to skip a stream, simply close the window).
4 (Optional) Load a previous calibration from disk and simply updates the markers coordinates.
5 Write the output calibration as a JSON file.
"""

import argparse
import copy
import json

import numpy as np
import cv2

from bob.io.stream import Stream, StreamFile
from bob.io.image import bob_to_opencvbgr

from .calibration import detect_chessboard_corners, preprocess_image

pixels_xy = []


def point_picking_event_cb(event, x, y, flags, params):
    """
    This function used as a callback when a mouse left button event is activated
    by clicking on the opencv image. It saves the pixel selected in a global
    list 'pixels_xy'.
    """

    global pixels_xy
    if event == cv2.EVENT_LBUTTONDOWN:
        pixels_xy.append([x, y])
        print("Point selected for marker {}: {}".format(len(pixels_xy), pixels_xy))


def warp_calibrate(h5_file, config, verbosity):
    """
    This function load the streams saved in datasets of an hdf5 file, with images
    of the chessboard targets. It select the frame defined, convert from bob to
    grayscale <H,W>, process if necessary and try to detect a target. The four side
    corners are saved as markers to be later used for linear warp calibration in
    bob.ip.stereo.
    If the target is not detected, an interactive figure is opened, where the user
    should click on the 4 corners (markers), in this order:
        1. down-left
        2. up-left
        3. down-right
        4. up-right

    Parameters
    ----------
    h5_file : :py:class:`str`
        Hdf5 file path with captured image of the target in datasets.
    config : :py:class:`dict`
        A configuration to read the streams in the hdf5 file and run the target
        detection.

    Returns
    -------
    :py:class:`dict`
        A dictionnary with detected markers for each streams.
    """

    # The detection findes the inner points of the chessboard pattern, which
    # are 1 less than the actual number of squares in each direction
    rows = config["pattern_rows"] - 1
    columns = config["pattern_columns"] - 1
    pattern_size = (rows, columns)
    frame = config["frame"]

    with StreamFile(h5_file, config["stream_config"]) as f:
        calibration = {}
        for stream_name, params in config["streams"].items():
            # Load Stream, select frame, convert from bob to opencv grayscale
            # and squeeze to 1
            stream = Stream(stream_name, f)
            image = stream.normalize()[frame]
            if image.shape[0] == 3:
                image = cv2.cvtColor(bob_to_opencvbgr(image), cv2.COLOR_BGR2GRAY)
            image = image.squeeze()

            if params is not None:
                if params["invert"]:
                    image = np.ones_like(image) * 255 - image
                prep_image = preprocess_image(image, params["closing"], params["threshold"])
            else:
                prep_image = None
            ret, ptrn_pts = detect_chessboard_corners(image, prep_image, pattern_size, verbosity)

            if ret:
                print("Stream : {} : Detected chessboard corners.".format(stream.name))
                markers = np.stack(
                    [
                        ptrn_pts[0][0],
                        ptrn_pts[rows - 1][0],
                        ptrn_pts[rows * (columns - 1)][0],
                        ptrn_pts[rows * columns - 1][0],
                    ]
                )
            else:
                print("Stream : {} : Failed to detect chessboard corners.".format(stream.name))
                window_name = "image_{}".format(stream.name)
                cv2.imshow(window_name, image)
                global pixels_xy
                pixels_xy = []
                cv2.setMouseCallback(window_name, point_picking_event_cb)
                while True:
                    key = cv2.waitKey(1)
                    if len(pixels_xy) == 4:
                        print(
                            "Stream : {} : Finished to collect manually\
                                the corners.".format(
                                stream.name
                            )
                        )
                        cv2.destroyAllWindows()
                        markers = np.stack(copy.copy(pixels_xy))
                        break
                    if key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                        print(
                            "Stream : {} : Failed to collect manually\
                                the corners.".format(
                                stream.name
                            )
                        )
                        cv2.destroyAllWindows()
                        markers = None
                        break

            if markers is not None:
                # As markers are ndarray, tolist() is used to serialized the values
                calibration[stream.name] = {"markers": markers.tolist()}

    return calibration


def fill_calibration(calibration, reference):
    """Add more elements (keys) to the calibration dictionnary to make it work with bob.ip.stereo standard
    
    bob.ip.stereo expects some keys to be present in a calibration JSON files, however when using only warp transform
    most of them are not required. This function simply adds them with values None. If the keys are already present, do
    not change them ; if they are missing, set them to None.

    Parameters
    ----------
    calibration : :py:class:`dict`
        A dictionary with streams/warp-markers as keys/values.
    reference : :py:class:`str`
        reference stream.

    Returns
    -------
    :py:class:`dict`
        The filled calibration.
    """

    # Make sure that all the keys used in bob.ip.stereo.Camera.load_camera_config()
    # are defined.
    standard_calibration_keys = [
        "camera_matrix",
        "distortion_coefs",
        "markers",
        "relative_rotation",
        "relative_translation",
    ]
    # load calibration config
    fill_calibration = copy.copy(calibration)
    for camera, camera_config in calibration.items():
        for key in standard_calibration_keys:
            if key not in camera_config.keys():
                # Projection markers as the 4 external corners
                fill_calibration[camera][key] = None

        if "reference" not in camera_config.keys():
            fill_calibration[camera]["reference"] = reference

    return fill_calibration


def update_calibration(markers_calibration, bobipstereo_calibration):
    """Updates the markers in bobipstereo_calibration with values from markers_calibration

    Parameters
    ----------
    markers_calibration : dict
        Calibration dictionary containing only markers values per camera
    bobipstereo_calibration : dict
        Calibration dictionnary with all keys needed for bob.ip.stereo usage.
    """

    if set(bobipstereo_calibration.keys()) != set(bobipstereo_calibration.keys()):
        raise ValueError("Stream names in warp calibration config and loaded config to update do not match!")
    for camera in bobipstereo_calibration.keys():
        if camera in markers_calibration.keys():
            bobipstereo_calibration[camera]["markers"] = markers_calibration[camera]["markers"]

    return bobipstereo_calibration


def parse_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="An absolute path to the JSON file containing the configuration \
              to run the warp calibration.",
    )
    parser.add_argument("-r", "--reference", type=str, default=None, help="Reference stream.")
    parser.add_argument("-i", "--h5-file", type=str, default=None, help="Input hdf5 file.")
    parser.add_argument("-o", "--output-file", type=str, default=None, help="Output calibration JSON file.")
    parser.add_argument(
        "-u",
        "--update_calibration",
        type=str,
        default=None,
        help="This calibration will used for the output values, except for the markers position which are updated by the calibration.",
    )
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
    with open(args.config) as f:
        config = json.load(f)

    calibration = warp_calibrate(args.h5_file, config, args.verbosity)

    # Duplicate warp calibration for specified pair of stream with the same sensor, often the case
    # in cameras with a depth stream created from infrared (NIR) sensor(s).
    if "duplicate_calibration" in config.keys():
        for stream, duplicate_stream in config["duplicate_calibration"].items():
            calibration[duplicate_stream] = calibration[stream]

    # If there is a configuration to update: we load it and update the markers
    # fields of the cameras
    if args.update_calibration is not None:
        with open(args.update_calibration) as calib_f:
            to_update_calib = json.load(calib_f)
        calibration = update_calibration(calibration, to_update_calib)

    # If not we still add some keys to the calibration dictionnary to comply
    # with what bob.ip.stereo expects.
    else:
        calibration = fill_calibration(calibration, args.reference)

    print(calibration)
    if args.output_file is not None:
        with open(args.output_file, "w") as f:
            json.dump(calibration, f, indent=4, sort_keys=True)
        print("{} written.".format(args.output_file))


if __name__ == "__main__":
    main()
