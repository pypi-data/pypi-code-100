#!/usr/bin/env python3.7
import glob
import pandas as pd
import os
import numpy as np
import argparse
from bfg_analysis import supplements
# Author: Roujia Li
# email: Roujia.li@mail.utoronto.ca

"""
Process output from read count
In each folder (yAD*DB*), take the read counts files (up/dn rawcounts and combined counts)
"""

# global variables
# conditions = ["Baseline", "H2O2", "MMS", "PoorCarbon"]

def read_files(arguments):
    """
    read csv files from input_dir,
    Input dir contains all by all (or AD*DB*) folders (ex. yAD1DB4)
    Inside each subfolder, there are counts files which are needed for calculating IS
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
        
        IS_norm = calculate_IS(pre, med, high, arguments.preFloor, arguments.weight)
        all_scores.append(IS_norm)
        i+=1
        if i == 5:
            break
        print(IS_norm)
    IS_norm_all = pd.concat(all_scores, axis=1)
    print(IS_norm_all)
    merged_IS = select_rank(IS_norm_all, arguments.rank)
    print(merged_IS)
    return merged_IS


def select_rank(IS_norm, rank):
    """
    Return interaction pairs taken based on rank
    @param IS_norm: normalized interaction scores
    @param rank: which rank to keep (default=2)
    @return df: df contains [Interaction (AD_DB ORF), AD_name, DB_name, Score]
    """
    # convert input matrix to a 3 col table
    transform = IS_norm.unstack().reset_index()
    transform.columns = ['DB_name', 'AD_name', 'Score']
    # split cols
    transform[['DB', 'DB_BC']] = transform['DB_name'].str.split('_', expand=True)
    transform[['AD', 'AD_BC']] = transform['AD_name'].str.split('_', expand=True)
    # merge cols
    transform['Interaction'] = transform.AD.str.cat(transform.DB, sep="_")
    # remove interactions with nan scores
    transform = transform.dropna(subset=["Score"])
    # group by interaction
    # only get certain index
    sort = transform.sort_values(["Score"], ascending=False).groupby(['Interaction'])
    # take the 2nd highest if not null(rank=2)
    df = sort.nth(rank-1).dropna(how="any")
    df = df[["AD_name", "DB_name", "Score"]]
    df = df[df["Score"]>0]
    # sort df by IS
    df = df.sort_values(by='Score', ascending=False)
    return df


def select_rank_old(IS_norm, rank, mode, summary_dir):
    """
    From normalized score matrix, select score for AD and DB pair
    based on rank
    """
    # summary for AD (all the genes and group)
    # yeast
    yAD_summary = os.path.join(summary_dir, "20180627_byORFeome_AD.csv")
    # human
    hAD_summary = os.path.join(summary_dir, "20180927_bhORFeome_AD_RL.csv")
    # human with null
    hvAD_summary = os.path.join(summary_dir, "20180927_bhORFeome_AD_RL_withNull.csv")

    # summary for DB (all the genes and group)
    # yeast
    yDB_summary = os.path.join(summary_dir, "20180627_byORFeome_DB_AA.csv")
    # human
    hDB_summary = os.path.join(summary_dir, "20180927_bhORFeome_DB_RL.csv")
    # human with null
    hvDB_summary = os.path.join(summary_dir, "20180927_bhORFeome_DB_RL_withNull.csv")
    # hedgy summary
    heDB_summary = os.path.join(summary_dir, "20201014_hEDGY_Screen1_ORF_BC_list.csv")

    # virus
    vADNC = os.path.join(summary_dir, "vADNC_withNull.csv")
    vAD2u = os.path.join(summary_dir, "vAD2u_withNull.csv")
    vDBNC = os.path.join(summary_dir, "vDBNC_withNull.csv")
    vADall = os.path.join(summary_dir, "vADall_withNull.csv")

    # get AD and DB genes
    # get AD and DB genes from different files based on the mode
    if mode == "yeast":
        AD_genes, DB_genes = supplements.read_summary(yAD_summary, yDB_summary, "Gall", "Gall")

    elif mode =="human":
        AD_genes, DB_genes = supplements.read_summary(hAD_summary, hDB_summary, "Gall", "Gall")

    elif mode == "virus":
        if "G" in AD_GROUP: # human
            AD_GROUP = AD_GROUP.split("_")[-1]
        if "G" in DB_GROUP: # human
            DB_GROUP = DB_GROUP.split("_")[-1]
        AD_genes, DB_genes = supplements.read_summary_virus(hvAD_summary, hvDB_summary, AD_GROUP, DB_GROUP)

    elif mode == "hedgy":
        AD_GROUP = AD_GROUP.split("_")[-1]
        AD_genes, DB_genes = supplements.read_summary_hedgy(hvAD_summary, heDB_summary, AD_GROUP)
    else:
        raise ValueError("Please pride valid mode: yeast or human orvirus")

    # AD_genes, DB_genes are the gene identifier (gene_name with bc)
    AD_unique = pd.Series([i.split("_")[0] if "ull" not in i else i for i in AD_genes]).unique()
    DB_unique = pd.Series([i.split("_")[0] if "ull" not in i else i for i in DB_genes]).unique()
    print(len(AD_unique))
    print(len(DB_unique))


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

    # calculate marginal frequencies for GFP_pre
    GFP_pre_ADfreq, GFP_pre_DBfreq = marginal_freq(GFP_pre)
    # floor values in AD and DB
    GFP_pre_ADfreq = GFP_pre_ADfreq.clip(lower=preFloor)
    GFP_pre_DBfreq = GFP_pre_DBfreq.clip(lower=preFloor)
    # rebuild matrix from two vectors
    freq_mx = np.outer(GFP_pre_ADfreq, GFP_pre_DBfreq)
    GFP_pre_freq = pd.DataFrame(data = freq_mx, columns = GFP_pre_DBfreq.index.tolist(), index = GFP_pre_ADfreq.index.tolist())
    # calculate frequencies for GFP_med and GFP_high
    GFP_med_freq = freq(GFP_med)
    GFP_high_freq = freq(GFP_high)
    # use GFP_pre, med and high to calculate IS
    IS = ((weightHigh * GFP_high_freq) + GFP_med_freq) / GFP_pre_freq
    #score normalization
    IS_norm = IS.sub(IS.median(axis=1), axis=0).sub(IS.median(axis=0), axis=1)
    # first normalize with AD
    IS_norm = IS_norm.apply(lambda x: normalization(x), axis=1)
    # then normalize with DB
    IS_norm = IS_norm.apply(lambda x: normalization(x), axis=0)
    
    return IS_norm

# help functions
def normalization(vector):
    """
    Normalize scores in this vector
    """
    x = vector[vector>0]
    beta = x.quantile(0.9)
    updated_vector = vector/beta
    return updated_vector


def freq(matrix):

    # sum of matrix
    total = matrix.values.sum()
    freq_df = matrix / total
    return freq_df


def marginal_freq(matrix):
    # sum of matrix
    total = matrix.values.sum()
    col_freq = matrix.sum(axis=0)/total
    row_freq = matrix.sum(axis=1)/total
    return row_freq, col_freq


if __name__ == "__main__":

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
