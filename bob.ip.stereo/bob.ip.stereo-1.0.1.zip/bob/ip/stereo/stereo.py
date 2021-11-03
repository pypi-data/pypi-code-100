#!/usr/bin/env python
#==============================================================================

import numpy as np
import cv2 as cv

import datetime

import bob.io.image
import bob.ip.color

from .camera import Camera, CameraPair
from .parameters import StereoParameters
from .utils import convert_to_uint8
from ._library import remap, project_map, project_bounding_box, project_image_points

#==============================================================================

def stereo_match(img_l, img_r, camera_pair, stereo_parameters=StereoParameters()):
    """ This function performs stereo reconstruction on a pair of images.
    
        The reconstruction process begins by converting the input image pair to 
        grayscale and then rectifying them using the :class:`~bob.ip.stereo.CameraPair` 
        object, if requested a 2x downscaling is also performed. Image disparity is then 
        computed accordingly to the algorithm and parameters described in the
        :class:`~bob.ip.stereo.StereoParameters` object, if requested in these options voids 
        in the resulting disparity map are filled using an in-painting algorithm. 
        Finally, the disparity map is converted to a 3D map using geometric 
        information from the :class:`~bob.ip.stereo.CameraPair` object.

        Parameters
        ----------
        img_l : :obj:`numpy.ndarray`
            Left image.
        img_r : :obj:`numpy.ndarray`
            Right image.
        camera_pair : :obj:`~bob.ip.stereo.CameraPair`
            Camera pair object containing geometric information of the cameras.
        stereo_parameters: :obj:`~bob.ip.stereo.StereoParameters`
            Parameters for the stereo reconstruction algorithm.

        Returns
        -------
        :obj:`numpy.ndarray`
            The resulting 3D reconstructed scene.
    """

    # convert to gray

    if len(img_l.shape) == 3:
        if img_l.shape[0] == 1:
            img_l = img_l[0]
        else:
            img_l = bob.ip.color.rgb_to_gray(img_l)
    if len(img_r.shape) == 3:
        if img_r.shape[0] == 1:
            img_r = img_r[0]
        else:
            img_r = bob.ip.color.rgb_to_gray(img_r)

    # assert shape

    assert img_l.shape[0] == img_r.shape[0]
    assert img_l.shape[1] == img_r.shape[1]

    # rectify

    img_l, img_r, Q = camera_pair.stereo_rectify(img_l, img_r)

    # downscale & normalize

    if stereo_parameters.downscale:
        img_l = cv.pyrDown(img_l)
        img_r = cv.pyrDown(img_r)

    img_l = convert_to_uint8(img_l, stereo_parameters.normalize)
    img_r = convert_to_uint8(img_r, stereo_parameters.normalize)

    #block match

    if stereo_parameters.algorithm == stereo_parameters.STEREO_CV_SGBM:

        stereo = cv.StereoSGBM_create(minDisparity      = stereo_parameters.min_disparity,
                                      numDisparities    = stereo_parameters.num_disparities,
                                      blockSize         = stereo_parameters.block_size,
                                      P1                = stereo_parameters.p1,
                                      P2                = stereo_parameters.p2,
                                      disp12MaxDiff     = stereo_parameters.disp12_max_diff,
                                      uniquenessRatio   = stereo_parameters.uniqueness_ratio,
                                      speckleWindowSize = stereo_parameters.speckle_window_size,
                                      speckleRange      = stereo_parameters.speckle_range,
                                      mode              = stereo_parameters.sgbm_mode)


        disparity = stereo.compute(img_l,img_r)

        disparity = disparity.astype('float32')/16.0

    else:

        raise Exception('Unknown stereo algorithm')

    # inpaint depth map holes

    if stereo_parameters.erode:
        
        kernel = np.ones((5,5), np.uint8) 
        disparity = cv.erode(disparity, kernel, iterations=3) 

    if stereo_parameters.inpaint:

        min_disp = np.amin(disparity)
        mask = np.where(disparity == min_disp , 1, 0).astype(np.uint8)

        #disparity = cv.inpaint(disparity, mask, 3, cv.INPAINT_TELEA)
        disparity = cv.inpaint(disparity, mask, 3, cv.INPAINT_NS)

    # upscale

    if stereo_parameters.downscale:
        disparity = cv.pyrUp(disparity)
        disparity = disparity*2

    # convert to 3d

    img3d = cv.reprojectImageTo3D(disparity, Q)

    # convert to <xyz, h, w> format

    img3d = np.rollaxis(img3d, 2)

    return img3d

#==============================================================================

def reproject_image(img, img3d, camera, camera_pair, bounding_box=None, image_points=None):
    """ This function projects a camera view at any point in 3D space on the 3D point
        cloud obtained by stereo reconstruction and re-project back on the left camera
        view, thus allowing for instance precise alignment of an RGB camera on the 
        3D stereo image.

        This process works in two steps. In a first stage the 3D point cloud is projected 
        on the camera view to be re-mapped, taking into account the distortion of this 
        particular camera, yielding a mapping from the left rectified 2D coordinates to the 
        camera under consideration 2D view. In a second stage this mapping is inverted and the 
        image is re-mapped to the left rectified view. The resolution of the source image is 
        automatically rescaled to match the resolution of the stereo view. In addition, it is
        possible to transform a bounding box object and an arbitrary number of image points
        (for instance an object bounding box and landmarks on the original 2D image). 


        Parameters
        ----------
        img : :obj:`numpy.ndarray`
            Image to be re-projected (int8, int16 and float64 are supported).
        img3d : :obj:`numpy.ndarray`
            3D image (point cloud) of the scene.
        camera : :obj:`~bob.ip.stereo.Camera`
            Camera object containing geometric information of the camera to be re-projected.
        camera_pair : :obj:`~bob.ip.stereo.CameraPair`
            Camera pair object containing geometric information of the stereo cameras.
        bounding_box : :obj:`numpy.ndarray`
            2x2 numpy array [[top, bottom], [left, right]] bounding box (int64), the array is 
            modified by the functions.
        image_point : :obj:`numpy.ndarray`
            Nx2 numpy array containing coordinates of the image points, the array is modified by 
            the function.

        Returns
        -------
        :obj:`numpy.ndarray`
            The resulting reprojected image.
    """

    # shape

    img_dim0 = img.shape[1]
    img_dim1 = img.shape[2]

    map_dim0 = img3d.shape[1]
    map_dim1 = img3d.shape[2]

    # transformations

    RL, RR, PL, PR, Q = camera_pair.get_rectification_matrices(map_dim0, map_dim1)

    r_mat = RL.T.dot(camera.R)
    t_vec = camera.T[:,0]

    # allocate 

    image = np.zeros((img.shape[0], map_dim0, map_dim1), dtype=img.dtype)
    u_map = np.zeros((map_dim0,map_dim1), dtype='uint16')
    v_map = np.zeros((map_dim0,map_dim1), dtype='uint16')

    # project
    # Opencv's dist_coefs is list of list. 1st element of 1st list is the dist_coeffs we need.
    project_map(u_map, v_map, img3d, r_mat, t_vec, camera.camera_matrix, camera.dist_coeffs[0], img_dim0, img_dim1)

    # remap image

    remap(img, image, u_map, v_map)

    # bounding box

    if bounding_box is not None:
        assert bounding_box.dtype == 'int64'
        assert bounding_box.shape[0] == 2
        assert bounding_box.shape[1] == 2
        project_bounding_box(u_map, v_map, bounding_box)

    # image points

    if image_points is not None:
        assert image_points.dtype == 'float64'
        assert image_points.shape[1] == 2
        u_inv = np.empty_like(u_map)
        v_inv = np.empty_like(v_map)
        project_image_points(u_map, v_map, u_inv, v_inv, image_points)

    return image


# original python implementation for reference
def __get_reprojected_stream_original(img, img3d, camera_pair, R, T, camera_matrix, dist_coeffs):

    # shape

    img_dim0 = img.shape[1]
    img_dim1 = img.shape[2]

    map_dim0 = img3d.shape[1]
    map_dim1 = img3d.shape[2]

    # transformation matrices

    RL, RR, PL, PR, Q = camera_pair.get_rectification_matrices(map_dim0, map_dim1)

    # arrays

    image = np.zeros((  img.shape[0], 
                        map_dim0,
                        map_dim1),
                    dtype=img.dtype)
    xyz = np.zeros((map_dim0*map_dim1,3))

    def kuv(u,v):
        return v  + u * map_dim1

    for u in range(map_dim0):
        for v in range(map_dim1):
            xyz[kuv(u,v),:] = img3d[:,u,v]

    rvec, _ = cv.Rodrigues(RL.T.dot(R))

    uv,_ =cv.projectPoints(objectPoints = xyz, rvec=rvec, tvec=T, cameraMatrix=camera_matrix, distCoeffs=dist_coeffs)

    for u in range(map_dim0):
        for v in range(map_dim1):
            k = kuv(u,v)
            u_new = int(uv[k, 0, 1])    
            v_new = int(uv[k, 0, 0])
            if u_new >= 0 and u_new < img_dim0 and v_new >= 0 and v_new < img_dim1:
                image[:,u,v] = img[:,u_new, v_new]

    return image

# script entry point
def main():
    import argparse
    import pkg_resources

    def parse_arguments():

        default_config = pkg_resources.resource_filename('batl.utils',
                                                         'config/idiap_st3_config.json')
        parser = argparse.ArgumentParser(description=__doc__)

        parser.add_argument("-l", "--left-image", type=str, help="Left PNG image for stereo.")
        parser.add_argument("-r", "--right-image", type=str, help="Right PNG image for stereo.")
        parser.add_argument("-o", "--output-image", type=str, help="RGB output PNG image of stereo point cloud.")
        return parser.parse_args()

    args = parse_arguments()

    im_left     = bob.io.image.load(args.left_image)
    im_right    = bob.io.image.load(args.right_image)

    im_out      = stereo_match(im_left, im_right, CameraPair())

    # rescale and write file

    for i in range(3):
        im_out[i,:,:] -= im_out[i,:,:].min()
        im_out[i,:,:] *= (255.0/im_out[i,:,:].max())

    bob.io.image.save(im_out.astype('uint8'), args.output_image)


#==============================================================================
if __name__ == "__main__":
    main()


