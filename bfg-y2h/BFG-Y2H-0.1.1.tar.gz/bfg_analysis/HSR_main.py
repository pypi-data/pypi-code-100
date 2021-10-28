#!/usr/bin/env python3.7
import glob
import pandas as pd
import os
import numpy as np
import argparse
from bfg_analysis import supplements
# Author: Roujia Li
# email: Roujia.li@mail.utoronto.ca

def read_files(arguments):
    """
    read count files for HSR
    """

    all_csv_files = glob.glob(f"{arguments.input}/*/*_combined_counts.csv")
    # extract all folder names
    all_groups = list(set([os.path.dirname(i).split("/")[-1] for i in all_csv_files]))
    # save all the normalized score in a matrix
    all_scores = []
    i=0
    for g in all_groups: # for each AD/DB combination, get their GFP pre|med|high files
        count_files = [f for f in all_csv_files if g in f]
        if len(count_files) < 3:
            raise ValueError("Need at least 3 counts files for calculating scores")
        print(g)
        # pass combined counts file for processing
        pre = [s for s in count_files if "_GFP_pre_" in s][0]
        med = [s for s in count_files if "_GFP_med_" in s][0]
        high = [s for s in count_files if "_GFP_high_" in s][0]


def calculate_IS(GFP_pre, GFP_med, GFP_high, preFloor, weightHigh):
    """
    Input files contains a list of file paths for a specific AD and DB combination
    Required: GFP_pre, GFP_med, GFP_high
    """
    # DB as colnames and AD as row names
    # load three matrix
    GFP_pre = pd.read_csv(GFP_pre, index_col=0)
    GFP_med = pd.read_csv(GFP_med, index_col=0)
    GFP_high = pd.read_csv(GFP_high, index_col=0)

    # calculate frequencies for GFP_med and GFP_high
    GFP_pre_freq = freq(GFP_pre)
    GFP_med_freq = freq(GFP_med)
    GFP_high_freq = freq(GFP_high)


def freq(matrix):
    # sum of matrix
    total = matrix.values.sum()
    freq_df = matrix / total
    return freq_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BFG-Y2H (scoring)')

    # parameters for cluster
    parser.add_argument("--input", help="Path to all read count files you want to analyze")
    #parser.add_argument("--output", help="Output path for sam files")
    parser.add_argument("--mode", help="pick yeast or human or virus or hedgy", default="yeast")

    #parser.add_argument("--alignment", action="store_true", help= "turn on alignment")
    parser.add_argument("--summary", help="path to all summary files", default="/home/rothlab/rli/02_dev/08_bfg_y2h/bfg_data/summary/")
    #parser.add_argument("--ref", help="path to all reference files", default="/home/rothlab/rli/02_dev/08_bfg_y2h/bfg_data/reference/")
    #parser.add_argument("--readCount", action="store_true", help= "turn on read counting")

    # arguments with default values set
    parser.add_argument("--preFloor", type=float, help="assign floor value for GFP pre marginal frequencies", default=0.00001)
    parser.add_argument("--weight", type=float, help="weight for GFP_high", default=1)
    parser.add_argument("--rank", type=int, help="final rank to pick", default=2)
    args = parser.parse_args()
    read_files(args)
