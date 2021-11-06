import numpy as np
from .core import find_k
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.utils._testing import ignore_warnings
from sklearn.exceptions import ConvergenceWarning

def select_model(X,k_range,models=[KMeans()],verbose=False):
	"""
	"""
	model_scores = {}

	for estimator in models:
		(k_vals, scores) = find_k(X,k_range,model=estimator,out='full',verbose=verbose)
		model_scores[str(estimator)] = np.min(scores)

	return model_scores


def select_feature(X,k_range):
	"""
	"""
	var_ = np.zeros(X.shape[1])
	mean_ = np.zeros(X.shape[1])
	min_ = np.zeros(X.shape[1])
	max_ = np.zeros(X.shape[1])

	for i in range(X.shape[1]):
		X_only_one = X[:,i][:,np.newaxis]
		(k_vals,scores) = find_k(X_only_one,k_range,verbose=True, out='full')
		min_[i] = np.min(scores)
		max_[i] = np.max(scores)
		mean_[i] = np.mean(scores)
		var_[i] = np.var(scores)
		print('Mean: ', mean_[i])
		print('Variance: ', var_[i])

	return (var_, mean_, min_, max_)



@ignore_warnings(category=ConvergenceWarning)
def repeated_EM(X, k_range, n_passes=3, lmbda=500):
	"""
	Repeatedly apply the Entropy Method.
	"""

	# estimate number of clusters k for X
	k = find_k(X,k_range,verbose=True)

	if (n_passes > 1):
		# cluster X with k to obtain X, y
		y = KMeans(n_clusters=k).fit_predict(X)

		# classify X, y with L1-regularized logistic regression
		lmbda = find_regularizer(X,y)
		coef_mat = LogisticRegression(penalty='l1', C=1/lmbda, solver='saga', 
			multi_class='multinomial').fit(X,y).coef_
		print(coef_mat)
		features = (np.sum(coef_mat != 0, axis=0) > 0)
		print('\t -> Number of features selected:', np.sum(features))

		# select meaningful features of X -> X_red
		X_new = X[:,features]
		return repeated_EM(X_new, k_range,n_passes=n_passes-1)

	elif (n_passes == 1):
		return k

@ignore_warnings(category=ConvergenceWarning)
def find_regularizer(X,y,lmbda_min=1e-5,lmbda_max=1e+5, n_lmbda=7,n_folds=5,tol=0.005, min_iter=3):
	"""
	Tune the regularization strength for l1-penalized logistic regression.
	"""

	top_accuracy = 0
	top_lmbda = None
	keep_going = True

	j = 0
	while keep_going:
		j = j + 1
		print('Starting loop...')
		if (j >= min_iter):
			keep_going = False # stop unless we see improvement during this iteration

		# store lmbda values in reverse order, so that final choice is LARGEST satisfying lambda
		lmbda_grid = list(np.exp(np.linspace(np.log(lmbda_min), np.log(lmbda_max), n_lmbda)))[::-1]
		accuracy = []

		for i, lmbda in enumerate(lmbda_grid):
			classifier = LogisticRegression(penalty='l1',C=1/lmbda, solver='saga',
											multi_class='multinomial')
			accuracy.append(np.mean(cross_val_score(classifier,X,y,scoring='accuracy',cv=n_folds)))
			print('\tLambda =', lmbda, "-> accuracy =", accuracy[i])

		# hone in on the lmbda values giving the best accuracy
		if np.max(accuracy) > (1+tol)*top_accuracy:
			print('Saving improvement...')
			top_accuracy = np.max(accuracy)
			top_lmbda = lmbda_grid[np.argmax(accuracy)]
			# keep in mind reverse order of lmbda_grid for assignments below:
			lmbda_max = lmbda_grid[np.max([0,np.argmax(accuracy)-1])]
			lmbda_min = lmbda_grid[np.min([len(lmbda_grid)-1, np.argmax(accuracy)+1])]
			keep_going = True

	return top_lmbda



