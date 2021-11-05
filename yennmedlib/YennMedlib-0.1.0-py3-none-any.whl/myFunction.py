import SimpleITK as sitk
import nibabel as nib
import os
import shutil

import numpy as np

def convert_to_niigz():
    path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\VP"
    dst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\test"
    bmdst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\masknii_bm"
    vpdst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\masknii_vp"
    filenames = os.listdir(path)
    for i in filenames:
        f_path = os.path.join(path, i)
        img_head = sitk.ReadImage(f_path)
        #img_arr = sitk.GetArrayFromImage(img_head)
        #Selected_img = sitk.GetImageFromArray(img_arr)
        sitk.WriteImage(img_head, os.path.join(dst_path, i + ".nii"))


# remove file which contain the character "bm"
def remove_bmSuffix():
    path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\VP"
    dst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\test"
    bmdst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\masknii_bm"
    vpdst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\masknii_vp"
    filenames = os.listdir(path)
    for i in filenames:
        print(i)
        f_path = os.path.join(dst_path, i)
        f_dst_path = os.path.join(bmdst_path, i)
        if(i[-9:-7] == "BM"):
            print(f_path)
            os.remove(f_path)

# shuffle all data
def shuffle():
    image_path = r"F:\myData\HCCUS\images"
    label_path = r"F:\myData\HCCUS\labels"

    file_list = os.listdir(image_path)
    file_num = len(file_list)



#convert_to_niigz()

def print_image_list():
    imagepath = "/home/yexuehua/data/Task05_USHCC/imagesTr"
    labelpath = "/home/yexuehua/data/Task05_USHCC/labelsTr"

    filesimage = os.listdir(imagepath)
    fileslabel = os.listdir(labelpath)
    b = ""
    for i,j in zip(filesimage, fileslabel):
        a = ",{\"image\":\"./imagesTr/" + i + "\",\"label\":\"./labelsTr/" + j + "\"}"
        b = b+a
    print(b)

def print_test_list():
    imagepath = "/home/yexuehua/data/Task05_USHCC/imagesTs"
    labelpath = "/home/yexuehua/data/Task05_USHCC/labelsTs"

    filesimage = os.listdir(imagepath)
    fileslabel = os.listdir(labelpath)
    b = ""
    for i in filesimage:
        a = ",\"./imagesTs/" + i + "\""
        b = b + a
    print(b)

def copy_validation_file():
    folder_path = r"F:\code\nnunet\DataSet\nnUnet_raw\nnUNet_raw_data\Task008_HCCUS\labelsTr"
    dst_folder_path = r"F:\code\nnunet\DataSet\nnUnet_raw\nnUNet_raw_data\Task008_HCCUS\labelsValid"
    files_name_list = os.listdir(folder_path)
    valid_file = ['fanli_0', 'fanli_13', 'fanli_2', 'fanli_3', 'fanli_35', 'fanli_4', 'fanli_41', 'fanli_48', 'fanli_8', 'fanli_9', 'guzhen_10', 'guzhen_11', 'guzhen_12', 'guzhen_2', 'guzhen_21', 'guzhen_23', 'guzhen_24', 'guzhen_27', 'guzhen_28', 'guzhen_29', 'guzhen_3', 'guzhen_37', 'guzhen_5', 'guzhen_51', 'guzhen_52', 'guzhen_61', 'guzhen_62', 'guzhen_67', 'guzhen_71', 'guzhen_8', 'hanjinbiao1_11', 'hanjinbiao1_15', 'hanjinbiao1_16', 'hanjinbiao1_19', 'hanjinbiao1_27', 'hanjinbiao1_37', 'hanjinbiao1_41', 'hanjinbiao1_42', 'hanjinbiao1_48', 'hanjinbiao1_54', 'hanjinbiao1_58', 'hanjinbiao1_69', 'hanjinbiao1_75', 'hanjinbiao1_77', 'hanjinbiao1_84', 'hanjinbiao1_91', 'hanjinbiao1_92', 'lvshufeng_10', 'lvshufeng_14', 'lvshufeng_25', 'lvshufeng_26', 'lvshufeng_29', 'lvshufeng_3', 'lvshufeng_34', 'lvshufeng_36', 'lvshufeng_38', 'lvshufeng_4', 'lvshufeng_43', 'lvshufeng_53', 'lvshufeng_54', 'lvshufeng_6', 'lvshufeng_61', 'lvshufeng_62', 'lvshufeng_68', 'lvshufeng_70', 'lvshufeng_75', 'lvshufeng_81', 'panshuyi_0', 'wuzhixun_22', 'wuzhixun_28', 'wuzhixun_33', 'wuzhixun_34', 'wuzhixun_37', 'wuzhixun_42', 'wuzhixun_46', 'wuzhixun_57', 'wuzhixun_58', 'wuzhixun_59', 'wuzhixun_61', 'wuzhixun_66', 'wuzhixun_69', 'wuzhixun_73', 'wuzhixun_75', 'wuzhixun_83', 'yangjianfeng_10', 'yangjianfeng_15', 'yangjianfeng_19', 'yangjianfeng_24', 'yangjianfeng_29', 'yangjianfeng_41', 'yangjianfeng_42', 'yangjianfeng_5', 'yangjianfeng_50', 'yangjianfeng_56', 'yangjianfeng_62', 'yangjianfeng_63', 'yangjianfeng_64', 'yangsen_13', 'yangsen_16', 'yangsen_33', 'yangsen_34', 'yangsen_8']
    for f in valid_file:
        if f in valid_file:
            f_path = os.path.join(folder_path, f+".nii.gz")
            #f_path = os.path.join(folder_path, f + ".nii.gz")
            shutil.copy(f_path, dst_folder_path)
        #f_path = os.path.join(folder_path, f)

def move_specific_file():
    folder_path = r"C:\Users\212774000\Downloads\new_data\VP_BM_KF"
    dst_folder_path = r"F:\code\nnunet\DataSet\nnUnet_raw\nnUNet_raw_data\Task008_HCCUS\validTr"
    files_name_list = os.listdir(folder_path)
    for f in files_name_list:
        f_path = os.path.join(folder_path, f)
       # print(f)
        if f[-6:-4] == "vp":
            print(f)
            shutil.move(f_path, dst_folder_path)

def copy_specific_file():
    folder_path = r"C:\Users\212774000\Downloads\new_data\VP_BM_KF"
    dst_folder_path = r"F:\myData\HCCUS\2021-11-2\vplabels"
    files_name_list = os.listdir(folder_path)
    for f in files_name_list:
        f_path = os.path.join(folder_path, f)
       # print(f)
        if f[-6:-4] == "vp":
            print(f)
            shutil.copy(f_path, dst_folder_path)

def rename_niigz():
    imageTr_path = r"F:\myData\HCCUS\2021-11-2\vplabels"
    filesname = os.listdir(imageTr_path)
    for i in filesname:
        j = i[:-7] + ".nii.gz"
        os.renames(os.path.join(imageTr_path,i), os.path.join(imageTr_path,j))

def random_rename_niigz():
    image_folder = r"F:\myData\HCCUS\20211102ArrangedData\images"
    label_folder = r"F:\myData\HCCUS\20211102ArrangedData\labels"
    file_list = os.listdir(image_folder)
    file_num = len(file_list)
    random_num = np.random.choice(file_num, file_num, replace=False)
    for idx, i in enumerate(file_list):
        j = str(random_num[idx]) + ".nii.gz"
        os.renames(os.path.join(image_folder,i), os.path.join(image_folder,j))
        os.renames(os.path.join(label_folder, i), os.path.join(label_folder, j))

def extract_frame_from_DCEUS():
    folder_path = "/home/yexuehua/data/dynamic_image"
    label_path = "/home/yexuehua/data/dynamic_label"
    image_name_list = os.listdir(folder_path)
    label_name_list = os.listdir(label_path)
    for f in label_name_list:
        f_label_path = os.path.join(label_path, f)
        f_image_path = os.path.join(folder_path, f)
        image = sitk.ReadImage(f_image_path)
        label = sitk.ReadImage(f_label_path)
        extract_frames(image, label, f)

def extract_frames(image, label, filename):
    dst_image_path = "/home/yexuehua/data/frame_image"
    dst_label_path = "/home/yexuehua/data/frame_label"
    image_arr = sitk.GetArrayFromImage(image)
    label_arr = sitk.GetArrayFromImage(label)
    baseName = filename[:-4]
    i = 0
    for image_frame_rgb, label_frame in zip(image_arr, label_arr):
        if (np.max(label_frame)>0):
            image_frame = RGB2Gray(image_frame_rgb)
            image_frame_img = sitk.GetImageFromArray(image_frame)
            label_frame = np.expand_dims(label_frame, 0)
            label_frame_img = sitk.GetImageFromArray(label_frame)
            sitk.WriteImage(image_frame_img, os.path.join(dst_image_path, baseName + "_" + str(i) + ".nii.gz"))
            sitk.WriteImage(label_frame_img, os.path.join(dst_label_path, baseName + "_" + str(i) + ".nii.gz"))
            i = i+1

def RGB2Gray(img_arr):
    img_arr_r = img_arr[:, :, 0]
    img_arr_g = img_arr[:, :, 1]
    img_arr_b = img_arr[:, :, 2]
    img_arr_r = np.expand_dims(img_arr_r, 0)
    img_arr_g = np.expand_dims(img_arr_g, 0)
    img_arr_b = np.expand_dims(img_arr_b, 0)

    r_coe, g_coe, b_coe = 0.229, 0.587, 0.114
    # convert to gray
    return r_coe * img_arr_r + g_coe * img_arr_g + b_coe * img_arr_b


def convert_to_singlechannel():
    #path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\Image_Tr_backup"
    path = r"C:\Users\212774000\Desktop\yexuehua\Code\nnUNet-1-master\nnUNet-1-master\DataSet\nnUnet_raw\nnUNet_raw_data\Task05_USHCC\imagesTs"
    dst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\test"
    dst_r_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\image_single_channel\test\r"
    dst_g_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\image_single_channel\test\g"
    dst_b_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\image_single_channel\test\b"

    filenames = os.listdir(path)
    for i in filenames:
        f_path = os.path.join(path, i)
        img_head = sitk.ReadImage(f_path)
        print(img_head.GetDimension())
        print(img_head.GetSpacing())
        print(img_head.GetOrigin())
        print(img_head.GetDirection())
        img_arr = sitk.GetArrayFromImage(img_head)
        img_arr_r = img_arr[:, :, 0]
        img_arr_g = img_arr[:, :, 0]
        img_arr_b = img_arr[:, :, 0]
        img_arr_r = np.expand_dims(img_arr_r, 0)
        img_arr_g = np.expand_dims(img_arr_g, 0)
        img_arr_b = np.expand_dims(img_arr_b, 0)

        print(img_arr_r.shape)
        Selected_img_r = sitk.GetImageFromArray(img_arr_r)
        Selected_img_g = sitk.GetImageFromArray(img_arr_g)
        Selected_img_b = sitk.GetImageFromArray(img_arr_b)

        Selected_img_r.SetSpacing((1,1,1))
        Selected_img_r.SetOrigin((0, 0, 0))

        sitk.WriteImage(Selected_img_r, os.path.join(dst_r_path, i[:-7] + ".nii.gz"))
        sitk.WriteImage(Selected_img_g, os.path.join(dst_g_path, i[:-7] + "_g.nii.gz"))
        sitk.WriteImage(Selected_img_b, os.path.join(dst_b_path, i[:-7] + "_b.nii.gz"))


def convert_to_GrayChannel():

    path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\valid_image_niigz"
    dst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\valida_gray_image_niigz"
    filenames = os.listdir(path)

    for i in filenames:
        f_path = os.path.join(path, i)
        img_head = sitk.ReadImage(f_path)
        img_arr = sitk.GetArrayFromImage(img_head)
        img_arr_r = img_arr[:, :, 0]
        img_arr_g = img_arr[:, :, 1]
        img_arr_b = img_arr[:, :, 2]
        img_arr_r = np.expand_dims(img_arr_r, 0)
        img_arr_g = np.expand_dims(img_arr_g, 0)
        img_arr_b = np.expand_dims(img_arr_b, 0)

        r_coe, g_coe, b_coe = 0.229, 0.587, 0.114
        # convert to gray
        img_gray = r_coe * img_arr_r + g_coe * img_arr_g + b_coe * img_arr_b

        print(img_gray.shape)
        Saved_Gray_image = sitk.GetImageFromArray(img_gray)

        Saved_Gray_image.SetSpacing((1,1,1))
        Saved_Gray_image.SetOrigin((0, 0, 0))

        sitk.WriteImage(Saved_Gray_image, os.path.join(dst_path, i[:-7] + ".nii.gz"))


def convert_to_3modality():
    path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\Image_Tr_backup"
    dst_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\test"
    dst_r_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\image_single_channel\test\r"
    dst_g_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\image_single_channel\test\g"
    dst_b_path = r"C:\Users\212774000\Desktop\yexuehua\Data\DeepLearning_LiverHCC_Data_for_Segmentation\image_single_channel\test\b"

    filenames = os.listdir(path)
    for i in filenames:
        f_path = os.path.join(path, i)
        img_head = sitk.ReadImage(f_path)
        img_arr = sitk.GetArrayFromImage(img_head)
        # img_arr =
        # print(img_arr.shape)

def extract_EH_BMode():
    folder_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\image"
    label_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\label"
    image_name_list = os.listdir(folder_path)
    label_name_list = os.listdir(label_path)
    for f in label_name_list:
        f_label_path = os.path.join(label_path, f)
        f_image_path = os.path.join(folder_path, f)
        image = sitk.ReadImage(f_image_path)
        label = sitk.ReadImage(f_label_path)
        print(f)
        extract_EH_BMode_frames(image, label, f)

def extract_EH_BMode_frames(image, label, filename):
    dst_image_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\frame_EH_image"
    dst_label_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\frame_EH_label"
    dst_B_image_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\frame_B_image"
    dst_B_label_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\frame_B_label"
    dst_2Mod_image_path = r"C:\Users\212774000\Desktop\yexuehua\data\Tracking\frame_2Mod_image"
    image_arr = sitk.GetArrayFromImage(image)
    label_arr = sitk.GetArrayFromImage(label)
    baseName = filename[:-4]
    # pos_dict {"name":(y0,y1,x0,x1)} for perfusion mode
    EH_pos_dict = {"fanli": (140, 746, 116, 640), "lvshufeng": (88, 648, 64, 480), "guzhen":(88, 648, 64, 480), "hanjinbiao1":(140, 746, 116, 640), "panshuyi":(88, 584, 64, 480), "wuzhixun":(88, 648, 64, 480), "yangjianfeng":(88, 584, 64, 480), "yangsen":(88, 648, 64, 480), "yanzhengxu2":(140, 746, 116, 640)}
    B_pos_dict = {"fanli": (140, 746, 640, 1164), "lvshufeng": (88, 648, 480, 896), "guzhen":(88, 648, 480, 896), "hanjinbiao1":(140, 746, 640, 1164), "panshuyi":(88, 584, 480, 896), "wuzhixun":(88, 648, 480, 896), "yangjianfeng":(88, 584, 480, 896), "yangsen":(88, 648, 480, 896), "yanzhengxu2":(140, 746, 640, 1164)}
    pos_EH = EH_pos_dict[baseName]
    pos = B_pos_dict[baseName]
    label_pos = EH_pos_dict[baseName]
    #pos = EH_pos_dict[baseName]
    image_arr_EH = image_arr[:, pos_EH[0]:pos_EH[1], pos_EH[2]:pos_EH[3], :]
    image_arr_B = image_arr[:, pos[0]:pos[1], pos[2]:pos[3], :]
    label_arr = label_arr[:, label_pos[0]:label_pos[1], label_pos[2]:label_pos[3]]
    i = 0
    for image_frame_rgb,image_frame_EH_rgb, label_frame in zip(image_arr_B, image_arr_EH, label_arr):
        if (np.max(label_frame)>0):
            image_frame = RGB2Gray(image_frame_rgb)
            image_frame_EH = RGB2Gray(image_frame_EH_rgb)
            image_frame = np.concatenate((image_frame, image_frame_EH), axis=0)
            image_frame = np.expand_dims(image_frame, 1)
            image_frame_img = sitk.GetImageFromArray(image_frame)
            label_frame = np.expand_dims(label_frame, 0)
            label_frame_img = sitk.GetImageFromArray(label_frame)
            sitk.WriteImage(image_frame_img, os.path.join(dst_2Mod_image_path, baseName + "_" + str(i) + ".nii.gz"))
            # sitk.WriteImage(image_frame_img, os.path.join(dst_B_image_path, baseName + "_" + str(i) + ".nii.gz"))
            # sitk.WriteImage(label_frame_img, os.path.join(dst_B_label_path, baseName + "_" + str(i) + ".nii.gz"))
            #print("Save")
            # sitk.WriteImage(image_frame_img, os.path.join(dst_image_path, baseName + "_" + str(i) + ".nii.gz"))
            # sitk.WriteImage(label_frame_img, os.path.join(dst_label_path, baseName + "_" + str(i) + ".nii.gz"))
            i = i+1


def test():
    print("yenn, you got it!")