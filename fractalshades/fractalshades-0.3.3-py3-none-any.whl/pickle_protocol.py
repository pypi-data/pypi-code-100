# -*- coding: utf-8 -*-
import pickle
import os
import numpy as np

import fractalshades.utils as fsutils


directory = r"/home/geoffroy/Pictures/math/github_fractal_rep/Fractal-shades/tests/REFERENCE_DATA/xdata_REF"


def ref_point_file(iref, calc_name):
    """
    Returns the file path to store or retrieve data arrays associated to a 
    data chunk
    """
    return os.path.join(directory, "data",
            calc_name + "_pt{0:d}.ref".format(iref))


def save_ref_point(FP_params, Z_path, iref, calc_name):
    """
    Write to a dat file the following data:
       - params = main parameters used for the calculation
       - codes = complex_codes, int_codes, termination_codes
       - arrays : [Z, U, stop_reason, stop_iter]
    """
    save_path = ref_point_file(iref, calc_name)
    fsutils.mkdir_p(os.path.dirname(save_path))
    with open(save_path, 'wb+') as tmpfile:
        print("Path computed, saving", save_path)
        pickle.dump(FP_params, tmpfile, pickle.HIGHEST_PROTOCOL - 1)
        pickle.dump(Z_path, tmpfile, pickle.HIGHEST_PROTOCOL - 1)

def reload_ref_point(iref, calc_name, scan_only=False):
    """
    Reload arrays from a data file
       - params = main parameters used for the calculation
       - codes = complex_codes, int_codes, termination_codes
       - arrays : [Z, U, stop_reason, stop_iter]
    """
    save_path = ref_point_file(iref, calc_name)
    with open(save_path, 'rb') as tmpfile:
        FP_params = pickle.load(tmpfile)
        if scan_only:
            return FP_params
        Z_path = pickle.load(tmpfile)
    return FP_params, Z_path

def main():
    FP_params, Z_path = reload_ref_point(0, "64SA")
    print("FP_params", FP_params)
    print("Z_path", Z_path)
    save_ref_point(FP_params, Z_path, 0, "64SA")
    
if __name__ == "__main__":
    main()