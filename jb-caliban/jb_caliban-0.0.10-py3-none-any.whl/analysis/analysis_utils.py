"""
This module contains all the functions necessary for data preprocessing as well
as data wrangling.

@authors: Saveliy Yusufov, Columbia University, sy2685@columbia.edu
          Jack Berry, Columbia University, jeb2242@columbia.edu
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from analysis.resampling import Resampler

from itertools import product
from scipy.stats import fisher_exact 

def read_ethovision(etho_filepath):
    """
    Reads in data from an Ethovision raw data file (converted to .csv format).
    Expected format is a T x B matrix, where T is time bins, and B is the
    automatically tracked behaviors.

    Intended to to be used as a helper function for preprocess_behavior

    Args:
        etho_filepath: str
            The file path to the raw Ethovision .csv file

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

    # rename columns
    new_cols = []
    for col in behavior.columns:
        col = col.replace(' ', '_').replace("In_zone(", '').replace("_/_center-point)", '')
        new_cols.append(col)

    behavior.columns = new_cols

    # convert Trial_time to timedelta function to enable time operations
    behavior.Trial_time = pd.to_timedelta(behavior.Trial_time, unit='s')

    return behavior

def read_observer(observer_filepath):
    """
    Reads in data from an observer file (converted to .csv format). Expected
    format is a T x B matrix, where T is time bins, and B is the hand-scored
    behaviors.

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

def preprocess_behavior(etho_filepath=None, observer_filepath=None):
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
        etho_behavior = read_ethovision(etho_filepath)
        obs_behavior = read_observer(observer_filepath)
        num_obs = len(obs_behavior.columns)
        
        #Merge Ethovision and Observer data
        behavior = pd.merge(etho_behavior, obs_behavior, how="left", left_index=True, right_index=True)
        behavior.update(behavior[behavior.columns[-num_obs:]].fillna(0))
        
        return behavior

    elif etho_filepath:
        etho_behavior = read_ethovision(etho_filepath)
        return etho_behavior
        
    elif observer_filepath:
        obs_behavior = read_observer(observer_filepath)
        return obs_behavior
    
    else:
        raise ValueError("You did not provide an ethovision or observer file path")

def z_score_data(data, mew=None):
    """This function simply z scores all the given neural signal data.

    Args:
        data: DataFrame
            Ca2 transient data in T x N format, where N is the # of neuron
            column vectors, and T is the number of observations (rows),
            all in raw format.

        mew: int, optional, default: None
            The mean value for the baseline of the data.
            Note: if the raw data comes from CNMF_E, use 0 for the baseline.

    Returns:
        z_scored_data: DataFrame
            The z scored raw cell data in T x N format.
    """
    pop_offset = np.percentile(data.values, 50)
    sigma = np.std(data.values, axis=0)

    if mew is None:
        mew = np.mean(data.values[data.values < pop_offset])
    else:
        mew = mew

    z_scored_data = pd.DataFrame(data=((data.values - mew) / sigma))
    return z_scored_data


def pairwise_dist(x_coords):
    """Computes consecutive pairwise differences in a Series.

    NOTE: This is a helper function for distance_moved.

    Args:
        x_coords: pandas Series
            A one-dimensional ndarray of x coordinates, over time.

    Returns:
        dx: pandas Series
            A series containing all the values x[i] - x[i-1]

    """
    x_coords = x_coords.astype(float)
    delta_x = (np.roll(x_coords, -1) - x_coords).shift(1)
    return delta_x


def distance_moved(x_coords, y_coords):
    """Computes the distance moved per frame

    Args:
        x_coords: pandas Series
            A one-dimensional ndarray of x coordinates, over time.

        y_coords:
            A one-dimensional ndarray of y coordinates, over time.

    Returns
        Series containing distance moved per frame

    """
    if len(x_coords) != len(y_coords):
        raise ValueError("x_coords and y_coords are not of equal length!")

    delta_x = pairwise_dist(x_coords.astype(float))
    delta_y = pairwise_dist(y_coords.astype(float))

    dist_moved = delta_x**2 + delta_y**2
    dist_moved = dist_moved.apply(np.sqrt)
    return dist_moved


def compute_velocity(dist_moved, framerate=10):
    """
    Args:
        dist_moved: pandas Series
            A one-dimensional ndarray containing distance moved.

        framerate: int, optional, default: 10
            The frame rate corresponding to the dist_moved Series.

    Returns:
        velocity: pandas Series
            A one-dimensional ndarray containing velocity.
    """
    velocity = dist_moved.apply(lambda x: x * framerate)
    return velocity


def define_immobility(velocity, min_dur=1, min_vel=2, framerate=10, min_periods=1):
    """Define time periods of immobility based on a rolling window of velocity.

    A Mouse is considered immobile if velocity has not exceeded min_vel for the
    previous min_dur seconds.

    Default values for min_dur and min_vel are taken from:
    Stefanini...Fusi et al. 2018 (https://doi.org/10.1101/292953)

    Args:
        velocity: pandas Series
            A one-dimensional ndarray of the velocity data.

        min_dur: int, optional, default: 1
            The minimum length of time in seconds in which velocity must be low.

        min_vel: int, optional, default: 2
            The minimum velocity in cm/s for which the mouse can be considered
            mobile.

        framerate: int, optional, default: 10
            The frame rate of the velocity Series. Default is 10 fps.

        min_periods: int, optional, default: 1
            Minimum number of datapoints needed to determine immobility. This
            value is needed to define immobile time bins at the beginning of the
            session. If min_periods=8, then the first 8 time bins will be be
            considered immobile, regardless of velocity.

    Returns:
        mobile_immobile: pandas Series
            A one-dimensional ndarray of 0's and 1's, where 1 signifies immobile
            times and 0 signifies mobile times.

    """
    window_size = framerate * min_dur
    rolling_max_vel = velocity.rolling(window_size, min_periods=min_periods).max()
    mobile_immobile = (rolling_max_vel < min_vel).astype(int)

    return mobile_immobile


def find_file(root_directory, target_file):
    """Finds a file in a given root directory (folder).

    Args:
        root_directory: str
            The name of the first or top-most directory (folder)
            to search for the target file (e.g. "Hen_Lab/Mice").

        target_file: str
            The full name of the file to be found (e.g. "mouse1_spikes.csv").

    Returns:
        file_path: str
            The full path to the target file.

    """
    root_directory = os.path.join(os.path.expanduser("~"), root_directory)

    if not os.path.exists(root_directory):
        raise FileNotFoundError("{} does not exist!".format(root_directory))
    if not os.path.isdir(root_directory):
        raise NotADirectoryError("{} is not a directory!".format(root_directory))

    for subdir, _, files in os.walk(root_directory):
        for file in files:
            if file == target_file:
                file_path = os.path.join(subdir, file)
                return file_path

    raise FileNotFoundError("{} not found!".format(target_file))


def extract_epochs(mouse, behavior):
    """Extract all epochs of a continuous behavior/event.

    Args:
        mouse: Mouse
            An instance of the Mouse class that has a `spikes_and_beh`
            pandas DataFrame, where `spikes_and_beh` has neural activity
            and corresponding behavior concatenated.

        behavior: str
            The name of the behavior to use when extracting continuous time
            periods/events.

    Returns:
        epochs: pandas Series
            A Series that has hierarchical indices, where "behavior" is the
            outermost index, followed by "interval". Each interval contains
            an ndarray of timepoints in which the corresponding behavior was
            observed, continuously.
    """
    if behavior not in mouse.spikes_and_beh.columns:
        raise ValueError("'{}' is not a column (i.e. behavior) in the mouse's dataframe".format(behavior))

    dataframe = mouse.spikes_and_beh.copy()

    # Find all timepoints where the behavior discontinues
    dataframe["interval"] = (dataframe[behavior].shift(1) != dataframe[behavior]).astype(int).cumsum()

    # Put the index into the dataframe as a column, without creating a new DataFrame
    dataframe.reset_index(inplace=True)

    # Group the dataframe by behavior and corresponding intervals,
    # and apply np.array to the index column of each group.
    epochs = dataframe.groupby([behavior, "interval"])["index"].apply(np.array)

    return epochs


def filter_epochs(interval_series, framerate=10, seconds=1):
    """Helper function for extract_epochs.

    Args:
        interval_series: pandas Series
            A Series with an ndarray of continous behavior timepoints, for each
            index.

        framerate: int, optional, default: 10
            The framerate that corresponds to the session from which the
            intervals were extracted.

        seconds: int, optional, default: 1
            The amount of seconds.

    Returns:
        intervals: list
            A list of all the intervals that are at least as long as the
            provided framerate multiplied by the provided seconds.
    """
    intervals = [interval for interval in interval_series if len(interval) >= framerate*seconds]
    return intervals

def get_binary_cols(df):
    """
    Helper function that returns the column names of all columns in a dataframe
    that only have boolean values (0 or 1)
    
    Inputs:
        df, pandas dataframe
    
    Returns:
        cols, list of str
            list of boolean column names
    """
    
    cols = []
    for c in df.columns:
        vals = set(df[c])
        if vals==set([0,1]):
            cols.append(c)
    return cols

class Mouse:
    """A base class for keeping all relevant & corresponding objects, i.e.,
    spikes, cell transients, & behavior dataframes, with their respective
    mouse.
    """

    def __init__(self, cell_transients=None, spikes=None, behavior=None, 
                 A=None, Cn=None, **kwargs):
        self.name = kwargs.get("name", None)
        self.age = kwargs.get("age", None)
        self.sex = kwargs.get("sex", None)
        self.FR = kwargs.get('FR', None)
        self.session = kwargs.get('session', None)
        self.group = kwargs.get('group', None)
        self.raw = kwargs.get('raw', None)
        self.cell_transients = cell_transients
        self.spikes = spikes
        self.A = A
        self.Cn = Cn

        if behavior is not None:
            self.behavior = behavior
            self.spikes_and_beh = self.spikes.join(self.behavior, how="left")
        else:
            print("A behavior dataframe was not provided.", file=sys.stderr)

        velocity_cutoff = kwargs.get("velocity_cutoff", None)

        # Adds "Running_frames" column to the end of the behavior Dataframe
        if velocity_cutoff is not None:
            running_frames = np.where(self.behavior["Velocity"] > velocity_cutoff, 1, 0)
            self.behavior = self.behavior.assign(Running_frames=running_frames)
            
    def rates(self,cols=None, in_zone=True):
        """
        Computes the average rate for each neuron during the entire session, and during each
        behavior/zone.
        
        Inputs:
            cols: list, optional
                The column names in Mouse.behavior for which to compute rates.
            in_zone: boolean, optional
                A flag which indicates whether rate calculation should be performed for
                periods during behavior/zone or NOT during behavior/zone. 
        
        """
        
        if cols is None:
#            cols = []
#            for c in self.behavior.columns:
#                vals = set(self.behavior[c])
#                if vals==set([0,1]):
#                    cols.append(c)
            cols = get_binary_cols(self.behavior)
        fr = self.FR
        if fr is None:
            print('No framerate given, defaulting to 10', file=sys.stderr)
            fr = 10
        
        rate_df = pd.DataFrame()
        sb = self.spikes_and_beh
        
        rate_df.loc[:,'entire_session'] = fr * self.spikes.mean()

        #computes the average rate for each neuron during each behavior/zone
        if in_zone == True:
            for c in cols:
                rate_df.loc[:,c] = fr * self.spikes.loc[sb[c] != 0,:].mean()
            rate_df.index.name='neuron'
            rate_df.reset_index(inplace=True)
        #computes the average rate for each neuron when each behavior/zone is NOT occurring
        elif in_zone == False:
            for c in cols:
                rate_df.loc[:,'not_' + c] = fr * self.spikes.loc[sb[c] == 0,:].mean()
            rate_df.index.name='neuron'
            rate_df.reset_index(inplace=True)
        
        if self.name:
            rate_df.loc[:,'mouse'] = np.tile(self.name, len(rate_df)) 
        
        return rate_df

    def rateShuffle(self, resamples=10000, statistic=Resampler.diff_of_mean_rate, cols=None):
        """
        Wrapper method for the Resampler.shuffle function which generates a permutation
        distribution for neuron selectivity analysis.

          Inputs:
            resamples: int, optional
                The number of permutations to perform.
            statistic: Resampler method, optional
                Defines the test statistic to be calculated with each shuffle. Default method
                is a difference of mean rate between in-zone and out-of-zone periods.
            cols: list, optional
                The column names in Mouse.behavior for which to compute rates.
        """
        dataframe = self.spikes
        
        shuffle_dict = {}
        if cols is None:
            cols = get_binary_cols(self.behavior)
        fr = self.FR
        for col in cols:
            shuffle_dict[col] = Resampler.shuffle(resamples, dataframe, statistic, self.behavior[col])
        
        return shuffle_dict
    
    def selectivity(self, p_cutoff=0.05, rate_data_df=None, shuffle_dict=None, cols=None):
        """
        Wrapper method for the cellSelectivity function which calculates single neuron
        selectivity for each neuron for particular behaviors/zones.
        
        Inputs:
            p_value: float, optional
                The p-value cutoff for significant selectivity (i.e. p = 0.05).
                Default is 0.05.
            rate_data_df: pd.DataFrame, optional
                The DataFrame containing single cell event rates for each neuron.
                If none is provided the mouse.rates method will be used.
            shuffle_dict: dict, optional
                A dictionary with key:value pairs of a string indicating the behavior/zone
                and a pd.DataFrame with the permutation distribution for that behavior/zone.
                If none is provided the mouse.rateShuffle method will be used.
            cols: list, optional
                The column names in mouse.behavior for which to compute rates.
        """
        if cols is None:
            cols = get_binary_cols(self.behavior)

        if rate_data_df is None:
            rate_data_df = self.rates()

        if shuffle_dict is None:
            shuffle_dict = self.rateShuffle()

        fr = self.FR

        for col in cols:
            shuffle = shuffle_dict[col]
            classified, z_scores = cellSelectivity(self, shuffle_dict[col], col, p_cutoff=p_cutoff)
            rate_data_df[col + '_selectivity'] = classified
            rate_data_df[col + '_z_score'] = z_scores

        return rate_data_df
    
    def resample(self, new_FR, method='default'):
        """
        Resamples the time series dataframes of a mouse object to a new framerate
        and returns a new mouse object
        
        Inputs:
            new_FR: float
                New frame rate (in seconds)
            method: str, optional
                Method used to resample the dataframes. Must be 'default','mean' or 'sum'
                If 'default', self.spikes will be resampled with 'sum' method, and all others
                will be resampled with 'mean'. This maintains the spike rates and 
                fluorescence values (raw, cell_transients) for plotting purposes.
        Returns:
            resampled_mouse: Mouse object
                New mouse object 
        
        """
        
        import copy
        resampled_mouse = copy.deepcopy(self)
        new_fields = ['spikes','raw','cell_transients','spikes_and_beh','behavior']
    
        for field,data in resampled_mouse.__dict__.items():
            if field in new_fields:
                if method=='default':
                    if field=='spikes':
                        meth = 'sum'
                    else:
                        meth = 'mean'
                else:
                    meth = method
                
                if field in ['spikes_and_beh','behavior']:
                    bin_cols = get_binary_cols(getattr(self,field))
                    # add back Trial_time
                    data_new = resample_ts(data,current_FR=str(np.round(1000/self.FR,3))+'ms',
                                          new_FR=str(np.round(1000/new_FR,3))+'ms',method=meth,drop_time=False)
                    for col in bin_cols:
                        data_new[col] = data_new[col].where(data_new[col] < 0.5, 1)
                        data_new[col] = data_new[col].where(data_new[col] >= 0.5, 0)
                #data = data.fillna(method='ffill')
                else:
                    data_new = resample_ts(data,current_FR=str(np.round(1000/self.FR,3))+'ms',
                          new_FR=str(np.round(1000/new_FR,3))+'ms',method=meth,drop_time=True)
                
                setattr(resampled_mouse,field,data_new)
        resampled_mouse.FR = new_FR
    
        return resampled_mouse

    def reconvolve(self, tau):
        import copy
        new_mouse = copy.deepcopy(self)        
        conv_func = _get_conv_func(tau=tau, FR = self.FR)
        new_mouse.cell_transients = new_mouse.spikes.apply(np.convolve, args=[conv_func,'same'])
        
        return new_mouse    

    def subsample(self,n_neurons,replace=False,random_state=None):
        """
        Returns a Mouse object that contains a subsample of the neurons

        Parameters
        ----------
        n_neurons : int
            The number of neurons to subsample. If n_neurons > the actual number
            of neurons in the Mouse object, the function will return an identical
            Mouse object
        replace : bool, optional
            Sample with replacement. The default is False.
        random_state : int, optional
            The seed that is passed to pandas.DataFrame.sample function.
            The default is None.

        Returns
        -------
        subsampled mouse object.

        """
        import copy
        mouse_samp = copy.deepcopy(self)
        
        if n_neurons < len(self.spikes.columns):
            
            mouse_samp.spikes = self.spikes.sample(n_neurons,axis=1,replace=replace,random_state=random_state)
            mouse_samp.raw = self.raw[mouse_samp.spikes.columns]
            mouse_samp.cell_transients = self.cell_transients[mouse_samp.spikes.columns]
    
        return mouse_samp

def _get_conv_func(tau, FR=10):
    """
    Helper function that returns an exponential decay function to be used
    to re-convolve mouse.cell_transients with the desired tau

    Parameters
    ----------
    tau : float
        decay constant (in seconds) for the convolution function
    FR : int, optional
        Frames per second of the function. The default is 10.

    Returns
    -------
    conv_func : numpy array
        An exponential decay function. It is 1000 frames long, with the
        funtion beginning at frame 500.

    """
    
    n_samples = 500
    tau_frame=tau * FR #tau, in number of frames
    conv_func = np.roll(np.exp(-np.arange(n_samples) / tau_frame), int(n_samples/2))
    conv_func[:int(n_samples/2)] = 0
    
    #conv_func /= np.sum(conv_func)
    
    return conv_func
def cellSelectivity(mouse, permutation_distribution, behavior, statistic=Resampler.diff_of_mean_rate, p_cutoff=0.05):
    """Performs cell selectivity analysis on neural data.

    This function can define cell selectivity for particular behavioral epochs. It computes a test statistic 
    *statistic* (i.e. difference of means) on neural data *mouse.spikes* with a particular behavior/zone *behavior 
    and utilizes a shuffle distribution *permutation_distribution* with a calculated p-value to determine if a cell 
    is 'selective' as defined by a p-value cutoff *p_cutoff (has increased activity in one behavioral epoch vs another 
    behavioral epoch).

    Inputs:
        mouse: Mouse object
            The mouse object from which spike and behavior data are drawn from.
            
        permutation_distribution: Dataframe
            A pandas Dataframe of the permutation distribution.
        
        behavior: string
            The string identifying the behavior/zone used to index the behavior DataFrame.
        
        statistic: function
            The test statistic that is computed on each neuron's activity data. 
            Default is Resampler.diff_of_mean_rate.

        p_cutoff: float
            The p-value cutoff for significant selectivity (i.e. p = 0.05);
            default is 0.05.

    Returns:
        classified: np.array
            An np.array with the selectivity classifications for each neuron during the desired behavior/zone.
        
        z_scores: np.array
            An np.array with the z-scores for each neuron during the desired behavior/zone.
    """
    # draw neural data and framerate from mouse object
    neural_data = mouse.spikes
    fr = mouse.FR
    
    # get the boolean vectors for periods when the mouse is or is not performing a behavior or in a zone
    beh = mouse.behavior[behavior] == 1
    not_beh = mouse.behavior[behavior] == 0
    
    # calculates the test statistic for each neuron
    statistic_vec = statistic(neural_data, beh, not_beh, frame_rate=fr)
    
    # calculates p-values for each neuron
    p_values = np.array([Resampler.p_value(statistic_vec[idx], permutation_distribution[neuron]) for idx,neuron in enumerate(neural_data.columns)])
    
    # calculates z-scores for each neuron
    z_scores = np.array([Resampler.z_score(statistic_vec[idx], permutation_distribution[neuron]) for idx,neuron in enumerate(neural_data.columns)])
    
    #determines the cell selectivity for each neuron
    classified = np.array([None] * len(neural_data.columns))
    classified[(statistic_vec > 0) & (p_values < p_cutoff)] = behavior + '_activated'
    classified[(statistic_vec < 0) & (p_values < p_cutoff)] = behavior + '_inhibited'
    classified[(p_values > p_cutoff)] = 'non_selective'
    
    return classified, z_scores

def downsample_dataframe(dataframe, row_multiple):
    """Downsample a given pandas DataFrame

    Args:
        dataframe: DataFrame
            The pandas DataFrame to be downsampled.

        row_multiple: int
            The row multiple is the rows to be removed,
            e.g., a row_multiple of 3 would remove every 3rd row from the
            provided dataframe

    Returns:
        dataframe: DataFrame
            The downsampled pandas DataFrame.
    """

    # Drop every nth (row multiple) row
    dataframe = dataframe.iloc[0::row_multiple, :]

    # Reset and drop the old indices of the pandas DataFrame
    dataframe.reset_index(inplace=True, drop=True)

    return dataframe

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


def activity_by_neurons(spikes_and_beh, neuron_names, *behaviors, **kwargs):
    """Computes the neuron activity rates for given behaviors

    This function computes the rates for a given animal's activity and
    neuron, given some set of behaviors.

    Args:
        spikes_and_beh: DataFrame
            A concatenated pandas DataFrame of the neuron activity and
            the corresponding behavior, for a given animal.

        neuron_names: list
            The names of the neurons whose rates are to be computed.

        behaviors: arbitrary argument list
            The behaviors for which to compute the activity rates.
            NOTE: If no behaviors are provided, then the average rate over the
            entire session.

        frame_rate: int, optional, default: 10
            The framerate by which to multiply the activity rate.

    Returns:
        activity_df: DataFrame
            A pandas DataFrame of the neuron activity rates.
    """
    if set(neuron_names).issubset(spikes_and_beh.columns) is False:
        raise ValueError("neuron_names is NOT a subset of the columns in spikes_and_beh!")

    frame_rate = kwargs.get("frame_rate", None)

    if frame_rate is None:
        print("You did not specify a frame rate! Defaulting to 10", file=sys.stderr)
        frame_rate = 10

    activity_df = pd.DataFrame(columns=behaviors)

    for behavior in behaviors:
        if behavior in spikes_and_beh.columns:
            activity_df.loc[:, behavior] = frame_rate * spikes_and_beh.loc[spikes_and_beh[behavior] != 0, neuron_names].mean()
        else:
            raise ValueError("{} is not a column (i.e. behavior) in spikes_and_beh.".format(behavior))

    # Return average rate over entire session if no behavior(s) is/are provided
    if not behaviors:
        behavior = "entire_session"
        activity_df = pd.DataFrame(columns=[behavior])
        activity_df.loc[:, behavior] = frame_rate * spikes_and_beh.loc[:, neuron_names].mean()

    return activity_df

def old_div(a, b):
    """
    DEPRECATED: import ``old_div`` from ``past.utils`` instead.

    Equivalent to ``a / b`` on Python 2 without ``from __future__ import
    division``.

    TODO: generalize this to other objects (like arrays etc.)
    
    
    Used in caimain functions
    """

    return a // b


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

def behavior_start_stop(beh_intervals, time, fr):
        
    beh_starts = [beh_intervals[i][0] for i in range(len(beh_intervals))]
    beh_stops = [beh_intervals[i][-1] for i in range(len(beh_intervals))]
    start_range = [[i-time*fr,i+time*fr] for i in beh_starts]
    stop_range = [[i-time*fr,i+time*fr] for i in beh_stops]

    return start_range, stop_range

def event_triggered_activity(mice, behavior=None, time=5, min_time=1):
    beh_intervals = {}

    activity_start = {} #dict storing event-start activity
    activity_stop = {} #dict storing event-stop activity

    for k,v in mice.items():
        if behavior in mice[k].behavior.columns:

            beh_intervals[k] = extract_epochs(mice[k],behavior)[1]
            beh_intervals[k] = filter_epochs(beh_intervals[k],framerate=mice[k].FR,seconds=min_time)

            #get time ranges for behavior start and stop 
            start_range, stop_range = behavior_start_stop(beh_intervals[k], time, v.FR)

            #define the time points which to analyze
            xax = np.arange(-time,time,1/v.FR)

            #initialize activity arrays
            act_start_array = np.zeros(shape=(len(xax), len(mice[k].cell_transients.columns), 1))
            act_stop_array = np.zeros(shape=(len(xax), len(mice[k].cell_transients.columns), 1))
            
            #get all neural activity during the start and stop time windows
            for i in start_range:
                act_start = np.array(v.cell_transients.loc[i[0]:i[1]-1,:].reset_index(drop=True))[:,:,np.newaxis]
                if (len(act_start) == len(xax)):
                    act_start_array = np.concatenate([act_start_array, act_start], axis=2)

            for i in stop_range:
                act_stop = np.array(v.cell_transients.loc[i[0]:i[1]-1,:].reset_index(drop=True))[:,:,np.newaxis]
                if (len(act_stop) == len(xax)):
                    act_stop_array = np.concatenate([act_stop_array, act_stop], axis=2)

            activity_start[k] = act_start_array
            activity_stop[k] = act_stop_array
            
    return activity_start, activity_stop, xax

def get_eta(activity, xax, which_cells):
    
    temp = []
    for m in which_cells['mouse'].unique():
        behavior = which_cells['Behavior'].unique()[0]
        neurons = which_cells.query(f"mouse == '{m}'")['neuron'].values - 1
        
        temp.append(activity[m, behavior][:,neurons,:].mean(axis=2))
    
    temp = tuple(temp)
    
    eta = np.concatenate(temp, axis=1)
        
    return eta   

def plot_eta(eta, xax, ax, color='k'):
    mu = np.mean(eta,1)
    se = np.std(eta,1)/np.sqrt(eta.shape[1])
    #fig,ax = plt.subplots(figsize=(2.5,2.5))

    ax.plot(xax,mu, linewidth=1, color=color)
    ax.fill_between(xax,mu+se,mu-se, zorder=0, alpha=.3, color=color)
    ax.axvline(x=0,color='r',linestyle='--')
    ax.set_xlabel('Time Relative \nto Behavior (s)')
    ax.set_ylabel('Average Z-scored \nActivity')

def analyze_eta(mice, behavior, ax=None, time=5, min_time=1, which_cells=[], colors=['k','b']):
    
    if ax is None:
        fig,ax = plt.subplots(1, 2, figsize=(4,2))
    colors = colors
    
    activity_start, activity_stop, xax = event_triggered_activity(mice=mice, behavior=behavior, time=time, min_time=min_time)
    
    for i, cells in enumerate(which_cells):
        eta_start = get_eta(activity_start, xax, cells)
        eta_stop = get_eta(activity_stop, xax, cells)


        plot_eta(eta_start, xax, ax[0], color=colors[i])
        ax[0].set_title(behavior+' start')
        
        plot_eta(eta_stop, xax, ax[1], color=colors[i])
        ax[1].set_title(behavior+' stop')
        ax[1].set_ylabel('')
    return ax
    
def resample_ts(timeseries, current_FR, new_FR, method='mean',drop_time=True):
    timeseries = timeseries.assign(Trial_time=pd.timedelta_range(0, periods=len(timeseries.index), freq=current_FR))
    if method=='mean':
        timeseries = timeseries.resample(new_FR, on="Trial_time").mean().reset_index(drop = drop_time)
    elif method=='sum':
        timeseries = timeseries.resample(new_FR, on="Trial_time").sum().reset_index(drop = drop_time)
    else:
        print('Unsopported resampling method: please choose mean or sum')
        return;
    return timeseries

# Analysis Functions for Single Neuron Properties

def selectivity_counts(neuron_data_df, behaviors, normalize=False):
    """Determines the frequency of activated, inhibited, and non-selective neurons for specified behaviors/zones.
    
    This function takes a DataFrame containing information regarding single neurons (e.g. selectivity_data_df)
    and calculates the frequency of activated, inhibited, and non-selective neurons for each specified
    behavior/zone.

    Inputs:
        neuron_data_df: pd.DataFrame
            A pandas DataFrame containing information (e.g. rates, selectivity, z-scores, other metrics) regarding
            single neurons.
        behaviors: list
            A list of strings which define the behaviors or zones of interest. These should correspond to column
            names in neuron_data_df
        normalize: boolean
            Flag which indicates whether absolute or relative frequencies should be calculated.
            Default is False which produces absolute frequencies.
        
    Returns:
        selectivity_counts_df: pd.DataFrame
            A 'wide' pandas DataFrame with the specified behaviors as columns and 
            index = ['activated', 'inihibited', 'non_selective']. Values are either the absolute or 
            relative frequencies.
    """
    selectivity_col_names = [behavior + '_selectivity' for behavior in behaviors]
    selectivity_counts_df = neuron_data_df[selectivity_col_names].replace(
        {r'(^.*activated.*$)':'activated', r'(^.*inhibited.*$)':'inhibited'}, regex=True).apply(
        pd.value_counts, normalize=normalize).fillna(0)
    selectivity_counts_df.columns = [col_name.replace('_selectivity', '') for col_name in selectivity_counts_df.columns]
    
    if normalize == False:
        selectivity_counts_df = selectivity_counts_df.astype('int')
    
    return selectivity_counts_df
    
    
    #dfs = [] # initialize an empty list to accumulate processed counts DataFrames for each behavior/zone
    #for behavior in behaviors:
        # change the column labels to remove the string '_selectivity' and the indices to remove behavior/zone
    #    temp = neuron_data_df[behavior+'_selectivity'].value_counts(normalize=normalize).rename(
    #        index={behavior+'_activated':'activated', behavior+'_inhibited':'inhibited'}).sort_index()
    #    temp.name = behavior
    #    dfs.append(temp)
    #selectivity_counts_df = pd.concat(dfs, axis=1, sort=True).fillna(0)
    
def PairwiseCategoricalOverlap(categorical_df, statistical_test=fisher_exact):
    # Generate the index by using the cartesian product of each column name with the unique entries in the column
    ind_list = []
    for name, values in categorical_df.items():
        ind_list.extend(list(product([name], np.sort(values.unique()))))
    overlap_index = pd.MultiIndex.from_tuples(ind_list) # Create a pandas MultiIndex
    
    # Create empty DataFrames to collect p-values and odds ratios using the index generated above as both the index 
    # and column labels
    p_value_df = pd.DataFrame(index=overlap_index, columns=overlap_index)
    odds_ratio_df = pd.DataFrame(index=overlap_index, columns=overlap_index)
    
    # Generate a 2x2 table for each pair of categorical values and compute the p-value and odds ratio using a
    # statistical test which should take as input the 2x2 table and output an odds ratio and p-value
    for ind in overlap_index:
        for col in overlap_index:
            tab = pd.crosstab((categorical_df[ind[0]] == ind[1]).astype('str'), 
                              (categorical_df[col[0]] == col[1]).astype('str')).loc[['True', 'False'],['True','False']]
            odds_ratio_df.loc[ind,col], p_value_df.loc[ind,col] = statistical_test(tab)
    
    # Typecast the p-value and odds ratio DataFrames to floats
    p_value_df = p_value_df.astype('float')
    odds_ratio_df = odds_ratio_df.astype('float')
    
    return p_value_df, odds_ratio_df

def SelectivityOverlap(neuron_data_df, behaviors, statistical_test=fisher_exact):
    
    selectivity_cat_df = neuron_data_df[[behavior+'_selectivity' for behavior in behaviors]].copy()
    selectivity_cat_df.replace({r'(^.*activated.*$)':'activated', r'(^.*inhibited.*$)':'inhibited'}, regex=True, inplace=True)
    selectivity_cat_df.columns = [colname.replace('_selectivity', '') for colname in selectivity_cat_df.columns]
    
    p_value_df, odds_ratio_df = PairwiseCategoricalOverlap(selectivity_cat_df, statistical_test=statistical_test)
    
    return p_value_df, odds_ratio_df
    
