"""
This module contains the core functionality for estimating the number 
of clusters with the Entropy Method.

METHODS
	compute_prob_mat(X, k, ...)
	entropy_score(P, k, ...)
	find_k(X, k_vals, ...)

"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import newton

import sklearn.linear_model as linear
import sklearn.model_selection as validation
from sklearn.cluster import KMeans
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning

from collections import Counter


def compute_prob_mat(X, k, model=KMeans(), B=100, f=0.5, sampling_method='no_replace',
	conf=False, seed=None):
	"""
	Compute the matrix of cluster co-membership probabilities for a 
	given number of clusters k. Each entry i,j of the output matrix 
	stores the empirical conditional probability that data points
	i and j are placed in the same cluster, given that both points are
	selected in the same subsample of the data.

	Parameters
	----------
	X : ndarray 
		The data matrix (each row is a data point)
	k : int
		The number of clusters
	model : clustering algorithm
		Any clustering algorithm that uses the sklearn API, needs to
		have an attribute n_clusters for the number of clusters, as well
		as a method fit_predict for assigning cluster labels to data
	B : int, default=100
		Number of subsamples used to compute probabilities
	f : float between 0 and 1, default=0.5
		Number of data points in each subsample, expressed as a fraction
		of total sample size. When f=0.5 (default), each subsampled data
		set contains 50% of the data points
	sampling_method : str, default='no_replace'
		Specify sampling method. If type='no_replace', sample from the data
		without replacement. If type='bootstrap', take bootstrap resamples.
	seed : int, default=None
		If an int, sets the seed for randomized computations

	Returns
	-------
	P : ndarray
		The matrix of cluster co-membership probabilities for k clusters

	"""
	if seed:
		np.random.seed(seed)

	n = X.shape[0]
	m = int(np.floor(n*f))
	
	# set clustering algorithm
	cluster = model
	cluster.n_clusters = k

	# association matrix tracks which data points are put in same cluster
	assoc_mat = np.zeros(shape=(n,n))
	# occurrence matrix tracks how often data points appear in same subsample
	occ_mat = np.zeros(shape=assoc_mat.shape)
	
	for b in range(B):
		# resample the data
		subsample = compute_subsample(n, m, method=sampling_method)

		# remember which data points appeared in the subsample together
		occ_mat[subsample[:, np.newaxis], subsample[np.newaxis,:]] += 1
	
		# obtain cluster memberships for subsampled data
		cluster_sub = cluster.fit_predict(X=X[subsample, :])
		# remember which pairs of datapoints cluster together
		for group in np.unique(cluster_sub):
			this_cluster = subsample[cluster_sub == group]
			assoc_mat[this_cluster[:, np.newaxis], this_cluster[np.newaxis,:]] += 1

	P = assoc_mat/occ_mat

	if conf:
		conf_low, conf_high = binom_wilson(P,occ_mat)
		return P, conf_low, conf_high
	else:
		return P


def binom_wilson(P,N,z=1):
	"""
	Estimate p with a Wilson binomial confidence interval.
	"""
	center = (P + (z**2)/(2*N))/(1 + (z**2)/N)
	spread = np.sqrt(P*(1-P)/N + (z**2)/(4*(N**2))) * (z / (1 + (z**2)/N))
	
	return (center-spread,center+spread)


def compute_subsample(n,m,method='no_replace'):
	"""
	Compute indices for a subsample.

	Parameters
	----------
	n : int
		Number of samples in the imput data
	m : int
		Desired number of samples in the subsample
	method : str, default='no_replace'
		Specify sampling method. If type='no_replace', sample from the
		data without replacement. If type='bootstrap', take bootstrap
		resamples.

	Returns
	-------
	out : ndarray, shape (m,)
		Array of indices defining the subsample
	"""

	if method=='bootstrap':
		return np.random.choice(n, m, replace=True)
	elif method=='no_replace':
		return np.random.choice(n, m, replace=False)
	else:
		raise Exception('invalid subsampling method. Choose method="bootstrap" or method="no_replace".')


def rho_fixedpt(x,k,n):
	"""
	Fixed point equation for the saddle point rho, which is used for 
	approximating the ratio of Sterling numbers of the second kind. 

	More precisely, the saddle point rho is the solution to the equation
	rho_fixedpt(x,k,n) = 0 in x.

	This function is a helper for the function rho, which is used in the
	function prob_w_rho. For more information, see the documentation for
	prob_w_rho.

	Parameters
	----------
	x : float
		Dummy argument of fixed point equation
	k : int
		Number of partitions
	n : int
		Number of elements

	Returns
	-------
	out : float
		Fixed point equation evaluated at x

	"""
	return ((1-np.exp(-x))/x) - (k/n)


def rho(k,n):
	"""
	Solve the fixed point equation for the saddle point rho, which is used
	for approximating the ratio of Sterling numbers of the second kind.

	This function is a helper for the function prob_w_rho. For more
	information, see the documentation for prob_w_rho.

	Parameters
	----------
	k : int 
		Number of partitions
	n : int 
		Number of elements

	Returns
	-------
	out : float
		Saddle point rho

	"""
	return newton(rho_fixedpt, 1/k, args=(k,n))


def prob_w_rho(k,n):
	"""
	Compute the probability that two elements of a set end up in the 
	same partition, when partitions are sampled uniformly at random.

	This function approximates the true probability, which is a ratio
	of Sterling numbers of the second kind. The approximation for the
	probability is rho/k, where rho is the output of the function rho.

	Parameters
	----------
	k : int
		Number of partitions
	n : int
		Number of elements in the set

	Returns
	-------
	out : float
		Approximate probability that two elements are placed in the same partition

	"""
	assert (k >= 1) and (k <= n), 'number of clusters k must lie ' + \
		'between 1 and the number of samples'
	out = rho(k,n)/n if k < n else 0
	return (1/k) if out > (1/k) else np.max([0, out])


def compute_ref_prob(k,n,ref_prob='approx_exact'):
	"""
	Compute the probability that two data points are randomly placed in the
	same cluster.

	Parameters
	----------
	k : int
		Number of clusters
	n : int
		Number of data points
	ref_prob : string, default='approx_exact'
		If ref_prob='approx_exact', approximate exact probability. If ref_prob=
		'naive', use 1/k instead.

	Returns
	-------
	out : float
		Probability that two data points are randomly placed in the same cluster
	"""

	if ref_prob=='approx_exact':
		return prob_w_rho(k,n)
	elif ref_prob=='naive':
		return 1/k
	else :
		raise Exception('invalid method for computing reference probability. ' + 
						' Use ref_prob="approx_exact" or ref_prob="naive"')


def sample_partition(n,k):
	"""
	Uniformly sample a partition of n elements into k groups.
	
	Returns a list of k lists, one for each partition.
	"""
	# BASE CASES
	if (k==1):
		return [list(range(1,n+1))]
	
	if (n==k):
		return [[i] for i in range(1,n+1)]
	
	# RECURSIVE CASE
	# either make one element a singleton or place it into k partitions on n-1 elements
	p_thold = k*prob_w_rho(k,n) # k*sterling(n-1,k)/sterling(n,k)

	if np.random.uniform() > p_thold:
		# make element n a singleton
		return [[n], *sample_partition(n-1,k-1)]
	else:
		# place element n into one of the partitions of
		z = sample_partition(n-1,k)
		z[int(np.random.choice(a=k))].append(n)
		return z
	

def compute_null_probs(n,k,B):
	"""
	Count the number of times each pair of data points ends up in the
	same cluster under a null model.
	"""
	mat = np.zeros(shape=(n,n))
	
	for b in range(B):
		partition = sample_partition(n,k)
		for k_id in range(0,k):
			idx = np.array(partition[k_id])-1
			mat[idx[:,np.newaxis],idx[np.newaxis,:]] += 1
			
	return mat/B


def binary_entropy(P):
	"""
	Compute binary entropy of probability matrix.
	"""
	np.seterr(all="ignore")
	entropy_w_nan = -(P*np.log2(P) + (1-P)*np.log2(1-P))
	entropy_mat = np.nan_to_num(entropy_w_nan, nan=0.0)

	return entropy_mat


def null_entropy(n,k,B):
	"""
	Compute reference entropy under a null model that randomly
	partitions the data.
	"""
	P = compute_null_probs(n,k,B)

	return np.mean(binary_entropy(P))


	
def entropy_score(P, k, m, ref_prob='approx_exact',logtransform=False):
	"""
	Compute Entropy Score from cluster co-membership matrix, for a given
	number of clusters k.

	Parameters
	----------
	P : ndarray 
		Cluster co-membership matrix (see entropymethod.core.compute_prob_mat)
	k : int
		Number of clusters for which P was computed
	m : int
		Number of samples in each subsample used for computing P. Typically
		equals n*f, where n is the total sample size (P.shape[0]) and f is
		the subsampling density
	ref_prob : string, default='approx_exact'
		If ref_prob='approx_exact', approximate exact probability. If ref_prob=
		'naive', use 1/k instead.

	Returns
	-------
	S : float
		Entropy Score measuring cluster stability. A low number reflects a good
		choice of k (a highly stable clustering)

	"""
	ref_prob = compute_ref_prob(k,m,ref_prob=ref_prob)
	ref_entropy = ref_prob*np.log2(1/ref_prob) + (1-ref_prob)*np.log2(1/(1-ref_prob))
	
	if not logtransform:
		return np.mean(binary_entropy(P))/ref_entropy
	else:
		return np.log10(np.mean(binary_entropy(P))/ref_entropy)


def compute_max_k(X, f, min_pts_per_cluster):
	"""
	Compute the maximum allowed number of clusters k.
	"""
	m = int(np.floor(X.shape[0]*f)) # sample size of subsamples
	return m/min_pts_per_cluster


def find_k(X, k_vals, model=KMeans(), B=100, f=0.5, out='argmin', sd_reps = 5,
	ref_prob='approx_exact', sampling_method='no_replace', logtransform=True, best_k_mode='greatest',
	override_k=False, min_pts_per_cluster=10, verbose=False, tabspace='',seed=None, plot=False, 
	add_title=None,kticks=None,yticks=None, filename=None):
	"""
	Estimate the number of clusters with the Entropy Method.

	Parameters
	----------
	X : ndarray 
		The data matrix (each row is a data point).
	k_vals : iterable
		Enumerates the numbers of clusters to consider
	B : int, default=100
		The number of subsamples used to compute cluster co-membership 
		probabilities
	f : float between 0 and 1, default=0.5
		Number of data points in each subsample, expressed as a fraction
		of total sample size. When f=0.5 (default), each subsampled data
		set contains 50% of the data points
	out : {'argmin', 'full'}, default='argmin'
		Specifies the desired form of the output. If out='argmin', return the
		best choice for the number of clusters. If out='full', return a tuple
		(k_vals, scores), where scores is a list of Entropy Scores that
		correspond to the numbers of clusters given in k_vals (also a list).
	ref_prob : string, default='approx_exact'
		If ref_prob='approx_exact', approximate the exact probability. 
		If ref_prob='naive', use 1/k instead.
	sampling_method : str, default='no_replace'
		Specify sampling method. If type='no_replace', sample from the data
		without replacement. If type='bootstrap', take bootstrap
		resamples. 
	logtransform : bool
		Choose whether to use the log of the normalized Entropy Score
	best_k_mode : str
		Choose whether to use the greatest or smallest k in range of the argmin
	override_k : bool, default=False
		If override_k=True, override our warning against evaluating stability
		for very large numbers of clusters (compared to subsample size). Doing
		this will likely yield the wrong output for the optimal k, since large 
		numbers of clusters have misleadingly high stability. For instance,
		when the number of clusters equals the sample size, each data point is
		forced into its own cluster, which guarantees perfect stability.
	verbose : bool, default=False
		Decide whether the algorithm should print its progress and final result
	seed : int, default=None
		If an int, sets the seed for randomized computations


	Returns
	-------
	k : int
		The optimal number of clusters k. This is the output when out='argmin'.
	(k_vals, scores) : tuple(list, list)
		k_vals is a list of the different numbers of clusters considered, and
		scores is a list of the corresponding Entropy Scores. This is the output
		when out='full'.
	"""

	m = int(np.floor(X.shape[0]*f)) # sample size of subsamples
	k_thold = compute_max_k(X,f,min_pts_per_cluster)
	kthold_str = 'nf/' + str(min_pts_per_cluster)
	scores = [] # mean entropy scores
	scores_sd = [] # empirical sd of mean entropy scores
	k_list = []

	if verbose:
		print(tabspace+'Assessing stability for different numbers of clusters...')
	for i, k in enumerate(k_vals):
		if (k <= k_thold) or override_k:
			k_list.append(k)
			score_reps = []
			for j in range(sd_reps):
				P = compute_prob_mat(X, k, model, B, f, 
									 sampling_method=sampling_method,seed=None if not seed else seed+j)
				new_score = entropy_score(P,k,m,ref_prob=ref_prob,logtransform=logtransform)
				score_reps.append(new_score)

			scores.append(np.mean(score_reps))
			scores_sd.append(np.sqrt(1+(1/B))*np.std(score_reps,ddof=1)) #/np.sqrt(sd_reps))

			if verbose:
				if not logtransform:
					print(tabspace+'\tk = ' + 
						np.format_float_positional(k,precision=0,
													pad_left=1+int(np.log10(np.max(k_vals))),
													trim='-') + 
						':  S = ' + 
						str(np.format_float_scientific(scores[i], precision=3)) + ', sd = ' + 
						str(np.format_float_scientific(scores_sd[i], precision=3)))
				elif logtransform:
					print(tabspace+'\tk = ' +
						np.format_float_positional(k,precision=0,
													pad_left=1+int(np.log10(np.max(k_vals))),
													trim='-') + 
						':  log(S) = ' + 
						str(np.format_float_positional(scores[i], 2, pad_right=2)) + ', sd = ' + 
						str(np.format_float_scientific(scores_sd[i], precision=0,trim='-')))
		elif (k > k_thold):
			if verbose:
				print(tabspace+'\tWarning: dropped k = ' + str(k) + ' (<' + 
					str(min_pts_per_cluster) + ' points per cluster).' +
					' To override, see docs.')

	if verbose:
		print(tabspace+'Stability analysis completed.')
		#print('Most stable number of clusters: k = ' + str(best_k))

	if plot:
		draw_errorbar_plot(k_list,scores,scores_sd,add_title=add_title,kticks=kticks, 
			yticks=yticks, filename=filename)
		plt.show()

	return process_scores(k_list,scores,scores_sd,out=out,verbose=verbose,tabspace=tabspace,
							best_k_mode=best_k_mode)


def draw_errorbar_plot(k,scores,sd, add_title=None, kticks=None, yticks=None, filename=None):
	"""
	Draw a plot of the normalized Entropy Scores vs the number of clusters,
	with errorbars. 

	This method only draws the plot, using Matplotlib. You may have to type
	matplotlib.pyplot.show() in order to display your plot.
	"""
	plt.rcParams.update({'font.size': 20,'figure.dpi': 300})

	plt.figure()

	plt.plot(k,scores,c='tab:blue',linewidth=2,linestyle='-',alpha=0.5)
	plt.errorbar(k, scores, yerr=sd, fmt='o', markersize=5, marker='o',color='black',
				markeredgecolor='gray', markeredgewidth=2,
				ecolor='gray', elinewidth=1.5, capsize=5)

	if kticks:
		plt.gca().set_xticks(kticks)
	else:
		k_tick_marks = list(plt.gca().get_xticks())
		k_tick_marks.append(k[np.argmin(scores)])
		plt.gca().set_xticks(np.ceil(k_tick_marks).astype('int'))

	if yticks:
		plt.gca().set_yticks(yticks)
	else:
		plt.gca().set_yticks(np.round(plt.gca().get_yticks(),1))

	plt.xlabel('k')
	plt.ylabel('log S').set_rotation(0);
	if add_title:
		plt.title('Normalized Entropy Score (S) vs Number of Clusters (k)');

	if filename:
		plt.savefig(filename,bbox_inches='tight')

	plt.show()

def compute_best_k(k,score,score_sd,mode='greatest',out='single'):
	"""
	Compute the recommended estimate for the number of clusters, given
	the scores and standard deviations for candidate numbers of k.

	If out='single', only output the recommended k. If out='set', output
	a tuple (k, K), where K is a set of recommended values for k.
	"""

	# transform lists to arrays
	score = np.array(score)
	score_sd = np.nan_to_num(np.array(score_sd),nan=0.0)
	k_arr = np.array(k)

	# compute set of candidate k values
	k_argmin = np.argmin(score)
	thold = score[k_argmin] + 2*score_sd[k_argmin]
	k_set = set(k_arr[score - 2*score_sd <= thold])

	# determine whether to take the greatest or smallest candidate k
	if (mode == 'greatest'):
		k_estimate = max(k_set)
	elif (mode == 'smallest'):
		k_estimate = min(k_set)
	else:
		raise ValueError("invalid value for mode. Choose 'greatest' " + \
						 "/'smallest' to use the" + \
						 "greatest/smallest k within range of the argmin.")

	if out=='single':
		return k_estimate
	else:
		return (k_estimate, k_set)




def process_scores(k_list,scores,scores_sd,out,verbose=False, tabspace='', 
	best_k_mode='greatest'):
	"""
	Interpret Entropy Scores and their associated standard deviations.
	Produce user-friendly output.

	Parameters
	----------
	k_list : list
	scores : list
	scores_sd : list
	out : str

	Returns
	-------

	"""

	# determine whether to take the greatest or smallest candidate k
	if (best_k_mode == 'greatest'):
		k_estimate, k_set = compute_best_k(k_list,scores,scores_sd,
											mode='greatest', out='set')
	elif (best_k_mode == 'smallest'):
		k_estimate, k_set = compute_best_k(k_list,scores,scores_sd,
											mode='greatest', out='set')
	else:
		raise ValueError("invalid value for best_k_mode. Choose 'greatest' " +
						 "or 'smallest' to estimate the number of clusters " + 
						 "as the greatest or smallest k within range of the " + 
						 "argmin.")

	# find index for best k and compute score and stdev
	k_arr = np.array(k_list)
	k_estimate_score = np.array(scores)[k_arr == k_estimate][0]
	k_estimate_sd = np.array(scores_sd)[k_arr == k_estimate][0]

	if verbose:
		print(tabspace+'Potential numbers of clusters: ', k_set)
		print(tabspace+'Estimated number of clusters: ', k_estimate)

	if (out == 'argmin'):
		return k_estimate, k_estimate_score, k_estimate_sd
	elif (out == 'full'):
		return (k_arr, scores, scores_sd)



def find_hierarchical_k(X, k_vals, f=0.5, min_pts_per_cluster=10, 
	best_k_mode='greatest',**kwargs):
	"""
	Find the number of clusters with the Hierarchical Entropy Method.
	"""
	print('Analyzing Clusters...')

	best_k, best_score, best_score_sd = find_k(X,k_vals,min_pts_per_cluster=min_pts_per_cluster,
												best_k_mode=best_k_mode,**kwargs)
	thold = best_score + 2*best_score_sd

	if not 'model' in kwargs:
		model = KMeans()
	model.n_clusters = best_k
	y = model.fit_predict(X)
	
	k_total = 0 # count of the total number of clusters
	out_list = [] # nested list to represent hierarchical structure
	for i in range(best_k):
		recursive_result = recursive_partition(X[y==i,:], k_vals, thold=thold,
										parent_str='', child_id=i, depth=1, 
										f=f, 
										min_pts_per_cluster=min_pts_per_cluster, 
										best_k_mode=best_k_mode,
										global_idx=np.arange(X.shape[0])[y==i],
										**kwargs)
		k_total += recursive_result[0]
		out_list.append(recursive_result[1])

	return (k_total, out_list)


def recursive_partition(X_cluster,k_vals, thold, parent_str, child_id, depth, f, 
	min_pts_per_cluster, best_k_mode, global_idx, **kwargs):
	"""
	Recursively partition clusters into subclusters.
	"""
	tabspace = '\t' * depth
	print(tabspace + 'Analyzing Cluster ' + parent_str + '.' + str(child_id+1) + ' ...')

	# run entropy method if you have enough samples
	if np.min(k_vals) > np.floor(X_cluster.shape[0]*f)/min_pts_per_cluster:
		# don't subcluster the data
		print(tabspace + '\t' + "NO, don't subcluster (not enough samples).")

		# check if the global indices are single data point [i]
		if (len(global_idx)==1):
			out_list = [global_idx[0]]
		else: # otherwise, make lists out of the individual indices
			out_list = [x for x in list(global_idx)]
		return (1, out_list)
	
	best_k, best_score, best_score_sd = find_k(X_cluster,k_vals, tabspace=tabspace,
												best_k_mode=best_k_mode,
												min_pts_per_cluster=min_pts_per_cluster,
												**kwargs)

	max_k = compute_max_k(X_cluster, f, min_pts_per_cluster)
	if (np.max(k_vals) < max_k): max_k = np.max(k_vals)

	# compare best stability score to thold (stability score for the whole cluster)
	if decide_to_subcluster(best_k,max_k,best_score,best_score_sd,thold,depth):
		# accept subclustering and recurse
		if not 'model' in kwargs:
			model = KMeans()
		model.n_clusters = best_k
		y = model.fit_predict(X_cluster)

		# compute threshold for subclustering the clusters
		new_thold = best_score + 2*best_score_sd

		# compute total number of subclusters in this cluster
		k_total = 0
		out_list = []
		for i in range(best_k):
			recursive_result = recursive_partition(
									X_cluster[y==i,:], 
									k_vals, 
									f=f, 
									min_pts_per_cluster=min_pts_per_cluster,
									thold = new_thold,
									parent_str = parent_str + '.' + str(child_id+1), 
									child_id=i, 
									depth=depth + 1, 
									global_idx = global_idx[y == i],
									best_k_mode=best_k_mode,**kwargs)
			k_total += recursive_result[0]
			out_list.append(recursive_result[1])


		return (k_total, out_list)
	
	else: # don't subcluster this data

		# check if the global indices are single data point [i]
		if (len(global_idx)==1):
			out_list = [global_idx[0]]
		else: # otherwise, make lists out of the individual indices
			out_list = [x for x in list(global_idx)]
		return (1, out_list)


def decide_to_subcluster(best_k,max_k,best_score,best_score_sd,thold,depth):
	"""
	Decide whether to further subcluster a cluster. Helper function for
	find_hierarchical_k.
	"""
	out = True if (((best_k > 2) and (best_k < max_k)) or (best_score < thold)) else False
	tabspace = '\t' * (depth+1)
	msg = tabspace + ("YES, subcluster!" if out else "NO, don't subcluster.")
	print(msg)
	return out


def majority_feature_vote(feature_lists,mode='majority'):
	"""
	Given multiple lists of features, keep only those features that appear in
	a majority of the given lists.
	"""
	n_votes = len(feature_lists)
	flattened_list = [feat_idx for feat_list in feature_lists for feat_idx in feat_list]
	vote_tallies = Counter(flattened_list)
	if mode=='strict_majority':
		return [idx for idx in vote_tallies.keys() if (vote_tallies[idx] > n_votes/2)]
	elif mode=='unanimous':
		return [idx for idx in vote_tallies.keys() if (vote_tallies[idx] == n_votes)]
	elif mode=='loose_majority':
		return [idx for idx in vote_tallies.keys() if (vote_tallies[idx] >= n_votes/2)]


@ignore_warnings(category=ConvergenceWarning)
def choose_features(X,y,reg_min=1e-5,reg_max=1e+5,n_reg_grid=10,n_folds=5,n_data_splits=2,
					consensus_mode='strict_majority'):
	"""
	Select features that are important for clustering the data.
	"""
	reg_grid = np.exp(np.linspace(np.log(reg_min), np.log(reg_max), n_reg_grid))
	
	n_samples = X.shape[0]
	permuted_idx = np.random.permutation(n_samples)
	n_pts_per_split = int(n_samples/n_data_splits)
	my_reg = []
	
	feature_lists = [] #set(range(X.shape[1]))
	
	for j in range(n_data_splits):
		# Compute the indices for this data split
		data_idx = permuted_idx[j*n_pts_per_split:(j+1)*n_pts_per_split]

		# Compute CV accuracy for each choice of the regularization parameter        
		cv_acc = np.zeros(len(reg_grid))
		for i, reg in enumerate(reg_grid):
			model = linear.LogisticRegression(penalty='l1', C=1/reg, max_iter=100, 
											solver='saga', multi_class='multinomial')
			cv_acc[i] = np.mean(validation.cross_val_score(model,X[data_idx,:],y[data_idx],
														   scoring='accuracy', cv=n_folds))

		my_reg_idx = np.argmax(cv_acc)
		my_reg.append(reg_grid[my_reg_idx])
		
		# Fit model with the desired regularization strength
		model = linear.LogisticRegression(penalty='l1', C=1/my_reg[j], max_iter=100, 
											solver='saga', multi_class='multinomial')
		model.fit(X[data_idx,:],y[data_idx])
		
		# Add selected features to list of chosen features from other data splits
		features_chosen_bool = (np.sum(model.coef_ != 0, axis=0) > 0)
		feature_lists.append(np.arange(X.shape[1])[features_chosen_bool])
	
	# Vote on which features to select; output results
	features_chosen_idx = np.array(majority_feature_vote(feature_lists,mode=consensus_mode),dtype=int)
	X_reduced = X[:,features_chosen_idx]

	return {'features': features_chosen_idx, 'reduced_data': X_reduced, 'reg': np.prod(my_reg)**(1/n_data_splits)}


def find_repeated_k(X,k_vals,n_runs=3, reg_min=1e-5, reg_max=1e+5, 
					  n_reg_grid=10, model=KMeans(),feature_subset=None, 
					  runs_completed=0, n_data_splits=2, verbose=False,
					  all_iteration_results=None, out='full', method='basic',
					  consensus_mode='strict_majority',
					  k_start=None,
					  incr_splits=True,
					  **kwargs):
	"""
	Estimate the number of clusters with the Repeated Entropy Method.
	"""
	
	# at the last run, no longer compute feature subset
	if (runs_completed >= n_runs):
		k, score, score_sd = find_k(X,k_vals,verbose=verbose,out=out,**kwargs)
		if out=='argmin':
			return k, score, score_sd
		else:
			return {'k': k, 'score': score, 'score_sd': score_sd, 
					'features': np.sort(feature_subset), 
					'all_iterations': all_iteration_results}
	
	else: # estimate k, run logistic regression on cluster labels, compute feature subset

		# if this is the first iteration and we selected a starting k, use it
		if k_start and (runs_completed==0):
			print('We are really doing this!')
			best_k = k_start
			k = k_vals 
		else:
			if method=='basic':
				k, score, score_sd = find_k(X,k_vals,verbose=verbose,out=out,**kwargs)
			elif method=='hierarchical':
				out = 'argmin'
				k = find_hierarchical_k(X,k_vals,verbose=verbose,**kwargs)[0]

			if out=='argmin':
				best_k = k
			else:
				best_k = compute_best_k(k,score,score_sd,out='single',mode='greatest')

		# obtain cluster labels
		model.n_clusters = best_k  
		y = model.fit_predict(X)

		# choose relevant features
		print("Choosing features with " + str(n_data_splits) + "-fold split...")
		feature_data = choose_features(X,y, reg_min=reg_min,reg_max=reg_max,
							  n_reg_grid=n_reg_grid,n_data_splits=n_data_splits,
							  consensus_mode=consensus_mode)
		
		# if this is the first run, refine the seach grid for the regularization param
		if (runs_completed==0):
			all_iteration_results = {'k':k,'score':[],'sd':[]}
			reg_min, reg_max = adjust_reg_range(feature_data['reg'], runs_completed)
			feature_data = choose_features(X,y, reg_min=reg_min,reg_max=reg_max,
								  n_reg_grid=n_reg_grid,n_data_splits=n_data_splits,
								  consensus_mode=consensus_mode)
			
		features = feature_data['features'] if feature_subset is None else feature_subset[feature_data['features']]
		
		if verbose:
			print('\nSelected features:', np.sort(features),'\n')
		
		# append scores and standard deviations if they have been computed
		if (out=='full') and not (k_start and (runs_completed==0)):
			all_iteration_results['score'].append(score)
			all_iteration_results['sd'].append(score_sd)

		# increment counter of completed runs	
		runs_completed += 1

		# increase number of data splits to yield fewer features
		if incr_splits:
			print("Increasing number of data splits...")
			n_data_splits += 1
		
		# adjust regularization parameter search grid for the next round
		reg_min, reg_max = adjust_reg_range(feature_data['reg'], runs_completed)
		
		return find_repeated_k(feature_data['reduced_data'],k_vals,n_runs=n_runs,
								 reg_min=reg_min, reg_max=reg_max,
								 feature_subset=features, 
								 runs_completed=runs_completed, 
								 verbose=verbose,
								 n_data_splits=n_data_splits,
								 all_iteration_results=all_iteration_results,
								 out = out,
								 method = method,
								 consensus_mode=consensus_mode,
								 incr_splits=incr_splits,
								 **kwargs)


def adjust_reg_range(current_reg, runs_completed):
	"""
	Narrow the range for searching the regularization parameter. Helper
	function for find_repeated_k.
	"""
	min_exp = -np.max([2.-runs_completed,1])
	max_exp = np.max([2.-runs_completed,1])
	reg_min = current_reg*(10.**min_exp)
	reg_max = current_reg*(10.**max_exp)

	return (reg_min, reg_max)






