import os
import sys


def built_in_resources(resources_path, resources_file='resources'):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('')
    return os.path.join(base_path, os.path.join(resources_file, resources_path))
