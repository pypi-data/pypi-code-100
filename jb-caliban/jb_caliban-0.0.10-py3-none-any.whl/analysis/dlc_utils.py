"""
This module contains helper functions to manipulate videos 

@authors: Gergo Turi gt2253@cumc.columbia.edu
"""
import os
import copy
import numpy as np
import pandas as pd
import statsmodels.api as sm

import cv2
import analysis.analysis_utils as au
import analysis.roi_tools as rt
import analysis.visualize as vis


def mount_gdrive():
    """
    mounts Google Drive in a Google Colab notebook
    """
    from google.colab import drive
    drive.mount('/content/drive')


def get_fps(vid_path):
    """
    retrieves acqusition rate from AVI video.

    Parameters:
    ===========
    vid_path: str
        path to the video

    Returns:
    ========
    fps: float
    """
    
    video = cv2.VideoCapture(vid_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    print(f'fps is {fps}')
    return fps

def load_tracking(tracking_path):
    """
    loads tracking from h5 file

    Parameters:
    ===========
    tracking_path: str
        path to the h5 file

    Returns:
    ========
    pandas dataframe
    """

    t = pd.read_hdf(tracking_path)
    if len(t.columns.names)==3:
        t.columns = t.columns.droplevel(0)
        
    return t

def in_zone_oft(x, y, rois):
    """
    determines which zone the point is in
    in the open field

    Parameters:
    ===========
    x: T x 1 numpy array or pandas series
        containing x positions at all time points
    y: T x 1 numpy array or pandas series
        containing y positions at all time points
    rois: list of tuples
        the coordinates defining the ROIs

    Returns:
    ========
    points_bool: list of tuples
        list of (name, boolean vector) tuples defining whether the point
        is in the ROI for each time point
    """

    bools = rt.in_zone(x, y, rois)    
    b = pd.DataFrame()

    for boo in bools:
        b[boo[0]] = boo[1]
   
    return b

def transform_rois(rois, px_per_cm):
    """
    transforms rois pixel to cm

    Parameters:
    ===========
    rois: list of tuples
        the coordinates defining the ROIs

    Returns:
    ========
    new_rois: list
    """
    new_rois = copy.deepcopy(rois)
    
    for roi in new_rois:
        for i,coord in enumerate(roi[1]):
            roi[1][i] = [c/px_per_cm for c in coord]
    return new_rois

def transform_tracking(dlc_tracking, px_per_cm):
    """
    transforms tracking data to cm

    Parameters:
    ===========
    dlc_tracking: pandas dataframe
        contains the tracing info
    px_per_cm: 

    Returns:
    ========
    new_tracking: pandas dataframe
    """

    body_parts = list(set(dlc_tracking.columns.get_level_values(0)))
    
    new_tracking = copy.deepcopy(dlc_tracking)
    
    for part in body_parts:
        new_tracking.loc[:,(part,'x')] = dlc_tracking.loc[:,(part,'x')] / px_per_cm
        new_tracking.loc[:,(part,'y')] = dlc_tracking.loc[:,(part,'y')] / px_per_cm
    return new_tracking

def oft_pixel_to_cm(rois, dlc_tracking,
    floor_length):
    """
    pixel to cm conversion defined by floor length

    Parameters:
    ===========
    rois: list of tuples
        the coordinates defining the ROIs
    dlc_tracking: pandas dataframe
        contains the tracking info
    floor_length: int
        the lenght of the arena in cm

    Returns:
    ========
    rois_cm : 
    tracking_cm : pandas dataframe

    """    
    
    floor_xcoords = list(zip(*rois[1][1]))[0]
    floor_len = np.max(floor_xcoords) - np.min(floor_xcoords)

    px_per_cm = floor_len / floor_length
    
    rois_cm = transform_rois(rois, px_per_cm)
    tracking_cm = transform_tracking(dlc_tracking, px_per_cm)
    
    return rois_cm, tracking_cm

def get_corner_coords(corner_point, corner_width, point_id):
    """
    defines corner coordinates of the arena

    Parameters:
    ===========
    corner_point: 
    params : dict
        dict of paramerters contain the arena info
        e.g. {'fr':12,
         'stretch_threshold':1.2,
          'arena_width':30,
         'center_width':15,
          'corner_width':4,
         'rear_pad': 'na'}
    point_id

    Returns:
    ========
    corner_zone: 

    """    
    x,y = corner_point
    if point_id == 'corner_ul':
        corner_zone = ([x, y],
                    [x+corner_width, y],
                    [x+corner_width, y+corner_width],
                    [x, y+corner_width])
    if point_id == 'corner_ur':
        corner_zone = ([x, y],
                    [x-corner_width, y],
                    [x-corner_width, y+corner_width],
                    [x, y+corner_width]) 
    if point_id == 'corner_ll':
        corner_zone = ([x, y],
                    [x+corner_width, y],
                    [x+corner_width, y-corner_width],
                    [x, y-corner_width])
    if point_id == 'corner_lr':
        corner_zone = ([x, y],
                    [x-corner_width, y],
                    [x-corner_width, y-corner_width],
                    [x, y-corner_width])
        
    return corner_zone

def add_center_quadrants(rois):
    """
    adds four center zones to opn field.

    Parameters:
    ===========
    rois : list
        coordinates of open field rois
    """

    center = rois[2][1]
    center_x = list(zip(*center))[0]
    center_y = list(zip(*center))[1]

    x_avg = np.mean(center_x)
    y_avg = np.mean(center_y)

    #for each point in center, make the corresponding quadrant roi
    for x,y in center:

        #ul
        if x<x_avg and y<y_avg:
            center_ul = ([x,y],
                        [x_avg,y],
                        [x_avg,y_avg],
                        [x,y_avg])

        #ur
        if x>x_avg and y<y_avg:
            center_ur = ([x_avg,y],
                        [x,y],
                        [x,y_avg],
                        [x_avg,y_avg])
        #ll
        if x>x_avg and y>y_avg:
            center_ll = ([x,y],
                        [x_avg,y],
                        [x_avg,y_avg],
                        [x,y_avg])

        #lr
        if x<x_avg and y>y_avg:
            center_lr = ([x,y],
                        [x,y_avg],
                        [x_avg,y_avg],
                        [x_avg,y])

    rois.append(('center_ul',center_ul))
    rois.append(('center_ur',center_ur))
    rois.append(('center_ll',center_ll))
    rois.append(('center_lr',center_lr))

    return rois

def add_center_perim_corners(rois, params):
    """
    adds center perimeter and corner zones to the rois

    Parameters:
    ===========
    rois : list
        list of rois drawn on the arena
    params : dict
        paramater dict e.g. 
        {'fr':12,
         'stretch_threshold':1.2,
          'arena_width':30,
         'center_width':15,
          'corner_width':4,
         'rear_pad': 'na'}
    """
    center_width = params['center_width']
    corner_width = params['corner_width']

    floor_coords = rois[1][1]
    floor_xcoords = list(zip(*floor_coords))[0]
    floor_ycoords = list(zip(*floor_coords))[1] 

    x_avg = np.mean(floor_xcoords)
    y_avg = np.mean(floor_ycoords)

    corner_points = {}

    for x,y in floor_coords:
        if x<x_avg and y<y_avg:
            corner_points['corner_ul'] = (x,y)
        if x>x_avg and y<y_avg:
            corner_points['corner_ur'] = (x,y)
        if x<x_avg and y>y_avg:
            corner_points['corner_ll'] = (x,y)
        if x>x_avg and y>y_avg:
            corner_points['corner_lr'] = (x,y)

    #center region is centered around 
    center_point = (np.mean(floor_xcoords), np.mean(floor_ycoords))
    center = ([center_point[0]-center_width/2, center_point[1]-center_width/2],
             [center_point[0]+center_width/2, center_point[1]-center_width/2],
             [center_point[0]+center_width/2, center_point[1]+center_width/2],
             [center_point[0]-center_width/2, center_point[1]+center_width/2])


    rois.append(('Center',center))
    add_center_quadrants(rois)

    for k,p in corner_points.items():
        corner_zone = get_corner_coords(p, corner_width,k)
        rois.append((k,corner_zone))

    return rois

def FitSARIMAXModel(x, p, pcutoff, alpha, ARdegree, MAdegree,
    nforecast=0, disp=False):
    """
    Seasonal Autoregressive Integrated Moving-Average with
    eXogenous regressors (SARIMAX)
    see http://www.statsmodels.org/stable/statespace.html#seasonal-autoregressive-integrated-moving-average-with-exogenous-regressors-sarimax
    """
    Y = x.copy()
    Y[p < pcutoff] = np.nan  # Set uncertain estimates to nan (modeled as missing data)
    if np.sum(np.isfinite(Y)) > 10:

        # SARIMAX implemetnation has better prediction models
        # than simple ARIMAX (however we do not use the seasonal etc.
        # parameters!)
        mod = sm.tsa.statespace.SARIMAX(
            Y.flatten(),
            order=(ARdegree, 0, MAdegree),
            seasonal_order=(0, 0, 0, 0),
            simple_differencing=True,
        )
        # Autoregressive Moving Average ARMA(p,q) Model
        # mod = sm.tsa.ARIMA(Y, order=(ARdegree,0,MAdegree)) #order=(ARdegree,0,MAdegree)
        try:
            res = mod.fit(disp=disp)
        except ValueError:  # https://groups.google.com/forum/#!topic/pystatsmodels/S_Fo53F25Rk (let's update to statsmodels 0.10.0 soon...)
            startvalues = np.array([convertparms2start(pn) for pn in mod.param_names])
            res = mod.fit(start_params=startvalues, disp=disp)
        except np.linalg.LinAlgError:
            # The process is not stationary, but the default
            # SARIMAX model tries to solve for such a distribution...
            # Relaxing those constraints should do the job.
            mod = sm.tsa.statespace.SARIMAX(
                Y.flatten(),
                order=(ARdegree, 0, MAdegree),
                seasonal_order=(0, 0, 0, 0),
                simple_differencing=True,
                enforce_stationarity=False,
                enforce_invertibility=False,
                use_exact_diffuse=False,
            )
            res = mod.fit(disp=disp)

        predict = res.get_prediction(end=mod.nobs + nforecast - 1)
        return predict.predicted_mean, predict.conf_int(alpha=alpha)
    else:
        return np.nan * np.zeros(len(Y)), np.nan * np.zeros((len(Y), 2))

def arima_filter(df,  windowlength=5, p_bound=0.8, ARdegree=3,
    MAdegree=1, alpha=0.1):

    nrows = df.shape[0]
    temp = df.values.reshape((nrows, -1, 3))
    placeholder = np.empty_like(temp)
    for i in range(temp.shape[1]):
        x, y, p = temp[:, i].T
        meanx, _ = FitSARIMAXModel(
            x, p, p_bound, alpha, ARdegree, MAdegree, False
        )
        meany, _ = FitSARIMAXModel(
            y, p, p_bound, alpha, ARdegree, MAdegree, False
        )
        meanx[0] = x[0]
        meany[0] = y[0]
        placeholder[:, i] = np.c_[meanx, meany, p]
    data = pd.DataFrame(
        placeholder.reshape((nrows, -1)),
        columns=df.columns,
        index=df.index,
    )
    return data

def dump_df_to_csv(df, file_name, output_directory=None, **kwargs):
    """
    Saves a pandas dataframe to a comma separated  csv.
    For more kwargs see pandas.DataFrame.to_csv

    Parameters:
    ===========
    df : pandas dataframe
    file_name: str
        name of the file
    output_directory: str, path-like
        the destination the file to be saved.

    output:
    ========
    .csv
    if not output_directory is given then the file will be saved
    in the current directory

    """
    if not file_name.endswith('csv'):
        file_name = file_name+'.csv'
    if output_directory is not None:
        output_file = os.path.join(output_directory, file_name)
    else:
        output_file = file_name
    
    df.to_csv(output_file)