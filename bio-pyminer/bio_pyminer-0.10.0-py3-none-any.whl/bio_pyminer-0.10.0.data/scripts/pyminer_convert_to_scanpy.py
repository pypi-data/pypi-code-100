import h5py
import scanpy as sp
try:
    from pyminer.common_functions import *
    from pyminer.pyminer_objs import pyminer_obj
except:
    from common_functions import *
    from pyminer_objs import pyminer_obj
###############################################




def adata_to_pm_input(adata, analysis_dir):
	print("\n\nThe adata object you feed into pyminer needs to be:\nQC filtered, depth normalized (downsampling recommended), and log transformed\n\n")
	analysis_dir = process_dir(analysis_dir)
	## make the ID_
	gene_ids_list = list(adata.var.gene_ids)
	col_ids_list = list(adata.obs.index)
	## write them
	gene_out_str = "\n".join(list(map(str,gene_ids_list)))
	ID_list = os.path.join(analysis_dir, "ID_list.txt")
	make_file(gene_out_str, ID_list)
	col_out_str = "\n".join(["vars"]+col_ids_list)
	columns = os.path.join(analysis_dir,"column_IDs.txt")
	make_file(col_out_str, columns)
	## now make the main hdf5
	out_file = os.path.join(analysis_dir+'data.hdf5')
	temp_data = adata.X.transpose()
	f = h5py.File(out_file, "w")
	dset = f.create_dataset("infile",
		                    temp_data.shape,
		                    dtype=np.float32)
	## because this is a csc file, we'll go by columns
	bins = get_bins(len(col_ids_list))
	for i in range(1,len(bins)):
		start = bins[i-1]
		end = bins[i]
		dset[:,start:end]+=temp_data[:,start:end].toarray()
	f.close()
	return(out_file, ID_list, columns)


########################################################
## final AnnData object looks like this:
# AnnData object with n_obs × n_vars = 2638 × 1838
#     obs: 'n_genes', 'n_genes_by_counts', 'total_counts', 'total_counts_mt', 'pct_counts_mt', 'leiden'
#     var: 'gene_ids', 'n_cells', 'mt', 'n_cells_by_counts', 'mean_counts', 'pct_dropout_by_counts', 'total_counts', 'highly_variable', 'means', 'dispersions', 'dispersions_norm', 'mean', 'std'
#     uns: 'hvg', 'leiden', 'leiden_colors', 'neighbors', 'pca', 'rank_genes_groups', 'umap'
#     obsm: 'X_pca', 'X_umap'
#     varm: 'PCs'
#     obsp: 'connectivities', 'distances'


def set_hvg_to_used_for_clust(adata, analysis_dir):
	## read in the used_for_clustering

	# sc.pp.highly_variable_genes(adata, min_mean=0.0125, max_mean=3, min_disp=0.5)
	# extracting highly variable genes
	#     finished (0:00:00)
	# --> added
	#     'highly_variable', boolean vector (adata.var)
	#     'means', float vector (adata.var)
	#     'dispersions', float vector (adata.var)
	#     'dispersions_norm', float vector (adata.var)

	# finished: added to `.uns['neighbors']`
    # `.obsp['distances']`, distances for each pair of neighbors
    # `.obsp['connectivities']`, weighted adjacency matrix (0:00:01)
	return(adata)


def set_adata_clust_res(adata):
	# running Leiden clustering
	# finished: found 8 clusters and added
	# 'leiden', the cluster labels (adata.obs, categorical) (0:00:00)
	return(adata)

def set_umap_coords(adata):
	## 'X_umap', UMAP coordinates (adata.obsm)
	return(adata)


def set_de_and_markers(adata):
	# sc.tl.rank_genes_groups(adata, 'leiden', method='t-test')
	# sc.pl.rank_genes_groups(adata, n_genes=25, sharey=False)
	# ranking genes
	#     finished: added to `.uns['rank_genes_groups']`
	#     'names', sorted np.recarray to be indexed by group ids
	#     'scores', sorted np.recarray to be indexed by group ids
	#     'logfoldchanges', sorted np.recarray to be indexed by group ids
	#     'pvals', sorted np.recarray to be indexed by group ids
	#     'pvals_adj', sorted np.recarray to be indexed by group ids (0:00:00)
	return(adata)



def pyminer_obj_to_sp(pm_obj, adata=None):
	return(adata)


