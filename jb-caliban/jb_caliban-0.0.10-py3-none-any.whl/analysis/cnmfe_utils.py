#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-

"""
Helper functions for manipulating data from CNMFE (https://github.com/zhoupc/CNMF_E)

Many of these functions were written by Tim Machado (https://github.com/zhoupc/CNMF_E/tree/master/python_wrapper), or
were taken from Caiman (https://github.com/flatironinstitute/CaImAn)
"""

import os
import sys

sys.path.append("/OASIS/")

from matplotlib import pyplot as plt
import scipy.sparse as sparse
import numpy as np
import scipy.io as sio
import h5py
import pandas as pd
import analysis.analysis_utils as au

from oasis.functions import estimate_parameters
from oasis.oasis_methods import oasisAR1

def process_cnmfe(neuron, analysis_FR, normalize='std_noise', neural_FR=None, smin=10):
    """
    Deconvolves output from CNMFE and (optionally) normalizes the traces. The 
    raw traces and deconvolved spikes and traces are returned as TxN pandas 
    DataFrame

    Parameters
    ----------
    neuron : dict
        CNMFE results
    analysis_FR : int
        Frames per second that the neural data will be resampledto
    normalize : str
        Indicates which type of normalization to apply to traces
            ('zscore', 'std_noise'). Any other input will prevent normalization
    neural_FR : TYPE, optional
        The current frame rate of the calcium traces. If none is provided,
        this value will be taken from neuron['Fs']. The default is None.
    smin : int, optional
        Minimum spike size is smin*sn, where sn is the computed noise for
        each neuron. The default is 10.

    Returns
    -------
    f : pandas DataFrame
        raw traces
    s : pandas DataFrame
        deconvolved spikes
    c : pandas DataFrame
        deconvolved traces
    """


    F = pd.DataFrame(neuron['C_raw'].T)
    C = pd.DataFrame(neuron['C'].T)
    S = pd.DataFrame(neuron['S'].T)

    #Add timedelta column as index of neural DFs
    if neural_FR is None:
        neural_FR = neuron['Fs']
    frame_length = str(np.round(1000/neural_FR,3)) + 'ms'
    analysis_frame_length = str(np.round(1000/analysis_FR,3)) + 'ms'

    f = au.resample_ts(F, frame_length, analysis_frame_length)
    c = au.resample_ts(C, frame_length, analysis_frame_length)
    s = au.resample_ts(S, frame_length, analysis_frame_length)

    c,s,f = deconvolve_df(f, smin=smin, normalize = normalize) #normalize = 'zscore', 'std_noise'

    c = pd.DataFrame(c)
    s = pd.DataFrame(s)
    f = pd.DataFrame(f)

    s.columns = [x+1 for x in s.columns]
    c.columns = [x+1 for x in c.columns]
    f.columns = [x+1 for x in f.columns]

    return f, s, c
  
def import_cnmfe_caiman(file_path):
    """
    Reads in .hdf5 file containing the estimates structure from CaImAn CNMF-E
    
    Inputs:
        file_path: str
            File path for the .hdf5 CNMF-E CaImAn results
    
    Returns:
        neuron: dict
            Dictionary containing raw, c, s, and frame rate from the .hdf5 results file
    """
    
    # Loads a cnmfe results file that has been saved as a results.hdf5
    cnmf_obj = h5py.File(file_path, 'r')
    
    # Extracts the caiman estimates and frame rate of the calcium imaging recording
    data = cnmf_obj['estimates']
    fr = cnmf_obj['params']['data']['fr'][()]
    
    # Extracts raw, C, and S from the caiman estimates 
    raw = data['C'][()] + data['YrA'][()]
    C = data['C'][()]
    S = data['S'][()]
    
    # Constructs a neuron dictionary to interface with process_cnmfe function
    neuron = {'C_raw':raw,
              'C':C,
              'S':S,
              'Fs':fr}
    
    return neuron
  
def deconvolve_df(F, smin=10, normalize = None):
    """
    Deconvolve raw fluorescence traces

    Inputs:

        F: N x T pandas DataFrame
            Raw fluorescence traces for 1 mouse. This is neuron.C_raw

        smin: float
            Used to limit the minimim spike size. Min spike size = smin * sn

        normalize: str
            Options:
                - 'zscore': divide all traces by standard deviation of raw fluorescence trace.
                - 'std_noise': divide all traces by standard devation of the noise (C_raw - C)
                - anything else: don't normalize
    Returns:
        c: dict
            deconvolved trace
        s: dict
            deconvolved spikes
        F_norm: dict
            normalized raw trace

    """

    c=dict()
    s=dict()
    F_norm = dict()

    #make all nonnegative values 0 to ensure oasis convergence
    #F = F[F>0]
    #F = F.fillna(0)

    for i in F.columns:
        #define which trace to use
        f = F[i].values

        #estimate g, sn parameters
        est = estimate_parameters(f,p=1,fudge_factor=0.99)
        g=est[0]
        sn=est[1]
        # Deconvolve with threshold s_min = 10*sn

        c[i], s[i] = oasisAR1(f, g = g, s_min = smin*sn)


        #Optional: normalize f,c,s
        # from PC: instead of normalizing by dividing by std(F), normalize by dividing by std(F-C)
        sigma = 1
        if normalize == 'zscore':
            sigma = np.std(f)
        elif normalize == 'std_noise':
            sigma = np.std(f - c[i])

        f = f / sigma
        c[i] = c[i] / sigma
        s[i] = s[i] / sigma

        F_norm[i] = f

    return c, s, F_norm

def get_cnmfe_data(data_folder, mouse, behavior):
    """
    Reads in .mat file containing the neuron structure from Matlab CNMF_E
    Assumes folder structure is designed as follows:
        data_folder/mouse/behavior/cnmfe_results.mat
    Converts all sparse arrays to dense

    Inputs:
        data_folder: str
            Folder where all the data files are located
        mouse: str
            Name of the mouse
        behavior:str
            Name of the behavior
    Returns:
        data: dict
            Python dictionary containing all data from matlab
    """
    import glob

    mouse_folder = os.path.join(data_folder,mouse)

    if not os.path.isdir(mouse_folder):
        print('Error! There is no folder for ' + mouse)
        return

    behavior_folder = None
    for folder in os.listdir(mouse_folder):
        #if behavior in folder:
        if folder.endswith(behavior):
            behavior_folder = folder
    if not behavior_folder:
        print('Error! There is no folder for '+ mouse + ' '+ behavior)
        return

    file = glob.glob(os.path.join(mouse_folder, behavior_folder, '*.mat'))
    data={}
    if file:
        file = file[0]
        data = loadmat(file)

        #if neuron was saved using CNMFE's save function, need to load neuron_results
        if 'C_raw' not in data.keys():
            if 'neuron_results' in data.keys():
                data = data['neuron_results']
        #data = sio.loadmat(os.path.join(mouse_folder, behavior_folder, 'cnmfe_results.mat'), squeeze_me = True, struct_as_record = False)

    for k,v in data.items():
        if sparse.issparse(v):
            data[k] = v.todense()
    return data

def loadmat(filename):
    '''
    this function should be called instead of direct sio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects

    from https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries/7418519
    '''
    data = sio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries

    from https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries/7418519

    '''
    for key in dict:
        if isinstance(dict[key], sio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries

    from https://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries/7418519

    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, sio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict

def xy_dist(p1, p2):
    """
    Computes the euclidian distance between two 2D points

    Inputs:
        p1,p2: tuple of floats
            The (x,y) location of each point
    Returns:
        dist: float
            The Euclidian distance between p1 and p2
    """

    dist = np.sqrt((p1[0]-p2[0])**2 + (p1[1] - p2[1])**2)
    return dist

def normalize(trace, percentile=True):
    """ Normalize a fluorescence trace by its max or its 99th percentile. """
    #trace = trace - np.min(trace)

    if percentile:
        if np.percentile(trace, 99) > 0:
            trace = trace / np.percentile(trace, 99)

    elif np.max(trace) > 0:
        trace = trace / np.max(trace)

    return trace


def com(A, d1, d2):
    """Calculation of the center of mass for spatial components

       From Caiman: https://github.com/flatironinstitute/CaImAn
       @author: agiovann

     Inputs:
     ------
     A:   np.ndarray
          matrix of spatial components (d x K)

     d1:  int
          number of pixels in x-direction

     d2:  int
          number of pixels in y-direction

     Output:
     -------
     cm:  np.ndarray
          center of mass for spatial components (K x 2)
    """
    nr = np.shape(A)[-1]
    Coor = dict()
    Coor['x'] = np.kron(np.ones((d2, 1)), np.expand_dims(list(range(d1)),
                                                         axis=1))
    Coor['y'] = np.kron(np.expand_dims(list(range(d2)), axis=1),
                        np.ones((d1, 1)))
    cm = np.zeros((nr, 2))        # vector for center of mass
    cm[:, 0] = old_div(np.dot(Coor['x'].T, A), A.sum(axis=0))
    cm[:, 1] = old_div(np.dot(Coor['y'].T, A), A.sum(axis=0))

    return cm


def plot_contours(A, Cn, thr=None, thr_method='max', maxthr=0.2, nrgthr=0.9,
                  display_numbers=True, max_number=None,
                  cmap=None, swap_dim=False, colors='w', vmin=None,
                  vmax=None, neuron_list=None, show_bg=False, **kwargs):
    """Plots contour of spatial components against a background image
       and returns their coordinates

       From Caiman: https://github.com/flatironinstitute/CaImAn
       @author: agiovann

     Parameters:
     -----------
     A:   np.ndarray or sparse matrix
               Matrix of Spatial components (d x K)

     Cn:  np.ndarray (2D)
               Background image (e.g. mean, correlation)

     thr_method: [optional] string
              Method of thresholding:
                  'max' sets to zero pixels that have value less
                  than a fraction of the max value
                  'nrg' keeps the pixels that contribute up to a
                  specified fraction of the energy

     maxthr: [optional] scalar
                Threshold of max value

     nrgthr: [optional] scalar
                Threshold of energy

     thr: scalar between 0 and 1
               Energy threshold for computing contours (default 0.9)
               Kept for backwards compatibility.
               If not None then thr_method = 'nrg', and nrgthr = thr

     display_number:     Boolean
               Display number of ROIs if checked (default True)

     max_number:    int
               Display the number for only the first max_number components
               (default None, display all numbers)

     cmap:     string
               User specifies the colormap (default None, default colormap)

     neuron_list:   list
               User specififies which neurons to plot

     Returns:
     --------
     Coor: list of coordinates with center of mass,
        contour plot coordinates and bounding box for each component
    """

    linewidths = kwargs.get('linewidths', 1)
    fontsize = kwargs.get('fontsize', 12)
    fontname = kwargs.get('fontname', 'Arial')
    fontweight = kwargs.get('fontweight', 'bold')
    fontcolor = kwargs.get('fontcolor', colors)
    if sparse.issparse(A):
        A = np.array(A.todense())
    else:
        A = np.array(A)

    if swap_dim:
        Cn = Cn.T
        print('Swapping dim')

    d1, d2 = np.shape(Cn)
    d, nr = np.shape(A)
    if max_number is None:
        max_number = nr

    if neuron_list:
        neuron_list = [i-1 for i in neuron_list]
    else:
        neuron_list = range(np.minimum(nr, max_number))

    if thr is not None:
        thr_method = 'nrg'
        nrgthr = thr
        print("The way to call utilities.plot_contours has changed.")

    if show_bg:
        x, y = np.mgrid[0:d1:1, 0:d2:1]
    else:
        x, y = np.mgrid[d1:0:-1, 0:d2:1] #reverse y direction to get correct orientation
    ax = plt.gca()

    if show_bg:
        if vmax is None and vmin is None:
            plt.imshow(Cn, interpolation=None, cmap=cmap,
                       vmin=np.percentile(Cn[~np.isnan(Cn)], 1),
                       vmax=np.percentile(Cn[~np.isnan(Cn)], 99))
        else:
            plt.imshow(Cn, interpolation=None, cmap=cmap,
                       vmin=vmin, vmax=vmax)

    coordinates = []
    cm = com(A, d1, d2)
    for i in neuron_list:
        pars = dict(kwargs)
        if thr_method == 'nrg':
            indx = np.argsort(A[:, i], axis=None)[::-1]
            cumEn = np.cumsum(A[:, i].flatten()[indx]**2)
            cumEn /= cumEn[-1]
            Bvec = np.zeros(d)
            Bvec[indx] = cumEn
            thr = nrgthr

        else:
            if thr_method != 'max':
                print("Unknown threshold method. Choosing max")
            Bvec = A[:, i].flatten()
            Bvec /= np.max(Bvec)
            thr = maxthr

        if swap_dim:
            Bmat = np.reshape(Bvec, np.shape(Cn), order='C')
        else:
            Bmat = np.reshape(Bvec, np.shape(Cn), order='F')
        cs = plt.contour(y, x, Bmat, [thr], colors=colors, linewidths = linewidths)

        # this fix is necessary for having disjoint figures and borders
        p = cs.collections[0].get_paths()
        v = np.atleast_2d([np.nan, np.nan])
        for pths in p:
            vtx = pths.vertices
            num_close_coords = np.sum(np.isclose(vtx[0, :], vtx[-1, :]))
            if num_close_coords < 2:
                if num_close_coords == 0:
                    # case angle
                    newpt = np.round(old_div(vtx[-1, :], [d2, d1])) * [d2, d1]
                    vtx = np.concatenate((vtx, newpt[np.newaxis, :]), axis=0)

                else:
                    # case one is border
                    vtx = np.concatenate((vtx, vtx[0, np.newaxis]), axis=0)

            v = np.concatenate((v, vtx, np.atleast_2d([np.nan, np.nan])),
                               axis=0)

        pars['CoM'] = np.squeeze(cm[i, :])
        pars['coordinates'] = v
        pars['bbox'] = [np.floor(np.min(v[:, 1])), np.ceil(np.max(v[:, 1])),
                        np.floor(np.min(v[:, 0])), np.ceil(np.max(v[:, 0]))]
        pars['neuron_id'] = i + 1
        coordinates.append(pars)

    if display_numbers:
        for i in neuron_list:

            x = cm[i, 1]
            if show_bg:
                y = cm[i, 0]
            else:
                y = d1-cm[i, 0] #need to flip to preserve location if theres no background

            if swap_dim:
                ax.text(y, x, str(i + 1), color=colors)
            else:
                ax.text(x, y, str(i + 1), color=fontcolor,
                        fontsize=fontsize, fontname=fontname,
                        fontweight=fontweight)

    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_aspect('equal')
    
    return coordinates

def old_div(a, b):
    """
    DEPRECATED: import ``old_div`` from ``past.utils`` instead.

    Equivalent to ``a / b`` on Python 2 without ``from __future__ import
    division``.

    TODO: generalize this to other objects (like arrays etc.)
    """

    return a // b