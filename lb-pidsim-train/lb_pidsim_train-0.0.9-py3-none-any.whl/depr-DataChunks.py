import numpy as np 
import pandas as pd 
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import sys
import uproot4
from tqdm import trange

from .utils import NaNFilter



class DataChunks:
  """
  Data-chunks
  ===========
  ...
  Attributes
  ----------
    ...
  Methods
  -------
    ...
  """
  def __init__ ( 
                 self               ,
                 file_list          ,
                 tree_name   = None , 
                 input_vars  = None ,
                 output_vars = None ,
                 weight_vars = None ,
                 selection   = None ,
                 chunk_size  = 1000 ,
                 max_files   = 100  ,
               ):
    """
    Constructor.
    Parameters
    ----------
      ...
    Attributes
    ----------
      ...
    Returns
    -------
      None
    """
    self.in_branches  = input_vars
    self.out_branches = output_vars
    self.w_branches   = weight_vars
    self.selection    = selection
    self.chunk_size   = chunk_size
    self.max_files    = max_files

    self.trees   = list()
    self.entries = list()

    for f in file_list: 
      root_file = uproot4.open (f)

      if tree_name:
        key = tree_name
      else:
        k = root_file.keys()
        key = k[0].split(';')[0]   # take the TTree name

      tree = root_file [ key ]
      self.trees   . append ( tree )

      tree_entry = tree.num_entries
      self.entries . append ( tree_entry )


  ##############
  ##  Iterator
  ##############
  def __iter__ (self):
    """
    Iterator.
    Parameters
    ----------
      None
    Attributes
    ----------
      None
    Returns
    -------
      ...
    """
    branches = self.in_branches + self.out_branches + self.w_branches
    while True:
      db = self._load_data_from_tree (branches, verbose = True)
      yield (db) 


  #########################
  ##  Load data from tree
  #########################
  def _load_data_from_tree (self, branches, verbose = False):
    """
    Internal method.
    ...
    Parameters
    ----------
      ...
    Attributes
    ----------
      None
    Returns
    -------
      ...
    """
    id_trees = np.random.permutation (len (self.trees)) [:self.max_files]
    tot_entries = np.sum (self.entries)
    datasets = list()

    for i in id_trees:
      tree = self.trees[i]
      fraction  = float ( self.entries[i] / tot_entries ) 
      tree_size = int ( fraction * self.chunk_size )  
      entry_start = np.random.randint ( 0, max (1, self.entries[i] - tree_size) ) 
      entry_stop  = entry_start + tree_size

      datasets . append ( 
                          tree.arrays ( branches                  ,
                                        cut = self.selection      ,
                                        entry_start = entry_start ,
                                        entry_stop  = entry_stop  ,
                                        library = 'pd'            )
                        )

    if verbose:
      print ( "Loaded data from ROOT files as DataFrame of %d rows" % sum ([len (d) for d in datasets]) ) 
    return pd.concat (datasets)


  ##############
  ##  Get data
  ##############
  def getDatasets (self):
    branches = self.in_branches + self.out_branches + self.w_branches
    return self._load_data_from_tree (branches, verbose = True)


  #################################
  ##  Get data for classification
  #################################
  def getClassDatasets (
                         self              , 
                         preprocessing     , 
                         noise_size        , 
                         generator         , 
                         num_datasets = 10 ,
                       ):
    """
    Get datasets method.
    ...
    Parameters
    ----------
      ...
    Attributes
    ----------
      None
    Returns
    -------
      ...
    """
    train_sets  = list()
    label_sets  = list()
    weight_sets = list()

    for dset in range (num_datasets):
      gen_cands, ref_cands = self._get_cols_per_branch (preprocessing, noise_size, generator)
      X_gen, Y_gen, w_gen  = gen_cands
      X_ref, Y_ref, w_ref  = ref_cands

      XY_gen = np.concatenate ([X_gen, Y_gen], axis = 1)
      XY_ref = np.concatenate ([X_ref, Y_ref], axis = 1)
      label_gen = np.array (['gen' for i in range (len (XY_gen))])
      label_ref = np.array (['ref' for i in range (len (XY_ref))])

      XY = np.concatenate ([XY_gen, XY_ref], axis = 0)
      labels  = np.concatenate ([label_gen, label_ref], axis = 0)
      weights = np.concatenate ([w_gen, w_ref], axis = 0) . flatten()

      index = np.random.permutation (len (XY))
      train_sets  . append (XY[index] . astype (np.float32))
      label_sets  . append (labels[index])
      weight_sets . append (weights[index] . astype (np.float32))

    return train_sets, label_sets, weight_sets


  #############################
  ##  Get data for validation
  #############################
  def getValDatasets (
                       self              , 
                       preprocessing     , 
                       noise_size        , 
                       generator         , 
                       num_datasets = 10 ,
                     ):
    """
    Get datasets method.
    ...
    Parameters
    ----------
      ...
    Attributes
    ----------
      None
    Returns
    -------
      ...
    """
    gen_sets  = list()
    ref_sets  = list()

    for dset in range (num_datasets):
      gen_cands, ref_cands = self._get_cols_per_branch (preprocessing, noise_size, generator)
      X_gen, Y_gen, w_gen  = gen_cands
      X_ref, Y_ref, w_ref  = ref_cands

      cols = ['probe_Brunel_P', 'probe_Brunel_ETA', 'nTracks_Brunel'] + \
             self.out_branches + ['probe_sWeight']

      gen_data = pd.DataFrame ( columns = cols )
      gen_data.loc [:, self.in_branches]  = X_gen
      gen_data.loc [:, self.out_branches] = Y_gen
      gen_data ['probe_sWeight'] = w_gen
      gen_sets . append (gen_data)

      ref_data = pd.DataFrame ( columns = cols )
      ref_data.loc [:, self.in_branches]  = X_ref
      ref_data.loc [:, self.out_branches] = Y_ref
      ref_data ['probe_sWeight'] = w_ref
      ref_sets . append (ref_data)

    return gen_sets, ref_sets


  ############################
  ##  Get columns per branch
  ############################
  def _get_cols_per_branch (self, preprocessing, noise_size, generator):
    """
    Internal method.
    ...
    Parameters
    ----------
      ...
    Attributes
    ----------
      None
    Returns
    -------
      ...
    """
    scaler_X, scaler_Y = preprocessing

    gen_branches = self.in_branches + self.w_branches
#    gen_branches = self.in_branches + self.out_branches + self.w_branches
    gen_db = self._load_data_from_tree ( gen_branches, verbose = False )

    ref_branches = self.in_branches + self.out_branches + self.w_branches
    ref_db = self._load_data_from_tree ( ref_branches, verbose = False )

    db_size = min ( len(gen_db), len(ref_db) )
    gen_db  = gen_db[:db_size]
    ref_db  = ref_db[:db_size]
    print ( "Loaded 2 DataFrames of %d rows from ROOT files" % db_size ) 

    # Input variables
    X_gen = NaNFilter ( np.stack ([gen_db[v] for v in self.in_branches]) ) . T
    X_ref = NaNFilter ( np.stack ([ref_db[v] for v in self.in_branches]) ) . T

    # Prepare noise array to stack to the input
    batch_size, num_feats = X_gen.shape
    noise_input  = np.random.normal (size = (batch_size, noise_size))
    X_gen_scaled = scaler_X . transform (X_gen)

    # Model inference
    gen_input  = np.concatenate ([X_gen_scaled, noise_input], axis = -1)
    gen_input  = tf.convert_to_tensor (gen_input . astype (np.float32))
    gen_output = generator (gen_input) . numpy()

    # Output variables
    Y_gen = scaler_Y . inverse_transform (gen_output)
#    Y_gen = NaNFilter ( np.stack ([gen_db[v] for v in self.out_branches]) ) . T
    Y_ref = NaNFilter ( np.stack ([ref_db[v] for v in self.out_branches]) ) . T

    # Weights variables
    if self.w_branches is not None:
      w_gen = np.c_ [ gen_db[self.w_branches] ]
      w_ref = np.c_ [ ref_db[self.w_branches] ]
    else:
      w_gen = np.ones (X_gen.shape[0])
      w_ref = np.ones (X_ref.shape[0])

    gen_candidates = ( X_gen, Y_gen, w_gen )
    ref_candidates = ( X_ref, Y_ref, w_ref )
    return gen_candidates, ref_candidates