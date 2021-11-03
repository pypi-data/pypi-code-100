"""
Author      : Yi-Chieh Wu
Class       : HMC CS 158
Date        : 2017 Feb 27
Description : Famous Faces
"""

import collections
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


######################################################################
# classes
######################################################################

class Point(object) :
    
    def __init__(self, name, label, attrs) :
        """
        A data point.
        
        Attributes
        --------------------
            name  -- string, name
            label -- string, label
            attrs -- numpy array, features
        """
        
        self.name = name
        self.label = label
        self.attrs = attrs
    
    
    #============================================================
    # utilities
    #============================================================
    
    def distance(self, other) :
        """
        Return Euclidean distance of this point with other point.
        
        Parameters
        --------------------
            other -- Point, point to which we are measuring distance
        
        Returns
        --------------------
            dist  -- float, Euclidean distance
        """
        # Euclidean distance metric
        return np.linalg.norm(self.attrs-other.attrs)
    
    
    def __str__(self) :
        """
        Return string representation.
        """
        return "%s : (%s, %s)" % (self.name, str(self.attrs), self.label)


class Cluster(object) :
    
    def __init__(self, points) :
        """
        A cluster (set of points).
        
        Attributes
        --------------------
            points -- list of Points, cluster elements
        """        
        self.points = points
    
    
    def __str__(self) :
        """
        Return string representation.
        """
        s = ""
        for point in self.points :
            s += str(point)
        return s
        
    #============================================================
    # utilities
    #============================================================
    
    def purity(self) :
        """
        Compute cluster purity.
        
        Returns
        --------------------
            n           -- int, number of points in this cluster
            num_correct -- int, number of points in this cluster
                                with label equal to most common label in cluster
        """        
        labels = []
        for p in self.points :
            labels.append(p.label)
        
        cluster_label, count = stats.mode(labels)
        return len(labels), np.float64(count)
    
    
    def centroid(self) :
        """
        Compute centroid of this cluster.
        
        Returns
        --------------------
            centroid -- Point, centroid of cluster
        """
        
        X = []
        labels = []
        for p in self.points :
            X.append(p.attrs)
            labels.append(p.label)
        label, count = stats.mode(labels) # label is most common label in cluster
        centroid = Point(str(np.mean(X,0)), label, np.mean(X,0))
        return centroid
    
    
    def medoid(self) :
        """
        Compute medoid of this cluster, that is, the point in this cluster
        that is closest to all other points in this cluster.
        
        Returns
        --------------------
            medoid -- Point, medoid of this cluster
        """
        
        min_dist = float("inf")
        medoid = None
        
        for p in self.points :
            total_dist = 0
            for other in self.points :
                total_dist += p.distance(other)
            if total_dist < min_dist:
                min_dist = total_dist
                medoid = p
        
        if medoid is None :
            raise Exception('Warning Empty Cluster!')
        
        return medoid
    
    
    def equivalent(self, other) :
        """
        Determine whether this cluster is equivalent to other cluster.
        Two clusters are equivalent if they contain the same set of points
        (not the same actual Point objects but the same geometric locations).
        
        Parameters
        --------------------
            other -- Cluster, cluster to which we are comparing this cluster
        
        Returns
        --------------------
            flag  -- bool, True if both clusters are equivalent or False otherwise
        """
        
        if len(self.points) != len(other.points) :
            return False
        
        matched = []
        for point1 in self.points :
            for point2 in other.points :
                if point1.distance(point2) == 0 and point2 not in matched :
                    matched.append(point2)
        return len(matched) == len(self.points)


class ClusterSet(object):

    def __init__(self) :
        """
        A cluster set (set of clusters).
        
        Parameters
        --------------------
            members -- list of Clusters, clusters that make up this set
        """
        self.members = []
    
    
    #============================================================
    # utilities
    #============================================================    
    
    def centroids(self) :
        """
        Return centroids of each cluster in this cluster set.
        
        Returns
        --------------------
            centroids -- list of Points, centroids of each cluster in this cluster set
        """
        
        centroids = []
        for cluster in self.members :
            centroids.append(cluster.centroid())
        return centroids
    
    
    def medoids(self) :
        """
        Return medoids of each cluster in this cluster set.
        
        Returns
        --------------------
            medoids -- list of Points, medoids of each cluster in this cluster set
        """
        
        medoids = []
        for cluster in self.members :
            medoids.append(cluster.medoid())
        return medoids
    
    
    def score(self) :
        """
        Compute average purity across clusters in this cluster set.
        
        Returns
        --------------------
            score -- float, average purity
        """
        
        total_correct = 0
        total = 0
        for c in self.members :
            n, n_correct = c.purity()
            total += n
            total_correct += n_correct
        return total_correct / float(total)
    
    
    def equivalent(self, other) :
        """ 
        Determine whether this cluster set is equivalent to other cluster set.
        Two cluster sets are equivalent if they contain the same set of clusters
        (as computed by Cluster.equivalent(...)).
        
        Parameters
        --------------------
            other -- ClusterSet, cluster set to which we are comparing this cluster set
        
        Returns
        --------------------
            flag  -- bool, True if both cluster sets are equivalent or False otherwise
        """
        
        if len(self.members) != len(other.members):
            return False
        
        matched = []
        for cluster1 in self.members :
            for cluster2 in other.members :
                if cluster1.equivalent(cluster2) and cluster2 not in matched:
                    matched.append(cluster2)
        return len(matched) == len(self.members)
    
    
    #============================================================
    # manipulation
    #============================================================

    def add(self, cluster):
        """
        Add cluster to this cluster set (only if it does not already exist).
        
        If the cluster is already in this cluster set, raise a ValueError.
        
        Parameters
        --------------------
            cluster -- Cluster, cluster to add
        """
        
        if cluster in self.members :
            raise ValueError
        
        self.members.append(cluster)


######################################################################
# k-means and k-medoids
######################################################################

def random_init(points, k) :
    """
    Randomly select k unique elements from points to be initial cluster centers.
    
    Parameters
    --------------------
        points         -- list of Points, dataset
        k              -- int, number of clusters
    
    Returns
    --------------------
        initial_points -- list of k Points, initial cluster centers
    """
    return np.random.choice(points, k, replace=False)


def cheat_init(points) :
    """
    Initialize clusters by cheating!
    
    Details
    - Let k be number of unique labels in dataset.
    - Group points into k clusters based on label (i.e. class) information.
    - Return medoid of each cluster as initial centers.
    
    Parameters
    --------------------
        points         -- list of Points, dataset
    
    Returns
    --------------------
        initial_points -- list of k Points, initial cluster centers
    """
    
    clusters = collections.defaultdict(list) # key = class, val = list of points with this class
    for point in points :
        clusters[point.label].append(point)
    
    medoids = []
    for cluster in clusters :
        medoids.append(Cluster(clusters[cluster]).medoid())
    return medoids


def kAverages(points, k, average=ClusterSet.centroids, init='random', plot=False) :
    """
    Cluster points into k clusters using variations of k-means algorithm.
    
    Parameters
    --------------------
        points  -- list of Points, dataset
        k       -- int, number of clusters
        average -- method of ClusterSet
                   determines how to calculate average of points in cluster
                   allowable: ClusterSet.centroids, ClusterSet.medoids
        init    -- string, method of initialization
                   allowable: 
                       'cheat'  -- use cheat_init to initialize clusters
                       'random' -- use random_init to initialize clusters
        plot    -- bool, True to plot clusters with corresponding averages
                         for each iteration of algorithm
    
    Returns
    --------------------
        k_clusters -- ClusterSet, k clusters
    """
    
    # initialize
    if init == 'cheat':
        centroids = cheat_init(points)
        if len(centroids) != k:
            raise Warning("The chosen k is not equal to the number of actual classes.")
    else:
        centroids = random_init(points, k)
    
    it = 0
    old_clusters = ClusterSet()
    new_clusters = ClusterSet()
    for centroid in centroids :
        new_clusters.add(Cluster([centroid]))
    centroids = average(new_clusters)
    
    # clustering step
    while not new_clusters.equivalent(old_clusters) :
        # key = centroid
        # val = list of Points closest to this centroid (compared to other centroids)
        cluster_assignments = collections.defaultdict(list)
        
        ## step 1: get new cluster assignments
        for point in points :
            min_dist = float('inf')
            best_centroid = None
            for centroid in centroids :
                dist = point.distance(centroid)
                if dist < min_dist :
                    min_dist = dist
                    best_centroid = centroid
            cluster_assignments[best_centroid].append(point)
        
        ## step 2: create new ClusterSet based on new assignments
        ##         then update centroids
        old_clusters = new_clusters
        new_clusters = ClusterSet()
        for centroid in cluster_assignments :
            new_clusters.add(Cluster(cluster_assignments[centroid]))
        centroids = average(new_clusters)
        
        # plot if desired
        if plot :
            plot_clusters(new_clusters, 'Iteration'+str(it), average)
        
        it += 1
    
    return new_clusters


def kMeans(points, k, init='random', plot=False) :
    """
    Cluster points into k clusters using k-means clustering.
    (Wrapper around kAverages(...).)
    """
    return kAverages(points, k, ClusterSet.centroids, init, plot)


def kMedoids(points, k, init='random', plot=False) :
    """
    Cluster points in k clusters using k-medoids clustering.
    (Wrapper around kAverages(...).)
    """
    return kAverages(points, k, ClusterSet.medoids, init, plot)


def plot_clusters(clusters, title, average) :
    """
    Plot clusters along with average points of each cluster.

    Parameters
    --------------------
        clusters -- ClusterSet, clusters to plot
        title    -- string, plot title
        average  -- method of ClusterSet
                    determines how to calculate average of points in cluster
                    allowable: ClusterSet.centroids, ClusterSet.medoids
    """
    
    plt.figure()
    np.random.seed(20)
    label = 0
    colors = {}
    centroids = average(clusters)
    for c in centroids :
        coord = c.attrs
        plt.plot(coord[0],coord[1], 'ok', markersize=12)
    for cluster in clusters.members :
        label += 1
        colors[label] = np.random.rand(3,)
        for point in cluster.points :
            coord = point.attrs
            plt.plot(coord[0], coord[1], 'o', color=colors[label])
    plt.title(title)
    plt.show()