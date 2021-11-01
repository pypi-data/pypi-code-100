#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the additional color segmentation algorithms used after the
color filters have been run
"""


import sklearn.linear_model as lm
import sklearn.neighbors as nei
import numpy as np

from . import settings

# this function creates the color masks
# given the rules from a color_rules file
def createColorMasks(HSV, rules):
    hsv_2_index = dict(H=0, S=1, V=2)
    if len(HSV.shape) == 3:
        shape = HSV.shape[:2]
    elif len(HSV.shape) == 2:
        shape = HSV.shape[:1]

    def makeMaskRules(color_rule, shape):
        mask = np.ones(shape, dtype='bool')
        for channel, ch_rules in color_rule.items():
            if len(ch_rules) == 0:
                continue
            channel_mask = np.zeros(shape, dtype='bool')
            i = hsv_2_index[channel]
            for rule in ch_rules:
                channel_mask |= ((rule[0] <= HSV[...,i]) &\
                                (HSV[...,i] <= rule[1]))
            mask &= channel_mask
        return mask
    
    whiteMask = makeMaskRules(rules['background'], shape)
    
    tissueMask = makeMaskRules(rules['tissue'], shape)
    tissueMask &= np.logical_not(whiteMask)

    stainMask = makeMaskRules(rules['stain'], shape)
    stainMask &= np.logical_not(whiteMask)

    otherMask = np.logical_not(whiteMask|stainMask|tissueMask)

    return whiteMask, tissueMask, stainMask, otherMask

#segement out the white from other/unknown
#this uses linear regression on the already categorized white in order to
#predict which uncategorized pixels may be white
def findWhite(whiteMask,tissueMask,stainMask,otherMask,HSV):
    whiteVTissueMask = whiteVsColor(whiteMask,tissueMask,otherMask,HSV)
    whiteVStainMask = whiteVsColor(whiteMask,stainMask,otherMask,HSV)
    otherwhiteMask = whiteVTissueMask & whiteVStainMask
    return otherwhiteMask

#categorize white pixes in other/unknown given the pixes which are white and
#colored from the rest of the image
def whiteVsColor(whiteMask,colorMask,otherMask,HSV_flat):
    labels = np.ones(shape=(colorMask.sum()+whiteMask.sum()), dtype='int8')
    labels[:colorMask.sum()] = 0 #0 for color 1 for white

    w_and_c = np.ones((len(labels), 3), dtype='int8')
    w_and_c[:colorMask.sum(),:] = HSV_flat[colorMask]
    w_and_c[colorMask.sum():,:] = HSV_flat[whiteMask]
    
    other = HSV_flat[otherMask,:]

    regress = lm.LogisticRegression()
    regress.fit(w_and_c,labels)
    pred = regress.predict(other)

    otherWhiteMask = whiteMask.copy()
    otherWhiteMask[otherMask] = pred

    return otherWhiteMask

#segement out stain and tissue from other/unkown
#this uses KNN to predict the color label for unkown pixels
def findStainAndTissue(whiteMask,tissueMask,stainMask,otherMask,LAB_flat):
    num_pixels = min(settings['KNN']['max_pixels'], LAB_flat.shape[0])
    num_stain = int(num_pixels * settings['KNN']['frac_stain'])
    num_tissue = int(num_pixels * settings['KNN']['frac_tissue'])
    num_white = num_pixels - num_stain - num_tissue
    
    other = LAB_flat[otherMask,:]
    
    pixels = np.empty((num_pixels,3), dtype=LAB_flat.dtype)
    locs = np.random.choice(stainMask.sum(),
                            size=num_stain,
                            replace=(num_stain > stainMask.sum()))
    pixels[:num_stain] = LAB_flat[stainMask][locs]
    locs = np.random.choice(tissueMask.sum(),
                            size=num_tissue,
                            replace=(num_tissue > tissueMask.sum()))
    pixels[num_stain:(num_stain+num_tissue)] = LAB_flat[tissueMask][locs]
    locs = np.random.choice(whiteMask.sum(),
                            size=num_white,
                            replace=(num_white > whiteMask.sum()))
    pixels[(num_stain+num_tissue):] = LAB_flat[whiteMask][locs]
    
    labels = np.ones((num_pixels), dtype=LAB_flat.dtype)
    labels[:num_stain] = 0 #stain label
    labels[num_stain:(num_stain+num_tissue)] = 1 #tissue label
    labels[(num_stain+num_tissue):] = 2 #white label

    regress = nei.KNeighborsClassifier(**settings['KNN']['raw'])
    regress.fit(pixels,labels)
    
    pred_prob = regress.predict_proba(other)
    pred_round = np.argmax(pred_prob,axis=1)
    max_prob = np.max(pred_prob,axis=1)
    pred_round[max_prob < settings['KNN']['min_consensus']] = -1
    pred_round[pred_round == 2] = -1

    other_labels = np.ones(otherMask.shape, dtype='int16')*-2
    other_labels[otherMask] = pred_round
    
    knn_stain_mask = stainMask | (other_labels == 0)
    knn_tissue_mask = tissueMask | (other_labels == 1)
    knn_white_mask = whiteMask | (other_labels == 2)
    knn_other_mask = otherMask | (other_labels == -1)

    return knn_stain_mask, knn_tissue_mask, knn_white_mask, knn_other_mask
