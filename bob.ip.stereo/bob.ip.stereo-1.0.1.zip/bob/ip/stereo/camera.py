import numpy as np
import cv2 as cv

import json

import bob.ip.color


#==============================================================================

def load_camera_config(filepath, camera_name=None):
    """ Load camera config from a JSON file."""
    camera_list = {}
    with open(filepath, 'r') as data_config_file:
        data_config = json.load(data_config_file)
        for name in data_config:
            camera_config   = data_config[name]
            camera_matrix   = np.array(camera_config['camera_matrix'])
            dist_coeffs     = np.array(camera_config['distortion_coefs'])
            R               = np.array(camera_config['relative_rotation'])
            T               = np.array(camera_config['relative_translation'])
            markers         = np.array(camera_config['markers'])

            camera_list[name] = Camera(camera_matrix, dist_coeffs, R, T, markers)
    if camera_name is not None:
        return camera_list[camera_name]
    else:
        return camera_list

#==============================================================================

class Camera:
    """ This class represents the camera view in 3D space together with its
        projection matrix and lens distortion. In addition, 4 marker points
        can be added to perform 2D perspective transformations.

        Attributes
        ----------
        camera_matrix : :obj:`numpy.ndarray`
            Camera projection matrix, according to OpenCV's standards.
        dist_coeffs : :obj:`numpy.ndarray`
            Distortion coefficeints, according to OpenCV's standards.
        R : :obj:`numpy.ndarray`
            Rotation matrix relative to left stereo camera.
        T : :obj:`numpy.ndarray`
            Translation vector relative to left stereo camera.
        markers : :obj:`numpy.ndarray`
            Four points in 2D image coordinates that can be maapped 
            to another set of four points in a different camera view.
    """

    def __init__(self, camera_matrix, dist_coeffs, R, T, markers):
        self.camera_matrix  = camera_matrix
        self.dist_coeffs    = dist_coeffs
        self.R              = R
        self.T              = T
        self.markers        = markers

#==============================================================================
 
class CameraPair:
    """ This class represents the camera view in 3D space together with its
        projection matrix and lens distortion. In addition, 4 marker points
        can be added to perform 2D perspective transformations.

        Attributes
        ----------
        camera_matrix : :obj:`numpy.ndarray`
            Camera projection matrix, according to OpenCV's standards.
        dist_coeffs : :obj:`numpy.ndarray`
            Distortion coefficeints, according to OpenCV's standards.
        R : :obj:`numpy.ndarray`
            Rotation matrix relative to left stereo camera.
        T : :obj:`numpy.ndarray`
            Translation vector relative to left stereo camera.
        markers : :obj:`numpy.ndarray`
            Four points in 2D image coordinates that can be maapped 
            to another set of four points in a different camera view.
    """

    def __init__(self, camera_left, camera_right):
        self.camera_matrix_l    = camera_left.camera_matrix
        self.camera_matrix_r    = camera_right.camera_matrix
        self.dist_coeffs_l      = camera_left.dist_coeffs
        self.dist_coeffs_r      = camera_right.dist_coeffs
        self.R                  = camera_right.R
        self.T                  = camera_right.T

    def get_rectification_matrices(self, dim0, dim1):
        RL, RR, PL, PR, Q, _, _ = cv.stereoRectify( self.camera_matrix_l, 
                                                    self.dist_coeffs_l, 
                                                    self.camera_matrix_r, 
                                                    self.dist_coeffs_r,  
                                                    (dim0, dim1), 
                                                    self.R,
                                                    self.T,
                                                    alpha=-1)
        return RL, RR, PL, PR, Q

    def stereo_rectify(self, img_l, img_r):
        RL, RR, PL, PR, Q = self.get_rectification_matrices(img_l.shape[0], img_l.shape[1])
        mapL1, mapL2 = cv.initUndistortRectifyMap(  self.camera_matrix_l, 
                                                    self.dist_coeffs_l, 
                                                    RL, 
                                                    PL, 
                                                    img_l.shape[::-1], 
                                                    cv.CV_32FC1)
        mapR1, mapR2 = cv.initUndistortRectifyMap(  self.camera_matrix_r, 
                                                    self.dist_coeffs_r, 
                                                    RR, 
                                                    PR, 
                                                    img_l.shape[::-1], 
                                                    cv.CV_32FC1)
        undistorted_rectifiedL = cv.remap(img_l, mapL1, mapL2, cv.INTER_LINEAR)
        undistorted_rectifiedR = cv.remap(img_r, mapR1, mapR2, cv.INTER_LINEAR)
        return undistorted_rectifiedL, undistorted_rectifiedR, Q
