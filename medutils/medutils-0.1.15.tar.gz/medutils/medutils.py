# -*- coding: utf-8 -*-
"""
Possible functions on loading, saving, processing itk files.
=============================================================
Created on Tue Apr  4 09:35:14 2017
@author: fferreira and Jingnan
"""

import csv
import glob
import os
import threading

import SimpleITK as sitk
import numpy as np
import pandas as pd
import pingouin as pg
from scipy import ndimage


def appendrows_to(fpath: str, data: np.ndarray, head=None):
    if not os.path.isfile(fpath) and head is not None:
        with open(fpath, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(head)

    with open(fpath, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        if len(data.shape) == 1:  # when data.shape==(-1,)  which means data batch size = 1
            writer.writerow(data)
            # data = data.reshape(-1, 1)
        else:
            writer.writerows(data)



def icc(label_fpath, pred_fpath):
    icc_dict = {}

    label = pd.read_csv(label_fpath)
    pred = pd.read_csv(pred_fpath)
    if 'ID' == label.columns[0]:
        del label["ID"]
    if "Level" == label.columns[0]:
        del label["Level"]
    if 'ID' == pred.columns[0]:
        del pred["ID"]
    if "Level" == pred.columns[0]:
        del pred["Level"]
    original_columns = label.columns

    # if len(label.columns) == 3:
    #     columns = ['disext', 'gg', 'retp']
    # elif len(label.columns) == 5:
    #     columns = ['L1', 'L2', 'L3', 'L4', 'L5']
    # else:
    #     raise Exception('wrong task')

    # label.columns = columns
    # pred.columns = columns
    ori_columns = list(label.columns)

    label['ID'] = np.arange(1, len(label) + 1)
    label['rater'] = 'label'

    pred['ID'] = np.arange(1, len(pred) + 1)
    pred['rater'] = 'pred'

    data = pd.concat([label, pred], axis=0)

    for column in original_columns:
        icc = pg.intraclass_corr(data=data, targets='ID', raters='rater', ratings=column).round(2)
        icc = icc.set_index("Type")
        icc = icc.loc['ICC2']['ICC']
        prefix = label_fpath.split("/")[-1].split("_")[0]
        icc_dict['icc_' + prefix + '_' + column] = icc

    column = "combined"
    label_all = pd.DataFrame(dtype='float')
    pred_all = pd.DataFrame(dtype='float')

    pred_all['combined'] = pd.concat([pred[i] for i in ori_columns], axis=0).astype(float)
    label_all['combined'] = pd.concat([label[i] for i in ori_columns], axis=0).astype(float)

    label_all['ID'] = np.arange(1, len(label_all) + 1)
    label_all['rater'] = 'label'

    pred_all['ID'] = np.arange(1, len(pred_all) + 1)
    pred_all['rater'] = 'pred'

    data_all = pd.concat([label_all, pred_all], axis=0)
    icc = pg.intraclass_corr(data=data_all, targets='ID', raters='rater', ratings=column).round(2)
    icc = icc.set_index("Type")
    icc = icc.loc['ICC2']['ICC']
    prefix = label_fpath.split("/")[-1].split("_")[0]
    icc_dict['icc_all' + prefix + '_' + column] = icc
    return icc_dict


def count_parameters(model):
    total_params = 0
    for name, parameter in model.named_parameters():
        if not parameter.requires_grad:
            continue
        param = parameter.numel()
        total_params += param
    print(f"Total Trainable Params: {total_params}")
    return total_params


def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x


def get_all_ct_names(path, number=None, prefix=None, name_suffix=None):
    suffix_list = [".nrrd", ".mhd", ".mha", ".nii", ".nii.gz"]  # todo: more suffix

    if prefix and name_suffix:
        files = glob.glob(path + '/' + prefix + "*" + name_suffix + suffix_list[0])
        for suffix in suffix_list[1:]:
            files.extend(glob.glob(path + '/' + prefix + "*" + name_suffix + suffix))
    elif prefix:
        files = glob.glob(path + '/' + prefix + "*" + suffix_list[0])
        for suffix in suffix_list[1:]:
            files.extend(glob.glob(path + '/' + prefix + "*" + suffix))
    elif name_suffix:
        if 'SSc' in path:
            files = glob.glob(path + '/*/' + "*" + name_suffix + '.mha')
        else:
            files = glob.glob(path + '/' + "*" + name_suffix + suffix_list[0])
            for suffix in suffix_list[1:]:
                files.extend(glob.glob(path + '/' + "*" + name_suffix + suffix))

    else:
        files = glob.glob(path + '/*' + suffix_list[0])
        for suffix in suffix_list[1:]:
            files.extend(glob.glob(path + '/*' + suffix))

    scan_files = sorted(files)
    if len(scan_files) == 0:
        raise Exception(f'Scan files are None, please check the data directory: {path}')
    if isinstance(number, int) and number != 0:
        scan_files = scan_files[:number]
    elif isinstance(number, list):  # number = [3,7]
        scan_files = scan_files[number[0]:number[1]]

    return scan_files


def get_ct_pair_filenames(gdth_path, pred_path):
    gdth_files = get_all_ct_names(gdth_path)
    pred_files = get_all_ct_names(pred_path)

    if len(gdth_files) == 0:
        raise Exception('ground truth files  are None, Please check the directories: ', gdth_path)
    if len(pred_files) == 0:
        raise Exception('predicted files are None, Please check the directories: ', pred_path)

    # if any(['fissure' in file for file in pred_files]):  # check no fissure files are included
    #     fissure_gdth, fissure_pred = get_fissure_filenames(gdth_path, pred_path)
    #     gdth_files = set(gdth_files) - set(fissure_gdth)
    #     pred_files = set(pred_files) - set(fissure_pred)
    gdth_files, pred_files = get_intersection_files(gdth_files, pred_files)

    return gdth_files, pred_files


def recall(seg, gt):
    im1 = np.asarray(seg > 0).astype(np.bool)
    im2 = np.asarray(gt > 0).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError(f"Shape mismatch: im1 and im2 must have the same shape, but the im1.shape is {im1.shape} and "
                         f"im2.shape is {im2.shape}")

    intersection = np.logical_and(im1, im2).astype(float)

    if im2.sum() > 0:
        return intersection.sum() / (im2.sum())
    else:
        return 1.0


def get_fissure_filenames(gdth_path, pred_path, fissureradius=0):
    if fissureradius:  # if given fissure radius, then get all ct names with specific fissure radius
        gdth_files = get_all_ct_names(gdth_path, prefix="fissure_" + str(fissureradius))
        pred_files = get_all_ct_names(pred_path, prefix="fissure_" + str(fissureradius))
    else:  # else, get all ct names no matter the radius is
        gdth_files = get_all_ct_names(gdth_path, prefix="fissure")
        pred_files = get_all_ct_names(pred_path, prefix="fissure")
    gdth_files, pred_files = get_intersection_files(gdth_files, pred_files)

    return gdth_files, pred_files


def get_intersection_files(gdth_files, pred_files):
    gdth_files = list(gdth_files)
    pred_files = list(pred_files)
    file_list_gdth = []
    gdth_idx_list = []
    for i, gdth_file in enumerate(gdth_files):
        base = os.path.basename(gdth_file)
        file, ext = os.path.splitext(base)
        file_list_gdth.append(file)
        gdth_idx_list.append(i)

    file_list_pred = []
    pred_idx_list = []
    for j, pred_file in enumerate(pred_files):
        base = os.path.basename(pred_file)
        file, ext = os.path.splitext(base)
        file_list_pred.append(file)
        pred_idx_list.append(j)

    intersection = set(file_list_gdth) & set(file_list_pred)

    new_gdth_files = []
    new_pred_files = []
    for inter in intersection:
        i = file_list_gdth.index(inter)
        j = file_list_pred.index(inter)
        new_gdth_files.append(gdth_files[i])
        new_pred_files.append(pred_files[j])

    return sorted(new_gdth_files), sorted(new_pred_files)


def get_gdth_pred_names(gdth_path, pred_path):
    # if fissure:
    #     gdth_files, pred_files = get_fissure_filenames(gdth_path, pred_path, fissureradius=fissureradius)
    # else:
    gdth_files, pred_files = get_ct_pair_filenames(gdth_path, pred_path)

    return gdth_files, pred_files


def load_itk(filename, require_ori_sp=False):
    """

    :param filename: absolute file path
    :return: ct, origin, spacing, all of them has coordinate (z,y,x) if filename exists. Otherwise, 3 empty list.
    """
    #     print('start load data')
    # Reads the image using SimpleITK
    if os.path.isfile(filename):
        itkimage = sitk.ReadImage(filename)

    else:
        raise FileNotFoundError("image" + filename+ " was not found")

    # Convert the image to a  numpy array first ands then shuffle the dimensions to get axis in the order z,y,x
    ct_scan = sitk.GetArrayFromImage(itkimage)

    # ct_scan[ct_scan>4] = 0 #filter trachea (label 5)
    # Read the origin of the ct_scan, will be used to convert the coordinates from world to voxel and vice versa.
    origin = np.array(list(reversed(itkimage.GetOrigin())))  # note: after reverseing, origin=(z,y,x)

    # Read the spacing along each dimension
    spacing = np.array(list(reversed(itkimage.GetSpacing())))  # note: after reverseing,  spacing =(z,y,x)
    orientation = itkimage.GetDirection()
    if orientation[-1] == -1:
        ct_scan = ct_scan[::-1]
    if require_ori_sp:
        return ct_scan, origin, spacing
    else:
        return ct_scan
    

# %%
def save_itk(filename, scan, origin, spacing, dtype='int16'):
    """
    Save a array to itk file.

    :param filename: saved file name, a string.
    :param scan: scan array, shape(z, y, x)
    :param origin: origin of itk file, shape (z, y, x)
    :param spacing: spacing of itk file, shape (z, y, x)
    :param dtype: 'int16' default
    :return: None
    """
    stk = sitk.GetImageFromArray(scan.astype(dtype))
    # origin and spacing 's coordinate are (z,y,x). but for image class,
    # the order shuld be (x,y,z), that's why we reverse the order here.
    stk.SetOrigin(origin[::-1])
    # numpy array is reversed after convertion from image, but origin and spacing keep unchanged
    stk.SetSpacing(spacing[::-1])

    sitk.WriteImage(stk, filename, useCompression=True)

    # writer = sitk.ImageFileWriter()
    # writer.SetFileName(filename)
    # writer.Execute(stk)


# %%
def normalize(image, min_=-1000.0, max_=400.0):
    """
    Set the values to [0~1].

    :param image: image array
    :param min_: bottom
    :param max_: top
    :return: convert ct scan to 0~1
    """
    image = (image - min_) / (max_ - min_)
    image[image > 1] = 1.
    image[image < 0] = 0.

    return image


def one_hot_decoding(img, labels, thresh=None):
    """
    get the one hot decode of img.

    :param img:
    :param labels:
    :param thresh:
    :return:
    """
    new_img = np.zeros((img.shape[0], img.shape[1]))
    r_img = img.reshape(img.shape[0], img.shape[1], -1)

    aux = np.argmax(r_img, axis=-1)
    for i, l in enumerate(labels[1::]):
        if thresh is None:
            new_img[aux == (i + 1)] = l
        else:
            new_img[r_img[:, :, i + 1] > thresh] = l

    return new_img


def downsample(scan, is_mask=False, ori_space=None, trgt_space=None, ori_sz=None, trgt_sz=None, order=1, labels=None):
    """

    :param labels: used for advanced downsample when order = 1 for is_mask
    :param is_mask: mask have smooth upsampling
    :param scan: shape(z,y,x,chn)
    :param ori_space: shape(z,y,x)
    :param trgt_space: shape(z,y,x)
    :param ori_sz: shape(z,y,x,chn)
    :param trgt_sz: shape(z,y,x)
    :param order:
    :return:
    """
    if trgt_sz is None:
        trgt_sz = []
    if ori_sz is None:
        ori_sz = []

    if labels is None:
        labels = [1]
    trgt_sz = list(trgt_sz)
    ori_sz = list(ori_sz)
    if len(scan.shape) == 3:  # (657, 512, 512)
        scan = scan[..., np.newaxis]  # (657, 512, 512, 1)
    if len(ori_sz) == 3:
        ori_sz.append(1)  # (657, 512, 512, 1)
    if len(trgt_sz) == 3:
        trgt_sz.append(1)  # (657, 512, 512, 1)
    print('scan.shape, ori_space, trgt_space, ori_sz, trgt_sz', scan.shape, ori_space, trgt_space, ori_sz, trgt_sz)
    if any(trgt_space):
        print('rescaled to new spacing  ')
        zoom_seq = np.array(ori_space, dtype='float') / np.array(trgt_space, dtype='float')
        zoom_seq = np.append(zoom_seq, 1)
    elif any(trgt_sz):
        print('rescaled to target size')
        zoom_seq = np.array(trgt_sz, dtype='float') / np.array(ori_sz, dtype='float')
    else:
        raise Exception('please assign how to rescale')

    print('zoom_seq', zoom_seq)

    if is_mask is True and order == 1 and len(labels) > 2:
        # multi labels and not nearest neighbor, seperate each label and do interpolation
        x_onehot = one_hot_encode_3d(scan, labels)  # (657, 512, 512, 6/2)
        mask1 = []
        for i in range(x_onehot.shape[-1]):
            one_chn = x_onehot[..., i]  # (657, 512, 512)
            one_chn = one_chn[..., np.newaxis]  # (657, 512, 512, 1)
            x1 = ndimage.interpolation.zoom(one_chn, zoom_seq, order=order, prefilter=order)
            mask1.append(x1[..., 0])
        mask1 = np.array(mask1)  # (6/2, 567, 512, 512)
        mask1 = np.rollaxis(mask1, 0, start=4)  # (567, 512, 512, 6/2)
        mask3 = []
        for p in mask1:  # p.shape (512, 512, 6/2)
            mask3.append(one_hot_decoding(p, labels))  # p.shape (512, 512)
        x = np.array(mask3, dtype='uint8')  # (567, 512, 512)
        x = x[..., np.newaxis]  # (567, 512, 512, 1)
    else:  # [0, 1] vesel mask or original ct scans, or onhoted mask
        x = ndimage.interpolation.zoom(scan, zoom_seq, order=order, prefilter=order)  # (143, 271, 271, 1)
        # x = x[..., 0]

    print('size after rescale:', x.shape)  # 64, 144, 144, 1
    if any(zoom_seq > 1):  # correct shape is not neessary during down sampling in training,
        # because in training we only have the requirement on spacing
        x = correct_shape(x, trgt_sz)  # correct the shape mistakes made by sampling

    return x


def one_hot_encode_3d(patch, labels):
    """

    :param patch: 3 or 4 or 5 dimensions
    :param labels: a list
    :return: 3 or 4 dimension input are conveted to 4 dimensions, 5 dimensions are converted to 5 dimensions.
    """

    # todo: simplify this function

    # assert len(patch.shape)==5 # (5, 128, 128, 64, 1)
    labels = np.array(labels)  # i.e. [0,4,5,6,7,8]
    if len(patch.shape) == 5 and patch.shape[-1] == 1:  # (5, 128, 128, 64, 1)
        patch = np.reshape(patch, (patch.shape[0], patch.shape[1], patch.shape[2], patch.shape[3]))
    elif len(patch.shape) == 4 and patch.shape[-1] == 1:  # (128, 128, 64, 1)
        patch = np.reshape(patch, (patch.shape[0], patch.shape[1], patch.shape[2]))
    patches = []
    # print('patch.shape', patch.shape)
    for i, l in enumerate(labels):
        a = np.where(patch != l, 0, 1)
        patches.append(a)

    patches = np.array(patches)
    patches = np.rollaxis(patches, 0, len(patches.shape))  # from [6, 64, 128, 128] to [64, 128, 128, 6]

    return np.float64(patches)


def save_model_best(dice_file, segment, model_fpath):
    with open(dice_file, 'r', newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        dice_list = []
        for row in reader:
            print(row)
            dice = float(row['ave_total'])  # str is the default type from csv
            dice_list.append(dice)
    max_dice = max(dice_list)
    if dice >= max_dice:
        segment.save(model_fpath)
        print("this 'ave_total' is the best: ", str(dice), "save valid model at: ", model_fpath)
    else:
        print("this 'ave_total' is not the best: ", str(dice), 'we do not save the model')

    return max_dice


def correct_shape(final_pred, original_shape):
    """

    :param final_pred:  must be 3 dimensions
    :param original_shape:
    :return:
    """
    print('after rescale, the shape is: ', final_pred.shape)
    if final_pred.shape[0] != original_shape[0]:

        nb_slice_lost = abs(original_shape[0] - final_pred.shape[0])

        if original_shape[0] > final_pred.shape[0]:
            print(
                'there are {} slices lost along z axis, they will be repeated by the last slice'.format(nb_slice_lost))
            for i in range(nb_slice_lost):
                added_slice = np.expand_dims(final_pred[-1], axis=0)
                final_pred = np.concatenate((final_pred, added_slice))
            print('after repeating, the shape became: ', final_pred.shape)
        else:
            print('there are {} slices more along z axis, they will be cut'.format(nb_slice_lost))
            final_pred = final_pred[:original_shape[0]]  # original shape: (649, 512, 512)
            print('after cutting, the shape became: ', final_pred.shape)

    if final_pred.shape[1] != original_shape[1]:

        nb_slice_lost = abs(original_shape[1] - final_pred.shape[1])

        if original_shape[1] > final_pred.shape[1]:
            print('there are {} slices lost along x,y axis, they will be repeated by the last slice'.format(
                nb_slice_lost))
            for i in range(nb_slice_lost):
                added_slice = final_pred[:, -1, :]
                added_slice = np.expand_dims(added_slice, axis=1)
                print('x axis final_pred.shape', final_pred.shape)
                print('x axis add_slice.shape', added_slice.shape)
                final_pred = np.concatenate((final_pred, added_slice), axis=1)
                print('after first repeating, the shape is: ', final_pred.shape)

                added_slice = np.expand_dims(final_pred[:, :, -1], axis=2)
                print('y axis final_pred.shape', final_pred.shape)
                print('y axis add_slice.shape', added_slice.shape)
                final_pred = np.concatenate((final_pred, added_slice), axis=2)
            print('after repeating, the shape became: ', final_pred.shape)
        else:
            print('there are {} slices more along x,y axis, they will be cut'.format(nb_slice_lost))
            final_pred = final_pred[:, :original_shape[1], :original_shape[1]]  # original shape: (649, 512, 512)
            print('after cutting, the shape became: ', final_pred.shape)
    return final_pred


def execute_the_function_multi_thread(consumer, workers=10):
    """
    :param consumer: function to be multi-thread executed
    :param workers:
    :return:
    """
    thd_list = []
    mylock = threading.Lock()
    for i in range(workers):
        thd = threading.Thread(target=consumer, args=(mylock,))
        thd.start()
        thd_list.append(thd)

    for thd in thd_list:
        thd.join()
