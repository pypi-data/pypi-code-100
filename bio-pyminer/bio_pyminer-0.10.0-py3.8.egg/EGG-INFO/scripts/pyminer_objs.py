#!python
import numpy as np
import pandas as pd
import fileinput
import os
try:
	from pyminer.common_functions import read_table, get_sample_k_lists, import_dict
except:
	from common_functions import read_table, get_sample_k_lists, import_dict


def load_relative_table(in_dir, rel_path, out_type="numpy", no_head = False):
	in_file = os.path.join(in_dir,rel_path)
	if os.path.isfile(in_file):
		if out_type == "numpy":
			return(np.array(read_table(in_file)))
		if out_type == "pandas":
			if no_head:
				return(pd.read_csv(in_file, sep='\t', header=None))
			else:
				return(pd.read_csv(in_file, sep='\t'))
		if out_type == "list":
			return(read_table(in_file))
	else:
		print("\n\nWARNING: Could not find the file: "+in_file+"\n\n")
		return(None)

##################

class ap_obj(object):
	def __init__(self, in_dir):
		self.in_dir = in_dir
		self.load_ap_interactions()

	def load_ap_interactions(self):
		self.all_num_clust_interactions = load_relative_table(self.in_dir, "autocrine_paracrine_signaling/all_cell_cell_interaction_summary.tsv", out_type = "pandas")
		self.pathway_neg_log_p_vals = load_relative_table(self.in_dir, "autocrine_paracrine_signaling/combined_neg_log10p_gprofiler.tsv", out_type = "pandas")
		self.pathway_importance = load_relative_table(self.in_dir, "autocrine_paracrine_signaling/individual_class_importance.tsv", out_type = "pandas")
		#autocrine_paracrine_signaling/extracellular_extracellular_cell_type_specific_interactions.txt
		#autocrine_paracrine_signaling/extracellular_plasma_membrane_cell_type_specific_interactions.txt
		#autocrine_paracrine_signaling/plasma_membrane_plasma_membrane_cell_type_specific_interactions.txt

	def load_clust_clust_interactions(self, clust_1, clust_2):
		print("loading all the interactions between", clust_1, "and", clust_2)
		## filter for only the correct ones & return a pandas table
		## clust_1: 1
		## clust_2: 5
		"autocrine_paracrine_signaling/all_cell_type_specific_interactions.tsv"
		return()

	def load_pathway(self, pathway):
		## do a grep like thing for this table and the pathway
		## return a pandas table containing only the lines pertinent to the pathway
		"autocrine_paracrine_signaling/all_cell_type_specific_interactions_gprofiler.tsv"
		return()

	def load_clust_clust_pathways(self, clust_1, clust_2):
		## do a grep like thing for this table and the pathway
		## return a pandas table containing only the lines pertinent to the pathway
		"autocrine_paracrine_signaling/all_cell_type_specific_interactions_gprofiler.tsv"
		return()

	def __str__(self):
		out_str = "PyMINEr autocrine paracrine analyses"
		out_str += "\nObjects of interest:"
		out_str += "\n\t<object>.all_num_clust_interactions: An adjacency list of all clusters with all other \n\t\tclusters and the number of interactions that they have with each other."
		out_str += "\n\t<object>.pathway_neg_log_p_vals: Pathway (row) -log10(p-values) and their corresponding \n\t\tclusters-cluster pairs & their signaling interactions (columns). \n\t\tTable is sorted by how informative a given pathway is."
		out_str += "\n\t<object>.pathway_importance: A 2D table of pathways (rows) & their importance for each \n\t\tcluster-cluster pair (column). Sort this table by a given column \n\t\tto get the most informative pathways that describe the given gene module."
		out_str += "\n\n\nFunctions of interest"
		out_str += "\n\t<object>.: "
		return(out_str)

	def __repr__(self):
		return("ap_obj('"+self.in_dir+"')")

##################
class goi_obj(object):
	def __init__(self, in_dir):
		self.in_dir = in_dir
		self.load_goi()

	def load_goi(self):
		self.goi_dir = os.path.join(self.in_dir,"genes_of_interest")
		if os.path.isdir(self.goi_dir):
			goi_short_path_file = os.path.join(self.goi_dir,"genes_of_interest_shortest_path_list.txt")
			if os.path.isfile(goi_short_path_file):
				self.goi_shortest_paths = load_relative_table(self.in_dir, goi_short_path_file, out_type = "pandas")
		else:
			self.goi_dir = None
			self.goi_shortest_paths = None

	def __str__(self):
		out_str = "PyMINEr genes of interest analyses"
		out_str += "\nObjects of interest:"
		out_str += "\n\t<object>.goi_dir: The directory that contains the plots that were automatically \n\t\tgenerated for your genes of interest"
		out_str += "\n\t<object>.goi_shortest_paths: A 2D table that contains your genes of interest (columns) \n\t\tand all other genes, and indicates the shortest path distance in \n\t\tthe co-expression network graph from the pertinent gene of interest."
		return(out_str)

	def __repr__(self):
		return("goi_obj('"+self.in_dir+"')")

##################
class network_obj(object):
	def __init__(self, in_dir):
		print("loading network analysis")
		self.in_dir = in_dir
		self.load_modules()

	def load_modules(self):
		self.communities = load_relative_table(self.in_dir, "pos_cor_graphs/communities.txt", out_type = "pandas")
		self.community_cluster_use_stats = load_relative_table(self.in_dir, "pos_cor_graphs/community_analysis/global_statistics.tsv", out_type = "pandas")
		self.pathway_neg_log_p_vals = load_relative_table(self.in_dir, "pos_cor_graphs/community_analysis/combined_neg_log10p_gprofiler.tsv", out_type = "pandas")
		self.pathway_importance = load_relative_table(self.in_dir, "pos_cor_graphs/community_analysis/individual_class_importance.tsv", out_type = "pandas")

	def load_individual_modules(self):
		pass
		# module_dict = {}
		# ## 
		# for 

	def load_network(self, full_network=False):
		## this is not run automatically because these networks can be large
		self.graph_full_file = os.path.join(self.in_dir,"pos_cor_graphs/full_graph_full.graphpkl")
		self.graph_file = os.path.join(self.in_dir,"pos_cor_graphs/large_comps.graphpkl")
		pass

	def __str__(self):
		out_str = "PyMINEr network analyses"
		out_str += "\nObjects of interest:"
		out_str += "\n\t<object>.communities: Annotations of all genes and their co-expression module/community,\n\t\tas well as some other stats like page rank and local page rank (the later is an \n\t\talgorithm not yet published)"
		out_str += "\n\t<object>.community_cluster_use_stats: Statistics for whether a module is differentially\n\t\tutilized across clusters."
		out_str += "\n\t<object>.pathway_neg_log_p_vals: Pathway (row) -log10(p-values) and their corresponding\n\t\tclusters (columns). Table is sorted by how informative a given pathway is."
		out_str += "\n\t<object>.pathway_importance: A 2D table of pathways (rows) & their importance for each \n\t\tgene module/community (column). Sort this table by a given column to get the most \n\t\tinformative pathways that describe the given gene module."
		# out_str += "\n\t<object>.: "
		# out_str += "\n\t<object>.: "
		return(out_str)

	def __repr__(self):
		return("network_obj('"+self.in_dir+"')")

##################
class clust_plotting_obj(object):
	def __init__(self, in_dir):
		self.in_dir = in_dir
		self.load_cluster_plotting()

	def load_cluster_plotting(self):
		self.cluster_pkl = import_dict(os.path.join(self.in_dir,"sample_clustering_and_summary/clustering_plots.pkl"))
		## all plots
		self.plotting_subset = self.cluster_pkl["sample_indices_for_plotting"]
		self.cluster_colors = self.cluster_pkl["color_vect"]
		self.linear_groups = self.cluster_pkl["linear_groups"]
		self.sample_k_lists = self.cluster_pkl["sample_k_lists"]
		## 2D plots
		self.plots = self.cluster_pkl["plots"]
		## heatmap
		self.group_reordering_vector = self.cluster_pkl["group_reordering_vector"]
		self.reordered_colors = self.cluster_pkl["reordered_colors"]
		## cell embedding
		cell_embedding_file = os.path.join(self.in_dir,"sample_clustering_and_summary/cell_embedding.graphpkl")
		if os.path.isfile(cell_embedding_file):
			self.cell_embedding_network = import_dict(cell_embedding_file)
		else:
			self.cell_embedding_network = "clustering wasn't done with Louvain modularity, so there's no graph network representation of the cell embedding"

	def __str__(self):
		out_str = "\nPyMINEr cluster plotting analyses"
		out_str += "\nObjects of interest:"
		out_str += "\n\n:Objects relevant to all plots"
		out_str += "\n\t<object>.plotting_subset: These are really important: only a subset of cells are \n\t\ttypically use for plotting in datasets of sufficient size (default=15k). This vector are the \n\t\tindices of that subset from the original dataset."
		out_str += "\n\t<object>.cluster_colors: The vector of colors used by PyMINEr to make all of the \n\t\tcluster-colorized plots."
		out_str += "\n\t<object>.linear_groups: The group level annotations for the subset of cells used."
		out_str += "\n\t<object>.sample_k_lists: A re-organization of linear_groups that is a list of lists, \n\t\twith the first level being the cluster number, and each of those lists being the indices \n\t\tof the cells that belong to that cluster. Note again that the indices are for the \n\t\tsubset of cells used for plotting."
		out_str += "\n\n2D-scatter related objects:"
		out_str += "\n\t<object>.plots: 2D projections of the <object>.plotting_subset subset of cells & \n\t\ttheir x,y coords, color,and the file name for where that image is saved. This could be useful \n\t\tif you want to use the same UMAP x/y projection for additional plots or something like that."
		out_str += "\n\nHeatmap related objects:"
		out_str += "\n\t<object>.group_reordering_vector: After subsetting the expression matrix for the \n\t\t<object>.plotting_subset cells, use this vector to reorder that subset to plot a heatmap that \n\t\tgoes in serial from cluster 0 forward."
		out_str += "\n\t<object>.reordered_colors: the vector of colors that has been re-ordered to go in \n\t\tserial from cluster 0 onward"
		out_str += "\n\nNetwork graph embedding of ALL cells (Only if you used Louvain modularity as the \n\t\tclustering method)"
		out_str += "\n\t<object>.cell_embedding_network: the networkx graph object containing the network \n\t\tof the pertinent subset of cells."
		# out_str += "\n\t<object>.:"
		return(out_str)

	def __repr__(self):
		return("clust_plotting_obj('"+self.in_dir+"')")

#####################
class clust_obj(object):
	def __init__(self, in_dir):
		self.in_dir = in_dir
		self.load_labels()
		self.load_expression_stats()
		self.load_marker_table()
		self.load_clust_genes()
		self.load_enrich_genes()
		self.create_clust_plot()

	def load_labels(self):
		label_table = load_relative_table(self.in_dir, "sample_clustering_and_summary/sample_k_means_groups.tsv")
		self.samples = label_table[:,0].tolist()
		self.sample_idx_dict = {key:value for value, key in enumerate(self.samples)}
		self.labels = np.array(label_table[:,1],dtype=float)
		self.cluster_lists = get_sample_k_lists(self.labels.tolist())

	def load_marker_table(self):
		print("loading the cluster level marker gene annotations")
		self.best_markers = load_relative_table(self.in_dir, "sample_clustering_and_summary/significance/high_markers/best_sorted_markers.tsv", out_type = "pandas", no_head = True)
		self.all_markers = load_relative_table(self.in_dir, "sample_clustering_and_summary/significance/high_markers/marker_gene_annotations.tsv", out_type = "pandas")

	def load_expression_stats(self):
		print("loading the global & cluster expression metrics")
		self.global_non_zero_mean = load_relative_table(self.in_dir, "sample_clustering_and_summary/expression_metrics/global_non_zero_mean.tsv", out_type = "pandas")
		self.global_percent_express = load_relative_table(self.in_dir, "sample_clustering_and_summary/expression_metrics/global_percent_express.tsv", out_type = "pandas")
		self.cluster_percent_express = load_relative_table(self.in_dir, "sample_clustering_and_summary/expression_metrics/k_group_percent_express.tsv", out_type = "pandas")
		self.cluster_non_zero_mean_expression = load_relative_table(self.in_dir, "sample_clustering_and_summary/expression_metrics/non_zero_mean_expression.tsv", out_type = "pandas")
		self.ratio_non_zero_mean_expression = load_relative_table(self.in_dir, "sample_clustering_and_summary/expression_metrics/ratio_non_zero_mean_expression.tsv", out_type = "pandas")
		self.ratio_percent_express = load_relative_table(self.in_dir, "sample_clustering_and_summary/expression_metrics/ratio_percent_express.tsv", out_type = "pandas")
		self.cluster_express_mean = load_relative_table(self.in_dir, "sample_clustering_and_summary/k_group_means.tsv", out_type = "pandas")
		self.cluster_express_sd = load_relative_table(self.in_dir, "sample_clustering_and_summary/k_group_sd.tsv", out_type = "pandas")

	def load_clust_genes(self):
		self.clust_genes = load_relative_table(self.in_dir, "sample_clustering_and_summary/genes_used_for_clustering.txt", out_type = "numpy")

	def load_enrich_genes(self):
		print("loading the genes that are enriched in each group & their pathway analyses")
		self.enrich_table = load_relative_table(self.in_dir, "sample_clustering_and_summary/sample_var_enrichment_Zscores.txt", out_type = "pandas")
		self.enrich_bool_table = load_relative_table(self.in_dir, "sample_clustering_and_summary/significance/significant_and_enriched_boolean_table.tsv", out_type = "pandas", no_head = True)
		self.significance_table = load_relative_table(self.in_dir, "sample_clustering_and_summary/significance/groups_1way_anova_results.tsv", out_type = "pandas")
		self.pathway_importance = load_relative_table(self.in_dir, "sample_clustering_and_summary/significance/individual_class_importance.tsv", out_type = "pandas")
		self.pathway_neg_log_p_vals = load_relative_table(self.in_dir, "sample_clustering_and_summary/significance/combined_neg_log10p_gprofiler.tsv", out_type = "pandas")

	def create_clust_plot(self):
		self.plt_info = clust_plotting_obj(self.in_dir)

	def __str__(self):
		out_str = "PyMINEr clustering analyses"
		out_str += "\nObjects of interest:"
		out_str += "\n\nsample level info:"
		out_str += "\n\t<object>.samples: the vector of sample IDs"
		out_str += "\n\t<object>.sample_idx_dict: a dictionary with the sample names as keys & their index in the \n\t\tdataset as the value"
		out_str += "\n\t<object>.labels: the cluster labels in the form of cluster number"
		out_str += "\n\t<object>.cluster_lists: a list of lists where the first level is the cluster, & the \n\t\tsecond level is the sample indexes that belong to that cluster"
		out_str += "\n\nmarker gene info:"
		out_str += "\n\t<object>.best_markers: The top n marker genes that define each cluster."
		out_str += "\n\t<object>.all_markers: A table of all genes, how good of markers they make, & what their \n\t\tbest cluster mapping is."
		out_str += "\n\nexpression statistics info:"
		out_str += "\n\t<object>.global_non_zero_mean: in the whole dataset what is the non-zero mean?"
		out_str += "\n\t<object>.cluster_non_zero_mean_expression: within each cluster, what is the non-zero mean?"
		out_str += "\n\t<object>.ratio_non_zero_mean_expression: for each cluster, what's the ratio beteween its \n\t\tnon-zero mean and the global non-zero mean?"
		out_str += "\n\t<object>.global_percent_express: in the whole dataset, what's the percentage of \n\t\tnon-zero expression?"
		out_str += "\n\t<object>.cluster_percent_express: within each cluster, what's the percentage of \n\t\tnon-zero expression?"
		out_str += "\n\t<object>.ratio_percent_express: for each cluster, what's the ratio of the \n\t\tnon-zero percentage & the global non-zero percent expressed?"
		out_str += "\n\t<object>.cluster_express_mean: the mean expression of genes in each cluster"
		out_str += "\n\t<object>.cluster_express_sd: the standard deviation of gene expression in each cluster"
		out_str += "\n\ncluster expression enrichment info:"
		out_str += "\n\t<object>.enrich_table: the cluster level Z-score table for expression"
		out_str += "\n\t<object>.enrich_bool_table: a boolean T/F table for all genes and clusters for \n\t\twhether or not a gene was significantly enriched in that cluster"
		out_str += "\n\t<object>.significance_table: the anova significance table. (global F-statistic, \n\t\tnot pairwise comparisons)"
		out_str += "\n\t<object>.pathway_importance: A table of pathway importance factors (rows) for each \n\t\tcluster (columns). Sort a column to see what pathways are most informative/unique\n\t\tin that specific cluster."
		out_str += "\n\t<object>.pathway_neg_log_p_vals: A table of the -log10(p-values) for pathways (rows) \n\t\tfor each cluster (column), sorted by PyMINEr's information ranking system \n\t\t(based on KL-divergence)"
		out_str += "\n\nclustering and plotting info:"
		out_str += "\n\t<object>.plt_info: An object that contains detailed plotting info. Print that \n\t\tobject for it's own help guide."
		# out_str += "\n\t<object>.samples:"
		# out_str += "\n\t<object>.samples:"
		# out_str += "\n\t<object>.samples:"
		return(out_str)

	def __repr__(self):
		return("clust_obj('"+self.in_dir+"')")
##################

class gene_annotations_obj(object):
	def __init__(self, in_dir):
		self.in_dir = in_dir
		self.load_anno()

	def load_anno(self):
		self.annotations = load_relative_table(self.in_dir, "annotations.tsv", out_type = "pandas")
		ortho_file = os.path.join(self.in_dir,"human_orthologues.tsv")
		if os.path.isfile(ortho_file):
			self.human_ortho = load_relative_table(self.in_dir, "human_orthologues.tsv", out_type = "pandas")
		else:
			self.human_ortho = None

	def __str__(self):
		out_str = "PyMINEr gene annotations"
		out_str += "\nObjects of interest:"
		out_str += "\n\t<object>.annotations: A table of gene level annotations, including Ensembl gene \n\t\tmapping & gene descriptions."
		out_str += "\n\t<object>.human_ortho: If you didn't run a human sample, there should be a table \n\t\tannotating the human orthologues. Otherwise, this is None."
		return(out_str)

	def __repr__(self):
		return("gene_annotations_obj('"+self.in_dir+"')")

##################

class pyminer_obj(object):
	def __init__(self, in_dir):
		self.in_dir = in_dir
		self.gene_anno = gene_annotations_obj(in_dir)
		self.clust = clust_obj(in_dir)
		self.goi = goi_obj(in_dir)
		self.network = network_obj(in_dir)
		self.ap = ap_obj(in_dir)
		
	def set_dir(self, new_in_dir):
		self.in_dir = new_in_dir
		self.gene_anno.in_dir = new_in_dir
		self.clust.in_dir = new_in_dir
		self.goi.in_dir = new_in_dir
		self.network.in_dir = new_in_dir
		self.ap.in_dir = new_in_dir

	def __str__(self):
		out_str = "PyMINEr object:\n"
		out_str += "\nEach of the elements contained within the PyMINEr object is it's own class\n\t\tYou can print each of these objects to get the help section on it."
		out_str += "\n\t<object>.gene_anno: an object that contains tables annotating the input genes"
		out_str += "\n\t<object>.clust: This object has lots of info on the clusters, differential \n\t\texpression, pathway analysis, etc. just do print(<object>.clust) to get the details!"
		out_str += "\n\t<object>.goi: If you used genes of interest, the direcotry of the output \n\t\tplots and the shortest-paths of all other genes to them are located here."
		out_str += "\n\t<object>.network: The co-expression network and details on gene-module \n\t\tusage, module pathway analysis, etc"
		out_str += "\n\t<object>.ap: Details of the autocrine/paracrine signaling between clusters \n\t\tand pathway analysis of those signaling networks."
		#out_str += "\n\t<object>.: "
		out_str += "\n\nThere is also the PyMINEr website file that provides a walk-through of the results:\n"+os.path.join(self.in_dir,"PyMINEr_summary.html")+"\n\n"
		#out_str += "\n:"+
		return(out_str)

	def __repr__(self):
		return("pyminer_obj("+self.in_dir+")")
