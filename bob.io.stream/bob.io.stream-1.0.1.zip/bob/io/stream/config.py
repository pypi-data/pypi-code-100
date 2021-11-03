import json
import numpy as np


CALIBRATION_PARAMETERS = ['markers',
                          'camera_matrix',
                          'distortion_coefs',
                          'relative_rotation',
                          'relative_translation']

def load_data_config(path, update_submodalities=True):
    with open(path, 'r') as data_config_file:
        data_config = json.load(data_config_file)
        return data_config

def dump_data_config(data_config, path):
    data_config = data_config.copy()
    with open(path, 'w') as data_config_file:
        json.dump(data_config, data_config_file, indent=4, sort_keys=True)