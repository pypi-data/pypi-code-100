#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:07:17 2019

@author: alexj, grat05
"""

from scipy.ndimage import gaussian_filter
from scipy.ndimage.morphology import binary_erosion
from skimage.morphology import disk
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
global erode

def FindNuclei(imarr_rgb, tol, RGB, Brightness):
    print('started!')
    upper = RGB + RGB*tol
    lower = RGB - RGB*tol
    avg = np.mean(imarr_rgb, axis=2)
    imrat = imarr_rgb/avg[...,None]
    magnitude = np.less(avg, Brightness)
    colormatch = np.sum(np.logical_and(imrat>lower,imrat<upper),axis=2)
    regions = 255*np.invert(np.logical_and(magnitude==True,colormatch==3))
    regions_filter = gaussian_filter(regions, sigma=2)
    mask = np.less(regions_filter,225)
    erode = binary_erosion(mask, disk(3))
    coordN =  np.array(np.where(erode == 1)).transpose()
    C_scale = StandardScaler().fit_transform(coordN)
    db = DBSCAN(eps=0.005, min_samples=5, n_jobs=-1).fit(C_scale)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labelsN = db.labels_
    n_clusters = np.max(labelsN)+1
    centroidsN = np.zeros((np.max(labelsN)+1,3))
    for i in range(np.max(labelsN)+1):
        indices = np.where(labelsN == i)[0]
        coordNi = coordN[indices]
        centroidsN[i,0:2] = np.mean(coordNi,axis=0) # centroid of each cluster
        centroidsN[i,2] = np.max(np.sum(np.abs(coordNi[:,0:2]-centroidsN[i,0:2]),axis=1))
    print("Nuclei identified: %d" %n_clusters)
    return centroidsN

def FindBrownDots(imarr_rgb, tol, RGB, Brightness):
    global erode
    print('started!')
    upper = RGB + RGB*tol
    lower = RGB - RGB*tol
    avg = np.mean(imarr_rgb, axis=2)
    imrat = imarr_rgb/avg[...,None]
    magnitude = np.less(avg, Brightness)
    colormatch = np.sum(np.logical_and(imrat>lower,imrat<upper),axis=2)
    regions = 255*np.invert(np.logical_and(magnitude==True,colormatch==3))
    regions_filter = gaussian_filter(regions, sigma=2)
    mask = np.less(regions_filter,190)
    erode = binary_erosion(mask, disk(1))

    coordB = np.array(np.where(erode == 1)).transpose()
    C_scale = StandardScaler().fit_transform(coordB)
    db = DBSCAN(eps=0.01, min_samples=5, n_jobs=-1).fit(C_scale)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labelsB = db.labels_
    n_clusters = np.max(labelsB)+1
    centroidsB = np.zeros((np.max(labelsB)+1,3))
    for i in range(np.max(labelsB)+1):
        indices = np.where(labelsB == i)[0]
        coordBi = coordB[indices]
        centroidsB[i,0:2] = np.mean(coordBi,axis=0) # centroid of each cluster
        centroidsB[i,2] = np.max(np.sum(np.abs(coordBi[:,0:2]-centroidsB[i,0:2]),axis=1))
    print("Macrophages identified: %d" %n_clusters)
#    print(centroidsB)
    return centroidsB

def Colocalize(centroidsB, centroidsN):
    selected = []
    for i in range(len(centroidsB)):
        dists = np.sum(np.abs(centroidsB[i,0:2]-centroidsN[:,0:2]),axis=1)
        min_pos = np.argmin(dists)
        min_dist = dists[min_pos]
        if min_dist <= 3*(centroidsB[i,2]+centroidsN[min_pos,2]):
            selected.append(centroidsB[i,0:2])
    sel = np.asarray(selected)
    print("Macrophages Detected after Colocalization: %d" %len(sel))
    return sel