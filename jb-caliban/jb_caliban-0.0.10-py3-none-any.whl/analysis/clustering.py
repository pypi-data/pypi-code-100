"""
This module contains useful functions for clustering.

@authors: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
          Jack Berry, Columbia University, jeb2242@columbia.edu
"""


from sklearn import cluster
from sklearn.metrics import normalized_mutual_info_score
from sklearn.metrics import mutual_info_score
import itertools
import pandas as pd
import numpy as np

def similarity_matrix(dataframe, similarity_measure=normalized_mutual_info_score):
    """
    Create a DataFrame similarity matrix

    Inputs:
        dataframe: pandas DataFrame
            A TxN DataFrame where T is the number of observations (time bins)
            and N is the number of variables (neurons)

        similarity_measure: function, optional
            The similarity metric to be used. Default is
            sklearn.metrics.normalized_mutual_info_score. any function can be used,
            including the pearsonr wrapper in this module.

    Returns:
        matrix: pandas DataFrame
            A DataFrame storing the similarity matrix for all neurons
    """
    rows = []

    for col in dataframe:
        row = dataframe.apply(similarity_measure, args=(dataframe[col],))
        rows.append(row)

    matrix = pd.DataFrame(rows, index=dataframe.columns)
    return matrix

def compute_connections(dataframe, similarity_measure=normalized_mutual_info_score):
    """
    Create a dict of neuron pairs and their corresponding correlation/similarity

    Inputs:
        dataframe: pandas DataFrame
            A TxN DataFrame where T is the number of observations (time bins)
            and N is the number of variables (neurons)

        similarity_measure: function, optional
            The similarity metric to be used. Default is
            sklearn.metrics.normalized_mutual_info_score. any function can be
            used, including the pearsonr wrapper in this module.

    Returns:
        connections: dict
            A dictionary in the form of {(i,j):similarity}
    """


    connections = {}
    matrix = similarity_matrix(dataframe, similarity_measure)

    for combination in itertools.combinations(matrix.columns, 2):
        similarity = matrix[combination[0]][combination[1]]
        connections[combination] = similarity

    return connections

def pearsonr(a, b):
    """
    Wrapper for the numpy corrcoef function to compute pearson correlation coefficient.

    Inputs:
        a,b: array-like
            vectors to compute pearson correlation coefficient

    Returns:
        corr: float
            The pearson correlation coefficient

    """
    corr = np.corrcoef(a, b)[0][1]
    return corr

def compute_nmi(dataframe):
    connections = {}
    matrix = nmi_matrix(dataframe)

    for combination in itertools.combinations(matrix.columns, 2):
        nmi = matrix[combination[0]][combination[1]]
        connections[combination] = nmi

    return connections

def nmi_matrix(dataframe):
    rows = []

    for col in dataframe:
        row = dataframe.apply(normalized_mutual_info_score, args=(dataframe[col],))
        rows.append(row)

    return pd.DataFrame(rows, index=dataframe.columns)

def compute_mi(dataframe):
    connections = {}
    matrix = mi_matrix(dataframe)

    for combination in itertools.combinations(matrix.columns, 2):
        mi = matrix[combination[0]][combination[1]]
        connections[combination] = mi

    return connections

def mi_matrix(dataframe):
    rows = []

    for col in dataframe:
        row = dataframe.apply(mutual_info_score, args=(dataframe[col],))
        rows.append(row)

    return pd.DataFrame(rows, index=dataframe.columns)



def compute_corrcoef(dataframe, threshold=0):
    connections = {}

    for neuron_pair in itertools.combinations(dataframe.columns, 2):
        if dataframe[neuron_pair[0]].std() == 0 or dataframe[neuron_pair[1]].std() == 0:
            continue

        corrcoef = np.corrcoef(dataframe[neuron_pair[0]].values, dataframe[neuron_pair[1]].values)[0][1]
        if corrcoef >= threshold:
            connections[neuron_pair] = corrcoef

    return connections

def affinity_propagation(similiarity_matrix):
    """Perform Affinity Propagation Clustering of data

    Note: This function is a wrapper for AffinityPropagation from scikit-learn
    Source: http://scikit-learn.org/stable/modules/generated/sklearn.cluster.AffinityPropagation.html

    Args:
        similarity_matrix: DataFrame, shape (n_samples, n_samples)
            Matrix of similarities between points.

    Returns:
        clusters: dictionary
            A dictionary of <sample: cluster label> key-value pairs.
    """
    clusters = {}

    labels = cluster.AffinityPropagation().fit_predict(similiarity_matrix)
    n_labels = labels.max()

    clusters = {}
    for i in range(n_labels+1):
        for neuron in list(similiarity_matrix.columns[labels==i]):
            clusters[neuron] = i

    return clusters

def extract_clusters(clusters):
    """Extract all the clusters into a dictionary of lists.

    This function takes in a dictionary of <neuron: cluster label>
    key-value pairs and produces a dictionary of <cluster label: neurons>

    Args:
        clusters: dictionary
            A dictionary of <sample: cluster label> key-value pairs.

    Returns:
        extracted_clusters: dictionary
            A dictionary of <cluster label: neurons list> key-value pairs.
    """
    extracted_clusters = {}

    for neuron, cluster_label in clusters.items():
        if extracted_clusters.get(cluster_label, None):
            extracted_clusters[cluster_label].append(neuron)
        else:
            extracted_clusters[cluster_label] = [neuron]

    return extracted_clusters
