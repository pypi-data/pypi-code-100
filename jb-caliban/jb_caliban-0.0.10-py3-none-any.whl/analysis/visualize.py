"""This module contains wrapper functions for plotting and visualizing data.

    @authors: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
              Jack Berry, Columbia University, jeb2242@columbia.edu
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
from scipy.ndimage.filters import gaussian_filter
import scipy.sparse as sparse
import math
import analysis.analysis_utils as au

from itertools import combinations_with_replacement
from matplotlib.patches import Rectangle

#### Plotting functions for spatial activity ####

def plot_spatial_maps(mouse, neuron_data_df, m, neuron_list=None, norm_by_mouse=True, savefig=False,
                      filepath=None, filename=None, heatmap_bin_size=1, h=2, behavior=None, fmt='png', **kwargs):

    """
    Plots an event plot and ratemap for a subset of neurons in a given session

    TODO: finish commenting

    """
    
    #figsize = kwargs.get('figsize',(8,8))
    #cmap = kwargs.get('cmap','jet')
    #vmin = kwargs.get('vmin',0)
    neural_df = mouse.spikes
    beh_df = mouse.behavior[['X_bin', 'Y_bin']]
    df = pd.concat([neural_df, beh_df],axis=1)
    occupancy = df.groupby(['X_bin', 'Y_bin']).size()
    activity = df.groupby(['X_bin', 'Y_bin']).sum()
    x_max, y_max = behavior_boundaries(mouse.behavior.X_center, mouse.behavior.Y_center)

    max_rate = None

    if norm_by_mouse:
        max_rate = mouse_max_rate(activity_df=activity, occupancy_df=occupancy,
                                  heatmap_bin_size=heatmap_bin_size, h=h, fr=mouse.FR)

    if not neuron_list:
        neuron_list = mouse.spikes.columns

    for n in neuron_list:

        neural = mouse.spikes[n]
        behavior_df = mouse.behavior
        neuron_data = neuron_data_df.set_index(['mouse', 'neuron']).xs([m, n])

        plot_spatial(neural=neural, behavior_df=behavior_df, neuron_data=neuron_data, m=m, n=n,
                     heatmap_bin_size=heatmap_bin_size, savefig=savefig, filepath=filepath, filename=filename,
                     max_rate=max_rate, h=h, x_max=x_max, y_max=y_max, behavior=behavior, fmt=fmt,**kwargs)

def mouse_max_rate(activity_df, occupancy_df, heatmap_bin_size=1, h=2, fr=10):
    """
    Computes the maximum rate in any heatmap bin for the entire FOV. Intended to be used as a
    helper function for plot_spatial_maps. This is used to normalize the ratemap per mouse, as
    opposed to each neuron.

    TODO: finish commenting

    """
    activity_norm = activity_df.apply(lambda x: fr*x/occupancy_df)
    mouse_max = activity_norm.max().max()

    s = h/heatmap_bin_size
    mouse_gauss_max = (mouse_max/(s**2*math.pi))

    return mouse_gauss_max

def behavior_boundaries(x, y):
    """
    Defines the width and length of the behavioral arena, as defined by the mouse position. Intended to be used as a helper funtion
    for plot_spatial_maps

    TODO: finish commenting

    """

    x_max = x.max() - x.min()
    y_max = y.max() - y.min()

    return x_max, y_max


def plot_spatial(neural = None, behavior_df = None, neuron_data = None, m = None, n = None,
                 heatmap_bin_size = 1, h = 2, max_rate = None, savefig = False, filepath = None, 
                 filename = None, x_max = 50, y_max = 50, behavior = None, fmt='png',**kwargs):
    """
    Plots event map and rate map for a given neuron.

    TODO: finish commenting and make more general by taking out arm score

    Inputs:
        neural: Pandas Series
            The spike train for one neuron. 
        behavior_df: Pandas DataFrame
            Behavior DataFrame
        neuron_data: Pandas Series
            Relevant data
        m: str
            mouse name
        n: str
            neuron name
        filepath: str
            location to save figures
        heatmap_bin_size: int
            size (in cm) of bin size for plotting
        h: int
            smoothing kernel size (cm), genenrally the same as the bin size (for calculating spatial info)
        x_max: float
            width of arena, used for setting heatmap bin size
        y_max: float
            length of arena, usd for setting heatmap bin size
    
    """   

    df = pd.concat([neural, behavior_df],axis=1)
    occupancy = df.groupby(['X_bin','Y_bin']).size()
    activity = df.groupby(['X_bin','Y_bin']).sum()

    activity_norm = activity.apply(lambda x: 10*x/occupancy)

    x_bin = activity.reset_index().X_bin
    y_bin = activity.reset_index().Y_bin

    b = (x_max/heatmap_bin_size, y_max/heatmap_bin_size) 

    s = h/heatmap_bin_size #sigma =smoothing factor

    t= "{}, neuron {}.{}".format(m,n,fmt)

    #nipy_spectral

    if not filename:
        filename = "{}, EPM, neuron {}".format(m,n)

    filename1 = filename + ', eventmap.png'
    filename2 = filename + ', ratemap.png'

    #_=neuron_activity_plot(x, y, neural, t, savefig = savefig, filepath = filepath, filename = filename1)

    figsize = kwargs.get('figsize',(8,8))

    neuron_event_plot(df, neuron = n, behavior = behavior, title = t, savefig = savefig,
                      filepath = filepath, filename = filename1,**kwargs)
    
    cmap = kwargs.get('cmap','jet')
    vmin=kwargs.get('vmin',0)
    plot_heatmap(x_bin, y_bin, bins = b, weights = activity_norm[n], sigma = s, vmin = vmin, vmax = max_rate, 
                     cmap = cmap, title = t, savefig = savefig, filename = filename2, filepath = filepath,
                     figsize=figsize)


def neuron_event_plot(df, neuron, behavior = None, ax=None, **kwargs):
    """
    Plots event map for a given neuron
    
    TODO: finish commenting
    
    """
    
    df[neuron] = df[neuron].where(df[neuron] == 0, 1)
    lw = kwargs.get('linewidth',1)
    s = kwargs.get('s',5) #markersize
    if ax is None:
        figsize = kwargs.get('figsize', (8,8))
        f,ax = plt.subplots(figsize=figsize)
        
    x = df.X_center
    y = df.Y_center

    savefig = kwargs.get('savefig', False)
    filepath = kwargs.get('filepath', None)
    filename = kwargs.get('filename', None)
    title = kwargs.get('title', None)
    
    show_path = kwargs.get('show_path',True)
    a1=0
    if show_path:
        a1 = .1
    ax.scatter(x, y, alpha=a1, linewidth = 0, s=s/2, color = 'grey')
    sns.scatterplot(x = 'X_center', y = 'Y_center', color = 'red', 
                    palette = sns.color_palette(['blue','red']), s = s,
                    marker = 'x', alpha = 0.6, linewidth = lw, hue = behavior,
                    legend = False, hue_order = [0,1], 
                    data = df[df[neuron]>0], ax=ax)
    sns.despine()
    plt.title(title)
    
    if savefig:
        plt.savefig(os.path.join(filepath, filename), dpi = 300)
        
    return ax

def set_weights(x, y, neuron, data, max_rate, framerate=10):
    """Create list of weights by time spent in a location

    Args:
        x: str
            The name of the x-coordinate column in data.

        y: str
            The name of the y-coordinate column in data.

        neuron: str or int
            The name of the neuron column in data.

        data: DataFrame
            The concatenated neuron and behavior DataFrame.

        framerate: int, optional: default: 10
            The framerate of the calcium imaging video.

    Returns:
        weights: list
            A list of values ``w_i`` weighing each coordinate, (x_i, y_i)
    """
    time_spent = data.groupby([x, y]).size()

    # Convert multilevel indexes into columns
    time_spent_df = pd.DataFrame(time_spent)
    time_spent_df.reset_index(inplace=True)

    # Convert coordinate columns and neuron columns into list of 3-tuples
    x_y_count = list(zip(time_spent_df[x], time_spent_df[y], time_spent_df[0]))

    # Convert list of 3-tuples into dict of (x, y): count
    time_at_coords = {(x, y): count for x, y, count in x_y_count}

    neuron = data[neuron].tolist()

    # Convert coordinate columns into list of 2-tuples
    coords_list = list(zip(data[x], data[y]))

    weights = []

    # Go through each component of the neuron column vector, and
    # if the component is not 0, then for the corresponding coordinate-pair,
    # we set the weight to: (flourescence * framerate) divided by the time spent at
    # that location (coordinate-pair).
    for i, coord in enumerate(coords_list):
        if neuron[i] != 0:
            weight = (framerate * neuron[i]) / time_at_coords[coord]
            
            #normalize by the maximum rate 
            weight = weight/max_rate
        else:
            weight = 0

        weights.append(weight)

    return weights

def generate_heatmap(x, y, sigma=2, **kwargs):
    """Generates a heatmap for plotting.

    Wrapper function meant for generating heatmap using the gaussian_filter
    function implemented in scipy, as well as NumPy's histogram2d function.

    Sources:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter.html

    Args:
        x: array_like, shape (N,)
            An array containing the x coordinates of the points to be
            histogrammed.

        y: array_like, shape (N,)
            An array containing the y coordinates of the points to be
            histogrammed.

        bins: int or array_like or [int, int], optional, default: (50, 50)

        sigma: scalar, optional, default: 2
            Standard deviation for Gaussian kernel.

        weights : array_like, shape(N,), optional, default: None
            An array of values ``w_i`` weighing each sample ``(x_i, y_i)``.
            Weights are normalized to 1 if `normed` is True. If `normed` is
            False, the values of the returned histogram are equal to the sum of
            the weights belonging to the samples falling into each bin.

    Returns:
        heatmap: ndarray
            Returned array of same shape as input. We return the transpose of
            the array in order to preserve the view.

        extent: scalars (left, right, bottom, top)
            The bounding box in data coordinates that the image will fill. The
            image is stretched individually along x and y to fill the box.
            Source: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.imshow.html
    """
    if len(x) != len(y):
        raise ValueError("x and y are not of equal length!")

    bins = kwargs.get("bins", (50, 50))
    weights = kwargs.get("weights", None)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins, weights=weights)
    heatmap = gaussian_filter(heatmap, sigma=sigma)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

def plot_heatmap(x, y, sigma=2, **kwargs):
    """Plots a heatmap.

    Wrapper function for matplotlib and generate_heatmap that plots the actual
    generated heatmap.

    Args:
        x: array_like, shape (N,)
            An array containing the x coordinates of the points to be
            histogrammed.

        y: array_like, shape (N,)
            An array containing the y coordinates of the points to be
            histogrammed.

        bins: int or array_like or [int, int], optional, default: (50, 50)

        sigma: scalar, optional; default: 2
            Standard deviation for Gaussian kernel.

        weights: array_like, shape(N,), optional, default: None
            An array of values ``w_i`` weighing each sample ``(x_i, y_i)``.
            Weights are normalized to 1 if `normed` is True. If `normed` is
            False, the values of the returned histogram are equal to the sum of
            the weights belonging to the samples falling into each bin.

        bounds: tuple, optional, default: None
            If a boundary tuple is provided, the x-axis will be set as follows:
            [bounds[0], bounds[1]]. Similarly, the y-axis will be set as:
            [bounds[0], bounds[1]].

        cmap: matplotlib.colors.LinearSegmentedColormap, optional, default: plt.cm.jet
            The colormap to use for plotting the heatmap.

        figsize: tuple, optional, default: (10, 10)
            The size of the heatmap plot.

        title: str, optional, default: 'Title Goes Here'
            The title of the heatmap plot.
            Note: If title is provided, title will be used as the name of
            the file when the figure is saved.

        dpi: int, optional, default: 600
            The amount of dots per inch to use when saving the figure. In
            accordance with Nature's guidelines, the default is 600.
            Source: https://www.nature.com/nature/for-authors/final-submission

        savefig: bool, optional, default: False
            When True, the plotted heatmap will be saved to the current working
            directory in pdf (IAW Nature's guidelines) format.
            Source: https://www.nature.com/nature/for-authors/final-submission
    """
    if len(x) != len(y):
        raise ValueError("x and y are not of equal length!")

    cmap = kwargs.get("cmap", cm.jet)
    title = kwargs.get("title", None)
    filename = kwargs.get("filename",None)
    filepath = kwargs.get("filepath",None)
    bins = kwargs.get("bins", (50, 50))
    weights = kwargs.get("weights", None)
    figsize = kwargs.get("figsize", (10, 10))
    bounds = kwargs.get("bounds", None)
    x_bounds = kwargs.get("x_bounds", None)
    y_bounds = kwargs.get("y_bounds", None)
    vmin = kwargs.get("vmin",None)
    vmax = kwargs.get("vmax",None)
    ax = kwargs.get('ax',None)
    show_colorbar = kwargs.get('show_colorbar',True)
    # Set user-defined x-axis and y-axis boundaries by appending them to x and y
    if bounds:
        x = x.copy()
        y = y.copy()
        x.loc[len(x)] = bounds[0]
        x.loc[len(x)] = bounds[1]
        y.loc[len(y)] = bounds[0]
        y.loc[len(y)] = bounds[1]
        if not weights is None:
            weights = weights.copy()
            weights.loc[len(weights)] = 0
            weights.loc[len(weights)] = 0
    if x_bounds and y_bounds:
        x = x.copy()
        y = y.copy()
        x.loc[len(x)] = x_bounds[0]
        x.loc[len(x)] = x_bounds[1]
        y.loc[len(y)] = y_bounds[0]
        y.loc[len(y)] = y_bounds[1]
        if not weights is None:
            weights = weights.copy()
            weights.loc[len(weights)] = 0
            weights.loc[len(weights)] = 0


    if ax is None:
        fig,ax = plt.subplots(figsize=figsize)
    heatmap, extent = generate_heatmap(x, y, sigma, bins=bins, weights=weights)
    image = ax.imshow(heatmap, origin="lower", extent=extent, cmap=cmap,vmin=vmin, vmax=vmax)
    if show_colorbar:
        plt.colorbar(image,fraction=.03)
    
    if title:
        plt.title(title)

    dpi = kwargs.get("dpi", 600)
    savefig = kwargs.get("savefig", False)
    if savefig:
        if filename:
            filename = filename
        elif title:
            filename = title
        else:
            filename = "my_smoothed_heatmap"

        plt.savefig("{}{}".format(filepath,filename), dpi=dpi)

##### End of spatial plotting functions #####

def show_traces(mouse, neuron_list, time_period, **kwargs):
    """
    Inputs:
        mouse: mouse object with dataframes for raw, s, and c
        neuron_list: list of neurons to show
        time_period: tuple of ints representing the first and last time bin to show
    """
    m = mouse.name
    b = mouse.session
    fr = mouse.FR
    
    if len(neuron_list) == 0:
        num_plots = len(mouse.spikes.columns)
    else:
        num_plots = len(neuron_list)
        
    figsize = kwargs.get('figsize', (4,3))
    which_traces = kwargs.get('which_traces', ['F','C','S'])
    savefig = kwargs.get('savefig', False)
    filename = kwargs.get('filename', None)
    filepath = kwargs.get('filepath', None)
    dpi = kwargs.get('dpi', 300)
    lw = kwargs.get('linewidth',1)
    fontsize = kwargs.get('fontsize', 6)
    
    colors = kwargs.get('colors',['grey','b','r'])
    
    #if only 1 or 2 colors are given, add the remaining default colors
    n_colors = len(colors)
    if n_colors < 3:
        missing_colors = 3-n_colors
        default_color = ['grey','b','r']
        for i in range(missing_colors):
            colors.append(default_color[i+n_colors])
    
    fig, ax = plt.subplots(num_plots, 1, figsize=figsize)
    title = kwargs.get('title',m+'_'+b)
    

    S = mouse.spikes  # Inferred spikes
    C = mouse.cell_transients  # Denoised fluorescence
    F = mouse.raw  # Raw fluorescence

    if not neuron_list:
        neuron_list = S.columns

    if not time_period:
        #time_period = (0,len(S))
        time_period = (0,S.index[-1])
    t = list(range(time_period[0], time_period[1]))
    x = [j/fr for j in t] #Show seconds, not frames, on the x axis
    
    ylim = kwargs.get('ylim',None)
    for i,n in enumerate(neuron_list):
        
        #Plot in reverse order
        j = (len(neuron_list) - 1) - i
        
        if 'F' in which_traces:
            _=ax[j].plot(x,F.loc[t,n], colors[0],linewidth=lw)
        if 'C' in which_traces:
            _=ax[j].plot(x,C.loc[t,n], colors[1],linewidth=lw)
        if 'S' in which_traces:
            _=ax[j].plot(x,S.loc[t,n], colors[2], linewidth=lw)
        
        ax[j].set_frame_on(False)
        if i!=0:
            ax[j].set_xticks([])
        ax[j].set_yticks([])
        ax[j].set_ylabel(n, rotation=0,fontsize=fontsize)
        
        if ylim:
            ax[j].set_ylim(ylim)
        
    plt.subplots_adjust(wspace=0.0, hspace=0.0)
        

    ax[0].set_title(title, fontsize=fontsize+2, fontweight='bold',fontname='Arial')
    ax[-1].set_xlabel('Time (s)', fontsize = fontsize, fontweight = 'bold', fontname = 'Arial')
    plt.xticks(fontsize = fontsize, fontname = 'Arial')
    
    if savefig:
        plt.tight_layout()
        plt.savefig(os.path.join(filepath, filename), dpi=dpi)
        

def abline(slope, intercept, ax=None, **kwargs):

    """
    Plot a line from slope and intercept
    Inputs:
        slope: float
        intercept: float
    """
    if ax is None:
        fig,ax=plt.subplots()
    x_vals = np.array(ax.get_xlim())
    y_vals = intercept + slope * x_vals
    ax.plot(x_vals, y_vals, **kwargs)
    return ax

    
def pie_chart(sizes, *labels, **kwargs):
    """Wrapper method for matplotlib's pie chart.

    The slices will be ordered and plotted counter-clockwise.

    Args:
        sizes: list
            A list of the sizes of each category.

        labels: str, variable number of args
            The label for each corresponding slice size.

        figsize: tuple, optional, default: (5, 5)
            The size of the figure to be plotted.
    """
    if len(labels) != len(sizes):
        raise ValueError("Length of sizes and amount of labels must be equal.")

    figsize = kwargs.get("figsize", (5, 5))

    _, ax1 = plt.subplots(figsize=figsize)
    ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax1.axis("equal")
    plt.show()

def plot_corr_heatmap(dataframe, **kwargs):
    """Seaborn correlation heatmap wrapper function

    A wrapper function for seaborn to quickly plot a
    correlation heatmap with a lower triangle, only.

    Args:
        dataframe: DataFrame
            A Pandas dataframe to be plotted in the correlation heatmap.

        figsize: tuple, optional, default: (16, 16)
            The size of the heatmap to be plotted.

        title: str, optional, default: None
            The title of the heatmap plot.
            Note: If title is provided, title will be used as the name of
            the file when the figure is saved.

        dpi: int, optional, default: 600
            The amount of dots per inch to use when saving the figure. In
            accordance with Nature's guidelines, the default is 600.
            Source: https://www.nature.com/nature/for-authors/final-submission

        savefig: bool, optional, default: False
            When True, the plotted heatmap will be saved to the current working
            directory in pdf (IAW Nature's guidelines) format.
            Source: https://www.nature.com/nature/for-authors/final-submission
    """
    title = kwargs.get("title", None)

    # Generate a mask for the upper triangle
    mask = np.zeros_like(dataframe.corr(), dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True

    # Set up the matplotlib figure
    _, _ = plt.subplots(figsize=kwargs.get("figsize", (16, 16)))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(dataframe.corr(), mask=mask, cmap=cmap, vmax=1.0, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    if title:
        plt.title(title)

    dpi = kwargs.get("dpi", 600)
    savefig = kwargs.get("savefig", False)
    if savefig:
        if title:
            filename = title
        else:
            filename = "my_seaborn_heatmap"

        plt.savefig("{}.pdf".format(filename), dpi=dpi)

def plot_clustermap(dataframe, **kwargs):
    """Seaborn clustermap wrapper function

    A wrapper function for seaborn to quickly plot a clustermap using the
    "centroid" method to find clusters.

    Args:
        dataframe: DataFrame
            The Pandas dataframe to be plotted in the clustermap.

        figsize: tuple, optional, default: (15, 15)
            The size of the clustermap to be plotted.

        dendrograms: bool, optional, default: True
            If set to False, the dendrograms (row & col) will NOT be plotted.

        cmap: str, optional, default: "vlag"
            The colormap to use for plotting the clustermap.

        title: str, optional, default: None
            The title of the heatmap plot.
            Note: If title is provided, title will be used as the name of
            the file when the figure is saved.

        dpi: int, optional, default: 600
            The amount of dots per inch to use when saving the figure. In
            accordance with Nature's guidelines, the default is 600.
            Source: https://www.nature.com/nature/for-authors/final-submission

        savefig: bool, optional, default: False
            When True, the plotted heatmap will be saved to the current working
            directory in pdf (IAW Nature's guidelines) format.
            Source: https://www.nature.com/nature/for-authors/final-submission
    """
    cmap = kwargs.get("cmap", "vlag")
    figsize = kwargs.get("figsize", (15, 15))
    title = kwargs.get("title", None)
    dendrograms = kwargs.get("dendrograms", True)

    cluster_map = sns.clustermap(dataframe.corr(), center=0, linewidths=.75, figsize=figsize, method="centroid", cmap=cmap)

    # Set the dendrograms in accordance with passed-in args
    cluster_map.ax_row_dendrogram.set_visible(dendrograms)
    cluster_map.ax_col_dendrogram.set_visible(dendrograms)

    if title:
        cluster_map.fig.suptitle(title)

    dpi = kwargs.get("dpi", 600)
    savefig = kwargs.get("savefig", False)
    if savefig:
        if title:
            filename = title
        else:
            filename = "my_seaborn_clustermap"

        plt.savefig("{}.pdf".format(filename), dpi=dpi)

def plot_contours(A, Cn, thr=None, thr_method='max', maxthr=0.2, nrgthr=0.9,
                  display_numbers=True, max_number=None,
                  cmap=None, swap_dim=False, colors='w', vmin=None,
                  vmax=None, neuron_list = None, show_bg = False, **kwargs):
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
    cm = au.com(A, d1, d2)
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
                    newpt = np.round(au.old_div(vtx[-1, :], [d2, d1])) * [d2, d1]
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
            
            x = cm[i,1]
            if show_bg: 
                y = cm[i,0]
            else:
                y = d1-cm[i,0] #need to flip to preserve location if theres no background
                
            if swap_dim:
                ax.text(y, x, str(i + 1), color=colors)
            else:
                ax.text(x, y, str(i + 1), color=fontcolor, fontsize = fontsize, fontname = fontname, fontweight = fontweight) 

    return coordinates

def raster_plot(mouse, neurons=[], binsize=2, behaviors=[], colors=[], ax=None):
    """
    Plots summary of neural data as a raster, and as a histogram showing a sum
    of the total activity per time bin
    
    Inputs:
        
        mouse: Mouse object
        neurons: list of ints (optional)
            List of the neurons to plot. Default is to show all neurons
        binsize: int
            Length of each time bin, in seconds. Applies to lower plot only.
        behaviors: list of str (optional)
            Names of behavior columns in mouse.behavior to display.
        colors: list
            Colors of behaviors
            
    Returns:
        ax: matplotlib.axes object
    """
    
    if ax is None:
        fig,ax = plt.subplots(2,1,figsize=(2.5,3))

    current_FR = mouse.FR #in frames per second
    framelength = 1/current_FR
    str_fr = str(int(1000/current_FR))+'ms' 
    bin_fr = str(binsize)+'s'

    s=mouse.spikes
    
    if len(neurons)==0:
        neurons = s.columns
    
    xax = [framelength*i for i in s.index]
    events=[]    
    for i,col in enumerate(neurons):
        n = s[col]
        times = n[n>0].index.tolist()

        #convert times from frame number to time
        times = [t*framelength for t in times]

        events.append(times)
    ax[0].eventplot(events, color='k',linelengths=.5, linewidths=.5)

    s = au.resample_ts(s[neurons], current_FR = str_fr, new_FR=bin_fr,method='sum')
    spikes_sum = s.mean(axis=1)

    xax_bin = [binsize*i for i in spikes_sum.index]
        
    ax[1].bar(xax_bin, spikes_sum.values, width=binsize, color='k',linewidth=1,edgecolor='k')

    if len(mouse.behavior)>0:
        for index, b in enumerate(behaviors):
            try:
                evt=au.extract_epochs(mouse,b)
                interval = au.filter_epochs(evt[1],framerate=mouse.FR, seconds=.2)
                alpha=.5

                color = colors[index]

                for i in interval:
                    # convert i from frame number to seconds
                    j = [t*framelength for t in i]
                    ax[0].axvspan(j[0], j[-1], alpha=alpha, color=color,linewidth=0)
                    ax[1].axvspan(j[0], j[-1], alpha=alpha, color=color,linewidth=0)
            except:
                continue
    ax[1].set_xticks(ax[1].get_xticks(),ax[0].get_xticklabels())
    ax[0].set_xlim(0,np.max(xax))
    ax[1].set_xlim(0,np.max(xax))
    #ax[1].set_ylim(0,.3)
    ax[0].set_xticks([])
    ax[0].set_title(mouse.name)
    ax[0].set_ylabel('Cell Number')
    ax[1].set_ylabel('Activity')
    ax[1].set_xlabel('Time (s)')
    ax[0].axes.spines['bottom'].set_visible(False)
    plt.subplots_adjust(wspace=0, hspace=0)
    return ax

def cum_dist_plot(var=None, hue=None, data=None, ax=None, **kwargs):
    if ax is None:
        figsize = kwargs.get('figsize',(2,2))
        fig,ax = plt.subplots(figsize=figsize)

    hue_vals = kwargs.get('order',list(set(data[hue])))

    colors = kwargs.get('colors',None)
    cmap = kwargs.get('cmap','Reds')
    colors = kwargs.get('colors',None)
    lw = kwargs.get('linewidth',1)
    
    colormap=None
    if colors is None:     
        colormap = get_cmap(len(hue_vals),cmap)
    
    #find max and min values and draw horizontal line for each hue to extend
    max_val = np.max([data[data[hue]==h][var].max() for i,h in enumerate(hue_vals)])
    min_val = np.min([data[data[hue]==h][var].min() for i,h in enumerate(hue_vals)])
    
    for i,h in enumerate(hue_vals):
        a=np.sort(data[data[hue]==h][var])
        label=kwargs.get('label',h)
        if colormap:
            c=colormap(i)
        else:
            c=colors[i]   
        ax.step(a,np.arange(len(a))/len(a),color=c, label=label,linewidth=lw)
        
        #draw lines to ensure all hues extend to the same x coordinate
        
        
        ax.hlines(y=1, xmin=np.max(a), xmax=max_val, color=c, linewidth=lw)
        ax.hlines(y=0, xmin=min_val, xmax=np.min(a), color=c, linewidth=lw)
        
        #draw vertical line to ensure data lines go to y=1
        
        y_max_data = 1-1/len(a)
        ax.vlines(x=np.max(a), ymin=y_max_data, ymax=1, color=c, linewidth=lw)
    title= kwargs.get('title',None)
    if title:
        ax.set_title(title)
    ax.set_xlabel(var)
    ax.set_ylabel('Cumulative \nProportion')
    return ax

def get_cmap(n, name="tab20"):
    """ Returns a function that maps each index in 0,1,...,n-1 
        to a distinct RGB color; the keyword argument name must 
        be a standard mpl colormap name.
    """
    return plt.cm.get_cmap(name, n)

def plot_positions_dlc(rois, tracking=None,xlim=[5,85], ylim=[-5,65], style='line',**kwargs):
    from matplotlib.patches import Polygon
    #from matplotlib.collections import PatchCollection
    
    bins = kwargs.get('bins',(50,50))
    sigma = kwargs.get('sigma',2)
    cmap=kwargs.get('cmap','Greys')
    autofit = kwargs.get('autofit',True)
    which_rois = kwargs.get('which_rois',None)
    roi_colors = kwargs.get('roi_colors',['k','b','r'])
    title = kwargs.get('title',None)
    roi_linewidth = kwargs.get('linewidth',7)
    pos_linewidth = kwargs.get('pos_lw',1)
    ax=kwargs.get('ax',None)
    
    if ax is None:
        fig,ax = plt.subplots(figsize=(10,10))
    patches=[]

    for i,r in enumerate(rois):
        if which_rois:
            if i not in which_rois:
                continue;
        patches.append(Polygon(r[1], edgecolor = roi_colors[i], linewidth=roi_linewidth, fill=False))
                
    for p in patches:
        ax.add_patch(p)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim[1],ylim[0]) #flip y axis
    ax.set_xticks([])
    ax.set_yticks([])
    spines = ['top','bottom','left','right']
    for s in spines:
        ax.spines[s].set_visible(False)
    ax.set_aspect('equal')
    ax.set_title(title)
    if tracking is not None:      
        if style=='line':
            ax.plot(tracking['x'], tracking['y'], color = 'grey', alpha=.5,linewidth=pos_linewidth)
            
        elif style=='heatmap':
            import analysis.visualize as vis
            show_colorbar = kwargs.get('show_colorbar',False)
            weights = pd.Series(np.tile(1,len(tracking)))
            if autofit:
                arena_x = list(zip(*rois[0][1]))[0]
                arena_y = list(zip(*rois[0][1]))[1]
                x_bounds = (np.min(arena_x), np.max(arena_x))
                y_bounds = (np.min(arena_y), np.max(arena_y))
                vis.plot_heatmap(tracking['x'], tracking['y'], sigma=sigma, bins=bins, ax=ax, show_colorbar=show_colorbar,
                             x_bounds=x_bounds, y_bounds=y_bounds, cmap=cmap,vmin=.01,norm=True,weights=weights)         
            else:
                vis.plot_heatmap(tracking['x'], tracking['y'], sigma=sigma, bins=bins, ax=ax, show_colorbar=show_colorbar,
                            cmap=cmap,vmin=.01,norm=True,weights=weights)
        else:
            print('Only plot styles of "line" or "heatmap" are supported')
    
    return ax

# Plots for Single Neuron Properties (e.g. selectivity)

def selectivity_stacked_bar(selectivity_counts_df, colors):
    ind = np.arange(selectivity_counts_df.shape[1])
    width = 0.75
    
    darker = [adjust_lightness(color, amount=0.8) for color in colors]
    lighter = [adjust_lightness(color, amount=1.5) for color in darker]
    
    act = selectivity_counts_df.loc['activated',:]
    inhib = selectivity_counts_df.loc['inhibited',:]
    ns = selectivity_counts_df.loc['non_selective',:]
    
    fig, ax = plt.subplots()
    ax.bar(ind, act, width, color=darker)
    ax.bar(ind, inhib, width, bottom=act, color=lighter)
    ax.bar(ind, ns, width, bottom=act+inhib, color='lightgray')
    for i in range(len(act)):
        ax.text(ind[i], act[i]/2, str(int(np.round(act[i]*100)))+'%\nact.', fontsize=3, ha='center', va='center', color='black')
        ax.text(ind[i], inhib[i]/2 + act[i], str(int(np.round(inhib[i]*100)))+'%\ninh.', fontsize=3, ha='center', va='center', color='black')
        ax.text(ind[i], ns[i]/2 + act[i] + inhib[i], str(int(np.round(ns[i]*100)))+'%\nns', fontsize=3, ha='center', va='center', color='black')
    ax.set_xticks(ind)
    ax.set_xticklabels(selectivity_counts_df.columns, rotation=25)
    #ax.axes.get_yaxis().set_visible(False)
    ax.set_title('Selective Neuron Proportions')
    return ax

def SelectivityOverlapHeatmap(p_value_df, odds_ratio_df, p_cutoff=0.05, save=False, save_path=None):
    
    log_df = -np.log(p_value_df) # Generate a -log(p-value) DataFrame from the p-value DataFrame
    
    # Set up a MultiIndex IndexSlice object and define the categories for cell-selectivity
    idx = pd.IndexSlice
    selectivity = ['activated', 'inhibited', 'non_selective']
    
    # Generate a heatmap for each pair of cell-selectivity categories and highlight the cells which have a p-value
    # that is smaller than the defined p-cutoff, pairs which are overlapping are highlighted lightcoral and pairs
    # that are distinct are highlighted cornflowerblue
    for pair in list(combinations_with_replacement(selectivity, 2)):
        
        # Subset the -log(p-value) Dataframe
        log_subset = log_df.loc[idx[:,pair[0]], idx[:,pair[1]]]
        log_subset.index = log_subset.index.droplevel(1)
        log_subset.columns = log_subset.columns.droplevel(1)
        
        # Generate an upper-triangular mask to hide the upper portion of the heatmap
        mask = np.ones_like(log_subset, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = False
        
        # Plot the -log(p-value) subset as a heatmap
        ax = sns.heatmap(data=log_subset * mask, square=True, cmap='Greys', cbar_kws={'shrink':0.5, 
                                                                                      'label':'-log(p value)'})

        # Get the integer indices for the entries which have a -log(p-value) that is greater than the -log(p-cutoff)
        x, y = np.where(log_subset >= -np.log(p_cutoff))
        coord = [(i,j) for i,j in zip(x,y) if i < j]
        
        # Subset the odds ratio DataFrame
        odds_subset = odds_ratio_df.loc[idx[:,pair[0]], idx[:,pair[1]]]
        odds_subset.index = odds_subset.index.droplevel(1)
        odds_subset.columns = odds_subset.columns.droplevel(1)
        
        # Highlight the cells which correspond to cell-selectivity pairs that have p-values below the p-cutoff
        for co in coord:
            if odds_subset.iloc[co] >= 1:
                ax.add_patch(Rectangle(co, 1, 1, fill=False, edgecolor='lightcoral', lw=1))
            elif odds_subset.iloc[co] < 1:
                ax.add_patch(Rectangle(co, 1, 1, fill=False, edgecolor='cornflowerblue', lw=1))
                
        plt.xlabel(pair[1])
        plt.ylabel(pair[0])
        plt.title('Cell Selectivity Overlap')
        
        if save == True:
            plt.savefig(save_path + f'{pair[0]}_{pair[1]}_overlap_heatmap.png')
            
        plt.show()

        # Helper Functions

def adjust_lightness(color, amount=0.5):
    """
    Changes the lightness of the given color by multiplying by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple. Colors get
    lighter with amount > 1 and darker with amount < 1.
    
    Source: 
    https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib

    Examples:
    >> adjust_lightness('g', 0.3)
    >> adjust_lightness('#F034A3', 0.6)
    >> adjust_lightness((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])