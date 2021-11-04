import numpy as np
import pandas as pd
import tensorflow as tf
#tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from sklearn.tree     import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier

import os
import io
import time
import yaml
import pickle
import requests
import multiprocessing as mp
import matplotlib.pyplot as plt
from html_reports import Report

from .DataChunks import DataChunks
from .utils      import predictClassProbas



class BdtClassifier:
  """
  BDT Classifier
  ==============
  ...
  Attributes
  ----------
    ...
  Methods
  -------
    ...
  """
  def __init__ ( 
                 self                   ,
                 data_files             ,
                 selection              ,
                 X_vars, Y_vars, w_var  ,
                 chunk_size  = int(5e5) ,
                 tree_name   = None     ,
                 model_dir   = None     ,
                 model_name  = None     ,
                 num_epochs  = None     ,
                 num_checks  = None     ,
                 export_dir  = None     ,
                 export_name = None     ,
                 report_dir  = None     ,
                 report_name = None     ,
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
    ## Setup for data loading
    self.data_chunk = DataChunks ( file_list   = data_files ,
                                   tree_name   = tree_name  ,
                                   input_vars  = X_vars     ,
                                   output_vars = Y_vars     ,
                                   weight_vars = w_var if w_var else [] ,
                                   selection   = '&'.join ('({})'.format(s) for s in selection) ,
                                   chunk_size  = chunk_size )

    ## Setup for model loading
    self.model_dir = model_dir
    if self.model_dir is None:
      raise AttributeError ('No model will be loaded because `model_dir` is not defined.')

    self.model_name = model_name
    if self.model_name is None:
      raise AttributeError ('No model will be loaded because `model_name` is not defined.')
    
    if num_epochs is None:
      self.ep_step = None
      self.model_list = [self.model_name + '_final']
    else:
      self.ep_step = int (num_epochs / num_checks)
      self.model_list = [ '{}_checkpoint_ep{:04d}' . format (self.model_name, self.ep_step * i) \
                          for i in range (1, num_checks) ]
      self.model_list . append (self.model_name + '_final')

    self.export_dir  = '{}/{}' . format (export_dir, self.model_name)
    self.export_name = export_name
    if not os.path.exists (self.export_dir):
      os.makedirs (self.export_dir)

    self.report_dir  = '{}/{}' . format (report_dir, self.model_name)
    self.report_name = report_name 
    if not os.path.exists (self.report_dir):
      os.makedirs (self.report_dir)


  ########################
  ##  Run training steps
  ########################
  def learn ( 
              self                        ,
              num_bdt                     ,
              train_ratio   = 0.7         ,
              n_estimators  = 500         ,
              learning_rate = 0.5         ,
              max_leaves    = 14          ,
              max_depth     = 5           ,
              trial_id      = None        ,
              send_training_score = False ,
            ):
    """
    Training method.
    ...
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
    self.n_estimators  = n_estimators
    self.learning_rate = learning_rate
    self.max_leaves    = max_leaves
    self.max_depth     = max_depth

    ## Build classifier
    clf = GradientBoostingClassifier (
              learning_rate = self.learning_rate ,
              n_estimators = self.n_estimators   ,
              criterion = 'friedman_mse'         ,
              max_leaf_nodes = self.max_leaves   ,
              max_depth = self.max_depth         ,
              random_state = 42                  )

    epochs   = list()
    KSD_vals = list()
    KSD_errs = list()
    strong_clf_list = list()
    for k, checkpoint in enumerate (self.model_list):
      print ('\nModel {}/{}' . format (k + 1, len (self.model_list)))
      print ('-' * 15)

      dir_name  = '{}/{}/{}' . format (self.model_dir, self.model_name, checkpoint)

      ## Recover preprocessing transformation
      scalerXname = '{}/transform_X.pkl' . format (dir_name)
      scalerYname = '{}/transform_Y.pkl' . format (dir_name)
      scaler_X = pickle.load ( open (scalerXname, 'rb') )
      scaler_Y = pickle.load ( open (scalerYname, 'rb') )
      scalers  = ( scaler_X, scaler_Y )

      ## Recover latent space dimension
      with open (dir_name + '/hyperparams.yaml') as file:
        hyperparams = yaml.full_load (file)
      noise_size  = hyperparams ['latent_space_dim']

      ## Load the generator model
      generator = tf.keras.models.load_model (dir_name + '/saved_model')

      dsets, labels, weights = self.data_chunk.getClassDatasets (
                                     preprocessing = scalers    ,
                                     noise_size    = noise_size , 
                                     generator     = generator  ,
                                     num_datasets  = num_bdt    ,
                                   )
      print ('Model correctly loaded from {}/{}' . format (self.model_dir, checkpoint))
      
      multi_attributes = [ (clf, dsets[i], labels[i], weights[i], train_ratio) for i in range (num_bdt) ]

      ## Start multi-thread training
      print ('\n**************** Multi-thread training ****************')
      with mp.Pool (processes = num_bdt) as pool:
        results = pool.starmap (predictClassProbas, multi_attributes)
      print ('*' * 55, '\n')

      list_bdt_clf  = list()
      list_df_train = list()
      list_df_test  = list()
      accuracy_train, recall_train = list(), list()
      accuracy_test , recall_test  = list(), list()
      for i in range (num_bdt):
        list_bdt_clf   . append (results[i][0])   # list of trained classifiers
        list_df_train  . append (results[i][1])   # list of dataframes
        list_df_test   . append (results[i][2])   # list of dataframes
        accuracy_train . append (results[i][3])   # list of numbers
        accuracy_test  . append (results[i][4])   # list of numbers
        recall_train   . append (results[i][5])   # list of numbers
        recall_test    . append (results[i][6])   # list of numbers

      print ( 'Accuracy : {:.3f} +/- {:.3f} ({:.3f} +/- {:.3f})' . format ( np.mean (accuracy_test) , np.std (accuracy_test)  ,
                                                                            np.mean (accuracy_train), np.std (accuracy_train) ) )
      print ( 'Recall   : {:.3f} +/- {:.3f} ({:.3f} +/- {:.3f})' . format ( np.mean (recall_test)   , np.std (recall_test)    ,
                                                                            np.mean (recall_train)  , np.std (recall_train)   ) )
      
      KSD_mean, KSD_std, id_KSD_max = self._class_result (checkpoint, list_df_train, list_df_test)

      if self.ep_step is None:
        epochs . append ( None )
      else:
        epochs . append ( self.ep_step * (k + 1) )
      KSD_vals . append ( KSD_mean )
      KSD_errs . append ( KSD_std  )
      strong_clf_list . append ( list_bdt_clf [id_KSD_max] )

    best_model_id = np.argmin (KSD_vals)                # model with the best KS-test
    best_model_name = self.model_list [best_model_id]   # name of the best model
    best_score    = KSD_vals [best_model_id]            # best KS-test score
    best_bdt      = strong_clf_list [best_model_id]     # BDT of the best model
  
    exp_dict = {
                 'model_name' : best_model_name ,
                 'score_val'  : best_score      ,
                 'clf_model'  : best_bdt
               } 

    ## Send the training score to the Optuna-server
    if send_training_score:
      if trial_id is None:
        raise ValueError ('To send the training score to the OptunAPI server you should provide a valid trial number!')
      std_model_name = '_' . join ( self.model_name . split ('_') [:-1] )

      HOST = 'http://193.206.190.136:9000'   # move to connection config file
      path_req = HOST + '/optunapi/score/{}' . format (std_model_name)
      http_req = requests.get (path_req + '?trial_id={}&score={}' . format (trial_id, best_score))
      
      print ('Training score correctly sent to the Optuna-server ({})' . format (http_req))

    ## Export the classification result
    exp_bdt_file = '{}/clf_info.pkl' . format (self.export_dir)
    pickle.dump ( exp_dict, open (exp_bdt_file, 'wb') ) 

    exp_score_file = '{}/scores.npz' . format (self.export_dir)
    np.savez ( 
               exp_score_file                 ,
               epochs = np.array (epochs)     ,
               KSD_vals = np.array (KSD_vals) ,
               KSD_errs = np.array (KSD_errs) ,
             )

    print ( '\nClassification output correctly exported to {}\n' . format (self.export_dir) )


  ##################################
  ##  Report classification result
  ##################################
  def _class_result (self, model_name, list_df_train, list_df_test, flatten = False):
    """
    Internal method.
    ...
    Parameters
    ----------
      ...
    Attributes
    ----------
      ...
    Returns
    -------
      ...
    """
    rep = Report()

    if self.report_dir is None:
      print ('Warning! No report will be produced because `report_dir` is not defined')
    report_name = 'classification_' + model_name

    ## Print hyperparameters on the report
    rep.add_markdown ( '# Hyperparameters List' )
    rep.add_markdown ( '**Learning rate:** {}'      . format (self.learning_rate) )
    rep.add_markdown ( '**Number of trees:** {}'    . format (self.n_estimators)  )
    rep.add_markdown ( '**Maximum tree depth:** {}' . format (self.max_depth)     )
    rep.add_markdown ( '**Maximum number of leaf nodes:** {}' . format (self.max_leaves) )

    ## Classification plots
    rep.add_markdown ('# BDT Result Plots')

    KSD_test_list  = list()
    KSD_train_list = list()
    for df_train, df_test in zip (list_df_train, list_df_test):
      df_test_gen  = df_test  [ df_test ['true_label'] == True  ]   # true label: gen
      df_test_ref  = df_test  [ df_test ['true_label'] == False ]   # true label: ref
      df_train_gen = df_train [ df_train['true_label'] == True  ]   # true label: gen
      df_train_ref = df_train [ df_train['true_label'] == False ]   # true label: ref

      if flatten:
        rnd_1 = np.random.normal ( 0, 1e-6, len (df_test_gen ['proba']) )
        rnd_2 = np.random.normal ( 0, 1e-6, len (df_test_ref ['proba']) )
        rnd_3 = np.random.normal ( 0, 1e-6, len (df_train_gen['proba']) )
        rnd_4 = np.random.normal ( 0, 1e-6, len (df_train_ref['proba']) )

        ## Compute quantile of class probability distribution
        y = np.linspace ( 0, 1, 5000 )
        q = np.quantile ( df_test_ref['proba'] + rnd_2, y )

        ## Flatten distributions (with respect to reference) for p_gen
        proba_test_gen  = np.interp (df_test_gen ['proba'] + rnd_1, q, y)
        proba_test_ref  = np.interp (df_test_ref ['proba'] + rnd_2, q, y)
        proba_train_gen = np.interp (df_train_gen['proba'] + rnd_3, q, y)
        proba_train_ref = np.interp (df_train_ref['proba'] + rnd_4, q, y)
      
      else:
        ## No-flatten distributions for p_gen
        proba_test_gen  = df_test_gen ['proba']
        proba_test_ref  = df_test_ref ['proba']
        proba_train_gen = df_train_gen['proba']
        proba_train_ref = df_train_ref['proba']

      ## Prepare Kolmogorov-Smirnov test
      bins = 100
      p_test_ref_entries, _  = np.histogram ( proba_test_ref,
                                              bins = bins, range = [0, 1],
                                              weights = df_test_ref  ['weight'] )
      p_test_gen_entries, _  = np.histogram ( proba_test_gen,
                                              bins = bins, range = [0, 1],
                                              weights = df_test_gen  ['weight'] )
      p_train_ref_entries, _ = np.histogram ( proba_train_ref,
                                              bins = bins, range = [0, 1],
                                              weights = df_train_ref ['weight'] )
      p_train_gen_entries, _ = np.histogram ( proba_train_gen,
                                              bins = bins, range = [0, 1],
                                              weights = df_train_gen ['weight'] )

      ## Compute Kolmogorov-Smirnov distance
      entries_test  = { "ref" : p_test_ref_entries  , "gen" : p_test_gen_entries  }
      entries_train = { "ref" : p_train_ref_entries , "gen" : p_train_gen_entries }
      for entries, KSD in zip ( (entries_test, entries_train), (KSD_test_list, KSD_train_list) ):
        R_proba  = np.cumsum (entries["ref"])
        R_proba /= R_proba[-1]   # normalized cumulative
        G_proba  = np.cumsum (entries["gen"])
        G_proba /= G_proba[-1]   # normalized cumulative
        KSD . append ( np.absolute (R_proba - G_proba) . max() )

      ## Class probability distributions plot
      plt.figure (figsize = (8,5))
      plt.title  ('Class probability distributions', fontsize = 14)
      plt.xlabel ("Class probability for 'gen' label", fontsize = 12)
      plt.ylabel ('Entries', fontsize = 12)

      ## Normalized weights
      w_test_gen  = df_test_gen  ['weight'] / len (df_test_gen  ['weight'])
      w_test_ref  = df_test_ref  ['weight'] / len (df_test_ref  ['weight'])
      w_train_gen = df_train_gen ['weight'] / len (df_train_gen ['weight'])
      w_train_ref = df_train_ref ['weight'] / len (df_train_ref ['weight'])

      ## Plot normalized histograms
      h_test_ref  = plt.hist (proba_test_ref , bins = bins, range = [0, 1], weights = w_test_ref,
                              color = 'royalblue', alpha = 0.5, label = 'Reference test-set')
#      h_train_ref = plt.hist (proba_train_ref, bins = bins, range = [0, 1], weights = w_train_ref,
#                              color = 'royalblue', histtype = 'step', label = 'Reference train-set')
      h_test_gen  = plt.hist (proba_test_gen , bins = bins, range = [0, 1], weights = w_test_gen,
                              color = 'deeppink' , alpha = 0.5, label = 'Generated test-set')
      h_train_gen = plt.hist (proba_train_gen, bins = bins, range = [0, 1], weights = w_train_gen,
                              color = 'deeppink' , histtype = 'step', label = 'Generated train-set')

      y_max  = max ( max (h_test_ref[0]), max (h_test_gen[0]), max (h_train_gen[0]) )
      y_max += 0.1 * y_max

      plt.legend (loc = 'upper left', fontsize = 10)
      plt.text (0.07, 0.70 * y_max, 'K-S test: %.3lf' % (KSD_test_list[-1]), fontsize = 12)
      plt.axis ([0., 1., 0., y_max])

      rep.add_figure(); plt.close()

    rep.write_report (filename = '{}/{}.html' . format (self.report_dir, report_name))

    ## Compute average on KS-distances
    KSD_mean_test  = np.mean ( KSD_test_list  )
    KSD_mean_train = np.mean ( KSD_train_list )
    KSD_std_test  = np.std ( KSD_test_list  )
    KSD_std_train = np.std ( KSD_train_list )
    print ( 'K-S test : {:.3f} +/- {:.3f} ({:.3f} +/- {:.3f})' . format ( KSD_mean_test  , KSD_std_test  , 
                                                                          KSD_mean_train , KSD_std_train ) )

    id_KSD_max = np.argmax ( KSD_test_list  )   # index of the BDT with the highest KS-test

    return KSD_mean_test, KSD_std_test, id_KSD_max



if __name__ == '__main__':
  print (BdtClassifier.__doc__)