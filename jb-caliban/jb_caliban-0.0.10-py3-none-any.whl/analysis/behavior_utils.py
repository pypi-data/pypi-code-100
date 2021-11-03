"""
Miscellaneous, or unfinished functions written by Jack Berry 
to be used for calcium imaging analysis
3/1/2019
"""
import numpy as np
import pandas as pd
import analysis.analysis_utils as au

##### Behavior Functions #######


def read_ethovision(etho_filepath, track_point):
    """
    Reads in data from an Ethovision raw data file (converted to .csv format). Expected format is a T x B matrix,
    where T is time bins, and B is the automatically tracked behaviors.
    
    Intended to to be used as a helper function for preprocess_behavior
    
    Args:
        etho_filepath: str
            The file path to the raw Ethovision .csv file
            
        track_point: str
            The tracking point to be used (options: 'center', 'nose', 'tail')
            
    Returns:
        behavior: pandas DataFrame
            The processed Ethovision data    
    """       
    
    # read ethovision data and rename columns
    nrowsheader = pd.read_csv(etho_filepath, nrows=0, encoding="latin1", header=0)
    nrowsheader = int(nrowsheader.columns[1])

    behavior = pd.read_csv(etho_filepath, header=nrowsheader-2, encoding="latin1", low_memory=False)
    behavior = behavior.drop(behavior.index[0])
    behavior = behavior.apply(pd.to_numeric, errors='coerce')

    # remove columns that track other body points (ie. if track_point = 'center', remove all nose and tail columns)
    all_points = set(['center', 'nose', 'tail'])
    unwanted_points = all_points - set([track_point])
    cols = [c for c in behavior.columns if not any(s in c for s in unwanted_points)]
    behavior = behavior[cols]       
    
    #each track_point has a different string in the column name that should be removed
    track_point_dict = {"center": "_/_center-point)", "nose": "_/_nose-point)", "tail": "_/_tail-base" }
    track_point_dict_etho14 = {"center": "(center-point)", "nose": "(nose-point)","tail": "(tail-base)"}
    # rename columns
    new_cols = []
    for col in behavior.columns:
        col = col.replace(' ', '_').replace("In_zone(", '').replace(track_point_dict[track_point], '')
        col = col.replace(track_point_dict_etho14[track_point], '')
        new_cols.append(col)
    behavior.columns = new_cols

    old_x = 'X_' + track_point
    old_y = 'Y_' + track_point
    #for now, keep _center so spatial info code will work
    behavior = behavior.rename(columns = {old_x : 'X_center', old_y : 'Y_center'})
    
    # convert Trial_time to timedelta function to enable time operations    
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')

    return behavior

def read_observer(observer_filepath):
    """
    Reads in data from an observer file (converted to .csv format). Expected format is a T x B matrix,
    where T is time bins, and B is the hand-scored behaviors.
    
    Intended to to be used as a helper function for preprocess_behavior
    
    Args:
        observer_filepath: str
            The file path to the raw observer .csv file
            
    Returns:
        behavior: pandas DataFrame
            The processed observer data
    
    """
    behavior = pd.read_csv(observer_filepath)
    behavior = behavior.drop(["Observation", "Event Log", "Time"], axis=1)
    behavior.index += 1
    behavior.fillna(0, inplace=True)
    behavior = behavior.apply(pd.to_numeric, errors='coerce')
    behavior[behavior != 0] = 1
    
    return behavior

def make_freq_string(fr):
    # converts the framerate to a frequency in ms
    freq = np.round(1 / fr * 1000, 3)
    freq_string = str(freq) + 'ms'
    
    return freq_string

def read_boris(boris_filepath, freq_string):
    # read in from csv (BORIS or stopwatch) the start and stop times for various behaviors
    csv = pd.read_csv(boris_filepath, header = [15])
    rec_length = csv['Total length'][0]
    frames = csv['FPS'][0] * (rec_length)
    frames = frames.astype('int')
    
    # make a timedelta array that is as long as the recording time of the behavior video, use 30fps to generate the array
    # assumes frame rate of 30fps here
    time = pd.timedelta_range(0, periods=frames, freq=freq_string)
    #make dt column
    dt = pd.DataFrame(np.roll(time, -1) - time).shift(1)

    
    # make a dataframe with timedelta array as the index
    beh = pd.DataFrame(np.zeros(shape=(len(time),len(csv['Behavior'].unique())),dtype='int'))
    beh = beh.set_index(time)
    beh.index.names = ['Trial_time']
    beh.columns = csv['Behavior'].unique()
    
    # convert start stop times to timedelta
    pairs_raw = pd.to_timedelta(csv['Time'], unit = 's')
    
    # convert timedeltas from the csv to the closest timedelta in the full length timedelta array 
    for i in pairs_raw:
        pairs_raw[pairs_raw == i] = time[np.abs(time-i).argmin()]
        
    # make pairs_raw timedelta the index for the behavior and start-stop arrays
    data = csv[['Behavior', 'Unnamed: 8']]
    data.index = pairs_raw
    
    # generate pairs of indices to slice the full length timedelta array
    for b in data['Behavior'].unique():
        temp = data.query("Behavior == @b")
        pairs = list(zip(temp.index[::2], temp.index[1::2]))
        for pair in pairs:
            beh.loc[pair[0]:pair[1], b] = 1
        
    return beh

def preprocess_behavior(etho_filepath=None, observer_filepath=None, track_point='center'):
    """
    Processes original ethovision and observer files (converted to .csv format)
    Args:
        etho_filepath: str
            The file path to raw ethovision behavior .csv file.
        observer_filepath: str
            The file path to the raw observer .csv file.
    Returns:
        behavior: DataFrame
            The preprocessed behavior DataFrame.
    """

    if etho_filepath and observer_filepath:
        #Read in behavior files
        etho_behavior = read_ethovision(etho_filepath, track_point)
        obs_behavior = read_observer(observer_filepath)
        num_obs = len(obs_behavior.columns)
        
        #Merge Ethovision and Observer data
        behavior = pd.merge(etho_behavior, obs_behavior, how="left", left_index=True, right_index=True)
        behavior.update(behavior[behavior.columns[-num_obs:]].fillna(0))
        
        return behavior

    if etho_filepath:
        etho_behavior = read_ethovision(etho_filepath, track_point)
        return etho_behavior
        
    if observer_filepath:
        obs_behavior = read_observer(observer_filepath)
        return obs_behavior
    
    raise ValueError("You did not provide an ethovision or observer file path")


def process_EPM_behavior(behavior, analysis_frame_length = '100ms', hd_open=False):
    """
    Process behavior dataframe containing tracking information from an EPM experiment.
    Assumes there is not already a Center zone, and assumes the mouse is in the 
    center whenever it is not in closed or open arms. 
    
    Inputs:
        behavior: T x B Pandas DataFrame
            - raw Ethovision (with or without manual scoring from Observer)
            behavior tracking file for EPM.
        analysis_frame_length: str
            - desired frame length of the final behavior dataframe. eg. "100ms"
        hd_open: bool, optional
            - if True, all time bins during which the mouse is headdiping will
            be considered OpenArms. This fix can be used to correct times when
            the mouse is tracked to be in the center or closed arms, but is
            in actually investigating the open arms.
            - if False, normal tracking will be used
    Returns:
        behavior: T x B Pandas DataFrame
            - processed behavior dataframe that has been downsampled, interpolated
            and new columns added
    """

    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')
    behavior.set_index('Trial_time', inplace=True, drop=True)
    behavior = behavior.resample(analysis_frame_length).mean()
    #behavior = behavior.resample("100ms", on="Trial_time").mean()
    
    #After resampling, zone columns no longer contain only 0 and 1 (ie. when 
    #mouse transitioned between frames. To avoid ambiguity, round values to 0 or 1
    
    varlist = ['OpenArms', 'ClosedArms', 'Open1', 'Open2', 'Closed1', 'Closed2', 'Headdips']
    for var in varlist:
        if var in behavior.columns:
            behavior[var] = behavior[var].fillna(method='bfill')
            behavior[var] = behavior[var].where(behavior[var] < 0.5, 1)
            behavior[var] = behavior[var].where(behavior[var] >= 0.5, 0)
    
    #remove NaNs in X,Y due to point being outside of Arena (Ethovision doesn't interpolate in this situation) by interpolating  

    behavior.X_center = behavior.X_center.interpolate()
    behavior.Y_center = behavior.Y_center.interpolate()
    
    x=behavior.X_center.astype(float)
    y=behavior.Y_center.astype(float)
    behavior['Distance_moved'] = au.distance_moved(x,y)
    behavior['Velocity'] = au.compute_velocity(behavior.Distance_moved)    
    
    #Add column to identify immobile time bins (min_vel = 2, min_dur=1)

    behavior['immobile'] = au.define_immobility(behavior.Velocity)

    #Add Center and other columns to behavior df

    center = (behavior["OpenArms"] + behavior["ClosedArms"])
    center = 1-center
    behavior.loc[:,'Center'] = center
    behavior.loc[:,"Open_Center"] = behavior["OpenArms"] + behavior["Center"]
    
    if 'Headdips' in behavior.columns:
        #Add not Headdips, Center_Headdips, Open+Headdips
        behavior.loc[behavior['Headdips'] == 0, 'no_Headdips'] = 1
        behavior['no_Headdips'] = behavior['no_Headdips'].fillna(0).astype(int)
        behavior.loc[behavior['Headdips'] +  behavior['Center']==2,'Center_Headdips'] = 1
        behavior['Center_Headdips'] = behavior['Center_Headdips'].fillna(0)
        
        if hd_open:
            
            behavior.loc[behavior['Center_Headdips']==1,'Center'] = 0
            behavior.loc[behavior['Center_Headdips']==1,'OpenArms'] = 1
    
    
    behavior.reset_index(inplace = True)
    
    return behavior

def process_ABAB_behavior(behavior):
    """
    Process behavior dataframe containing tracking information from an EPM experiment.
    Assumes there is not already a Center zone, and assumes the mouse is in the 
    center whenever it is not in closed or open arms. 
    
    Inputs:
        behavior: T x B Pandas DataFrame
            - raw Ethovision (with or without manual scoring from Observer)
            behavior tracking file for EPM.
            
    Returns:
        behavior: T x B Pandas DataFrame
            - processed behavior dataframe that has been downsampled, interpolated
            and new columns added
    """

    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')
    behavior.set_index('Trial_time', inplace=True, drop=True)
    behavior = behavior.resample('100ms').mean()
    #behavior = behavior.resample("100ms", on="Trial_time").mean()
    
    #After resampling, zone columns no longer contain only 0 and 1 (ie. when 
    #mouse transitioned between frames. To avoid ambiguity, round values to 0 or 1
    
    varlist = []
    for var in varlist:
        if var in behavior.columns:
            behavior[var] = behavior[var].where(behavior[var] < 0.5, 1)
            behavior[var] = behavior[var].where(behavior[var] >= 0.5, 0)
    
    #remove NaNs in X,Y due to point being outside of Arena (Ethovision doesn't interpolate in this situation) by interpolating  

    behavior.X_center = behavior.X_center.interpolate()
    behavior.Y_center = behavior.Y_center.interpolate()
    
    x=behavior.X_center.astype(float)
    y=behavior.Y_center.astype(float)
    behavior['Distance_moved'] = au.distance_moved(x,y)
    behavior['Velocity'] = au.compute_velocity(behavior.Distance_moved)    
    
    #Add column to identify immobile time bins (min_vel = 2, min_dur=1)

    behavior['immobile'] = au.define_immobility(behavior.Velocity)
    
    behavior.reset_index(inplace = True)
    
    return behavior

def process_OFT_behavior(behavior, analysis_frame_length = '100ms'):
    """
    Process behavior dataframe containing tracking information from an OFT experiment.
    Assumes there is a Center and Periphery zone. 
    
    Inputs:
        behavior: T x B Pandas DataFrame
            - raw Ethovision (with or without manual scoring from Observer)
            behavior tracking file for OFT.
        analysis_frame_length: str
            - desired frame length of the final behavior dataframe. eg. "100ms"
    Returns:
        behavior: T x B Pandas DataFrame
            - processed behavior dataframe that has been downsampled, interpolated
            and new columns added
    """

    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')
    behavior.set_index('Trial_time', inplace=True, drop=True)
    behavior = behavior.resample(analysis_frame_length).mean()
    #behavior = behavior.resample("100ms", on="Trial_time").mean()
    
    #After resampling, zone columns no longer contain only 0 and 1 (ie. when 
    #mouse transitioned between frames. To avoid ambiguity, round values to 0 or 1
    
    varlist = ['center','periphery']
    for var in varlist:
        if var in behavior.columns:
            behavior[var] = behavior[var].where(behavior[var] < 0.5, 1)
            behavior[var] = behavior[var].where(behavior[var] >= 0.5, 0)
    
    #remove NaNs in X,Y due to point being outside of Arena (Ethovision doesn't interpolate in this situation) by interpolating  

    behavior.X_center = behavior.X_center.interpolate()
    behavior.Y_center = behavior.Y_center.interpolate()
    
    x=behavior.X_center.astype(float)
    y=behavior.Y_center.astype(float)
    behavior['Distance_moved'] = au.distance_moved(x,y)
    behavior['Velocity'] = au.compute_velocity(behavior.Distance_moved)    
    
    #Add column to identify immobile time bins (min_vel = 2, min_dur=1)

    behavior['immobile'] = au.define_immobility(behavior.Velocity)

    behavior.reset_index(inplace = True)
    
    return behavior

########## Below are functions to import AnyMaze files

def read_AnyMaze(AM_filepath):
    """
    Reads in data from an AnyMaze raw data file (in to .csv format). Expected format is a T x B matrix,
    where T is time bins, and B is the automatically tracked behaviors (i.e., Open Arm 1, etc.).
    
    Intended to to be used as a helper function for preprocess_behavior_AM
    
    Args:
        AM_filepath: str
            The file path to the raw AnyMaze .csv file
            
    Returns:
        behavior: pandas DataFrame
            The processed AnyMaze data    
    """   
    
    # read AnyMaze data 
    nrowsheader = pd.read_csv(AM_filepath, nrows=0, encoding="latin1", header=0)
    # nrowsheader = int(nrowsheader.columns[1])
    behavior = pd.read_csv(AM_filepath)
    
    # drop nan's and 1st row 
    behavior = behavior.drop(behavior.index[0]) 
    #behavior = behavior.apply(pd.to_numeric, errors='coerce')
    behavior = behavior.replace([np.inf, -np.inf], np.nan) # drop inf and NaN's
    behavior = behavior.dropna()  

    # rename columns of anymaze file
    renamed = []
    for i in behavior.columns:
        i = i.replace(' ','_').replace('Centre_position_','').replace('In_','').replace('_arm_','').replace('_Arm_','')
        renamed.append(i)
    behavior.columns = renamed  
    
    behavior = behavior.rename(columns={'Time':'Trial_time', 'X':'X_center','Y':'Y_center'})
    
    # add up the 2 separate files for closed and open arms
    behavior['Closed_Arms'] = behavior['Closed1'] + behavior['Closed2']
    behavior['Open_Arms'] = behavior['Open1'] + behavior['Open2']
    
    # convert Trial_time to timedelta function to enable time operations
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')

    return behavior

def preprocess_behavior_AM(AM_filepath=None):
    """
    Processes original AnyMaze files (converted to .csv format)

    Args:
        AM_filepath: str
            The file path to raw AnyMaze behavior .csv file.

    Returns:
        behavior: DataFrame
            The preprocessed behavior DataFrame.
    """

    if AM_filepath:
        #Read in behavior files
        AM_behavior = read_AnyMaze(AM_filepath)
        
        behavior = AM_behavior

        return behavior
    
    raise ValueError("You did not provide an AnyMaze file path.")
    
    
def process_EPM_behavior_AM(behavior, analysis_frame_length = '200ms'):
    """
    Process behavior dataframe containing tracking information from an EPM experiment.
    
    Inputs:
        behavior: T x B Pandas DataFrame
            - raw AnyMaze file (with or without manual scoring from Observer)
            behavior tracking file for EPM.
            **NOTE that there are no 'headdip' analyses for AnyMaze files 
        analysis_frame_length: str
            - desired frame length of the final behavior dataframe. eg. "200ms"
        hd_open: bool, optional
            - if True, all time bins during which the mouse is headdiping will
            be considered OpenArms. This fix can be used to correct times when
            the mouse is tracked to be in the center or closed arms, but is
            in actually investigating the open arms.
            - if False, normal tracking will be used
    Returns:
        behavior: T x B Pandas DataFrame
            - processed behavior dataframe that has been downsampled, interpolated
            and new columns added
    """
    
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')
    behavior.set_index('Trial_time', inplace=True, drop=True) 
    behavior = behavior.resample(analysis_frame_length).mean()
    #behavior = behavior.resample(analysis_frame_length, on='Trial_time').mean() # this usually messes up the fxn
    
    #After resampling, zone columns no longer contain only 0 and 1 (ie. when 
    #mouse transitioned between frames. To avoid ambiguity, round values to 0 or 1
    
    varlist = ['Closed1', 'Open1', 'Center', 'Closed2', 'Open2', 'Closed_Arms', 'Open_Arms']
    for var in varlist:
        if var in behavior.columns:
            behavior[var] = behavior[var].where(behavior[var] < 0.5, 1)
            behavior[var] = behavior[var].where(behavior[var] >= 0.5, 0)

    #remove NaNs in X,Y due to point being outside of Arena (AnyMaze MAY ALREADY) by interpolating  
    #behavior.X_center = behavior.X_center.interpolate()
    #behavior.Y_center = behavior.Y_center.interpolate()
    
    x=behavior.X_center.astype(float)
    y=behavior.Y_center.astype(float)
    behavior['Distance_moved'] = au.distance_moved(x,y)
    behavior['Velocity'] = au.compute_velocity(behavior.Distance_moved)   
    
    behavior=behavior.dropna()
    
    #Add column to identify immobile time bins (min_vel = 2, min_dur=1)
    behavior['immobile'] = au.define_immobility(behavior.Velocity)
    
    behavior=behavior.reset_index(inplace = False)
    
    return behavior

##### Below are functions to import StopWatch files #####

def read_StopWatch(SW_filepath):
    """
    Reads in data from an StopWatch raw data file (in to .csv format). Expected format is a T x B matrix,
    where T is time bins, and B is the automatically tracked behaviors (i.e., freezing).
    
    NOTE: The StopWatch file (original) should have been converted previously in Matlab. 
    
    Intended to to be used as a helper function for preprocess_behavior_SW
    
    Args:
        SW_filepath: str
            The file path to the converted StopWatch .csv file
            
    Returns:
        behavior: pandas DataFrame
            The processed StopWatch data    
    """   
    
    # read StopWatch data 
    nrowsheader = pd.read_csv(SW_filepath, nrows=0, encoding="latin1", header=0)
    # nrowsheader = int(nrowsheader.columns[1])
    behavior = pd.read_csv(SW_filepath)
    
    # drop nan's and 1st row 
    behavior = behavior.drop(behavior.index[0]) 
    #behavior = behavior.apply(pd.to_numeric, errors='coerce')
    behavior = behavior.replace([np.inf, -np.inf], np.nan) # drop inf and NaN's
    behavior = behavior.dropna()  
    
    # rename the time trial only
    behavior = behavior.rename(columns={'time':'Trial_time'})
    
    
    # convert Trial_time to timedelta function to enable time operations
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')

    return behavior

def preprocess_behavior_SW(SW_filepath=None):
    """
    Processes original StopWatch files (converted to .csv format)

    Args:
        SW_filepath: str
            The file path to raw StopWatch behavior .csv file.

    Returns:
        behavior: DataFrame
            The preprocessed behavior DataFrame.
    """

    if SW_filepath:
        #Read in behavior files
        SW_behavior = read_StopWatch(SW_filepath)
        
        behavior = SW_behavior

        return behavior
    
    raise ValueError("You did not provide a StopWatch file path.")
    
    
def process_CFC_behavior_SW(behavior, analysis_frame_length = '200ms'):
    """
    Process behavior dataframe containing tracking information from a CFC experiment.
    
    Inputs:
        behavior: T x B Pandas DataFrame
            - StopWatch file, converted from its original to an "AnyMaze" like format
            on Matlab
        analysis_frame_length: str
            - desired frame length of the final behavior dataframe. eg. "200ms"
    Returns:
        behavior: T x B Pandas DataFrame
            - processed behavior dataframe that has been downsampled, interpolated
            and new columns added
    """
    
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')
    behavior.set_index('Trial_time', inplace=True, drop=True) 
    behavior = behavior.resample(analysis_frame_length).mean()
    #behavior = behavior.resample(analysis_frame_length, on='Trial_time').mean() # this usually messes up the fxn
    
    #After resampling, zone columns no longer contain only 0 and 1 (ie. when 
    #mouse transitioned between frames. To avoid ambiguity, round values to 0 or 1
    
    varlist = ['freezing']
    for var in varlist:
        if var in behavior.columns:
            behavior[var] = behavior[var].where(behavior[var] < 0.5, 1)
            behavior[var] = behavior[var].where(behavior[var] >= 0.5, 0)

    # add a column to the behavioral dataframe that indicates "moving" 
    behavior['moving']=~behavior['freezing']
    
    behavior=behavior.dropna()
    
    behavior=behavior.reset_index(inplace = False)
    
    return behavior

def process_TST_behavior_SW(behavior, analysis_frame_length = '200ms'):
    """
    Process behavior dataframe containing tracking information from a TST experiment.
    The files should be in a StopWatch (hand-scored) format.
    
    Inputs:
        behavior: T x B Pandas DataFrame
            - StopWatch file, converted from its original to an "AnyMaze" like format
            on Matlab
        analysis_frame_length: str
            - desired frame length of the final behavior dataframe. eg. "200ms"
    Returns:
        behavior: T x B Pandas DataFrame
            - processed behavior dataframe that has been downsampled, interpolated
            and new columns added
    """
    
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit = 's')
    behavior.set_index('Trial_time', inplace=True, drop=True) 
    behavior = behavior.resample(analysis_frame_length).mean()
    #behavior = behavior.resample(analysis_frame_length, on='Trial_time').mean() # this usually messes up the fxn
    
    #After resampling, zone columns no longer contain only 0 and 1 (ie. when 
    #mouse transitioned between frames. To avoid ambiguity, round values to 0 or 1
    
    varlist = ['freezing']
    for var in varlist:
        if var in behavior.columns:
            behavior[var] = behavior[var].where(behavior[var] < 0.5, 1)
            behavior[var] = behavior[var].where(behavior[var] >= 0.5, 0)

    # add a column to the behavioral dataframe that indicates "moving" 
    behavior['moving']=~behavior['freezing']
    
    behavior=behavior.dropna()
    
    behavior=behavior.reset_index(inplace = False)
    
    return behavior
