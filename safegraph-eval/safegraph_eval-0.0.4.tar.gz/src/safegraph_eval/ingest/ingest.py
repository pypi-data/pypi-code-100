import os
import io
import zipfile
import re
import shutil
import pandas as pd

def sg_unzip(path):
    """
    Unzips zipfiles downloaded from SafeGraph Shop into a folder structure reflective 
    of the original nested zipfile structure.
    Detects whether a zipfile is nested.
    """
    
    # Find the zipfile in the directory
    ext = '.zip'
    for item in os.listdir(path):
        if item.endswith(ext):
            file = os.path.join(path, item)
            
    z = zipfile.ZipFile(file)
    name_list = z.namelist()
    
    # check if the zipfile is nested and extract the nested files
    if any('.zip' in i for i in name_list):
        output_path = []
        # iterate through sub-zipfiles
        for f in z.namelist():
            # create a directory for each file's path root (i.e. folder name)
            dirname = os.path.join(path, os.path.splitext(f)[0])
            
            if os.path.exists(dirname):
                shutil.rmtree(dirname)
            
            os.mkdir(dirname)
            output_path.append(dirname)

            # read inner zip file into bytes buffer
            content = io.BytesIO(z.read(f))
            zip_file = zipfile.ZipFile(content)

            # iterate through zipped files and extract them
            for i in zip_file.namelist():
                zip_file.extract(i, dirname)
            
            zip_file.close()
    
    # otherwise, extract the files from the unnested zip
    else:
        for i in name_list:
            dirname = os.path.join(path, os.path.splitext(file)[0])
            z.extract(i, dirname)
            output_path = dirname
            
    z.close()
    
    return output_path

def read_files(path, return_supplemental_files = True):

    """
    Unzips zipfiles downloaded from SafeGraph Shop into a folder structure reflective 
    of the original nested zipfile structure.
    Detects whether a zipfile is nested.
    """
    
    output = {}
    
    files = os.listdir(path)
        
    data_file = [i for i in files if re.search('core_poi|patterns|geometry|.gz', i)][0]
    data_path = os.path.join(path, data_file)

    data_types = {
        'naics_code':str,
        'latitude':'float64',
        'longitude':'float64',
        'postal_code':str,
        'phone_number':str,
        'enclosed':bool,
        'is_synthetic':bool,
        'poi_cbg':str
    }
        
    data = pd.read_csv(data_path, dtype = data_types)
    # remove prefixes
    data.columns = data.columns.str.replace(r'sg_.__', '', regex = True)
    output['data'] = data

    if return_supplemental_files:
        if any('brand_info' in i for i in files):
            tmp_path = os.path.join(path, 'brand_info.csv')
            brand_info = pd.read_csv(tmp_path, dtype = {'naics_code':str})
            output['brand_info'] = brand_info
        if any('normalization_stats' in i for i in files):
            tmp_path = os.path.join(path, 'normalization_stats.csv')
            norm_stats = pd.read_csv(tmp_path)
            output['normalization_stats'] = norm_stats
        if any('visit_panel_summary' in i for i in files):
            tmp_path = os.path.join(path, 'visit_panel_summary.csv')
            vps = pd.read_csv(tmp_path)
            output['visit_panel_summary'] = vps
        if any('home_panel_summary' in i for i in files):
            tmp_path = os.path.join(path, 'home_panel_summary.csv')
            hps = pd.read_csv(tmp_path, dtype = {'census_block_group':str})
            output['home_panel_summary'] = hps
    
    return(output)

def load_data(path, return_supplemental_files = True):
    """
    Reads unzipped files from SafeGraph Shop.

    If `return_supplemental_files = True`, returns a dictionary where the keys correspond to the data (`data`) or the relevant supplemental files.
    """
    
    if type(path) is list:
        data_list = []
        brand_list = []
        norm_stats_list = []
        hps_list = []
        vps_list = []
        
        for i in path:
            tmp_output = read_files(path = i, return_supplemental_files = return_supplemental_files)
            data_list.append(tmp_output['data'])
            if return_supplemental_files:
                brand_list.append(tmp_output['brand_info'])
                norm_stats_list.append(tmp_output['normalization_stats'])
                hps_list.append(tmp_output['home_panel_summary'])
                vps_list.append(tmp_output['visit_panel_summary'])
        
        output = {}
        output['data'] = pd.concat(data_list)
        if return_supplemental_files:
            output['brand_info'] = brand_list[-1] # keep only the newest brand file
            output['normalization_stats'] = pd.concat(norm_stats_list)
            output['visit_panel_summary'] = pd.concat(vps_list)
            output['home_panel_summary'] = pd.concat(hps_list)
            
    else:
        output = read_files(path, return_supplemental_files = return_supplemental_files)
    
    if return_supplemental_files:
        return(output)
    else:
        return(output['data'])

def read_sg_shop_zipfile(path, return_supplemental_files = True):

    """
    Unzips and reads zipfiles containing data downloaded from the SafeGraph Shop.

    If `return_supplemental_files = True`, returns a dictionary where the keys correspond to the data (`data`) or the relevant supplemental files.
    """
    
    unzipped_path = sg_unzip(path)
    
    output = load_data(unzipped_path, return_supplemental_files)
    
    return(output)