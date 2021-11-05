#!python

##import dependency libraries
import sys,time,glob,os,pickle,fileinput
from subprocess import Popen
from operator import itemgetter
import gc, fileinput
import numpy as np
import argparse
from copy import deepcopy
import pandas as pd
try:
    from pyminer.common_functions import *
except:
    from common_functions import *
##############################################################


##################################################################
## processing functions


def get_group(i,
              sig_q_and_dist, 
              group_names, 
              k_group_max, 
              k_group_means):
    if np.sum(k_group_means[i]) == 0.0:
        return(["None","None"])
    indexes = np.where(k_group_means[i] == k_group_max[i])[0]
    ## I can't believe this actually happened, but I came accross a dataset with a 
    ## non-zero tie for mean expression
    if indexes.size > 1:
        return(["None","None"])
    else:
        index = indexes[0]
    if not sig_q_and_dist[i]:
        return(["None", group_names[index]])
    else:
        return([group_names[index], group_names[index]])


def process_symbol(in_symbol_list,ensg):
    if len(in_symbol_list)==0:
        return(ensg)
    else:
        return('_'.join(in_symbol_list))


def process_def(in_def):
    if len(in_def)==0:
        return("NA")
    else:
        return(in_def[0])


def get_best_match_for_all_subset(summary_table,
                                  group_names,
                                  top_n_genes = 5):
    headers = summary_table[0]
    summary_table = summary_table[1:]
    print(headers)
    df = pd.DataFrame(summary_table, columns = headers)
    print(df.head())
    previously_selected_genes = []
    selected_genes = {}
    selected_genes_linear = []
    selected_genes_table = []
    #['gene','gene_symbol','gene_def', 'aov_BH_p', 'range', 'dist_from_max_to_second_max', 'q_value', 'specific_marker_for_group','best_match_group']
    df = df.sort_values(by="dist_from_max_to_second_max", ascending=False)
    for group_name in group_names:
        temp_genes = list(df.loc[df["specific_marker_for_group"] == group_name,"gene"])
        len_temp_genes = len(temp_genes)
        capture = min([top_n_genes,len_temp_genes])
        temp_genes = temp_genes[:capture]
        num_genes_left = top_n_genes - len(temp_genes)
        if num_genes_left>0:
            ## in case their aren't a ton of very specific
            ## we'll top it off with genes that are just highly enriched, but not specific
            temp_genes_2 = list(df.loc[df["best_match_group"] == group_name,"gene"])
            capture_2 = min([top_n_genes,num_genes_left])
            temp_genes += list(temp_genes_2[:capture_2])
        selected_genes[group_name] = temp_genes
        selected_genes_linear += temp_genes
        for temp_gene in temp_genes:
            selected_genes_table.append([temp_gene, temp_gene + "_" + group_name])
    return(selected_genes_table)


## </processing functions>
##########################################################################


def get_marker_genes(symbol_def_dict, 
                     means,
                     sig,
                     out,
                     sig_cutoff = 0.05,
                     q_cutoff = 0.5,
                     percentile = 0.9):
    ## import the annotation dict
    symbol_dict, def_dict = import_dict(symbol_def_dict)

    k_group_means_file = np.array(read_table(means))
    id_list = k_group_means_file[1:,0].tolist()
    group_names = k_group_means_file[0,1:].tolist()

    if len(group_names)<3:
    	sys.exit('need at least 3 groups')

    ###########################
    ## get the means array
    k_group_means = np.array(k_group_means_file[1:,1:],dtype=float)
    k_group_min = np.min(k_group_means,axis=1)
    k_group_max = np.max(k_group_means,axis=1)
    k_group_range = k_group_max - k_group_min
    ## get the distance from max to second max
    dist_max_to_second = np.zeros((len(id_list)))
    q_value_vect = np.zeros((len(id_list)))
    for i in range(0,len(id_list)):
    	temp_sorted = np.sort(k_group_means[i,:])[::-1]
    	dist_max_to_second[i]=temp_sorted[0]-temp_sorted[1]
    	q_value_vect[i] = dist_max_to_second[i]/k_group_range[i]

    sorted_dist_to_max = np.sort(dist_max_to_second[:],kind="mergesort")
    index_for_cutoff = int(len(id_list)*percentile)
    dist_max_to_second_cutoff = sorted_dist_to_max[index_for_cutoff]

    ##########################
    ## 
    BH_corrected_aov_file = np.array(read_table(sig))
    BH_corrected_aov = np.array(BH_corrected_aov_file[1:,3],dtype=float)

    ##
    ## only consider significant genes
    sig_bool = BH_corrected_aov<sig_cutoff
    q_bool = q_value_vect>q_cutoff
    dist_to_second_max_bool = dist_max_to_second>dist_max_to_second_cutoff
    print('\n\n\nsig_bool',sig_bool,sum(sig_bool))
    print('q_bool',q_bool,sum(q_bool))
    print('dist_to_second_max_bool',dist_to_second_max_bool,sum(dist_to_second_max_bool))
    sig_q_and_dist = (np.array(sig_bool,dtype=int) + np.array(q_bool,dtype=int) + np.array(dist_to_second_max_bool,dtype=int))==3
    print('\ncombined\n',sig_q_and_dist)


    print('found',sum(sig_q_and_dist),'highly expressed, somewhat "exclusive" marker genes')

    print('making the output table...')

    out_file = [['gene','gene_symbol','gene_def', 'aov_BH_p', 'range', 'dist_from_max_to_second_max', 'q_value', 'specific_marker_for_group','best_match_group']]

    for i in range(0,len(id_list)):
        ## in the case of entrez IDs
        try:
            int(float(id_list[i]))
        except:
            temp_id = id_list[i]
        else:
            temp_id = str(int(float(id_list[i])))
        temp_line = []
        temp_line.append(temp_id)
        temp_line.append(process_symbol(symbol_dict[temp_id],temp_id))
        temp_line.append(process_def(def_dict[temp_id]))
        temp_line.append(BH_corrected_aov[i])
        temp_line.append(k_group_range[i])
        temp_line.append(dist_max_to_second[i])
        temp_line.append(q_value_vect[i])
        temp_line+=get_group(i,
                             sig_q_and_dist, 
                             group_names, 
                             k_group_max, 
                             k_group_means)
        out_file.append(temp_line)

    ## get the input for plot_subset...
    plot_subset_input = []
    for i in range(0,len(out_file)):
    	if out_file[i][-1]!="None":
    		plot_subset_input.append([out_file[i][0],out_file[i][1]])

    best_match_for_all_subset = get_best_match_for_all_subset(deepcopy(out_file),
                                                              group_names)

    subset_best_for_all_markers_file = os.path.join(out,"best_sorted_markers.tsv")
    subset_input_file = os.path.join(out,"subset_input.txt")
    print("out:",out)
    print("subset_input_file",subset_input_file)
    print("subset_best_for_all_markers_file",subset_best_for_all_markers_file)
    write_table(plot_subset_input,subset_input_file)
    write_table(best_match_for_all_subset, subset_best_for_all_markers_file)
    write_table(out_file,os.path.join(out,'marker_gene_annotations.tsv'))
    #cmd("plot_subset.py -i ""-plot_subset "+subset_input_file)
    return()


if __name__ ==  "__main__":
    parser = argparse.ArgumentParser()
    ## global arguments
    parser.add_argument(
        '-means','-m','-mean',
        dest='means',
        type=str)
    parser.add_argument(
        '-significance','-sig','-anovas','-anova', '-aov',
        dest='sig',
        type=str)
    parser.add_argument(
        '-out','-o',
        help = "output directory",
        dest='out',
        type=str)
    parser.add_argument(
        '-annotation_dict','-ad',
        dest='symbol_def_dict',
        type=str)
    args = parser.parse_args()
    get_marker_genes(symbol_def_dict=args.symbol_def_dict, 
                     means=args.means,
                     sig=args.sig,
                     out=args.out)

