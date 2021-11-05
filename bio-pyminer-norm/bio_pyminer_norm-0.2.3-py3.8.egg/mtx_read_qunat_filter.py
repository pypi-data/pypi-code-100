#!/usr/local/env python3
import os
import csv
import h5py
import gzip
import argparse
import fileinput
import scipy.io
import scipy.sparse
import numpy as np
import seaborn as sns
from scipy.sparse import sparsetools
from matplotlib import pyplot as plt
from pyminer.common_functions import read_table, read_file, process_dir, strip_split
from pyminer_norm.combine_col_sums_counts import get_col_sums_counts
try:
    from pyminer_norm.malat1_and_mito_filter import get_mal_mito_percent, plot_single_mal_mito
else:
    from malat1_and_mito_filter import get_mal_mito_percent, plot_single_mal_mito


def read_and_convert_mtx(mat_file,
                         col_file,
                         row_file,
                         out_file=None):
    """
    takes in the mtx matrix file, and it's associated 
    """
    mat = scipy.io.mmread(mat_file)
    mat = scipy.sparse.csc_matrix(mat)
    feature_ids = read_table(row_file)
    print(feature_ids[:5])
    barcodes = read_file(col_file, "lines")
    if out_file is None:
        return(mat, barcodes, feature_ids)
    ## first we'll open and write the header for the file
    f = open(out_file, 'w')
    f.writelines('genes\t'+'\t'.join(barcodes)+'\n')
    for i in range(0,mat.shape[0]):
        temp_row_vect = mat[i,:].toarray().tolist()
        temp_row_vect = temp_row_vect[0]
        temp_row_vect = list(map(str,temp_row_vect))
        if i% 1000 == 0:
            print('\t',i)
        temp_row_vect = str(feature_ids[i][0])+'\t'+'\t'.join(temp_row_vect)
        if i != mat.shape[0]-1:
            temp_row_vect += '\n'
        f.writelines(temp_row_vect)
    f.close()
    return


def plot_colsums_counts(in_mat_list, 
                        col_counts=False, 
                        in_name_list=None, 
                        out_dir = None):
    if in_name_list is None:
        in_name_list = range(len(in_mat_list))
    all_col_sums = []
    plt.clf()
    for i in range(len(in_mat_list)):
        if col_counts:
            print("doing column counts")
            in_mat_list[i].data = 1
            #colsums = np.array(np.sum(np.array(in_mat_list[i]!=0),axis=0))
        else:
            print("doing column sums")
        colsums = np.array(np.sum(in_mat_list[i],axis=0))
        if len(colsums.shape)==2:
            ## then it was a matrix rather than an array
            ## matrices can't be flattened, so convert to numpy
            ## then check if it's 2D & get rid of the second if needed
            colsums = colsums[0]
        all_col_sums.append(colsums)
        sns.distplot(np.log10(colsums+1), label = in_name_list[i])
    if out_dir is None:
        plt.show()
    else:
        out_dir = process_dir(out_dir)
        if col_counts:
            out_file_name = os.path.join(out_dir, "log_column_counts.png")
        else:
            out_file_name = os.path.join(out_dir, "log_column_sums.png")
        plt.savefig(out_file_name,
                    dpi=600,
                    bbox_inches='tight')
    return(all_col_sums)


def read_several_mtx(mat_file_list, col_file_list, row_file_list):
    assert len(mat_file_list) == len(col_file_list)
    assert len(col_file_list) == len(row_file_list)
    mat_list = []
    col_list = []
    row_list = []
    for i in range(len(mat_file_list)):
        temp_mat, temp_col, temp_row = read_and_convert_mtx(mat_file_list[i], col_file_list[i], row_file_list[i])
        mat_list.append(temp_mat)
        col_list.append(temp_col)
        row_list.append(temp_row)
    return(mat_list, col_list, row_list)

###########################################

def read_in_chromium_h5(in_file):
    print("reading", in_file)
    in_hdf5 = h5py.File(in_file,'r')
    mat = scipy.sparse.csc_matrix((in_hdf5["matrix"]["data"], 
                                   in_hdf5["matrix"]["indices"], 
                                   in_hdf5["matrix"]["indptr"]), 
                                  shape=in_hdf5["matrix"]["shape"])
    barcodes = np.array(in_hdf5["matrix"]["barcodes"]).tolist()
    barcodes = [temp_feat.decode() for temp_feat in barcodes]
    temp_feats = np.array(in_hdf5["matrix"]['features']['id']).tolist()
    feature_ids = [temp_feat.decode() for temp_feat in temp_feats]
    in_hdf5.close()
    return(mat, barcodes, feature_ids)


def get_chromium_name(in_file):
    return(os.path.basename(os.path.dirname(os.path.dirname(in_file))))


def write_count_sum_file(barcodes, metric, type_of_analysis, out_dir, name):
    out_file = os.path.join(out_dir, name + '_col_' + type_of_analysis + '.txt')
    f = open(out_file,'w')
    f.write('\t'.join(['sample', type_of_analysis])+"\n")
    for i in range(len(barcodes)):
        out_line = '\t'.join([barcodes[i], str(metric[i])])
        if i < len(barcodes)-1:
            out_line+="\n"
        f.write(out_line)
    f.close()
    return(out_file)


def get_csc_sums_and_counts(in_file, mat, barcodes, name = None):
    if name is None:
        name = os.path.splitext(in_file)[0]
    out_dir = os.path.dirname(in_file)
    print("\tcalculating colsums")
    colsums = np.array(np.sum(mat,axis=0)).flatten()
    mat.data = np.ones(mat.data.shape, dtype = "uint8")
    print("\tcalculating colcounts")
    colcounts = np.array(np.sum(mat,axis=0)).flatten()
    write_count_sum_file(barcodes, colsums, "sum", out_dir, name = name)
    write_count_sum_file(barcodes, colcounts, "count", out_dir, name = name)
    return(colsums, colcounts)


def process_all_chromium_h5(all_h5_files,
                            out_dir,
                            species="mmusculus"):
    out_dir = process_dir(out_dir)
    mal_mito_dict = {}
    for in_file in all_h5_files:
        mat, barcodes, feature_ids = read_in_chromium_h5(in_file)
        name = get_chromium_name(in_file)
        file_dir = os.path.dirname(in_file)
        colsums, colcounts = get_csc_sums_and_counts(in_file, 
                                                     mat, 
                                                     barcodes, 
                                                     name = name)
        # malat, mito = get_mal_mito_percent(mat, barcodes, feature_ids, in_file, colsums, species=species)
        # print("malat:",malat)
        # print("mito:",mito)
        # write_count_sum_file(barcodes, malat, "malat1", file_dir, name = name)
        # write_count_sum_file(barcodes, colcounts, "mito", file_dir, name = name)
        # plot_single_mal_mito(malat, mito, colsums, file_dir)
        # mal_mito_dict[name]={"malat1":malat,
        #                      "mito":mito}
    get_col_sums_counts(all_h5_files, out_dir)
    return()


##################################################

def get_name_from_file(in_file):
    file_dir = os.path.dirname(in_file)+os.path.sep
    possible_files = list(glob.glob(file_dir+"*_col_count.txt"))
    if len(possible_files)==0:
        return(os.path.splitext(in_file)[0])
    else:
        temp_colcount_file = possible_files[0]
        return(os.path.basename(temp_colcount_file).replace("_col_count.txt",""))


def get_colsum_file(in_file):
    file_dir = os.path.dirname(in_file)+os.path.sep
    possible_files = list(glob.glob(file_dir+"*_col_sum.txt"))
    temp_colcount_file = possible_files[0]
    return(temp_colcount_file)


def get_colcount_file(in_file):
    file_dir = os.path.dirname(in_file)+os.path.sep
    possible_files = list(glob.glob(file_dir+"*_col_count.txt"))
    temp_colcount_file = possible_files[0]
    return(temp_colcount_file)


def get_min_sum(all_files):
    temp_min=999999999
    print("finding minimum of datasets")
    for temp_file in all_files:
        first = True
        for line in fileinput.input(get_colsum_file(temp_file)):
            if first:
                first=False
            else:
                temp_min = min([temp_min,int(strip_split(line)[1])])
        fileinput.close()
    return(temp_min)


def get_h5_shape(in_h5):
    f = h5py.File(in_h5,'r')
    shape = np.array(f["matrix"]["shape"])
    f.close()
    return(shape)


def get_mtx_shape(in_mtx):
    mat = scipy.io.mmread(in_mtx)
    #mat = scipy.sparse.csc_matrix(mat)
    return(mat.shape)


def get_single_pass(in_file, lower, upper):
    keep_cell=set()
    first = True
    for line in fileinput.input(in_file):
        if first:
            first = False
        else:
            line = strip_split(line)
            if int(line[1])>lower and int(line[1])<upper:
                keep_cell.add(line[0])
    fileinput.close()
    return(keep_cell)


def get_passing_cells(temp_colcounts_file,
                       temp_colsums_file,
                       c_low,
                       c_high,
                       s_low,
                       s_high):
    count_keep = get_single_pass(temp_colcounts_file, c_low, c_high)
    sum_keep = get_single_pass(temp_colsums_file, s_low, s_high)
    final_keep = count_keep.intersection(sum_keep)
    return(final_keep)


def get_sorted_idxs_and_bcode(barcodes, keep_barcodes):
    counter=0
    keep_barcodes_sorted = np.zeros((len(keep_barcodes))).tolist()
    keep_idxs = np.zeros((len(keep_barcodes)))
    for i in range(len(barcodes)):
        if barcodes[i] in keep_barcodes:
            keep_barcodes_sorted[counter]=barcodes[i]
            keep_idxs[counter] = i
            counter+=1
    return keep_idxs, keep_barcodes_sorted


def get_h5_barcodes(in_file, keep_barcodes):
    in_hdf5 = h5py.File(in_file,'r')
    barcodes = np.array(in_hdf5["matrix"]["barcodes"]).tolist()
    barcodes = [temp_feat.decode() for temp_feat in barcodes]
    return get_sorted_idxs_and_bcode(barcodes, keep_barcodes)


def get_mtx_barcodes(in_file, col_file, keep_barcodes):
    return get_sorted_idxs_and_bcode(read_file(col_file, "lines"), keep_barcodes)


def get_all_keep_cell_dict(in_h5=[], 
                           in_mtx_mat=[], 
                           in_mtx_cols=[], 
                           in_mtx_rows=[],
                           c_low=-np.inf,
                           c_high=np.inf,
                           s_low=None,
                           s_high=np.inf):
    data_file_dict = {}
    all_files = in_h5+in_mtx_mat
    for i in range(len(all_files)):
        temp_file = all_files[i]
        data_file_dict[temp_file]={}
        data_file_dict[temp_file]["name"] = get_name_from_file(temp_file)
        if temp_file in in_h5:
            temp_type = "h5"
        elif temp_file in in_mtx_mat:
            temp_type = "mtx"
        else:
            temp_type = None
        temp_colsums_file = get_colsum_file(temp_file)
        data_file_dict[temp_file]["type"]=temp_type
        data_file_dict[temp_file]["colsum_file"] = temp_colsums_file
        temp_colcounts_file = get_colcount_file(temp_file)
        data_file_dict[temp_file]["colcount_file"] = temp_colcounts_file
        data_file_dict[temp_file]["keep_cells"] = get_passing_cells(temp_colcounts_file,
                                                                   temp_colsums_file,
                                                                   c_low,
                                                                   c_high,
                                                                   s_low,
                                                                   s_high)
        print(data_file_dict[temp_file]["name"])
        print("\tkeeping",len(data_file_dict[temp_file]["keep_cells"]),"cells")
        if temp_type == "h5":
            keep_idxs, keep_barcodes = get_h5_barcodes(temp_file, data_file_dict[temp_file]["keep_cells"])
            data_file_dict[temp_file]["keep_indices"] = keep_idxs
            data_file_dict[temp_file]["keep_cells"] = keep_barcodes
            data_file_dict[temp_file]["col_file"] = None
            data_file_dict[temp_file]["row_file"] = None
            data_file_dict[temp_file]["shape"] = get_h5_shape(temp_file)
        if temp_type == "mtx":
            keep_idxs, keep_barcodes = get_mtx_barcodes(temp_file, 
                                                        in_mtx_cols[i-len(in_h5)],
                                                        data_file_dict[temp_file]["keep_cells"])
            data_file_dict[temp_file]["keep_indices"] = keep_idxs
            data_file_dict[temp_file]["keep_cells"] = keep_barcodes
            data_file_dict[temp_file]["col_file"] = in_mtx_cols[i-len(in_h5)]
            data_file_dict[temp_file]["row_file"] = in_mtx_rows[i-len(in_h5)]
            data_file_dict[temp_file]["shape"] = get_mtx_shape(temp_file)
    return(data_file_dict)



def to_csr(in_mat):
    assert in_mat.ndim == 2
    # Pass 1: sum duplicates
    in_mat.sum_duplicates()
    # Pass 2: sort indices
    order = np.lexsort(in_mat.coords[::-1])
    row, col = in_mat.coords[:, order]
    data = in_mat.data[order]
    # Pass 3: count nonzeros in each row
    indptr = np.zeros(in_mat.shape[0] + 1, dtype=in_mat.dtype)
    np.cumsum(np.bincount(row, minlength=in_mat.shape[0]), out=indptr[1:])
    return csr_matrix((data, col, indptr), shape=in_mat.shape)


def write_out_tsv_subset(out_file, in_file, keep_idxs, dset_type, in_cols=None, in_rows=None):
    if dset_type=="h5":
        ## then it's an h5 file
        mat, barcodes, feature_ids = read_in_chromium_h5(in_file)
    elif dset_type=="mtx":
        assert in_cols is not None
        assert in_rows is not None
        mat, barcodes, feature_ids = read_and_convert_mtx(in_file, in_cols, in_rows)
    ## convert to row based sparse mat
    mat = scipy.sparse.csr_matrix(mat)
    #mat=sparsetools.csc_tocsr(mat)# = scipy.sparse.csr_matrix(mat)
    keep_idxs = np.array(keep_idxs,dtype=int)
    barcodes = np.array(barcodes)
    print("writing:",out_file)
    f=open(out_file, 'w')
    ## write the header
    f.write('\t'.join(['genes']+barcodes[keep_idxs].tolist())+'\n')
    ## write the rows
    num_rows = len(feature_ids)
    for i in range(num_rows):
        out_line = '\t'.join([feature_ids[i]]+list(map(str,mat[i,keep_idxs].todense().tolist()[0])))
        if i < (num_rows-1):
            out_line+='\n'
        f.write(out_line)
    f.close()
    return()


def filter_and_write_individual_files(full_data_dict):
    for dset in full_data_dict.keys():
        out_dir = os.path.dirname(dset)
        out_file_name = os.path.join(out_dir,full_data_dict[dset]["name"]+".tsv")
        out_data_shape = (full_data_dict[dset]["shape"][0],len(full_data_dict[dset]["keep_cells"]))
        full_data_dict[dset]
        write_out_tsv_subset(out_file_name, 
                             dset, 
                             full_data_dict[dset]["keep_indices"], 
                             dset_type=full_data_dict[dset]["type"], 
                             in_cols=full_data_dict[dset]["col_file"], 
                             in_rows=full_data_dict[dset]["row_file"])
    return()


def apply_filters_downsample_log(out_dir, full_data_dict, no_merge=False, in_memory=True):
    ## do preflight checks
    temp_rows = None
    for dset in full_data_dict.keys():
        if temp_rows is None:
            temp_rows = full_data_dict[dset]["shape"][0]
        else:
            if temp_rows != full_data_dict[dset]["shape"][0]:
                raise Error("These datasets don't have the same number of rows!")
    if no_merge:
        filter_and_write_individual_files(full_data_dict)
        return
    #####################
    ## TODO: complete the rest of the merger, downsample and log transform here.
    ## first make the 
    #full_data_dict
    return


def filter_merge_sparse(out_dir,
                        in_h5=[], 
                        in_mtx_mat=[], 
                        in_mtx_cols=[], 
                        in_mtx_rows=[],
                        c_low=-np.inf,
                        c_high=np.inf,
                        s_low=None,
                        s_high=np.inf,
                        in_memory=True,
                        no_merge=False):
    assert len(in_mtx_mat) == len(in_mtx_cols)
    assert len(in_mtx_cols) == len(in_mtx_rows)
    assert len(in_mtx_mat) + len(in_mtx_cols) + len(in_mtx_rows) + len(in_h5) > 0
    ## if no cutoff is given, make it the lowest included cell
    if s_low is None:
        s_low = get_min_sum(in_h5+in_mtx_mat)
    full_data_dict = get_all_keep_cell_dict(in_h5=all_h5_files,#in_h5, 
                                           # in_mtx_mat=in_mtx_mat, 
                                           # in_mtx_cols=in_mtx_cols, 
                                           # in_mtx_rows=in_mtx_rows,
                                           c_low=c_low,
                                           c_high=c_high,
                                           s_low=s_low,
                                           s_high=s_high)
    apply_filters_downsample_log(out_dir, 
                                 full_data_dict, 
                                 no_merge = no_merge, 
                                 in_memory=in_memory)
    # mat = scipy.sparse.csc_matrix((in_hdf5["matrix"]["data"], 
    #                                in_hdf5["matrix"]["indices"], 
    #                                in_hdf5["matrix"]["indptr"]), 
    #                               shape=in_hdf5["matrix"]["shape"])
    # barcodes = np.array(in_hdf5["matrix"]["barcodes"]).tolist()
    # barcodes = [temp_feat.decode() for temp_feat in barcodes]
    # temp_feats = np.array(in_hdf5["matrix"]['features']['id']).tolist()



##################################################
#in_file = '/media/scott/ssd_2tb/alignment_refs/ExUt_E105_1/ExUt_E105_1/outs/filtered_feature_bc_matrix.h5'
#mat, barcodes, feature_ids = read_in_chromium_h5(in_file)
#colsums, colcounts = get_csc_sums_and_counts(in_file, mat, barcodes, name = get_chromium_name(in_file))
all_h5_files = ["/media/scott/ssd_2tb/alignment_refs/ExUt_E85_1/ExUt_E85_1/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E85_pool23/ExUt_E85_pool23/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_5/ExUt_E105_5/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_6/ExUt_E105_6/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_7/ExUt_E105_7/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E85_1/InUt_E85_1/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E85_pool23/InUt_E85_pool23/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E105_2/InUt_E105_2/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E105_3/InUt_E105_3/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E105_5/InUt_E105_5/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_1/ExUt_E105_1/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_2/ExUt_E105_2/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_3/ExUt_E105_3/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/ExUt_E105_4/ExUt_E105_4/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E105_1/InUt_E105_1/outs/filtered_feature_bc_matrix.h5","/media/scott/ssd_2tb/alignment_refs/InUt_E105_4/InUt_E105_4/outs/filtered_feature_bc_matrix.h5"]
process_all_chromium_h5(all_h5_files, '/media/scott/ssd_2tb/alignment_refs/combined_summary' )

filter_merge_sparse(None,in_h5=all_h5_files,c_low=1200,c_high=6000,s_low=3750,s_high=20000,no_merge=True)


###########################################

if __name__ == "__main__":
    mtx_files = ["./InUt_E105_1/InUt_E105_1.mtx",
                "./InUt_E105_2/InUt_E105_2.mtx",
                "./ExUt_E105_1/ExUt_E105_1.mtx",
                "./ExUt_E105_2/ExUt_E105_2.mtx",
                "./ExUt_E105_3/ExUt_E105_3.mtx",
                "./ExUt_E105_4/ExUt_E105_4.mtx"]
    barcode_files = ["./InUt_E105_1/InUt_E105_1.barcodes.txt",
                "./InUt_E105_2/InUt_E105_2.barcodes.txt",
                "./ExUt_E105_1/ExUt_E105_1.barcodes.txt",
                "./ExUt_E105_2/ExUt_E105_2.barcodes.txt",
                "./ExUt_E105_3/ExUt_E105_3.barcodes.txt",
                "./ExUt_E105_4/ExUt_E105_4.barcodes.txt"]
    feature_files = ["./InUt_E105_1/InUt_E105_1.genes.txt",
                "./InUt_E105_2/InUt_E105_2.genes.txt",
                "./ExUt_E105_1/ExUt_E105_1.genes.txt",
                "./ExUt_E105_2/ExUt_E105_2.genes.txt",
                "./ExUt_E105_3/ExUt_E105_3.genes.txt",
                "./ExUt_E105_4/ExUt_E105_4.genes.txt"]
    name_list = ["InUt_E105_1",
                "InUt_E105_2",
                "ExUt_E105_1",
                "ExUt_E105_2",
                "ExUt_E105_3",
                "ExUt_E105_4"]
    mat_list, col_list, row_list = read_several_mtx(mtx_files,
                                                    barcode_files,
                                                    feature_files)
    out_dir = "./combined_summary"
    colsums = plot_colsums_counts(mat_list, 
                                col_counts=False, 
                                in_name_list=name_list, 
                                out_dir = out_dir)
    colcounts = plot_colsums_counts(mat_list, 
                                col_counts=True, 
                                in_name_list=name_list, 
                                out_dir = out_dir)
