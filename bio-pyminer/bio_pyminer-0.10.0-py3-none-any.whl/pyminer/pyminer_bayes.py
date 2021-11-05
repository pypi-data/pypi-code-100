#!/usr/bin/env python3
import numpy as np
import h5py
import ray
try:
    from pyminer.common_functions import *
    from pyminer.pyminer_common_stats_functions import dense_rank
except:
    from common_functions import *
    from pyminer_common_stats_functions import dense_rank
#######################################################################

def dense_rank_lin_norm_and_bin(a, num_bins = 3):
	a = rankdata(a,method="dense")
	a -= np.min(a)
	a_max = np.max(a)
	if a_max == 0:
		## to prevent everything from going to infinity if something is non-expressed or invariant
		return(np.ones(np.shape(a), dtype = np.int8))
	a /= a_max
	## at this point min is 0 and max is 1
	a_out = np.ones(np.shape(a), dtype = np.int8)
	a_out[a>0.66665]=2
	a_out[a<0.33334]=0
	return(a_out)


def get_rel_abund(a):
	n = np.max(np.shape(a))
	a0 = np.sum(a==0)/n
	a1 = np.sum(a==1)/n
	a2 = np.sum(a==2)/n
	return(a0, a1, a2)


@ray.remote
def ray_hdf5_rel_abund():



def get_per_gene_rel_abund():




def make_cont_mat(a,b):
	## a couple functions that allow us to quickly figure out the contingency table
	n = np.max(np.shape(a))
	a0 = a==0
	a1 = a==1
	a2 = a==2
	b0 = b==0
	b1 = b==1
	b2 = b==2
	cont_mat = np.zeros(3,3,dtype = int32)
	## a is rows, b is columns
	cont_mat[0,0] = np.sum(a0*b0)
	cont_mat[1,0] = np.sum(a1*b0)
	cont_mat[2,0] = np.sum(a2*b0)
	cont_mat[0,1] = np.sum(a0*b1)
	cont_mat[1,1] = np.sum(a1*b1)
	cont_mat[2,1] = np.sum(a2*b1)
	cont_mat[0,2] = np.sum(a0*b2)
	cont_mat[1,2] = np.sum(a1*b2)
	cont_mat[2,2] = np.sum(a2*b2)
	return(cont_mat)#, a_rel_abund, b_rel_abund)


def rank_lin_bin_rows(a, bin_size = 5000, axis = 0):
	a = np.apply_along_axis(dense_rank_lin_norm_and_bin, axis, a)



def dense_rank_bin_transform(ID_list_file,
	                         adj_list_file,
	                         community_annotation_file,
	                         in_mat = None,
	                         in_hdf5_file = None,
	                         bin_size = 5000,
	                         processes = None):
	ID_list = read_file(ID_list_file,'lines')
	ID_hash = {value:key for key, value in enumerate(ID_list)}
	rank_lin_bin_rows()


def bayes_main():
	pass

if __name__ == "__main__":
	bayes_main()