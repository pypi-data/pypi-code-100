"""
Module for IO relevant functions
"""
import sys
import os
import json
sys.path.insert(0, os.path.abspath('./dmitio/'))
from .arguments import arguments

def read_json(infile):
    """Reads data from a json file

    Parameters
    ----------
    infile : str
        Full path to json input file

    Returns
    -------
    data : dict
        dict with data
    """
    with open(infile, 'r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = []
    return data


def save_json(datadict,outfile):
    """Saves dict to a json file

    Parameters
    ----------
    datadict : dict
        json object (dict)
    outfile : str
        Full path to json output file
    """
    with open(outfile,'w') as f:
        json.dump(datadict,f)
    return
