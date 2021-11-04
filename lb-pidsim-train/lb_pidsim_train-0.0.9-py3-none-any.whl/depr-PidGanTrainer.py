import numpy as np
import pandas as pd
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

TF_FLOAT = tf.float32

num_gpu = len (tf.config.list_physical_devices ('GPU'))
gpu_boost = num_gpu > 0

from sklearn.compose             import ColumnTransformer
from sklearn.preprocessing       import MinMaxScaler, StandardScaler, QuantileTransformer, FunctionTransformer
from tensorflow.keras.models     import Sequential
from tensorflow.keras.layers     import InputLayer, Dense
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras            import backend

import os
import sys
import time
import yaml
import pickle
from datetime     import timedelta, datetime
from tqdm         import trange
from html_reports import Report
import matplotlib.pyplot as plt

from .DataChunks import DataChunks
from .algorithms import BceGAN, CramerGAN
from .layers     import AddRandomFeatures
from .utils      import NaNFilter, getModelSummary



class PidGanTrainer:
  """
  PID GAN Trainer
  ===============
  ...
  Attributes
  ----------
    ...
  Methods
  -------
    ...
  """
  def __init__ (
                 self                  ,
                 name                  ,
                 data_files            ,
                 selection             ,
                 X_vars, Y_vars, w_var ,
                 chunk_size  = 100000  ,
                 tree_name   = None    ,
                 export_dir  = None    ,
                 export_name = None    ,
                 report_dir  = None    ,
                 report_name = None    , 
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
    self.name = name
    self.X_vars, self.Y_vars, self.w_var = X_vars, Y_vars, w_var

    self.export_dir  = export_dir
    self.export_name = export_name
    if not os.path.exists (self.export_dir):
      os.makedirs (self.export_dir)

    self.report_dir  = report_dir
    self.report_name = report_name
    if not os.path.exists (self.report_dir):
      os.makedirs (self.report_dir)

    ## Setup for data loading
    self.data_chunk = iter ( DataChunks ( 
                                          file_list   = data_files  ,
                                          tree_name   = tree_name   ,
                                          input_vars  = self.X_vars ,
                                          output_vars = self.Y_vars ,
                                          weight_vars = self.w_var if self.w_var else [] ,
                                          selection   = '&'.join ('({})' . format (s) for s in selection) ,
                                          chunk_size  = chunk_size )
                           )


  ############################
  ##  Build gen-disc players
  ############################
  def build ( 
              self,
              all_hparams ,
              preprocessing        = 'StandardScaler' ,
              gan_algorithm        = 'CramerGAN'      ,
              generator_layers     = [ Dense (256, activation = 'relu', kernel_initializer = 'he_normal') ] ,
              discriminator_layers = [ Dense (256, activation = 'relu', kernel_initializer = 'he_normal') ] ,
            ):
    """
    Build method.
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
    self.hp_dict = all_hparams
    self.dtype = TF_FLOAT

    ## Preprocessing step
    print ('')   # new line
    X, Y, w = self._load_data (dtype = self.dtype)
    if preprocessing == 'MinMaxScaler':
      num_scaler_X = MinMaxScaler()
      num_scaler_Y = MinMaxScaler()
    elif preprocessing == 'StandardScaler':
      num_scaler_X = StandardScaler()
      num_scaler_Y = StandardScaler()
    elif preprocessing == 'QuantileTransformer':
      num_scaler_X = QuantileTransformer (
                                            n_quantiles = 500,
                                            subsample = 10000,
                                            output_distribution = 'normal'
                                          )
      num_scaler_Y = QuantileTransformer (
                                            n_quantiles = 500,
                                            subsample = 10000,
                                            output_distribution = 'normal'
                                          )
    else:
      raise ValueError ("Preprocessing step not implemented.")
    print ("\nData preprocessed through the Scikit-Learn's {}" . format (preprocessing))
    bin_X_vars_idx = list()
    num_X_vars_idx = list()
    for idx, var in enumerate (self.X_vars):
      if (var == "probe_Brunel_trackcharge") or (var == "probe_Brunel_isMuon"):
        bin_X_vars_idx . append (idx)   # indeces of charge and isMuon features
      else:
        num_X_vars_idx . append (idx)   # all the other indeces
    start_time = time.time()
    self.scaler_X = ColumnTransformer ( [
                                        ("num_scaler", num_scaler_X, num_X_vars_idx),
                                        ("bin_scaler", FunctionTransformer(), bin_X_vars_idx)   # identity transformation
                                      ] ) . fit (X)
    self.scaler_Y = num_scaler_Y . fit (Y)
    print ('---> Preprocessing step completed in {:.3f} s\n' . format (time.time() - start_time))

    ## GAN algorithm
    gan_algo = gan_algorithm
    if gan_algo == 'CramerGAN':
      print ('\n\t\t\t+-------------------------+\n\t\t\t|   CramerGAN algorithm   |\n\t\t\t+-------------------------+\n')
    elif gan_algo == 'BceGAN':
      print ('\n\t\t\t+----------------------+\n\t\t\t|   BceGAN algorithm   |\n\t\t\t+----------------------+\n')
    else:
      raise ValueError ('GAN algorithm not implemented.')

    ## Generator model
    generator = Sequential()
    z_dim     = int ( self.hp_dict['latent_space_dim'] )
    generator . add ( AddRandomFeatures (n_normal = z_dim) )   # layer n.0
    for layer in generator_layers:
      generator . add (layer)   # hidden layers
    generator . add ( Dense (Y.shape[1], activation = 'linear', kernel_initializer = 'he_normal') )
    generator . layers[ 1] . _name = 'first_hidden_layer'
    generator . layers[-4] . _name =  'last_hidden_layer'

    ## Discriminator model
    discriminator = Sequential()
    h_dim         = int ( self.hp_dict['critic_func_dim'] )
    for layer in discriminator_layers:
      discriminator . add (layer)   # hidden layers
    if gan_algo == 'CramerGAN':
      discriminator . add ( Dense (h_dim, activation = None, kernel_initializer = 'glorot_uniform') )
    elif gan_algo == 'BceGAN':
      discriminator . add ( Dense (1, activation = 'sigmoid', kernel_initializer = 'he_normal') )
    else:
      raise ValueError ('GAN algorithm not implemented.')
    discriminator . layers[ 0] . _name = 'first_hidden_layer'
    discriminator . layers[-4] . _name =  'last_hidden_layer'

    if gan_algo == 'CramerGAN':
      self.gan = CramerGAN (generator, discriminator)
      self.gan.gp = float ( self.hp_dict['grad_penalty'] )
    elif gan_algo == 'BceGAN':
      self.gan = BceGAN (generator, discriminator)
    else:
      raise ValueError ('GAN algorithm not implemented.')


  ###############
  ##  Load data 
  ###############
  def _load_data (self, dtype):
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
    dataset = next ( self.data_chunk )
    X =  NaNFilter ( np.stack ([dataset[v] for v in self.X_vars]) ) . T
    Y =  NaNFilter ( np.stack ([dataset[v] for v in self.Y_vars]) ) . T
    self.data_rows = len (X)

    if self.w_var is not None:
      w =  np.c_ [ dataset[self.w_var] ]
    else:
      w =  np.ones ( X.shape[0], dtype = dtype )

    X = X.astype ( dtype.as_numpy_dtype )
    Y = Y.astype ( dtype.as_numpy_dtype )
    w = w.astype ( dtype.as_numpy_dtype )
    return X, Y, w


  ########################
  ##  Run training steps
  ########################
  def learn ( 
              self ,
              batch_size    : int = 1000 ,
              num_epochs    : int = 500  ,
              num_checks    : int = 50   ,
              disc_updates  : int = 1    ,
              learning_rate : float = 1e-5 ,
              scheduling_lr : float = None ,
              optimizer     : str = 'RMSprop' ,
            ):
    """
    Learn method.
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
    ## Number of epochs
    num_epochs  = int ( num_epochs )

    ## Batch-size
    if self.gan.name == 'CramerGAN':
      # to take account of input data splitting
      self.batch_size = int ( 2 * batch_size )
    else:
      self.batch_size = int ( batch_size )
    self.disc_updates = disc_updates

    ## Learning rate and scheduling
    lr = float ( self.hp_dict['learning_rate'] )
    if scheduling_lr:
      gen_drop_rate  = float ( self.hp_dict['gen_drop_rate']  )
      disc_drop_rate = float ( self.hp_dict['disc_drop_rate'] )
      ep_lr_sched = max ( 1, int (num_epochs / 50) )
    else:
      pass

    ## Models optimizers
    if optimizer == 'RMSprop':
      rho      = float ( self.hp_dict['opt_param_1'] )
      momentum = float ( self.hp_dict['opt_param_2'] )
      epsilon  = float ( self.hp_dict['opt_epsilon'] )
      self.g_opt = RMSprop ( lr, rho, momentum, epsilon )
      self.d_opt = RMSprop ( lr, rho, momentum, epsilon )
    elif optimizer == 'Adam':
      beta_1   = float ( self.hp_dict['opt_param_1'] )
      beta_2   = float ( self.hp_dict['opt_param_2'] )
      epsilon  = float ( self.hp_dict['opt_epsilon'] )
      self.g_opt = Adam ( lr, beta_1, beta_2, epsilon )
      self.d_opt = Adam ( lr, beta_1, beta_2, epsilon )
    else:
      raise ValueError ("Optimizer not implemented.")

    ## Export frequency
    scan_per_batch = 10   # loss scan per batch
    checkpoint_freq = int (num_epochs / num_checks)

    ## Initial values
    tot_iterations  = 0
    g_loss = d_loss = 0.
    g_lr   = d_lr   = lr
    self.g_lrs = list()
    self.d_lrs = list()
    self.g_weights = [list(), list()]
    self.d_weights = [list(), list()]

    ## Training start
    start_time = time.time()
    for epoch in range (num_epochs):
      print ('\nEpoch {}/{}' . format (epoch + 1, num_epochs))
      print ('-' * 15)

      ## Data loading   
      X, Y, w = self._load_data (dtype = self.dtype)
      # <--- YANDEX --->
      #num_batches = int ( self.data_rows / (self.batch_size * (self.disc_updates + 1)) )
      num_batches = int ( self.data_rows / self.batch_size )
      # < --- >

      batch_step = int (num_batches / scan_per_batch)   # batch step for loss scan
      batch_step = batch_step if batch_step else 1

      self.batch_trange = trange (num_batches, unit = 'batch', file = sys.stdout)
      self.batch_trange.set_description (
          '| g_loss: {:.3f} | d_loss: {:.3f} | g_lr: {:.3e} | d_lr: {:.3e} |' \
          . format (g_loss, d_loss, g_lr, d_lr) )

      self.g_losses  = [0. for i in range (num_batches)]
      self.d_losses  = [0. for i in range (num_batches)]

      ## Data preprocessing
      sX = self.scaler_X . transform (X)
      sY = self.scaler_Y . transform (Y)
      if gpu_boost:
        with tf.device ( '/gpu:0' ):
          sX = tf.cast ( tf.convert_to_tensor (sX) , self.dtype )
          sY = tf.cast ( tf.convert_to_tensor (sY) , self.dtype )
          w  = tf.cast ( tf.convert_to_tensor (w)  , self.dtype )
      else:
        with tf.device ( '/cpu:0' ):
          sX = tf.cast ( tf.convert_to_tensor (sX) , self.dtype )
          sY = tf.cast ( tf.convert_to_tensor (sY) , self.dtype )
          w  = tf.cast ( tf.convert_to_tensor (w)  , self.dtype )

      ## Loop over batches
      for batch in self.batch_trange:
        g_loss, d_loss = self._train_on_batch (sX, sY, w)

        self.g_losses[batch] = g_loss.numpy() 
        self.d_losses[batch] = d_loss.numpy()

        if ((batch + 1) % batch_step) == 0:
          for i, layer in enumerate (['first_hidden_layer', 'last_hidden_layer']):
            g_layer = self.gan.generator.get_layer (layer)
            d_layer = self.gan.discriminator.get_layer (layer)
            self.g_weights[i] . append ( g_layer.weights[0] . numpy() )   # trainable weights
            self.d_weights[i] . append ( d_layer.weights[0] . numpy() )   # trainable weights
      
      self.g_lrs . append ( self.g_opt.learning_rate . numpy() )
      self.d_lrs . append ( self.d_opt.learning_rate . numpy() )

      ## Learning rate scheduling
      if scheduling_lr:
        if (epoch % ep_lr_sched) == 0:
          g_lr = self.g_opt.learning_rate * gen_drop_rate
          d_lr = self.d_opt.learning_rate * disc_drop_rate
          backend.set_value ( self.g_opt.learning_rate, g_lr )
          backend.set_value ( self.d_opt.learning_rate, d_lr )
      else:
        pass

      self._update_report (start_iters = tot_iterations, sample_size = num_batches, num_scans = scan_per_batch)
      tot_iterations += num_batches

      if (epoch + 1) < num_epochs:
        if (epoch + 1) % checkpoint_freq == 0:
          self.input_to_build = self.gan.generator.layers[0] (sX)   # to build the model for exporting
          self._export_model (self.gan.generator, 'checkpoint', epoch + 1)

    train_time = int (time.time() - start_time)
    print ( '\nComplete! Training time: {}\n' . format ( str (timedelta (seconds = train_time)) ) )
    self.input_to_build = self.gan.generator.layers[0] (sX)   # to build the model for exporting
    self._export_model (self.gan.generator, 'final')


  ############################
  ##  Training step on batch
  ############################
  @tf.function
  def _train_on_batch (self, X, Y, w):
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
    for k in tf.range (self.disc_updates):
      x_gen, x_ref, y_ref, w_gen, w_ref = self._trainset_from_data (X, Y, w)
      d_grads = self._compute_grad (x_gen, x_ref, y_ref, w_gen, w_ref, 'discriminator')
      self.d_opt.apply_gradients (zip (d_grads, self.gan.discriminator.trainable_variables))

    x_gen, x_ref, y_ref, w_gen, w_ref = self._trainset_from_data (X, Y, w)
    g_grads = self._compute_grad (x_gen, x_ref, y_ref, w_gen, w_ref, 'generator')
    self.g_opt.apply_gradients (zip (g_grads, self.gan.generator.trainable_variables))

    g_loss = self.gan.generator_loss     (x_gen, x_ref, y_ref, w_gen, w_ref, training = False) 
    d_loss = self.gan.discriminator_loss (x_gen, x_ref, y_ref, w_gen, w_ref, training = False) 
    return g_loss, d_loss


  #################################
  ##  Extract trainset from chunk
  #################################
  @tf.function ( input_signature = ( 
                 tf.TensorSpec (shape = [None, None], dtype = TF_FLOAT),
                 tf.TensorSpec (shape = [None, None], dtype = TF_FLOAT),
                 tf.TensorSpec (shape = [None, None], dtype = TF_FLOAT), ) )
  def _trainset_from_data (self, X, Y, w):
    """
    Internal method.
    Method to extract a batchsize from the data-chunck.
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
    id_gen = tf.random.uniform ( (self.batch_size,1), 0, len(X), tf.dtypes.int32 )
    id_ref = tf.random.uniform ( (self.batch_size,1), 0, len(X), tf.dtypes.int32 )
   
    X_gen = tf.gather_nd ( X, id_gen )
    X_ref = tf.gather_nd ( X, id_ref )
    Y_ref = tf.gather_nd ( Y, id_ref )
    w_gen = tf.gather_nd ( w, id_gen )
    w_ref = tf.gather_nd ( w, id_ref )
    return X_gen, X_ref, Y_ref, w_gen, w_ref


  ##########################
  ## Compute loss gradient
  ##########################
  def _compute_grad (self, x_gen, x_ref, y_ref, w_gen, w_ref, which_grad):
    """
    Internal method.
    Method to compute gradients.
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
    if which_grad == 'generator':
      with tf.GradientTape() as tape:
        loss = self.gan.generator_loss (x_gen, x_ref, y_ref, w_gen, w_ref, training = True)
      model = self.gan.generator

    if which_grad == 'discriminator':
      with tf.GradientTape() as tape:
        loss = self.gan.discriminator_loss (x_gen, x_ref, y_ref, w_gen, w_ref, training = True)
      model = self.gan.discriminator  
    
    return tape.gradient (loss, model.trainable_variables)


  ##########################
  ##  Export trained model
  ##########################
  def _export_model (self, model, label = None, epoch = None):
    """
    Internal method.
    Method to export the trained model.
    Parameters
    ----------
      ...
    Attributes
    ----------
      None
    Returns
    -------
      None
    """
    exp_model = Sequential()
    for layer in model.layers[1:]:    # to avoid adding custom objects
      exp_model . add (layer)
    exp_model (self.input_to_build)   # to build the computational graph

    if self.export_dir is None:
      print ('Warning! No model will be saved because `export_dir` is not defined.')
    try:
      timestamp = str (datetime.now()) . split ('.') [0]
      timestamp = timestamp . replace (':','_') . replace (' ','_')
      modelname = self.export_name or '{}_{}' . format (self.gan.name, timestamp)
      dirname = '{}/{}/{}' . format (self.export_dir, modelname, modelname)
      if label is not None: dirname += '_{}' . format (label)
      if epoch is not None: dirname += '_ep{:04d}' . format (epoch)

      if not os.path.exists (dirname):
        os.makedirs (dirname)

      scalerXname = '{}/transform_X.pkl' . format (dirname)
      scalerYname = '{}/transform_Y.pkl' . format (dirname)
      pickle . dump (self.scaler_X, open (scalerXname, 'wb'))
      pickle . dump (self.scaler_Y, open (scalerYname, 'wb'))

      exp_model . save (dirname + '/saved_model')
      with open (dirname + '/hyperparams.yaml', 'w') as file:
        exp_hp = yaml.dump (self.hp_dict, file)
      print ('Model exported to {}' . format (dirname))
    except:
      print ('Warning! Some problems with model export have occurred.')


  ########################
  ##  Update HTML report
  ########################
  def _update_report (self, start_iters, sample_size, num_scans):
    """
    Internal method.
    Method to update the report.
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
    rep = Report()

    if self.report_dir is None:
      print ('Warning! No report will be produced because `report_dir` is not defined')
    if self.report_name is None:
      self.report_name = "training_" + self.name

    ## Print hyperparameters on the report
    rep.add_markdown ('# Hyperparameters List')
    for key, val in self.hp_dict.items():
      rep.add_markdown ('**{}:** {}' . format (key, val))

    ## Print generator architecture on the report
    rep.add_markdown ('# Generator Architecture')
    gen_model_summary, gen_num_params = getModelSummary (self.gan.generator)
    rep.add_markdown (gen_model_summary)
    rep.add_markdown ('**Total parameters:** {}' . format (gen_num_params))

    ## Print discriminator architecture on the report
    rep.add_markdown ('# Discriminator Architecture')
    disc_model_summary, disc_num_params = getModelSummary (self.gan.discriminator)
    rep.add_markdown (disc_model_summary)
    rep.add_markdown ('**Total parameters:** {}' . format (disc_num_params))

    ## Training plots
    rep.add_markdown ('# Training Plots')

    ## Loss values database
    if not hasattr (self, 'loss_db'):
      self.loss_db = pd.DataFrame ( columns = ['gen' , 'gen_err' ,
                                               'disc', 'disc_err'] )

    scan_step = int (sample_size / num_scans)
    scan_step = scan_step if scan_step else 1

    for scan in range (num_scans):
      id_  = start_iters + (scan + 1) * scan_step
      low  = scan * scan_step
      high = (scan + 1) * scan_step
      self.loss_db.loc [id_] = (
                                 np.mean ( self.g_losses [low:high] ),
                                 np.std  ( self.g_losses [low:high] ),
                                 np.mean ( self.d_losses [low:high] ),
                                 np.std  ( self.d_losses [low:high] ),
                               )

    iterations = self.loss_db.index . to_numpy()
    flashback  = max ( 100, int (iterations.size / 2) )

    ## Loss report: min-max definition
    min_loss  = min ( min (self.loss_db['gen'][-flashback:] - \
                           self.loss_db['gen_err'][-flashback:] / 2.),
                      min (self.loss_db['disc'][-flashback:] - \
                           self.loss_db['disc_err'][-flashback:] / 2.) )
    min_loss -= max ( max (self.loss_db['gen_err'][-flashback:] / 2.),
                      max (self.loss_db['disc_err'][-flashback:] / 2.) )
    max_loss  = max ( max (self.loss_db['gen'][-flashback:] + \
                           self.loss_db['gen_err'][-flashback:] / 2.),
                      max (self.loss_db['disc'][-flashback:] + \
                           self.loss_db['disc_err'][-flashback:] / 2.) )
    max_loss += max ( max (self.loss_db['gen_err'][-flashback:] / 2.), 
                      max (self.loss_db['disc_err'][-flashback:] / 2.) )

    ## Loss report: plot setup
    plt.figure (figsize = (8,5))
    plt.title  ('Learning curves', fontsize = 14)
    plt.xlabel ('Training iterations', fontsize = 12)
    plt.ylabel (self.gan.loss_name, fontsize = 12)
    plt.grid (alpha = 0.5)

    plt.plot ( iterations, self.loss_db['gen'], color = 'deeppink', lw = 0.5, label = 'generator' )
    plt.fill_between ( iterations, 
                       self.loss_db['gen'] - self.loss_db['gen_err'] / 2.,
                       self.loss_db['gen'] + self.loss_db['gen_err'] / 2.,
                       color = 'deeppink', alpha = 0.2 )

    plt.plot ( iterations, self.loss_db['disc'], color = 'royalblue', lw = 0.5, label = 'discriminator' )
    plt.fill_between ( iterations, 
                       self.loss_db['disc'] - self.loss_db['disc_err'] / 2.,
                       self.loss_db['disc'] + self.loss_db['disc_err'] / 2.,
                       color = 'royalblue', alpha = 0.2 )

    plt.legend (title = 'Training players', loc = 'upper left', fontsize = 10)
    plt.axis ([0, iterations[-1], min_loss, max_loss])

    rep.add_figure(); plt.clf(); plt.close()

    ## Learning rate report: plot setup
    plt.figure (figsize = (8,5))
    plt.title  ('Learning rate scheduling', fontsize = 14)
    plt.xlabel ('Training epochs', fontsize = 12)
    plt.ylabel ('Learning rate', fontsize = 12)
    plt.grid (alpha = 0.5)

    plt.plot ( np.arange (len(self.g_lrs) + 1)[1:], np.array (self.g_lrs),
               color = 'deeppink' , lw = 1, label = 'generator' )
    plt.plot ( np.arange (len(self.d_lrs) + 1)[1:], np.array (self.d_lrs), 
               color = 'royalblue', lw = 1, label = 'discriminator' )

    plt.legend (title = 'Training players', loc = 'upper left', fontsize = 10)
    plt.xlim (0, len(self.g_lrs))

    rep.add_figure(); plt.clf(); plt.close()
    rep.add_markdown ('<br/>')
    
    ## Weights values database
    if not hasattr (self, 'weights_db'):
      self.weights_db = pd.DataFrame ( columns = ['gen_mse_1st' , 'gen_mse_last' ,
                                                  'disc_mse_1st', 'disc_mse_last'] )

    for scan in range (num_scans):
      start = (len(self.g_lrs) - 1) * num_scans
      new_w_gen_1st   = self.g_weights[0][start + scan] . flatten()
      new_w_gen_last  = self.g_weights[1][start + scan] . flatten()
      new_w_disc_1st  = self.d_weights[0][start + scan] . flatten()
      new_w_disc_last = self.d_weights[1][start + scan] . flatten()

      if start == 0 and scan == 0:
        old_w_gen_1st   = 0.
        old_w_gen_last  = 0.
        old_w_disc_1st  = 0.
        old_w_disc_last = 0.
      else:
        old_w_gen_1st   = self.g_weights[0][start + scan - 1] . flatten()
        old_w_gen_last  = self.g_weights[1][start + scan - 1] . flatten()
        old_w_disc_1st  = self.d_weights[0][start + scan - 1] . flatten()
        old_w_disc_last = self.d_weights[1][start + scan - 1] . flatten()
          
      id_ = start_iters + (scan + 1) * scan_step
      self.weights_db.loc [id_] = (
                 np.sum ( np.square ( new_w_gen_1st   - old_w_gen_1st   ) ),
                 np.sum ( np.square ( new_w_gen_last  - old_w_gen_last  ) ),
                 np.sum ( np.square ( new_w_disc_1st  - old_w_disc_1st  ) ),
                 np.sum ( np.square ( new_w_disc_last - old_w_disc_last ) )
                                  )

    ## Generator weights report: min-max definition
    min_mse  = min ( min (self.weights_db['gen_mse_1st'][-flashback:]), 
                     min (self.weights_db['gen_mse_last'][-flashback:]) )
    min_mse /= 10
    max_mse  = max ( max (self.weights_db['gen_mse_1st'][-flashback:]), 
                     max (self.weights_db['gen_mse_last'][-flashback:]) )
    max_mse *= 10

    ## Generator weights report: plot setup
    plt.figure (figsize = (8,5))
    plt.title  ('Generator weights', fontsize = 14)
    plt.xlabel ('Training iterations', fontsize = 12)
    plt.ylabel ('Weights update', fontsize= 12)
    plt.grid (alpha = 0.5)
    plt.plot ( iterations, self.weights_db['gen_mse_1st'],
               color = 'black', lw = 0.5, label = 'first_hidden_layer' )
    plt.plot ( iterations, self.weights_db['gen_mse_last'],
               color = 'red'  , lw = 0.5, label = 'last_hidden_layer' )
    plt.legend (loc = 'upper right', fontsize = 10)
    plt.axis ([0, iterations[-1], min_mse, max_mse])
    plt.yscale ('log')

    rep.add_figure(); plt.clf(); plt.close()

    ## Discriminator weights report: min-max definition
    min_mse  = min ( min (self.weights_db['disc_mse_1st'][-flashback:]), 
                     min (self.weights_db['disc_mse_last'][-flashback:]) )
    min_mse /= 10
    max_mse  = max ( max (self.weights_db['disc_mse_1st'][-flashback:]), 
                     max (self.weights_db['disc_mse_last'][-flashback:]) )
    max_mse *= 10

    ## Discriminator weights report: plot setup
    plt.figure (figsize = (8,5))
    plt.title  ('Discriminator weights', fontsize = 14)
    plt.xlabel ('Training iterations', fontsize = 12)
    plt.ylabel ('Weights update', fontsize= 12)
    plt.grid (alpha = 0.5)
    plt.plot ( iterations, self.weights_db['disc_mse_1st'],
               color = 'black', lw = 0.5, label = 'first_hidden_layer' )
    plt.plot ( iterations, self.weights_db['disc_mse_last'],
               color = 'red'  , lw = 0.5, label = 'last_hidden_layer' )
    plt.legend (loc = 'upper right', fontsize = 10)
    plt.axis ([0, iterations[-1], min_mse, max_mse])
    plt.yscale ('log')

    rep.add_figure(); plt.clf(); plt.close()
    rep.add_markdown ('<br/>')
    

    rep.write_report (filename = '{}/{}.html' . format (self.report_dir, self.report_name))



if __name__ == '__main__':
  print (PidGanTrainer.__doc__)