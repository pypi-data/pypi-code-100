"""
This module provides algorithms for sampling cluster centers for a 
ClusterData object.

CLASSES AND METHODS

	BoundedSepCenters : sample cluster centers obeying separation constraints
		__init__(self, min_sep, max_sep, ...)
		place_centers(self, clusterdata)
		
"""

import numpy as np
import scipy.stats as stats
from .core import CenterGeom
from scipy.spatial.distance import mahalanobis
from scipy.stats import chi2

class BoundedSepCenters(CenterGeom):
	"""
	Sample cluster centers by specifying maximum and minimum separation 
	between centers.

	The minimum separation constraint ensures that no clusters are too 
	close together. On the other hand, the maximum separation constraint 
	guarantees that no cluster is too far away from all other clusters

	Separation is expressed on a scale derived from Mahalanobis distance. 
	A separation of 1.0 means that two clusters are just touching (when 
	each cluster is considered as a hard sphere filling 95% of the 
	cluster's probability mass). Lower values of separation imply overlap 
	between the clusters; higher values cleanly separate the clusters. 

	Note that the above interpretation of separation value is strictly 
	valid only for Gaussian clusters; for clusters with other data 
	distributions, separation values below or above 1.0 may be necessary
	for two clusters to be "just touching."

	Attributes
	----------
	min_sep : float (positive)
		Minimum separation between clusters. Value 1.0 means "just touching",
		lower values allow overlaps. See discussion in the class description.
	max_sep : float (positive)
		Maximum separation between clusters. Value 1.0 means "just touching",
		lower values imply overlap. See discussion in the class description.
	packing : float between 0 and 1, default=0.1
		Ratio of total cluster volume to sampling volume, used in rejection
		sampling. Here, cluster volume is computed from the maximum standard
		deviation among cluster shapes.

	"""
	
	def __init__(self, min_sep, max_sep, packing=.1):
		"""
		Create a BoundedSepCenters object.

		Parameters
		----------
		min_sep : float (positive)
			Minimum separation between clusters. Value 1.0 means "just touching",
			lower values allow overlaps. See discussion in the class description.
			max_sep : float (positive)
		Maximum separation between clusters. Value 1.0 means "just touching",
			lower values imply overlap. See discussion in the class description.
		packing : float between 0 and 1, default=0.1
			Ratio of total cluster volume to sampling volume, used in rejection
			sampling. Here, cluster volume is computed from the maximum standard
			deviation among cluster shapes.

		Returns
		-------
		out : BoundedSepCenters
			Object for sampling cluster centers obeying separation constraints.
		"""

		self.min_sep = min_sep
		self.max_sep = max_sep
		self.packing = packing
		

	def place_centers(self, clusterdata, seed=None, verbose=True):
		"""
		Place cluster centers sequentially with rejection sampling.

		Sample possible cluster centers uniformly within a box. To achieve 
		desired separation between clusters, only accept new centers whose
		separation from all other clusters is greater than self.min_sep (ensure
		no clusters overlap too much). In addition, only accept new centers
		whose separation from at least one other cluster is less than 
		self.max_sep (ensure no cluster is far away from all other clusters).

		Parameters
		----------
		self : BoundedSepCenters
			This instance of BoundedSepCenters
		clusterdata : ClusterData
			The data generator

		Returns
		-------
		centers : ndarray
			Cluster centers arranged in a matrix. Each row is a cluster center.
		"""

		np.random.seed(seed)

		# find the maximum sd
		cluster_sd = clusterdata.cluster_sd
		#max_sd = np.mean(np.array([np.mean(sd_vec) for sd_vec in cluster_sd]))
		max_sd = np.max(np.array([np.max(sd_vec) for sd_vec in cluster_sd]))

		cov_inv = clusterdata.cov_inv
		
		n_clusters = clusterdata.n_clusters
		n_dim = clusterdata.n_dim
		centers = np.zeros(shape=(n_clusters, n_dim))

		total_cluster_vol = n_clusters * ((4*max_sd)**n_dim)
		sampling_vol = total_cluster_vol / self.packing
		sampling_width = sampling_vol**(1/n_dim)

		# compute reference chi square value (take 0.95 quantile)
		q_chi_sq_min = chi2.ppf(self.min_sep, df=n_dim)
		q_chi_sq_max = chi2.ppf(self.max_sep, df=n_dim)

		# what's the reference distribution for the sum of squared scaled exponentials?
		# compute 0.95 quantile of distribution of the sum of n_dim Exp(1)**2 random variables

		# sum of squared scaled standard t distributions?
		
		for new_center in range(n_clusters):
			accept = False
			while not accept:
				proposed_center = sampling_width * np.random.uniform(size=n_dim)
				far_enough = True # Need to uphold minimum distance to other centers.
				close_enough = False # New center shouldn't be far away from all centers.

				# Check distances to previously selected centers
				for prev_ctr in range(new_center):
					d_1 = mahalanobis(proposed_center, centers[prev_ctr], 
										 cov_inv[new_center])
					d_2 = mahalanobis(proposed_center, centers[prev_ctr], 
										 cov_inv[prev_ctr])

					# quantile corresponding to chi^2 distribution with df=n_dim
					q_sq = 1/(((1/d_1) + (1/d_2))**2)
					# min_sep = q_sq_(1-alpha_min), max_sep = q_sq_(1-alpha_max),
					# e.g. min_sep = 0.95, max_sep = 0.9999

					if (q_sq <= q_chi_sq_min):
						far_enough = False 
						break

					if (q_sq <= q_chi_sq_max):
						close_enough = True
				
				if ((far_enough and close_enough) or (new_center == 0)):
					accept = True
					#UNCOMMENT FOR DEBUGGING PURPOSES:
					#if not (new_center == 0): 
					#	print(chi_1, chi_2)
					centers[new_center,:] = proposed_center
					if verbose: print('\t' + str(1+new_center) + 
						'/' + str(n_clusters) + ' placed!')
				
		return(centers)