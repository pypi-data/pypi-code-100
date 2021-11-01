#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blue Fibrosis Analysis

This file contains the body of loading analyzing and saving the images
for the specific algorithms see fibrosis_analysis.py and for
settings and colo profiles see settings.yaml and color_rules.yaml
"""


import matplotlib.pyplot as plt
import numpy as np
from skimage import color #io, img_as_float, img_as_uint
import yaml

from . import settings
from .fibrosis_segmentation import createColorMasks, findStainAndTissue, findWhite
from .gui.plot_masked_images import showMask, coverUnMasked, beautify
from .tools import openImage

#gethers user input and processes all files, saving and ploting as requested
def processAllFiles(image_filepaths, 
                    save_res_filepath, 
                    save_images_dirpath,
                    color_rules_filepath=None):

    if len(image_filepaths) == 0:
        print("No Image Files Provided")
        return

    savefile = None
    if save_res_filepath != '':
        savefile = open(save_res_filepath, 'w')
        savefile.write(('file name, % stain, Tissue count filter, '
                        'stain count filter, background count filter, '
                        'other count filter, background count regression, '
                        'Tissue count KNN, stain count KNN, background count KNN, '
                        'other count KNN, Tissue count final, stain count final, '
                        'background count final, other count final\n'))

    if color_rules_filepath is not None:
        with open(color_rules_filepath, 'r') as stream:
            color_rules = yaml.safe_load(stream)
            color_rules = color_rules['color_rules']
    else:
        color_rules = settings['color_rules']

    if settings['save_settings'] and save_res_filepath != '':
        settings_filepath = '/'.join(save_res_filepath.split('/')[:-1]+['settings.yaml'])
        settings_cpy = settings.copy()
        settings_cpy.update(dict(color_rules=color_rules))
        with open(settings_filepath, 'w') as file:
            yaml.dump(settings_cpy, file)

    for filepath in image_filepaths:
        im = openImage(filepath)

        filename = filepath.split('/')[-1]
        data = processOne(im, color_rules)

        if savefile is not None:
            savefile.write((
                    '{filename}, {precStainVTissue},'
                    '{tissueFilter}, {stainFilter}, {whiteFilter}, {otherFilter},'
                    '{whiteReg},'
                    '{tissueKNN}, {stainKNN}, {whiteKNN}, {otherKNN},'
                    '{tissueFinal}, {stainFinal}, {whiteFinal}, {otherFinal}\n')\
                    .format(filename=filename,
                            precStainVTissue=data['precStainVTissue'],
                            **data['colorCounts']))
                
        printTextOne(filename, data)
        if settings['show_images']:
            plotOne(filename, data, im)
        if settings['save_images'] and save_images_dirpath != '':
            saveOne(filename, save_images_dirpath, data, im)
#    plt.show()
    if savefile is not None:
        savefile.close()


#process one file, dividing the file into stain, 
# tissue, background (white), and unclassified
def processOne(im, color_rules):
    RGB = np.asarray(im.convert('RGB'))
    RGB_flat = RGB.reshape((RGB.shape[0]*RGB.shape[1], 3))
    uniq_rgb, uniq_inv, uniq_counts = np.unique(RGB_flat, 
                                                return_inverse=True,
                                                return_counts=True,
                                                axis=0)
    
    uniq_hsv = np.squeeze(color.rgb2hsv(uniq_rgb[np.newaxis, ...]))
    uniq_hsv = (uniq_hsv*255).astype('uint8')
    
    uniq_lab = np.squeeze(color.rgb2lab(uniq_rgb[np.newaxis, ...]))

#   beware! LAB space is float and can take up lots of memory    
#    LAB = color.rgb2lab(RGB)

    #apply color filters
    whiteMaskFilter, tissueMaskFilter, stainMaskFilter, otherMaskFilter = createColorMasks(uniq_hsv, color_rules)
    
    whiteMaskReg = findWhite(whiteMaskFilter,
                               tissueMaskFilter,
                               stainMaskFilter,
                               otherMaskFilter,
                               uniq_lab)
    otherMask = otherMaskFilter & np.logical_not(whiteMaskReg)

    #catagorize other
    stainMaskKNN, tissueMaskKNN, whiteMaskKNN, otherMaskKNN =\
        findStainAndTissue(whiteMaskReg,
                       tissueMaskFilter,
                       stainMaskFilter,
                       otherMask,
                       uniq_lab)

    tissueMaskFlat = tissueMaskKNN[uniq_inv]
    stainMaskFlat = stainMaskKNN[uniq_inv]
    whiteMaskFlat = whiteMaskKNN[uniq_inv]
    otherMaskFlat = otherMaskKNN[uniq_inv]
    
    tissueMask = tissueMaskFlat.reshape((RGB.shape[0], RGB.shape[1]))
    stainMask = stainMaskFlat.reshape((RGB.shape[0], RGB.shape[1]))
    whiteMask = whiteMaskFlat.reshape((RGB.shape[0], RGB.shape[1]))
    otherMask = otherMaskFlat.reshape((RGB.shape[0], RGB.shape[1]))
   
    colorCounts = dict(tissueFinal=np.sum(tissueMask),
                       stainFinal=np.sum(stainMask),
                       whiteFinal=np.sum(whiteMask),
                       otherFinal=np.sum(otherMask),
                       tissueFilter=np.sum(tissueMaskFilter.astype(int)*uniq_counts),
                       stainFilter=np.sum(stainMaskFilter.astype(int)*uniq_counts),
                       whiteFilter=np.sum(whiteMaskFilter.astype(int)*uniq_counts),
                       otherFilter=np.sum(otherMaskFilter.astype(int)*uniq_counts),
                       whiteReg=np.sum(whiteMaskReg.astype(int)*uniq_counts),
                       stainKNN=np.sum(stainMaskKNN.astype(int)*uniq_counts),
                       tissueKNN=np.sum(tissueMaskKNN.astype(int)*uniq_counts),
                       whiteKNN=np.sum(whiteMaskKNN.astype(int)*uniq_counts),
                       otherKNN=np.sum(otherMaskKNN.astype(int)*uniq_counts),
                   )
    # Calculate the area of the tissue pixels
    tissuecount = np.sum(tissueMask)
    staincount = np.sum(stainMask)
    precStainVTissue=100*(staincount/(staincount+tissuecount))

    data = dict(
        tissueMask = tissueMask,
        stainMask = stainMask,
        whiteMask = whiteMask,
        otherMask = otherMask,
        colorCounts = colorCounts,
        precStainVTissue = precStainVTissue
        )
    return data

#prints the summary text from the analysis of one file
def printTextOne(filename, data):
    text = (
        '{filename}\n'
        'Pixels counts:\n'
        '\tPass 1 (Filter): '
            'Tissue: {tissueFilter}, '
            'Stain: {stainFilter}, '
            'Background: {whiteFilter}, '
            'Other: {otherFilter}\n'
        '\tPass 2 (Regression): '
            'Background: {whiteReg}\n'
        '\tPass 3 (KNN): '
            'Tissue: {tissueKNN}, '
            'Stain: {stainKNN}, '
            'Background: {whiteKNN}, '
            'Other: {otherKNN}\n'
        '\tFinal: '
            'Tissue: {tissueFinal}, '
            'Stain: {stainFinal}, '
            'Background: {whiteFinal}, '
            'Other: {otherFinal}\n'
        'The percent stained tissue in relation to the tissue is %{precStainVTissue}'
        )
    print(text.format(filename=filename,
                      precStainVTissue=data['precStainVTissue'],
                      **data['colorCounts']))
    

#saves the images generated by the analysis
def saveOne(filename, savedir, data, im):
    if savedir is None or len(savedir) == 0:
        return
    filename = filename.split('.')[0]

    savename = '{}/{}_{{}}.jpeg'.format(savedir,filename)

    im.save(savename.format('original'))

    coverUnMasked(im, data['tissueMask'])\
        .save(savename.format('TissueFinal'))
    coverUnMasked(im, data['stainMask'])\
        .save(savename.format('StainFinal'))
    coverUnMasked(im, data['whiteMask'])\
        .save(savename.format('BackgroundFinal'))
    coverUnMasked(im, data['otherMask'])\
        .save(savename.format('OtherFinal'))
    
    beautifyStain = beautify(data['stainMask'], im)
    beautifyStain.save(savename.format('HighlightStain'))

#plots the images generated by analysis
def plotOne(filename, data, im):
    ## Display orginal image
    plt.figure();
    plt.title(filename);
    plt.axis('off')
    plt.imshow(im);

    plt.figure(figsize = (1,2))
    plt.subplot(1,2,1)
    showMask(im, data['tissueMask'], 'Tissue')
    plt.subplot(1,2,2)
    showMask(im, data['stainMask'], 'Stain')

    plt.figure(figsize = (1,2))
    plt.subplot(1,2,1)
    showMask(im, data['whiteMask'], 'Background')
    plt.subplot(1,2,2)
    showMask(im, data['otherMask'], 'Other')

    plt.figure()
    plt.title('Highlight Fibrosis')
    plt.axis('off')
    beautifyStain = beautify(data['stainMask'], im)
    plt.imshow(beautifyStain)



