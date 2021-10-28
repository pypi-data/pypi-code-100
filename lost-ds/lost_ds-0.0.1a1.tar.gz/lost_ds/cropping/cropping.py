import os

from tqdm import tqdm
import pandas as pd 
from joblib import Parallel, delayed, cpu_count
import cv2

from lost_ds.io.file_man import FileMan
from lost_ds.functional.validation import validate_empty_images
from lost_ds.cropping.ds_cropper import DSCropper
from lost_ds.util import get_fs


def crop_anno(img_path, crop_position, df, im_w=None, im_h=None, 
              filesystem:FileMan=None):
    """Calculate annos for a crop-position in an image
    
    Args:
        img_path (str): image to calculate the crop-annos
        crop_position (list): crop-position like: [xmin, ymin, xmax, ymax] 
            in absolute data-format
        im_w (int): width of image if available
        im_h (int): height of image if available
        df (pd.DataFrame): dataframe to apply 
        filesystem (fsspec.filesystem, FileMan): filesystem to use. Use local
            if not initialized
            
    Returns:
        pd.DataFrame 
    """
    cropper = DSCropper(filesystem=filesystem)
    return cropper.crop_anno(img_path, df, crop_position, im_w, im_h)

    
def crop_dataset(df, dst_dir, crop_shape=(500, 500), overlap=(0,0),
                 write_empty=False, fill_value=0, filesystem:FileMan=None):
    """Crop the entire dataset with fixed crop-shape

    Args:
        df (pd.DataFrame): dataframe to apply bbox typecast
        dst_dir (str): Directory to store the new dataset
        crop_shape (tuple, list): [H, W] cropped image dimensions
        overlap (tuple, list): [H, W] overlap between crops
        write_empty (bool): Flag if crops without annos wil be written
        fill_value (float): pixel value to fill the rest of crops at borders
        filesystem (fsspec.filesystem, FileMan): filesystem to use. Use local
            if not initialized
    Returns:
        pd.DataFrame
    """
    fs = get_fs(filesystem)
    fs.makedirs(dst_dir, True)
    df = validate_empty_images(df)
    
    def crop_and_recalculate(img_path, img_df):
        cropper = DSCropper(filesystem=filesystem)
        img = cropper.fs.read_img(img_path)
        im_h, im_w, im_c = img.shape
                
        crops, positions, padding = cropper.crop_img(img, crop_shape, overlap, 
                                                     fill_value)
        img_name, img_ending = img_path.split('/')[-1].split('.')
        
        result_df = []
        for i, position in enumerate(positions):
            crop_name = img_name + '_crop_' + str(i) + '.' + img_ending
            crop_path = os.path.join(dst_dir, crop_name)
            crop_df = cropper.crop_anno(img_path, img_df, position, im_w, im_h, 
                                        padding)
            data_present = crop_df.anno_data.notnull()
            
            if data_present.any() or write_empty:
                crop_df['img_path'] = crop_path
                cropper.fs.write_img(crops[i], crop_path)
                result_df.append(crop_df)
                
        return pd.concat(result_df)
    
    crop_dfs = Parallel(n_jobs=-1)(delayed(crop_and_recalculate)(path, df) 
                                    for path, df in tqdm(df.groupby('img_path'), 
                                                     desc='crop dataset'))
    # crop_dfs = []
    # for path in tqdm(df.img_path.unique(), desc='crop dataset'):
    #     crop_dfs.append(crop_and_recalculate(path))
        
    return pd.concat(crop_dfs)