#!python
import sys, os, glob, time
import numpy as np
import random
import scipy
from subprocess import Popen
from time import sleep
from scipy.sparse import csr_matrix, dok_matrix
from scipy.stats import spearmanr
from time import time
import fileinput,pickle
from scipy.stats import gaussian_kde, rankdata
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import h5py
from copy import deepcopy
try:
    from pyminer.common_functions import *
    from pyminer.pyminer_common_stats_functions import *
    from pyminer.pyminer_common_stats_functions import no_p_spear, get_Z_cutoff, get_empiric_FPR, get_linear_triangle#, get_empiric_log_odds_FPR
except:
    from common_functions import *
    from pyminer_common_stats_functions import *
    from pyminer_common_stats_functions import no_p_spear, get_Z_cutoff, get_empiric_FPR, get_linear_triangle#, get_empiric_log_odds_FPR

##################################################################################

def cutoff_check(r,p):
    global FPR, rho_cutoff, rho_cutoff_bool
    if rho_cutoff_bool:
        return(abs(r)>=rho_cutoff)
    else:
        return(p<=FPR)
    

#########

def get_spearman_h5(var_index):
    
    ## the offset is for a ! denoted header
    ## in general, this should be 1 because of the title line
    global temp, FPR, many_variables, IDlist, verbose, num_vars, infile
    
    output_lines = []
    cur_var_name1 = IDlist[var_index]
    for i in range(var_index+1,num_vars):
        if i%1000==0:
            print('\t',i)
        cur_var_name2 = IDlist[i]
        r,p=spearmanr(infile[var_index], infile[i])
        if cutoff_check(r,p):
            #print('found a relationship',r,p)
            output_lines.append([cur_var_name1, cur_var_name2, r])
            output_lines.append([cur_var_name2, cur_var_name1, r])
            #print(output_lines[-1])

    ## write status to temp log for this processes
    make_file("working on row "+str(var_index+1),log_file)

    
    if output_lines != []:
        return(output_lines)
    else:
        return(None)





##################################################################################
##############################################################
import argparse
parser = argparse.ArgumentParser()

parser.add_argument("-infile_path", '-i',
    help="the input dataset for making the adjacency list")
parser.add_argument("-adj_list_out", '-o',
    help="the ouptut adj list")
parser.add_argument("-id_list", '-ids',
    help="the file containing the IDs in the appropriate order")
parser.add_argument("-col_ids", "-cols","-columns","-column_ids",
    help="the file containing column IDs")
parser.add_argument("-rho_cutoff", '-rho',
    help="the cutoff to use for rho values",
    type = float)
parser.add_argument("-hdf5",
    action = 'store_true',
    default = False, 
    help="if the input file is in the hdf5 format")
parser.add_argument("-block_size",
    help = 'how many variables will be used at once for correlation analyzis; this helps keep memory requirements down and prevents a segmentation fault memory error',
     type = int,
     default = 5000)
parser.add_argument("-time",
    action = 'store_true',
    default = False, 
    help="if you only want to test the speed of relationship detection")
parser.add_argument("-sc_clust",
    action = 'store_true',
    default = False, 
    help="if scRNAseq clustering is going to be done")
parser.add_argument("-transpose",
    action = 'store_true',
    default = False, 
    help="if we're going to make an adjacency list on the columns rather than the rows")
parser.add_argument(
    "-rand_seed",'-seed',
    help='the random number input for random number seed, default = 12345',
    dest = 'rand_seed',
    type = int,
    default = 12345)

parser.add_argument("-hdf5_out",
    action = 'store_true',
    default = False, 
    help="if we want to make an hdf5 as the output instead of the rho dicts")
parser.add_argument("-euclidean_dist",
    action = 'store_true',
    default = False, 
    help="if we are going to also calculate the euclidean distance of all points against each other and store as an hdf5.")
parser.add_argument("-row_subset",
    help="a file with the row indices to include if we only want to do this on a subset of the rows. Note that this operation is performed before the transpose if need be.")
parser.add_argument(
    "-rho_dict_dir",
    help='the destination directory')

parser.add_argument(
    "-FPR_multiple",'-mult',
    help="the multiple to use for FPR based anti-correlation feature selection. Only use this if you really know what you're doing.",
    type = int,
    default = 15)
parser.add_argument(
    "-num_pos_cor_cutoff",
    help="the The minimum number of positive correlations that a gene must have to be included in the clustering. Default is 10. Only use this if you really know what you're doing.",
    type = int,
    default = 10)


parser.add_argument("-prop","-proportaionality",
    action = 'store_true',
    default = False, 
    help="if you only want to use proportionality instead of Spearman")


parser.add_argument("-log_odds","-lod",
    action = 'store_true',
    default = False, 
    help="if you only want to use proportionality instead of Spearman")

args = parser.parse_args()


np.random.seed(args.rand_seed)
random.seed(args.rand_seed)



## constants
FPR = 1000 ## 1 in 1000 false positive rate for negative correlation clustering
FPR_multiple = args.FPR_multiple ## the number of times the expected number of false positives to be included in clustering
pos_FPR = int(1e3)


do_sum_neg = args.sc_clust

##############################################################
args.infile_path = os.path.realpath(args.infile_path)
if args.adj_list_out is None:
    args.adj_list_out = os.path.join(os.path.dirname(args.infile_path), 'adj_list_rho.tsv')
print("adj list output will be:", args.adj_list_out)


rho_cutoff_bool = True
rho_cutoff = args.rho_cutoff

if args.log_odds:
    args.block_size = int(args.block_size/2)



##############

## run spearman analysis

infile_path=args.infile_path
if args.hdf5:
    h5f = h5py.File(infile_path, 'r')
    infile=h5f["infile"]
else:
	infile = np.array(read_table(infile_path))



if args.id_list is None and not args.hdf5:
    IDlist = list(infile[1:,0])
    col_ids = list(infile[0,1:])
    infile = np.array(infile[1:,1:],dtype = float)
elif args.id_list != None and not args.hdf5:
    infile = np.array(infile[1:,1:],dtype = float)
    ID_list = args.id_list
    IDlist = read_file(ID_list,'lines')
else:
    ID_list = args.id_list
    IDlist = read_file(ID_list,'lines')

## subset for the pertinent rows
if args.row_subset!=None:
    row_indices = read_file(args.row_subset,'lines')
    row_indices = sorted(list(map(int,row_indices)))
    infile = infile[row_indices,:]



## here's where we'll transpose the input
if args.transpose:
    if args.hdf5:
        infile = np.transpose(infile)
        IDlist = read_file(args.col_ids,'lines')[1:]# start at 1 because of the leader column
    else:
        infile = np.transpose(infile)
        IDlist = col_ids


num_vars = len(IDlist)
## sanity check that the ID list length is equal to the row num
if num_vars != np.shape(infile)[0]:
    print('the length of the ID list does not equal the number of rows in the input dataset')
    print("infile:",np.shape(infile)[0], )
    print("IDlist:",num_vars, IDlist[0:5])
    sys.exit()

index=0

temp_dir=str(infile_path).split('/')
temp_dir=('/').join(temp_dir[:-1])

bin_size = args.block_size
bin_size = min([bin_size,len(IDlist)])## this prevents the program from hitting index errors for small datasets


count=0


print('finding the spearman correlations for very big file')
print('this may take a while if your dataset has lots of variables...')

################################################
if args.rho_dict_dir==None:
    rho_dict_dir = temp_dir+'/rho_dicts'
else:
    rho_dict_dir = args.rho_dict_dir
process_dir(rho_dict_dir)
#########################################################

#output_lines = [["X_var","Y_var","Spearman_p_val","Spearman_rho"]]
output_lines = []


total_vars = len(IDlist)
print("total_vars",total_vars)
bins = []
cur_bin = 0
while cur_bin<total_vars:
	bins.append(min(cur_bin, total_vars))
	cur_bin+=bin_size

bins.append(total_vars)
if args.hdf5_out:
    print('making the hdf5 spearman output file')
    ## make the hdf5 output file
    hdf5_spear_out_file = rho_dict_dir+"/spearman.hdf5"
    print(hdf5_spear_out_file)
    #rm(hdf5_spear_out_file)
    
    spear_f = h5py.File(hdf5_spear_out_file, "a")
    try:
        spear_out_hdf5 = spear_f.create_dataset("infile", (total_vars,total_vars), dtype=np.float16)
    except:
        spear_out_hdf5 = spear_f["infile"]



print("input shape:",np.shape(infile))

print("bins:",bins)

########################################################
## define some plotting functions
def get_density(in_vect):
    in_vect = np.array(in_vect)
    in_vect = in_vect[np.array((np.isnan(in_vect)*-1)+1,dtype=bool)]## remove nans
    in_vect = in_vect[np.array((np.isinf(in_vect)*-1)+1,dtype=bool)]## remove infs
    offset = min(in_vect)
    #print(offset)
    in_vect = in_vect - offset
    #print(in_vect)
    density = gaussian_kde(in_vect)
    #print(in_vect)
    #print(density)
    xs = np.arange(0,max(in_vect),max(in_vect)/150)
    #print(xs)
    #density.covariance_factor = lambda : 2.5
    #density._compute_covariance()
    #print(density(xs))
    y = density(xs)
    y = y/sum(y)
    return(xs+offset,y)

def plot_one_density(neg_cor_density_x, neg_cor_density_y,out_file, label = 'negative correlation Rhos from bootstrap shuffled negative control'):
    global args
    x_min = np.min(neg_cor_density_x)
    y_min = np.min(neg_cor_density_y)
    x_max = np.max(neg_cor_density_x)
    y_max = np.max(neg_cor_density_y)

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = label,
        color = 'blue',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')
    return()

def plot_one_density_x_cutoff(neg_cor_density_x, neg_cor_density_y,cutoff,out_file,log = False,poisson_mu=None,label = "density"):
    global args
    from scipy.stats import poisson
    x_min = np.min(neg_cor_density_x)
    y_min = np.min(neg_cor_density_y)
    x_max = np.max(neg_cor_density_x)
    y_max = np.max(neg_cor_density_y)

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = label,
        color = 'blue',
        linewidth = 3)
    plt.plot([cutoff,cutoff],[y_min,y_max],
        color = 'k',
        lw = 2,
        label = 'cutoff')

    ## calculate the poisson at the given mu=cutoff
    if poisson_mu != None:
        temp_x = np.arange(x_max-x_min)+x_min
        dist = poisson(poisson_mu)
        plt.plot(np.log2(temp_x+1), np.log2(dist.pmf(temp_x)+1), ls='--', color='red',
                     label='poisson' , linestyle='steps-mid')
    plt.legend()

    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')
    return


def plot_densities(neg_cor_density_x, neg_cor_density_y,series_2_x,series_2_y,out_file):
    global args
    x_min = min([np.min(neg_cor_density_x),np.min(series_2_x)])
    y_min = min([np.min(neg_cor_density_y),np.min(series_2_y)])
    x_max = max([np.max(neg_cor_density_x),np.max(series_2_x)])
    y_max = max([np.max(neg_cor_density_y),np.max(series_2_y)])

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = 'sum of negative correlations per gene',
        color = 'blue',
        linewidth = 3)
    plt.plot(series_2_x, series_2_y, 
        label = 'bootstrap shuffled negative control',
        color = 'red',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')

def plot_avg_densities(neg_cor_density_x, neg_cor_density_y,series_2_x,series_2_y,out_file):
    global args
    x_min = min([np.min(neg_cor_density_x),np.min(series_2_x)])
    y_min = min([np.min(neg_cor_density_y),np.min(series_2_y)])
    x_max = max([np.max(neg_cor_density_x),np.max(series_2_x)])
    y_max = max([np.max(neg_cor_density_y),np.max(series_2_y)])

    plt.clf()
    plt.plot(neg_cor_density_x, neg_cor_density_y, 
        label = 'average Rho of negative correlations per gene',
        color = 'blue',
        linewidth = 3)
    plt.plot(series_2_x, series_2_y, 
        label = 'average Rho of negative correlations per boostrap negative control',
        color = 'red',
        linewidth = 3)
    plt.legend()
    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight')

def density_scatter(x,y,out_file,log_density=0,expected_x=[],expected_y=[]):
    ## remove points that are on the origin
    x=np.array(x)
    y=np.array(y)
    non_origin = (np.array(x==0, dtype = int) + np.array(y==0,dtype=int)) < 2
    x = x[non_origin].tolist()
    y = y[non_origin].tolist()
    if len(x)<2:
        return()
    xy = np.vstack([x,y])
    try:
        z = gaussian_kde(xy)(xy)
    except:
        print("error in getting the gaussian KDE")
        return()
    if log_density:
        while log_density:
            log_density-=1
            z = np.log2(z+1)
            z = z-min(z)
            z = z/max(z)
    plt.clf()
    fig, ax = plt.subplots()
    ax.scatter(x, y, c=z, s=5, edgecolor=[[0,0,0,0]]*len(x), cmap=plt.cm.jet)
    ###############################################
    if (expected_x is not []) and (expected_y is not []) :
        ax.plot(expected_x,expected_y,linestyle='-',c='black')
        plt.xlim((-1,max(x)+1))
        plt.ylim((0,max(y)+1))

    plt.savefig(out_file,
        dpi=600,
        bbox_inches='tight'
        )
    return

######################################################################


###################################################################
## this variable is if we're doing a global negative rho cutoff, or a variable one based on sparsity
single_cutoff = True
if not single_cutoff:
    ## This var is for keeping track of the sparsity of every gene
    gene_num_zero = np.zeros((total_vars))
    gene_non_zero_mean = np.zeros((total_vars))
    num_cells = infile.shape[1]

##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
## first we'll get the null background

def get_rho_cutoff_vect(r, neg_control_sample_idxs, gene_percent_express, out_dir):
    ## Probably won't use this function, but in case a reviewer is curious or something, we'll keep it here
    print("finding dynamic FPR")
    neg_ctrl_percent_express = gene_percent_express[neg_control_sample_idxs]
    list_of_percent_express = []
    list_of_negative_rhos = []
    for i in range(r.shape[0]):
        temp_neg_rhos = r[i,r[i,:]<0].tolist()
        list_of_negative_rhos += temp_neg_rhos
        list_of_percent_express += np.repeat(neg_ctrl_percent_express[i], len(temp_neg_rhos)).tolist()
    out_file = os.path.join(out_dir, "percentExpressX_vs_NullNegRhos.png")
    print("plotting subset percent express vs null negative Rho distributions")
    ################
    neg_control_sample_idxs = np.arange(len(list_of_percent_express))
    ## remove any genes that are zero in all samples
    np.random.shuffle(neg_control_sample_idxs)
    subset_idxs = neg_control_sample_idxs[:20000]
    ################
    print(len(list_of_percent_express))
    list_of_percent_express = np.array(list_of_percent_express)
    list_of_negative_rhos = np.array(list_of_negative_rhos)
    density_scatter(rankdata(list_of_percent_express[subset_idxs],method="dense"),list_of_negative_rhos[subset_idxs],out_file)
    sys.exit()
    return()


##########
## get the null
log_odds_correction = 0
if do_sum_neg or args.rho_cutoff==None or args.log_odds:
    ## run the bootstrap negative control for finding sum negative relationships
    ## first get a bin_size random set of variables to do the negative control on
    neg_control_sample_idxs = np.arange(len(IDlist))
    print(neg_control_sample_idxs)
    ## remove any genes that are zero in all samples
    non_zero_idxs = np.where(np.sum(infile,axis=1)>0)[0]
    neg_control_sample_idxs = neg_control_sample_idxs[non_zero_idxs]
    np.random.shuffle(neg_control_sample_idxs)
    #print(np.shape(neg_control_sample_idxs))
    neg_ctrl_bin_size = min([bin_size, np.shape(neg_control_sample_idxs)[0]])
    print("bin_size",neg_ctrl_bin_size)
    neg_control_sample_idxs = neg_control_sample_idxs[:neg_ctrl_bin_size]
    ##############################################################
    ## 11/14/2020
    ## add lowest & highest % expression to make sure we cover the whole range
    ## & don't cause an error with lowess later
    if not single_cutoff:
        percent_express_sorted_idxs = np.argsort(gene_percent_express)
        highest_percent_idx = percent_express_sorted_idxs[0]
        lowest_percent_idx = percent_express_sorted_idxs[percent_express_sorted_idxs.shape[0]-1]
        if highest_percent_idx not in neg_control_sample_idxs:
            neg_control_sample_idxs[0] = highest_percent_idx
        if lowest_percent_idx not in neg_control_sample_idxs:
            neg_control_sample_idxs[-1] = lowest_percent_idx
    ##############################################################
    neg_control_sample_idxs = neg_control_sample_idxs.tolist()
    neg_control_sample_idxs.sort()
    #print(np.shape(neg_control_sample_idxs))

    ## subset these IDs
    neg_control_subset_mat = np.array(infile[neg_control_sample_idxs,:])
    print('making negative control bootstrap shuffled matrix',np.shape(neg_control_subset_mat))

    ## go through each row and shuffle them within variables
    for i in range(0,np.shape(neg_control_subset_mat)[0]):
        temp_row_shuffle_order = np.arange(np.shape(neg_control_subset_mat)[1])
        np.random.shuffle(temp_row_shuffle_order)
        temp_row_shuffle_order = temp_row_shuffle_order.tolist()
        neg_control_subset_mat[i,:] = neg_control_subset_mat[i,temp_row_shuffle_order]

    ## get the spearman_rhos for the shuffled matrix
    print("neg_control_subset_mat shape:",np.shape(neg_control_subset_mat)[0])
    if np.shape(neg_control_subset_mat)[0]<2:
        ## this is likely a bad input, but handle it just in case it comes up
        r=np.zeros((neg_ctrl_bin_size,neg_ctrl_bin_size))
        linear_rho = np.zeros(neg_ctrl_bin_size)
        neg_cutoff=0
        FPR=0
        rho_cutoff = 0
        args.rho_cutoff = 0
    else:
        r=no_p_spear(neg_control_subset_mat, neg_control_subset_mat, axis = 1, prop=args.prop, log_odds = args.log_odds)#, log_odds_correction = log_odds_correction)
        linear_rho = get_linear_triangle(r[:neg_ctrl_bin_size,:neg_ctrl_bin_size], neg_ctrl_bin_size)
        #########################################
        ## THIS IS WHERE WE SET THE LOG-ODDS BIAS CORRECTION. It's just the median of the null distribution to center it & future comparisons
        if args.log_odds:
            log_odds_correction = np.median(linear_rho)
            print("\n\n\nlog_odds_correction:", log_odds_correction,"\n\n\n\n")
            linear_rho -= log_odds_correction
        else:
            log_odds_correction = 0
        #########################################
        print("min of negative control is now:", np.min(linear_rho))
        print("median of negative control is now:", np.median(linear_rho))
        print("max of negative control is now:", np.max(linear_rho))
        print("rho shape",np.shape(r))
        
        if single_cutoff:
            print("linear_rho.shape:",linear_rho.shape)
            neg_idxs = np.where(linear_rho<0)[0]
            print("np.where(linear_rho<0)",np.where(linear_rho<0))
            pos_idxs = np.where(linear_rho>0)[0]
            negative_control_negative_rho_vect = linear_rho[neg_idxs]
            negative_control_positive_rho_vect = linear_rho[pos_idxs]
            #calculate_mad(negative_control_negative_rho_vect)

            ## plot the average Rho per negative correlation
            #print(negative_control_negative_rho_vect)
            
            if not args.transpose:
                neg_cor_density_x, neg_cor_density_y = get_density(negative_control_negative_rho_vect)
                pos_cor_density_x, pos_cor_density_y = get_density(negative_control_positive_rho_vect)
                ## this is only for gene-gene correlations, not sample-sample
                print(args.adj_list_out)
                out_dir = os.path.dirname(args.adj_list_out)
                sum_neg_plot = os.path.join(out_dir,'boostrap_neg_cor_rhos.png')
                print("plotting boostrap_neg_cor_rhos.png")
                plot_one_density(neg_cor_density_x, neg_cor_density_y, sum_neg_plot, label="density of negative correlation null distribution")
                pos_rho_plot = os.path.join(out_dir,'boostrap_pos_cor_rhos.png')
                print("plotting boostrap_pos_cor_rhos.png")
                plot_one_density(pos_cor_density_x, pos_cor_density_y,pos_rho_plot, label="density of positive correlation null distribution")

                ## plot the distribution of all bootstrap negative control Rhos
                neg_cor_density_x, neg_cor_density_y = get_density(linear_rho)
                sum_neg_plot = os.path.join(out_dir,'boostrap_cor_rhos.png')
                print("plotting boostrap_cor_rhos.png")
                plot_one_density(neg_cor_density_x, neg_cor_density_y, sum_neg_plot,label="density of all correlation null distribution")

            print("\n\ncalculating negative correlation FPR cutoff from null distribution:")
            #neg_cutoff = get_FPR_cutoff(negative_control_negative_rho_vect,FPR)
            #neg_cutoff, FPR = get_Z_cutoff(negative_control_negative_rho_vect, z=3)
            if args.log_odds:
                neg_cutoff, FPR = get_empiric_FPR(negative_control_negative_rho_vect)
            else:
                neg_cutoff, FPR = get_empiric_FPR(negative_control_negative_rho_vect)
            print('\nEmpiric FPR for anti-corr:',FPR)
            print('\nEmpiric neg_cutoff for anti-corr:',neg_cutoff)
            print("\n\ncalculating adj list FPR cutoffs from null distribution:")
            #pos_cutoff = get_FPR_cutoff(negative_control_positive_rho_vect,pos_FPR, positive = True)
            if args.log_odds:
                pos_z_cut = 3.0
                pos_cutoff = get_Z_cutoff(negative_control_positive_rho_vect, z=pos_z_cut, positive = True, cap=None)
                neg_cutoff_adj_list, dummy = get_Z_cutoff(negative_control_negative_rho_vect, z=pos_z_cut, positive = False, cap=None)
            else:
                pos_z_cut = 5.5
                pos_cutoff = get_Z_cutoff(negative_control_positive_rho_vect, z=pos_z_cut, positive = True)
                neg_cutoff_adj_list, dummy = get_Z_cutoff(negative_control_negative_rho_vect, z=pos_z_cut, positive = False)
            rho_cutoff = pos_cutoff
            args.rho_cutoff = pos_cutoff
            #sys.exit()
        else:
            ##############################################################
            ## this means that we just have a dynamic negative rho cutoff as determined by gene expression sparsity
            rho_cutoff_vect, FPR_vect = get_rho_cutoff_vect(r, neg_control_sample_idxs, gene_non_zero_mean, os.path.dirname(args.adj_list_out))
    ##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
## Do all of the comparisons

start = time.time()
if total_vars==bins[1] and args.hdf5_out:
    print("total num vars is equal to the number of bins, so we'll do it in one go")
    r=no_p_spear(infile[:,:], axis = 1, prop=args.prop, log_odds = args.log_odds, log_odds_correction = log_odds_correction)
    print(r.shape)
    print(spear_out_hdf5.shape)
    spear_out_hdf5[:,:]=r[:,:]
else:
    print("finding block...")
    for i in range(0,(len(bins)-1)):
        temp_first = infile[bins[i]:bins[i+1],]
        if not single_cutoff:
            gene_num_zero[bins[i]:bins[i+1]] = np.sum(temp_first==0,axis=1)
            gene_non_zero_mean[bins[i]:bins[i+1]] = np.sum(temp_first,axis=1) / (num_cells - gene_num_zero[bins[i]:bins[i+1]])
        for j in range(i,(len(bins)-1)):
            if (i!=j) or (len(bins) == 2):#True:
                out_rho_dict = rho_dict_dir+"/rho_"+str(bins[i])+"_to_"+str(bins[i+1])+"_vs_"+str(bins[j])+"_to_"+str(bins[j+1])+".pkl"

                ## if we're writing to an hdf5 file, check if the values are already entered
                if args.hdf5_out:
                    #do_top_left = np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]]==0)
                    #do_top_right = np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0)
                    #do_bottom_left = np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0)
                    #do_bottom_right = np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]]==0)
                    do_top_left = np.all(spear_out_hdf5[bins[i],bins[i]:bins[i+1]]==0)
                    do_top_right = np.all(spear_out_hdf5[bins[i],bins[j]:bins[j+1]]==0)
                    do_bottom_left = np.all(spear_out_hdf5[bins[j],bins[i]:bins[i+1]]==0)
                    do_bottom_right = np.all(spear_out_hdf5[bins[j],bins[j]:bins[j+1]]==0)
                    do_one = (do_top_left or do_top_right or do_bottom_left or do_bottom_right)
                    print(do_top_left , do_top_right , do_bottom_left , do_bottom_right)
                    #print(spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]])
                else:
                    do_one = False
                
                #print((not os.path.exists(out_rho_dict) and not args.hdf5_out) , (args.hdf5_out and do_one))
                #sys.exit()
                if (not os.path.exists(out_rho_dict) and not args.hdf5_out) or (args.hdf5_out and do_one):
                    ## find the spearman correlations

                    print('working on',bins[i],bins[i+1],'vs',bins[j],bins[j+1], "prop:",args.prop, "log_odds:",args.log_odds,log_odds_correction)
                    r=no_p_spear(temp_first,infile[bins[j]:bins[j+1],:], axis = 1, prop=args.prop, log_odds = args.log_odds, log_odds_correction = log_odds_correction)
                    
                    ## if we're not making the spearman correlation matrix into an hdf5 file - save the dictionary:
                    if not args.hdf5_out:
                        save_dict(r,out_rho_dict)

                    ## if we are making the spearman correlation matrix an hdf5 file, we've got some work to do:
                    else:
                        #print(np.shape(r))
                        if np.shape(r)[0] == 2*bin_size:
                            #print('is symmetric:',r[bin_size:,bin_size:] == r[:bin_size,:bin_size])
                            if len(bins)==2:#False#np.shape(r)[0]<=bin_size:
                                ## there is a special case, where the number of variables is less than the
                                ## bin size. In this case, the returned matrix will be symmetric in all 4
                                ## quadrants, so we'll reduce it down to just the one
                                r = r[bin_size:,bin_size:]
                        #print(np.shape(r))


                        ## because h5py's fancy indexing doesn't work very well with slicing in 2D...

                        ## first set the top left corner bins
                        if np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]]==0):
                            print("setting top left")
                            # temp_r = np.array(r[:bin_size,:bin_size],dtype=np.float16)
                            # print(temp_r.shape)
                            print(bins[i],bins[i+1])
                            print()
                            if spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]].shape[0]-1==r[:bin_size,:bin_size].shape[0]:
                                spear_out_hdf5[bins[i]:bins[i+1]-1,bins[i]:bins[i+1]-1] = np.array(r[:bin_size,:bin_size],dtype=np.float16)
                            else:
                                spear_out_hdf5[bins[i]:bins[i+1],bins[i]:bins[i+1]] = np.array(r[:bin_size,:bin_size],dtype=np.float16)
                        
                        ## top right
                        if len(bins)!=2:
                            try:
                                if np.all(spear_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0):
                                    print("setting top right")
                                    spear_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]] = np.array(r[:bin_size,bin_size:],dtype=np.float16)
                            except:
                                print(sys.exit('error setting the top right'))
                                pass
                        
                        ## bottom left
                        if len(bins)!=2:
                            try:
                                if np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0):
                                    print('setting bottom left')
                                    spear_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1],] = np.array(r[bin_size:,:bin_size],dtype=np.float16)
                            except:
                                print(sys.exit('error setting the bottom left'))
                                pass
                        
                        ## bottom right
                        if len(bins)!=2:
                            try:
                                if np.all(spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]]==0):
                                    print('setting bottom right')
                                    spear_out_hdf5[bins[j]:bins[j+1],bins[j]:bins[j+1]] = np.array(r[bin_size:,bin_size:],dtype=np.float16)
                            except:
                                print(sys.exit('error setting the bottom right'))
                                pass
                else:
                    print('already finished block',bins[i],bins[i+1],'vs',bins[j],bins[j+1])

end = time.time()

######################
## finish cateloguing the number of zeros
if not single_cutoff:
    temp_first = infile[bins[-1]:,]
    gene_num_zero[bins[-1]:] = np.sum(temp_first==0,axis=1)
    gene_non_zero_mean[bins[-1]:] = np.sum(temp_first,axis=1) / (num_cells - gene_num_zero[bins[-1]:])
    gene_percent_express = (num_cells - gene_num_zero)/num_cells
######################


##############################################################################################################################################
##############################################################################################################################################
##############################################################################################################################################
## If we're doing the Euclidean distance of the Spearman distances, then calculate them here
if args.euclidean_dist:
    from sklearn import metrics
    euclidean_distances = metrics.pairwise.euclidean_distances
    print('making the negative euclidean distance matrix')
    ## make the euclidean distance output matrix
    ## make the hdf5 output file
    hdf5_euc_out_file = rho_dict_dir+"/neg_euc_dist.hdf5"
    print(hdf5_euc_out_file)
    euc_f = h5py.File(hdf5_euc_out_file, "a")
    ## set up the data matrix (this assumes float32)
    float_type = np.float16
    try:
        neg_euc_out_hdf5 = euc_f.create_dataset("infile", (total_vars,total_vars), dtype=float_type)
    except:
        neg_euc_out_hdf5 = euc_f["infile"]
    # else:
    #     neg_euc_out_hdf5 = euc_f.create_dataset("infile", (total_vars,total_vars), dtype=np.float32)
    # ## go through and calculate the negative euclidean distances
    ###########################
    spear_min = 99999
    temp_start=int(0)
    temp_end=int(args.block_size)
    print("calculating the minimum non-zero Spearman rho")
    while temp_end < spear_out_hdf5.shape[0]:
        print(round(100*temp_start/spear_out_hdf5.shape[0],2),"% ","done")
        spear_min=min([spear_min,np.nanmin(spear_out_hdf5[temp_start:temp_end,:])/np.log2(total_vars)])
        temp_start+=args.block_size
        temp_end+=args.block_size
    ## catch the last bit
    spear_min=min([spear_min,np.nanmin(spear_out_hdf5[temp_start:,:])])
    #spear_min = np.nanmin(spear_out_hdf5)/np.log2(total_vars)
    print("spear_min",spear_min)
    ###########################
    for i in range(0,(len(bins)-1)):
        for j in range(i,(len(bins)-1)):
            #print(np.all(neg_euc_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0) , np.all(neg_euc_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0))
            if (np.all(neg_euc_out_hdf5[bins[i],bins[j]:bins[j+1]]==0) and np.all(neg_euc_out_hdf5[bins[j],bins[i]:bins[i+1]]==0)):
                print('calculating negative euclidean distance for',bins[i],bins[i+1],'vs',bins[j],bins[j+1])
                #temp_neg_euc = -euclidean_distances(np.array(spear_out_hdf5[bins[i]:bins[i+1],:],dtype=np.float32),np.array(spear_out_hdf5[bins[j]:bins[j+1],:],dtype=np.float32),squared=True)
                #temp_neg_euc = -euclidean_distances(np.array(spear_out_hdf5[bins[i]:bins[i+1],:],dtype=float_type),np.array(spear_out_hdf5[bins[j]:bins[j+1],:],dtype=float_type),squared=True)/np.log2(total_vars)
                temp_subset_mat_1 = np.array(spear_out_hdf5[bins[i]:bins[i+1],:],dtype=float_type)/np.log2(total_vars)
                temp_subset_mat_2 = np.array(spear_out_hdf5[bins[j]:bins[j+1],:],dtype=float_type)/np.log2(total_vars)
                #print('before')
                #print(temp_subset_mat_1[np.where(np.isnan(temp_subset_mat_1))])
                temp_subset_mat_1[np.where(np.isnan(temp_subset_mat_1))]=spear_min
                #print(temp_subset_mat_1[np.where(np.isnan(temp_subset_mat_1))])
                #print('after')
                temp_subset_mat_2[np.where(np.isnan(temp_subset_mat_2))]=spear_min
                #print(temp_subset_mat_1)
                #print(temp_subset_mat_2)
                num_nan_1 = np.sum(np.isnan(temp_subset_mat_1))
                num_inf_1 = np.sum(np.isinf(temp_subset_mat_1))
                num_nan_2 = np.sum(np.isnan(temp_subset_mat_2))
                num_inf_2 = np.sum(np.isinf(temp_subset_mat_2))
                if num_nan_1+num_inf_1+num_nan_2+num_inf_2 >0:
                    print('num_nan_1:',num_nan_1)
                    print('num_inf_1:',num_inf_1)
                    print('num_nan_2:',num_nan_2)
                    print('num_inf_2:',num_inf_2)
                else:
                    pass#print('no nans or infs')
                temp_neg_euc = -euclidean_distances(temp_subset_mat_1,temp_subset_mat_2)*np.log2(total_vars)
                neg_euc_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]] = temp_neg_euc
                neg_euc_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]] = np.transpose(temp_neg_euc)
                #print(temp_neg_euc)
                #print(neg_euc_out_hdf5[:,:])
                #neg_euc_out_hdf5 = np.transpose(temp_neg_euc)
                #print(np.all(neg_euc_out_hdf5[bins[i]:bins[i+1],bins[j]:bins[j+1]]==0) , np.all(neg_euc_out_hdf5[bins[j]:bins[j+1],bins[i]:bins[i+1]]==0))
            else:
                print('already finished',bins[i],bins[i+1],'vs',bins[j],bins[j+1])
    for i in range(0,np.shape(neg_euc_out_hdf5)[0]):
        neg_euc_out_hdf5[i,i]=-0.0

    euc_f.close()



if args.hdf5_out:
    ## close the hdf5 file
    spear_f.close()


if args.time:
    print((end-start)/60,'minutes spent finding correlations')
    sys.exit()


###############################################################



################################################################################
## read in the ID list
print('logging all the IDs')

ID_hash = {}
for i in range(0,len(IDlist)):
	ID_hash[IDlist[i]] = i
	

################################################################################
## get the rho dictionaries

## parse the name of the file to get the 
def parse_dict_name(dict_path):
	dict_path = dict_path.split('/')
	dict_path = dict_path[-1]
	dict_path = dict_path.strip('rho_')
	dict_path = dict_path.strip('.pkl')
	dict_path = dict_path.split('_vs_')
	dict_path[0] = dict_path[0].split('_to_')
	dict_path[1] = dict_path[1].split('_to_')
	dict_path[0][0]=int(dict_path[0][0])
	dict_path[0][1]=int(dict_path[0][1])
	dict_path[1][0]=int(dict_path[1][0])
	dict_path[1][1]=int(dict_path[1][1])
	temp_id_indices = np.concatenate((np.arange(dict_path[0][0],dict_path[0][1]),np.arange(dict_path[1][0],dict_path[1][1])))
	temp_IDs=[IDlist[i] for i in temp_id_indices]
	return((temp_id_indices,temp_IDs))

rho_properties_dict = {}
rho_files = []
for glob in glob.glob(rho_dict_dir+'/*.pkl'):
	rho_files.append(glob)
	rho_properties_dict[glob]=parse_dict_name(glob)
	#print(glob,'\n',rho_properties_dict[glob])

	
################################################################################
## make the adjacency list
print('making the adjacency list')
    
## make the output file
rm(args.adj_list_out)
rm(args.adj_list_out[:-4]+"_dedup.tsv")
out_file_name = args.adj_list_out[:-4]+"_dedup.tsv"
out_file = open(out_file_name, "a")

#out_file.write('\t'.join(['var_1', 'var_2', 'NA', 'NA','NA','NA','rho'])+'\n')
if args.log_odds:
    out_file.write('\t'.join(['var_1', 'var_2', 'rLog(OR)'])+'\n')
elif args.prop:
    out_file.write('\t'.join(['var_1', 'var_2', 'phi_proportionality'])+'\n')
else:
    out_file.write('\t'.join(['var_1', 'var_2', 'rho'])+'\n')



#################
## look at the sum of all negative correlations
sum_neg = []
#all_vars_adj_dict = {}
#neg_vars_adj_dict = {}
#total_neg_vars_adj_dict = {}
num_vars = len(IDlist)
all_vars_adj_dict = dok_matrix((num_vars,num_vars),dtype = bool)
#neg_vars_adj_dict = csr_matrix((num_vars,num_vars),dtype = bool)
total_neg_vars_adj_dict = dok_matrix((num_vars,num_vars),dtype = bool)
for i in range(0,len(IDlist)):
    ## [ID, sum_negative_rho, count_below_threshold, total_number_negative, (count_below_threshold+1)/(count_above_threshold +1)] # later we also append to this line a T/F pass call
    sum_neg.append([IDlist[i],0,0,0,0])
    # all_vars_adj_dict[IDlist[i]] = np.zeros(len(IDlist,),dtype = bool)
    # neg_vars_adj_dict[IDlist[i]] = np.zeros(len(IDlist,),dtype = bool)
    # total_neg_vars_adj_dict[IDlist[i]] = np.zeros(len(IDlist,),dtype = bool)
#################



num_pos_cor_dict = {str(temp_id):0 for idx, temp_id in enumerate(IDlist)}## This used to be in the loop
for rho in rho_files:
    ## go through all the rho dict files
    print('reading in', rho)
    temp_rho_mat = import_dict(rho)
    temp_indices, temp_IDs = rho_properties_dict[rho]
    for i in range(0,np.shape(temp_rho_mat)[0]):
        ## go through each line in the rho matrix and log the pertinent indices
        cur_var_1 = temp_IDs[i]
        cur_var_1_index = ID_hash[cur_var_1]
        #print("pos cutoff:",args.rho_cutoff)
        sig_indices = np.where(temp_rho_mat[i,:]>=args.rho_cutoff)[0].tolist()
        #print("neg cutoff:",neg_cutoff_adj_list)
        sig_indices +=  np.where(temp_rho_mat[i,:]<=neg_cutoff_adj_list)[0].tolist()
        sig_IDs = [temp_IDs[j] for j in sig_indices]
        sig_rhos = temp_rho_mat[i,sig_indices]
        ## go through the significant indicies
        for q in range(0,len(sig_IDs)):
            var2_idx = ID_hash[sig_IDs[q]]
            if cur_var_1_index > var2_idx:
                ## check if variable pair has been done already
                #temp_relationships = all_vars_adj_dict[cur_var_1,:]
                ## check if it has been done (ie: currently set to zero.)
                #print(cur_var_1)
                #print(var2_idx)
                if all_vars_adj_dict[cur_var_1_index,var2_idx] == False:
                    all_vars_adj_dict[cur_var_1_index,var2_idx]=True## this is the indicator that we've doen it already
                    #all_vars_adj_dict[cur_var_1] = temp_relationships
                    #temp_out_line = [str(cur_var_1), str(sig_IDs[q]), 'NA', 'NA','NA','NA',str(sig_rhos[q])]
                    temp_out_line = [str(cur_var_1), str(sig_IDs[q]), str(sig_rhos[q])]
                    out_file.write('\t'.join(temp_out_line)+'\n')
                    ## also log the positive correlations
                    num_pos_cor_dict[str(cur_var_1)] = 1 + num_pos_cor_dict[str(cur_var_1)] 
                    num_pos_cor_dict[str(sig_IDs[q])] = 1 + num_pos_cor_dict[str(sig_IDs[q])] 
        if do_sum_neg:
            ## do the same for all of the negative correlations, regardless of magnitude
            total_negative_indices = np.where(temp_rho_mat[i,:]<0)[0] ## negative gobal indices relative to current gene
            neg_IDs = [temp_IDs[j] for j in total_negative_indices] ## other variable's names
            neg_rhos = temp_rho_mat[i,total_negative_indices]
            for q in range(0,len(neg_rhos)):
                cur_var_2 = neg_IDs[q]
                cur_var_2_index = ID_hash[neg_IDs[q]]
                if cur_var_1_index < cur_var_2_index:
                    if (cur_var_1 =="Gene1" or cur_var_1 == "Gene2" or cur_var_2 =="Gene1" or cur_var_2 == "Gene2") and (len(cur_var_1)<=7 and len(cur_var_2)<=7):
                        local_verbose = False
                        #print("cur_var_1",cur_var_1,"\tvs\t",cur_var_2)
                    else:
                        local_verbose = False
                    ## check if variable pair has been done already
                    #temp_relationships = total_neg_vars_adj_dict[cur_var_1] ## pull the boolean cateloge of what's been done
                    #temp_relationships2 = total_neg_vars_adj_dict[cur_var_2] ## pull the boolean cateloge of what's been done
                    #if temp_relationships[cur_var_2_index] == False and temp_relationships2[cur_var_1_index] == False: ## meaning we haven't check this pair yet
                    if total_neg_vars_adj_dict[cur_var_1_index,cur_var_2_index] == False and total_neg_vars_adj_dict[cur_var_2_index,cur_var_1_index] == False:
                        ## housekeeping to keep track of which variables we've already done
                        #temp_relationships[cur_var_2_index] = True ## first log that we have now done the comparison
                        #temp_relationships2[cur_var_1_index] = True
                        #total_neg_vars_adj_dict[cur_var_1] = temp_relationships ## set it again
                        #total_neg_vars_adj_dict[cur_var_2] = temp_relationships2
                        total_neg_vars_adj_dict[cur_var_1_index,cur_var_2_index] = True
                        total_neg_vars_adj_dict[cur_var_2_index,cur_var_1_index] = True
                        ########################
                        ## now log the results
                        sum_neg[cur_var_1_index][3]+=1 ## this is the total number of negative correlations
                        sum_neg[cur_var_2_index][3]+=1 ## this is the total number of negative correlations
                        ## then if it's actually less than the simulation determined cutoff, log it for that as well
                        #######################################################
                        ## 11/14/2020 this is where we can change the cutoff to be dynamic depending on the percent express
                        #######################################################
                        if single_cutoff:
                            if neg_rhos[q] < neg_cutoff:# and neg_rhos[q]>-1 :
                                sum_neg[cur_var_1_index][1]+=neg_rhos[q] ## this is the number of "significant" negative correlations
                                sum_neg[cur_var_2_index][1]+=neg_rhos[q] ## this is the number of "significant" negative correlations

                                ## total number < auto-determined Rho cutoff from bootstrap shuffled negative correlations
                                sum_neg[cur_var_1_index][2]+=1
                                sum_neg[cur_var_2_index][2]+=1
                                if local_verbose:
                                    print("\trho:",neg_rhos[q])
                                    print("\ttotal_neg_vars_adj_dict[cur_var_1]",total_neg_vars_adj_dict[cur_var_1])
                                    print("\ttotal_neg_vars_adj_dict[cur_var_2]", total_neg_vars_adj_dict[cur_var_2])
                                    print("\tsum_neg[cur_var_1_index][3]",sum_neg[cur_var_1_index][3])
                                    print("\tsum_neg[cur_var_2_index][3]",sum_neg[cur_var_2_index][3])
                                    print("\tsum_neg[cur_var_1_index][1]",sum_neg[cur_var_1_index][1])
                                    print("\tsum_neg[cur_var_2_index][1]",sum_neg[cur_var_2_index][1])
                                    print("\tsum_neg[cur_var_1_index][2]",sum_neg[cur_var_1_index][2])
                                    print("\tsum_neg[cur_var_2_index][2]",sum_neg[cur_var_2_index][2])

                        else:
                            ## if it's less than the i variable's cutoff
                            if neg_rhos[q] < neg_cutoff_vect[cur_var_1_index]:
                                sum_neg[cur_var_1_index][1]+=neg_rhos[q] ## this is the number of "significant" negative correlations
                                ## total number < auto-determined Rho cutoff from bootstrap shuffled negative correlations
                                sum_neg[cur_var_1_index][2]+=1
                            if neg_rhos[q] < neg_cutoff_vect[cur_var_2_index]:
                                sum_neg[cur_var_2_index][1]+=neg_rhos[q] ## this is the sum of all of the negative rhos - turned out to be less useful
                                ## total number < auto-determined Rho cutoff from bootstrap shuffled negative correlations
                                sum_neg[cur_var_2_index][2]+=1 ## this is the number of "significant" negative correlations

out_file.close()


def pass_cutoff(above, total, num_pos_cor, num_pos_cor_cutoff = 10):
    global FPR,FPR_multiple, expected_x, expected_y
    ## the FPR variable is really the denominator of the actuall false positive rate. 
    ## This means that 1 in every FPR negative correlations should exceed the cutoff
    ## purely by chance.
    ## So , 
    this_genes_number_of_expected = total*(1/FPR)
    this_genes_multiple_of_expected_cutoff = this_genes_number_of_expected * FPR_multiple
    # print("\tabove:", above,"total:",total, "FPR:",FPR, "FPR_multiple:",FPR_multiple)
    # print("\tthis_genes_number_of_expected:",this_genes_number_of_expected)
    # print("\tthis_genes_multiple_of_expected_cutoff:",this_genes_multiple_of_expected_cutoff)
    # print("\tpassing?:",above > this_genes_multiple_of_expected_cutoff)
    if above < 1:#10:
        return("False")
    #elif total/above < (FPR/FPR_multiple) and num_pos_cor >= num_pos_cor_cutoff:
    elif (above > this_genes_multiple_of_expected_cutoff) and num_pos_cor >= num_pos_cor_cutoff:
        return("True")
    else:
        return("False")


if do_sum_neg:
    ## sum up the negative correlations for the bootstrap shuffled negative control
    negative_control_sum_neg = []
    negative_control_count_neg = []
    for i in range(0,np.shape(r)[0]):
        neg_indices = np.where(r[i,:]<0)[0]
        count_neg = np.shape(neg_indices)[0]
        negative_control_count_neg.append(count_neg)
        sum_neg_rhos = sum(r[i,neg_indices])
        negative_control_sum_neg.append(sum_neg_rhos)

    ## calculate the average per comparison for each gene, then multiply it by the number of comparisons 
    ## in the full dataset. This extrapolates the subset to the size of the full dataset.
    ## this will then be used to dynamicaly set the cutoff of what counts as a negative correlation 
    ## at the desired FDR (default FDR = 0.05)
    #print("negative_control_sum_neg",negative_control_sum_neg)
    #print("negative_control_count_neg",negative_control_count_neg)
    negative_control_avg_neg = np.array(negative_control_sum_neg)/np.array(negative_control_count_neg)
    negative_control_sum_neg = (np.array(negative_control_sum_neg)/bin_size)*len(IDlist)
    #negative_control_avg_neg = 
    max_neg_ctr = max(negative_control_sum_neg)
    print("max of the negative control =",max_neg_ctr)


    ######################################################################################
    ## process the sum negative table into a vector so that we can do interesting things with it
    #print(sum_neg[:10])
    sum_neg_vect = np.zeros(len(sum_neg),dtype = float)
    sum_neg_count = np.zeros(len(sum_neg),dtype = float)
    sum_neg_count_total = np.zeros(len(sum_neg),dtype = float)
    non_sig_neg_count = np.zeros(len(sum_neg),dtype = float)
    for i in range(0,len(sum_neg)):
        sum_neg_vect[i]=sum_neg[i][1]
        sum_neg_count[i]=sum_neg[i][2]
        sum_neg_count_total[i]=sum_neg[i][3]
        non_sig_neg_count[i] = sum_neg[i][3] - sum_neg[i][2]

    sum_neg_vect = np.array(sum_neg_vect)
    sum_neg_count = np.array(sum_neg_count)
    sum_neg_count_total = np.array(sum_neg_count_total)
    count_above_threshold = sum_neg_count_total - sum_neg_count
    count_above_below_ratio = (sum_neg_count+1)/(count_above_threshold+1)

    ## log the ratios in the output file
    for i in range(0,len(sum_neg)):
        sum_neg[i][4]=count_above_below_ratio[i]

    avg_neg = sum_neg_vect/sum_neg_count
    #print(sum_neg_vect[:10])


    ## neg count
    #print('\n\t\tcalculating median absolute deviation for the total significant negative count')
    # given the total number of observed negative correlations (expected_y)
    print("max of sum_neg_count_total",np.max(sum_neg_count_total))
    expected_y = np.arange(np.max(sum_neg_count_total))
    expected_x = expected_y/(FPR/FPR_multiple)
    expected_x = np.log2(expected_x)
    expected_x = expected_x[1:]
    expected_y = expected_y[1:]
    #print(expected_y)
    #print(expected_x)
    #sys.exit()
    sum_neg_count = np.log2(sum_neg_count+1)
    #med,med_dev,cutoff = calculate_mad(sum_neg_count,mean=False)

    ## append whether or not they passed the cutoff to the summary matrix
    #[ID, sum_negative_rho, count_below_threshold, total_number_negative, (count_below_threshold+1)/(count_above_threshold +1)]
    included_indices = []
    for i in range(0,len(sum_neg)):
        #print(sum_neg[i][0])
        sum_neg[i].append(pass_cutoff(sum_neg[i][2],sum_neg[i][3], num_pos_cor_dict[sum_neg[i][0]], num_pos_cor_cutoff = args.num_pos_cor_cutoff))
        if eval(sum_neg[i][-1]):
            included_indices.append(i)
        # sum_neg[]
        # temp_pass = "False"
        # if sum_neg_count[i] > np.log2(expected_false_positives+1):
        #     temp_pass = "True"
        # sum_neg[i].append(temp_pass)


    # ## plot the average Rho per negative correlation
    # neg_cor_density_x, neg_cor_density_y = get_density(avg_neg)
    # series_2_x, series_2_y = get_density(negative_control_sum_neg)
    
    # sum_neg_plot = os.path.dirname(args.adj_list_out)+'/avg_neg_cor.png'
    # plot_densities(neg_cor_density_x, neg_cor_density_y, series_2_x, series_2_y, sum_neg_plot) 

    ## plot the ratio of negative correlations below and above the bootstrap shuffled determined cutoff
    print('count_above_below_ratio',count_above_below_ratio)
    neg_cor_density_x, neg_cor_density_y = get_density(count_above_below_ratio)
    
    sum_neg_plot = os.path.dirname(args.adj_list_out)+'/ratio_of_neg_cor_above_below_cutoff.png'
    plot_one_density(neg_cor_density_x, neg_cor_density_y, sum_neg_plot) 

    ## plot the counts of negative correlations against
    neg_cor_density_x, neg_cor_density_y = get_density(count_above_below_ratio)
    
    sum_neg_plot = os.path.dirname(args.adj_list_out)+'/ratio_of_neg_cor_above_below_cutoff.png'
    plot_one_density_x_cutoff(neg_cor_density_x, neg_cor_density_y, 1/1000, sum_neg_plot) 

    ## plot the counts of significant vs non-significant
    count_sig_vs_non_sig = os.path.dirname(args.adj_list_out)+'/sig_neg_count_vs_total_neg_count.png'
    density_scatter(sum_neg_count,sum_neg_count_total,count_sig_vs_non_sig,log_density=4,expected_x=expected_x,expected_y=expected_y)
    count_sig_vs_non_sig = os.path.dirname(args.adj_list_out)+'/sig_neg_count_vs_total_neg_count_included_only.png'
    if len(included_indices)>0:
        density_scatter(sum_neg_count[included_indices],sum_neg_count_total[included_indices],count_sig_vs_non_sig,log_density=4,expected_x=expected_x,expected_y=expected_y)



    ## write the results to file
    sum_neg_out = os.path.dirname(args.adj_list_out)+'/sum_neg_cor.txt'
    write_table(sum_neg,sum_neg_out)

###############################################
## copied over from pyminer.py
out_adj = args.adj_list_out

pos_neg_count = np.zeros((len(IDlist),2))

out_adj_pos = out_adj[:-4]+'_dedup_pos.tsv'
rm(out_adj_pos)
pos_f_out=open(out_adj_pos,'a')

out_adj_neg = out_adj[:-4]+'_dedup_neg.tsv'
rm(out_adj_neg)
neg_f_out=open(out_adj_neg,'a')

counter = 0
first = True
for line in fileinput.input(out_adj[:-4]+'_dedup.tsv'):
    if first:
        print('reading ',out_adj[:-4]+'_dedup.tsv')
        #print(float(temp_line[-1]))
        pos_f_out.write(line)
        neg_f_out.write(line)
        first = False
    else:
        temp_line = strip_split(line)
        #print(float(temp_line[-1]))
        try:
            float(temp_line[-1])
        except:
            print('error at line:',counter)
            print('\t',line)
        if float(temp_line[-1])>0:
            pos_f_out.write(line)
            pos_neg_count[ID_hash[temp_line[0]]][0]+=1
            pos_neg_count[ID_hash[temp_line[1]]][0]+=1
        else:
            neg_f_out.write(line)
            pos_neg_count[ID_hash[temp_line[0]]][1]+=1
            pos_neg_count[ID_hash[temp_line[1]]][1]+=1
    counter+=1
pos_f_out.close()
neg_f_out.close()


## log some stats about how many positive and negative relationships there are
pos_neg_count = pos_neg_count.tolist()
for i in range(0,len(pos_neg_count)):
    pos_neg_count[i] = [IDlist[i]] + pos_neg_count[i]

pos_neg_count = [['ID','num_pos_cor','num_neg_cor']]+ pos_neg_count

write_table(pos_neg_count, os.path.join(os.path.dirname(out_adj),'positive_negative_cor_counts.txt'))