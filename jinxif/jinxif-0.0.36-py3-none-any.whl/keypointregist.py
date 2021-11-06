#####
# code adapted from chandler gatenbee and brian white
# https://github.com/IAWG-CSBC-PSON/registration-challenge
#####
# 
# Guillaume 20210427: commented in the email 'python image registration code' 
# about applying Chandler Gatenbee and Brian White's code.
#
# for python registration I used:
# + SIFT
#     - cv2.SIFT_create()
#     - I extract the features kp1, desc1 = SIFT.detectAndCompute(moving, None)
# + match the features:
#     - matcher = cv2.BFMatcher(normType=cv2.NORM_L2, crossCheck=True)
#     - matches = matcher.match(desc1, desc2)
# + find homography:
#     - H, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, ransacReprojThreshold=10)
#     - Estimate the transformation
#     - transformer.estimate(moving_pts, target_pts)
# + make the final transform
#    - transform.warp(moving, transformer.inverse, output_shape=output_shape_rc)
#
# most of it if from the hackathon, but I normalize the images first (they didn't do) and then use SIFT.
# the last part is the bottleneck and makes the entire code useless.
#
# So I'm testing some of the libraries listed here: http://pyimreg.github.io
#
#####

# library
import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
from skimage import io, transform, util

# development
#import importlib
#importlib.reload()


# function
def _keypoint_distance(target_pts, moving_pts, img_h, img_w):
    '''
    :calculate mean moving to target keypoint distance.
    :return:
    '''
    dst = np.sqrt(np.sum((moving_pts - target_pts)**2, axis=1)) / np.sqrt(img_h**2 + img_w**2)
    return(np.mean(dst))


def _match_keypoints(ai_img_target, ai_img_moving, feature_detector):
    '''
    :param ai_img_target: image to which the moving image will be aligned
    :param ai_img_moving: image that is to be warped to align with target image
    :param feature_detector: a feature detector from opencv
    :return:
    '''

    kp1, desc1 = feature_detector.detectAndCompute(ai_img_moving, None)
    kp2, desc2 = feature_detector.detectAndCompute(ai_img_target, None)

    matcher = cv2.BFMatcher(normType=cv2.NORM_L2, crossCheck=True)
    matches = matcher.match(desc1, desc2)

    src_match_idx = [m.queryIdx for m in matches]
    dst_match_idx = [m.trainIdx for m in matches]

    src_points = np.float32([kp1[i].pt for i in src_match_idx])
    dst_points = np.float32([kp2[i].pt for i in dst_match_idx])

    H, mask = cv2.findHomography(src_points, dst_points, cv2.RANSAC, ransacReprojThreshold=10)

    good = [matches[i] for i in np.arange(0, len(mask)) if mask[i] == [1]]

    filtered_src_match_idx = [m.queryIdx for m in good]
    filtered_dst_match_idx = [m.trainIdx for m in good]

    filtered_src_points = np.float32([kp1[i].pt for i in filtered_src_match_idx])
    filtered_dst_points = np.float32([kp2[i].pt for i in filtered_dst_match_idx])

    return(filtered_src_points, filtered_dst_points)


def apply_transform(ai_img_target, ai_img_moving, target_pts, moving_pts, transformer, output_shape_rc=None):
    '''
    :param transformer: transformer object from skimage. See https://scikit-image.org/docs/dev/api/skimage.transform.html for different transformations
    :param output_shape_rc: shape of warped image (row, col). If None, uses shape of target image
    :return:
    '''
    if output_shape_rc is None:
        output_shape_rc = ai_img_target.shape[:2]

    if str(transformer.__class__) == "<class 'skimage.transform._geometric.PolynomialTransform'>":
        transformer.estimate(target_pts, moving_pts)
        ai_img_warped = transform.warp(ai_img_moving, transformer, output_shape=output_shape_rc)

        ### Restimate to warp points
        transformer.estimate(moving_pts, target_pts)
        warped_pts = transformer(moving_pts)
    else:
        transformer.estimate(moving_pts, target_pts)
        ai_img_warped = transform.warp(ai_img_moving, transformer.inverse, output_shape=output_shape_rc)
        warped_pts = transformer(moving_pts)

    ai_img_warped = util.img_as_ubyte(ai_img_warped)
    #ai_img_warped = util.img_as_uint(ai_img_warped)
    return(ai_img_warped, warped_pts)


def register(ai_img_target, ai_img_moving, s_pathfile_qcplot='QC/RegistrationPlots/qc_registration_rigid_align.png'):
    '''
    version: 2021-10-29

    input:
        ai_img_target: as numpy array loaded image.
            load like this: util.img_as_ubyte(util.img_as_float(io.imread(s_target_file)))
        ai_img_moving: as numpy array loaded image. 
            load like this: util.img_as_ubyte(util.img_as_float(io.imread(s_moving_file)))
        s_path_qcplot: path to put registration qc plots. can be None.
            if None no qc plots will be generated.

    output:
        moving_pts: moving points object
        target_pts: target points object
        warped_pts: warped points object
        transformer: transformer object
        registartion qc plot, if s_path_qcplot not is None.

    description:
        main function to do keypoint registration.
    '''
    # registration
    # bue 20201112 jenny said, alternatively kaze can be used, though akaze is a superior feature detection algorithm.
    #fd = cv2.KAZE_create(extended=True)
    fd = cv2.AKAZE_create()
    moving_pts, target_pts = _match_keypoints(
        ai_img_target=ai_img_target, 
        ai_img_moving=ai_img_moving, 
        feature_detector=fd
    )

    transformer = transform.SimilarityTransform()

    ai_img_warped, warped_pts = apply_transform(
        ai_img_target=ai_img_target, 
        ai_img_moving=ai_img_moving, 
        target_pts=moving_pts, 
        moving_pts=moving_pts, 
        transformer=transformer
    )

    # qc plot
    if not (s_pathfile_qcplot is None):
        # get offset
        r_unaligned_offset = _keypoint_distance(target_pts=target_pts, moving_pts=moving_pts, img_h=ai_img_moving.shape[0], img_w=ai_img_moving.shape[1])
        r_aligned_offset = _keypoint_distance(target_pts=target_pts, moving_pts=warped_pts, img_h=ai_img_moving.shape[0], img_w=ai_img_moving.shape[1])

        # generate qc plot
        fig, ax = plt.subplots(2,2, figsize=(10,10))
        ax[0][0].imshow(ai_img_target)
        ax[0][0].imshow(ai_img_moving, alpha=0.5)
        ax[1][0].scatter(target_pts[:,0], -target_pts[:,1])
        ax[1][0].scatter(moving_pts[:,0], -moving_pts[:,1])
        ax[0][0].set_title(f"Unaligned offset: {r_unaligned_offset}")

        ax[0][1].imshow(ai_img_target)
        ax[0][1].imshow(ai_img_warped, alpha=0.5)
        ax[1][1].scatter(target_pts[:,0], -target_pts[:,1])
        ax[1][1].scatter(warped_pts[:,0], -warped_pts[:,1])
        ax[0][1].set_title(f"Aligned offset: {r_aligned_offset}")

        # save qc plot
        s_erase = s_pathfile_qcplot.split('/')[-1]
        s_path_qcplot = s_pathfile_qcplot.replace(s_erase,'')
        os.makedirs(s_path_qcplot, exist_ok=True)
        plt.savefig(s_pathfile_qcplot, format="png", facecolor='white')

    # output results
    return(ai_img_warped, target_pts, moving_pts, warped_pts, transformer)

