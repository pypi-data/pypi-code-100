# -*- coding: utf-8 -*-
"""
Created on June 18 06:54:04 2021
GUI routine for Laue neural network training and prediction

@author: Ravi raj purohit PURUSHOTTAM RAJ PUROHIT (purushot@esrf.fr)
@guide: jean-Sebastien MICHA (micha@esrf.fr)

Lattice and symmetry routines are extracted and modified from the PYMICRO repository

TODO:
    1. Include an exhaustive list of space groups and their forbidden reflections
    2. HDF5 file format output instead of pickle
    3. Notebook to post process the results (choice of bin width, data selectivity, etc...)
"""
import pkg_resources  # part of setuptools
version_package = pkg_resources.require("lauetoolsnn")[0].version

frame_title = "Laue Neural-Network model- v2 @Ravi @Jean-Sebastien \n@author: Ravi raj purohit PURUSHOTTAM RAJ PUROHIT (purushot@esrf.fr) \n@guide: Jean-Sebastien MICHA (micha@esrf.fr)"

import warnings
warnings.filterwarnings('ignore')
import logging
logger = logging.getLogger()
old_level = logger.level
logger.setLevel(100)

import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rcParams.update({'font.size': 14})
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
import os
import collections
import random, itertools
import re
import glob
import _pickle as cPickle
from random import random as rand1
from math import acos
import time, datetime
import sys
import inspect
import threading
import multiprocessing as multip
from multiprocessing import Process, Queue, cpu_count
import enum
import functools
import math
from numpy import pi, dot, radians
import ast, configparser
import scipy
from scipy.spatial.transform import Rotation as R
# from functools import partial
from sklearn.metrics import classification_report

# =============================================================================
# Additonal networkx module
import networkx as nx
# =============================================================================

from PyQt5 import QtCore#, QtGui
from PyQt5.QtCore import QSettings
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,\
                            QPushButton, QWidget, QFormLayout, \
                            QToolBar, QStatusBar, \
                            QVBoxLayout, QTextEdit, QProgressBar, \
                            QComboBox, QLineEdit, QFileDialog

## LaueTools import
import LaueTools.dict_LaueTools as dictLT
import LaueTools.IOLaueTools as IOLT
import LaueTools.generaltools as GT
import LaueTools.CrystalParameters as CP
import LaueTools.lauecore as LT
import LaueTools.LaueGeometry as Lgeo
import LaueTools.readmccd as RMCCD
import LaueTools.FitOrient as FitO
import LaueTools.findorient as FindO
from LaueTools.matchingrate import Angular_residues_np

## for faster binning of histogram
## C version of hist
from fast_histogram import histogram1d
import h5py

## Keras import
tensorflow_keras = True
try:
    import tensorflow as tf
    from tensorflow.keras.callbacks import Callback
    import keras
    from keras.models import model_from_json
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Dropout
    from tensorflow.keras.utils import to_categorical
    from keras.callbacks import EarlyStopping, ModelCheckpoint
    from keras.regularizers import l2
    # from tf.keras.layers.normalization import BatchNormalization
except:
    tensorflow_keras = False

## GPU Nvidia drivers needs to be installed! Ughh
## if wish to use only CPU set the value to -1 else set it to 0 for GPU
## CPU training is suggested (as the model requires more RAM)
try:
    # Disable all GPUS
    tf.config.set_visible_devices([], 'GPU')
    visible_devices = tf.config.get_visible_devices()
    for device in visible_devices:
        assert device.device_type != 'GPU'
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

Logo = resource_path("lauetoolsnn_logo.png")

CST_ENERGYKEV = 12.398

default_initialization = True
if default_initialization:
    material_global = "Cu" ## same key as used in LaueTools
    material1_global = "Si" ## same key as used in LaueTools
    symmetry_global = "cubic"
    symmetry1_global = "cubic"
    prefix_global = ""
    detectorparameters_global = [79.583,976.202,931.883,0.4411,0.3921]
    pixelsize_global = 0.0734 # 0.079142 #
    ccd_label_global = "sCMOS" #"MARCCD165" #"Cor"#
    dim1_global = 2018 #2048 #
    dim2_global = 2016 #2048 #
    emax_global = 23
    emin_global = 5
    UB_matrix_global = 5
    image_grid_globalx = 21
    image_grid_globaly = 51
    intensity_threshold_global = 80 #75 800
    boxsize_global = 8
    fit_peaks_gaussian_global = 1
    FitPixelDev_global = 20
    strain_label_global = "NO" ## compute and plot strains
    tolerance_strain = [0.35,0.25,0.15]   ## reduced tolerance for strain calculations
    tolerance_strain1 = [0.35,0.25,0.15]
    hkls_list_global = "[1,1,0],[1,0,0],[1,1,1]"#,[3,1,0],[5,2,9],[7,5,7],[7,5,9]"
    ##exp directory
    if material_global == material1_global:
        fn1 = material_global + prefix_global
    else:
        fn1 = material_global + "_" + material1_global + prefix_global
    expfile_global = r"C:\Users\purushot\Desktop\Tungsten_olivier_data\d0-300MPa"
    exp_prefix_global = "Wmap_WB_13sep_d0_300MPa_" #"nw2_" #None #"roi3_" #
    modelfile_global = r"C:\Users\purushot\Desktop\pattern_matching\experimental\GUIv0\latest_version" + "//" + fn1
    if material_global == material1_global:
        fn1 = material_global
        if exp_prefix_global == None:
            exp_prefix_global = material_global + "_"
        weightfile_global = modelfile_global + "//" + "model_" + material_global + ".h5"
    else:
        fn1  = material_global + "_" + material1_global
        if exp_prefix_global == None:
            exp_prefix_global = material_global + "_"+material1_global + "_"
        weightfile_global = modelfile_global + "//" + "model_" + material_global + "_" + material1_global + ".h5"
    main_directory = os.getcwd()
    hkl_max_global = 6
    elements_global = "all"
    freq_rmv_global = 100
    hkl_max1_global = 6
    elements1_global = "all"
    freq_rmv1_global = 100
    maximum_angle_to_search_global = 90
    step_for_binning_global = 0.1
    nb_grains_per_lp_global = 5
    nb_grains_per_lp1_global = 5
    grains_nb_simulate_global = 500
    include_scm_global = False
    batch_size_global = 50
    epochs_global = 5
    tolerance_global = 0.7
    tolerance_global1 = 0.7
    model_weight_file = None
    softmax_threshold_global = 0.80 # softmax_threshold
    mr_threshold_global = 0.95 # match rate threshold
    cap_matchrate = 0.01 * 100 ## any UB matrix providing MR less than this will be ignored
    coeff = 0.3 ## should be same as cap_matchrate or no?
    coeff_overlap1212 = 0.3
    NumberMaxofFits = 3000 ### Max peaks per LP
    mode_spotCycle = "graphmode" ## slow: to cycle through all spots else: cycles through smartly selected pair of spots
    material0_limit1212 = 100000
    material1_limit1212 = 100000
    use_previous_UBmatrix = False
    write_mtex_file = True
    material0_lauegroup = 11
    material1_lauegroup = 11
    misorientation_angle1 = 1

GUI_START_TIME = time.time() #in ms
metricsNN = [
            keras.metrics.FalseNegatives(name="fn"),
            keras.metrics.FalsePositives(name="fp"),
            keras.metrics.TrueNegatives(name="tn"),
            keras.metrics.TruePositives(name="tp"),
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="accuracy"),
            ]
ACCEPTABLE_FORMATS = [".npz"]
gui_state = np.random.randint(1e6)
#%% Main module
class Window(QMainWindow):
    """Main Window."""
    def __init__(self, winx=None, winy=None):
        """Initializer."""
        super(Window, self).__init__()
        # QMainWindow.__init__(self)

        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        if winx==None or winy==None:
            self.setFixedSize(16777215,16777215)
        else:
            self.setFixedSize(winx, winy)
        
        self.setWindowTitle("Laue Neural-Network v2")
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        
        ## init variables
        self.input_params = {}
        self.factor = 5 ## fixed for 20% validation dataset generation
        self.state = 0
        self.state1 = 0
        self.state2 = 0
        self.model = None
        
        
        self.mode_spotCycleglobal = mode_spotCycle
        self.softmax_threshold_global = softmax_threshold_global
        self.mr_threshold_global = mr_threshold_global
        self.cap_matchrate = cap_matchrate
        self.coeff = coeff
        self.coeff_overlap = coeff_overlap1212
        self.fit_peaks_gaussian_global = fit_peaks_gaussian_global
        self.FitPixelDev_global = FitPixelDev_global
        self.NumberMaxofFits = NumberMaxofFits
        self.tolerance_strain = tolerance_strain
        self.tolerance_strain1 = tolerance_strain1
        self.misorientation_angle = misorientation_angle1

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.layout)
        self._createDisplay() ## display screen
        self.setDisplayText("Lauetoolsnn v"+ str(version_package))
        self.setDisplayText(frame_title)
        self.setDisplayText("Uses base libraries of LaueTools (micha@esrf.fr) to simulate Laue patterns for a given detector geometry \nFollows convention of BM32 beamline at ESRF")
        self.setDisplayText("Polefigure and IPF plot modules are taken and modified from PYMICRO repository")
        self.setDisplayText("This version supports multiprocessing \nGUI initialized! \nLog will be printed here \nPlease Train a model first, if not already done.\n")
        self.setDisplayText("New materials and extinction rules can be set in LaueTools DictLP file before launching this module")
        self.setDisplayText("For now the Learning rate of optimizer, Kernel and Bias weight Initializers are already optimized and set in the in-built model (can also be set to different values in the config window)"+\
                            " (TO find another set of parameters please use Hyper parameter optimization routine in GUI)")
        self.setDisplayText("Load a config file first (for example see the example_config tab)")
        self._formLayout() ## buttons and layout
        self.popups = []
        self.timermp = QtCore.QTimer()
        # self.showMaximized()
        self.setFixedSize(16777215,16777215)
        
    def closeEvent(self, event):
        try:
            self.text_file_log.close()
        except:
            print("Nothing to close")
        self.close
        QApplication.closeAllWindows()
        super().closeEvent(event)
        
    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Load Config', self.getfileConfig)
        self.menu.addAction('&Exit', self.close)
    
    def getfileConfig(self):
        filenameConfig = QFileDialog.getOpenFileName(self, 'Select the config text file')
        self.load_config_from_file(filenameConfig[0])
    
    def load_config_from_file(self, configFile):
        
        global material_global, symmetry_global, material1_global, symmetry1_global
        global prefix_global, main_directory, emin_global, emax_global, ccd_label_global
        global detectorparameters_global, pixelsize_global, dim1_global, dim2_global
        global UB_matrix_global, image_grid_globalx , image_grid_globaly 
        global intensity_threshold_global, boxsize_global, fit_peaks_gaussian_global, FitPixelDev_global
        global strain_label_global, tolerance_strain, tolerance_strain1, hkls_list_global
        global expfile_global, exp_prefix_global, modelfile_global, weightfile_global
        global hkl_max_global, elements_global, freq_rmv_global, hkl_max1_global
        global elements1_global, freq_rmv1_global, maximum_angle_to_search_global
        global step_for_binning_global, nb_grains_per_lp_global, nb_grains_per_lp1_global
        global grains_nb_simulate_global, include_scm_global, batch_size_global, epochs_global
        global tolerance_global, model_weight_file, material0_limit1212, material1_limit1212, tolerance_global1
        global softmax_threshold_global, mr_threshold_global, cap_matchrate, coeff
        global coeff_overlap1212, mode_spotCycle, NumberMaxofFits, use_previous_UBmatrix
        global write_mtex_file, material0_lauegroup, material1_lauegroup, misorientation_angle1
        
        config = configparser.ConfigParser()
        config.read_file(open(configFile))

        material_global = config.get('MATERIAL', 'material')
        symmetry_global = config.get('MATERIAL', 'symmetry')
        
        try:
            material1_global = config.get('MATERIAL', 'material1')
            symmetry1_global = config.get('MATERIAL', 'symmetry1')
        except:
            material1_global = "none"
            symmetry1_global = "none"
            self.write_to_console("Only one material is defined, by default taking the other one as 'none'")
        
        if material1_global == "none" and symmetry1_global =="none":
            material1_global = material_global
            symmetry1_global = symmetry_global         
        
        prefix_global = str(config.get('GLOBAL_DIRECTORY', 'prefix'))
        main_directory = str(config.get('GLOBAL_DIRECTORY', 'main_directory'))
        
        detectorfile = config.get('DETECTOR', 'detectorfile')
        try:
            emax_global = float(config.get('DETECTOR', 'emax'))
            emin_global = float(config.get('DETECTOR', 'emin'))
        except:
            self.write_to_console("Detector energy range not defined, using default values of 5-23KeV")
            
        try:
            _file = open(detectorfile, "r")
            text = _file.readlines()
            _file.close()
            # first line contains parameters
            parameters = [float(elem) for elem in str(text[0]).split(",")]
            detectorparameters_global = parameters[:5]
            pixelsize_global = parameters[5]
            dim1_global = parameters[6]
            dim2_global = parameters[7]
            # others are comments
            comments = text[1:]
            ccd_label_global = ""
            for line in comments:
                if line.startswith("# CCDLabel"):
                    ccd_label_global = line.split(":")[1].strip()
            if ccd_label_global == "":
                self.write_to_console("CCD label cannot be read from the calibration file, setting it to latest detector sCMOS")
                ccd_label_global = "sCMOS"
        except IOError as error:
            self.write_to_console("Error opening file\n" + str(error))
        except UnicodeDecodeError as error:
            self.write_to_console("Error opening file\n" + str(error))
        
        try:
            UB_matrix_global = int(config.get('PREDICTION', 'UB_matrix_to_detect'))
        except:
            self.write_to_console("UB matrix to identify not defined, can be set in the Prediction window")
        
        try:
            image_grid_globalx = int(config.get('EXPERIMENT', 'image_grid_x'))
            image_grid_globaly = int(config.get('EXPERIMENT', 'image_grid_y'))
        except:
            self.write_to_console("Scan grid not defined, can be set in the Prediction window")
        
        try:
            softmax_threshold_global = float(config.get('PREDICTION', 'softmax_threshold_global'))
        except:
            self.write_to_console("Softmax threshold not defined, using default 80%")
        self.softmax_threshold_global = softmax_threshold_global
        
        try:
            mr_threshold_global = float(config.get('PREDICTION', 'mr_threshold_global'))
        except:
            self.write_to_console("Matching rate threshold not defined, using default 95%")
        self.mr_threshold_global = mr_threshold_global
        
        try:
            coeff = float(config.get('PREDICTION', 'coeff'))
        except:
            self.write_to_console("Coeff Overlap v0 not defined, using default 30%")
        self.coeff=coeff
        
        try:
            coeff_overlap1212 = float(config.get('PREDICTION', 'coeff_overlap'))
        except:
            self.write_to_console("Coeff Overlap not defined, using default 30%")
        self.coeff_overlap=coeff_overlap1212
        
        try:
            mode_spotCycle = str(config.get('PREDICTION', 'mode_spotCycle'))
        except:
            self.write_to_console("Analysis mode not defined, using default graphmode, can be set in Prediction window")
        self.mode_spotCycleglobal = mode_spotCycle
        
        try:
            material0_limit1212 = int(config.get('PREDICTION', 'material0_limit'))
        except:
            self.write_to_console("Max Nb of UB per material 0 not defined, using default maximum")
        self.material0_limit = material0_limit1212
        
        try:
            material1_limit1212 = int(config.get('PREDICTION', 'material1_limit'))
        except:
            self.write_to_console("Max Nb of UB per material 1 not defined, using default maximum")
        self.material1_limit = material1_limit1212
        
        intensity_threshold_global = float(config.get('PEAKSEARCH', 'intensity_threshold'))
        boxsize_global = int(config.get('PEAKSEARCH', 'boxsize'))
        
        try:
            fit_peaks_gaussian_global = int(config.get('PEAKSEARCH', 'fit_peaks_gaussian'))
        except:
            self.write_to_console("Fitting of peaks not defined, using default Gaussian fitting")
        self.fit_peaks_gaussian_global = fit_peaks_gaussian_global
        
        try:
            FitPixelDev_global = float(config.get('PEAKSEARCH', 'FitPixelDev'))
        except:
            self.write_to_console("Fitting PixelDev of peaks not defined, using default 20 pix")
        self.FitPixelDev_global=FitPixelDev_global
        
        try:
            NumberMaxofFits = float(config.get('PEAKSEARCH', 'NumberMaxofFits'))
        except:
            self.write_to_console("Max fits per LP not defined, using default 3000")
        self.NumberMaxofFits=NumberMaxofFits
        
        
        strain_label_global = config.get('STRAINCALCULATION', 'strain_compute') == "true"
        if strain_label_global:
            strain_label_global = "YES"
        else:
            strain_label_global = "NO"
        tolerance_strain_temp = config.get('STRAINCALCULATION', 'tolerance_strain_refinement').split(",")
        tolerance_strain = [float(i) for i in tolerance_strain_temp]
        self.tolerance_strain = tolerance_strain
        
        tolerance_strain_temp1 = config.get('STRAINCALCULATION', 'tolerance_strain_refinement1').split(",")
        tolerance_strain1 = [float(i) for i in tolerance_strain_temp1]
        self.tolerance_strain1 = tolerance_strain1
        
        try:
            hkls_list_global = config.get('POSTPROCESS', 'hkls_subsets')
        except:
            self.write_to_console("HKL post processing not defined, currently not used")
        
        expfile_global = config.get('EXPERIMENT', 'experiment_directory')
        exp_prefix_global = config.get('EXPERIMENT', 'experiment_file_prefix')
        
        ##exp directory
        if material_global == material1_global:
            fn = material_global + prefix_global
        else:
            fn = material_global + "_" + material1_global + prefix_global
        
        try:
            model_weight_file = config.get('PREDICTION', 'model_weight_file')
        except:
            model_weight_file = "none"
        
        modelfile_global = main_directory + "//" + fn
        if material_global == material1_global:
            if model_weight_file == "none":
                weightfile_global = modelfile_global + "//" + "model_" + material_global + ".h5"
            else:
                weightfile_global = model_weight_file
        else:
            if model_weight_file == "none":
                weightfile_global = modelfile_global + "//" + "model_" + material_global + "_" + material1_global + ".h5"
            else:
                weightfile_global = model_weight_file
        
        try:
            freq_rmv_global = int(config.get('TRAINING', 'classes_with_frequency_to_remove'))
        except:
            self.write_to_console("Frequency removal for HKLs not defined, can be defined in the config window")
        
        try:
            elements_global = config.get('TRAINING', 'desired_classes_output')
        except:
            self.write_to_console("Elements for HKLs not defined, can be defined in the config window")
        try:
            hkl_max_global = config.get('TRAINING', 'max_HKL_index')
        except:
            self.write_to_console("Max HKLs not defined, can be defined in the config window")
        try:
            nb_grains_per_lp_global = int(config.get('TRAINING', 'max_nb_grains'))
        except:
            self.write_to_console("Nb. of grains per LP not defined, can be defined in the config window")
        try:
            freq_rmv1_global = int(config.get('TRAINING', 'classes_with_frequency_to_remove1'))
        except:
            self.write_to_console("Frequency removal for HKLs 1 not defined, can be defined in the config window")
        try:
            elements1_global = config.get('TRAINING', 'desired_classes_output1')
        except:
            self.write_to_console("Elements for HKLs 1 not defined, can be defined in the config window")
        try:
            hkl_max1_global = config.get('TRAINING', 'max_HKL_index1')
        except:
            self.write_to_console("Max HKLs 1 not defined, can be defined in the config window")
        try:
            nb_grains_per_lp1_global = int(config.get('TRAINING', 'max_nb_grains1'))
        except:
            self.write_to_console("Nb. of grains per LP 1 not defined, can be defined in the config window")
        try:
            maximum_angle_to_search_global = float(config.get('TRAINING', 'angular_distance'))
        except:
            self.write_to_console("Histogram angle not defined, can be defined in the config window")
        try:
            step_for_binning_global = float(config.get('TRAINING', 'step_size'))
        except:
            self.write_to_console("steps for histogram binnning not defined, can be defined in the config window")
        try:
            grains_nb_simulate_global = int(config.get('TRAINING', 'max_simulations'))
        except:
            self.write_to_console("Number of simulations per LP not defined, can be defined in the config window")
        try:
            include_scm_global = config.get('TRAINING', 'include_small_misorientation') == "true"
        except:
            self.write_to_console("Single crystal misorientation not defined, can be defined in the config window")
        try:
            misorientation_angle = float(config.get('TRAINING', 'misorientation_angle'))
        except:
            misorientation_angle = misorientation_angle1
            self.write_to_console("Angle of Single crystal misorientation along Z not defined, can be defined in the config window")
        self.misorientation_angle = misorientation_angle
        try:
            batch_size_global = int(config.get('TRAINING', 'batch_size'))
        except:
            self.write_to_console("Batch size not defined, can be defined in the config window")
        try:
            epochs_global = int(config.get('TRAINING', 'epochs'))
        except:
            self.write_to_console("Epochs not defined, can be defined in the config window")
        
        try:
            cap_matchrate = float(config.get('PREDICTION', 'cap_matchrate')) * 100
        except:
            self.write_to_console("Cap_Matching rate not defined, setting default value of 1%")
        self.cap_matchrate=cap_matchrate
        try:
            tolerance_global = float(config.get('PREDICTION', 'matrix_tolerance'))
        except:
            self.write_to_console("Angle tolerance to detect grains not defined, using default 0.7")
        try:
            tolerance_global1 = float(config.get('PREDICTION', 'matrix_tolerance1'))
        except:
            self.write_to_console("Angle tolerance for Mat 1 to detect grains not defined, using default 0.7")
        try:
            use_previous_UBmatrix = config.get('PREDICTION', 'use_previous') == "true"
        except:
            self.write_to_console("Use previous solutions not defined, using default value False")
        self.use_previous_UBmatrix = use_previous_UBmatrix
        try:
            material_phase_always_present = config.get('DEVELOPMENT', 'material_phase_always_present')
        except:
            material_phase_always_present = "none"
            self.write_to_console("material_phase_always_present not defined, default is NONE")
            
        if material_phase_always_present == "none":
            material_phase_always_present = None
        else:
            material_phase_always_present = int(material_phase_always_present)
        self.material_phase_always_present = material_phase_always_present
        try:
            write_mtex_file = config.get('DEVELOPMENT', 'write_MTEX_file') == "true"
        except:
            self.write_to_console("Write MTEX texture file not defined, by default True")
        try:
            material0_lauegroup = config.get('DEVELOPMENT', 'material0_lauegroup')
        except:
            self.write_to_console("Laue group of first material not defined, can be defined in the config windoby default Cubic")
        try:
            material1_lauegroup = config.get('DEVELOPMENT', 'material1_lauegroup')
        except:
            self.write_to_console("Laue group of second material not defined, can be defined in the config windoby default Cubic")
                  
        self.write_to_console("Config file loaded successfully.")

    def _createToolBar(self):
        self.tools = QToolBar()
        self.addToolBar(self.tools)
        self.trialtoolbar101 = self.tools.addAction('Example_config', self.show_window_config)
        self.trialtoolbar10 = self.tools.addAction('Re-Train saved model', self.show_window_retraining_fromfile)
        self.trialtoolbar1 = self.tools.addAction('Re-Train GUI model', self.show_window_retraining)
        self.trialtoolbar10.setEnabled(False)
        self.trialtoolbar1.setEnabled(False)
        
    def show_window_parameters(self):
        w2 = AnotherWindowParams(self.state, gui_state)
        w2.got_signal.connect(self.postprocesstrain)
        w2.show()
        self.popups.append(w2)
        self.state = self.state +1
    
    def show_window_retraining(self):
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.train_model(prefix="_"+c_time, tag = 1)
        
    def show_window_retraining_fromfile(self):
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.train_model(prefix="_"+c_time, tag = 2)
        
    def show_window_config(self):
        w21 = sample_config()
        w21.show()
        self.popups.append(w21)
        
    def show_window_liveprediction(self):
        if self.material_ != self.material1_:
            with open(self.save_directory+"//classhkl_data_nonpickled_"+self.material_+".pickle", "rb") as input_file:
                hkl_all_class0 = cPickle.load(input_file)[0]

            with open(self.save_directory+"//classhkl_data_nonpickled_"+self.material1_+".pickle", "rb") as input_file:
                hkl_all_class1 = cPickle.load(input_file)[0]

        else:
            hkl_all_class1 = None
            with open(self.save_directory+"//classhkl_data_nonpickled_"+self.material_+".pickle", "rb") as input_file:
                hkl_all_class0 = cPickle.load(input_file)[0]
                        
        w2 = AnotherWindowLivePrediction(self.state2, gui_state, 
                                         material_=self.material_, material1_=self.material1_, emin=self.emin, 
                                         emax=self.emax, symmetry=self.symmetry, symmetry1=self.symmetry1,
                                         detectorparameters=self.detectorparameters, pixelsize=self.pixelsize,
                                         lattice_=self.lattice_material, lattice1_ =self.lattice_material1,
                                         hkl_all_class0 = hkl_all_class0, hkl_all_class1=hkl_all_class1,
                                         mode_spotCycleglobal=self.mode_spotCycleglobal,
                                         softmax_threshold_global = self.softmax_threshold_global,
                                         mr_threshold_global =    self.mr_threshold_global,
                                         cap_matchrate =    self.cap_matchrate,
                                         coeff =    self.coeff,
                                         coeff_overlap1212 =    self.coeff_overlap,
                                         fit_peaks_gaussian_global =    self.fit_peaks_gaussian_global,
                                         FitPixelDev_global =    self.FitPixelDev_global,
                                         NumberMaxofFits =    self.NumberMaxofFits,
                                         tolerance_strain =    self.tolerance_strain,
                                         tolerance_strain1 =    self.tolerance_strain1,
                                         material0_limit = self.material0_limit,
                                         material1_limit = self.material1_limit,
                                         symmetry_name = self.symmetry_name, 
                                         symmetry1_name = self.symmetry1_name,
                                         use_previous_UBmatrix_name = self.use_previous_UBmatrix,
                                         material_phase_always_present = self.material_phase_always_present)
        w2.show()
        self.popups.append(w2)
        self.state2 += 1
        
    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("status")
        self.setStatusBar(self.status)

    def _formLayout(self):
        self.formLayout = QFormLayout()
        
        self.progress = QProgressBar()
        
        self.configure_nn = QPushButton('Configure parameters')
        self.configure_nn.clicked.connect(self.show_window_parameters)
        self.configure_nn.setEnabled(True)
        
        self.generate_nn = QPushButton('Generate Training dataset')
        self.generate_nn.clicked.connect(self.generate_training_data)
        self.generate_nn.setEnabled(False)
        
        self.train_nn = QPushButton('Train Neural Network')
        self.train_nn.clicked.connect(self.train_neural_network)
        self.train_nn.setEnabled(False)
        
        self.train_nnhp = QPushButton('Hypergrid Params OPT')
        self.train_nnhp.clicked.connect(self.grid_search_hyperparams)
        self.train_nnhp.setEnabled(False)
        
        # self.predict_nnc = QPushButton('Config Prediction')
        # self.predict_nnc.clicked.connect(self.show_window_prediction)
        # self.predict_nnc.setEnabled(False)
        
        self.predict_nn = QPushButton('Prediction')
        self.predict_nn.clicked.connect(self.predict_preprocess)
        self.predict_nn.setEnabled(False)
        
        self.predict_lnn = QPushButton('Live Prediction with IPF map')
        self.predict_lnn.clicked.connect(self.show_window_liveprediction)
        self.predict_lnn.setEnabled(False)
        
        self.formLayout.addRow(self.progress)
        self.formLayout.addRow(self.configure_nn)
        self.formLayout.addRow(self.generate_nn)
        self.formLayout.addRow(self.train_nn)
        self.formLayout.addRow(self.train_nnhp)
        # self.formLayout.addRow(self.predict_nnc, self.predict_nn)
        # self.formLayout.addRow(self.predict_lnnc, self.predict_lnn)
        self.formLayout.addRow(self.predict_lnn)
        self.layout.addLayout(self.formLayout)
        
    def write_to_console(self, line, to_push=0):
        try:
            self.text_file_log.write(line + "\n")
        except:
            print("Log file not yet created: "+ str(line.encode('utf-8','ignore')))
        self.setDisplayText(str(line.encode('utf-8','ignore'),errors='ignore'))
        QApplication.processEvents() 
    
    def postprocesstrain(self, emit_dict):
        self.input_params = {
                            "material_": emit_dict["material_"], ## same key as used in LaueTools
                            "material1_": emit_dict["material1_"],
                            "prefix": emit_dict["prefix"],
                            "symmetry": emit_dict["symmetry"],
                            "symmetry1": emit_dict["symmetry1"],
                            "hkl_max_identify" : emit_dict["hkl_max_identify"], # can be "auto" or an index i.e 12
                            "hkl_max_identify1" : emit_dict["hkl_max_identify1"],
                            "maximum_angle_to_search" : emit_dict["maximum_angle_to_search"],
                            "step_for_binning" : emit_dict["step_for_binning"],
                            "mode_of_analysis" : emit_dict["mode_of_analysis"],
                            "nb_grains_per_lp" : emit_dict["nb_grains_per_lp"], ## max grains to expect in a LP
                            "nb_grains_per_lp1" : emit_dict["nb_grains_per_lp1"],
                            "grains_nb_simulate" : emit_dict["grains_nb_simulate"],
                            "detectorparameters" : emit_dict["detectorparameters"],
                            "pixelsize" : emit_dict["pixelsize"],
                            "dim1" : emit_dict["dim1"],
                            "dim2" : emit_dict["dim2"],
                            "emin" : emit_dict["emin"],
                            "emax" : emit_dict["emax"],
                            "batch_size" : emit_dict["batch_size"], ## batches of files to use while training
                            "epochs" : emit_dict["epochs"], ## number of epochs for training
                            "texture": emit_dict["texture"],
                            "mode_nn": emit_dict["mode_nn"],
                            "grid_bool": emit_dict["grid_bool"],
                            "directory": emit_dict["directory"],
                            "freq_rmv":  emit_dict["freq_rmv"],
                            "elements":  emit_dict["elements"],
                            "freq_rmv1":  emit_dict["freq_rmv1"],
                            "elements1":  emit_dict["elements1"],
                            "include_scm":  emit_dict["include_scm"],
                            "lr":  emit_dict["lr"],
                            "kc":  emit_dict["kc"],
                            "bc":  emit_dict["bc"],
                            }
        ## Gray out options based on the mode_nn
        if self.input_params["mode_nn"] == "Generate Data & Train":
            self.write_to_console("Generate and Train the Model")
            self.generate_nn.setEnabled(True)
            
        elif self.input_params["mode_nn"] == "Train":
            self.write_to_console("Data already exists ? Train the Model")
            self.train_nn.setEnabled(True)
            self.trialtoolbar10.setEnabled(True)
            
        elif self.input_params["mode_nn"] == "Predict":
            self.write_to_console("Model already exists? Lets Predict!")
            self.write_to_console("on the fly prediction (fingers crossed)")
            self.predict_nn.setEnabled(True)
            # self.predict_nnc.setEnabled(True)
            self.predict_lnn.setEnabled(True)

        if self.input_params["grid_bool"] == "True":
            self.train_nnhp.setEnabled(True)
        
        self.include_scm = False
        if self.input_params["include_scm"] == "yes":
            self.include_scm = True  
            
        self.freq_rmv = self.input_params["freq_rmv"]
        self.freq_rmv1 = self.input_params["freq_rmv1"]
        if self.input_params["elements"] == "all":
            self.elements = self.input_params["elements"] #"all"
            self.elements1 = self.input_params["elements1"] #"all"
        else:
            self.elements = int(self.input_params["elements"])
            self.elements1 = int(self.input_params["elements1"])
            
        self.material_ = self.input_params["material_"]
        self.material1_ = self.input_params["material1_"]
        
        self.emin, self.emax = self.input_params["emin"], self.input_params["emax"]
        
        self.learning_rate, self.kernel_coeff, self.bias_coeff = self.input_params["lr"],self.input_params["kc"],self.input_params["bc"]
        
        if self.input_params["directory"] == None: ## default path
            if self.material_ == self.material1_:
                self.save_directory = os.getcwd()+"//"+self.input_params["material_"]+self.input_params["prefix"]
            else:
                self.save_directory = os.getcwd()+"//"+self.input_params["material_"]+"_"+self.input_params["material1_"]+self.input_params["prefix"]
        else:
            if self.material_ == self.material1_:
                self.save_directory = self.input_params["directory"]+"//"+self.input_params["material_"]+self.input_params["prefix"]
            else:
                self.save_directory = self.input_params["directory"]+"//"+self.input_params["material_"]+"_"+self.input_params["material1_"]+self.input_params["prefix"]

        self.n = self.input_params["hkl_max_identify"]
        self.n1 = self.input_params["hkl_max_identify1"]
        self.maximum_angle_to_search = self.input_params["maximum_angle_to_search"]
        self.step_for_binning = self.input_params["step_for_binning"]
        self.mode_of_analysis = self.input_params["mode_of_analysis"]
        self.nb_grains_per_lp = self.input_params["nb_grains_per_lp"]
        self.nb_grains_per_lp1 = self.input_params["nb_grains_per_lp1"]
        self.grains_nb_simulate = self.input_params["grains_nb_simulate"]
        self.detectorparameters = self.input_params["detectorparameters"]
        self.pixelsize = self.input_params["pixelsize"]
        # =============================================================================
        # Symmetry input
        # =============================================================================
        a, b, c, alpha, beta, gamma = dictLT.dict_Materials[self.material_][1]
        a, b, c = a*0.1, b*0.1, c*0.1
        self.rules = dictLT.dict_Materials[self.material_][-1]
        self.symmetry_name = self.input_params["symmetry"]
        if self.input_params["symmetry"] =="cubic":
            self.symmetry = Symmetry.cubic
            self.lattice_material = Lattice.cubic(a)
        elif self.input_params["symmetry"] =="monoclinic":
            self.symmetry = Symmetry.monoclinic
            self.lattice_material = Lattice.monoclinic(a, b, c, beta)
        elif self.input_params["symmetry"] == "hexagonal":
            self.symmetry = Symmetry.hexagonal
            self.lattice_material = Lattice.hexagonal(a, c)
        elif self.input_params["symmetry"] == "orthorhombic":
            self.symmetry = Symmetry.orthorhombic
            self.lattice_material = Lattice.orthorhombic(a, b, c)
        elif self.input_params["symmetry"] == "tetragonal":
            self.symmetry = Symmetry.tetragonal
            self.lattice_material = Lattice.tetragonal(a, c)
        elif self.input_params["symmetry"] == "trigonal":
            self.symmetry = Symmetry.trigonal
            self.lattice_material = Lattice.rhombohedral(a, alpha)
        elif self.input_params["symmetry"] == "triclinic":
            self.symmetry = Symmetry.triclinic
            self.lattice_material = Lattice.triclinic(a, b, c, alpha, beta, gamma)
        
        if self.material_ != self.material1_:
            self.symmetry1_name = self.input_params["symmetry1"]
            a1, b1, c1, alpha1, beta1, gamma1 = dictLT.dict_Materials[self.material1_][1]
            a1, b1, c1 = a1*0.1, b1*0.1, c1*0.1
            self.rules1 = dictLT.dict_Materials[self.material1_][-1]
            if self.input_params["symmetry1"] =="cubic":
                self.symmetry1 = Symmetry.cubic
                self.lattice_material1 = Lattice.cubic(a1)
            elif self.input_params["symmetry1"] =="monoclinic":
                self.symmetry1 = Symmetry.monoclinic
                self.lattice_material1 = Lattice.monoclinic(a1, b1, c1, beta1)
            elif self.input_params["symmetry1"] == "hexagonal":
                self.symmetry1 = Symmetry.hexagonal
                self.lattice_material1 = Lattice.hexagonal(a1, c1)
            elif self.input_params["symmetry1"] == "orthorhombic":
                self.symmetry1 = Symmetry.orthorhombic
                self.lattice_material1 = Lattice.orthorhombic(a1, b1, c1)
            elif self.input_params["symmetry1"] == "tetragonal":
                self.symmetry1 = Symmetry.tetragonal
                self.lattice_material1 = Lattice.tetragonal(a1, c1)
            elif self.input_params["symmetry1"] == "trigonal":
                self.symmetry1 = Symmetry.trigonal
                self.lattice_material1 = Lattice.rhombohedral(a1, alpha1)
            elif self.input_params["symmetry1"] == "triclinic":
                self.symmetry1 = Symmetry.triclinic
                self.lattice_material1 = Lattice.triclinic(a1, b1, c1, alpha1, beta1, gamma1)
        else:
            self.rules1 = None
            self.symmetry1 = None
            self.lattice_material1 = None
            self.symmetry1_name = self.input_params["symmetry"]
        
        self.modelp = "random" 
        ### Load texture files based on symmetry
        if self.input_params["texture"] == "in-built_Uniform_Distribution":
            self.write_to_console("# Using uniform distribution generated with Neper for Training dataset \n") 
            self.modelp = "uniform"
        elif self.input_params["texture"] == "random":
            self.write_to_console("# Using random orientation distribution for Training dataset \n") 
            self.modelp = "random"
        else:
            self.modelp = "experimental"
            self.write_to_console("# User defined texture to be used: TODO \n") 
        
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        self.write_to_console("Working directory :"+ self.save_directory)
        
        ## Golbal log file
        now = datetime.datetime.fromtimestamp(GUI_START_TIME)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        if self.material_ == self.material1_:
            self.text_file_log = open(self.save_directory+"//log_"+self.material_+".txt", "a")
        else:
            self.text_file_log = open(self.save_directory+"//log_"+self.material_+"_"+self.material1_+".txt", "a")
        self.text_file_log.write("# Log file created at "+ c_time + "\n") 
    
    def postprocesspred(self,):
        pass
        
    def predict_preprocess(self,):
        pass

    def commonclass(self, hkl1, hkl2, lattice_material, symmetry_):
        """ test if hkl1 and hkl2 belong to the same class"""
        h,k,l = hkl1
        h1,k1,l1 = hkl2
        h_obj = HklPlane(h,k,l, lattice=lattice_material)
        normal = np.round(h_obj.normal(), 6)
        h_obj1 = HklPlane(h1,k1,l1, lattice=lattice_material)
        family = h_obj1.get_family(h_obj1.miller_indices(), lattice=h_obj1._lattice, 
                                   include_friedel_pairs=True, crystal_structure=symmetry_)
        normals = np.array([np.round(ijk.normal(),6) for ijk in family])
        cond1 = h_obj in family
        cond2 = np.any(np.all(normal == normals, axis=1))
        return cond1 or cond2
    
    def temp_HKL(self, removeharmonics=1):
        material_= self.input_params["material_"]
        nbgrains = self.input_params["nb_grains_per_lp"]
        nbtestspots = 0
        hkl_sol_all = np.zeros((1,4))
        verbose=0
        for _ in range(10):
            seednumber = np.random.randint(1e6)
            tabledistancerandom, hkl_sol, \
                                    _, _, _, _, _ = self.prepare_LP(nbgrains, 0,
                                                                    material_,
                                                                    None,
                                                                    verbose,
                                                                    plotLauePattern=False,
                                                                    seed=seednumber,
                                                                    detectorparameters=self.input_params["detectorparameters"], 
                                                                    pixelsize=self.input_params["pixelsize"],
                                                                    dim1=self.input_params["dim1"],
                                                                    dim2=self.input_params["dim2"],
                                                                    removeharmonics=removeharmonics)
                                    
            spots_in_center = [sp for sp in range(len(tabledistancerandom))] # take all spots in Laue pattern
            hkl_sol_all = np.vstack((hkl_sol_all, hkl_sol))
            nbtestspots = nbtestspots + len(spots_in_center)

        if self.material_ != self.material1_:
            copy1 = np.copy(int(np.max(np.abs(hkl_sol_all))))
            copy1_min = np.copy(int(np.min(hkl_sol_all)))
            material_= self.input_params["material1_"]
            nbgrains = self.input_params["nb_grains_per_lp1"]
            hkl_sol_all = np.zeros((1,4))
            verbose=0
            for _ in range(10):
                seednumber = np.random.randint(1e6)
                tabledistancerandom, hkl_sol, \
                                        _, _, _, _, _ = self.prepare_LP(nbgrains, 0,
                                                                        material_,
                                                                        None,
                                                                        verbose,
                                                                        plotLauePattern=False,
                                                                        seed=seednumber,
                                                                        detectorparameters=self.input_params["detectorparameters"], 
                                                                        pixelsize=self.input_params["pixelsize"],
                                                                        dim1=self.input_params["dim1"],
                                                                        dim2=self.input_params["dim2"],
                                                                        removeharmonics=removeharmonics)
                                        
                spots_in_center = [sp for sp in range(len(tabledistancerandom))] # take all spots in Laue pattern
                hkl_sol_all = np.vstack((hkl_sol_all, hkl_sol))
                nbtestspots = nbtestspots + len(spots_in_center)
            hkl_sol_all = np.delete(hkl_sol_all, 0, axis =0)
            copy_ = np.copy(int(np.max(np.abs(hkl_sol_all))))
            copy_min_ = np.copy(int(np.min(hkl_sol_all)))
            self.write_to_console("Total spots created for calculating HKL bounds:"+str(nbtestspots))
            self.write_to_console("Max HKL index for "+self.material_+" :"+str(copy1))
            self.write_to_console("Min HKL index "+self.material_+" :"+str(copy1_min))
            self.write_to_console("Max HKL index for "+self.material1_+" :"+str(copy_))
            self.write_to_console("Min HKL index "+self.material1_+" :"+str(copy_min_))
            return int(copy1), int(copy_)

        self.write_to_console("Total spots created for calculating HKL bounds:"+str(nbtestspots))
        self.write_to_console("Max HKL index:"+str(np.max(hkl_sol_all)))
        self.write_to_console("Min HKL index:"+str(np.min(hkl_sol_all)))
        return int(np.max(np.abs(hkl_sol_all))), int(np.max(np.abs(hkl_sol_all)))
    
    def prepare_LP(self, nbgrains, nbgrains1, material_, material1_, verbose, plotLauePattern, seed=None, sortintensity=False,
                   detectorparameters=None, pixelsize=None, dim1=2048, dim2=2048, removeharmonics=1):
        s_tth, s_chi, s_miller_ind, s_posx, s_posy, \
                                        s_intensity, _, _ = Window.simulatemultiplepatterns(nbgrains, nbgrains1, seed=seed, 
                                                                                    key_material=material_,
                                                                                    key_material1=material1_,
                                                                                    detectorparameters=detectorparameters,
                                                                                    pixelsize=pixelsize,
                                                                                    emin=self.emin,
                                                                                    emax=self.emax,
                                                                                    sortintensity=sortintensity, 
                                                                                    dim1=dim1,dim2=dim2,
                                                                                    removeharmonics=removeharmonics,
                                                                                    misorientation_angle=1)
        # considering all spots
        allspots_the_chi = np.transpose(np.array([s_tth/2., s_chi]))
        tabledistancerandom = np.transpose(GT.calculdist_from_thetachi(allspots_the_chi, allspots_the_chi))
        # ground truth
        hkl_sol = s_miller_ind
        return tabledistancerandom, hkl_sol, s_posx, s_posy, s_intensity, s_tth, s_chi
    
    def run_(self, n, rules, lattice_material, symmetry, material_):
        temp_ = GT.threeindices_up_to(int(n))
        classhkl_ = CP.ApplyExtinctionrules(temp_, rules)
        self.write_to_console("Generating HKL objects", to_push=1)
        # generate HKL object
        self.progress.setMaximum(len(classhkl_))
        hkl_all = {}
        for i in range(len(classhkl_)):
            h_obj = HklPlane(classhkl_[i,0],classhkl_[i,1],classhkl_[i,2], lattice=lattice_material)
            h_dir_ = HklDirection(*(classhkl_[i,0],classhkl_[i,1],classhkl_[i,2]), lattice=lattice_material)
            family = h_obj.get_family(h_obj.miller_indices(), lattice=h_obj._lattice, 
                                      include_friedel_pairs=True, crystal_structure=symmetry)
            normals = np.array([np.round(ijk.normal(),6) for ijk in family])

            tempp = np.array([ijk.miller_indices() for ijk in family])
            compx = []
            for ij in range(len(tempp)):
                compx.append(sum(np.sign(tempp[ij,:])))
            inde = np.where(compx==np.max(compx))[0][0]
            classhkl_[i] = tempp[inde]
            
            h_dir = [HklDirection(*ijk.miller_indices(), lattice=lattice_material) for ijk in family]
            hkl_all[str(classhkl_[i])] = {"HKL_object": h_obj,
                                          "HKL_dir": np.round(h_dir_.direction(),6),
                                          "HKL_direction": h_dir,
                                          "family": family,
                                          "normals": normals}
            self.progress.setValue(i+1)
            QApplication.processEvents() 
            
        ## Lets sort the HKL list by simple SUM    
        # create array with all the miller indices
        hkl_list = [hkl_all[str(j)]["HKL_object"] for j in hkl_all]
        hkl_array = np.empty((len(hkl_list), 3), dtype=int)
        for i in range(len(hkl_list)):
            hkl = hkl_list[i]
            hkl_array[i] = np.array(hkl.miller_indices())
        # first start by ordering the HklObjects by ascending miller indices sum
        hkl_sum = np.sum(np.abs(hkl_array), axis=1)
        hkl_sum_sort = np.argsort(hkl_sum)[::-1]
        classhkl_ = classhkl_[hkl_sum_sort]
        
        ## FAST IMPLEMENTATION
        ## make comprehensive list of dictionary
        normal_hkl = np.zeros((1,3))
        # direction_hkl = np.zeros((1,3))
        for j in classhkl_:
            # stack_dir = np.array([np.round(ijk.direction(),6) for ijk in hkl_all[str(j)]["HKL_direction"]])
            # direction_hkl = np.vstack((direction_hkl, stack_dir))
            normal_hkl = np.vstack((normal_hkl, hkl_all[str(j)]["normals"]))
        normal_hkl = np.delete(normal_hkl, 0, axis =0)
        # direction_hkl = np.delete(direction_hkl, 0, axis =0)
        
        count = 0
        index_hkl = [count+j for j,k in enumerate(classhkl_) for i in range(len(hkl_all[str(k)]["family"]))]
        
        ## harmonics also taken care of here...(as GT.filterharmonics is memory extensive)
        self.write_to_console("Removing harmonics and building equivalent HKL objects", to_push=1)
        self.progress.setMaximum(len(classhkl_))
        ind_rmv = []
        for i1 in range(len(classhkl_)):
            ## HKL plane comparison
            hkl_object = hkl_all[str(classhkl_[i1])]["HKL_object"]
            normal = np.round(hkl_object.normal(), 6)
            temp1_ = np.all(normal == normal_hkl, axis=1)
            ## HKL direction comparison
            # direction = hkl_all[str(classhkl_[i1])]["HKL_dir"]
            # temp1_ = np.all(direction == direction_hkl, axis=1)
            ## compare
            if len(np.where(temp1_)[0]) != 0:
                ind_ = np.where(temp1_)[0]
                for inin in ind_:
                    if index_hkl[inin] > i1:
                        ind_rmv.append(i1)
                        break         
            self.progress.setValue(i1+1)
            QApplication.processEvents() 
        ind_rmv = np.unique(ind_rmv)
        classhkl = np.delete(classhkl_, ind_rmv, axis = 0)
        
        ########### FINAL HKL CLASS FOR THE MATERIAL
        self.write_to_console("Finalizing the HKL objects", to_push=1)
        hkl_all_class = {}
        hkl_millerindices = {}
        self.progress.setMaximum(len(classhkl))
        for i in range(len(classhkl)): ## progress
            h_obj = HklPlane(classhkl[i,0],classhkl[i,1],classhkl[i,2], lattice=lattice_material)
            family = h_obj.get_family(h_obj.miller_indices(), lattice=h_obj._lattice, 
                                      include_friedel_pairs=True, crystal_structure=symmetry)
            normals = np.array([np.round(ijk.normal(),6) for ijk in family])

            hkl_all_class[str(classhkl[i])] = {"HKL_object": h_obj,
                                         "family": family,"normals": normals}
            
            hkl_millerindices[str(classhkl[i])] =  np.array([ii.miller_indices() for ii in family])
            
            self.progress.setValue(i+1)
            QApplication.processEvents() 
        # self.progress.setValue(0)

        with open(self.save_directory + "//hkl_data_"+material_+".pickle", "wb") as output_file:
            cPickle.dump([hkl_millerindices], output_file)
        
        with open(self.save_directory + "//classhkl_data_"+material_+".pickle", "wb") as output_file:
            cPickle.dump([classhkl, classhkl_, ind_rmv, n, temp_, \
                          hkl_all_class, hkl_all, lattice_material, symmetry], output_file)
        
        ### Lets dump the hkl miller of each family into an array to avoid pickling issues
        tempdict = {}
        for i in hkl_all_class.keys():
            tempdict[i] = [ii.miller_indices() for ii in hkl_all_class[i]['family']]
            
        with open(self.save_directory + "//classhkl_data_nonpickled_"+material_+".pickle", "wb") as output_file:
            cPickle.dump([tempdict], output_file)       
        
        self.write_to_console("Saved class HKL data in : "+self.save_directory + "//classhkl_data_"+material_+".pickle")
    
    def get_material_data(self, material_="Cu", ang_maxx = 45, step = 0.5, hkl_ref=13, classhkl = None):
        a, b, c, alpha, beta, gamma = dictLT.dict_Materials[material_][1]
        Gstar = CP.Gstar_from_directlatticeparams(a, b, c, alpha, beta, gamma)
        rules = dictLT.dict_Materials[material_][-1]
        
        hkl2 = GT.threeindices_up_to(int(hkl_ref))
        hkl2 = CP.ApplyExtinctionrules(hkl2,rules)
        hkl2 = hkl2.astype(np.int16)
    
        query_angle = ang_maxx/2.
        angle_tol = ang_maxx/2.
        metrics = Gstar

        hkl1 = classhkl
        H1 = hkl1
        n1 = hkl1.shape[0]
        H2 = hkl2
        n2 = hkl2.shape[0]
        dstar_square_1 = np.diag(np.inner(np.inner(H1, metrics), H1))
        dstar_square_2 = np.diag(np.inner(np.inner(H2, metrics), H2))
        scalar_product = np.inner(np.inner(H1, metrics), H2) * 1.0
        d1 = np.sqrt(dstar_square_1.reshape((n1, 1))) * 1.0
        d2 = np.sqrt(dstar_square_2.reshape((n2, 1))) * 1.0
        outy = np.outer(d1, d2)
        
        ratio = scalar_product / outy
        ratio = np.round(ratio, decimals=7)
        tab_angulardist = np.arccos(ratio) / (np.pi / 180.0)
        np.putmask(tab_angulardist, np.abs(tab_angulardist) < 0.001, 400)
        
        self.write_to_console("Calculating Mutual angular distances", to_push=1)
        self.progress.setMaximum(len(tab_angulardist))
        closest_angles_values = []
        for ang_ in range(len(tab_angulardist)):
            tab_angulardist_ = tab_angulardist[ang_,:]
            angles_set = np.ravel(tab_angulardist_)  # 1D array
            sorted_ind = np.argsort(angles_set)
            sorted_angles = angles_set[sorted_ind]
            
            angle_query = angle_tol
            if isinstance(query_angle, (list, np.ndarray, tuple)):
                angle_query = query_angle[0]
            
            array_angledist = np.abs(sorted_angles - angle_query)
            pos_min = np.argmin(array_angledist)
            closest_angle = sorted_angles[pos_min]
            
            if np.abs(closest_angle - query_angle) > angle_tol:
                if angle_query > 0.5:
                    pass
                print("TODO function get_material_data")
                
            condition = array_angledist <= angle_tol
            closest_index_in_sorted_angles_raw = np.where(condition)[0]
            closest_angles_values.append(np.take(sorted_angles, closest_index_in_sorted_angles_raw))
            self.progress.setValue(ang_+1)
            QApplication.processEvents() 
        
        self.write_to_console("Constructing histograms", to_push=1)
        self.progress.setMaximum(len(closest_angles_values))
        codebars = []
        angbins = np.arange(0, ang_maxx+step, step)
        for i in range(len(closest_angles_values)):
            angles = closest_angles_values[i]
            # fingerprint = np.histogram(angles, bins=angbins, density=False)[0]
            fingerprint = histogram1d(angles, range=[min(angbins),max(angbins)], bins=len(angbins)-1)
            ## Normalize the histogram by its maximum: simple way 
            ## Maybe better normalization is possible.. to be seen
            max_codebars = np.max(fingerprint)
            fingerprint = fingerprint/ max_codebars
            codebars.append(fingerprint)
            self.progress.setValue(i+1)
            QApplication.processEvents() 
        # self.progress.setValue(0)
        return codebars, angbins
    
    def load_dataset(self, material_="Cu", material1_="Cu", ang_maxx=18.,step=0.1, mode=0, 
                     nb_grains=1, nb_grains1=1, grains_nb_simulate=100, data_realism = False, 
                     detectorparameters=None, pixelsize=None, type_="training",
                     var0 = 0, dim1=2048, dim2=2048, removeharmonics=1): 
        """
        works for all symmetries now.
        """
        ## make sure directory exists
        save_directory_ = self.save_directory+"//"+type_
        if not os.path.exists(save_directory_):
            os.makedirs(save_directory_)

        try:
            with open(self.save_directory+"//classhkl_data_"+material_+".pickle", "rb") as input_file:
                classhkl, _, _, n, _, \
                    _, hkl_all, lattice_material, symmetry = cPickle.load(input_file)
                    
            if material_ != material1_:
                with open(self.save_directory+"//classhkl_data_"+material1_+".pickle", "rb") as input_file:
                    classhkl1, _, _, n, _, \
                        _, hkl_all1, lattice_material1, symmetry1 = cPickle.load(input_file)
        except:
            self.write_to_console("Class HKL library data not found, please run it first")
            return None
        
        if var0==1:
            codebars, angbins = self.get_material_data(material_ = material_, ang_maxx = ang_maxx, step = step,
                                                       hkl_ref=n, classhkl=classhkl)
            loc = np.array([ij for ij in range(len(classhkl))])
            ## routine implemented after the HCP fiasco!!!
            self.write_to_console("Verifying if two different HKL class have same angular distribution (can be very time consuming depending on the symmetry)")
            index = []
            self.progress.setMaximum(len(codebars))
            count_cbs = 0
            for i, j in enumerate(codebars):
                for k, l in enumerate(codebars):
                    if i != k and np.all(j == l):
                        index.append((i,k))
                        string0 = "HKL's "+ str(classhkl[i])+" and "+str(classhkl[k])+" have exactly the same angular distribution."
                        self.write_to_console(string0)
                count_cbs += 1
                self.progress.setValue(count_cbs)
                QApplication.processEvents()
                  
            if len(index) == 0:
                self.write_to_console("Great! No two HKL class have same angular distribution")
            else:
                self.write_to_console("Some HKL's have similar angular distribution; this will likely reduce the accuracy of the neural network; verify if symmetry matrix and other parameters are properly configured")
            
            np.savez_compressed(self.save_directory+'//conflict_angular_distribution_debug.npz', codebars, index)
            np.savez_compressed(save_directory_+'//grain_init.npz', codebars, loc)
            np.savez_compressed(self.save_directory+'//grain_classhkl_angbin.npz', classhkl, angbins)
            
            
            if material_ != material1_:
                codebars, angbins = self.get_material_data(material_ = material1_, ang_maxx = ang_maxx, step = step,
                                                       hkl_ref=n, classhkl=classhkl1)
                ind_offset = loc[-1] + 1
                loc = np.array([ind_offset + ij for ij in range(len(classhkl1))])
                self.write_to_console("Verifying if two different HKL class have same angular distribution (can be very time consuming depending on the symmetry)")
                index = []
                self.progress.setMaximum(len(codebars))
                count_cbs = 0
                for i, j in enumerate(codebars):
                    for k, l in enumerate(codebars):
                        if i != k and np.all(j == l):
                            index.append((i,k))
                            string0 = "HKL's "+ str(classhkl1[i])+" and "+str(classhkl1[k])+" have exactly the same angular distribution."
                            self.write_to_console(string0)
                    count_cbs += 1
                    self.progress.setValue(count_cbs)
                    QApplication.processEvents()

                if len(index) == 0:
                    self.write_to_console("Great! No two HKL class have same angular distribution")
                else:
                    self.write_to_console("Some HKL's have similar angular distribution; this will likely reduce the accuracy of the neural network; verify if symmetry matrix and other parameters are properly configured")
                
                np.savez_compressed(self.save_directory+'//conflict_angular_distribution1_debug.npz', codebars, index)
                np.savez_compressed(save_directory_+'//grain_init1.npz', codebars, loc)
                np.savez_compressed(self.save_directory+'//grain_classhkl_angbin1.npz', classhkl1, angbins)
        
        ## make comprehensive list of dictionary    
        normal_hkl_ = np.zeros((1,3))
        for j in classhkl:
            normal_hkl_ = np.vstack((normal_hkl_, hkl_all[str(j)]["normals"]))
        normal_hkl = np.delete(normal_hkl_, 0, axis =0)
        
        if material_ != material1_:
            normal_hkl1_ = np.zeros((1,3))
            for j in classhkl1:
                normal_hkl1_ = np.vstack((normal_hkl1_, hkl_all1[str(j)]["normals"]))
            normal_hkl1 = np.delete(normal_hkl1_, 0, axis =0)
        
        index_hkl = [j for j,k in enumerate(classhkl) for i in range(len(hkl_all[str(k)]["family"]))]
        
        if material_ != material1_:
            ind_offset = index_hkl[-1] + 1
            index_hkl1 = [ind_offset+j for j,k in enumerate(classhkl1) for i in range(len(hkl_all1[str(k)]["family"]))]
        
        if material_ == material1_:
            index_hkl1 = None
            normal_hkl1 = None
            classhkl1 = None
            hkl_all1 = None
            lattice_material1 = None
            # symmetry1 = None
        
        self.write_to_console("Generating "+type_+" and saving them")
        
        if mode == 1:
            if material_ != material1_:
                nb_grains_list = list(range(nb_grains+1))
                nb_grains1_list = list(range(nb_grains1+1))
                list_permute = list(itertools.product(nb_grains_list, nb_grains1_list))
                list_permute.pop(0)
                max_progress = len(list_permute)*grains_nb_simulate
            else:
                max_progress = nb_grains*grains_nb_simulate
            if self.include_scm:
                max_progress = max_progress + grains_nb_simulate
                if material_ != material1_:
                     max_progress = max_progress + 2*grains_nb_simulate
                     
        self.progress.setMaximum(max_progress)

        self._inputs_queue = Queue()
        self._outputs_queue = Queue()
        self._worker_process = {}
        for i in range(self.ncpu):
            self._worker_process[i]= Process(target=Window.worker_generation, args=(self._inputs_queue, 
                                                                              self._outputs_queue, 
                                                                              i+1),)
        for i in range(self.ncpu):
            self._worker_process[i].start()            
        time.sleep(0.1)    
        
        if mode == 1:
            if material_ != material1_:
                if self.modelp == "uniform":
                    if type_ =="training_data":
                        xlim, ylim = 0, int(0.8*2000)
                    else:
                        xlim, ylim = int(0.8*2000), 2000-1
                    
                    if grains_nb_simulate <= 2000:
                        path_array = resource_path("uniform_orientations_2000.npz")
                    else:
                        path_array = resource_path("uniform_orientations.npz")
                    arr = np.load(path_array)
                    
                    if symmetry == symmetry.cubic:
                        odf_data = arr["arr_6"][xlim:ylim]
                        print("Laue group 11")
                    elif symmetry == symmetry.hexagonal:
                        odf_data = arr["arr_5"][xlim:ylim]
                        print("Laue group 9")
                    elif symmetry == symmetry.trigonal:
                        odf_data = arr["arr_4"][xlim:ylim]
                        print("Laue group 7")
                    elif symmetry == symmetry.tetragonal:
                        odf_data = arr["arr_3"][xlim:ylim]
                        print("Laue group 5")
                    elif symmetry == symmetry.orthorhombic:
                        odf_data = arr["arr_2"][xlim:ylim]
                        print("Laue group 3")
                    elif symmetry == symmetry.monoclinic:
                        odf_data = arr["arr_1"][xlim:ylim]
                        print("Laue group 2")
                    elif symmetry == symmetry.triclinic:
                        odf_data = arr["arr_0"][xlim:ylim]
                        print("Laue group 1")
                                        
                    if symmetry1 == symmetry.cubic:
                        odf_data1 = arr["arr_6"][xlim:ylim]
                        print("Laue group 11")
                    elif symmetry1 == symmetry.hexagonal:
                        odf_data1 = arr["arr_5"][xlim:ylim]
                        print("Laue group 9")
                    elif symmetry1 == symmetry.trigonal:
                        odf_data1 = arr["arr_4"][xlim:ylim]
                        print("Laue group 7")
                    elif symmetry1 == symmetry.tetragonal:
                        odf_data1 = arr["arr_3"][xlim:ylim]
                        print("Laue group 5")
                    elif symmetry1 == symmetry.orthorhombic:
                        odf_data1 = arr["arr_2"][xlim:ylim]
                        print("Laue group 3")
                    elif symmetry1 == symmetry.monoclinic:
                        odf_data1 = arr["arr_1"][xlim:ylim]
                        print("Laue group 2")
                    elif symmetry1 == symmetry.triclinic:
                        odf_data1 = arr["arr_0"][xlim:ylim]
                        print("Laue group 1")
                ## list of combination of training dataset
                ## to be seen if this improves the prediction quality
                ## increases time significantly to generate the data 
                nb_grains_list = list(range(nb_grains+1))
                nb_grains1_list = list(range(nb_grains1+1))
                list_permute = list(itertools.product(nb_grains_list, nb_grains1_list))
                list_permute.pop(0) ## removing the 0,0 index
 
                # Idea 2 Or generate a database upto n grain LP
                values = []
                for i in range(len(list_permute)):
                    ii, jj = list_permute[i]
                    
                    for j in range(grains_nb_simulate):
                        if data_realism:
                            ## three types of data augmentation to mimic reality ?
                            if j < grains_nb_simulate*0.25:
                                noisy_data = False
                                remove_peaks = False
                            elif (j >= grains_nb_simulate*0.25) and (j < grains_nb_simulate*0.5):
                                noisy_data = True
                                remove_peaks = False
                            elif (j >= grains_nb_simulate*0.5) and (j < grains_nb_simulate*0.75):
                                noisy_data = False
                                remove_peaks = True
                            elif (j >= grains_nb_simulate*0.75):
                                noisy_data = True
                                remove_peaks = True
                        else:
                            noisy_data = False
                            remove_peaks = False
                        
                        if self.modelp == "uniform":
                            rand_choice = np.random.choice(len(odf_data), ii, replace=False)
                            rand_choice1 = np.random.choice(len(odf_data1), jj, replace=False)
                            data_odf_data = odf_data[rand_choice,:,:]
                            data_odf_data1 = odf_data1[rand_choice1,:,:]
                        else:
                            data_odf_data = None
                            data_odf_data1 = None
                        
                        seednumber = np.random.randint(1e6)
                        values.append([ii, jj, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        0, i, j, save_directory_, 
                                        data_odf_data,
                                        data_odf_data1,
                                        self.modelp,
                                        self.misorientation_angle])
                        
                chunks = Window.chunker_list(values, self.ncpu)
                chunks_mp = list(chunks)

                if self.include_scm:
                    meta = {'t1':time.time(),
                            'flag':0}
                else:
                    meta = {'t1':time.time(),
                            'flag':1}
                for ijk in range(int(self.ncpu)):
                    self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))

            else:
                # Idea 2 Or generate a database upto n grain LP
                if self.modelp == "uniform":
                    ## training split
                    if type_ =="training_data":
                        xlim, ylim = 0, int(0.8*2000)
                    else:
                        xlim, ylim = int(0.8*2000), 2000-1
                    
                    if grains_nb_simulate <= 2000:
                        path_array = resource_path("uniform_orientations_2000.npz")
                    else:
                        path_array = resource_path("uniform_orientations.npz")
                    arr = np.load(path_array)
                    
                    if symmetry == symmetry.cubic:
                        odf_data = arr["arr_6"][xlim:ylim]
                        print("Laue group 11")
                    elif symmetry == symmetry.hexagonal:
                        odf_data = arr["arr_5"][xlim:ylim]
                        print("Laue group 9")
                    elif symmetry == symmetry.trigonal:
                        odf_data = arr["arr_4"][xlim:ylim]
                        print("Laue group 7")
                    elif symmetry == symmetry.tetragonal:
                        odf_data = arr["arr_3"][xlim:ylim]
                        print("Laue group 5")
                    elif symmetry == symmetry.orthorhombic:
                        odf_data = arr["arr_2"][xlim:ylim]
                        print("Laue group 3")
                    elif symmetry == symmetry.monoclinic:
                        odf_data = arr["arr_1"][xlim:ylim]
                        print("Laue group 2")
                    elif symmetry == symmetry.triclinic:
                        odf_data = arr["arr_0"][xlim:ylim]
                        print("Laue group 1")

                values = []
                for i in range(nb_grains):
                    for j in range(grains_nb_simulate):
                        if data_realism:
                            ## three types of data augmentation to mimic reality ?
                            if j < grains_nb_simulate*0.25:
                                noisy_data = False
                                remove_peaks = False
                            elif (j >= grains_nb_simulate*0.25) and (j < grains_nb_simulate*0.5):
                                noisy_data = True
                                remove_peaks = False
                            elif (j >= grains_nb_simulate*0.5) and (j < grains_nb_simulate*0.75):
                                noisy_data = False
                                remove_peaks = True
                            elif (j >= grains_nb_simulate*0.75):
                                noisy_data = True
                                remove_peaks = True
                        else:
                            noisy_data = False
                            remove_peaks = False
                        
                        if self.modelp == "uniform":
                            rand_choice = np.random.choice(len(odf_data), i+1, replace=False)
                            data_odf_data = odf_data[rand_choice,:,:]
                            data_odf_data1 = None
                        else:
                            data_odf_data = None
                            data_odf_data1 = None
                            
                        seednumber = np.random.randint(1e6)
                        values.append([i+1, 0, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        0, i, j, save_directory_, 
                                        data_odf_data,
                                        data_odf_data1,
                                        self.modelp,
                                        self.misorientation_angle])
                chunks = Window.chunker_list(values, self.ncpu)
                chunks_mp = list(chunks)
                
                if self.include_scm:
                    meta = {'t1':time.time(),
                            'flag':0}
                else:
                    meta = {'t1':time.time(),
                            'flag':1}
                for ijk in range(int(self.ncpu)):
                    self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))

        if self.include_scm:
            self.write_to_console("Generating small angle misorientation single crystals")  
            values = []
            for i in range(grains_nb_simulate):
                if data_realism:
                    ## three types of data augmentation to mimic reality ?
                    if i < grains_nb_simulate*0.25:
                        noisy_data = False
                        remove_peaks = False
                    elif (i >= grains_nb_simulate*0.25) and (i < grains_nb_simulate*0.5):
                        noisy_data = True
                        remove_peaks = False
                    elif (i >= grains_nb_simulate*0.5) and (i < grains_nb_simulate*0.75):
                        noisy_data = False
                        remove_peaks = True
                    elif (i >= grains_nb_simulate*0.75):
                        noisy_data = True
                        remove_peaks = True
                else:
                    noisy_data = False
                    remove_peaks = False
                seednumber = np.random.randint(1e6)
                values.append([1, 0, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        1, i, i, save_directory_,
                                        None, None, self.modelp,
                                        self.misorientation_angle])
                
                if material_ != material1_:
                    seednumber = np.random.randint(1e6)
                    values.append([0, 1, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        2, i, i, save_directory_,
                                        None, None, self.modelp,
                                        self.misorientation_angle])
                    
                    ### include slightly misoriented two crystals of different materails
                    seednumber = np.random.randint(1e6)
                    values.append([1, 1, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        3, i, i, save_directory_,
                                        None, None, self.modelp,
                                        self.misorientation_angle])
                    
            chunks = Window.chunker_list(values, self.ncpu)
            chunks_mp = list(chunks)

            meta = {'t1':time.time(),
                    'flag':1}
            for ijk in range(int(self.ncpu)):
                self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))
                
        self.max_progress = max_progress
        while True:
            count = 0
            for i in range(self.ncpu):
                if not self._worker_process[i].is_alive():
                    self._worker_process[i].join()
                    count += 1
                else:
                    time.sleep(0.1)
                    self.progress.setValue(self.update_progress)
                    QApplication.processEvents()
                    
            if count == self.ncpu:
                self.progress.setValue(self.max_progress)
                QApplication.processEvents()
                return
        
    def update_data_mp(self):
        if not self._outputs_queue.empty():
            self.timermp.blockSignals(True)
            r_message = self._outputs_queue.get()
            self.update_progress = self.update_progress + r_message
            self.timermp.blockSignals(False)
            
    @staticmethod
    def chunker_list(seq, size):
        return (seq[i::size] for i in range(size))
    
    @staticmethod
    def getpatterns_(nb, nb1, material_=None, material1_=None, emin=5, emax=23, detectorparameters=None, pixelsize=None, 
                     sortintensity = False, ang_maxx = 45, step = 0.5, classhkl = None, classhkl1 = None, noisy_data=False, 
                     remove_peaks=False, seed = None,hkl_all=None, lattice_material=None, family_hkl=None,
                     normal_hkl=None, index_hkl=None, hkl_all1=None, lattice_material1=None, family_hkl1=None,
                     normal_hkl1=None, index_hkl1=None, dim1=2048, dim2=2048, removeharmonics=1, flag = 0,
                     img_i=None, img_j=None, save_directory_=None, odf_data=None, odf_data1=None, modelp=None,
                     misorientation_angle=None):
        
        s_tth, s_chi, s_miller_ind, _, _, _, ori_mat, ori_mat1 = Window.simulatemultiplepatterns(nb, nb1, seed=seed, key_material=material_, 
                                                                            key_material1=material1_,
                                                                            emin=emin, emax=emax,
                                                                             detectorparameters=detectorparameters,
                                                                             pixelsize=pixelsize,
                                                                             sortintensity = sortintensity, 
                                                                             dim1=dim1, dim2=dim2, 
                                                                             removeharmonics=removeharmonics,
                                                                             flag=flag, odf_data=odf_data,
                                                                             odf_data1=odf_data1, mode=modelp,
                                                                             misorientation_angle=misorientation_angle)
        if noisy_data:
            ## apply random gaussian type noise to the data (tth and chi)
            ## So adding noise to the angular distances
            ## Instead of adding noise to all HKL's ... Add to few selected HKLs
            ## Adding noise to randomly 30% of the HKLs
            ## Realistic way of introducting strains is through Pixels and not 2theta
            indices_noise = np.random.choice(len(s_tth), int(len(s_tth)*0.3), replace=False)
            noise_ = np.random.normal(0,0.05,len(indices_noise))
            s_tth[indices_noise] = s_tth[indices_noise] + noise_
            noise_ = np.random.normal(0,0.05,len(indices_noise)) 
            s_chi[indices_noise] = s_chi[indices_noise] + noise_
            
        if remove_peaks:
            len_mi = np.array([iq for iq in range(len(s_miller_ind))])
            len_mi = len_mi[int(0.5*len(s_miller_ind)):]
            indices_remove = np.random.choice(len_mi, int(len(len_mi)*0.3), replace=False)
            ## delete randomly selected less intense peaks
            ## to simulate real peak detection, where some peaks may not be
            ## well detected
            ## Include maybe Intensity approach: Delete peaks based on their SF and position in detector
            s_tth = np.delete(s_tth, indices_remove)
            s_chi = np.delete(s_chi, indices_remove)
            s_miller_ind = np.delete(s_miller_ind, indices_remove, axis=0)
            
        # replace all hkl class with relevant hkls
        ## better and faster way with PYMICRO library (list comparison; includes symmetry)
        location = []
        skip_hkl = []
        # count = 0
        for j, i in enumerate(s_miller_ind):
            if i[3] == 0: ##material 1
                h_obj = HklPlane(i[0],i[1],i[2], lattice=lattice_material)
                normal = np.round(h_obj.normal(), 6) 
                temp_ = np.all(normal == normal_hkl, axis=1)
                if len(np.where(temp_)[0]) == 1:
                    ind_ = np.where(temp_)[0][0]
                    location.append(index_hkl[ind_])
                elif len(np.where(temp_)[0]) == 0:
                    print("Entering -100 for "+ str(i) + "\n")
                    skip_hkl.append(j)
                elif len(np.where(temp_)[0]) > 1:
                    print("Entering -500: exiting as something is not proper with equivalent HKL module")
                    return
                
            elif i[3] == 1: ##material 2
                h_obj = HklPlane(i[0],i[1],i[2], lattice=lattice_material1)
                normal = np.round(h_obj.normal(), 6) 
                temp_ = np.all(normal == normal_hkl1, axis=1)
                if len(np.where(temp_)[0]) == 1:
                    ind_ = np.where(temp_)[0][0]
                    location.append(index_hkl1[ind_])
                elif len(np.where(temp_)[0]) == 0:
                    print("Entering -100 for "+ str(i) + "\n")
                    skip_hkl.append(j)
                elif len(np.where(temp_)[0]) > 1:
                    print("Entering -500: exiting as something is not proper with equivalent HKL module")
                    return
    
        allspots_the_chi = np.transpose(np.array([s_tth/2., s_chi]))
        tabledistancerandom = np.transpose(GT.calculdist_from_thetachi(allspots_the_chi, allspots_the_chi))
        
        codebars = []
        angbins = np.arange(0,ang_maxx+step,step)
        for i in range(len(tabledistancerandom)):
            if i in skip_hkl: ## not saving skipped HKL
                continue
            angles = tabledistancerandom[i]
            angles = np.delete(angles, i)# removing the self distance
            # fingerprint = np.histogram(angles, bins=angbins, density=False)[0]
            fingerprint = histogram1d(angles, range=[min(angbins),max(angbins)], bins=len(angbins)-1)
            ## same normalization as before
            max_codebars = np.max(fingerprint)
            fingerprint = fingerprint/ max_codebars
            codebars.append(fingerprint)
        
        if flag == 0:
            if len(codebars) != 0:
                np.savez_compressed(save_directory_+'//grain_'+str(img_i)+"_"+str(img_j)+'.npz', codebars, location, ori_mat, ori_mat1, flag)
            else:
                print("Skipping a simulation file: "+save_directory_+'//grain_'+str(img_i)+"_"+str(img_j)+'.npz'+"; Due to no data conforming user settings")
        elif flag == 1:
            if len(codebars) != 0:
                np.savez_compressed(save_directory_+'//grain_'+str(img_j)+'_smo.npz', codebars, location, ori_mat, ori_mat1, flag)
            else:
                print("Skipping a simulation file: "+save_directory_+'//grain_'+str(img_j)+'_smo.npz'+"; Due to no data conforming user settings")
        elif flag == 2:
            if len(codebars) != 0:
                np.savez_compressed(save_directory_+'//grain_'+str(img_j)+'_smo1.npz', codebars, location, ori_mat, ori_mat1, flag)
            else:
                print("Skipping a simulation file: "+save_directory_+'//grain_'+str(img_j)+'_smo1.npz'+"; Due to no data conforming user settings")
        elif flag == 3:
            if len(codebars) != 0:
                np.savez_compressed(save_directory_+'//grain_'+str(img_j)+'_smo2.npz', codebars, location, ori_mat, ori_mat1, flag)
            else:
                print("Skipping a simulation file: "+save_directory_+'//grain_'+str(img_j)+'_smo2.npz'+"; Due to no data conforming user settings")

    @staticmethod
    def Euler2OrientationMatrix(euler):
        """Compute the orientation matrix :math:`\mathbf{g}` associated with
        the 3 Euler angles :math:`(\phi_1, \Phi, \phi_2)`.
        :param euler: The triplet of the Euler angles (in degrees).
        :return g: The 3x3 orientation matrix.
        """
        (rphi1, rPhi, rphi2) = np.radians(euler)
        c1 = np.cos(rphi1)
        s1 = np.sin(rphi1)
        c = np.cos(rPhi)
        s = np.sin(rPhi)
        c2 = np.cos(rphi2)
        s2 = np.sin(rphi2)
        # rotation matrix g
        g11 = c1 * c2 - s1 * s2 * c
        g12 = s1 * c2 + c1 * s2 * c
        g13 = s2 * s
        g21 = -c1 * s2 - s1 * c2 * c
        g22 = -s1 * s2 + c1 * c2 * c
        g23 = c2 * s
        g31 = s1 * s
        g32 = -c1 * s
        g33 = c
        g = np.array([[g11, g12, g13], [g21, g22, g23], [g31, g32, g33]])
        return g

    @staticmethod
    def simulatemultiplepatterns(nbUBs, nbUBs1, seed=123, key_material=None, key_material1=None, 
                                 emin=5, emax=23, detectorparameters=None, pixelsize=None,
                                 sortintensity = False, dim1=2048, dim2=2048, removeharmonics=1, flag = 0,
                                 odf_data=None, odf_data1=None, mode="random", misorientation_angle = None):
        # UBelemagnles = np.random.random((3,nbUBs))*360-180
        orientation_send = []
        orientation_send1 = []
        if flag == 0:
            g = np.zeros((nbUBs, 3, 3))
            if key_material != key_material1:
                g1 = np.zeros((nbUBs1, 3, 3))

            if mode == "random":
                if key_material != key_material1:
                    for igr in range(nbUBs1):    
                        phi1 = rand1() * 360.
                        phi = 180. * acos(2 * rand1() - 1) / np.pi
                        phi2 = rand1() * 360.
                        g1[igr] = Window.Euler2OrientationMatrix((phi1, phi, phi2))
                        orientation_send1.append(g1[igr])
                        
                for igr in range(nbUBs):
                    phi1 = rand1() * 360.
                    phi = 180. * acos(2 * rand1() - 1) / np.pi
                    phi2 = rand1() * 360.
                    g[igr] = Window.Euler2OrientationMatrix((phi1, phi, phi2))
                    orientation_send.append(g[igr])
                    
            elif  mode == "uniform":
                if key_material != key_material1:
                    g1 = odf_data1
                    for igr in range(len(g1)):
                        orientation_send1.append(g1[igr])
                g = odf_data
                for igr in range(len(g)):
                    orientation_send.append(g[igr])
                
        elif flag == 1 or flag == 2 or flag == 3:
            nbUBs = 2
            g = np.zeros((nbUBs, 3, 3))
            for igr in range(nbUBs):
                if igr == 0:
                    phi1 = rand1() * 360.
                    phi = 180. * acos(2 * rand1() - 1) / np.pi
                    phi2 = rand1() * 360.
                    g[igr] = Window.Euler2OrientationMatrix((phi1, phi, phi2))
                    orientation_send.append(g[igr])
                elif igr == 1:
                    phi2 = phi2 + misorientation_angle ## adding user defined deg misorientation along phi2
                    g[igr] = Window.Euler2OrientationMatrix((phi1, phi, phi2))
                    orientation_send1.append(g[igr])                
    
        l_tth, l_chi, l_miller_ind, l_posx, l_posy, l_E, l_intensity = [],[],[],[],[],[],[]
        
        if flag == 1:
            for grainind in range(nbUBs):
                UBmatrix = g[grainind]
                grain = CP.Prepare_Grain(key_material, UBmatrix)
                s_tth, s_chi, s_miller_ind, s_posx, s_posy, s_E= LT.SimulateLaue_full_np(grain, emin, emax,
                                                                                         detectorparameters,
                                                                                         pixelsize=pixelsize,
                                                                                         dim=(dim1, dim2),
                                                                                         detectordiameter=None,
                                                                                         removeharmonics=removeharmonics)
                s_miller_ind = np.c_[s_miller_ind, np.zeros(len(s_miller_ind))]
                
                s_intensity = 1./s_E
                l_tth.append(s_tth)
                l_chi.append(s_chi)
                l_miller_ind.append(s_miller_ind)
                l_posx.append(s_posx)
                l_posy.append(s_posy)
                l_E.append(s_E)
                l_intensity.append(s_intensity)
                
        elif flag == 2:
            for grainind in range(nbUBs):
                UBmatrix = g[grainind]
                grain = CP.Prepare_Grain(key_material1, UBmatrix)
                s_tth, s_chi, s_miller_ind, s_posx, s_posy, s_E= LT.SimulateLaue_full_np(grain, emin, emax,
                                                                                         detectorparameters,
                                                                                         pixelsize=pixelsize,
                                                                                         dim=(dim1, dim2),
                                                                                         detectordiameter=None,
                                                                                         removeharmonics=removeharmonics)
                s_miller_ind = np.c_[s_miller_ind, np.ones(len(s_miller_ind))]
                
                s_intensity = 1./s_E
                l_tth.append(s_tth)
                l_chi.append(s_chi)
                l_miller_ind.append(s_miller_ind)
                l_posx.append(s_posx)
                l_posy.append(s_posy)
                l_E.append(s_E)
                l_intensity.append(s_intensity)
        
        elif flag == 3:
            for grainind in range(nbUBs):
                UBmatrix = g[grainind]
                if grainind == 0:
                    grain = CP.Prepare_Grain(key_material, UBmatrix)
                else:
                    grain = CP.Prepare_Grain(key_material1, UBmatrix)
                s_tth, s_chi, s_miller_ind, s_posx, s_posy, s_E= LT.SimulateLaue_full_np(grain, emin, emax,
                                                                                         detectorparameters,
                                                                                         pixelsize=pixelsize,
                                                                                         dim=(dim1, dim2),
                                                                                         detectordiameter=None,
                                                                                         removeharmonics=removeharmonics)
                s_miller_ind = np.c_[s_miller_ind, np.ones(len(s_miller_ind))]
                
                s_intensity = 1./s_E
                l_tth.append(s_tth)
                l_chi.append(s_chi)
                l_miller_ind.append(s_miller_ind)
                l_posx.append(s_posx)
                l_posy.append(s_posy)
                l_E.append(s_E)
                l_intensity.append(s_intensity)
        
        else:
            for grainind in range(nbUBs):
                UBmatrix = g[grainind]
                grain = CP.Prepare_Grain(key_material, UBmatrix)
                s_tth, s_chi, s_miller_ind, s_posx, s_posy, s_E= LT.SimulateLaue_full_np(grain, emin, emax,
                                                                                         detectorparameters,
                                                                                         pixelsize=pixelsize,
                                                                                         dim=(dim1, dim2),
                                                                                         detectordiameter=None,
                                                                                         removeharmonics=removeharmonics)
                s_miller_ind = np.c_[s_miller_ind, np.zeros(len(s_miller_ind))]
                
                s_intensity = 1./s_E
                l_tth.append(s_tth)
                l_chi.append(s_chi)
                l_miller_ind.append(s_miller_ind)
                l_posx.append(s_posx)
                l_posy.append(s_posy)
                l_E.append(s_E)
                l_intensity.append(s_intensity)
                
            if (key_material != key_material1):
                for grainind in range(nbUBs1):
                    UBmatrix = g1[grainind]
                    grain = CP.Prepare_Grain(key_material1, UBmatrix)
                    s_tth, s_chi, s_miller_ind, s_posx, s_posy, s_E= LT.SimulateLaue_full_np(grain, emin, emax,
                                                                                             detectorparameters,
                                                                                             pixelsize=pixelsize,
                                                                                             dim=(dim1, dim2),
                                                                                             detectordiameter=None,
                                                                                             removeharmonics=removeharmonics)
                    s_miller_ind = np.c_[s_miller_ind, np.ones(len(s_miller_ind))]
                    
                    s_intensity = 1./s_E
                    l_tth.append(s_tth)
                    l_chi.append(s_chi)
                    l_miller_ind.append(s_miller_ind)
                    l_posx.append(s_posx)
                    l_posy.append(s_posy)
                    l_E.append(s_E)
                    l_intensity.append(s_intensity)
                
        #flat_list = [item for sublist in l for item in sublist]
        s_tth = np.array([item for sublist in l_tth for item in sublist])
        s_chi = np.array([item for sublist in l_chi for item in sublist])
        s_miller_ind = np.array([item for sublist in l_miller_ind for item in sublist])
        s_posx = np.array([item for sublist in l_posx for item in sublist])
        s_posy = np.array([item for sublist in l_posy for item in sublist])
        s_E = np.array([item for sublist in l_E for item in sublist])
        s_intensity=np.array([item for sublist in l_intensity for item in sublist])
        
        if sortintensity:
            indsort = np.argsort(s_intensity)[::-1]
            s_tth=np.take(s_tth, indsort)
            s_chi=np.take(s_chi, indsort)
            s_miller_ind=np.take(s_miller_ind, indsort, axis=0)
            s_posx=np.take(s_posx, indsort)
            s_posy=np.take(s_posy, indsort)
            s_E=np.take(s_E, indsort)
            s_intensity=np.take(s_intensity, indsort)
            
        return s_tth, s_chi, s_miller_ind, s_posx, s_posy, s_intensity, orientation_send, orientation_send1
    
    @staticmethod
    def worker_generation(inputs_queue, outputs_queue, proc_id):
        while True:
            time.sleep(0.01)
            if not inputs_queue.empty():
                message = inputs_queue.get()
                num1, _, meta = message
                flag1 = meta['flag']
                for ijk in range(len(num1)):
                    nb, nb1, material_, material1_, emin, emax, detectorparameters, pixelsize, \
                     sortintensity, ang_maxx, step, classhkl, classhkl1, noisy_data, \
                     remove_peaks, seed,hkl_all, lattice_material, family_hkl,\
                     normal_hkl, index_hkl, hkl_all1, lattice_material1, family_hkl1,\
                     normal_hkl1, index_hkl1, dim1, dim2, removeharmonics, flag,\
                     img_i, img_j, save_directory_, odf_data, odf_data1, modelp,\
                         misorientation_angle = num1[ijk]
    
    
                    Window.getpatterns_(nb, nb1, material_, material1_, emin, emax, detectorparameters, pixelsize, \
                                             sortintensity, ang_maxx, step, classhkl, classhkl1, noisy_data, \
                                             remove_peaks, seed,hkl_all, lattice_material, family_hkl,\
                                             normal_hkl, index_hkl, hkl_all1, lattice_material1, family_hkl1,\
                                             normal_hkl1, index_hkl1, dim1, dim2, removeharmonics, flag,\
                                             img_i, img_j, save_directory_, odf_data, odf_data1, modelp, misorientation_angle)
                        
                    if ijk%10 == 0 and ijk!=0:
                        outputs_queue.put(11)
                if flag1 == 1:
                    break
    
    def write_training_testing_dataMTEX(self,):
        for imh in ["training_data", "testing_data"]:
            image_files = []
            path_ = self.save_directory+"//"+imh
            for dir_entry in os.listdir(path_):
                if os.path.isfile(os.path.join(path_, dir_entry)) and \
                        os.path.splitext(dir_entry)[1] in ACCEPTABLE_FORMATS:
                    file_name, file_extension = os.path.splitext(dir_entry)
                    image_files.append((file_name, file_extension,
                                        os.path.join(path_, dir_entry)))
            return_value = []
            for image_file, _, image_full_path in image_files:
                if image_file == "grain_classhkl_angbin" or image_file == "grain_classhkl_angbin1" or\
                    image_file == "grain_init" or image_file == "grain_init1":
                    continue
                return_value.append((image_full_path))
    
            ori_array1 = np.zeros((1,3,3))
            if self.material_ != self.material1_:
                ori_array2 = np.zeros((1,3,3))
            for bs in return_value:
                obj = np.load(bs)
                ori1 = obj["arr_2"]
                ori2 = obj["arr_3"] 
                flag = obj["arr_4"] 
                ## flag 0 is random data
                ## flag 1, 2, 3 are small angle miori data
                if flag == 0:
                    if len(ori1) != 0:
                        ori_array1 = np.vstack((ori_array1,ori1))
                    if self.material_ != self.material1_:
                        if len(ori2) != 0:
                            ori_array2 = np.vstack((ori_array2,ori2))
                        
            ori_array1 = np.delete(ori_array1, 0, axis=0)
            phase_ori1 = np.ones(len(ori_array1))
            
            ori_array = ori_array1
            phase_ori = phase_ori1
            if self.material_ != self.material1_:
                ori_array2 = np.delete(ori_array2, 0, axis=0)         
                phase_ori2 = np.ones(len(ori_array2))*2
                ori_array = np.vstack((ori_array, ori_array2))
                phase_ori = np.hstack((phase_ori, phase_ori2))
            
            if self.material_ == self.material1_:
                lattice = self.lattice_material
                material0_LG = material0_lauegroup
                header = [
                        "Channel Text File",
                        "Prj     lauetoolsnn",
                        "Author    [Ravi raj purohit]",
                        "JobMode    Grid",
                        "XCells    "+str(len(ori_array)),
                        "YCells    "+str(1),
                        "XStep    1.0",
                        "YStep    1.0",
                        "AcqE1    0",
                        "AcqE2    0",
                        "AcqE3    0",
                        "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
                        "Phases    1",
                        str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
                        str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
                            str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
                        "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]
            else:
                lattice = self.lattice_material
                lattice1 = self.lattice_material1
                material0_LG = material0_lauegroup
                material1_LG = material1_lauegroup
                header = [
                        "Channel Text File",
                        "Prj     lauetoolsnn",
                        "Author    [Ravi raj purohit]",
                        "JobMode    Grid",
                        "XCells    "+str(len(ori_array)),
                        "YCells    "+str(1),
                        "XStep    1.0",
                        "YStep    1.0",
                        "AcqE1    0",
                        "AcqE2    0",
                        "AcqE3    0",
                        "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
                        "Phases    2",
                        str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
                        str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
                            str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
                        str(lattice1._lengths[0]*10)+";"+str(lattice1._lengths[1]*10)+";"+\
                        str(lattice1._lengths[2]*10)+"\t"+str(lattice1._angles[0])+";"+\
                            str(lattice1._angles[1])+";"+str(lattice1._angles[2])+"\t"+"Material2"+ "\t"+material1_LG+ "\t"+"????"+"\t"+"????",
                        "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]
            # =================CALCULATION OF POSITION=====================================
            euler_angles = np.zeros((len(ori_array),3))
            phase_euler_angles = np.zeros(len(ori_array))
            for i in range(len(ori_array)):                
                euler_angles[i,:] = rot_mat_to_euler(ori_array[i,:,:])
                phase_euler_angles[i] = phase_ori[i]        
    
            a = euler_angles
            if self.material_ != self.material1_:
                filename125 = self.save_directory+ "//"+self.material_+"_"+self.material1_+"_MTEX_UBmat_"+imh+".ctf"
            else:
                filename125 = self.save_directory+ "//"+self.material_+"_MTEX_UBmat_"+imh+".ctf"
                
            f = open(filename125, "w")
            for ij in range(len(header)):
                f.write(header[ij]+" \n")
                    
            for j123 in range(euler_angles.shape[0]):
                y_step = 1
                x_step = 1 * j123
                phase_id = int(phase_euler_angles[j123])
                eul =  str(phase_id)+'\t' + "%0.4f" % x_step +'\t'+"%0.4f" % y_step+'\t8\t0\t'+ \
                                    "%0.4f" % a[j123,0]+'\t'+"%0.4f" % a[j123,1]+ \
                                        '\t'+"%0.4f" % a[j123,2]+'\t0.0001\t180\t0\n'
                string = eul
                f.write(string)
            f.close()
    
    def generate_training_data(self):
        ### using MP libraries
        self.ncpu = cpu_count()
        self.write_to_console("Using Multiprocessing ("+str(self.ncpu)+" cpus) for generation of simulated Laue patterns for training", to_push=1)
        self._inputs_queue = Queue()
        self._outputs_queue = Queue()
        ## Update data from multiprocessing
        self.update_progress = 0
        self.max_progress = 0
        self.timermp.setInterval(100) ## check every second (update the list of files in folder)
        self.timermp.timeout.connect(self.update_data_mp)
        self.timermp.start()
        
        self.write_to_console("Generating training dataset", to_push=1)
        self.status.showMessage("Training dataset generation in progress!")
        
        if self.input_params["hkl_max_identify"] == "auto" and self.input_params["hkl_max_identify1"] != "auto":
            self.write_to_console("Calculating the HKL bounds for training dataset", to_push=1)
            self.n, _ = self.temp_HKL(removeharmonics=1)
        elif self.input_params["hkl_max_identify"] == "auto" and self.input_params["hkl_max_identify1"] == "auto":
            self.write_to_console("Calculating the HKL bounds for training dataset", to_push=1)
            self.n, self.n1 = self.temp_HKL(removeharmonics=1)
        elif self.input_params["hkl_max_identify"] != "auto" and self.input_params["hkl_max_identify1"] == "auto":
            self.write_to_console("Calculating the HKL bounds for training dataset", to_push=1)
            _, self.n1 = self.temp_HKL(removeharmonics=1)
            
        ## generate reference HKL library      
        self.write_to_console("Directory for training dataset is : "+self.save_directory)
        ## procedure for generation of GROUND TRUTH classes
        # =============================================================================
        # VERY IMPORTANT; TAKES Significant time; verify again for other symmetries
        # =============================================================================
        self.run_(self.n, self.rules, self.lattice_material, self.symmetry, self.material_)
        if self.material_ != self.material1_:
            self.run_(self.n1, self.rules1, self.lattice_material1, self.symmetry1, self.material1_)
        
        ############ GENERATING TRAINING DATA  
        self.update_progress = 0
        self.max_progress = 0
        self.load_dataset(material_=self.material_, material1_=self.material1_, ang_maxx=self.maximum_angle_to_search,
                          step=self.step_for_binning, mode=self.mode_of_analysis, 
                          nb_grains=self.nb_grains_per_lp,
                          grains_nb_simulate=self.grains_nb_simulate,
                          data_realism = True, detectorparameters=self.detectorparameters, 
                          pixelsize=self.pixelsize, type_="training_data", var0=1,
                          dim1=self.input_params["dim1"], dim2=self.input_params["dim2"], removeharmonics=1)
                    ## var0 == 1; saves get_material_data()
        # ############ GENERATING TESTING DATA
        self.update_progress = 0
        self.max_progress = 0
        self.load_dataset(material_=self.material_, material1_=self.material1_, ang_maxx=self.maximum_angle_to_search,
                          step=self.step_for_binning, mode=self.mode_of_analysis, 
                          nb_grains=self.nb_grains_per_lp,
                          grains_nb_simulate=self.grains_nb_simulate//self.factor,
                          data_realism = True, detectorparameters=self.detectorparameters, 
                          pixelsize=self.pixelsize, type_="testing_data", var0=0,
                          dim1=self.input_params["dim1"], dim2=self.input_params["dim2"], removeharmonics=1)
        
        ## write MTEX data with training orientation
        self.write_training_testing_dataMTEX()
        
        self.status.showMessage("Training dataset generation completed with multi CPUs!")
        self.write_to_console("Press Train network button to Train")
        self.train_nn.setEnabled(True)

    def train_neural_network(self,):
        self.status.showMessage("Neural network training in progress!")
        self.train_nn.setEnabled(False)
        self.rmv_freq_class(freq_rmv=self.freq_rmv, elements=self.elements,
                            freq_rmv1=self.freq_rmv1, elements1=self.elements1)
        self.classhkl = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        self.angbins = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        self.loc_new = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_2"]
        with open(self.save_directory+"//class_weights.pickle", "rb") as input_file:
            class_weights = cPickle.load(input_file)
        self.class_weights = class_weights[0]
        ## load model and train
        self.model = self.model_arch_general(len(self.angbins)-1, len(self.classhkl),
                                             kernel_coeff= self.kernel_coeff, bias_coeff=self.bias_coeff, 
                                             lr=self.learning_rate)
        self.train_model()
        self.trialtoolbar1.setEnabled(True)
        self.predict_nn.setEnabled(True)
        # self.predict_nnc.setEnabled(True)
        self.predict_lnn.setEnabled(True)
        # self.predict_lnnc.setEnabled(True)
        self.status.showMessage("Neural network training completed!")
      
    def train_model(self, prefix="", tag = 0):
        if tag == 2:
            ## retraining from file
            try:
                self.classhkl = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
                self.angbins = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
                self.loc_new = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_2"]
                with open(self.save_directory+"//class_weights.pickle", "rb") as input_file:
                    class_weights = cPickle.load(input_file)
                self.class_weights = class_weights[0]
                ## need to compile again if loaded from file, better to just call the class, if architecture is same
                self.write_to_console("Constructing model")
                self.model = self.model_arch_general(len(self.angbins)-1, len(self.classhkl),
                                                     kernel_coeff= self.kernel_coeff, bias_coeff=self.bias_coeff, 
                                                     lr=self.learning_rate)
                list_of_files = glob.glob(self.save_directory+'//*.h5')
                latest_file = max(list_of_files, key=os.path.getctime)
                self.write_to_console("Taking the latest Weight file from the Folder: " + latest_file)
                load_weights = latest_file
                self.model.load_weights(load_weights)
                self.write_to_console("Uploading weights to model")
                self.write_to_console("All model files found and loaded")
            except:
                self.write_to_console("Model directory is not proper or files are missing. please configure the params")
                return
        ## temp function to quantify the spots and classes present in a batch
        batch_size = self.input_params["batch_size"] 
        trainy_inbatch = self.array_generator_verify(self.save_directory+"//training_data", batch_size, len(self.classhkl), self.loc_new)
        self.write_to_console("Number of spots in a batch of %i files : %i" %(batch_size, len(trainy_inbatch)))
        self.write_to_console("Min, Max class ID is %i, %i" %(np.min(trainy_inbatch), np.max(trainy_inbatch)))
        # try varying batch size and epochs
        epochs = self.input_params["epochs"] 
        ## Batch loading for numpy grain files (Keep low value to avoid overcharging the RAM)
        if self.material_ != self.material1_:
            nb_grains_list = list(range(self.nb_grains_per_lp+1))
            nb_grains1_list = list(range(self.nb_grains_per_lp1+1))
            list_permute = list(itertools.product(nb_grains_list, nb_grains1_list))
            list_permute.pop(0)
            # list_permute = list(itertools.permutations(range(self.nb_grains_per_lp+1), 2))
            # for ii in range(1,self.nb_grains_per_lp+1):
            #     list_permute.append((ii,ii))
            steps_per_epoch = (len(list_permute) * self.grains_nb_simulate)//batch_size
        else:
            steps_per_epoch = int((self.nb_grains_per_lp * self.grains_nb_simulate) / batch_size)
            
        val_steps_per_epoch = int(steps_per_epoch / self.factor)
        if steps_per_epoch == 0:
            steps_per_epoch = 1
        if val_steps_per_epoch == 0:
            val_steps_per_epoch = 1   
        ## Load generator objects from filepaths
        training_data_generator = self.array_generator(self.save_directory+"//training_data", batch_size, len(self.classhkl), self.loc_new)
        testing_data_generator = self.array_generator(self.save_directory+"//testing_data", batch_size, len(self.classhkl), self.loc_new)
        ######### TRAIN THE DATA
        self.progress.setMaximum(epochs*steps_per_epoch)
        # from clr_callback import CyclicLR
        # clr = CyclicLR(base_lr=0.0005, max_lr=0.001, step_size=steps_per_epoch*5, mode='triangular')
        es = EarlyStopping(monitor='val_accuracy', mode='max', patience=5)
        # es = EarlyStopping(monitor='categorical_crossentropy', patience=5)
        ms = ModelCheckpoint(self.save_directory+"//best_val_acc_model.h5", monitor='val_accuracy', mode='max', save_best_only=True)
        
        # model save directory and filename
        if self.material_ != self.material1_:
            model_name = self.save_directory+"//model_"+self.material_+"_"+self.material1_+prefix
        else:
            model_name = self.save_directory+"//model_"+self.material_+prefix
            
        log = LoggingCallback(self.write_to_console, self.progress, QApplication, self.model, model_name)

        stats_model = self.model.fit(
                                    training_data_generator, 
                                    epochs=epochs, 
                                    steps_per_epoch=steps_per_epoch,
                                    validation_data=testing_data_generator,
                                    validation_steps=val_steps_per_epoch,
                                    verbose=1,
                                    class_weight=self.class_weights,
                                    callbacks=[es, ms, log] # es, ms, clr
                                    )
        
        self.progress.setValue(epochs*steps_per_epoch)
        QApplication.processEvents() 
        # Save model config and weightsp
        if tag == 0:
            ## new trained model, save files
            model_json = self.model.to_json()
            with open(model_name+".json", "w") as json_file:
                json_file.write(model_json)            
        # serialize weights to HDF5
        self.model.save_weights(model_name+".h5")
        self.write_to_console("Saved model to disk")

        self.write_to_console( "Training Accuracy: "+str( stats_model.history['accuracy'][-1]))
        self.write_to_console( "Training Loss: "+str( stats_model.history['loss'][-1]))
        self.write_to_console( "Validation Accuracy: "+str( stats_model.history['val_accuracy'][-1]))
        self.write_to_console( "Validation Loss: "+str( stats_model.history['val_loss'][-1]))
        
        epochs = range(1, len(self.model.history.history['loss']) + 1)
        fig, ax = plt.subplots(1,2)
        ax[0].plot(epochs, self.model.history.history['loss'], 'r', label='Training loss')
        ax[0].plot(epochs, self.model.history.history['val_loss'], 'r', ls="dashed", label='Validation loss')
        ax[0].legend()
        ax[1].plot(epochs, self.model.history.history['accuracy'], 'g', label='Training Accuracy')
        ax[1].plot(epochs, self.model.history.history['val_accuracy'], 'g', ls="dashed", label='Validation Accuracy')
        ax[1].legend()
        if self.material_ != self.material1_:
            plt.savefig(self.save_directory+"//loss_accuracy_"+self.material_+"_"+self.material1_+prefix+".png", bbox_inches='tight',format='png', dpi=1000)
        else:
            plt.savefig(self.save_directory+"//loss_accuracy_"+self.material_+prefix+".png", bbox_inches='tight',format='png', dpi=1000)
        plt.close()
        
        if self.material_ != self.material1_:
            text_file = open(self.save_directory+"//loss_accuracy_logger_"+self.material_+"_"+self.material1_+prefix+".txt", "w")
        else:
            text_file = open(self.save_directory+"//loss_accuracy_logger_"+self.material_+prefix+".txt", "w")

        text_file.write("# EPOCH, LOSS, VAL_LOSS, ACCURACY, VAL_ACCURACY" + "\n")
        for inj in range(len(epochs)):
            string1 = str(epochs[inj]) + ","+ str(self.model.history.history['loss'][inj])+\
                    ","+str(self.model.history.history['val_loss'][inj])+","+str(self.model.history.history['accuracy'][inj])+\
                    ","+str(self.model.history.history['val_accuracy'][inj])+" \n"  
            text_file.write(string1)
        text_file.close()
        
        x_test, y_test = self.vali_array(self.save_directory+"//testing_data", 10, len(self.classhkl), self.loc_new)
        y_test = np.argmax(y_test, axis=-1)
        y_pred = np.argmax(self.model.predict(x_test), axis=-1)
        self.write_to_console(classification_report(y_test, y_pred))
        self.write_to_console( "Training is Completed; You can use the Retrain function to run for more epoch with varied batch size")
        self.write_to_console( "Training is Completed; You can use the Prediction and Live Prediction module now")
      
    def rmv_freq_class(self, freq_rmv = 0, elements="all", freq_rmv1 = 0, elements1="all"):
        classhkl0 = np.load(self.save_directory+"//grain_classhkl_angbin.npz")["arr_0"]
        self.write_to_console("First material index length: " + str(len(classhkl0)))
        ind_mat = np.array([ij for ij in range(len(classhkl0))])
        
        if self.material_ != self.material1_:
            classhkl1 = np.load(self.save_directory+"//grain_classhkl_angbin1.npz")["arr_0"]
            self.write_to_console("Second material index length: " + str(len(classhkl1)))
            pre_ind = ind_mat[-1] + 1
            ind_mat1 = np.array([pre_ind+ij for ij in range(len(classhkl1))])
            classhkl = np.vstack((classhkl0, classhkl1))
        else:
            classhkl = classhkl0
            # ind_mat = None
            ind_mat1 = None     
            elements1 = "all"
            freq_rmv1 = 0
        
        angbins = np.load(self.save_directory+"//grain_classhkl_angbin.npz")["arr_1"]
        loc = np.array([ij for ij in range(len(classhkl))])
        trainy_ = self.array_generatorV2(self.save_directory+"//training_data", ver=0)
        
        if self.material_ != self.material1_:
            ## split trainy_ for two materials index
            trainy_mat0 = []
            trainy_mat1 = []
            for ijnode in trainy_:
                if ijnode in ind_mat:
                    trainy_mat0.append(ijnode)
                elif ijnode in ind_mat1:
                    trainy_mat1.append(ijnode)
            trainy_mat0 = np.array(trainy_mat0)
            trainy_mat1 = np.array(trainy_mat1)
        else:
            trainy_mat0 = trainy_
            trainy_mat1 = None
                    
        self.write_to_console("Class ID and frequency; check for data imbalance and select appropriate LOSS function for training the model")
        
        ## lets extract the least common occuring classes to simply the training dataset
        if elements == "all":
            most_common0 = collections.Counter(trainy_mat0).most_common()
        else:
            most_common0 = collections.Counter(trainy_mat0).most_common()[:elements]
            
        if self.material_ != self.material1_:
            if elements1 =="all":
                most_common1 = collections.Counter(trainy_mat1).most_common()
            else:
                most_common1 = collections.Counter(trainy_mat1).most_common()[:elements1]
        else:
            most_common1 = []
                
        most_common = most_common0 + most_common1       
        print(most_common)

        class_present = [most_common[i][0] for i in range(len(most_common))]
        rmv_indices = []
        count = 0
        for i in loc:
            if i not in class_present:
                rmv_indices.append(i)
            elif i in class_present:
                ind_ = np.where(np.array(class_present)==i)[0]
                ij = most_common[ind_[0]]

                if self.material_ != self.material1_:
                    if (ij[0] in ind_mat) and (ij[1] <= freq_rmv):
                        rmv_indices.append(int(ij[0]))
                    if (ij[0] in ind_mat1) and (ij[1] <= freq_rmv1):
                        rmv_indices.append(int(ij[0]))
                else:
                    if (ij[1] <= freq_rmv):
                        rmv_indices.append(int(ij[0]))
            else:
                self.write_to_console("Something Fishy in Remove Freq Class module")
        
        if self.material_ != self.material1_:
            # ind_rmv_indmat = []
            # ind_rmv_indmat1 = []
            for i in rmv_indices:
                if i in ind_mat:
                    indd = np.where(ind_mat == i)[0]
                    ind_mat = np.delete(ind_mat, indd, axis=0)
                    # ind_rmv_indmat.append(i)
                elif i in ind_mat1:
                    indd = np.where(ind_mat1 == i)[0]
                    ind_mat1 = np.delete(ind_mat1, indd, axis=0)
                    # ind_rmv_indmat1.append(i)
        else:
            # ind_rmv_indmat = []
            for i in rmv_indices:
                if i in ind_mat:
                    indd = np.where(ind_mat == i)[0]
                    ind_mat = np.delete(ind_mat, indd, axis=0)
                    # ind_rmv_indmat.append(i)
                    
        loc_new = np.delete(loc, rmv_indices)

        occurances = [most_common[i][1] for i in range(len(most_common)) if int(most_common[i][0]) in loc_new]
        occurances = np.array(occurances)
        
        class_weight = {}
        class_weight_temp = {}
        count = 0
        for i in loc_new:
            for ij in most_common:
                if int(ij[0]) == i:
                    class_weight[count] = int(np.max(occurances)/ij[1]) ##+99 a quick hack to influence the weights
                    class_weight_temp[int(ij[0])] = int(np.max(occurances)/ij[1])
                    count += 1
        
        for occ in range(len(most_common)):
            if int(most_common[occ][0]) in loc_new:
                if int(most_common[occ][0]) == -100:
                    self.write_to_console("Unclassified HKL (-100); occurance : "+str(most_common[occ][1])+": NN_weights : 0.0")
                else:
                    self.write_to_console("HKL : " +str(classhkl[int(most_common[occ][0])])+"; occurance : "+str(most_common[occ][1])+\
                                          ": NN_weights : "+ str(class_weight_temp[int(most_common[occ][0])]))
        
        self.write_to_console(str(len(rmv_indices))+ " classes removed from the classHKL object [removal frequency: "+str(freq_rmv)+"] (before:"+str(len(classhkl))+", now:"+str(len(classhkl)-len(rmv_indices))+")")
        print(str(len(rmv_indices))+ " classes removed from the classHKL object [removal frequency: "+str(freq_rmv)+"] (before:"+str(len(classhkl))+", now:"+str(len(classhkl)-len(rmv_indices))+")")
                
        classhkl = np.delete(classhkl, rmv_indices, axis=0)
        ## save the altered classHKL object
        if self.material_ != self.material1_:
            np.savez_compressed(self.save_directory+'//MOD_grain_classhkl_angbin.npz', classhkl, angbins, loc_new, 
                                rmv_indices, freq_rmv, len(ind_mat), len(ind_mat1))
        else:
            np.savez_compressed(self.save_directory+'//MOD_grain_classhkl_angbin.npz', classhkl, angbins, loc_new, 
                                rmv_indices, freq_rmv)
        with open(self.save_directory + "//class_weights.pickle", "wb") as output_file:
            cPickle.dump([class_weight], output_file)
        self.write_to_console("Saved class weights data")

    def array_generator(self, path_, batch_size, n_classes, loc_new):
        """
        Assign a new class to data that is removed (to include in the training anyway)
        """
        array_pairs = self.get_path(path_, ver=0)
        random.shuffle(array_pairs)
        zipped = itertools.cycle(array_pairs)
        while True:
            temp_var = False
            for bs in range(batch_size):
                array_path = next(zipped)
                obj = np.load(array_path)
                trainX = obj["arr_0"]
                loc1 = obj["arr_1"]
                
                if len(trainX) == 0 or len(loc1) == 0:
                    self.write_to_console("Skipping File: "+ array_path+"; No data is found")
                    if bs == 0:
                        temp_var = True
                    continue                
                
                ## remove the non frequent class and rearrange the data
                loc1_new = []
                loc1_new_rmv = []
                for k, i in enumerate(loc1):
                    temp_loc = np.where(loc_new==i)[0]
                    if len(temp_loc) == 1:
                        loc1_new.append(temp_loc)
                    else:
                        loc1_new_rmv.append(k)   
                   
                loc1_new = np.array(loc1_new).ravel()
                loc1_new_rmv = np.array(loc1_new_rmv).ravel() 
                
                if len(trainX) != len(loc1_new):
                    if len(loc1_new_rmv) > 0:
                        trainX = np.delete(trainX, loc1_new_rmv, axis=0) 

                if bs == 0 or temp_var:
                    trainX1 = np.copy(trainX)
                    trainY1 = np.copy(loc1_new)
                else:
                    trainX1 = np.vstack((trainX1, trainX))
                    trainY1 = np.hstack((trainY1, loc1_new))

            ## To normalize the size of one hot encoding
            count = 0
            if np.min(trainY1) != 0:
                trainY1 = np.append(trainY1, 0)
                count += 1
            if np.max(trainY1) != (n_classes-1):
                trainY1 = np.append(trainY1, n_classes-1)
                count += 1
                
            trainY1 = to_categorical(trainY1)
            if count == 1:
                trainY1 = np.delete(trainY1, [len(trainY1)-1] ,axis=0)
            elif count == 2:
                trainY1 = np.delete(trainY1, [len(trainY1)-1,len(trainY1)-2] ,axis=0)
    
            yield trainX1, trainY1
            
    def vali_array(self, path_, batch_size, n_classes, loc_new):
        array_pairs = self.get_path(path_, ver=0)
        random.shuffle(array_pairs)
        zipped = itertools.cycle(array_pairs)
        temp_var = False
        for bs in range(batch_size):
            array_path = next(zipped)
            obj = np.load(array_path)
            trainX = obj["arr_0"]
            loc1 = obj["arr_1"]
            
            if len(trainX) == 0 or len(loc1) == 0:
                self.write_to_console("Skipping File: "+ array_path+"; No data is found")
                if bs == 0:
                    temp_var = True
                continue
            
            ## remove the non frequent class and rearrange the data
            loc1_new = []
            loc1_new_rmv = []
            for k, i in enumerate(loc1):
                temp_loc = np.where(loc_new==i)[0]
                if len(temp_loc) == 1:
                    loc1_new.append(temp_loc)
                else:
                    loc1_new_rmv.append(k)
            
            loc1_new = np.array(loc1_new).ravel()
            loc1_new_rmv = np.array(loc1_new_rmv).ravel()
            
            if len(trainX) != len(loc1_new):
                if len(loc1_new_rmv) > 0:
                    trainX = np.delete(trainX, loc1_new_rmv, axis=0)
                
            if bs == 0 or temp_var:
                trainX1 = trainX
                trainY1 = loc1_new
            else:
                trainX1 = np.vstack((trainX1, trainX))
                trainY1 = np.hstack((trainY1, loc1_new))
        
        count = 0
        if np.min(trainY1) != 0:
            trainY1 = np.append(trainY1, 0)
            count += 1
        if np.max(trainY1) != (n_classes-1):
            trainY1 = np.append(trainY1, n_classes-1)
            count += 1
            
        trainY1 = to_categorical(trainY1)
        if count == 1:
            trainY1 = np.delete(trainY1, [len(trainY1)-1] ,axis=0)
        elif count == 2:
            trainY1 = np.delete(trainY1, [len(trainY1)-1,len(trainY1)-2] ,axis=0)
    
        return trainX1, trainY1

    def get_path(self, path_, ver=0):
        image_files = []
        for dir_entry in os.listdir(path_):
            if os.path.isfile(os.path.join(path_, dir_entry)) and \
                    os.path.splitext(dir_entry)[1] in ACCEPTABLE_FORMATS:
                file_name, file_extension = os.path.splitext(dir_entry)
                image_files.append((file_name, file_extension,
                                    os.path.join(path_, dir_entry)))
        return_value = []
        for image_file, _, image_full_path in image_files:
            if image_file == "grain_classhkl_angbin":
                continue
            if image_file == "grain_classhkl_angbin1":
                continue
            if ver == 1 and image_file == "grain_init":
                continue
            if ver == 1 and image_file == "grain_init1":
                continue
            return_value.append((image_full_path))
        return return_value
    
    def array_generator_verify(self, path_, batch_size, n_classes, loc_new):
        array_pairs = self.get_path(path_, ver=1)
        random.shuffle(array_pairs)
        zipped = itertools.cycle(array_pairs)
        while True:
            temp_var = False
            for bs in range(batch_size):
                array_path = next(zipped)
                obj = np.load(array_path)
                loc1 = obj["arr_1"]            
                if len(loc1) == 0:
                    self.write_to_console("Skipping File: "+ array_path+"; No data is found")
                    if bs == 0:
                        temp_var = True
                    continue             
                ## remove the non frequent class and rearrange the data
                loc1_new = []
                for k, i in enumerate(loc1):
                    temp_loc = np.where(loc_new==i)[0]
                    if len(temp_loc) == 1:
                        loc1_new.append(temp_loc)     
                loc1_new = np.array(loc1_new).ravel()
                if bs == 0 or temp_var:
                    trainY1 = np.copy(loc1_new)
                else:
                    trainY1 = np.hstack((trainY1, loc1_new)) 
            return trainY1
    
    def array_generatorV2(self, path_, ver=1):
        array_pairs = self.get_path(path_, ver=ver)
        random.shuffle(array_pairs)
        self.progress.setMaximum(len(array_pairs))
        for bs in range(len(array_pairs)):
            loc1 = np.load(array_pairs[bs])["arr_1"]
            
            if bs == 0:
                trainY1 = loc1
            if bs > 0:
                trainY1 = np.hstack((trainY1, loc1))
            self.progress.setValue(bs+1)
            QApplication.processEvents() 
        return trainY1
    
    def model_arch_general(self, n_bins, n_outputs, kernel_coeff = 0.0005, bias_coeff = 0.0005, lr=None, verbose=1):
        """
        Very simple and straight forward Neural Network with few hyperparameters
        straighforward RELU activation strategy with cross entropy to identify the HKL
        Tried BatchNormalization --> no significant impact
        Tried weighted approach --> not better for HCP
        Trying Regularaization 
        l2(0.001) means that every coefficient in the weight matrix of the layer 
        will add 0.001 * weight_coefficient_value**2 to the total loss of the network
        """
        if n_outputs >= n_bins:
            param = n_bins
            if param*15 < (2*n_outputs): ## quick hack; make Proper implementation
                param = (n_bins + n_outputs)//2
        else:
            # param = n_outputs ## More reasonable ???
            param = n_outputs*2 ## More reasonable ???
            # param = n_bins//2
            
        model = Sequential()
        model.add(keras.Input(shape=(n_bins,)))
        ## Hidden layer 1
        model.add(Dense(n_bins, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.3)) ## Adding dropout as we introduce some uncertain data with noise
        ## Hidden layer 2
        model.add(Dense(((param)*15 + n_bins)//2, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.3))
        ## Hidden layer 3
        model.add(Dense((param)*15, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.3))
        ## Output layer 
        model.add(Dense(n_outputs, activation='softmax'))
        ## Compile model
        if lr != None:
            otp = tf.keras.optimizers.Adam(learning_rate=lr)
            model.compile(loss='categorical_crossentropy', optimizer=otp, metrics=[metricsNN])
        else:
            model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=[metricsNN])
        
        if verbose == 1:
            model.summary()
            stringlist = []
            model.summary(print_fn=lambda x: stringlist.append(x))
            short_model_summary = "\n".join(stringlist)
            self.write_to_console(short_model_summary)
        return model
    
    def grid_search_hyperparams(self,): 
        classhkl = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        angbins = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        loc_new = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_2"]
        with open(self.save_directory+"//class_weights.pickle", "rb") as input_file:
            class_weights = cPickle.load(input_file)
        class_weights = class_weights[0]
        
        batch_size = self.input_params["batch_size"] 
        trainy_inbatch = self.array_generator_verify(self.save_directory+"//training_data", batch_size, len(classhkl), loc_new)
        self.write_to_console("Number of spots in a batch of %i files : %i" %(batch_size, len(trainy_inbatch)))
        self.write_to_console("Min, Max class ID is %i, %i" %(np.min(trainy_inbatch), np.max(trainy_inbatch)))
        self.write_to_console("Starting hypergrid optimization: looking in a grid to optimize the learning rate and regularization coefficients.")
        # try varying batch size and epochs
        epochs = 1 #self.input_params["epochs"] 
        ## Batch loading for numpy grain files (Keep low value to avoid overcharging the RAM)
        steps_per_epoch = int((self.nb_grains_per_lp * self.grains_nb_simulate)/batch_size)
        val_steps_per_epoch = int(steps_per_epoch /self.factor)
        if steps_per_epoch == 0:
            steps_per_epoch = 1
        if val_steps_per_epoch == 0:
            val_steps_per_epoch = 1
        ## Load generator objects from filepaths
        training_data_generator = self.array_generator(self.save_directory+"//training_data", batch_size, len(classhkl), loc_new)
        testing_data_generator = self.array_generator(self.save_directory+"//testing_data", batch_size, len(classhkl), loc_new)

        # grid search values
        values = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
        
        all_train, all_test = list(), list()
        all_trainL, all_testL = list(), list()
        parameters = list()
        
        text_file = open(self.save_directory+"//parameter_hypergrid_"+self.material_+".txt", "w")
        text_file.write("# Iter, Learning_Rate, Bias_Coeff, Kernel_Coeff, Train_Acc, Train_Loss, Test_Acc, Test_Loss, LR_index, BC_index, KC_index" + "\n")
        
        self.progress.setMaximum(len(values)*len(values)*len(values))

        iter_cnt= 0 
        for i, param in enumerate(values):
            for j, param1 in enumerate(values):
                for k, param2 in enumerate(values):
                        # define model
                    iter_cnt += 1

                    model = self.model_arch_general(len(angbins)-1, len(classhkl), 
                                                       kernel_coeff = param2, 
                                                       bias_coeff = param1,
                                                       lr = param, verbose=0)
                        # fit model
                    stats_model = model.fit(
                                            training_data_generator, 
                                            epochs=epochs, 
                                            steps_per_epoch=steps_per_epoch,
                                            validation_data=testing_data_generator,
                                            validation_steps=val_steps_per_epoch,
                                            verbose=0,
                                            class_weight=class_weights,
                                            )
    
                        # evaluate the model
                    train_acc = stats_model.history['accuracy'][-1]
                    test_acc = stats_model.history['val_accuracy'][-1]
                    train_loss = stats_model.history['loss'][-1]
                    test_loss = stats_model.history['val_loss'][-1]
                    all_train.append(train_acc)
                    all_test.append(test_acc)
                    all_trainL.append(train_loss)
                    all_testL.append(test_loss)
                    parameters.append([param,param1,param2])
                    
                    string1 = str(iter_cnt) +","+ str(param) + ","+ str(param1)+\
                                ","+str(param2)+","+str(train_acc)+\
                                ","+str(train_loss)+ ","+str(test_acc)+","+str(test_loss)+","+ str(i) + ","+ str(j)+\
                                    ","+str(k)+ " \n"  
                    text_file.write(string1)                  
                    self.progress.setValue(iter_cnt)
                    QApplication.processEvents()         
        text_file.close()
    
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, subplot=1, mat_bool=True):
        fig = Figure(figsize=(width, height), dpi=dpi)
        if mat_bool:
            self.axes = fig.add_subplot(131)
            self.axes1 = fig.add_subplot(132)
            self.axes2 = fig.add_subplot(133)
        else:
            self.axes = fig.add_subplot(141)
            self.axes1 = fig.add_subplot(142)
            self.axes2 = fig.add_subplot(143)
            self.axes3 = fig.add_subplot(144)
        super(MplCanvas, self).__init__(fig)

class sample_config(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self._createDisplay() ## display screen
        
        texttstr = "\n\
### config file for LaueNeuralNetwork \n\
## comments\n\
\n\
[GLOBAL_DIRECTORY]\n\
prefix = \n\
## directory where all training related data and results will be saved \n\
main_directory = C:\\Users\\purushot\\Desktop\\pattern_matching\\experimental\\GUIv0\\latest_version\n\
\n\
[MATERIAL]\n\
## same material key as lauetools (see dictlauetools.py for complete key)\n\
## as of now symmetry can be cubic, hexagonal, orthorhombic, tetragonal, trigonal, monoclinic, triclinic\n\
\n\
material = In2Bi\n\
symmetry = hexagonal\n\
\n\
## if second phase is present, else none\n\
material1 = In_epsilon\n\
symmetry1 = tetragonal\n\
\n\
[DETECTOR]\n\
## path to detector calibration file (.det)\n\
detectorfile = C:\\Users\\purushot\\Desktop\\In_JSM\\calib.det\n\
## Max and Min energy to be used for generating training dataset, as well as for calcualting matching rate\n\
emax = 21\n\
emin = 5\n\
\n\
[TRAINING]\n\
## classes_with_frequency_to_remove: HKL class with less appearance than specified will be ignored in output\n\
## desired_classes_output : can be all or an integer: to limit the number of output classes\n\
## max_HKL_index : can be auto or integer: Maximum index of HKL to build output classes\n\
## max_nb_grains : Maximum number of grains to simulate per lauepattern\n\
####### Material 0\n\
classes_with_frequency_to_remove = 500\n\
desired_classes_output = all\n\
max_HKL_index = 5\n\
max_nb_grains = 1\n\
####### Material 1\n\
## HKL class with less appearance than specified will be ignored in output\n\
classes_with_frequency_to_remove1 = 500\n\
desired_classes_output1 = all\n\
max_HKL_index1 = 5\n\
max_nb_grains1 = 1\n\
\n\
## Max number of simulations per number of grains\n\
## Include single crystal misorientation (1 deg) data in training\n\
## Maximum angular distance to probe (in deg)\n\
## step size in angular distribution to discretize (in deg)\n\
## batch size and epochs for training\n\
max_simulations = 1000\n\
include_small_misorientation = false\n\
misorientation_angle = 30\n\
angular_distance = 90\n\
step_size = 0.1\n\
batch_size = 50\n\
epochs = 5\n\
\n\
[PREDICTION]\n\
# model_weight_file: if none, it will select by default the latest H5 weight file, else provide a specific model\n\
# softmax_threshold_global: thresholding to limit the predicted spots search zone\n\
# mr_threshold_global: thresholding to ignore all matricies less than the MR threshold\n\
# cap_matchrate: any UB matrix providing MR less than this will be ignored\n\
# coeff: should be same as cap_matchrate or no? (this is for try previous UB matrix)\n\
# coeff_overlap: coefficient to limit the overlapping between spots; if more than this, new solution will be computed\n\
# mode_spotCycle: How to cycle through predicted spots (slow or fast or multiorimat) ##slow is more reliable but slow as the name suggests\n\
UB_matrix_to_detect = 1\n\
image_grid_x = 51\n\
image_grid_y = 51\n\
\n\
matrix_tolerance = 0.9\n\
matrix_tolerance1 = 0.9\n\
\n\
material0_limit = 1\n\
material1_limit = 1\n\
\n\
model_weight_file = none\n\
softmax_threshold_global = 0.85\n\
mr_threshold_global = 0.80\n\
cap_matchrate = 0.01\n\
coeff = 0.3\n\
coeff_overlap = 0.3\n\
mode_spotCycle = slow\n\
##true for few crystal and prefered texture case, otherwise time consuming; advised for single phase alone\n\
use_previous = true\n\
\n\
[EXPERIMENT]\n\
experiment_directory = C:\\Users\\purushot\\Desktop\\In_JSM\\ech875_ROI01\n\
experiment_file_prefix = ech875_ROI01_\n\
\n\
[PEAKSEARCH]\n\
intensity_threshold = 90\n\
boxsize = 15\n\
fit_peaks_gaussian = 1\n\
FitPixelDev = 15\n\
NumberMaxofFits = 3000\n\
\n\
[STRAINCALCULATION]\n\
strain_compute = true\n\
tolerance_strain_refinement = 0.7,0.6,0.5,0.4,0.3,0.2\n\
tolerance_strain_refinement1 = 0.7,0.6,0.5,0.4,0.3,0.2\n\
\n\
[POSTPROCESS]\n\
hkls_subsets = [1,1,0],[1,0,0],[1,1,1]\n\
\n\
[DEVELOPMENT]\n\
# could be 1 or 2 / none in case of single phase\n\
material_phase_always_present = 1\n\
write_MTEX_file = true\n\
material0_lauegroup = 9\n\
material1_lauegroup = 5\n\
\n\
# Laue Groups\n\
#group 1 -- triclinic: '-1'\n\
#group 2 -- monoclinic: '2/m'\n\
#group 3 -- orthorhombic: 'mmm'\n\
#group 4 -- tetragonal: '4/m'\n\
#group 5 -- tetragonal: '4/mmm'\n\
#group 6 -- trigonal: '-3'\n\
#group 7 -- trigonal: '-3m'\n\
#group 8 -- hexagonal: '6/m'\n\
#group 9 -- hexagonal: '6/mmm'\n\
#group 10 -- cubic: 'm3'\n\
#group 11 -- cubic: 'm3m'"
        self.setDisplayText(texttstr)

    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()
        
class MyPopup(QWidget):
    def __init__(self, match_rate12, rotation_matrix12, mat_global12, fR_pix12, filename, 
                 straincrystal, strainsample, end_time, 
                 match_rate12fast, rotation_matrix12fast, mat_global12fast, fR_pix12fast, 
                 straincrystalfast, strainsamplefast, end_timefast,
                 match_rate12beamtime, rotation_matrix12beamtime, mat_global12beamtime, fR_pix12beamtime, 
                 straincrystalbeamtime, strainsamplebeamtime, end_timebeamtime,
                  match_rate12multiorimat, rotation_matrix12multiorimat, mat_global12multiorimat, fR_pix12multiorimat, 
                  straincrystalmultiorimat, strainsamplemultiorimat, end_timemultiorimat):
        QWidget.__init__(self)
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self._createDisplay() ## display screen

        texttstr = "Predicted for File: "+filename+ " \n" 
        self.setDisplayText(texttstr)
        self.setDisplayText("################## SLOW MODE ############### \n")
        for ijk in range(len(match_rate12)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystal[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsample[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_time) + " \n"
            self.setDisplayText(texttstr)        
        
        self.setDisplayText("################## FAST MODE ############### \n")
        for ijk in range(len(match_rate12fast)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12fast[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12fast[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12fast[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystalfast[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsamplefast[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12fast[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_timefast) + " \n"
            self.setDisplayText(texttstr)    
            
        self.setDisplayText("################## BEAMTIME MODE ############### \n")
        for ijk in range(len(match_rate12beamtime)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12beamtime[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12beamtime[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12beamtime[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystalbeamtime[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsamplebeamtime[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12beamtime[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_timebeamtime) + " \n"
            self.setDisplayText(texttstr)    
            
        self.setDisplayText("################## GRAPHMODE MODE ############### \n")
        for ijk in range(len(match_rate12multiorimat)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12multiorimat[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12multiorimat[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12multiorimat[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystalmultiorimat[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsamplemultiorimat[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12multiorimat[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_timemultiorimat) + " \n"
            self.setDisplayText(texttstr)
            
    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()

class AnotherWindowParams(QWidget):
    got_signal = QtCore.pyqtSignal(dict)
    def __init__(self, state=0, gui_state=0):
        super().__init__()
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.settings = QSettings("config_data_"+str(gui_state),"ConfigGUI_"+str(gui_state))
        ## Material detail        
        self.dict_LT = QComboBox()
        sortednames = sorted(dictLT.dict_Materials.keys(), key=lambda x:x.lower())
        for s in sortednames:
            self.dict_LT.addItem(s)
        
        self.dict_LT1 = QComboBox()
        sortednames = sorted(dictLT.dict_Materials.keys(), key=lambda x:x.lower())
        for s in sortednames:
            self.dict_LT1.addItem(s)
        
        if main_directory != None:
            self.modelDirecSave = main_directory
        else:
            self.modelDirecSave = None
        self.model_direc_save = QPushButton('Browse')
        self.model_direc_save.clicked.connect(self.getfiles)
        
        self.symmetry = QComboBox()
        symmetry_names = ["cubic","hexagonal","orthorhombic","tetragonal","trigonal","monoclinic","triclinic"]
        for s in symmetry_names:
            self.symmetry.addItem(s)
        
        self.symmetry1 = QComboBox()
        symmetry_names = ["cubic","hexagonal","orthorhombic","tetragonal","trigonal","monoclinic","triclinic"]
        for s in symmetry_names:
            self.symmetry1.addItem(s)
        
        self.prefix = QLineEdit()
        self.prefix.setText("") ## Prefix for folder
        
        self.hkl_max = QLineEdit()
        self.hkl_max.setText("auto") ## auto or some indices of HKL
        
        self.elements = QLineEdit()
        self.elements.setText("200") ## all or some length
        
        self.freq_rmv = QLineEdit()
        self.freq_rmv.setText("1") ## auto or some indices of HKL
        
        self.hkl_max1 = QLineEdit()
        self.hkl_max1.setText("auto") ## auto or some indices of HKL
        
        self.elements1 = QLineEdit()
        self.elements1.setText("200") ## all or some length
        
        self.freq_rmv1 = QLineEdit()
        self.freq_rmv1.setText("1") ## auto or some indices of HKL
        
        self.maximum_angle_to_search = QLineEdit()
        self.maximum_angle_to_search.setText("90")
        
        self.step_for_binning = QLineEdit()
        self.step_for_binning.setText("0.1")
        
        self.mode_of_analysis = QComboBox()
        mode_ = ["1","0"]
        for s in mode_:
            self.mode_of_analysis.addItem(s)
            
        self.nb_grains_per_lp = QLineEdit()
        self.nb_grains_per_lp.setText("5")
        
        self.nb_grains_per_lp1 = QLineEdit()
        self.nb_grains_per_lp1.setText("5")
        
        self.grains_nb_simulate = QLineEdit()
        self.grains_nb_simulate.setText("500")
        
        self.detectordistance = QLineEdit()
        self.detectordistance.setText("79.553")
        
        self.xycenter = QLineEdit()
        self.xycenter.setText("979.32,932.31")
        
        self.bgdetector = QLineEdit()
        self.bgdetector.setText("0.37,0.447")
        
        self.detectordim = QLineEdit()
        self.detectordim.setText("2018,2016")
        
        self.pixelsize = QLineEdit()
        self.pixelsize.setText("0.0734")
        
        self.minmaxE = QLineEdit()
        self.minmaxE.setText("5,18")
        
        self.include_scm = QComboBox()
        modes = ["no", "yes"]
        for s in modes:
            self.include_scm.addItem(s)
            
        self.architecture = QComboBox()
        modes = ["Classical-inbuilt","from file"]
        for s in modes:
            self.architecture.addItem(s)
            
        self.learningrate_rc = QLineEdit()
        self.learningrate_rc.setText("1e-3,1e-5,1e-6")

        self.mode_nn = QComboBox()
        modes = ["Generate Data & Train","Train","Predict"]
        for s in modes:
            self.mode_nn.addItem(s)
        
        self.batch_size = QLineEdit()
        self.batch_size.setText("20")
        
        self.epochs = QLineEdit()
        self.epochs.setText("5")
        
        self.grid_search_hyperparams = QComboBox()
        mode_ = ["False","True"]
        for s in mode_:
            self.grid_search_hyperparams.addItem(s)
            
        self.texture_model = QComboBox()
        mode_ = ["in-built_Uniform_Distribution","random","from file"]
        for s in mode_:
            self.texture_model.addItem(s)
            
        # button to continue training
        self.btn_config = QPushButton('Accept')
        self.btn_config.clicked.connect(self.send_details_mainGUI)
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.close)

        ### set some default values
        if freq_rmv_global != None:
            self.freq_rmv.setText(str(freq_rmv_global))
        if elements_global != None:
            self.elements.setText(elements_global)
        if hkl_max_global != None:
            self.hkl_max.setText(hkl_max_global)
        if nb_grains_per_lp_global != None:
            self.nb_grains_per_lp.setText(str(nb_grains_per_lp_global))
        
        if freq_rmv1_global != None:
            self.freq_rmv1.setText(str(freq_rmv1_global))
        if elements1_global != None:
            self.elements1.setText(elements1_global)
        if hkl_max1_global != None:
            self.hkl_max1.setText(hkl_max1_global)
        if nb_grains_per_lp1_global != None:
            self.nb_grains_per_lp1.setText(str(nb_grains_per_lp1_global))
            
        if include_scm_global:
            self.include_scm.setCurrentText("yes")
        else:
            self.include_scm.setCurrentText("no")
            
        if batch_size_global != None:
            self.batch_size.setText(str(batch_size_global))
        if epochs_global != None:
            self.epochs.setText(str(epochs_global))  
            
        if maximum_angle_to_search_global != None:
            self.maximum_angle_to_search.setText(str(maximum_angle_to_search_global))
        if step_for_binning_global != None:
            self.step_for_binning.setText(str(step_for_binning_global))
        if grains_nb_simulate_global != None:
            self.grains_nb_simulate.setText(str(grains_nb_simulate_global))    
            
        if symmetry_global != None:
            self.symmetry.setCurrentText(symmetry_global)
        if symmetry1_global != None:
            self.symmetry1.setCurrentText(symmetry1_global)
        if material_global != None:
            self.dict_LT.setCurrentText(material_global)
        if material1_global != None:
            self.dict_LT1.setCurrentText(material1_global)
        if prefix_global != None:
            self.prefix.setText(prefix_global)
        if detectorparameters_global != None:
            self.detectordistance.setText(str(detectorparameters_global[0]))
            self.xycenter.setText(str(detectorparameters_global[1])+","+str(detectorparameters_global[2]))
            self.bgdetector.setText(str(detectorparameters_global[3])+","+str(detectorparameters_global[4]))
            self.detectordim.setText(str(dim1_global)+","+str(dim2_global))
            self.pixelsize.setText(str(pixelsize_global))
            self.minmaxE.setText(str(emin_global)+","+str(emax_global))

        self.layout = QVBoxLayout() # QGridLayout()

        formLayout = QFormLayout()
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('Training parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Directory where \n model files are saved', self.model_direc_save)
        formLayout.addRow('Material details', QLineEdit().setReadOnly(True))
        formLayout.addRow('Prefix for save folder', self.prefix)
        formLayout.addRow('Choose Material and Symmetry \n (incase of 1 material, keep both same)', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.dict_LT, self.dict_LT1)
        formLayout.addRow(self.symmetry, self.symmetry1)
        formLayout.addRow('Class removal frequency', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.freq_rmv, self.freq_rmv1)
        formLayout.addRow('Class length', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.elements, self.elements1)
        formLayout.addRow('HKL max probed', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.hkl_max, self.hkl_max1)
        formLayout.addRow('Histogram parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Angular distance to probe (in deg)', self.maximum_angle_to_search)
        formLayout.addRow('Angular bin widths (in deg)', self.step_for_binning)
        formLayout.addRow('Simulation parameters', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Analysis mode', self.mode_of_analysis)
        formLayout.addRow('Max Nb. of grain in a LP', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.nb_grains_per_lp, self.nb_grains_per_lp1)
        formLayout.addRow('Nb. of simulations', self.grains_nb_simulate)
        formLayout.addRow('Include single crystal \n misorientation', self.include_scm)
        formLayout.addRow('Detector parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Detector distance', self.detectordistance)
        formLayout.addRow('Detector XY center', self.xycenter)
        formLayout.addRow('Detector Beta Gamma', self.bgdetector)
        formLayout.addRow('Detector Pixel size', self.pixelsize)
        formLayout.addRow('Detector dimensions (dim1,dim2)', self.detectordim)
        formLayout.addRow('Energy (Min, Max)', self.minmaxE)
        formLayout.addRow('Neural Network parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Mode of analysis', self.mode_nn)
        formLayout.addRow('Model Architecture', self.architecture)
        formLayout.addRow('LR, Regularization coefficient', self.learningrate_rc)
        formLayout.addRow('Batch size', self.batch_size)
        formLayout.addRow('Epochs', self.epochs)
        formLayout.addRow('Grid search for model Params', self.grid_search_hyperparams)
        formLayout.addRow('Texture for data', self.texture_model)
        
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow(close_button, self.btn_config)

        self.layout.addLayout(formLayout)
        self.setLayout(self.layout)
        self._gui_save()
        if state > 0:
            self._gui_restore()
    
    def getfiles(self):
        self.modelDirecSave = QFileDialog.getExistingDirectory(self, 'Select Folder in which model files will be saved')
    
    def _gui_save(self):
      # Save geometry
        for name, obj in inspect.getmembers(self):
          # if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current index from combobox
                text = obj.itemText(index)  # get the text for current index
                self.settings.setValue(name, text)  # save combobox selection to registry
            if isinstance(obj, QLineEdit):
                value = obj.text()
                self.settings.setValue(name, value)  # save ui values, so they can be restored next time
        self.settings.sync()

    def _gui_restore(self):
        # Restore geometry  
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current region from combobox
                value = (self.settings.value(name))
                if value == "":
                    continue
                index = obj.findText(value)  # get the corresponding index for specified string in combobox
          
                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index
            if isinstance(obj, QLineEdit):
                value = (self.settings.value(name))#.decode('utf-8'))  # get stored value from registry
                obj.setText(value)  # restore lineEditFile
        self.settings.sync()
        
    def send_details_mainGUI(self):
        self._gui_save()
        detector_params = [float(self.detectordistance.text()),
                           float(self.xycenter.text().split(",")[0]), 
                           float(self.xycenter.text().split(",")[1]),
                           float(self.bgdetector.text().split(",")[0]), 
                           float(self.bgdetector.text().split(",")[1])]
        
        global prefix_global, weightfile_global, modelfile_global, model_weight_file
        if self.prefix.text() != prefix_global:
            prefix_global = self.prefix.text()
            ##exp directory
            if material_global == material1_global:
                fn = material_global + prefix_global
            else:
                fn = material_global + "_" + material1_global + prefix_global
                        
            modelfile_global = self.modelDirecSave + "//" + fn
            if material_global == material1_global:
                if model_weight_file == "none":
                    weightfile_global = modelfile_global + "//" + "model_" + material_global + ".h5"
                else:
                    weightfile_global = model_weight_file
            else:
                if model_weight_file == "none":
                    weightfile_global = modelfile_global + "//" + "model_" + material_global + "_" + material1_global + ".h5"
                else:
                    weightfile_global = model_weight_file
                    
        # create a dictionary and emit the signal
        emit_dictionary = { "material_": self.dict_LT.currentText(), ## same key as used in LaueTools
                            "material1_": self.dict_LT1.currentText(),
                            "prefix": self.prefix.text(),
                            "symmetry": self.symmetry.currentText(),
                            "symmetry1": self.symmetry1.currentText(),
                            "hkl_max_identify" : self.hkl_max.text(), # can be "auto" or an index i.e 12
                            "hkl_max_identify1" : self.hkl_max1.text(), # can be "auto" or an index i.e 12
                            "maximum_angle_to_search" : float(self.maximum_angle_to_search.text()),
                            "step_for_binning" : float(self.step_for_binning.text()),
                            "mode_of_analysis" : int(self.mode_of_analysis.currentText()),
                            "nb_grains_per_lp" : int(self.nb_grains_per_lp.text()), ## max grains to expect in a LP
                            "nb_grains_per_lp1" : int(self.nb_grains_per_lp1.text()),
                            "grains_nb_simulate" : int(self.grains_nb_simulate.text()),
                            "detectorparameters" : detector_params,
                            "pixelsize" : float(self.pixelsize.text()),
                            "dim1":float(self.detectordim.text().split(",")[0]),
                            "dim2":float(self.detectordim.text().split(",")[1]),
                            "emin":float(self.minmaxE.text().split(",")[0]),
                            "emax" : float(self.minmaxE.text().split(",")[1]),
                            "batch_size": int(self.batch_size.text()), ## batches of files to use while training
                            "epochs": int(self.epochs.text()), ## number of epochs for training
                            "texture": self.texture_model.currentText(),
                            "mode_nn": self.mode_nn.currentText(),
                            "grid_bool": self.grid_search_hyperparams.currentText(),
                            "directory": self.modelDirecSave,
                            "freq_rmv": int(self.freq_rmv.text()),
                            "freq_rmv1": int(self.freq_rmv1.text()),
                            "elements": self.elements.text(),
                            "elements1": self.elements1.text(),
                            "include_scm": self.include_scm.currentText(),
                            "lr":float(self.learningrate_rc.text().split(",")[0]),
                            "kc" : float(self.learningrate_rc.text().split(",")[1]),
                            "bc":float(self.learningrate_rc.text().split(",")[0]),
                            }
        self.got_signal.emit(emit_dictionary)
        self.close() # close the window

class AnotherWindowLivePrediction(QWidget):#QWidget QScrollArea
    def __init__(self, state=0, gui_state=0, material_=None, material1_=None, emin=None, emax=None, 
                 symmetry=None, symmetry1=None, detectorparameters=None, pixelsize=None, lattice_=None, 
                 lattice1_=None, hkl_all_class0=None, hkl_all_class1=None, mode_spotCycleglobal=None,
                 softmax_threshold_global = None, mr_threshold_global =    None, cap_matchrate =    None,
                 coeff =    None, coeff_overlap1212 =    None, fit_peaks_gaussian_global =    None,
                 FitPixelDev_global =    None, NumberMaxofFits =    None, tolerance_strain =    None, tolerance_strain1 =    None,
                 material0_limit = None, material1_limit=None, symmetry_name=None, symmetry1_name=None,
                 use_previous_UBmatrix_name = None, material_phase_always_present=None):
        super(AnotherWindowLivePrediction, self).__init__()
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.material_phase_always_present = material_phase_always_present
        self.symmetry_name = symmetry_name
        self.symmetry1_name = symmetry1_name
        self.material0_limit = material0_limit
        self.material1_limit = material1_limit
        self.softmax_threshold_global = softmax_threshold_global
        self.mr_threshold_global = mr_threshold_global
        self.cap_matchrate = cap_matchrate
        self.coeff = coeff
        self.coeff_overlap = coeff_overlap1212
        self.fit_peaks_gaussian_global = fit_peaks_gaussian_global
        self.FitPixelDev_global = FitPixelDev_global
        self.NumberMaxofFits = NumberMaxofFits        
        self.tolerance_strain = tolerance_strain
        self.tolerance_strain1 = tolerance_strain1
        self.mode_spotCycle = mode_spotCycleglobal
        self.material_ = material_
        self.material1_ = material1_
        self.files_treated = []
        self.cnt = 0
        self.emin = emin
        self.emax= emax
        self.lattice_ = lattice_
        self.lattice1_ = lattice1_
        self.symmetry = symmetry
        self.symmetry1 = symmetry1
        self.hkl_all_class0 = hkl_all_class0
        self.hkl_all_class1 = hkl_all_class1
        self.col = np.zeros((10,3))
        self.colx = np.zeros((10,3))
        self.coly = np.zeros((10,3))
        self.match_rate = np.zeros((10,1))
        self.spots_len = np.zeros((10,1))
        self.iR_pix = np.zeros((10,1))
        self.fR_pix = np.zeros((10,1))
        self.mat_global = np.zeros((10,1))
        self.rotation_matrix = np.zeros((10,3,3))
        self.strain_matrix = np.zeros((10,3,3))
        self.strain_matrixs = np.zeros((10,3,3))
        self.strain_calculation = False
        self.cnt_matrix = True   
        self.use_previous_UBmatrix_name = use_previous_UBmatrix_name
        
        self.detectorparameters = detectorparameters
        self.pixelsize= pixelsize

        if expfile_global != None:
            self.filenameDirec = expfile_global
        else:
            self.filenameDirec = None
        self.experimental = QPushButton('Browse')
        self.experimental.clicked.connect(self.getfiles1)
        
        self.ipf_axis = QComboBox()
        choices = ["Z","Y","X"]
        for s in choices:
            self.ipf_axis.addItem(s)
        
        self.filenamebkg = None
        self.filename_bkg = QPushButton('Browse')
        self.filename_bkg.clicked.connect(self.getfilebkg_file)
        
        self.blacklist_file = None
        self.filename_blst = QPushButton('Browse')
        self.filename_blst.clicked.connect(self.getfileblst_file)
        
        self.tolerance = QLineEdit()
        self.tolerance.setText("0.5")
        
        self.tolerance1 = QLineEdit()
        self.tolerance1.setText("0.5")
        
        self.image_grid = QLineEdit()
        self.image_grid.setText("10,10")
        
        self.ubmat = QLineEdit()
        self.ubmat.setText("1")
        
        self.bkg_treatment = QLineEdit()
        self.bkg_treatment.setText("A-B")

        if modelfile_global != None:
            self.modelDirec = modelfile_global
        else:
            self.modelDirec = None
        self.model_direc = QPushButton('Browse')
        self.model_direc.clicked.connect(self.getfiles)

        if weightfile_global != None:
            self.filenameModel = [weightfile_global]
        else:
            self.filenameModel = None
        self.model_path = QPushButton('Browse')
        self.model_path.clicked.connect(self.getfileModel)
        
        self.ccd_label = QComboBox()
        self.ccd_label.addItem("Cor")
        choices = dictLT.dict_CCD.keys()
        for s in choices:
            self.ccd_label.addItem(s)
            
        self.intensity_threshold = QLineEdit()
        self.intensity_threshold.setText("1500")
        
        self.experimental_prefix = QLineEdit()
        self.experimental_prefix.setText("")
        
        self.boxsize = QLineEdit()
        self.boxsize.setText("5")
        
        self.hkl_plot = QLineEdit()
        self.hkl_plot.setText("[1,1,0],[1,1,1],[1,0,0]")
        
        self.matrix_plot = QComboBox()
        choices = ["1"]
        for s in choices:
            self.matrix_plot.addItem(s)
            
        self.strain_plot = QComboBox()
        choices = ["11_sample","22_sample","33_sample","12_sample","13_sample","23_sample",\
                   "11_crystal","22_crystal","33_crystal","12_crystal","13_crystal","23_crystal"]
        for s in choices:
            self.strain_plot.addItem(s)
        
        self.matrix_plot_tech = QComboBox()
        choices = ["Sequential", "MultiProcessing"]
        for s in choices:
            self.matrix_plot_tech.addItem(s)        
        
        self.analysis_plot_tech = QComboBox()
        choices = ["slow", "fast", "beamtime", "graphmode", "multiorimat"]
        for s in choices:
            self.analysis_plot_tech.addItem(s)
        
        self.strain_plot_tech = QComboBox()
        choices = ["NO", "YES"]
        for s in choices:
            self.strain_plot_tech.addItem(s)
            
        ### default values here
        if tolerance_global != None:
            self.tolerance.setText(str(tolerance_global))
        if tolerance_global1 != None:
            self.tolerance1.setText(str(tolerance_global1))
        if image_grid_globalx != None:
            self.image_grid.setText(str(image_grid_globalx)+","+str(image_grid_globaly))
        if exp_prefix_global != None:
            self.experimental_prefix.setText(exp_prefix_global)
        if ccd_label_global != None:
            self.ccd_label.setCurrentText(ccd_label_global)
        if intensity_threshold_global != None:
            self.intensity_threshold.setText(str(intensity_threshold_global))
        if UB_matrix_global != None:
            self.boxsize.setText(str(boxsize_global))
        if UB_matrix_global != None:
            self.ubmat.setText(str(UB_matrix_global)) 
        if strain_label_global != None:
            self.strain_plot_tech.setCurrentText(strain_label_global)
        if mode_spotCycle != None:
            self.analysis_plot_tech.setCurrentText(mode_spotCycle)
        if hkls_list_global != None:
            self.hkl_plot.setText(hkls_list_global) 
            
        # button to continue training
        self.btn_config = QPushButton('Predict and Plot')
        self.btn_config.clicked.connect(self.plot_pc)
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.plot_btn_stop)
        self.btn_save = QPushButton("Save data and plots")
        self.btn_save.clicked.connect(self.save_btn)
        self.btn_load = QPushButton("Predict single file")
        self.btn_load.clicked.connect(self.predict_single_file)
        self.btn_stop.setEnabled(False)
        self.btn_save.setEnabled(False)
        
        mat_bool = False
        if self.material_ == self.material1_:
            mat_bool = True
        
        self.layout = QVBoxLayout() # QGridLayout()
        self.canvas = MplCanvas(self, width=10, height=10, dpi=100, mat_bool=mat_bool)
        self.toolbar = NavigationToolbar(self.canvas, self)
             
        # set the layout
        self.layout.addWidget(self.toolbar, 0)
        self.layout.addWidget(self.canvas, 100)

        formLayout = QFormLayout()
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('Image XY grid size',self.image_grid)
        formLayout.addRow('IPF axis (Cubic and HCP system)', self.ipf_axis)
        # formLayout.addRow('Predicition config', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Directory where \n model files are', self.model_direc)
        # formLayout.addRow('Model weights path', self.model_path)
        # formLayout.addRow('Experimental file config', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Experimental Directory', self.experimental)
        # formLayout.addRow('Experimental file prefix', self.experimental_prefix)
        # formLayout.addRow('Experimental static noise', self.filename_bkg)
        # formLayout.addRow('BlackList peaks', self.filename_blst)
        # formLayout.addRow('Background treatment expression', self.bkg_treatment)
        # formLayout.addRow('if peak search required', QLineEdit().setReadOnly(True))
        # formLayout.addRow('CCD label', self.ccd_label)
        # formLayout.addRow('Peak Search Intensity threshold', self.intensity_threshold)
        # formLayout.addRow('Peak Search BOX size', self.boxsize)
        # formLayout.addRow('UB matrix config', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Tolerance angle', self.tolerance)
        formLayout.addRow('Matricies to predict (sequential)', self.ubmat)       
        formLayout.addRow('Matrix to plot', self.matrix_plot) 
        formLayout.addRow('Strain component to plot', self.strain_plot) 
        # formLayout.addRow('Calculate strain (rough)', self.strain_plot_tech) 
        formLayout.addRow('CPU mode', self.matrix_plot_tech) 
        formLayout.addRow('Analysis mode', self.analysis_plot_tech) 
        # formLayout.addRow('List of HKL subsets to plot', self.hkl_plot) 
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow(self.btn_stop, self.btn_config)
        formLayout.addRow(self.btn_load, self.btn_save)
        # formLayout.addRow(self.btn_save)

        self.layout.addLayout(formLayout)
        self.setLayout(self.layout)
        self.file_state=0
        self.timer = QtCore.QTimer()
        self.timermp1212 = QtCore.QTimer()
        self.popups = []
        
    def getfilebkg_file(self):
        self.filenamebkg = QFileDialog.getOpenFileName(self, 'Select the background image of same detector')
    
    def getfileblst_file(self):
        self.blacklist_file = QFileDialog.getOpenFileName(self, 'Select the list of peaks DAT file to blacklist')
    
    def predict_single_file(self,):
        ## Provide path to a single tiff or cor file to predict and write a pickle object
        filenameSingleExp = QFileDialog.getOpenFileName(self, 'Select a single experimental file')
        if len(filenameSingleExp[0]) == 0:
            return
        filenameSingleExp = filenameSingleExp[0]
        model_direc = self.modelDirec
        
        lim_x, lim_y = int(1), int(1)
                
        ## load model related files and generate the model
        if self.material_ != self.material1_:
            json_file = open(model_direc+"//model_"+self.material_+"_"+self.material1_+".json", 'r')
        else:
            json_file = open(model_direc+"//model_"+self.material_+".json", 'r')
                
        classhkl = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        angbins = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        
        if self.material_ != self.material1_:
            ind_mat = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_5"]
            ind_mat1 = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_6"]
        else: 
            ind_mat = None
            ind_mat1 = None  
        
        load_weights = self.filenameModel[0]
        wb = AnotherWindowLivePrediction.read_hdf5(load_weights)
        temp_key = list(wb.keys())
        
        # # load json and create model
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        print("Constructing model")
        load_weights = self.filenameModel[0]
        model.load_weights(load_weights)
        print("Uploading weights to model")
        print("All model files found and loaded")
        
        cond = self.strain_plot_tech.currentText()
        self.strain_calculation = False
        if cond == "YES":
            self.strain_calculation = True

        ## access grid files to process with multi-thread
        check = np.zeros(1)
        # self.grid_files = grid_files.reshape((self.lim_x,self.lim_y))
        # self.filenm = filenm.reshape((self.lim_x,self.lim_y))
        # =============================================================================
        try:
            blacklist = self.blacklist_file[0]
        except:
            blacklist = None
        
        ### Create a COR directory to be loaded in LaueTools
        cor_file_directory = self.filenameDirec + "//" + self.experimental_prefix.text()+"CORfiles"
        if not os.path.exists(cor_file_directory):
            os.makedirs(cor_file_directory)
        
        start_timemultiorimat = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
        strain_matrix12multiorimat, strain_matrixs12multiorimat, \
            rotation_matrix12multiorimat, col12multiorimat, \
                colx12multiorimat, coly12multiorimat,\
        match_rate12multiorimat, mat_global12multiorimat, cnt12multiorimat,\
            files_treated12multiorimat, spots_len12multiorimat, \
                iR_pix12multiorimat, fR_pix12multiorimat, check12multiorimat, best_match12multiorimat = AnotherWindowLivePrediction.predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "graphmode",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit)
        end_timemultiorimat = time.time() - start_timemultiorimat
        print("Total time to process one file in graph mode (in seconds): "+str(end_timemultiorimat))        
        
        start_timebeamtime = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
        strain_matrix12beamtime, strain_matrixs12beamtime, \
            rotation_matrix12beamtime, col12beamtime, \
                colx12beamtime, coly12beamtime,\
        match_rate12beamtime, mat_global12beamtime, cnt12beamtime,\
            files_treated12beamtime, spots_len12beamtime, \
                iR_pix12beamtime, fR_pix12beamtime, check12beamtime, best_match12beamtime = AnotherWindowLivePrediction.predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "beamtime",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit)
        end_timebeamtime = time.time() - start_timebeamtime
        print("Total time to process one file in beamtime mode (in seconds): "+str(end_timebeamtime))
        
        start_timefast = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
        strain_matrix12fast, strain_matrixs12fast, \
            rotation_matrix12fast, col12fast, \
                colx12fast, coly12fast,\
        match_rate12fast, mat_global12fast, cnt12fast,\
            files_treated12fast, spots_len12fast, \
                iR_pix12fast, fR_pix12fast, check12fast, best_match12fast = AnotherWindowLivePrediction.predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "fast",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit)
        end_timefast = time.time() - start_timefast
        print("Total time to process one file in fast mode (in seconds): "+str(end_timefast)) 
        
        start_time = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
        strain_matrix12, strain_matrixs12, \
            rotation_matrix12, col12, \
                colx12, coly12,\
        match_rate12, mat_global12, cnt12,\
            files_treated12, spots_len12, \
                iR_pix12, fR_pix12, check12, best_match12 = AnotherWindowLivePrediction.predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "slow",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit)
        end_time = time.time() - start_time
        print("Total time to process one file in slow mode (in seconds): "+str(end_time))
        
        save_name = filenameSingleExp.split(".")[0].split("/")[-1]
        np.savez_compressed(model_direc+'//'+save_name+'_SLOW_MODE.npz', strain_matrix12, strain_matrixs12, \
                                    rotation_matrix12, col12, \
                                        colx12, coly12,\
                                match_rate12, mat_global12, cnt12,\
                                    files_treated12, spots_len12, \
                                        iR_pix12, fR_pix12, check12, best_match12)
            
        w = MyPopup(match_rate12, rotation_matrix12, mat_global12, fR_pix12, 
                    filenameSingleExp, strain_matrix12, strain_matrixs12, end_time,
                    match_rate12fast, rotation_matrix12fast, mat_global12fast, fR_pix12fast, 
                    strain_matrix12fast, strain_matrixs12fast, end_timefast,
                    match_rate12beamtime, rotation_matrix12beamtime, mat_global12beamtime, fR_pix12beamtime, 
                    strain_matrix12beamtime, strain_matrixs12beamtime, end_timebeamtime,
                    match_rate12multiorimat, rotation_matrix12multiorimat, mat_global12multiorimat, fR_pix12multiorimat, 
                    strain_matrix12multiorimat, strain_matrixs12multiorimat, end_timemultiorimat)
        # w.setGeometry(QRect(100, 100, 400, 200))
        w.show()       
        self.popups.append(w)
                            
    def save_btn(self,):
        curr_time = time.time()
        now = datetime.datetime.fromtimestamp(curr_time)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        save_directory_ = self.model_direc+"//results_"+self.material_+"_"+c_time
        if not os.path.exists(save_directory_):
            os.makedirs(save_directory_)
        
        np.savez_compressed(save_directory_+ "//results.npz", 
                            self.best_match, self.mat_global, self.rotation_matrix, self.strain_matrix, 
                            self.strain_matrixs,
                            self.col, self.colx, self.coly, self.match_rate, self.files_treated,
                            self.lim_x, self.lim_y, self.spots_len, self.iR_pix, self.fR_pix,
                            self.material_, self.material1_)
        
        ## intermediate saving of pickle objects with results
        with open(save_directory_+ "//results.pickle", "wb") as output_file:
                cPickle.dump([self.best_match, self.mat_global, self.rotation_matrix, self.strain_matrix, 
                              self.strain_matrixs,
                              self.col, self.colx, self.coly, self.match_rate, self.files_treated,
                              self.lim_x, self.lim_y, self.spots_len, self.iR_pix, self.fR_pix,
                              self.material_, self.material1_, self.lattice_, self.lattice1_,
                              self.symmetry, self.symmetry1], output_file)     
        #%  Plot some data  
        global_plots(self.lim_x, self.lim_y, self.strain_matrix, self.strain_matrixs, self.col, 
                     self.colx, self.coly, self.match_rate, self.mat_global, self.spots_len, 
                     self.iR_pix, self.fR_pix, save_directory_, self.material_, self.material1_,
                     match_rate_threshold=5, bins=30)
        
        save_sst(self.lim_x, self.lim_y, self.strain_matrix, self.strain_matrixs, self.col, 
                self.colx, self.coly, self.match_rate, self.mat_global, self.spots_len, 
                self.iR_pix, self.fR_pix, save_directory_, self.material_, self.material1_,
                self.lattice_, self.lattice1_, self.symmetry, self.symmetry1, self.rotation_matrix,
                self.symmetry_name, self.symmetry1_name,
                      mac_axis = [0., 0., 1.], axis_text="Z", match_rate_threshold=5)
        
        ## TODO HKL selective plots (in development)
        hkls_list = ast.literal_eval(self.hkl_plot.text())
        if self.ipf_axis.currentText() == "Z":
            mac_axis = [0., 0., 1.]
        elif self.ipf_axis.currentText() == "Y":
            mac_axis = [0., 1., 0.]
        elif self.ipf_axis.currentText() == "X":
            mac_axis = [1., 0., 0.]
        print(mac_axis, hkls_list)
        # save_hkl_stats(self.lim_x, self.lim_y, self.strain_matrix, self.strain_matrixs, self.col, 
        #               self.colx, self.coly, self.match_rate, self.mat_global, self.spots_len, 
        #               self.iR_pix, self.fR_pix, save_directory_, self.material_, self.material1_,
        #               self.lattice_, self.lattice1_, self.symmetry, self.symmetry1, self.rotation_matrix, 
        #              hkls_list=hkls_list, angle=10., mac_axis = mac_axis, axis_text = self.ipf_axis.currentText())
        
        ## Write global text file with all results
        if self.material_ != self.material1_:
            text_file = open(save_directory_+"//prediction_stats_"+self.material_+"_"+self.material1_+".txt", "w")
        else:
            text_file = open(save_directory_+"//prediction_stats_"+self.material_+".txt", "w")

        filenames = list(np.unique(self.files_treated))
        filenames.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
        
        for i in range(self.lim_x*self.lim_y):
            text_file.write("# ********** \n")
            text_file.write("# Filename: "+ filenames[i] + "\n")
            for j in range(len(self.best_match)):
                stats_ = self.best_match[j][0][i]
                dev_eps_sample = self.strain_matrixs[j][0][i,:,:]
                dev_eps = self.strain_matrix[j][0][i,:,:]
                initial_residue = self.iR_pix[j][0][i][0]
                final_residue = self.fR_pix[j][0][i][0]
                mat = int(self.mat_global[j][0][i][0])
                if mat == 0:
                    case = "None"
                elif mat == 1:
                    case = self.material_
                elif mat == 2:
                    case = self.material1_
                
                text_file.write("# ********** UB MATRIX "+str(j+1)+" \n")
                text_file.write("Spot_index for 2 HKL are "+ str(stats_[0])+" ; "+ str(stats_[1])+ "\n")
                text_file.write("HKL1 "+str(stats_[2])+"; HKL2 "+str(stats_[3])+"\n")
                text_file.write("Coords of HKL1 "+str(stats_[4])+\
                                "; coords of HKL2 "+str(stats_[5])+"\n")
                text_file.write("Distance between 2 spots is "+ str(stats_[6])+ "\n")
                text_file.write("Distance between 2 spots in LUT is "+ str(stats_[7])+ "\n")
                text_file.write("Accuracy of NN for 2 HKL is "+ str(stats_[8])+\
                                "% ; "+str(stats_[9])+ "% \n")
                string1 = "Matched, Expected, Matching rate(%) : " + \
                            str(stats_[10]) +", "+str(stats_[11]) +", "+str(stats_[12])+" \n"
                text_file.write(string1)
                text_file.write("Rotation matrix for 2 HKL (multiplied by symmetry) is \n")
                temp_ = stats_[14].flatten()
                string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                            "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                                "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
                text_file.write(string1)
                
                text_file.write("dev_eps_sample is \n")
                temp_ = dev_eps_sample.flatten()
                string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                            "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                                "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
                text_file.write(string1)

                text_file.write("dev_eps is \n")
                temp_ = dev_eps.flatten()
                string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                            "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                                "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
                text_file.write(string1)

                text_file.write("Initial_pixel, Final_pixel residues are : "+str(initial_residue)+", "+str(final_residue)+" \n")
                
                text_file.write("Mat_id is "+str(mat)+"\n")
                text_file.write("Material indexed is "+case+"\n")
                text_file.write("\n")
        text_file.close()
        print("prediction statistics are generated") 
        
        ## write MTEX file
        rotation_matrix = [[] for i in range(len(self.rotation_matrix))]
        for i in range(len(self.rotation_matrix)):
            rotation_matrix[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))

        for i in range(len(self.rotation_matrix)):
            temp_mat = self.rotation_matrix[i][0]    
            for j in range(len(temp_mat)):
                orientation_matrix = temp_mat[j,:,:]
                ## rotate orientation by 40degrees to bring in Sample RF
                omega = np.deg2rad(-40.0)
                # # rotation de -omega autour de l'axe x (or Y?) pour repasser dans Rsample
                cw = np.cos(omega)
                sw = np.sin(omega)
                mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]]) #Y
                # mat_from_lab_to_sample_frame = np.array([[1.0, 0.0, 0.0], [0.0, cw, -sw], [0.0, sw, cw]]) #X
                # mat_from_lab_to_sample_frame = np.array([[cw, -sw, 0.0], [sw, cw, 0.0], [0.0, 0.0, 1.0]]) #Z
                orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
                if np.linalg.det(orientation_matrix) < 0:
                    orientation_matrix = -orientation_matrix
                rotation_matrix[i][0][j,:,:] = orientation_matrix
                          
        if self.material_ == self.material1_:
            lattice = self.lattice_
            material0_LG = material0_lauegroup
            header = [
                    "Channel Text File",
                    "Prj     lauetoolsnn",
                    "Author    [Ravi raj purohit]",
                    "JobMode    Grid",
                    "XCells    "+str(self.lim_x),
                    "YCells    "+str(self.lim_y),
                    "XStep    1.0",
                    "YStep    1.0",
                    "AcqE1    0",
                    "AcqE2    0",
                    "AcqE3    0",
                    "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
                    "Phases    1",
                    str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
                    str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
                        str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
                    "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]
        else:
            lattice = self.lattice_
            lattice1 = self.lattice1_
            material0_LG = material0_lauegroup
            material1_LG = material1_lauegroup
            header = [
                    "Channel Text File",
                    "Prj     lauetoolsnn",
                    "Author    [Ravi raj purohit]",
                    "JobMode    Grid",
                    "XCells    "+str(self.lim_x),
                    "YCells    "+str(self.lim_y),
                    "XStep    1.0",
                    "YStep    1.0",
                    "AcqE1    0",
                    "AcqE2    0",
                    "AcqE3    0",
                    "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
                    "Phases    2",
                    str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
                    str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
                        str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
                    str(lattice1._lengths[0]*10)+";"+str(lattice1._lengths[1]*10)+";"+\
                    str(lattice1._lengths[2]*10)+"\t"+str(lattice1._angles[0])+";"+\
                        str(lattice1._angles[1])+";"+str(lattice1._angles[2])+"\t"+"Material2"+ "\t"+material1_LG+ "\t"+"????"+"\t"+"????",
                    "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]
        # =================CALCULATION OF POSITION=====================================
        for index in range(len(self.rotation_matrix)):
            euler_angles = np.zeros((len(rotation_matrix[index][0]),3))
            phase_euler_angles = np.zeros(len(rotation_matrix[index][0]))
            for i in range(len(rotation_matrix[index][0])):
                if np.all(rotation_matrix[index][0][i,:,:] == 0):
                    continue
                euler_angles[i,:] = rot_mat_to_euler(rotation_matrix[index][0][i,:,:])
                phase_euler_angles[i] = self.mat_global[index][0][i]        
            
            euler_angles = euler_angles.reshape((self.lim_x,self.lim_y,3))
            phase_euler_angles = phase_euler_angles.reshape((self.lim_x,self.lim_y,1))
            
            a = euler_angles
            if self.material_ != self.material1_:
                filename125 = save_directory_+ "//"+self.material_+"_"+self.material1_+"_MTEX_UBmat_"+str(index)+".ctf"
            else:
                filename125 = save_directory_+ "//"+self.material_+"_MTEX_UBmat_"+str(index)+".ctf"
                
            f = open(filename125, "w")
            for ij in range(len(header)):
                f.write(header[ij]+" \n")
                    
            for i123 in range(euler_angles.shape[1]):
                y_step = 1 * i123
                for j123 in range(euler_angles.shape[0]):
                    x_step = 1 * j123
                    phase_id = int(phase_euler_angles[j123,i123,0])
                    eul =  str(phase_id)+'\t' + "%0.4f" % x_step +'\t'+"%0.4f" % y_step+'\t8\t0\t'+ \
                                        "%0.4f" % a[j123,i123,0]+'\t'+"%0.4f" % a[j123,i123,1]+ \
                                            '\t'+"%0.4f" % a[j123,i123,2]+'\t0.0001\t180\t0\n'
                    string = eul
                    f.write(string)
            f.close()        
         
    def plot_pc(self):
        ## update matrix plot box?
        if self.cnt_matrix:
            self.cnt_matrix = False
            for intmat in range(int(self.ubmat.text())):
                if intmat == 0:
                    continue
                self.matrix_plot.addItem(str(intmat+1))
        
        self.btn_config.setEnabled(False)
        self.model_direc = self.modelDirec
        
        self.lim_x, self.lim_y = int(self.image_grid.text().split(",")[0]), int(self.image_grid.text().split(",")[1])
        
        if self.cnt == 0:
            self.col = [[] for i in range(int(self.ubmat.text()))]
            self.colx = [[] for i in range(int(self.ubmat.text()))]
            self.coly = [[] for i in range(int(self.ubmat.text()))]
            self.rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
            self.strain_matrix = [[] for i in range(int(self.ubmat.text()))]
            self.strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
            self.match_rate = [[] for i in range(int(self.ubmat.text()))]
            self.spots_len = [[] for i in range(int(self.ubmat.text()))]
            self.iR_pix = [[] for i in range(int(self.ubmat.text()))]
            self.fR_pix = [[] for i in range(int(self.ubmat.text()))]
            self.mat_global = [[] for i in range(int(self.ubmat.text()))]
            self.best_match = [[] for i in range(int(self.ubmat.text()))]
            for i in range(int(self.ubmat.text())):
                self.col[i].append(np.zeros((self.lim_x*self.lim_y,3)))
                self.colx[i].append(np.zeros((self.lim_x*self.lim_y,3)))
                self.coly[i].append(np.zeros((self.lim_x*self.lim_y,3)))
                self.rotation_matrix[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
                self.strain_matrix[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
                self.strain_matrixs[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
                self.match_rate[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.spots_len[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.iR_pix[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.fR_pix[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.mat_global[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.best_match[i].append([[] for jk in range(self.lim_x*self.lim_y)])
                
        ## load model related files and generate the model
        if self.material_ != self.material1_:
            json_file = open(self.model_direc+"//model_"+self.material_+"_"+self.material1_+".json", 'r')
        else:
            json_file = open(self.model_direc+"//model_"+self.material_+".json", 'r')
                
        self.classhkl = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        self.angbins = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        
        if self.material_ != self.material1_:
            self.ind_mat = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_5"]
            self.ind_mat1 = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_6"]
        else: 
            self.ind_mat = None
            self.ind_mat1 = None  
        
        load_weights = self.filenameModel[0]
        self.wb = AnotherWindowLivePrediction.read_hdf5(load_weights)
        self.temp_key = list(self.wb.keys())
        
        # # load json and create model
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        print("Constructing model")
        load_weights = self.filenameModel[0]
        self.model.load_weights(load_weights)
        print("Uploading weights to model")
        print("All model files found and loaded")

        if self.file_state==0:
            ct = time.time()
            now = datetime.datetime.fromtimestamp(ct)
            self.c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
            self.file_state = 1
        
        self.update_plot()
        
        self.timer.setInterval(100) ## check every second (update the list of files in folder)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
        self.mode_spotCycle = self.analysis_plot_tech.currentText()
        
        if self.matrix_plot_tech.currentText() == "MultiProcessing":
            self.ncpu = cpu_count()
            self._inputs_queue = Queue()
            self._outputs_queue = Queue()
            
            run_flag = multip.Value('I', True)
            self._worker_processes = {}
            for i in range(self.ncpu):
                self._worker_processes[i]= Process(target=AnotherWindowLivePrediction.worker, args=(self._inputs_queue, self._outputs_queue, i+1, run_flag))
            for i in range(self.ncpu):
                self._worker_processes[i].start()
            ### Update data from multiprocessing
            self.timermp1212.setInterval(1) ## check every second (update the list of files in folder)
            self.timermp1212.timeout.connect(self.update_data_mp1212)
            self.timermp1212.start()
    
        self.out_name = None
        
        self.run = True
        self.temp_ = threading.Thread(target=self.plot_pcv1, daemon=False)
        self.temp_.start()
        
        self.btn_stop.setEnabled(True)
        self.btn_save.setEnabled(False)
        
    @staticmethod
    def worker(inputs_queue, outputs_queue, proc_id, run_flag):
        print(f'Initializing worker {proc_id}')
        while True:
            if not run_flag.value:
                break
            time.sleep(0.01)
            if not inputs_queue.empty(): 
                message = inputs_queue.get()
                if message == 'STOP':
                    print(f'[{proc_id}] stopping')
                    break

                num1, num2, meta = message
                files_worked = []
                while True:
                    if len(num1) == len(files_worked):
                        print("process finished")
                        break
                    for ijk in range(len(num1)):
                        if ijk in files_worked:
                            continue                       
                        if not run_flag.value:
                            num1, files_worked = [], []
                            print(f'[{proc_id}] stopping')
                            break
                        
                        files, cnt, rotation_matrix, strain_matrix, strain_matrixs,\
                        col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,mat_global,\
                        check,detectorparameters,pixelsize,angbins,\
                        classhkl, hkl_all_class0, hkl_all_class1, emin, emax,\
                        material_, material1_, symmetry, symmetry1,lim_x,lim_y,\
                        strain_calculation, ind_mat, ind_mat1,\
                        model_direc, tolerance , tolerance1,\
                        matricies, ccd_label,\
                        filename_bkg,intensity_threshold,\
                        boxsize,bkg_treatment,\
                        filenameDirec, experimental_prefix,\
                        blacklist_file, text_file, \
                        files_treated,try_previous1,\
                        wb, temp_key, cor_file_directory, mode_spotCycle1,\
                        softmax_threshold_global123,mr_threshold_global123,\
                        cap_matchrate123, tolerance_strain123, tolerance_strain1231,\
                        NumberMaxofFits123,fit_peaks_gaussian_global123,\
                        FitPixelDev_global123,coeff123,coeff_overlap,\
                        material0_limit, material1_limit, use_previous_UBmatrix_name1,\
                            material_phase_always_present1= num1[ijk]

                        if os.path.isfile(files):
                            # try:
                            strain_matrix12, strain_matrixs12, \
                                rotation_matrix12, col12, \
                                    colx12, coly12,\
                            match_rate12, mat_global12, cnt12,\
                                files_treated12, spots_len12, \
                                    iR_pix12, fR_pix12, check12, best_match12 = AnotherWindowLivePrediction.predict_preprocessMP(files, cnt, 
                                                                       rotation_matrix,strain_matrix,strain_matrixs,
                                                                       col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                                       mat_global,
                                                                       check,detectorparameters,pixelsize,angbins,
                                                                       classhkl, hkl_all_class0, hkl_all_class1, emin, emax,
                                                                       material_, material1_, symmetry, symmetry1,lim_x,lim_y,
                                                                       strain_calculation, ind_mat, ind_mat1,
                                                                       model_direc, tolerance, tolerance1,
                                                                       matricies, ccd_label,
                                                                       filename_bkg,intensity_threshold,
                                                                       boxsize,bkg_treatment,
                                                                       filenameDirec, experimental_prefix,
                                                                       blacklist_file, text_file, 
                                                                       files_treated,try_previous1,
                                                                       wb, temp_key, cor_file_directory, mode_spotCycle1,
                                                                       softmax_threshold_global123,mr_threshold_global123,
                                                                       cap_matchrate123, tolerance_strain123,
                                                                       tolerance_strain1231,NumberMaxofFits123,
                                                                       fit_peaks_gaussian_global123,
                                                                       FitPixelDev_global123, coeff123,coeff_overlap,
                                                                       material0_limit,material1_limit,
                                                                       use_previous_UBmatrix_name1,
                                                                       material_phase_always_present1)
                            if check12[cnt] == 1:
                                files_worked.append(ijk)
                                meta['proc_id'] = proc_id
                                r_message = (strain_matrix12, strain_matrixs12, rotation_matrix12, col12, \
                                             colx12, coly12, match_rate12, mat_global12, cnt12, meta, \
                                             files_treated12, spots_len12, iR_pix12, fR_pix12, best_match12, check12)
                                outputs_queue.put(r_message)
                            # except Exception as e:
                            #     print(e)
                            #     continue
                        ### safer to just break the multiprocessing loop after one trial has been ?
                        ### attempted to not let the CPUs occupied
        print("broke the worker while loop")
                                
    def update_plot(self):
        ## get color matrix to plot
        index_plotfnc = int(self.matrix_plot.currentText())-1
        strain_index_plotfnc = self.strain_plot.currentText()
        
        if "sample" in strain_index_plotfnc:
            title_plotfnc = "Deviatoric strain (sample frame)"
            strain_matrix_plot_plotfnc = self.strain_matrixs[index_plotfnc][0]
        elif "crystal" in strain_index_plotfnc:
            title_plotfnc = "Deviatoric strain (crystal frame)"
            strain_matrix_plot_plotfnc = self.strain_matrix[index_plotfnc][0]
        
        if "11" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,0,0]
        elif "22" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,1,1]
        elif "33" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,2,2]
        elif "12" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,0,1]
        elif "13" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,0,2]
        elif "23" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,1,2]
        strain_tensor_plot_plotfnc = strain_matrix_plot_plotfnc.reshape((self.lim_x, self.lim_y))
        
        if self.ipf_axis.currentText() == "Z":
            col_plot_plotfnc = self.col[index_plotfnc][0]
        elif self.ipf_axis.currentText() == "Y":
            col_plot_plotfnc = self.coly[index_plotfnc][0]
        elif self.ipf_axis.currentText() == "X":
            col_plot_plotfnc = self.colx[index_plotfnc][0]

        col_plot_plotfnc = col_plot_plotfnc.reshape((self.lim_x, self.lim_y, 3))
        mr_plot_plotfnc = self.match_rate[index_plotfnc][0]
        mr_plot_plotfnc = mr_plot_plotfnc.reshape((self.lim_x, self.lim_y))        
        mat_glob_plotfnc = self.mat_global[index_plotfnc][0]
        mat_glob_plotfnc = mat_glob_plotfnc.reshape((self.lim_x, self.lim_y))
        
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()
        self.canvas.axes.set_title("IPF map", loc='center', fontsize=8)
        self.canvas.axes.imshow(col_plot_plotfnc, origin='lower')
        self.canvas.axes2.cla()
        self.canvas.axes2.set_title(title_plotfnc, loc='center', fontsize=8) 
        self.canvas.axes2.imshow(strain_tensor_plot_plotfnc, origin='lower')
        self.canvas.axes1.cla()
        self.canvas.axes1.set_title("Matching rate", loc='center', fontsize=8) 
        self.canvas.axes1.imshow(mr_plot_plotfnc, origin='lower')
        
        if self.material_ != self.material1_:
            self.canvas.axes3.cla()
            self.canvas.axes3.set_title("Material Index (1: "+self.material_+"; 2: "+self.material1_+")", loc='center', fontsize=8) 
            self.canvas.axes3.imshow(mat_glob_plotfnc, origin='lower')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
    
    def update_data_mp1212(self):
        if not self._outputs_queue.empty():
            
            self.timermp1212.blockSignals(True)
            
            r_message_mpdata = self._outputs_queue.get()
            strain_matrix_mpdata, strain_matrixs_mpdata, rotation_matrix_mpdata, col_mpdata, \
                             colx_mpdata, coly_mpdata, match_rate_mpdata, mat_global_mpdata, \
                                 cnt_mpdata, meta_mpdata, files_treated_mpdata, spots_len_mpdata, \
                                     iR_pixel_mpdata, fR_pixel_mpdata, best_match_mpdata, check_mpdata = r_message_mpdata

            for i_mpdata in files_treated_mpdata:
                self.files_treated.append(i_mpdata)
                
            self.check[cnt_mpdata] = check_mpdata[cnt_mpdata]
            for intmat_mpdata in range(int(self.ubmat.text())):
                self.mat_global[intmat_mpdata][0][cnt_mpdata] = mat_global_mpdata[intmat_mpdata][0][cnt_mpdata]
                self.strain_matrix[intmat_mpdata][0][cnt_mpdata,:,:] = strain_matrix_mpdata[intmat_mpdata][0][cnt_mpdata,:,:]
                self.strain_matrixs[intmat_mpdata][0][cnt_mpdata,:,:] = strain_matrixs_mpdata[intmat_mpdata][0][cnt_mpdata,:,:]
                self.rotation_matrix[intmat_mpdata][0][cnt_mpdata,:,:] = rotation_matrix_mpdata[intmat_mpdata][0][cnt_mpdata,:,:]
                self.col[intmat_mpdata][0][cnt_mpdata,:] = col_mpdata[intmat_mpdata][0][cnt_mpdata,:]
                self.colx[intmat_mpdata][0][cnt_mpdata,:] = colx_mpdata[intmat_mpdata][0][cnt_mpdata,:]
                self.coly[intmat_mpdata][0][cnt_mpdata,:] = coly_mpdata[intmat_mpdata][0][cnt_mpdata,:]
                self.match_rate[intmat_mpdata][0][cnt_mpdata] = match_rate_mpdata[intmat_mpdata][0][cnt_mpdata]
                self.spots_len[intmat_mpdata][0][cnt_mpdata] = spots_len_mpdata[intmat_mpdata][0][cnt_mpdata]
                self.iR_pix[intmat_mpdata][0][cnt_mpdata] = iR_pixel_mpdata[intmat_mpdata][0][cnt_mpdata]
                self.fR_pix[intmat_mpdata][0][cnt_mpdata] = fR_pixel_mpdata[intmat_mpdata][0][cnt_mpdata]
                self.best_match[intmat_mpdata][0][cnt_mpdata] = best_match_mpdata[intmat_mpdata][0][cnt_mpdata]
            
            try:
                np.savez_compressed(self.model_direc+'//rotation_matrix_indexed.npz', self.rotation_matrix, self.mat_global, self.match_rate)
            except:
                print("Warning : Error saving the NPZ file; nothing to worry")
            
            self.timermp1212.blockSignals(False)
            
    def plot_pcv1(self):
        np.savez_compressed(self.model_direc+'//rotation_matrix_indexed.npz', self.rotation_matrix, self.mat_global, self.match_rate)
        
        cond = self.strain_plot_tech.currentText()
        self.strain_calculation = False
        if cond == "YES":
            self.strain_calculation = True
            
        cond_mode = self.matrix_plot_tech.currentText()
        # =============================================================================
        #         ## Multi-processing routine
        # =============================================================================
        # if cond_mode == "MultiProcessing":
        ## Number of files to generate
        grid_files = np.zeros((self.lim_x,self.lim_y))
        filenm = np.chararray((self.lim_x,self.lim_y), itemsize=1000)
        grid_files = grid_files.ravel()
        filenm = filenm.ravel()
        count_global = self.lim_x * self.lim_y
        
        if self.ccd_label.currentText() == "Cor" or self.ccd_label.currentText() == "cor":
            format_file = "cor"
        else:
            format_file = dictLT.dict_CCD[self.ccd_label.currentText()][7]

        list_of_files = glob.glob(self.filenameDirec+'//'+self.experimental_prefix.text()+'*.'+format_file)
        ## sort files
        ## TypeError: '<' not supported between instances of 'str' and 'int'
        list_of_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

        if len(list_of_files) == count_global:
            for ii in range(len(list_of_files)):
                grid_files[ii] = ii
                filenm[ii] = list_of_files[ii]               
        else:
            print("expected "+str(count_global)+" files based on the XY grid ("+str(self.lim_x)+","+str(self.lim_y)+") defined by user")
            print("But found "+str(len(list_of_files))+" files (either all data is not written yet or maybe XY grid definition is not proper)")
            digits = len(str(count_global))
            digits = max(digits,4)
            # if digits < 4:
            #     digits = 4
            
            for ii in range(count_global):
                text = str(ii)
                string = text.zfill(digits)
                file_name_temp = self.filenameDirec+'//'+self.experimental_prefix.text()+string+'.'+format_file
                ## store it in a grid 
                # grid_files[ii] = ii
                filenm[ii] = file_name_temp
            ## access grid files to process with multi-thread
        self.check = np.zeros(count_global)
        # self.grid_files = grid_files.reshape((self.lim_x,self.lim_y))
        # self.filenm = filenm.reshape((self.lim_x,self.lim_y))
        # =============================================================================
        try:
            blacklist = self.blacklist_file[0]
        except:
            blacklist = None
        
        ### Create a COR directory to be loaded in LaueTools
        cor_file_directory = self.filenameDirec + "//" + self.experimental_prefix.text()+"CORfiles"
        if not os.path.exists(cor_file_directory):
            os.makedirs(cor_file_directory)
        
        while True:
            if cond_mode == "Sequential":
                self.predict_preprocess(cnt=self.cnt, 
                                          rotation_matrix=self.rotation_matrix,
                                          strain_matrix=self.strain_matrix,
                                          strain_matrixs=self.strain_matrixs,
                                          col=self.col,
                                          colx=self.colx,
                                          coly=self.coly,
                                          match_rate=self.match_rate,
                                          spots_len=self.spots_len, 
                                          iR_pix=self.iR_pix, 
                                          fR_pix=self.fR_pix,
                                          best_match = self.best_match,
                                          mat_global=self.mat_global,
                                          check=self.check,
                                          detectorparameters=self.detectorparameters,
                                          pixelsize=self.pixelsize,
                                          angbins=self.angbins,
                                          classhkl=self.classhkl,
                                          hkl_all_class0=self.hkl_all_class0,
                                          hkl_all_class1=self.hkl_all_class1,
                                          emin=self.emin,
                                          emax=self.emax,
                                          material_=self.material_,
                                          material1_=self.material1_,
                                          symmetry=self.symmetry,
                                          symmetry1=self.symmetry1,   
                                          lim_x= self.lim_x,
                                          lim_y=self.lim_y,
                                          strain_calculation=self.strain_calculation, 
                                          ind_mat=self.ind_mat, ind_mat1=self.ind_mat1,
                                          model_direc=self.model_direc, tolerance=float(self.tolerance.text()),
                                          tolerance1=float(self.tolerance1.text()),
                                          matricies=int(self.ubmat.text()), ccd_label=self.ccd_label.currentText(), 
                                          filename_bkg=None, #self.filenamebkg,
                                          intensity_threshold=float(self.intensity_threshold.text()),
                                          boxsize=int(self.boxsize.text()),bkg_treatment=self.bkg_treatment.text(),
                                          filenameDirec=self.filenameDirec, 
                                          experimental_prefix=self.experimental_prefix.text(),
                                          blacklist_file =blacklist,
                                          text_file=None,
                                          files_treated=self.files_treated,
                                          try_previous1=True,
                                          wb = self.wb,
                                          temp_key = self.temp_key,
                                          cor_file_directory=cor_file_directory,
                                          mode_spotCycle1 = self.mode_spotCycle,
                                          softmax_threshold_global123 = self.softmax_threshold_global,
                                          mr_threshold_global123=self.mr_threshold_global,
                                          cap_matchrate123=self.cap_matchrate,
                                          tolerance_strain123=self.tolerance_strain,
                                          tolerance_strain1231=self.tolerance_strain1,
                                          NumberMaxofFits123=self.NumberMaxofFits,
                                          fit_peaks_gaussian_global123=self.fit_peaks_gaussian_global,
                                          FitPixelDev_global123=self.FitPixelDev_global,
                                          coeff123 = self.coeff,
                                          coeff_overlap=self.coeff_overlap,
                                          material0_limit=self.material0_limit,
                                          material1_limit=self.material1_limit,
                                          use_previous_UBmatrix_name=self.use_previous_UBmatrix_name,
                                          material_phase_always_present = self.material_phase_always_present)         
            elif cond_mode == "MultiProcessing":
                try_prevs = False
                if self.mode_spotCycle == "beamtime":
                    try_prevs = True
                
                valu12 = [[filenm[ii].decode(), ii,
                           self.rotation_matrix,
                            self.strain_matrix,
                            self.strain_matrixs,
                            self.col,
                            self.colx,
                            self.coly,
                            self.match_rate,
                            self.spots_len, 
                            self.iR_pix, 
                            self.fR_pix,
                            self.best_match,
                            self.mat_global,
                            self.check,
                            self.detectorparameters,
                            self.pixelsize,
                            self.angbins,
                            self.classhkl,
                            self.hkl_all_class0,
                            self.hkl_all_class1,
                            self.emin,
                            self.emax,
                            self.material_,
                            self.material1_,
                            self.symmetry,
                            self.symmetry1,   
                            self.lim_x,
                            self.lim_y,
                            self.strain_calculation, 
                            self.ind_mat, self.ind_mat1,
                            self.model_direc, float(self.tolerance.text()),
                            float(self.tolerance1.text()),
                            int(self.ubmat.text()), self.ccd_label.currentText(), 
                            None,
                            float(self.intensity_threshold.text()),
                            int(self.boxsize.text()),self.bkg_treatment.text(),
                            self.filenameDirec, 
                            self.experimental_prefix.text(),
                            blacklist,
                            None,
                            self.files_treated,
                            try_prevs, ## try previous is kept true, incase if its stuck in loop
                            self.wb,
                            self.temp_key,
                            cor_file_directory,
                            self.mode_spotCycle,
                            self.softmax_threshold_global,
                            self.mr_threshold_global,
                            self.cap_matchrate,
                            self.tolerance_strain,
                            self.tolerance_strain1,
                            self.NumberMaxofFits,
                            self.fit_peaks_gaussian_global,
                            self.FitPixelDev_global,
                            self.coeff,
                            self.coeff_overlap,
                            self.material0_limit,
                            self.material1_limit,
                            self.use_previous_UBmatrix_name,
                            self.material_phase_always_present] for ii in range(count_global)]
                
                chunks = AnotherWindowLivePrediction.chunker_list(valu12, self.ncpu)
                chunks_mp = list(chunks)

                meta = {'t1':time.time()}
                for ijk in range(int(self.ncpu)):
                    self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))
                    
            if cond_mode == "MultiProcessing":
                print("Launched all processes")
                break
            
            if (not self.run) or (self.cnt >= self.lim_x*self.lim_y):
                self.update_plot()
                print("BROKE the WHILE loop FREE")
                break

    def plot_btn_stop(self):        
        if self.matrix_plot_tech.currentText() == "MultiProcessing":
            # while not self._inputs_queue.empty():
            #     self._inputs_queue.get()
            #     print("Emptying input queue")
            # while not self._outputs_queue.empty():
            #     print("Emptying output queue")
            #     self._outputs_queue.get()
            # time.sleep(0.1)
            run_flag = multip.Value('I', False)
            time.sleep(0.1)
            # print('sending stop')
            # for ijk in range(self.ncpu):
            #     self._inputs_queue.put('STOP')

        self.run = False
        self.timer.stop()
        self.timermp1212.stop()    
        
        self.btn_config.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_save.setEnabled(True)
        
    def getfiles(self):
        self.modelDirec = QFileDialog.getExistingDirectory(self, 'Select Folder in which model files are located')
    
    def getfiles1(self):
        self.filenameDirec = QFileDialog.getExistingDirectory(self, 'Select Folder in which Experimental data is or will be stored')
    
    def getfileModel(self):
        self.filenameModel = QFileDialog.getOpenFileName(self, 'Select the model weights H5 or HDF5 file')
    
    def predict_preprocess(self,cnt,rotation_matrix,strain_matrix,strain_matrixs,
                            col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,mat_global,
                            check,detectorparameters,pixelsize,angbins,
                            classhkl, hkl_all_class0, hkl_all_class1, emin, emax,
                            material_, material1_, symmetry, symmetry1,lim_x,lim_y,
                            strain_calculation, ind_mat, ind_mat1,
                            model_direc=None, tolerance =None, tolerance1 =None,
                           matricies=None, ccd_label=None,
                           filename_bkg=None,intensity_threshold=None,
                           boxsize=None,bkg_treatment=None,
                           filenameDirec=None, experimental_prefix=None,
                           blacklist_file =None, text_file=None, files_treated=None,try_previous1=False,
                           wb=None, temp_key=None, cor_file_directory=None, mode_spotCycle1=None,
                           softmax_threshold_global123=None,mr_threshold_global123=None,cap_matchrate123=None,
                           tolerance_strain123=None,tolerance_strain1231=None,NumberMaxofFits123=None,fit_peaks_gaussian_global123=None,
                           FitPixelDev_global123=None, coeff123=None,coeff_overlap=None,
                           material0_limit=None, material1_limit=None, use_previous_UBmatrix_name=None,
                           material_phase_always_present=None):
        
        if ccd_label in ["Cor", "cor"]:
            format_file = "cor"
        else:
            format_file = dictLT.dict_CCD[ccd_label][7]

        list_of_files = glob.glob(filenameDirec+'//'+experimental_prefix+'*.'+format_file)
        ## sort files
        ## TypeError: '<' not supported between instances of 'str' and 'int'
        list_of_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
        
        for files in list_of_files:
            peak_detection_error = False
            if self.run == False:
                break

            if files in files_treated:
                continue
            
            files_treated.append(files)
                        
            if files.split(".")[1] != "cor":
                CCDLabel=ccd_label
                seednumber = "Experimental "+CCDLabel+" file"    
                
                try:
                    out_name = blacklist_file
                except:
                    out_name = None  
                    
                if bkg_treatment == None:
                    bkg_treatment = "A-B"
                    
                try:
                    ### Max space = space betzeen pixles
                    peak_XY = RMCCD.PeakSearch(
                                                files,
                                                stackimageindex = -1,
                                                CCDLabel=CCDLabel,
                                                NumberMaxofFits=NumberMaxofFits123,
                                                PixelNearRadius=10,
                                                removeedge=2,
                                                IntensityThreshold=intensity_threshold,
                                                local_maxima_search_method=0,
                                                boxsize=boxsize,
                                                position_definition=1,
                                                verbose=0,
                                                fit_peaks_gaussian=fit_peaks_gaussian_global123,
                                                xtol=0.001,                
                                                FitPixelDev=FitPixelDev_global123,
                                                return_histo=0,
                                                # Saturation_value=1e10,  # to be merged in CCDLabel
                                                # Saturation_value_flatpeak=1e10,
                                                MinIntensity=0,
                                                PeakSizeRange=(0.65,200),
                                                write_execution_time=1,
                                                Data_for_localMaxima = "auto_background",
                                                formulaexpression=bkg_treatment,
                                                Remove_BlackListedPeaks_fromfile=out_name,
                                                reject_negative_baseline=True,
                                                Fit_with_Data_for_localMaxima=False,
                                                maxPixelDistanceRejection=15.0,
                                                )
                    peak_XY = peak_XY[0]#[:,:2] ##[2] Integer peak lists
                except:
                    print("Error in Peak detection for "+ files)
                    for intmat in range(matricies):
                        rotation_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                        strain_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                        strain_matrixs[intmat][0][cnt,:,:] = np.zeros((3,3))
                        col[intmat][0][cnt,:] = 0,0,0
                        colx[intmat][0][cnt,:] = 0,0,0
                        coly[intmat][0][cnt,:] = 0,0,0
                        match_rate[intmat][0][cnt] = 0
                        mat_global[intmat][0][cnt] = 0
                    
                    cnt += 1
                    peak_detection_error = True
                    continue
                
                s_ix = np.argsort(peak_XY[:, 2])[::-1]
                peak_XY = peak_XY[s_ix]
                
                framedim = dictLT.dict_CCD[CCDLabel][0]
                twicetheta, chi = Lgeo.calc_uflab(peak_XY[:,0], peak_XY[:,1], detectorparameters,
                                                    returnAngles=1,
                                                    pixelsize=pixelsize,
                                                    kf_direction='Z>0')
                data_theta, data_chi = twicetheta/2., chi
                
                framedim = dictLT.dict_CCD[CCDLabel][0]
                dict_dp={}
                dict_dp['kf_direction']='Z>0'
                dict_dp['detectorparameters']=detectorparameters
                dict_dp['detectordistance']=detectorparameters[0]
                dict_dp['detectordiameter']=pixelsize*framedim[0]
                dict_dp['pixelsize']=pixelsize
                dict_dp['dim']=framedim
                dict_dp['peakX']=peak_XY[:,0]
                dict_dp['peakY']=peak_XY[:,1]
                dict_dp['intensity']=peak_XY[:,2]
                
                CCDcalib = {"CCDLabel":CCDLabel,
                            "dd":detectorparameters[0], 
                            "xcen":detectorparameters[1], 
                            "ycen":detectorparameters[2], 
                            "xbet":detectorparameters[3], 
                            "xgam":detectorparameters[4],
                            "pixelsize": pixelsize}
                
                path = os.path.normpath(files)
                IOLT.writefile_cor(cor_file_directory+"//"+path.split(os.sep)[-1].split(".")[0], twicetheta, 
                                   chi, peak_XY[:,0], peak_XY[:,1], peak_XY[:,2],
                                   param=CCDcalib, sortedexit=0)
                
            elif files.split(".")[1] == "cor":
                seednumber = "Experimental COR file"
                allres = IOLT.readfile_cor(files, True)
                data_theta, data_chi, peakx, peaky, intensity = allres[1:6]
                CCDcalib = allres[-1]
                detectorparameters = allres[-2]
                # print('detectorparameters from file are: '+ str(detectorparameters))
                pixelsize = CCDcalib['pixelsize']
                CCDLabel = CCDcalib['CCDLabel']
                framedim = dictLT.dict_CCD[CCDLabel][0]
                dict_dp={}
                dict_dp['kf_direction']='Z>0'
                dict_dp['detectorparameters']=detectorparameters
                dict_dp['detectordistance']=detectorparameters[0]
                dict_dp['detectordiameter']=pixelsize*framedim[0]
                dict_dp['pixelsize']=pixelsize
                dict_dp['dim']=framedim
                dict_dp['peakX']=peakx
                dict_dp['peakY']=peaky
                dict_dp['intensity']=intensity
            
            if peak_detection_error:
                continue
            
            sorted_data = np.transpose(np.array([data_theta, data_chi]))
            tabledistancerandom = np.transpose(GT.calculdist_from_thetachi(sorted_data, sorted_data))

            codebars_all = []
            
            if len(data_theta) == 0:
                print("No peaks Found for : " + files)
                for intmat in range(matricies):
                    rotation_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                    strain_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                    strain_matrixs[intmat][0][cnt,:,:] = np.zeros((3,3))
                    col[intmat][0][cnt,:] = 0,0,0
                    colx[intmat][0][cnt,:] = 0,0,0
                    coly[intmat][0][cnt,:] = 0,0,0
                    match_rate[intmat][0][cnt] = 0
                    mat_global[intmat][0][cnt] = 0
                        
                cnt += 1
                continue
            
            spots_in_center = np.arange(0,len(data_theta))

            for i in spots_in_center:
                spotangles = tabledistancerandom[i]
                spotangles = np.delete(spotangles, i)# removing the self distance
                # codebars = np.histogram(spotangles, bins=angbins)[0]
                codebars = histogram1d(spotangles, range=[min(angbins),max(angbins)], bins=len(angbins)-1)
                ## normalize the same way as training data
                max_codebars = np.max(codebars)
                codebars = codebars/ max_codebars
                codebars_all.append(codebars)
                
            ## reshape for the model to predict all spots at once
            codebars = np.array(codebars_all)
            ## Do prediction of all spots at once
            # prediction = model.predict(codebars)
            prediction = AnotherWindowLivePrediction.predict(codebars, wb, temp_key)
            max_pred = np.max(prediction, axis = 1)
            class_predicted = np.argmax(prediction, axis = 1)
            # print("Total spots attempted:"+str(len(spots_in_center)))
            # print("Took "+ str(time.time()-strat_time_P)+" seconds to predict spots")       
            predicted_hkl123 = classhkl[class_predicted]

            s_tth = data_theta * 2.
            s_chi = data_chi
            
            rotation_matrix1, mr_highest, mat_highest, \
                strain_crystal, strain_sample, iR_pix1, \
                            fR_pix1, spots_len1, best_match1 = AnotherWindowLivePrediction.predict_ubmatrix(seednumber, spots_in_center, classhkl, 
                                                                      hkl_all_class0, 
                                                                        hkl_all_class1, files,
                                                                        s_tth1=s_tth,s_chi1=s_chi,
                                                                        predicted_hkl1=predicted_hkl123,
                                                                        class_predicted1=class_predicted,
                                                                        max_pred1=max_pred,
                                                                        emin=emin,emax=emax,
                                                                        material_=material_, 
                                                                        material1_=material1_, 
                                                                        lim_y=lim_y, lim_x=lim_x, 
                                                                        cnt=cnt,
                                                                        dict_dp=dict_dp,
                                                                        rotation_matrix=rotation_matrix,
                                                                        mat_global=mat_global,
                                                                        strain_calculation=strain_calculation,
                                                                        ind_mat=ind_mat, 
                                                                        ind_mat1=ind_mat1,
                                                                        tolerance=tolerance,
                                                                        tolerance1 =tolerance1,
                                                                        matricies=matricies,
                                                                        tabledistancerandom=tabledistancerandom,
                                                                        text_file = text_file,
                                                                        try_previous1=try_previous1,
                                                                        mode_spotCycle = mode_spotCycle1,
                                                                        softmax_threshold_global123=softmax_threshold_global123,
                                                                        mr_threshold_global123=mr_threshold_global123,
                                                                        cap_matchrate123=cap_matchrate123,
                                                                        tolerance_strain123=tolerance_strain123,
                                                                        tolerance_strain1231=tolerance_strain1231,
                                                                        coeff123=coeff123,
                                                                        coeff_overlap=coeff_overlap,
                                                                        material0_limit=material0_limit, 
                                                                        material1_limit=material1_limit,
                                                                        model_direc=model_direc,
                                                                        use_previous_UBmatrix_name=use_previous_UBmatrix_name,
                                                                        material_phase_always_present=material_phase_always_present)
                
            for intmat in range(matricies):

                if len(rotation_matrix1[intmat]) == 0:
                    col[intmat][0][cnt,:] = 0,0,0
                    colx[intmat][0][cnt,:] = 0,0,0
                    coly[intmat][0][cnt,:] = 0,0,0
                else:
                    mat_global[intmat][0][cnt] = mat_highest[intmat][0]
                    self.mat_global[intmat][0][cnt] = mat_highest[intmat][0]
                    
                    final_symm =symmetry
                    if mat_highest[intmat][0] == 1:
                        final_symm = symmetry
                    elif mat_highest[intmat][0] == 2:
                        final_symm = symmetry1
                        
                    # strain_matrix[intmat][0][cnt,:,:] = strain_crystal[intmat][0]
                    # strain_matrixs[intmat][0][cnt,:,:] = strain_sample[intmat][0]
                    self.strain_matrix[intmat][0][cnt,:,:] = strain_crystal[intmat][0]
                    self.strain_matrixs[intmat][0][cnt,:,:] = strain_sample[intmat][0]
                    # rotation_matrix[intmat][0][cnt,:,:] = rotation_matrix1[intmat][0]
                    self.rotation_matrix[intmat][0][cnt,:,:] = rotation_matrix1[intmat][0]
                    col_temp = AnotherWindowLivePrediction.get_ipf_colour(rotation_matrix1[intmat][0], np.array([0., 0., 1.]), final_symm)
                    # col[intmat][0][cnt,:] = col_temp
                    self.col[intmat][0][cnt,:] = col_temp
                    col_tempx = AnotherWindowLivePrediction.get_ipf_colour(rotation_matrix1[intmat][0], np.array([1., 0., 0.]), final_symm)
                    # colx[intmat][0][cnt,:] = col_tempx
                    self.colx[intmat][0][cnt,:] = col_tempx
                    col_tempy = AnotherWindowLivePrediction.get_ipf_colour(rotation_matrix1[intmat][0], np.array([0., 1., 0.]), final_symm)
                    # coly[intmat][0][cnt,:] = col_tempy
                    self.coly[intmat][0][cnt,:] = col_tempy
                    # match_rate[intmat][0][cnt] = mr_highest[intmat][0]    
                    self.match_rate[intmat][0][cnt] = mr_highest[intmat][0]
                    # spots_len[intmat][0][cnt] = spots_len1[intmat][0]    
                    self.spots_len[intmat][0][cnt] = spots_len1[intmat][0]
                    # iR_pix[intmat][0][cnt] = iR_pix1[intmat][0]    
                    self.iR_pix[intmat][0][cnt] = iR_pix1[intmat][0]
                    # fR_pix[intmat][0][cnt] = fR_pix1[intmat][0]    
                    self.fR_pix[intmat][0][cnt] = fR_pix1[intmat][0]
                    # best_match[intmat][0][cnt] = best_match1
                    self.best_match[intmat][0][cnt] = best_match1[intmat][0]
            cnt += 1
    
    @staticmethod
    def chunker_list(seq, size):
        return (seq[i::size] for i in range(size))
    
    @staticmethod
    def read_hdf5(path):
        weights = {}
        keys = []
        with h5py.File(path, 'r') as f: # open file
            f.visit(keys.append) # append all keys to list
            for key in keys:
                if ':' in key: # contains data if ':' in key
                    weights[f[key].name] = f[key][:]
        return weights
    
    @staticmethod
    def softmax(x):
        return (np.exp(x).T / np.sum(np.exp(x).T, axis=0)).T
    
    @staticmethod
    def predict(x, wb, temp_key):
        # first layer
        layer0 = np.dot(x, wb[temp_key[1]]) + wb[temp_key[0]] 
        layer0 = np.maximum(0, layer0) ## ReLU activation
        # Second layer
        layer1 = np.dot(layer0, wb[temp_key[3]]) + wb[temp_key[2]] 
        layer1 = np.maximum(0, layer1)
        # Third layer
        layer2 = np.dot(layer1, wb[temp_key[5]]) + wb[temp_key[4]]
        layer2 = np.maximum(0, layer2)
        # Output layer
        layer3 = np.dot(layer2, wb[temp_key[7]]) + wb[temp_key[6]]
        layer3 = AnotherWindowLivePrediction.softmax(layer3) ## output softmax activation
        return layer3
    
    @staticmethod
    def predict_preprocessMP(files, cnt, 
                             rotation_matrix,strain_matrix,strain_matrixs,
                            col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,mat_global,
                            check,detectorparameters,pixelsize,angbins,
                            classhkl, hkl_all_class0, hkl_all_class1, emin, emax,
                            material_, material1_, symmetry, symmetry1,lim_x,lim_y,
                            strain_calculation, ind_mat, ind_mat1,
                            model_direc=None, tolerance =None, tolerance1 =None,
                           matricies=None, ccd_label=None,
                           filename_bkg=None,intensity_threshold=None,
                           boxsize=None,bkg_treatment=None,
                           filenameDirec=None, experimental_prefix=None,
                           blacklist_file =None, text_file=None, 
                           files_treated=None,try_previous1=False,
                           wb=None, temp_key=None, cor_file_directory=None, mode_spotCycle1=None,
                           softmax_threshold_global123=None,mr_threshold_global123=None,
                           cap_matchrate123=None,tolerance_strain123=None,tolerance_strain1231=None,NumberMaxofFits123=None,fit_peaks_gaussian_global123=None,
                           FitPixelDev_global123=None,coeff123=None, coeff_overlap=None,
                           material0_limit=None, material1_limit=None, use_previous_UBmatrix_name=None,
                           material_phase_always_present=None):
    
        if files in files_treated:
            return strain_matrix, strain_matrixs, rotation_matrix, col, colx, coly, match_rate, mat_global, cnt, files_treated,spots_len,iR_pix,fR_pix, check, best_match
            
        if files.split(".")[1] != "cor":
            CCDLabel=ccd_label
            seednumber = "Experimental "+CCDLabel+" file"    
            
            try:
                out_name = blacklist_file
            except:
                out_name = None  
                
            if bkg_treatment == None:
                bkg_treatment = "A-B"
                
            try:
                ### Max space = space betzeen pixles
                peak_XY = RMCCD.PeakSearch(
                                            files,
                                            stackimageindex = -1,
                                            CCDLabel=CCDLabel,
                                            NumberMaxofFits=NumberMaxofFits123,
                                            PixelNearRadius=10,
                                            removeedge=2,
                                            IntensityThreshold=intensity_threshold,
                                            local_maxima_search_method=0,
                                            boxsize=boxsize,
                                            position_definition=1,
                                            verbose=0,
                                            fit_peaks_gaussian=fit_peaks_gaussian_global123,
                                            xtol=0.001,                
                                            FitPixelDev=FitPixelDev_global123,
                                            return_histo=0,
                                            # Saturation_value=1e10,  # to be merged in CCDLabel
                                            # Saturation_value_flatpeak=1e10,
                                            MinIntensity=0,
                                            PeakSizeRange=(0.65,200),
                                            write_execution_time=1,
                                            Data_for_localMaxima = "auto_background",
                                            formulaexpression=bkg_treatment,
                                            Remove_BlackListedPeaks_fromfile=out_name,
                                            reject_negative_baseline=True,
                                            Fit_with_Data_for_localMaxima=False,
                                            maxPixelDistanceRejection=15.0,
                                            )
                peak_XY = peak_XY[0]#[:,:2] ##[2] Integer peak lists
            except:
                print("Error in Peak detection for "+ files)
                for intmat in range(matricies):
                    rotation_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                    strain_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                    strain_matrixs[intmat][0][cnt,:,:] = np.zeros((3,3))
                    col[intmat][0][cnt,:] = 0,0,0
                    colx[intmat][0][cnt,:] = 0,0,0
                    coly[intmat][0][cnt,:] = 0,0,0
                    match_rate[intmat][0][cnt] = 0
                    mat_global[intmat][0][cnt] = 0
                    spots_len[intmat][0][cnt] = 0
                    iR_pix[intmat][0][cnt] = 0
                    fR_pix[intmat][0][cnt] = 0
                check[cnt] = 0
                # files_treated.append(files)
                return strain_matrix, strain_matrixs, rotation_matrix, col, colx, coly, match_rate, mat_global, cnt, files_treated,spots_len,iR_pix,fR_pix, check, best_match
            
            s_ix = np.argsort(peak_XY[:, 2])[::-1]
            peak_XY = peak_XY[s_ix]
            
            framedim = dictLT.dict_CCD[CCDLabel][0]
            twicetheta, chi = Lgeo.calc_uflab(peak_XY[:,0], peak_XY[:,1], detectorparameters,
                                                returnAngles=1,
                                                pixelsize=pixelsize,
                                                kf_direction='Z>0')
            data_theta, data_chi = twicetheta/2., chi
            
            framedim = dictLT.dict_CCD[CCDLabel][0]
            dict_dp={}
            dict_dp['kf_direction']='Z>0'
            dict_dp['detectorparameters']=detectorparameters
            dict_dp['detectordistance']=detectorparameters[0]
            dict_dp['detectordiameter']=pixelsize*framedim[0]
            dict_dp['pixelsize']=pixelsize
            dict_dp['dim']=framedim
            dict_dp['peakX']=peak_XY[:,0]
            dict_dp['peakY']=peak_XY[:,1]
            dict_dp['intensity']=peak_XY[:,2]
            
            CCDcalib = {"CCDLabel":CCDLabel,
                        "dd":detectorparameters[0], 
                        "xcen":detectorparameters[1], 
                        "ycen":detectorparameters[2], 
                        "xbet":detectorparameters[3], 
                        "xgam":detectorparameters[4],
                        "pixelsize": pixelsize}
            
            path = os.path.normpath(files)
            IOLT.writefile_cor(cor_file_directory+"//"+path.split(os.sep)[-1].split(".")[0], twicetheta, 
                               chi, peak_XY[:,0], peak_XY[:,1], peak_XY[:,2],
                               param=CCDcalib, sortedexit=0)
            
        elif files.split(".")[1] == "cor":
            seednumber = "Experimental COR file"
            allres = IOLT.readfile_cor(files, True)
            data_theta, data_chi, peakx, peaky, intensity = allres[1:6]
            CCDcalib = allres[-1]
            detectorparameters = allres[-2]
            # print('detectorparameters from file are: '+ str(detectorparameters))
            pixelsize = CCDcalib['pixelsize']
            CCDLabel = CCDcalib['CCDLabel']
            framedim = dictLT.dict_CCD[CCDLabel][0]
            dict_dp={}
            dict_dp['kf_direction']='Z>0'
            dict_dp['detectorparameters']=detectorparameters
            dict_dp['detectordistance']=detectorparameters[0]
            dict_dp['detectordiameter']=pixelsize*framedim[0]
            dict_dp['pixelsize']=pixelsize
            dict_dp['dim']=framedim
            dict_dp['peakX']=peakx
            dict_dp['peakY']=peaky
            dict_dp['intensity']=intensity
    
        sorted_data = np.transpose(np.array([data_theta, data_chi]))
        tabledistancerandom = np.transpose(GT.calculdist_from_thetachi(sorted_data, sorted_data))
    
        codebars_all = []
        
        if len(data_theta) == 0:
            print("No peaks Found for : " + files)
            for intmat in range(matricies):
                rotation_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                strain_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                strain_matrixs[intmat][0][cnt,:,:] = np.zeros((3,3))
                col[intmat][0][cnt,:] = 0,0,0
                colx[intmat][0][cnt,:] = 0,0,0
                coly[intmat][0][cnt,:] = 0,0,0
                match_rate[intmat][0][cnt] = 0
                mat_global[intmat][0][cnt] = 0
                spots_len[intmat][0][cnt] = 0
                iR_pix[intmat][0][cnt] = 0
                fR_pix[intmat][0][cnt] = 0
            check[cnt] = 0
            # files_treated.append(files)
            return strain_matrix, strain_matrixs, rotation_matrix, col, colx, coly, match_rate, mat_global, cnt, files_treated,spots_len,iR_pix,fR_pix, check, best_match
        
        spots_in_center = np.arange(0,len(data_theta))
    
        for i in spots_in_center:
            spotangles = tabledistancerandom[i]
            spotangles = np.delete(spotangles, i)# removing the self distance
            # codebars = np.histogram(spotangles, bins=angbins)[0]
            codebars = histogram1d(spotangles, range=[min(angbins),max(angbins)], bins=len(angbins)-1)
            ## normalize the same way as training data
            max_codebars = np.max(codebars)
            codebars = codebars/ max_codebars
            codebars_all.append(codebars)
            
        ## reshape for the model to predict all spots at once
        codebars = np.array(codebars_all)
        ## Do prediction of all spots at once
        prediction = AnotherWindowLivePrediction.predict(codebars, wb, temp_key)
        
        # prediction = model.predict(codebars)
        max_pred = np.max(prediction, axis = 1)
        class_predicted = np.argmax(prediction, axis = 1)
        
        predicted_hkl123 = classhkl[class_predicted]
        s_tth = data_theta * 2.
        s_chi = data_chi
        
        rotation_matrix1, mr_highest, mat_highest, \
            strain_crystal, strain_sample, iR_pix1, \
                        fR_pix1, spots_len1, best_match1 = AnotherWindowLivePrediction.predict_ubmatrix(seednumber, spots_in_center, classhkl, 
                                                                  hkl_all_class0, 
                                                                  hkl_all_class1, files,
                                                                    s_tth1=s_tth,s_chi1=s_chi,
                                                                    predicted_hkl1=predicted_hkl123,
                                                                    class_predicted1=class_predicted,
                                                                    max_pred1=max_pred,
                                                                    emin=emin,emax=emax,
                                                                    material_=material_, 
                                                                    material1_=material1_, 
                                                                    lim_y=lim_y, lim_x=lim_x, 
                                                                    cnt=cnt,
                                                                    dict_dp=dict_dp,
                                                                    rotation_matrix=rotation_matrix,
                                                                    mat_global=mat_global,
                                                                    strain_calculation=strain_calculation,
                                                                    ind_mat=ind_mat, 
                                                                    ind_mat1=ind_mat1,
                                                                    tolerance=tolerance, 
                                                                    tolerance1 =tolerance1,
                                                                    matricies=matricies,
                                                                    tabledistancerandom=tabledistancerandom,
                                                                    text_file = text_file,
                                                                    try_previous1=try_previous1,
                                                                    mode_spotCycle=mode_spotCycle1,
                                                                    softmax_threshold_global123 = softmax_threshold_global123,
                                                                    mr_threshold_global123=mr_threshold_global123,
                                                                    cap_matchrate123=cap_matchrate123,
                                                                    tolerance_strain123=tolerance_strain123,
                                                                    tolerance_strain1231=tolerance_strain1231,
                                                                    coeff123=coeff123,
                                                                    coeff_overlap=coeff_overlap,
                                                                    material0_limit=material0_limit, 
                                                                    material1_limit=material1_limit,
                                                                    model_direc=model_direc,
                                                                    use_previous_UBmatrix_name=use_previous_UBmatrix_name,
                                                                    material_phase_always_present=material_phase_always_present)
        for intmat in range(matricies):
            if len(rotation_matrix1[intmat]) == 0:
                col[intmat][0][cnt,:] = 0,0,0
                colx[intmat][0][cnt,:] = 0,0,0
                coly[intmat][0][cnt,:] = 0,0,0
            else:
                mat_global[intmat][0][cnt] = mat_highest[intmat][0]
                
                final_symm =symmetry
                if mat_highest[intmat][0] == 1:
                    final_symm = symmetry
                elif mat_highest[intmat][0] == 2:
                    final_symm = symmetry1
                    
                strain_matrix[intmat][0][cnt,:,:] = strain_crystal[intmat][0]
                strain_matrixs[intmat][0][cnt,:,:] = strain_sample[intmat][0]
                rotation_matrix[intmat][0][cnt,:,:] = rotation_matrix1[intmat][0]
                col_temp = AnotherWindowLivePrediction.get_ipf_colour(rotation_matrix1[intmat][0], np.array([0., 0., 1.]), final_symm)
                col[intmat][0][cnt,:] = col_temp
                col_tempx = AnotherWindowLivePrediction.get_ipf_colour(rotation_matrix1[intmat][0], np.array([1., 0., 0.]), final_symm)
                colx[intmat][0][cnt,:] = col_tempx
                col_tempy = AnotherWindowLivePrediction.get_ipf_colour(rotation_matrix1[intmat][0], np.array([0., 1., 0.]), final_symm)
                coly[intmat][0][cnt,:] = col_tempy
                match_rate[intmat][0][cnt] = mr_highest[intmat][0]
                spots_len[intmat][0][cnt] = spots_len1[intmat][0]
                iR_pix[intmat][0][cnt] = iR_pix1[intmat][0]
                fR_pix[intmat][0][cnt] = fR_pix1[intmat][0]
                best_match[intmat][0][cnt] = best_match1[intmat][0]
                check[cnt] = 1
                
        files_treated.append(files)
        return strain_matrix, strain_matrixs, rotation_matrix, col, colx, coly, match_rate, \
                mat_global, cnt, files_treated, spots_len, iR_pix, fR_pix, check, best_match
    
    @staticmethod
    def predict_ubmatrix(seednumber, spots_in_center, classhkl, hkl_all_class0, 
                         hkl_all_class1, filename, 
                         s_tth1,s_chi1,predicted_hkl1,class_predicted1,max_pred1,
                         emin, emax, material_, material1_, lim_y, lim_x, cnt,
                         dict_dp,rotation_matrix,mat_global,strain_calculation,
                         ind_mat, ind_mat1,
                         tolerance=None,  tolerance1 =None, matricies=None, tabledistancerandom=None,
                         text_file=None,try_previous1=False, mode_spotCycle=None,
                         softmax_threshold_global123=None,mr_threshold_global123=None,
                         cap_matchrate123=None, tolerance_strain123=None,tolerance_strain1231=None, coeff123=None,
                         coeff_overlap=None, material0_limit=None, material1_limit=None, model_direc=None,
                         use_previous_UBmatrix_name=None, material_phase_always_present=None):

        print("# Predicting for "+ filename)
        input_params = {"tolerance": tolerance,
                         "tolerance1":tolerance1,
                        "tolerancestrain": tolerance_strain123, ## For strain calculations
                        "tolerancestrain1": tolerance_strain1231,
                        "emin": emin,
                        "emax": emax,
                        "mat":0}
        
        strain_matrix = [[] for i in range(matricies)]
        strain_matrixs = [[] for i in range(matricies)]
        best_matrix = [[] for i in range(matricies)]
        mr_highest = [[] for i in range(matricies)]
        ir_pixels = [[] for i in range(matricies)]
        fr_pixels = [[] for i in range(matricies)]
        spots_len = [[] for i in range(matricies)]
        mat_highest = [[] for i in range(matricies)]
        best_match = [[] for i in range(matricies)]
        spots1 = []
        spots1_global = [[] for i in range(matricies)]
        dist = tabledistancerandom        
        ## one time calculations
        lattice_params0 = dictLT.dict_Materials[material_][1]
        B0 = CP.calc_B_RR(lattice_params0)
        Gstar_metric0 = CP.Gstar_from_directlatticeparams(lattice_params0[0],lattice_params0[1],\
                                                         lattice_params0[2],lattice_params0[3],\
                                                             lattice_params0[4],lattice_params0[5])
        tab_distance_classhkl_data0 = AnotherWindowLivePrediction.get_material_dataP(Gstar_metric0, predicted_hkl1)
        
        if material_ != material1_:
            lattice_params1 = dictLT.dict_Materials[material1_][1]
            B1 = CP.calc_B_RR(lattice_params1)
            Gstar_metric1 = CP.Gstar_from_directlatticeparams(lattice_params1[0],lattice_params1[1],\
                                                             lattice_params1[2],lattice_params1[3],\
                                                                 lattice_params1[4],lattice_params1[5])
            tab_distance_classhkl_data1 = AnotherWindowLivePrediction.get_material_dataP(Gstar_metric1, predicted_hkl1)
        else:
            tab_distance_classhkl_data1 = None
            Gstar_metric1 = None
            B1 = None
            
        newmethod = True
        all_stats1 = []
        sort_ind1 = []
        max_mr1 = 0
        min_mr1= 0 
        spots = []
        first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, np.zeros((3,3))]
        max_mr = 0
        mat = 0
        iR = 0
        fR = 0
        strain_crystal = np.zeros((3,3))
        strain_sample = np.zeros((3,3))
        material0_count = 0
        material1_count = 0
        calcul_done = False
        objective_function1 = None
        
        for igrain in range(matricies):
            try_previous = try_previous1
            max_mr, min_mr = 0, 0
            iR, fR= 0, 0
            ## self.cnt gives the file number count
            case = "None"
            
            if use_previous_UBmatrix_name:
                try:
                    try_previous = False
                    ### try already indexed UB matricies
                    load_objectind = np.load(model_direc+"//rotation_matrix_indexed.npz")
                    rotationmatrix_indexed = load_objectind["arr_0"]
                    mat_global_indexed = load_objectind["arr_1"]
                    match_rate_indexed = load_objectind["arr_2"]
                    calcul_done = False
                    for ind_mat_UBmat in range(len(rotationmatrix_indexed[igrain][0])):
                        if calcul_done:
                            continue
                        
                        if np.all(rotationmatrix_indexed[igrain][0][ind_mat_UBmat,:,:]) == 0:
                            continue
                        
                        mat = mat_global_indexed[igrain][0][ind_mat_UBmat]
                        if mat == 1:
                            Keymaterial_ = material_
                            case = material_
                            Bkey = B0
                            input_params["mat"] = 1
                        elif mat == 2:
                            Keymaterial_ = material1_
                            case = material1_
                            Bkey = B1
                            input_params["mat"] = 2
                        else:
                            Keymaterial_ = None
                            Bkey = None
                            input_params["mat"] = 0
                            continue
                        
                        spots_prev, theo_spots_prev = AnotherWindowLivePrediction.remove_spots(s_tth1, s_chi1, rotationmatrix_indexed[igrain][0][ind_mat_UBmat,:,:], 
                                                                     Keymaterial_, input_params, dict_dp['detectorparameters'],
                                                                     dict_dp)
                        newmatchrate = 100*len(spots_prev)/theo_spots_prev
                        condition_prev = newmatchrate < 0.9*(match_rate_indexed[igrain][0][ind_mat_UBmat])
                        
                        # overlap = False
                        # for igr in range(len(spots1_global)):
                        #     if spots_prev > coeff_overlap*len(spots1_global[igr]):
                        #         overlap = True
                        
                        if condition_prev or (newmatchrate <= cap_matchrate123):# or overlap:
                            try_previous = False
                        else:
                            calcul_done = True
                            if strain_calculation:
                                strain_crystal, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth1, s_chi1, 
                                                                                              rotationmatrix_indexed[igrain][0][ind_mat_UBmat,:,:],
                                                                                              Keymaterial_, 
                                                                                             input_params, dict_dp['detectorparameters'], 
                                                                                             dict_dp, spots1, Bkey)
                            else:
                                strain_crystal, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                                rot_mat_UB = np.copy(rotationmatrix_indexed[igrain][0][ind_mat_UBmat,:,:])
                            spots = spots_prev
                            expected = theo_spots_prev
                            max_mr, min_mr = 100*(len(spots)/expected), 100*(len(spots)/expected)
                            first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                            0, len(spots), expected, max_mr, 0, rot_mat_UB]
                except:
                    try_previous = False
                    calcul_done = False
            
            
            if try_previous and (cnt % lim_y == 0) and cnt != 0:
                if np.all(rotation_matrix[igrain][0][cnt-lim_y,:,:]) == 0:
                    try_previous = False
                else:
                    mat = mat_global[igrain][0][cnt-lim_y]
                    if mat == 1:
                        Keymaterial_ = material_
                        case = material_
                        Bkey = B0
                        input_params["mat"] = 1
                    elif mat == 2:
                        Keymaterial_ = material1_
                        case = material1_
                        Bkey = B1
                        input_params["mat"] = 2
                    else:
                        Keymaterial_ = None
                        Bkey = None
                        input_params["mat"] = 0
                        continue
                    
                    spots_lr, theo_spots_lr = AnotherWindowLivePrediction.remove_spots(s_tth1, s_chi1, 
                                                                rotation_matrix[igrain][0][cnt-lim_y,:,:], 
                                                             Keymaterial_, input_params, dict_dp['detectorparameters'],
                                                             dict_dp)
                    last_row = len(spots_lr) <= coeff123*theo_spots_lr
                    
                    if last_row: ## new spots less than 8 count, not good match SKIP
                        try_previous = False
                    else:
                        try_previous = True
                        current_spots = [len(list(set(spots_lr) & set(spots1_global[igr]))) > coeff_overlap*len(spots1_global[igr]) for igr in range(len(spots1_global))]
                        if np.any(current_spots):
                            try_previous = False
                            continue
                        
                        if strain_calculation:
                            strain_crystal, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth1, s_chi1, 
                                                                                          rotation_matrix[igrain][0][cnt-lim_y,:,:], 
                                                                                          Keymaterial_, 
                                                                                         input_params, dict_dp['detectorparameters'], 
                                                                                         dict_dp, spots1, Bkey)
                        else:
                            strain_crystal, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                            rot_mat_UB = np.copy(rotation_matrix[igrain][0][cnt-lim_y,:,:])
                        spots = spots_lr
                        expected = theo_spots_lr
                        max_mr, min_mr = 100*(len(spots_lr)/theo_spots_lr), 100*(len(spots_lr)/theo_spots_lr)
                        first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                        0, len(spots), expected, max_mr, 0, rot_mat_UB]   
                    
            elif try_previous and (cnt % lim_y != 0):
                last_row = True
                left_row = True
                if np.all(rotation_matrix[igrain][0][cnt-1,:,:]) == 0:
                    left_row = True
                else:
                    mat = mat_global[igrain][0][cnt-1]
                    if mat == 1:
                        Keymaterial_ = material_
                        case = material_
                        Bkey = B0
                        input_params["mat"] = 1
                    elif mat == 2:
                        Keymaterial_ = material1_
                        case = material1_
                        Bkey = B1
                        input_params["mat"] = 2
                    else:
                        Keymaterial_ = None
                        Bkey = None
                        input_params["mat"] = 0
                        continue
                    ## new row start when % == 0
                    ## use left index pixels matrix values
                    spots_left, theo_spots_left = AnotherWindowLivePrediction.remove_spots(s_tth1, s_chi1, rotation_matrix[igrain][0][cnt-1,:,:], 
                                                             Keymaterial_, input_params, dict_dp['detectorparameters'],
                                                             dict_dp)
                    left_row = len(spots_left) <= coeff123*theo_spots_left 
                
                if cnt >= lim_y:
                    if np.all(rotation_matrix[igrain][0][cnt-lim_y,:,:]) == 0:
                        last_row = True   
                    else:
                        mat = mat_global[igrain][0][cnt-lim_y]
                        if mat == 1:
                            Keymaterial_ = material_
                            case = material_
                            Bkey = B0
                            input_params["mat"] = 1
                        elif mat == 2:
                            Keymaterial_ = material1_
                            case = material1_
                            Bkey = B1
                            input_params["mat"] = 2
                        else:
                            Keymaterial_ = None
                            Bkey = None
                            input_params["mat"] = 0
                            continue
                        ## use bottom index pixels matrix values
                        spots_lr, theo_spots_lr = AnotherWindowLivePrediction.remove_spots(s_tth1, s_chi1, rotation_matrix[igrain][0][cnt-lim_y,:,:], 
                                                                 Keymaterial_, input_params, dict_dp['detectorparameters'],
                                                                 dict_dp)
                        
                        last_row = len(spots_lr) <= coeff123*theo_spots_lr 
                    
                    
                if left_row and last_row: 
                    try_previous = False
                
                elif not left_row and not last_row:
                    try_previous = True
                    
                    if len(spots_lr) > len(spots_left):
                        current_spots = [len(list(set(spots_lr) & set(spots1_global[igr]))) > coeff_overlap*len(spots1_global[igr]) for igr in range(len(spots1_global))]
                        if np.any(current_spots):
                            try_previous = False
                            continue
                        
                        mat = mat_global[igrain][0][cnt-lim_y]
                        if mat == 1:
                            Keymaterial_ = material_
                            case = material_
                            Bkey = B0
                            input_params["mat"] = 1
                        elif mat == 2:
                            Keymaterial_ = material1_
                            case = material1_
                            Bkey = B1
                            input_params["mat"] = 2
                        else:
                            Keymaterial_ = None
                            Bkey = None
                            input_params["mat"] = 0
                            continue
                        
                        if strain_calculation:
                            strain_crystal, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth1, s_chi1, 
                                                                                          rotation_matrix[igrain][0][cnt-lim_y,:,:], 
                                                                                          Keymaterial_, 
                                                                                         input_params, dict_dp['detectorparameters'], 
                                                                                         dict_dp, spots1, Bkey)
                        else:
                            strain_crystal, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                            rot_mat_UB = np.copy(rotation_matrix[igrain][0][cnt-lim_y,:,:])
                        spots = spots_lr
                        expected = theo_spots_lr
                        max_mr, min_mr = 100*(len(spots_lr)/theo_spots_lr), 100*(len(spots_lr)/theo_spots_lr)
                        first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                    0, len(spots), expected, max_mr, 0, rot_mat_UB]
                    else:
                        current_spots = [len(list(set(spots_left) & set(spots1_global[igr]))) > coeff_overlap*len(spots1_global[igr]) for igr in range(len(spots1_global))]
                        if np.any(current_spots):
                            try_previous = False
                            continue
    
                        mat = mat_global[igrain][0][cnt-1]
                        if mat == 1:
                            Keymaterial_ = material_
                            case = material_
                            Bkey = B0
                            input_params["mat"] = 1
                        elif mat == 2:
                            Keymaterial_ = material1_
                            case = material1_
                            Bkey = B1
                            input_params["mat"] = 2
                        else:
                            Keymaterial_ = None
                            Bkey = None
                            input_params["mat"] = 0
                            continue
                        
                        if strain_calculation:
                            strain_crystal, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth1, s_chi1, 
                                                                                          rotation_matrix[igrain][0][cnt-1,:,:], 
                                                                                          Keymaterial_, 
                                                                                         input_params, dict_dp['detectorparameters'], 
                                                                                         dict_dp, spots1, Bkey)
                        else:
                            strain_crystal, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                            rot_mat_UB = np.copy(rotation_matrix[igrain][0][cnt-1,:,:])
                        spots = spots_left
                        expected = theo_spots_left
                        max_mr, min_mr = 100*(len(spots_left)/theo_spots_left), 100*(len(spots_left)/theo_spots_left)
                        first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                    0, len(spots), expected, max_mr, 0, rot_mat_UB]    
                
                elif not left_row and last_row:
                    try_previous = True
                    current_spots = [len(list(set(spots_left) & set(spots1_global[igr]))) > coeff_overlap*len(spots1_global[igr]) for igr in range(len(spots1_global))]
                    if np.any(current_spots):
                        try_previous = False
                        continue
                    
                    mat = mat_global[igrain][0][cnt-1]
                    if mat == 1:
                        Keymaterial_ = material_
                        case = material_
                        Bkey = B0
                        input_params["mat"] = 1
                    elif mat == 2:
                        Keymaterial_ = material1_
                        case = material1_
                        Bkey = B1
                        input_params["mat"] = 2
                    else:
                        Keymaterial_ = None
                        Bkey = None
                        input_params["mat"] = 0
                        continue
                    
                    if strain_calculation:
                        strain_crystal, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth1, s_chi1, 
                                                                                      rotation_matrix[igrain][0][cnt-1,:,:], 
                                                                                      Keymaterial_, 
                                                                                     input_params, dict_dp['detectorparameters'], 
                                                                                     dict_dp, spots1, Bkey)
                    else:
                        strain_crystal, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                        rot_mat_UB = np.copy(rotation_matrix[igrain][0][cnt-1,:,:])
                    spots = spots_left
                    expected = theo_spots_left
                    max_mr, min_mr = 100*(len(spots_left)/theo_spots_left), 100*(len(spots_left)/theo_spots_left)
                    first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                    0, len(spots), expected, max_mr, 0, rot_mat_UB]  
                        
                elif left_row and not last_row:
                    try_previous = True
                    current_spots = [len(list(set(spots_lr) & set(spots1_global[igr]))) > coeff_overlap*len(spots1_global[igr]) for igr in range(len(spots1_global))]
                    if np.any(current_spots):
                        try_previous = False
                        continue
                    
                    mat = mat_global[igrain][0][cnt-lim_y]
                    if mat == 1:
                        Keymaterial_ = material_
                        case = material_
                        Bkey = B0
                        input_params["mat"] = 1
                    elif mat == 2:
                        Keymaterial_ = material1_
                        case = material1_
                        Bkey = B1
                        input_params["mat"] = 2
                    else:
                        Keymaterial_ = None
                        Bkey = None
                        input_params["mat"] = 0
                        continue
                    
                    if strain_calculation:
                        strain_crystal, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth1, s_chi1, 
                                                                                      rotation_matrix[igrain][0][cnt-lim_y,:,:], 
                                                                                      Keymaterial_, 
                                                                                     input_params, dict_dp['detectorparameters'], 
                                                                                     dict_dp, spots1, Bkey)
                    else:
                        strain_crystal, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                        rot_mat_UB = np.copy(rotation_matrix[igrain][0][cnt-lim_y,:,:])
                        
                    spots = spots_lr
                    expected = theo_spots_lr    
                    max_mr, min_mr = 100*(len(spots_lr)/theo_spots_lr), 100*(len(spots_lr)/theo_spots_lr)
                    first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                    0, len(spots), expected, max_mr, 0, rot_mat_UB]  
    
            else:
                try_previous = False
            
            if not try_previous and not calcul_done:
                ### old version
                if mode_spotCycle == "slow":
                    # print("Slow mode of analysis")
                    first_match, max_mr, min_mr, spots, \
                            case, mat, strain_crystal, \
                                strain_sample, iR, fR  = AnotherWindowLivePrediction.get_orient_mat(s_tth1, s_chi1,
                                                                            material_, material1_, classhkl,
                                                                            class_predicted1, predicted_hkl1,
                                                                            input_params, hkl_all_class0, hkl_all_class1,
                                                                            max_pred1, dict_dp, 
                                                                            spots1, dist, 
                                                                            Gstar_metric0, Gstar_metric1, B0, B1,
                                                                            softmax_threshold=softmax_threshold_global123,
                                                                            mr_threshold=mr_threshold_global123,
                                                                            tab_distance_classhkl_data0=tab_distance_classhkl_data0,
                                                                            tab_distance_classhkl_data1=tab_distance_classhkl_data1,
                                                                            spots1_global = spots1_global,
                                                                            coeff_overlap = coeff_overlap,
                                                                            ind_mat=ind_mat, ind_mat1=ind_mat1, 
                                                                            strain_calculation=strain_calculation,
                                                                            cap_matchrate123=cap_matchrate123,
                                                                            material0_count=material0_count,
                                                                            material1_count=material1_count,
                                                                            material0_limit=material0_limit,
                                                                            material1_limit=material1_limit,
                                                                            igrain=igrain,
                                                                            material_phase_always_present=material_phase_always_present)
                elif mode_spotCycle == "fast":
                    # print("Fast mode of analysis")
                    first_match, max_mr, min_mr, spots, \
                            case, mat, strain_crystal, \
                                strain_sample, iR, fR  = AnotherWindowLivePrediction.get_orient_mat_fastv0(s_tth1, s_chi1,
                                                                            material_, material1_, classhkl,
                                                                            class_predicted1, predicted_hkl1,
                                                                            input_params, hkl_all_class0, hkl_all_class1,
                                                                            max_pred1, dict_dp, 
                                                                            spots1, dist, 
                                                                            Gstar_metric0, Gstar_metric1, B0, B1,
                                                                            softmax_threshold=softmax_threshold_global123,
                                                                            mr_threshold=mr_threshold_global123,
                                                                            tab_distance_classhkl_data0=tab_distance_classhkl_data0,
                                                                            tab_distance_classhkl_data1=tab_distance_classhkl_data1,
                                                                            spots1_global = spots1_global,
                                                                            coeff_overlap = coeff_overlap,
                                                                            ind_mat=ind_mat, ind_mat1=ind_mat1, 
                                                                            strain_calculation=strain_calculation,
                                                                            cap_matchrate123=cap_matchrate123,
                                                                            material0_count=material0_count,
                                                                            material1_count=material1_count,
                                                                            material0_limit=material0_limit,
                                                                            material1_limit=material1_limit,
                                                                            igrain=igrain,
                                                                            material_phase_always_present=material_phase_always_present)
                elif mode_spotCycle == "graphmode":
                    # print("Fast mode of analysis")
                    first_match, max_mr, min_mr, spots, \
                            case, mat, strain_crystal, \
                                strain_sample, iR, fR,objective_function1  = AnotherWindowLivePrediction.get_orient_mat_graph(s_tth1, s_chi1,
                                                                            material_, material1_, classhkl,
                                                                            class_predicted1, predicted_hkl1,
                                                                            input_params, hkl_all_class0, hkl_all_class1,
                                                                            max_pred1, dict_dp, 
                                                                            spots1, dist, 
                                                                            Gstar_metric0, Gstar_metric1, B0, B1,
                                                                            softmax_threshold=softmax_threshold_global123,
                                                                            mr_threshold=mr_threshold_global123,
                                                                            tab_distance_classhkl_data0=tab_distance_classhkl_data0,
                                                                            tab_distance_classhkl_data1=tab_distance_classhkl_data1,
                                                                            spots1_global = spots1_global,
                                                                            coeff_overlap = coeff_overlap,
                                                                            ind_mat=ind_mat, ind_mat1=ind_mat1, 
                                                                            strain_calculation=strain_calculation,
                                                                            cap_matchrate123=cap_matchrate123,
                                                                            material0_count=material0_count,
                                                                            material1_count=material1_count,
                                                                            material0_limit=material0_limit,
                                                                            material1_limit=material1_limit,
                                                                            igrain=igrain,
                                                                            material_phase_always_present=material_phase_always_present,
                                                                            objective_function= objective_function1)
                elif mode_spotCycle == "beamtime":
                    # print("Beamtime mode of analysis")
                    first_match, max_mr, min_mr, spots, \
                            case, mat, strain_crystal, \
                                strain_sample, iR, fR  = AnotherWindowLivePrediction.get_orient_mat_fast(s_tth1, s_chi1,
                                                                            material_, material1_, classhkl,
                                                                            class_predicted1, predicted_hkl1,
                                                                            input_params, hkl_all_class0, hkl_all_class1,
                                                                            max_pred1, dict_dp, 
                                                                            spots1, dist, 
                                                                            Gstar_metric0, Gstar_metric1, B0, B1,
                                                                            softmax_threshold=softmax_threshold_global123,
                                                                            mr_threshold=mr_threshold_global123,
                                                                            tab_distance_classhkl_data0=tab_distance_classhkl_data0,
                                                                            tab_distance_classhkl_data1=tab_distance_classhkl_data1,
                                                                            spots1_global = spots1_global,
                                                                            coeff_overlap = coeff_overlap,
                                                                            ind_mat=ind_mat, ind_mat1=ind_mat1, 
                                                                            strain_calculation=strain_calculation,
                                                                            cap_matchrate123=cap_matchrate123,
                                                                            material0_count=material0_count,
                                                                            material1_count=material1_count,
                                                                            material0_limit=material0_limit,
                                                                            material1_limit=material1_limit,
                                                                            igrain=igrain,
                                                                            material_phase_always_present=material_phase_always_present)
                elif mode_spotCycle == "multiorimat":
                    print("Experimental mode only for one phase: be carefull")
                    # print("Multiorimat mode of analysis")
                    first_match, max_mr, min_mr, spots, \
                            case, mat, strain_crystal, \
                                strain_sample, iR, fR,\
                                    all_stats1, sort_ind1,\
                                    max_mr1, min_mr1 = AnotherWindowLivePrediction.get_orient_mat_whole(s_tth1, s_chi1, 
                                                                material_, classhkl, class_predicted1, predicted_hkl1,
                                                                input_params, hkl_all_class0, max_pred1, dict_dp,
                                                                dist, Gstar_metric0, B0, spots1, softmax_threshold=softmax_threshold_global123, 
                                                                mr_threshold=mr_threshold_global123, 
                                                               tab_distance_classhkl_data=tab_distance_classhkl_data0, 
                                                               spots1_global=spots1_global,
                                                               coeff_overlap = coeff_overlap, 
                                                               strain_calculation=strain_calculation,
                                                               indgrain=igrain, flag = newmethod,
                                                               all_stats=all_stats1, sort_ind=sort_ind1, 
                                                               max_mr=max_mr1, min_mr=min_mr1)
                    newmethod = False
                    
            for ispot in spots:
                spots1.append(ispot)
                spots1_global[igrain].append(ispot)
    
            ## make copy of best rotation matrix
            best_match[igrain].append(np.copy(first_match))
            best_matrix[igrain].append(np.copy(first_match[14]))
            mr_highest[igrain].append(np.copy(max_mr))
            mat_highest[igrain].append(np.copy(mat))
            ir_pixels[igrain].append(np.copy(iR))
            fr_pixels[igrain].append(np.copy(fR))
            spots_len[igrain].append(np.copy(len(spots)))
            strain_matrix[igrain].append(np.copy(strain_crystal))
            strain_matrixs[igrain].append(np.copy(strain_sample))
            
            if mat == 1:
                material0_count += 1
            if mat == 2:
                material1_count += 1
                
        return best_matrix, mr_highest, mat_highest, strain_matrix, strain_matrixs, ir_pixels, fr_pixels, spots_len, best_match
    
    @staticmethod
    def get_material_dataP(Gstar, classhkl = None):
        hkl2 = np.copy(classhkl)
        hkl1 = np.copy(classhkl)
        # compute square matrix containing angles
        metrics = Gstar
        H1 = hkl1
        n1 = hkl1.shape[0]
        H2 = hkl2
        n2 = hkl2.shape[0]
        dstar_square_1 = np.diag(np.inner(np.inner(H1, metrics), H1))
        dstar_square_2 = np.diag(np.inner(np.inner(H2, metrics), H2))
        scalar_product = np.inner(np.inner(H1, metrics), H2) * 1.0
        d1 = np.sqrt(dstar_square_1.reshape((n1, 1))) * 1.0
        d2 = np.sqrt(dstar_square_2.reshape((n2, 1))) * 1.0
        outy = np.outer(d1, d2)
        ratio = scalar_product / outy
        ratio = np.round(ratio, decimals=7)
        tab_angulardist = np.arccos(ratio) / (np.pi / 180.0)
        np.putmask(tab_angulardist, np.abs(tab_angulardist) < 0.001, 400)
        return tab_angulardist
    
    @staticmethod
    def get_orient_mat_whole(s_tth, s_chi, material_, classhkl, class_predicted, predicted_hkl,
                                input_params, hkl_all_class0, max_pred, dict_dp,
                                dist, Gstar_metric, B, spots, softmax_threshold=0.85, mr_threshold=0.85, 
                               tab_distance_classhkl_data=None, spots1_global=None,
                               coeff_overlap = None, strain_calculation=None, indgrain=None, flag=None,
                               all_stats=None, sort_ind=None, max_mr=None, min_mr=None):
        
        case = material_
        mat = 1       
        if flag:
            all_stats = []
            for i in range(len(s_tth)):
                for j in range(i+1, len(s_tth)):                
                    _dist = dist[i,j]
                    distance_ = tab_distance_classhkl_data[i,j]
                    
                    if max_pred[i] > softmax_threshold and max_pred[j] > softmax_threshold:
                        
                        hkl1 = hkl_all_class0[str(predicted_hkl[i])]
                        hkl1_list = np.array(hkl1)
                        hkl2 = hkl_all_class0[str(predicted_hkl[j])]
                        hkl2_list = np.array(hkl2)
                        hkl_all = np.vstack((hkl1_list, hkl2_list))
                        
                        LUT = FindO.GenerateLookUpTable(hkl_all, Gstar_metric)
                        hkls = FindO.PlanePairs_2(_dist, 0.5, LUT, onlyclosest=1)
                        
                        tth_chi_spot1 = np.array([s_tth[i], s_chi[i]])
                        tth_chi_spot2 = np.array([s_tth[j], s_chi[j]])
                        
                        allres, nbclose, nballres, rot_mat = [], [], [], []
                        rot_mat_abs = []
        
                        if np.all(hkls == None):
                            continue
                        # implement the same operator for families considered
                        for ii in range(len(hkls)):
                            conti_ = False
                            
                            if np.all(hkls[ii][0] == hkls[ii][1]):
                                continue
                            
                            try: ## valueError due to same HKl vectors (of different grains?)
                                rot_mat1 = FindO.OrientMatrix_from_2hkl(hkls[ii][0], tth_chi_spot1, \
                                                                        hkls[ii][1], tth_chi_spot2,
                                                                        B)
                            except:
                                continue
                            
                            copy_rm = np.copy(rot_mat1)
                            copy_rm = np.round(np.abs(copy_rm),6)
                            copy_rm.sort(axis=1)
                            for iji in rot_mat_abs:
                                iji.sort(axis=1)
                                if np.all(iji==copy_rm):
                                    conti_ = True
                                    break
            
                            if conti_:
                                continue
                            ## get matching rate of the rotation matrix
                            AngRes = Angular_residues_np(rot_mat1, s_tth, s_chi,
                                                        key_material=material_,
                                                        emax=input_params["emax"],
                                                        ResolutionAngstrom=False,
                                                        ang_tol=input_params["tolerance"],
                                                        detectorparameters=dict_dp,
                                                        dictmaterials=dictLT.dict_Materials)     
                            (allres1, _, nbclose1, nballres1, _, _) = AngRes
                                  
                            allres.append(np.std(allres1))
                            nbclose.append(nbclose1)
                            nballres.append(nballres1)
                            rot_mat.append(rot_mat1)
                            rot_mat_abs.append(np.round(np.abs(rot_mat1),6))
                            
                        match_rate = np.array(nbclose)/np.array(nballres)
                        if len(match_rate) == 0:
                            continue
                        ind_mr = np.argmax(match_rate)
            
                        all_stats.append([i, j, \
                                          predicted_hkl[i], predicted_hkl[j], \
                                          tth_chi_spot1, tth_chi_spot2, \
                                          _dist, distance_, np.round(max_pred[i]*100,3), \
                                          np.round(max_pred[j]*100,3), nbclose[ind_mr], nballres[ind_mr],\
                                          match_rate[ind_mr]*100, allres[ind_mr], rot_mat[ind_mr]])

            ## sort indices by matchrate (first matrix)
            sort_ind = []
            for i in all_stats:
                sort_ind.append(i[-3])
            sort_ind = np.array(sort_ind)
            max_mr, min_mr = np.max(sort_ind), np.min(sort_ind)
            sort_ind = np.argsort(sort_ind)[::-1]
        
        if len(all_stats) == 0: ## Nothing found!! 
        ## Either peaks are not well defined or not found within tolerance and prediction accuracy
            first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                0, 0, 0, 0, 0, np.zeros((3,3))]
            max_mr, min_mr = 0, 0
            print("Nothing Found")
            rmv_ind = []
            return first_match, max_mr, min_mr, rmv_ind, case, mat, np.zeros(3,3), np.zeros(3,3), 0, 0, [], [], 0, 0

        for iii in range(len(sort_ind)):
            first_match = all_stats[sort_ind[iii]]
            ##update list            
            rmv_ind, theospots = AnotherWindowLivePrediction.remove_spots(s_tth, s_chi, first_match[14], 
                                                            material_, input_params, 
                                                            dict_dp['detectorparameters'], dict_dp)          
            overlap = False
            current_spots = [len(list(set(rmv_ind) & set(spots1_global[igr]))) > coeff_overlap*len(spots1_global[igr]) for igr in range(len(spots1_global))]
            if np.any(current_spots):
                overlap = True
            if not overlap:
                break
       
        if overlap:
            first_match = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                0, 0, 0, 0, 0, np.zeros((3,3))]
            max_mr, min_mr = 0, 0
            print("Nothing Found")
            rmv_ind = []
            return first_match, max_mr, min_mr, rmv_ind, case, mat, np.zeros(3,3), np.zeros(3,3), 0, 0, [], [], 0, 0
        
        
        if strain_calculation:
            dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, first_match[14], material_, 
                                                                 input_params, dict_dp['detectorparameters'], 
                                                                 dict_dp, spots, B)
        else:
            dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
            rot_mat_UB = np.copy(first_match[14])
        
        first_match[14] = rot_mat_UB
        return first_match, max_mr, min_mr, \
                rmv_ind, str(case), mat, dev_strain, strain_sample, iR, fR, all_stats, sort_ind, max_mr, min_mr
    
    @staticmethod
    def get_orient_mat_graph(s_tth, s_chi, material0_, material1_, classhkl, class_predicted, predicted_hkl,
                           input_params, hkl_all_class0, hkl_all_class1, max_pred, dict_dp, spots, 
                           dist, Gstar_metric0, Gstar_metric1, B0, B1, softmax_threshold=0.85, mr_threshold=0.85, 
                           tab_distance_classhkl_data0=None, tab_distance_classhkl_data1=None, spots1_global=None,
                           coeff_overlap = None, ind_mat=None, ind_mat1=None, strain_calculation=None, cap_matchrate123=None,
                           material0_count=None, material1_count=None, material0_limit=None, material1_limit=None,
                           igrain=None, material_phase_always_present=None, objective_function=None):
        
        if objective_function == None:
            init_mr = 0
            init_mat = 0
            init_material = "None"
            init_case = "None"
            init_B = None
            final_match_rate = 0
            match_rate_mma = []
            final_rmv_ind = []
    
            if material0_ == material1_:
                list_of_sets = []
                for ii in range(len(dist)):
                    if max_pred[ii] < softmax_threshold:
                        continue 
                    a1 = np.round(dist[ii],3)
                    a2 = np.round(tab_distance_classhkl_data0[ii],3)
                    for i in range(len(dist)):
                        if max_pred[i] < softmax_threshold:
                            continue
                        if np.abs(a1[i] - a2[i]) <= input_params["tolerance"]:
                            list_of_sets.append((ii,i))
            else:
                list_of_sets = []
                for ii in range(len(dist)):
                    if max_pred[ii] < softmax_threshold:
                        continue 
                    for i in range(len(dist)):
                        if max_pred[i] < softmax_threshold:
                            continue
                        if class_predicted[ii] < ind_mat and class_predicted[i] < ind_mat:
                            tab_distance_classhkl_data = tab_distance_classhkl_data0
                            tolerance_new = input_params["tolerance"]
                        elif (ind_mat <= class_predicted[ii] < (ind_mat+ind_mat1)) and \
                                            (ind_mat <= class_predicted[i] < (ind_mat+ind_mat1)):
                            tab_distance_classhkl_data = tab_distance_classhkl_data1
                            tolerance_new = input_params["tolerance1"]
                        else:
                            continue
                        a1 = np.round(dist[ii],3)
                        a2 = np.round(tab_distance_classhkl_data[ii],3)
                        if np.abs(a1[i] - a2[i]) <= tolerance_new:
                            list_of_sets.append((ii,i))
            
            ## build a direct connection graph object
            graph_obj = nx.DiGraph(list_of_sets)
            connected_nodes_length = []
            connected_nodes = [[] for i in range(len(graph_obj))]
            for i,line in enumerate(nx.generate_adjlist(graph_obj)):
                connected_nodes_length.append(len(line.split(" ")))
                connected_nodes[i].append([int(jj) for jj in line.split(" ")])
            
            ## sort by maximum node occurance
            connected_nodes_length = np.array(connected_nodes_length)
            connected_nodes_length_sort_ind = np.argsort(connected_nodes_length)[::-1]
      
            mat = 0
            case = "None"
            tried_spots = []
            
            objective_function = []
            for toplist in range(len(graph_obj)):
                overlap = False
                ## continue if less than 3 connections are found for a graph
                if connected_nodes_length[connected_nodes_length_sort_ind[toplist]] < 3:
                    continue
                
                for j in connected_nodes[connected_nodes_length_sort_ind[toplist]][0]:
                    init_mr = 0
                    final_match_rate = 0
                    final_rmv_ind = []
                    all_stats = []
                    for i in connected_nodes[connected_nodes_length_sort_ind[toplist]][0]:
                        if j == i:
                            continue
                        
                        if j in tried_spots and i in tried_spots:
                            continue
                        
                        if material0_ == material1_:
                            tab_distance_classhkl_data = tab_distance_classhkl_data0
                            hkl_all_class = hkl_all_class0
                            material_ = material0_
                            B = B0
                            Gstar_metric = Gstar_metric0
                            case = material_
                            mat = 1
                            input_params["mat"] = mat
                        else:
                            if class_predicted[i] < ind_mat and class_predicted[j] < ind_mat:
                                tab_distance_classhkl_data = tab_distance_classhkl_data0
                                hkl_all_class = hkl_all_class0
                                material_ = material0_
                                B = B0
                                Gstar_metric = Gstar_metric0
                                case = material_
                                mat = 1
                                input_params["mat"] = mat
                            elif (ind_mat <= class_predicted[i] < (ind_mat+ind_mat1)) and \
                                                (ind_mat <= class_predicted[j] < (ind_mat+ind_mat1)):
                                tab_distance_classhkl_data = tab_distance_classhkl_data1
                                hkl_all_class = hkl_all_class1
                                material_ = material1_
                                B = B1
                                Gstar_metric = Gstar_metric1
                                case = material_  
                                mat = 2
                                input_params["mat"] = mat
                            else:
                                mat = 0
                                case = "None"
                                input_params["mat"] = mat
                        
                        if mat == 0:
                            continue                    
                        
                        tth_chi_spot1 = np.array([s_tth[i], s_chi[i]])
                        tth_chi_spot2 = np.array([s_tth[j], s_chi[j]])         
            
                        hkl1 = hkl_all_class[str(predicted_hkl[i])]
                        hkl1_list = np.array(hkl1)
                        hkl2 = hkl_all_class[str(predicted_hkl[j])]
                        hkl2_list = np.array(hkl2)
                        
                        actual_mat, flagAM, \
                        spot1_hkl, spot2_hkl = AnotherWindowLivePrediction.propose_UB_matrix(hkl1_list, hkl2_list, 
                                                                                           Gstar_metric, input_params, 
                                                                                           dist[i,j],
                                                                                           tth_chi_spot1, tth_chi_spot2, 
                                                                                           B, method=0)
                        
                        if flagAM:
                            continue
                        
                        for iind in range(len(actual_mat)):
                            rot_mat123 = actual_mat[iind]
                            
                            # if mat == 1:
                            #     AngRes = Angular_residues_np(rot_mat123, s_tth, s_chi,
                            #                                 key_material=material_,
                            #                                 emax=input_params["emax"],
                            #                                 ResolutionAngstrom=False,
                            #                                 ang_tol=input_params["tolerance"],
                            #                                 detectorparameters=dict_dp,
                            #                                 dictmaterials=dictLT.dict_Materials)
                            # else:
                            #     AngRes = Angular_residues_np(rot_mat123, s_tth, s_chi,
                            #                                 key_material=material_,
                            #                                 emax=input_params["emax"],
                            #                                 ResolutionAngstrom=False,
                            #                                 ang_tol=input_params["tolerance1"],
                            #                                 detectorparameters=dict_dp,
                            #                                 dictmaterials=dictLT.dict_Materials) 
                            # (allres1, _, nbclose1, nballres1, _, _) = AngRes                            
                            # match_rate = 100 * np.array(nbclose1)/np.array(nballres1)
                        
                            rmv_ind, theospots = AnotherWindowLivePrediction.remove_spots(s_tth, s_chi, rot_mat123, 
                                                                    material_, input_params, 
                                                                    dict_dp['detectorparameters'], dict_dp)
                            
                            match_rate = np.round(100 * len(rmv_ind)/theospots, 3)
                            
                            match_rate_mma.append(match_rate)
                            # TODO verify and remove
                            # tm1 = 0
                            # tm2 = 1
                            # if match_rate == init_mr:
                            #     temp_mat = np.matmul(rot_mat123, B)
                            #     tm1, tm2 = np.argmin(np.abs(temp_mat[:,:2]), axis=0)
                            # if tm1 != 0 or tm2!= 1:
                            #     continue
                                
                            if match_rate > init_mr:                                
                                final_rmv_ind = rmv_ind                    
                                init_mat = np.copy(mat)
                                input_params["mat"] = init_mat
                                init_material = np.copy(material_)
                                init_case = np.copy(case)
                                init_B = np.copy(B)                                     
                                final_match_rate = np.copy(match_rate)
                                init_mr = np.copy(match_rate)                   
                                all_stats = [i, j, \
                                             spot1_hkl[iind], spot2_hkl[iind], \
                                            tth_chi_spot1, tth_chi_spot2, \
                                            dist[i,j], tab_distance_classhkl_data[i,j], np.round(max_pred[i]*100,3), \
                                            np.round(max_pred[j]*100,3), len(rmv_ind), theospots,\
                                            match_rate, 0.0, rot_mat123, init_mat, init_material, init_B, init_case]
                        tried_spots.append(i)                 
                        
                    if (final_match_rate <= cap_matchrate123) or overlap: ## Nothing found!! 
                        ## Either peaks are not well defined or not found within tolerance and prediction accuracy
                        all_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                            0, 0, 0, 0, 0, np.zeros((3,3))]
                        max_mr, min_mr = 0, 0
                        spot_ind = []
                        mat = 0
                        input_params["mat"] = 0
                        case = "None"
                        objective_function.append([0, [], []])
                    else:
                        objective_function.append([final_match_rate, final_rmv_ind, all_stats])     
                    tried_spots.append(j)
     
        sort_ind = []
        for ijk in objective_function:
            sort_ind.append(ijk[0])
        sort_ind = np.array(sort_ind)
        sort_ind = np.argsort(sort_ind)[::-1]
        
        for gr_count123 in range(len(sort_ind)):           
            max_mr = objective_function[sort_ind[gr_count123]][0]
            rmv_ind = objective_function[sort_ind[gr_count123]][1]
            all_stats = objective_function[sort_ind[gr_count123]][2]
            
            if len(rmv_ind) == 0 or max_mr==0:
                continue
            
            mat = all_stats[15]
            if mat == 1:
                if igrain==0 and material_phase_always_present ==2:
                    mat = 0
                    case="None"
                if material0_count >= material0_limit:
                    mat = 0
                    case="None"
            elif mat == 2:
                if igrain==0 and material_phase_always_present ==1:
                    mat = 0
                    case="None"
                if material1_count >= material1_limit:
                    mat = 0
                    case="None"
            
            if mat == 0:
                continue

            current_spots = [len(list(set(rmv_ind) & set(spots1_global[igr])))> 0.3*len(spots1_global[igr]) for igr in range(len(spots1_global))]
            
            if np.any(current_spots):
                continue
                      
            input_params["mat"] = all_stats[15]
            if strain_calculation:
                dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(all_stats[16]), 
                                                                     input_params, dict_dp['detectorparameters'], 
                                                                     dict_dp, spots, all_stats[17])
            else:
                dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                rot_mat_UB = np.copy(all_stats[14])
            all_stats[14] = rot_mat_UB     
            
            return all_stats, np.max(max_mr), np.min(max_mr), \
                    rmv_ind, str(all_stats[18]), all_stats[15], dev_strain, strain_sample, iR, fR, objective_function
        
        all_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                            0, 0, 0, 0, 0, np.zeros((3,3))]
        max_mr, min_mr = 0, 0
        spot_ind = []
        mat = 0
        input_params["mat"] = 0
        case = "None"
        return all_stats, max_mr, min_mr, spot_ind, case, mat, np.zeros((3,3)), np.zeros((3,3)), 0, 0, objective_function

    @staticmethod
    def get_orient_mat(s_tth, s_chi, material0_, material1_, classhkl, class_predicted, predicted_hkl,
                       input_params, hkl_all_class0, hkl_all_class1, max_pred, dict_dp, spots, 
                       dist, Gstar_metric0, Gstar_metric1, B0, B1, softmax_threshold=0.85, mr_threshold=0.85, 
                       tab_distance_classhkl_data0=None, tab_distance_classhkl_data1=None, spots1_global=None,
                       coeff_overlap = None, ind_mat=None, ind_mat1=None, strain_calculation=None,cap_matchrate123=None,
                       material0_count=None, material1_count=None, material0_limit=None, material1_limit=None,
                       igrain=None, material_phase_always_present=None):
        init_mr = 0
        init_mat = 0
        init_material = "None"
        init_case = "None"
        init_B = None
        final_match_rate = 0
        match_rate_mma = []
        final_rmv_ind = []
        current_spots1 = [0 for igr in range(len(spots1_global))]
        mat = 0
        case = "None"
        all_stats = []
        
        for i in range(len(s_tth)):
            for j in range(i+1, len(s_tth)):
                overlap = False

                if (max_pred[j] < softmax_threshold) or (j in spots) or \
                    (max_pred[i] < softmax_threshold) or (i in spots):
                    continue
                
                if material0_ == material1_:
                    tab_distance_classhkl_data = tab_distance_classhkl_data0
                    hkl_all_class = hkl_all_class0
                    material_ = material0_
                    B = B0
                    Gstar_metric = Gstar_metric0
                    case = material_
                    mat = 1
                    input_params["mat"] = mat
                else:
                    if class_predicted[i] < ind_mat and class_predicted[j] < ind_mat:
                        tab_distance_classhkl_data = tab_distance_classhkl_data0
                        hkl_all_class = hkl_all_class0
                        material_ = material0_
                        B = B0
                        Gstar_metric = Gstar_metric0
                        case = material_
                        mat = 1
                        if igrain==0 and material_phase_always_present == 2:
                            mat = 0
                            case="None"
                        if material0_count >= material0_limit:
                            mat = 0
                            case="None"
                        input_params["mat"] = mat
                    elif (ind_mat <= class_predicted[i] < (ind_mat+ind_mat1)) and \
                                        (ind_mat <= class_predicted[j] < (ind_mat+ind_mat1)):
                        tab_distance_classhkl_data = tab_distance_classhkl_data1
                        hkl_all_class = hkl_all_class1
                        material_ = material1_
                        B = B1
                        Gstar_metric = Gstar_metric1
                        case = material_  
                        mat = 2
                        if igrain==0 and material_phase_always_present == 1:
                            mat = 0
                            case="None"
                        if material1_count >= material1_limit:
                            mat = 0
                            case="None"
                        input_params["mat"] = mat
                    else:
                        mat = 0
                        case = "None"
                        input_params["mat"] = mat
                        continue
                
                if mat == 0:
                    continue
                
                tth_chi_spot1 = np.array([s_tth[i], s_chi[i]])
                tth_chi_spot2 = np.array([s_tth[j], s_chi[j]])

                hkl1 = hkl_all_class[str(predicted_hkl[i])]
                hkl1_list = np.array(hkl1)
                hkl2 = hkl_all_class[str(predicted_hkl[j])]
                hkl2_list = np.array(hkl2)
                
                actual_mat, flagAM, \
                spot1_hkl, spot2_hkl = AnotherWindowLivePrediction.propose_UB_matrix(hkl1_list, hkl2_list, 
                                                                                   Gstar_metric, input_params, 
                                                                                   dist[i,j],
                                                                                   tth_chi_spot1, tth_chi_spot2, 
                                                                                   B, method=0)
                
                if flagAM:
                    continue
   
                for iind in range(len(actual_mat)): 
                    rot_mat123 = actual_mat[iind]

                    rmv_ind, theospots = AnotherWindowLivePrediction.remove_spots(s_tth, s_chi, rot_mat123, 
                                                                                    material_, input_params, 
                                                                                    dict_dp['detectorparameters'], dict_dp)
                    
                    overlap = False
                    current_spots = [len(list(set(rmv_ind) & set(spots1_global[igr]))) for igr in range(len(spots1_global))]
                    for igr in range(len(spots1_global)):
                        if current_spots[igr] > coeff_overlap*len(spots1_global[igr]):
                            overlap = True
                    
                    if overlap:
                        continue
        
                    match_rate = np.round(100 * len(rmv_ind)/theospots,3)
                    match_rate_mma.append(match_rate)
                    if match_rate > init_mr:
                        current_spots1 = current_spots                       
                        init_mat = np.copy(mat)
                        input_params["mat"] = init_mat
                        init_material = np.copy(material_)
                        init_case = np.copy(case)
                        init_B = np.copy(B)
                        final_rmv_ind = rmv_ind                            
                        final_match_rate = np.copy(match_rate)
                        init_mr = np.copy(match_rate)
                        all_stats = [i, j, \
                                     spot1_hkl[iind], spot2_hkl[iind], \
                                    tth_chi_spot1, tth_chi_spot2, \
                                    dist[i,j], tab_distance_classhkl_data[i,j], np.round(max_pred[i]*100,3), \
                                    np.round(max_pred[j]*100,3), len(rmv_ind), theospots,\
                                    match_rate, 0.0, rot_mat123]
        
                    if (final_match_rate >= mr_threshold*100.) and not overlap:
                        if strain_calculation:
                            dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(init_material), 
                                                                                 input_params, dict_dp['detectorparameters'], 
                                                                                 dict_dp, spots, init_B)
                        else:
                            dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                            rot_mat_UB = np.copy(all_stats[14])
                        
                        all_stats[14] = rot_mat_UB
                        return all_stats, np.max(match_rate_mma), np.min(match_rate_mma), \
                                final_rmv_ind, str(init_case), init_mat, dev_strain, strain_sample, iR, fR

        overlap = False
        for igr in range(len(spots1_global)):
            if current_spots1[igr] > coeff_overlap*len(spots1_global[igr]):
                overlap = True
                
        if (final_match_rate <= cap_matchrate123) or overlap: ## Nothing found!! 
            ## Either peaks are not well defined or not found within tolerance and prediction accuracy
            all_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                0, 0, 0, 0, 0, np.zeros((3,3))]
            max_mr, min_mr = 0, 0
            spot_ind = []
            mat = 0
            input_params["mat"] = 0
            case = "None"
            return all_stats, max_mr, min_mr, spot_ind, case, mat, np.zeros((3,3)), np.zeros((3,3)), 0, 0

        input_params["mat"] = init_mat
        if strain_calculation:
            dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(init_material), 
                                                                 input_params, dict_dp['detectorparameters'], 
                                                                 dict_dp, spots, init_B)
        else:
            dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
            rot_mat_UB = np.copy(all_stats[14])
        all_stats[14] = rot_mat_UB  
        return all_stats, np.max(match_rate_mma), np.min(match_rate_mma), \
                final_rmv_ind, str(init_case), init_mat, dev_strain, strain_sample, iR, fR
            
    @staticmethod
    def get_orient_mat_fastv0(s_tth, s_chi, material0_, material1_, classhkl, class_predicted, predicted_hkl,
                           input_params, hkl_all_class0, hkl_all_class1, max_pred, dict_dp, spots, 
                           dist, Gstar_metric0, Gstar_metric1, B0, B1, softmax_threshold=0.85, mr_threshold=0.85, 
                           tab_distance_classhkl_data0=None, tab_distance_classhkl_data1=None, spots1_global=None,
                           coeff_overlap = None, ind_mat=None, ind_mat1=None, strain_calculation=None, cap_matchrate123=None,
                           material0_count=None, material1_count=None, material0_limit=None, material1_limit=None,
                           igrain=None, material_phase_always_present=None):
        init_mr = 0
        init_mat = 0
        init_material = "None"
        init_case = "None"
        init_B = None
        final_match_rate = 0
        match_rate_mma = []
        final_rmv_ind = []
        current_spots1 = [0 for igr in range(len(spots1_global))]
        if material0_ != material1_:
            cond0 = np.abs(dist - tab_distance_classhkl_data0) <= input_params["tolerance"]
            cond1 = np.abs(dist - tab_distance_classhkl_data1) <= input_params["tolerance1"]
            cond = np.logical_or(cond0,cond1)
        else:
            cond = np.abs(dist - tab_distance_classhkl_data0) <= input_params["tolerance"]
        listarray = np.where(cond)
        mat = 0
        case = "None"
        tried_spots = []
        
        for i, j in zip(listarray[0], listarray[1]):
            overlap = False
            
            if (i in tried_spots) and (j in tried_spots):
                continue

            if (max_pred[i] < softmax_threshold) or (max_pred[j] < softmax_threshold) or \
                (i in spots) or (j in spots):
                continue
            
            if material0_ == material1_:
                tab_distance_classhkl_data = tab_distance_classhkl_data0
                hkl_all_class = hkl_all_class0
                material_ = material0_
                B = B0
                Gstar_metric = Gstar_metric0
                case = material_
                mat = 1
                input_params["mat"] = mat
            else:
                if class_predicted[i] < ind_mat and class_predicted[j] < ind_mat:
                    tab_distance_classhkl_data = tab_distance_classhkl_data0
                    hkl_all_class = hkl_all_class0
                    material_ = material0_
                    B = B0
                    Gstar_metric = Gstar_metric0
                    case = material_
                    mat = 1
                    if igrain==0 and material_phase_always_present !=1 and material_phase_always_present !=None:
                        mat = 0
                        case="None"
                    if material0_count >= material0_limit:
                        mat = 0
                        case="None"
                    input_params["mat"] = mat
                elif (ind_mat <= class_predicted[i] < (ind_mat+ind_mat1)) and \
                                    (ind_mat <= class_predicted[j] < (ind_mat+ind_mat1)):
                    tab_distance_classhkl_data = tab_distance_classhkl_data1
                    hkl_all_class = hkl_all_class1
                    material_ = material1_
                    B = B1
                    Gstar_metric = Gstar_metric1
                    case = material_  
                    mat = 2
                    if igrain==0 and material_phase_always_present !=2 and material_phase_always_present !=None:
                        mat = 0
                        case="None"
                    if material1_count >= material1_limit:
                        mat = 0
                        case="None"
                    input_params["mat"] = mat
                else:
                    mat = 0
                    case = "None"
                    input_params["mat"] = mat
            
            if mat == 0:
                continue
            
            tth_chi_spot1 = np.array([s_tth[i], s_chi[i]])
            tth_chi_spot2 = np.array([s_tth[j], s_chi[j]])         

            hkl1 = hkl_all_class[str(predicted_hkl[i])]
            hkl1_list = np.array(hkl1)
            hkl2 = hkl_all_class[str(predicted_hkl[j])]
            hkl2_list = np.array(hkl2)
            
            actual_mat, flagAM, \
            spot1_hkl, spot2_hkl = AnotherWindowLivePrediction.propose_UB_matrix(hkl1_list, hkl2_list, 
                                                                               Gstar_metric, input_params, 
                                                                               dist[i,j],
                                                                               tth_chi_spot1, tth_chi_spot2, 
                                                                               B, method=0)
            
            if flagAM:
                continue
  
            for iind in range(len(actual_mat)):
                rot_mat123 = actual_mat[iind]

                rmv_ind, theospots = AnotherWindowLivePrediction.remove_spots(s_tth, s_chi, rot_mat123, 
                                                        material_, input_params, 
                                                        dict_dp['detectorparameters'], dict_dp)
                
                overlap = False
                current_spots = [len(list(set(rmv_ind) & set(spots1_global[igr]))) for igr in range(len(spots1_global))]
                for igr in range(len(spots1_global)):
                    if current_spots[igr] > coeff_overlap*len(spots1_global[igr]):
                        overlap = True
                
                if overlap:
                    continue
             
                match_rate = np.round(100 * len(rmv_ind)/theospots, 3)
                
                match_rate_mma.append(match_rate)
                if match_rate > init_mr:
                    # print(i, j, match_rate)
                    final_rmv_ind = rmv_ind                    
                    current_spots1 = current_spots                      
                    init_mat = np.copy(mat)
                    input_params["mat"] = init_mat
                    init_material = np.copy(material_)
                    init_case = np.copy(case)
                    init_B = np.copy(B)                                     
                    final_match_rate = np.copy(match_rate)
                    init_mr = np.copy(match_rate)                   
                    all_stats = [i, j, \
                                 spot1_hkl[iind], spot2_hkl[iind], \
                                tth_chi_spot1, tth_chi_spot2, \
                                dist[i,j], tab_distance_classhkl_data[i,j], np.round(max_pred[i]*100,3), \
                                np.round(max_pred[j]*100,3), len(rmv_ind), theospots,\
                                match_rate, 0.0, rot_mat123]
    
                if (final_match_rate >= mr_threshold*100.) and not overlap:
                    if strain_calculation:
                        dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(init_material), 
                                                                             input_params, dict_dp['detectorparameters'], 
                                                                             dict_dp, spots, init_B)
                    else:
                        dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                        rot_mat_UB = np.copy(all_stats[14])
                    
                    all_stats[14] = rot_mat_UB
                    return all_stats, np.max(match_rate_mma), np.min(match_rate_mma), \
                            final_rmv_ind, str(init_case), init_mat, dev_strain, strain_sample, iR, fR
        
        overlap = False
        for igr in range(len(spots1_global)):
            if current_spots1[igr] > coeff_overlap*len(spots1_global[igr]):
                overlap = True

        if (final_match_rate <= cap_matchrate123) or overlap: ## Nothing found!! 
            ## Either peaks are not well defined or not found within tolerance and prediction accuracy
            all_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                0, 0, 0, 0, 0, np.zeros((3,3))]
            max_mr, min_mr = 0, 0
            spot_ind = []
            mat = 0
            input_params["mat"] = 0
            case = "None"
            return all_stats, max_mr, min_mr, spot_ind, case, mat, np.zeros((3,3)), np.zeros((3,3)), 0, 0

        input_params["mat"] = init_mat
        if strain_calculation:
            dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(init_material), 
                                                                 input_params, dict_dp['detectorparameters'], 
                                                                 dict_dp, spots, init_B)
        else:
            dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
            rot_mat_UB = np.copy(all_stats[14])
        all_stats[14] = rot_mat_UB     
        return all_stats, np.max(match_rate_mma), np.min(match_rate_mma), \
                final_rmv_ind, str(init_case), init_mat, dev_strain, strain_sample, iR, fR

    @staticmethod
    def get_orient_mat_fast(s_tth, s_chi, material0_, material1_, classhkl, class_predicted, predicted_hkl,
                           input_params, hkl_all_class0, hkl_all_class1, max_pred, dict_dp, spots, 
                           dist, Gstar_metric0, Gstar_metric1, B0, B1, softmax_threshold=0.85, mr_threshold=0.85, 
                           tab_distance_classhkl_data0=None, tab_distance_classhkl_data1=None, spots1_global=None,
                           coeff_overlap = None, ind_mat=None, ind_mat1=None, strain_calculation=None, cap_matchrate123=None,
                           material0_count=None, material1_count=None, material0_limit=None, material1_limit=None,
                           igrain=None, material_phase_always_present=None):
        init_mat = 0
        init_case = "None"
        match_rate_mma = []
        final_rmv_ind = []
        list_of_sets = []
        all_list = []
        spot_link = [[] for i in range(len(dist))]
        spot_link_tol = [[] for i in range(len(dist))]

        if material0_ == material1_:
            list_of_sets = []
            for ii in range(len(dist)):
                if max_pred[ii] < softmax_threshold:
                    continue 
                a1 = np.round(dist[ii],3)
                a2 = np.round(tab_distance_classhkl_data0[ii],3)
                for i in range(len(dist)):
                    if max_pred[i] < softmax_threshold:
                        continue
                    if np.abs(a1[i] - a2[i]) <= input_params["tolerance"]:
                        list_of_sets.append((ii,i))
                        all_list.append(ii)
                        all_list.append(i)
                        spot_link[ii].append(i)
                        spot_link[i].append(ii)
                        spot_link_tol[ii].append(np.abs(a1[i] - a2[i]))
                        spot_link_tol[i].append(np.abs(a1[i] - a2[i])) 
        else:
            list_of_sets = []
            for ii in range(len(dist)):
                if max_pred[ii] < softmax_threshold:
                    continue 
                for i in range(len(dist)):
                    if max_pred[i] < softmax_threshold:
                        continue
                    if class_predicted[ii] < ind_mat and class_predicted[i] < ind_mat:
                        tab_distance_classhkl_data = tab_distance_classhkl_data0
                        tolerance_new = input_params["tolerance"]
                    elif (ind_mat <= class_predicted[ii] < (ind_mat+ind_mat1)) and \
                                        (ind_mat <= class_predicted[i] < (ind_mat+ind_mat1)):
                        tab_distance_classhkl_data = tab_distance_classhkl_data1
                        tolerance_new = input_params["tolerance1"]
                    else:
                        continue
                    a1 = np.round(dist[ii],3)
                    a2 = np.round(tab_distance_classhkl_data[ii],3)
                    if np.abs(a1[i] - a2[i]) <= tolerance_new:
                        list_of_sets.append((ii,i))
                        all_list.append(ii)
                        all_list.append(i)
                        spot_link[ii].append(i)
                        spot_link[i].append(ii)
                        spot_link_tol[ii].append(np.abs(a1[i] - a2[i]))
                        spot_link_tol[i].append(np.abs(a1[i] - a2[i])) 

        most_common = collections.Counter(all_list).most_common()
        
        mat = 0
        case = "None"
        tried_spots = []       
        
        ## find the match with minimum deviation
        #TODO verify again
        # sort_list = []
        # for ijij in range(len(spot_link_tol)):
        #     if len(np.unique(spot_link_tol[ijij]))>3:
        #         sort_list.append(np.average(np.unique(spot_link_tol[ijij])))
        #     else:
        #         sort_list.append(100)
        
        for toplist in range(len(most_common)):

            if most_common[toplist][1] < 2:
                continue            
            # taken the most common node from each connection
            j = most_common[toplist][0]
            
        # for j in np.argsort(sort_list):
        #     if sort_list[j] ==100:
        #         continue
            
            if (j in spots) or (max_pred[j] < softmax_threshold):
                continue
            
            for i in np.unique(spot_link[j]):
                if j == i or np.all(predicted_hkl[j] == predicted_hkl[i]) or\
                    (max_pred[i] < softmax_threshold) or (i in spots):
                    continue
                if (i in tried_spots) and (j in tried_spots):
                    continue
    
                if material0_ == material1_:
                    tab_distance_classhkl_data = tab_distance_classhkl_data0
                    hkl_all_class = hkl_all_class0
                    material_ = material0_
                    B = B0
                    Gstar_metric = Gstar_metric0
                    case = material_
                    mat = 1
                    input_params["mat"] = mat
                else:
                    if class_predicted[i] < ind_mat and class_predicted[j] < ind_mat:
                        tab_distance_classhkl_data = tab_distance_classhkl_data0
                        hkl_all_class = hkl_all_class0
                        material_ = material0_
                        B = B0
                        Gstar_metric = Gstar_metric0
                        case = material_
                        mat = 1
                        input_params["mat"] = mat
                    elif (ind_mat <= class_predicted[i] < (ind_mat+ind_mat1)) and \
                                        (ind_mat <= class_predicted[j] < (ind_mat+ind_mat1)):
                        tab_distance_classhkl_data = tab_distance_classhkl_data1
                        hkl_all_class = hkl_all_class1
                        material_ = material1_
                        B = B1
                        Gstar_metric = Gstar_metric1
                        case = material_  
                        mat = 2
                        input_params["mat"] = mat
                    else:
                        mat = 0
                        case = "None"
                        input_params["mat"] = mat
                
                tried_spots.append(i)
                tried_spots.append(j)
                
                if mat == 1:
                    if igrain==0 and material_phase_always_present ==2:
                        mat = 0
                        case="None"
                    if material0_count >= material0_limit:
                        mat = 0
                        case="None"
                elif mat == 2:
                    if igrain==0 and material_phase_always_present ==1:
                        mat = 0
                        case="None"
                    if material1_count >= material1_limit:
                        mat = 0
                        case="None"
                        
                if mat == 0:
                    continue
    
                tth_chi_spot1 = np.array([s_tth[i], s_chi[i]])
                tth_chi_spot2 = np.array([s_tth[j], s_chi[j]])         
                
                hkl1 = hkl_all_class[str(predicted_hkl[i])]
                hkl1_list = np.array(hkl1)
                hkl2 = hkl_all_class[str(predicted_hkl[j])]
                hkl2_list = np.array(hkl2)
                
                actual_mat, flagAM, \
                spot1_hkl, spot2_hkl = AnotherWindowLivePrediction.propose_UB_matrix(hkl1_list, hkl2_list, 
                                                                                   Gstar_metric, input_params, 
                                                                                   dist[i,j],
                                                                                   tth_chi_spot1, tth_chi_spot2, 
                                                                                   B, method=0)                
                if flagAM:
                    continue
                
                all_stats, max_mr_mma, min_mr_mma, \
                        final_rmv_ind, init_case, \
                            init_mat, dev_strain, strain_sample,\
                                iR, fR = AnotherWindowLivePrediction.getfastmatrix(i, j, hkl1_list, hkl2_list, tth_chi_spot1, tth_chi_spot2, B,
                                              s_tth, s_chi, material_, input_params, dict_dp, spots1_global,
                                              match_rate_mma, mat, case, dist, tab_distance_classhkl_data,
                                              max_pred, mr_threshold, strain_calculation, coeff_overlap, spots, cap_matchrate123,
                                              actual_mat, spot1_hkl, spot2_hkl)
                                
                if len(final_rmv_ind) == 0:
                    continue
    
                return all_stats, max_mr_mma, min_mr_mma, final_rmv_ind, init_case, \
                            init_mat, dev_strain, strain_sample, iR, fR
        ## after exhausting all the nodes, just return empty as nothing could be found
        all_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                0, 0, 0, 0, 0, np.zeros((3,3))]
        max_mr, min_mr = 0, 0
        spot_ind = []
        mat = 0
        case = "None"
        return all_stats, max_mr, min_mr, spot_ind, case, mat, np.zeros((3,3)), np.zeros((3,3)), 0, 0
            
    @staticmethod
    def getfastmatrix(i, j, hkl1_list, hkl2_list, tth_chi_spot1, tth_chi_spot2, B,
                      s_tth, s_chi, material_, input_params, dict_dp, spots1_global,
                      match_rate_mma, mat, case, dist, tab_distance_classhkl_data,
                      max_pred, mr_threshold, strain_calculation, coeff_overlap, spots, cap_matchrate123,
                      actual_mat, spot1_hkl, spot2_hkl):
        current_spots1 = [0 for igr in range(len(spots1_global))]
        init_mr = 0
        final_rmv_ind = []
        final_match_rate = 0

        for iind in range(len(actual_mat)):  
            rot_mat123 = actual_mat[iind]
            rmv_ind, theospots = AnotherWindowLivePrediction.remove_spots(s_tth, s_chi, rot_mat123, 
                                                    material_, input_params, 
                                                    dict_dp['detectorparameters'], dict_dp)            
            overlap = False
            current_spots = [len(list(set(rmv_ind) & set(spots1_global[igr]))) for igr in range(len(spots1_global))]
            for igr in range(len(spots1_global)):
                if current_spots[igr] > coeff_overlap*len(spots1_global[igr]):
                    overlap = True
            
            if overlap:
                continue
            
            match_rate = np.round(100 * len(rmv_ind)/theospots, 3)
            match_rate_mma.append(match_rate)
            
            # TODO verify and remove
            # tm1 = 0
            # tm2 = 1
            # if match_rate == init_mr:
            #     temp_mat = np.matmul(rot_mat123, B)
            #     tm1, tm2 = np.argmin(np.abs(temp_mat[:,:2]), axis=0)
            # if tm1 != 0 or tm2!= 1:
            #     continue
            
            if match_rate > init_mr:
                final_rmv_ind = rmv_ind                    
                current_spots1 = current_spots                      
                init_mat = np.copy(mat)
                input_params["mat"] = init_mat
                init_material = np.copy(material_)
                init_case = np.copy(case)
                init_B = np.copy(B)                                     
                final_match_rate = np.copy(match_rate)
                init_mr = np.copy(match_rate)   
                all_stats = [i, j, \
                             spot1_hkl[iind], spot2_hkl[iind], \
                            tth_chi_spot1, tth_chi_spot2, \
                            dist[i,j], tab_distance_classhkl_data[i,j], np.round(max_pred[i]*100,3), \
                            np.round(max_pred[j]*100,3), len(rmv_ind), theospots,\
                            match_rate, 0.0, rot_mat123]

            if (final_match_rate >= mr_threshold*100.) and not overlap:
                if strain_calculation:
                    dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(init_material), 
                                                                         input_params, dict_dp['detectorparameters'], 
                                                                         dict_dp, spots, init_B)
                else:
                    dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
                    rot_mat_UB = np.copy(all_stats[14])
                
                all_stats[14] = rot_mat_UB
                return all_stats, np.max(match_rate_mma), np.min(match_rate_mma), \
                        final_rmv_ind, str(init_case), init_mat, dev_strain, strain_sample, iR, fR
    
        overlap = False
        for igr in range(len(spots1_global)):
            if current_spots1[igr] > coeff_overlap*len(spots1_global[igr]):
                overlap = True
    
        if (final_match_rate <= cap_matchrate123) or overlap: ## Nothing found!! 
            ## Either peaks are not well defined or not found within tolerance and prediction accuracy
            all_stats = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                                0, 0, 0, 0, 0, np.zeros((3,3))]
            max_mr, min_mr = 0, 0
            spot_ind = []
            mat = 0
            input_params["mat"] = 0
            case = "None"
            return all_stats, max_mr, min_mr, spot_ind, case, mat, np.zeros((3,3)), np.zeros((3,3)), 0, 0

        input_params["mat"] = init_mat
        if strain_calculation:
            dev_strain, strain_sample, iR, fR, rot_mat_UB = AnotherWindowLivePrediction.calculate_strains_fromUB(s_tth, s_chi, all_stats[14], str(init_material), 
                                                                 input_params, dict_dp['detectorparameters'], 
                                                                 dict_dp, spots, init_B)
        else:
            dev_strain, strain_sample, iR, fR = np.zeros((3,3)), np.zeros((3,3)), 0, 0
            rot_mat_UB = np.copy(all_stats[14])
        all_stats[14] = rot_mat_UB     
        return all_stats, np.max(match_rate_mma), np.min(match_rate_mma), \
                final_rmv_ind, str(init_case), init_mat, dev_strain, strain_sample, iR, fR

    @staticmethod
    def propose_UB_matrix(hkl1_list, hkl2_list, Gstar_metric, input_params, dist123,
                          tth_chi_spot1, tth_chi_spot2, B, method=0):
        
        if method == 1:
            tab_angulardist_temp = CP.AngleBetweenNormals(hkl1_list, hkl2_list, Gstar_metric)
            
            if input_params["mat"] == 1:
                list_ = np.where(np.abs(tab_angulardist_temp-dist123) < input_params["tolerance"])
            elif input_params["mat"] == 2:
                list_ = np.where(np.abs(tab_angulardist_temp-dist123) < input_params["tolerance1"])
            
            if len(list_[0]) == 0:
                return None, True, 0, 0
    
            rot_mat_abs = []
            actual_mat = []
            spot1_hkl = []
            spot2_hkl = []
            
            triedspots = []
            for ii, jj in zip(list_[0], list_[1]):
                if ii in triedspots and jj in triedspots:
                    continue
    
                conti_ = False
                
                try:
                    rot_mat1 = FindO.OrientMatrix_from_2hkl(hkl1_list[ii], tth_chi_spot1, \
                                                            hkl2_list[jj], tth_chi_spot2,
                                                            B)
                except:
                    continue                    
                
                copy_rm = np.copy(rot_mat1)
                copy_rm = np.round(np.abs(copy_rm),5)
                copy_rm.sort(axis=1)
                for iji in rot_mat_abs:
                    iji.sort(axis=1)                        
                    if np.all(iji==copy_rm):
                        conti_ = True
                        break
                if conti_:
                    continue
                rot_mat_abs.append(np.round(np.abs(rot_mat1),5))
                actual_mat.append(rot_mat1)
                spot1_hkl.append(hkl1_list[ii])
                spot2_hkl.append(hkl2_list[jj])
                triedspots.append(ii)
                triedspots.append(jj)
        else:  
            # method 2
            hkl_all = np.vstack((hkl1_list, hkl2_list))
            LUT = FindO.GenerateLookUpTable(hkl_all, Gstar_metric)
            if input_params["mat"] == 1:
                hkls = FindO.PlanePairs_2(dist123, input_params["tolerance"], LUT, onlyclosest=1)
            elif input_params["mat"] == 2:
                hkls = FindO.PlanePairs_2(dist123, input_params["tolerance1"], LUT, onlyclosest=1)            
             
            if np.all(hkls == None):
                return None, True, 0, 0
                    
            rot_mat_abs = []
            actual_mat = []
            spot1_hkl = []
            spot2_hkl = []
            
            for ii in range(len(hkls)):
                if np.all(hkls[ii][0] == hkls[ii][1]):
                    continue
                conti_ = False
                
                try:
                    rot_mat1 = FindO.OrientMatrix_from_2hkl(hkls[ii][0], tth_chi_spot1, \
                                                            hkls[ii][1], tth_chi_spot2,
                                                            B)
                except:
                    continue                    
                
                copy_rm = np.copy(rot_mat1)
                copy_rm = np.round(np.abs(copy_rm),5)
                copy_rm.sort(axis=1)
                for iji in rot_mat_abs:
                    iji.sort(axis=1)
                    if np.all(iji==copy_rm):
                        conti_ = True
                        break

                if conti_:
                    continue
                rot_mat_abs.append(np.round(np.abs(rot_mat1),5))
                actual_mat.append(rot_mat1)
                spot1_hkl.append(hkls[ii][0])
                spot2_hkl.append(hkls[ii][1])
                
        #TODO align orientation matrix to the a* vector
        sum_sign = []
        for nkl in range(len(spot1_hkl)):
            sum_sign.append(sum(np.sign(spot1_hkl[nkl])) + sum(np.sign(spot2_hkl[nkl])) + \
                            len(np.where(spot1_hkl[nkl]==0)[0]) + len(np.where(spot2_hkl[nkl]==0)[0]))
        ind_sort = np.argsort(sum_sign)[::-1]
        ## rearrange
        actual_mat1 = []
        spot1_hkl1, spot2_hkl1 = [], []
        for inin in ind_sort:
            conti_ = False
            for act_mat_iji in actual_mat1:
                r_oa_t = np.transpose(act_mat_iji)
                r_ab = np.matmul(r_oa_t, actual_mat[inin])
                if np.isnan(np.rad2deg(np.arccos((np.trace(r_ab) - 1) / 2))) or \
                    np.rad2deg(np.arccos((np.trace(r_ab) - 1) / 2)) < 0.5:
                    conti_ = True
            if conti_:
                continue
            
            actual_mat1.append(actual_mat[inin])
            spot1_hkl1.append(spot1_hkl[inin])
            spot2_hkl1.append(spot2_hkl[inin])
        actual_mat, spot1_hkl, spot2_hkl = actual_mat1, spot1_hkl1, spot2_hkl1
        
        return actual_mat, False, spot1_hkl, spot2_hkl
    
    @staticmethod
    def remove_spots(s_tth, s_chi, first_match123, material_, input_params, detectorparameters, dict_dp):
        #### Spots in first match (no refining, just simple auto links to filter spots)
        try:
            grain = CP.Prepare_Grain(material_, first_match123, dictmaterials=dictLT.dict_Materials)
        except:
            return [], 100

        #### Perhaps better than SimulateResult function
        kf_direction = dict_dp["kf_direction"]
        detectordistance = dict_dp["detectorparameters"][0]
        detectordiameter = dict_dp["detectordiameter"]
        pixelsize = dict_dp["pixelsize"]
        dim = dict_dp["dim"]
               
        spots2pi = LT.getLaueSpots(CST_ENERGYKEV / input_params["emax"], CST_ENERGYKEV / input_params["emin"],
                                        [grain],
                                        fastcompute=1,
                                        verbose=0,
                                        kf_direction=kf_direction,
                                        ResolutionAngstrom=False,
                                        dictmaterials=dictLT.dict_Materials)

        TwicethetaChi = LT.filterLaueSpots_full_np(spots2pi[0][0], None, onlyXYZ=False,
                                                        HarmonicsRemoval=0,
                                                        fastcompute=1,
                                                        kf_direction=kf_direction,
                                                        detectordistance=detectordistance,
                                                        detectordiameter=detectordiameter,
                                                        pixelsize=pixelsize,
                                                        dim=dim)
        ## get proximity for exp and theo spots
        if input_params["mat"] == 1:
            angtol = input_params["tolerance"]
        elif input_params["mat"] == 2:
            angtol = input_params["tolerance1"]
        else:
            angtol=0
        List_Exp_spot_close, residues_link = AnotherWindowLivePrediction.getProximityv1(np.array([TwicethetaChi[0], TwicethetaChi[1]]),  # warning array(2theta, chi)
                                                  s_tth/2.0, s_chi,  # warning theta, chi for exp
                                                  angtol=angtol)
        
        return List_Exp_spot_close, len(TwicethetaChi[0])
    
    @staticmethod
    def getProximityv1_ambigious(TwicethetaChi, data_theta, data_chi, angtol=0.5):
        # theo simul data
        theodata = np.array([TwicethetaChi[0] / 2.0, TwicethetaChi[1]]).T
        # exp data
        sorted_data = np.array([data_theta, data_chi]).T
        table_dist = GT.calculdist_from_thetachi(sorted_data, theodata)
        prox_table = np.argmin(table_dist, axis=1)
        allresidues = np.amin(table_dist, axis=1)
        very_close_ind = np.where(allresidues < angtol)[0]
        List_Exp_spot_close = []
        if len(very_close_ind) > 0:
            for theospot_ind in very_close_ind:  # loop over theo spots index
                List_Exp_spot_close.append(prox_table[theospot_ind])
        return List_Exp_spot_close, allresidues[very_close_ind]
    
    @staticmethod
    def getProximityv1( TwicethetaChi, data_theta, data_chi, angtol=0.5):
        theodata = np.array([TwicethetaChi[0] / 2.0, TwicethetaChi[1]]).T
        # exp data
        sorted_data = np.array([data_theta, data_chi]).T
        table_dist = GT.calculdist_from_thetachi(sorted_data, theodata)
    
        prox_table = np.argmin(table_dist, axis=1)
        allresidues = np.amin(table_dist, axis=1)
        very_close_ind = np.where(allresidues < angtol)[0]
        List_Exp_spot_close = []
        Miller_Exp_spot = []
        if len(very_close_ind) > 0:
            for theospot_ind in very_close_ind:  # loop over theo spots index
                List_Exp_spot_close.append(prox_table[theospot_ind])
                Miller_Exp_spot.append(1)
        else:
            return [], []
        # removing exp spot which appears many times(close to several simulated spots of one grain)--------------
        arrayLESC = np.array(List_Exp_spot_close, dtype=float)
        sorted_LESC = np.sort(arrayLESC)
        diff_index = sorted_LESC - np.array(list(sorted_LESC[1:]) + [sorted_LESC[0]])
        toremoveindex = np.where(diff_index == 0)[0]
        if len(toremoveindex) > 0:
            # index of exp spot in arrayLESC that are duplicated
            ambiguous_exp_ind = GT.find_closest(np.array(sorted_LESC[toremoveindex], dtype=float), arrayLESC, 0.1)[1]
            for ind in ambiguous_exp_ind:
                Miller_Exp_spot[ind] = None
        
        ProxTablecopy = np.copy(prox_table)
    
        for theo_ind, exp_ind in enumerate(prox_table):
            where_th_ind = np.where(ProxTablecopy == exp_ind)[0]
            if len(where_th_ind) > 1:
                for indy in where_th_ind:
                    ProxTablecopy[indy] = -prox_table[indy]
                closest = np.argmin(allresidues[where_th_ind])
                ProxTablecopy[where_th_ind[closest]] = -ProxTablecopy[where_th_ind[closest]]
        
        singleindices = []
        refine_indexed_spots = {}
        # loop over close exp. spots
        for k in range(len(List_Exp_spot_close)):
            exp_index = List_Exp_spot_close[k]
            if not singleindices.count(exp_index):
                singleindices.append(exp_index)
                theo_index = np.where(ProxTablecopy == exp_index)[0]
                if (len(theo_index) == 1):  # only one theo spot close to the current exp. spot
                    refine_indexed_spots[exp_index] = [exp_index, theo_index, Miller_Exp_spot[k]]
                else:  # recent PATCH:
                    closest_theo_ind = np.argmin(allresidues[theo_index])
                    if allresidues[theo_index][closest_theo_ind] < angtol:
                        refine_indexed_spots[exp_index] = [exp_index, theo_index[closest_theo_ind], Miller_Exp_spot[k]]       
        listofpairs = []
        linkResidues = []        
        selectedAbsoluteSpotIndices = np.arange(len(data_theta))
        for val in list(refine_indexed_spots.values()):
            if val[2] is not None:
                localspotindex = val[0]
                if not isinstance(val[1], (list, np.ndarray)):
                    closetheoindex = val[1]
                else:
                    closetheoindex = val[1][0]
                absolute_spot_index = selectedAbsoluteSpotIndices[localspotindex]
                listofpairs.append(absolute_spot_index)  # Exp, Theo,  where -1 for specifying that it came from automatic linking
                linkResidues.append(allresidues[closetheoindex])

        return listofpairs, linkResidues

    @staticmethod
    def calculate_strains_fromUB(s_tth, s_chi, UBmat, material_, input_params, 
                                 detectorparameters, dict_dp, spots, B_matrix):
        # starting B0matrix corresponding to the unit cell   -----
        B0matrix = np.copy(B_matrix)
        latticeparams = dictLT.dict_Materials[material_][1]
        # initial_orientmatrix = np.copy(UBmat)
        ## Included simple multi level refinement of strains
        init_residues = -0.1
        final_residues = -0.1
        
        if input_params["mat"] == 1:
            straintolerance = input_params["tolerancestrain"]
        elif input_params["mat"] == 2:
            straintolerance = input_params["tolerancestrain1"]
        
        devstrain, deviatoricstrain_sampleframe = np.zeros((3,3)), np.zeros((3,3))
        for ijk, AngTol in enumerate(straintolerance):
            #### Spots in first match (no refining, just simple auto links to filter spots)        
            grain = CP.Prepare_Grain(material_, UBmat, dictmaterials=dictLT.dict_Materials)
            Twicetheta, Chi, Miller_ind, posx, posy, _ = LT.SimulateLaue(grain,
                                                                     input_params["emin"], 
                                                                     input_params["emax"], 
                                                                     detectorparameters,
                                                                     kf_direction=dict_dp['kf_direction'],
                                                                     removeharmonics=1,
                                                                     pixelsize=dict_dp['pixelsize'],
                                                                     dim=dict_dp['dim'],
                                                                     ResolutionAngstrom=False,
                                                                     detectordiameter=dict_dp['detectordiameter'],
                                                                     dictmaterials=dictLT.dict_Materials)
            ## get proximity for exp and theo spots
            linkedspots_link, linkExpMiller_link, \
                linkResidues_link = AnotherWindowLivePrediction.getProximityv0(np.array([Twicetheta, Chi]),  # warning array(2theta, chi)
                                                                                    s_tth/2.0, s_chi, Miller_ind,  # warning theta, chi for exp
                                                                                    angtol=float(AngTol))
            
            if len(linkedspots_link) < 8:
                return np.zeros((3,3)), np.zeros((3,3)), init_residues, final_residues, UBmat
            
            linkedspots_fit = linkedspots_link
            linkExpMiller_fit = linkExpMiller_link
            
            arraycouples = np.array(linkedspots_fit)
            exp_indices = np.array(arraycouples[:, 0], dtype=np.int)
            sim_indices = np.array(arraycouples[:, 1], dtype=np.int)
        
            nb_pairs = len(exp_indices)
            Data_Q = np.array(linkExpMiller_fit)[:, 1:]
            sim_indices = np.arange(nb_pairs)  # for fitting function this must be an arange...
        
            pixX = np.take(dict_dp['peakX'], exp_indices)
            pixY = np.take(dict_dp['peakY'], exp_indices)
            weights = None #np.take(dict_dp['intensity'], exp_indices)
            
            starting_orientmatrix = np.copy(UBmat)
        
            results = None
            # ----------------------------------
            #  refinement model
            # ----------------------------------
            # -------------------------------------------------------
            allparameters = np.array(detectorparameters + [1, 1, 0, 0, 0] + [0, 0, 0])
            # strain & orient
            initial_values = np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0])
            arr_indexvaryingparameters = np.arange(5, 13)
        
            residues, deltamat, newmatrix = FitO.error_function_on_demand_strain(
                                                                                initial_values,
                                                                                Data_Q,
                                                                                allparameters,
                                                                                arr_indexvaryingparameters,
                                                                                sim_indices,
                                                                                pixX,
                                                                                pixY,
                                                                                initrot=starting_orientmatrix,
                                                                                Bmat=B0matrix,
                                                                                pureRotation=0,
                                                                                verbose=1,
                                                                                pixelsize=dict_dp['pixelsize'],
                                                                                dim=dict_dp['dim'],
                                                                                weights=weights,
                                                                                kf_direction=dict_dp['kf_direction'])
            init_mean_residues = np.copy(np.mean(residues))
            
            if ijk == 0:
                init_residues = np.copy(init_mean_residues)
            
            results = FitO.fit_on_demand_strain(initial_values,
                                                    Data_Q,
                                                    allparameters,
                                                    FitO.error_function_on_demand_strain,
                                                    arr_indexvaryingparameters,
                                                    sim_indices,
                                                    pixX,
                                                    pixY,
                                                    initrot=starting_orientmatrix,
                                                    Bmat=B0matrix,
                                                    pixelsize=dict_dp['pixelsize'],
                                                    dim=dict_dp['dim'],
                                                    verbose=0,
                                                    weights=weights,
                                                    kf_direction=dict_dp['kf_direction'])
        
            if results is None:
                return np.zeros((3,3)), np.zeros((3,3)), init_residues, final_residues, UBmat
        
            residues, deltamat, newmatrix = FitO.error_function_on_demand_strain(
                                                                                results,
                                                                                Data_Q,
                                                                                allparameters,
                                                                                arr_indexvaryingparameters,
                                                                                sim_indices,
                                                                                pixX,
                                                                                pixY,
                                                                                initrot=starting_orientmatrix,
                                                                                Bmat=B0matrix,
                                                                                pureRotation=0,
                                                                                verbose=1,
                                                                                pixelsize=dict_dp['pixelsize'],
                                                                                dim=dict_dp['dim'],
                                                                                weights=weights,
                                                                                kf_direction=dict_dp['kf_direction'])
            # if np.mean(residues) > final_residues:
            #     return devstrain, deviatoricstrain_sampleframe, init_residues, final_residues, UBmat
            final_mean_residues = np.copy(np.mean(residues))
            final_residues = np.copy(final_mean_residues)
            # building B mat
            # param_strain_sol = results
            # varyingstrain = np.array([[1.0, param_strain_sol[2], param_strain_sol[3]],
            #                                 [0, param_strain_sol[0], param_strain_sol[4]],
            #                                 [0, 0, param_strain_sol[1]]])
            # newUmat = np.dot(deltamat, starting_orientmatrix)
            # newUBmat = np.dot(newUmat, varyingstrain)
            newUBmat = np.copy(newmatrix) 
            # Bstar_s = np.dot(newUBmat, B0matrix)
            # ---------------------------------------------------------------
            # postprocessing of unit cell orientation and strain refinement
            # ---------------------------------------------------------------
            UBmat = np.copy(newmatrix) 
            (devstrain, lattice_parameter_direct_strain) = CP.compute_deviatoricstrain(newUBmat, B0matrix, latticeparams)
            # overwrite and rescale possibly lattice lengthes
            # constantlength = "a"
            # lattice_parameter_direct_strain = CP.computeLatticeParameters_from_UB(newUBmat, material_, constantlength, dictmaterials=dictLT.dict_Materials)
            # print(lattice_parameter_direct_strain)
            deviatoricstrain_sampleframe = CP.strain_from_crystal_to_sample_frame2(devstrain, newUBmat)
            devstrain = np.round(devstrain * 1000, decimals=3)
            deviatoricstrain_sampleframe = np.round(deviatoricstrain_sampleframe * 1000, decimals=3)
        return devstrain, deviatoricstrain_sampleframe, init_residues, final_residues, UBmat #initial_orientmatrix #UBmat
    
    @staticmethod
    def getProximityv0(TwicethetaChi, data_theta, data_chi, data_hkl, angtol=0.5):
        # theo simul data
        theodata = np.array([TwicethetaChi[0] / 2.0, TwicethetaChi[1]]).T
        # exp data
        sorted_data = np.array([data_theta, data_chi]).T
        table_dist = GT.calculdist_from_thetachi(sorted_data, theodata)
    
        prox_table = np.argmin(table_dist, axis=1)
        allresidues = np.amin(table_dist, axis=1)
        very_close_ind = np.where(allresidues < angtol)[0]
        List_Exp_spot_close = []
        Miller_Exp_spot = []
        if len(very_close_ind) > 0:
            for theospot_ind in very_close_ind:  # loop over theo spots index
                List_Exp_spot_close.append(prox_table[theospot_ind])
                Miller_Exp_spot.append(data_hkl[theospot_ind])
        else:
            return [],[],[]
        # removing exp spot which appears many times(close to several simulated spots of one grain)--------------
        arrayLESC = np.array(List_Exp_spot_close, dtype=float)
        sorted_LESC = np.sort(arrayLESC)
        diff_index = sorted_LESC - np.array(list(sorted_LESC[1:]) + [sorted_LESC[0]])
        toremoveindex = np.where(diff_index == 0)[0]
        if len(toremoveindex) > 0:
            # index of exp spot in arrayLESC that are duplicated
            ambiguous_exp_ind = GT.find_closest(np.array(sorted_LESC[toremoveindex], dtype=float), arrayLESC, 0.1)[1]
            for ind in ambiguous_exp_ind:
                Miller_Exp_spot[ind] = None
        
        ProxTablecopy = np.copy(prox_table)
    
        for theo_ind, exp_ind in enumerate(prox_table):
            where_th_ind = np.where(ProxTablecopy == exp_ind)[0]
            if len(where_th_ind) > 1:
                for indy in where_th_ind:
                    ProxTablecopy[indy] = -prox_table[indy]
                closest = np.argmin(allresidues[where_th_ind])
                ProxTablecopy[where_th_ind[closest]] = -ProxTablecopy[where_th_ind[closest]]
        
        singleindices = []
        refine_indexed_spots = {}
        # loop over close exp. spots
        for k in range(len(List_Exp_spot_close)):
            exp_index = List_Exp_spot_close[k]
            if not singleindices.count(exp_index):
                singleindices.append(exp_index)
                theo_index = np.where(ProxTablecopy == exp_index)[0]
                if (len(theo_index) == 1):  # only one theo spot close to the current exp. spot
                    refine_indexed_spots[exp_index] = [exp_index, theo_index, Miller_Exp_spot[k]]
                else:  # recent PATCH:
                    closest_theo_ind = np.argmin(allresidues[theo_index])
                    if allresidues[theo_index][closest_theo_ind] < angtol:
                        refine_indexed_spots[exp_index] = [exp_index, theo_index[closest_theo_ind], Miller_Exp_spot[k]]
        
        listofpairs = []
        linkExpMiller = []
        linkResidues = []
        
        selectedAbsoluteSpotIndices = np.arange(len(data_theta))
        for val in list(refine_indexed_spots.values()):
            if val[2] is not None:
                localspotindex = val[0]
                if not isinstance(val[1], (list, np.ndarray)):
                    closetheoindex = val[1]
                else:
                    closetheoindex = val[1][0]
                absolute_spot_index = selectedAbsoluteSpotIndices[localspotindex]
                listofpairs.append([absolute_spot_index, closetheoindex])  # Exp, Theo,  where -1 for specifying that it came from automatic linking
                linkExpMiller.append([float(absolute_spot_index)] + [float(elem) for elem in val[2]])  # float(val) for further handling as floats array
                linkResidues.append([absolute_spot_index, closetheoindex, allresidues[closetheoindex]])
    
        linkedspots_link = np.array(listofpairs)
        linkExpMiller_link = linkExpMiller
        linkResidues_link = linkResidues
        return linkedspots_link, linkExpMiller_link, linkResidues_link
    
    @staticmethod
    def get_ipf_colour(orientation_matrix1, axis=np.array([0., 0., 1.]), symmetry=None, saturate=True):
        """Compute the IPF (inverse pole figure) colour for this orientation.
        Given a particular axis expressed in the laboratory coordinate system,
        one can compute the so called IPF colour based on that direction
        expressed in the crystal coordinate system as :math:`[x_c,y_c,z_c]`.
        There is only one tuple (u,v,w) such that:
        .. math::
          [x_c,y_c,z_c]=u.[0,0,1]+v.[0,1,1]+w.[1,1,1]
        and it is used to assign the RGB colour.
        :param ndarray axis: the direction to use to compute the IPF colour.
        :param Symmetry symmetry: the symmetry operator to use.
        :return tuple: a tuple contining the RGB values.
        """
        if not np.all(orientation_matrix1==0):
            orientation_matrix = orientation_matrix1
        else:
            return 0,0,0
        # ## rotate orientation by 40degrees to bring in Sample RF
        omega = np.deg2rad(-40.0)
        # rotation de -omega autour de l'axe x (or Y?) pour repasser dans Rsample
        cw = np.cos(omega)
        sw = np.sin(omega)
        mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]])
        orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
        if np.linalg.det(orientation_matrix) < 0:
            orientation_matrix = -orientation_matrix
        axis /= np.linalg.norm(axis)
        Vc = np.dot(orientation_matrix, axis)
        # get the symmetry operators
        syms = symmetry.symmetry_operators()
        syms = np.concatenate((syms, -syms))
        Vc_syms = np.dot(syms, Vc)
        # phi: rotation around 001 axis, from 100 axis to Vc vector, projected on (100,010) plane
        Vc_phi = np.arctan2(Vc_syms[:, 1], Vc_syms[:, 0]) * 180 / np.pi
        # chi: rotation around 010 axis, from 001 axis to Vc vector, projected on (100,001) plane
        # Vc_chi = np.arctan2(Vc_syms[:, 0], Vc_syms[:, 2]) * 180 / np.pi
        # psi : angle from 001 axis to Vc vector
        Vc_psi = np.arccos(Vc_syms[:, 2]) * 180 / np.pi
        if symmetry == symmetry.cubic:
            rgb = AnotherWindowLivePrediction.get_field_color(orientation_matrix, axis, symmetry)            
            return rgb
            # angleR = 45 - Vc_chi  # red color proportional to (45 - chi)
            # minAngleR = 0
            # maxAngleR = 45
            # angleB = Vc_phi  # blue color proportional to phi
            # minAngleB = 0
            # maxAngleB = 45
        elif symmetry == symmetry.hexagonal:
            angleR = 90 - Vc_psi  # red color proportional to (90 - psi)
            minAngleR = 0
            maxAngleR = 90
            angleB = Vc_phi  # blue color proportional to phi
            minAngleB = 0
            maxAngleB = 30
        else:
            rgb = AnotherWindowLivePrediction.get_field_color(orientation_matrix, axis, symmetry)            
            return rgb
        # find the axis lying in the fundamental zone
        fz_list = ((angleR >= minAngleR) & (angleR < maxAngleR) &
                   (angleB >= minAngleB) & (angleB < maxAngleB)).tolist()
        if not fz_list.count(True) == 1:
            return 0,0,0
        i_SST = fz_list.index(True)
        r = angleR[i_SST] / maxAngleR
        g = (maxAngleR - angleR[i_SST]) / maxAngleR * (maxAngleB - angleB[i_SST]) / maxAngleB
        b = (maxAngleR - angleR[i_SST]) / maxAngleR * angleB[i_SST] / maxAngleB
        rgb = np.array([r, g, b])
        if saturate:
            rgb = rgb / rgb.max()
        return rgb 
    
    @staticmethod
    def get_field_color(orientation_matrix, axis=np.array([0., 0., 1.]), symmetry=None):
        """Compute the IPF (inverse pole figure) colour for this orientation.
        Given a particular axis expressed in the laboratory coordinate system,
        one can compute the so called IPF colour based on that direction
        expressed in the crystal coordinate system as :math:`[x_c,y_c,z_c]`.
        There is only one tuple (u,v,w) such that:
        .. math::
          [x_c,y_c,z_c]=u.[0,0,1]+v.[0,1,1]+w.[1,1,1]
        and it is used to assign the RGB colour.
        :param ndarray axis: the direction to use to compute the IPF colour.
        :param Symmetry symmetry: the symmetry operator to use.
        :return tuple: a tuple contining the RGB values.
        """
        for sym in symmetry.symmetry_operators():
            Osym = np.dot(sym, orientation_matrix)
            Vc = np.dot(Osym, axis)
            if Vc[2] < 0:
                Vc *= -1.  # using the upward direction
            uvw = np.array([Vc[2] - Vc[1], Vc[1] - Vc[0], Vc[0]])
            uvw /= np.linalg.norm(uvw)
            uvw /= max(uvw)
            if (uvw[0] >= 0. and uvw[0] <= 1.0) and (uvw[1] >= 0. and uvw[1] <= 1.0) and (
                    uvw[2] >= 0. and uvw[2] <= 1.0):
                break
        uvw = uvw / uvw.max()
        return uvw    
    
class LoggingCallback(Callback):
    """Callback that logs message at end of epoch.
    """
    def __init__(self, print_fcn, progress_func, qapp, model, fn_model):
        Callback.__init__(self)
        self.print_fcn = print_fcn
        self.progress_func = progress_func
        self.batch_count = 0
        self.qapp = qapp
        self.model = model
        self.model_name = fn_model
    
    def on_batch_end(self, batch, logs={}):
        self.batch_count += 1
        self.progress_func.setValue(self.batch_count)
        self.qapp.processEvents() 
        
    def on_epoch_end(self, epoch, logs={}):
        msg = "{Epoch: %i} %s" % (epoch, ", ".join("%s: %f" % (k, v) for k, v in logs.items()))
        self.print_fcn(msg)
        model_json = self.model.to_json()
        with open(self.model_name+".json", "w") as json_file:
            json_file.write(model_json)            
        # serialize weights to HDF5
        self.model.save_weights(self.model_name+"_"+str(epoch)+".h5")

class Symmetry(enum.Enum):
    """
    Class to describe crystal symmetry defined by its Laue class symbol.
    """
    cubic = 'm3m'
    hexagonal = '6/mmm'
    orthorhombic = 'mmm'
    tetragonal = '4/mmm'
    trigonal = 'bar3m'
    monoclinic = '2/m'
    triclinic = 'bar1'
    
    def symmetry_operators(self, use_miller_bravais=False):
        """Define the equivalent crystal symmetries.
        Those come from Randle & Engler, 2000. For instance in the cubic
        crystal struture, for instance there are 24 equivalent cube orientations.
        :returns array: A numpy array of shape (n, 3, 3) where n is the \
        number of symmetries of the given crystal structure.
        """
        if self is Symmetry.cubic:
            sym = np.zeros((48, 3, 3), dtype=np.float)
            sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[1] = np.array([[0., 0., -1.], [0., -1., 0.], [-1., 0., 0.]])
            sym[2] = np.array([[0., 0., -1.], [0., 1., 0.], [1., 0., 0.]])
            sym[3] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
            sym[4] = np.array([[0., 0., 1.], [0., 1., 0.], [-1., 0., 0.]])
            sym[5] = np.array([[1., 0., 0.], [0., 0., -1.], [0., 1., 0.]])
            sym[6] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
            sym[7] = np.array([[1., 0., 0.], [0., 0., 1.], [0., -1., 0.]])
            sym[8] = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
            sym[9] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
            sym[10] = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 1.]])
            sym[11] = np.array([[0., 0., 1.], [1., 0., 0.], [0., 1., 0.]])
            sym[12] = np.array([[0., 1., 0.], [0., 0., 1.], [1., 0., 0.]])
            sym[13] = np.array([[0., 0., -1.], [-1., 0., 0.], [0., 1., 0.]])
            sym[14] = np.array([[0., -1., 0.], [0., 0., 1.], [-1., 0., 0.]])
            sym[15] = np.array([[0., 1., 0.], [0., 0., -1.], [-1., 0., 0.]])
            sym[16] = np.array([[0., 0., -1.], [1., 0., 0.], [0., -1., 0.]])
            sym[17] = np.array([[0., 0., 1.], [-1., 0., 0.], [0., -1., 0.]])
            sym[18] = np.array([[0., -1., 0.], [0., 0., -1.], [1., 0., 0.]])
            sym[19] = np.array([[0., 1., 0.], [1., 0., 0.], [0., 0., -1.]])
            sym[20] = np.array([[-1., 0., 0.], [0., 0., 1.], [0., 1., 0.]])
            sym[21] = np.array([[0., 0., 1.], [0., -1., 0.], [1., 0., 0.]])
            sym[22] = np.array([[0., -1., 0.], [-1., 0., 0.], [0., 0., -1.]])
            sym[23] = np.array([[-1., 0., 0.], [0., 0., -1.], [0., -1., 0.]])
            for i in range(24):
                sym[24+i] = -sym[i]
        elif self is Symmetry.hexagonal:
            # using the Miller-Bravais representation here
            if use_miller_bravais:
                sym = np.zeros((24, 4, 4), dtype=np.int)
                sym[0] = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
                sym[1] = np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
                sym[2] = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
                sym[3] = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
                sym[4] = np.array([[0, 0, 1, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1]])
                sym[5] = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, -1]])
                sym[6] = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
                sym[7] = np.array([[0, 0, -1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
                sym[8] = np.array([[0, -1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
                sym[9] = np.array([[-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
                sym[10] = np.array([[0, 0, -1, 0], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 0, -1]])
                sym[11] = np.array([[0, -1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, 0], [0, 0, 0, -1]])
                sym[12] = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
                sym[13] = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
                sym[14] = np.array([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
                sym[15] = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
                sym[16] = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, -1]])
                sym[17] = np.array([[0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1]])
                sym[18] = np.array([[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
                sym[19] = np.array([[-1, 0, 0, 0], [0, 0, -1, 0], [0, -1, 0, 0], [0, 0, 0, 1]])
                sym[20] = np.array([[0, 0, -1, 0], [0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
                sym[21] = np.array([[0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1]])
                sym[22] = np.array([[-1, 0, 0, 0], [0, 0, -1, 0], [0, -1, 0, 0], [0, 0, 0, -1]])
                sym[23] = np.array([[0, 0, -1, 0], [0, -1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, -1]])
            else:
                sym = np.zeros((12, 3, 3), dtype=np.float)
                s60 = np.sin(60 * np.pi / 180)
                sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
                sym[1] = np.array([[0.5, s60, 0.], [-s60, 0.5, 0.], [0., 0., 1.]])
                sym[2] = np.array([[-0.5, s60, 0.], [-s60, -0.5, 0.], [0., 0., 1.]])
                sym[3] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
                sym[4] = np.array([[-0.5, -s60, 0.], [s60, -0.5, 0.], [0., 0., 1.]])
                sym[5] = np.array([[0.5, -s60, 0.], [s60, 0.5, 0.], [0., 0., 1.]])
                sym[6] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
                sym[7] = np.array([[0.5, s60, 0.], [s60, -0.5, 0.], [0., 0., -1.]])
                sym[8] = np.array([[-0.5, s60, 0.], [s60, 0.5, 0.], [0., 0., -1.]])
                sym[9] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
                sym[10] = np.array([[-0.5, -s60, 0.], [-s60, 0.5, 0.], [0., 0., -1.]])
                sym[11] = np.array([[0.5, -s60, 0.], [-s60, -0.5, 0.], [0., 0., -1.]])
                # for i in range(12):
                #   sym[12+i] = -sym[i]
        elif self is Symmetry.orthorhombic:
            sym = np.zeros((8, 3, 3), dtype=np.float)
            sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[1] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
            sym[2] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
            sym[3] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
            sym[4] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
            sym[5] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[6] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
            sym[7] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
        elif self is Symmetry.monoclinic:
            sym = np.zeros((4, 3, 3), dtype=np.float)
            sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[1] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
            sym[2] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
            sym[3] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
        elif self is Symmetry.tetragonal:
            sym = np.zeros((8, 3, 3), dtype=np.float)
            sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[1] = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
            sym[2] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., 1.]])
            sym[3] = np.array([[0., 1., 0.], [-1., 0., 0.], [0., 0., 1.]])
            sym[4] = np.array([[1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
            sym[5] = np.array([[-1., 0., 0.], [0., 1., 0.], [0., 0., -1.]])
            sym[6] = np.array([[0., 1., 0.], [1., 0., 0.], [0., 0., -1.]])
            sym[7] = np.array([[0., -1., 0.], [-1., 0., 0.], [0., 0., -1.]])
        elif self is Symmetry.triclinic:
            sym = np.zeros((2, 3, 3), dtype=np.float)
            sym[0] = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
            sym[1] = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
        else:
            raise ValueError('warning, symmetry not supported: %s' % self)
        return sym

class Lattice:
    '''
    The Lattice class to create one of the 14 Bravais lattices.
    This particular class has been partly inspired from the pymatgen
    project at https://github.com/materialsproject/pymatgen
    Any of the 7 lattice systems (each corresponding to one point group)
    can be easily created and manipulated.
    The lattice centering can be specified to form any of the 14 Bravais
    lattices:
     * Primitive (P): lattice points on the cell corners only (default);
     * Body (I): one additional lattice point at the center of the cell;
     * Face (F): one additional lattice point at the center of each of
       the faces of the cell;
     * Base (A, B or C): one additional lattice point at the center of
       each of one pair of the cell faces.
    ::
      a = 0.352 # FCC Nickel
      l = Lattice.face_centered_cubic(a)
      print(l.volume())
    Addditionnally the point-basis can be controlled to address non
    Bravais lattice cells. It is set to a single atoms at (0, 0, 0) by
    default so that each cell is a Bravais lattice but may be changed to
    something more complex to achieve HCP structure or Diamond structure
    for instance.
    '''

    def __init__(self, matrix, centering='P', symmetry=None):
        '''Create a crystal lattice (unit cell).
        Create a lattice from a 3x3 matrix.
        Each row in the matrix represents one lattice vector.
        '''
        m = np.array(matrix, dtype=np.float64).reshape((3, 3))
        lengths = np.sqrt(np.sum(m ** 2, axis=1))
        angles = np.zeros(3)
        for i in range(3):
            j = (i + 1) % 3
            k = (i + 2) % 3
            angles[i] = dot(m[j], m[k]) / (lengths[j] * lengths[k])
        angles = np.arccos(angles) * 180. / pi
        self._angles = angles
        self._lengths = lengths
        self._matrix = m
        self._centering = centering
        self._symmetry = symmetry

    def __eq__(self, other):
        """Override the default Equals behavior.
        The equality of two Lattice objects is based on the equality of their angles, lengths, and centering.
        """
        if not isinstance(other, self.__class__):
            return False
        for i in range(3):
            if self._angles[i] != other._angles[i]:
                return False
            elif self._lengths[i] != other._lengths[i]:
                return False
        if self._centering != other._centering:
            return False
        if self._symmetry != other._symmetry:
            return False
        return True

    def reciprocal_lattice(self):
        '''Compute the reciprocal lattice.
        The reciprocal lattice defines a crystal in terms of vectors that
        are normal to a plane and whose lengths are the inverse of the
        interplanar spacing. This method computes the three reciprocal
        lattice vectors defined by:
        .. math::
         * a.a^* = 1
         * b.b^* = 1
         * c.c^* = 1
        '''
        [a, b, c] = self._matrix
        V = self.volume()
        astar = np.cross(b, c) / V
        bstar = np.cross(c, a) / V
        cstar = np.cross(a, b) / V
        return [astar, bstar, cstar]

    @property
    def matrix(self):
        """Returns a copy of matrix representing the Lattice."""
        return np.copy(self._matrix)

    def get_symmetry(self):
        """Returns the type of `Symmetry` of the Lattice."""
        return self._symmetry

    @staticmethod
    def symmetry(crystal_structure=Symmetry.cubic, use_miller_bravais=False):
        """Define the equivalent crystal symmetries.
        Those come from Randle & Engler, 2000. For instance in the cubic
        crystal struture, for instance there are 24 equivalent cube orientations.
        :param crystal_structure: an instance of the `Symmetry` class describing the crystal symmetry.
        :raise ValueError: if the given symmetry is not supported.
        :returns array: A numpy array of shape (n, 3, 3) where n is the \
        number of symmetries of the given crystal structure.
        """
        return crystal_structure.symmetry_operators(use_miller_bravais=use_miller_bravais)

    @staticmethod
    def cubic(a):
        '''
        Create a cubic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter (a = b = c here)
        *Returns*
        A `Lattice` instance corresponding to a primitice cubic lattice.
        '''
        return Lattice([[a, 0.0, 0.0], [0.0, a, 0.0], [0.0, 0.0, a]], symmetry=Symmetry.cubic)

    @staticmethod
    def body_centered_cubic(a):
        '''
        Create a body centered cubic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter (a = b = c here)
        *Returns*
        A `Lattice` instance corresponding to a body centered cubic
        lattice.
        '''
        return Lattice.from_parameters(a, a, a, 90, 90, 90, centering='I', symmetry=Symmetry.cubic)

    @staticmethod
    def face_centered_cubic(a):
        '''
        Create a face centered cubic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter (a = b = c here)
        *Returns*
        A `Lattice` instance corresponding to a face centered cubic
        lattice.
        '''
        return Lattice.from_parameters(a, a, a, 90, 90, 90, centering='F', symmetry=Symmetry.cubic)

    @staticmethod
    def tetragonal(a, c):
        '''
        Create a tetragonal Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter
        **c**: third lattice length parameter (b = a here)
        *Returns*
        A `Lattice` instance corresponding to a primitive tetragonal
        lattice.
        '''
        return Lattice.from_parameters(a, a, c, 90, 90, 90, symmetry=Symmetry.tetragonal)

    @staticmethod
    def body_centered_tetragonal(a, c):
        '''
        Create a body centered tetragonal Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter
        **c**: third lattice length parameter (b = a here)
        *Returns*
        A `Lattice` instance corresponding to a body centered tetragonal
        lattice.
        '''
        return Lattice.from_parameters(a, a, c, 90, 90, 90, centering='I', symmetry=Symmetry.tetragonal)

    @staticmethod
    def orthorhombic(a, b, c):
        '''
        Create a tetragonal Lattice unit cell with 3 different length
        parameters a, b and c.
        '''
        return Lattice.from_parameters(a, b, c, 90, 90, 90, symmetry=Symmetry.orthorhombic)

    @staticmethod
    def base_centered_orthorhombic(a, b, c):
        '''
        Create a based centered orthorombic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter
        **b**: second lattice length parameter
        **c**: third lattice length parameter
        *Returns*
        A `Lattice` instance corresponding to a based centered orthorombic
        lattice.
        '''
        return Lattice.from_parameters(a, b, c, 90, 90, 90, centering='C', symmetry=Symmetry.orthorhombic)

    @staticmethod
    def body_centered_orthorhombic(a, b, c):
        '''
        Create a body centered orthorombic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter
        **b**: second lattice length parameter
        **c**: third lattice length parameter
        *Returns*
        A `Lattice` instance corresponding to a body centered orthorombic
        lattice.
        '''
        return Lattice.from_parameters(a, b, c, 90, 90, 90, centering='I', symmetry=Symmetry.orthorhombic)

    @staticmethod
    def face_centered_orthorhombic(a, b, c):
        '''
        Create a face centered orthorombic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter
        **b**: second lattice length parameter
        **c**: third lattice length parameter
        *Returns*
        A `Lattice` instance corresponding to a face centered orthorombic
        lattice.
        '''
        return Lattice.from_parameters(a, b, c, 90, 90, 90, centering='F', symmetry=Symmetry.orthorhombic)

    @staticmethod
    def hexagonal(a, c):
        '''
        Create a hexagonal Lattice unit cell with length parameters a and c.
        '''
        return Lattice.from_parameters(a, a, c, 90, 90, 120, symmetry=Symmetry.hexagonal)

    @staticmethod
    def rhombohedral(a, alpha):
        '''
        Create a rhombohedral Lattice unit cell with one length
        parameter a and the angle alpha.
        '''
        return Lattice.from_parameters(a, a, a, alpha, alpha, alpha, symmetry=Symmetry.trigonal)

    @staticmethod
    def monoclinic(a, b, c, alpha):
        '''
        Create a monoclinic Lattice unit cell with 3 different length
        parameters a, b and c. The cell angle is given by alpha.
        The lattice centering id primitive ie. 'P'
        '''
        return Lattice.from_parameters(a, b, c, alpha, 90, 90, symmetry=Symmetry.monoclinic)

    @staticmethod
    def base_centered_monoclinic(a, b, c, alpha):
        '''
        Create a based centered monoclinic Lattice unit cell.
        *Parameters*
        **a**: first lattice length parameter
        **b**: second lattice length parameter
        **c**: third lattice length parameter
        **alpha**: first lattice angle parameter
        *Returns*
        A `Lattice` instance corresponding to a based centered monoclinic
        lattice.
        '''
        return Lattice.from_parameters(a, b, c, alpha, 90, 90, centering='C', symmetry=Symmetry.monoclinic)

    @staticmethod
    def triclinic(a, b, c, alpha, beta, gamma):
        '''
        Create a triclinic Lattice unit cell with 3 different length
        parameters a, b, c and three different cell angles alpha, beta
        and gamma.
        ..note::
           This method is here for the sake of completeness since one can
           create the triclinic cell directly using the `from_parameters`
           method.
        '''
        return Lattice.from_parameters(a, b, c, alpha, beta, gamma, symmetry=Symmetry.triclinic)
    
    @staticmethod
    def from_parameters(a, b, c, alpha, beta, gamma, x_aligned_with_a=False, centering='P', symmetry=Symmetry.triclinic):
        """
        Create a Lattice using unit cell lengths and angles (in degrees).
        The lattice centering can also be specified (among 'P', 'I', 'F',
        'A', 'B' or 'C').
        :param float a: first lattice length parameter.
        :param float b: second lattice length parameter.
        :param float c: third lattice length parameter.
        :param float alpha: first lattice angle parameter.
        :param float beta: second lattice angle parameter.
        :param float gamma: third lattice angle parameter.
        :param bool x_aligned_with_a: flag to control the convention used to define the Cartesian frame.
        :param str centering: lattice centering ('P' by default) passed to the `Lattice` class.
        :param symmetry: a `Symmetry` instance to be passed to the lattice.
        :return: A `Lattice` instance with the specified lattice parameters and centering.
        """
        alpha_r = radians(alpha)
        beta_r = radians(beta)
        gamma_r = radians(gamma)
        if x_aligned_with_a:  # first lattice vector (a) is aligned with X
            vector_a = a * np.array([1, 0, 0])
            vector_b = b * np.array([np.cos(gamma_r), np.sin(gamma_r), 0])
            c1 = c * np.cos(beta_r)
            c2 = c * (np.cos(alpha_r) - np.cos(gamma_r) * np.cos(beta_r)) / np.sin(gamma_r)
            vector_c = np.array([c1, c2, np.sqrt(c ** 2 - c1 ** 2 - c2 ** 2)])
        else:  # third lattice vector (c) is aligned with Z
            cos_gamma_star = (np.cos(alpha_r) * np.cos(beta_r) - np.cos(gamma_r)) / (np.sin(alpha_r) * np.sin(beta_r))
            sin_gamma_star = np.sqrt(1 - cos_gamma_star ** 2)
            vector_a = [a * np.sin(beta_r), 0.0, a * np.cos(beta_r)]
            vector_b = [-b * np.sin(alpha_r) * cos_gamma_star, b * np.sin(alpha_r) * sin_gamma_star, b * np.cos(alpha_r)]
            vector_c = [0.0, 0.0, float(c)]
        return Lattice([vector_a, vector_b, vector_c], centering=centering, symmetry=symmetry)

    def volume(self):
        """Compute the volume of the unit cell."""
        m = self._matrix
        return abs(np.dot(np.cross(m[0], m[1]), m[2]))

    def get_hkl_family(self, hkl):
        """Get a list of the hkl planes composing the given family for
        this crystal lattice.
        *Parameters*
        **hkl**: miller indices of the requested family
        *Returns*
        A list of the hkl planes in the given family.
        """
        planes = HklPlane.get_family(hkl, lattice=self, crystal_structure=self._symmetry)
        return planes

class HklObject:
    def __init__(self, h, k, l, lattice=None):
        '''Create a new hkl object with the given Miller indices and
           crystal lattice.
        '''
        if lattice == None:
            lattice = Lattice.cubic(1.0)
        self._lattice = lattice
        self._h = h
        self._k = k
        self._l = l

    @property
    def lattice(self):
        return self._lattice

    def set_lattice(self, lattice):
        """Assign a new `Lattice` to this instance.
        :param lattice: the new crystal lattice.
        """
        self._lattice = lattice

    @property
    def h(self):
        return self._h

    @property
    def k(self):
        return self._k

    @property
    def l(self):
        return self._l

    def miller_indices(self):
        '''
        Returns an immutable tuple of the plane Miller indices.
        '''
        return (self._h, self._k, self._l)

class HklDirection(HklObject):
    def direction(self):
        '''Returns a normalized vector, expressed in the cartesian
        coordinate system, corresponding to this crystallographic direction.
        '''
        (h, k, l) = self.miller_indices()
        M = self._lattice.matrix.T  # the columns of M are the a, b, c vector in the cartesian coordinate system
        l_vect = M.dot(np.array([h, k, l]))
        return l_vect / np.linalg.norm(l_vect)

    def angle_with_direction(self, hkl):
        '''Computes the angle between this crystallographic direction and
        the given direction (in radian).'''
        return np.arccos(np.dot(self.direction(), hkl.direction()))

    @staticmethod
    def angle_between_directions(hkl1, hkl2, lattice=None):
        '''Computes the angle between two crystallographic directions (in radian).
        :param tuple hkl1: The triplet of the miller indices of the first direction.
        :param tuple hkl2: The triplet of the miller indices of the second direction.
        :param Lattice lattice: The crystal lattice, will default to cubic if not specified.
        :returns float: The angle in radian.
        '''
        d1 = HklDirection(*hkl1, lattice=lattice)
        d2 = HklDirection(*hkl2, lattice=lattice)
        return d1.angle_with_direction(d2)

    @staticmethod
    def three_to_four_indices(u, v, w):
        """Convert from Miller indices to Miller-Bravais indices. this is used for hexagonal crystal lattice."""
        return (2 * u - v) / 3., (2 * v - u) / 3., -(u + v) / 3., w

    @staticmethod
    def four_to_three_indices(U, V, T, W):
        """Convert from Miller-Bravais indices to Miller indices. this is used for hexagonal crystal lattice."""
        u, v, w = U - T, V - T, W
        gcd = functools.reduce(math.gcd, (u, v, w))
        return u / gcd, v / gcd, w / gcd

    @staticmethod
    def angle_between_4indices_directions(hkil1, hkil2, ac):
        """Computes the angle between two crystallographic directions in a hexagonal lattice.
        The solution was derived by F. Frank in:
        On Miller - Bravais indices and four dimensional vectors. Acta Cryst. 18, 862-866 (1965)
        :param tuple hkil1: The quartet of the indices of the first direction.
        :param tuple hkil2: The quartet of the indices of the second direction.
        :param tuple ac: the lattice parameters of the hexagonal structure in the form (a, c).
        :returns float: The angle in radian.
        """
        h1, k1, i1, l1 = hkil1
        h2, k2, i2, l20 = hkil2
        a, c = ac
        lambda_square = 2. / 3 * (c / a) ** 2
        value = (h1 * h2 + k1 * k2 + i1 * i2 + lambda_square * l1 * l20) / \
                (np.sqrt(h1 ** 2 + k1 ** 2 + i1 ** 2 + lambda_square * l1 ** 2) *
                 np.sqrt(h2 ** 2 + k2 ** 2 + i2 ** 2 + lambda_square * l20 ** 2))
        return np.arccos(value)

class HklPlane(HklObject):
    '''
    This class define crystallographic planes using Miller indices.
    A plane can be create by speficying its Miller indices and the
    crystal lattice (default is cubic with lattice parameter of 1.0)
    ::
      a = 0.405 # FCC Aluminium
      l = Lattice.cubic(a)
      p = HklPlane(1, 1, 1, lattice=l)
      print(p)
      print(p.scattering_vector())
      print(p.interplanar_spacing())
    .. note::
      Miller indices are defined in terms of the inverse of the intercept
      of the plane on the three crystal axes a, b, and c.
    '''

    def __eq__(self, other):
        """Override the default Equals behavior.
        The equality of two HklObjects is based on the equality of their miller indices.
        """
        if isinstance(other, self.__class__):
            return self._h == other._h and self._k == other._k and \
                   self._l == other._l and self._lattice == other._lattice
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

    def normal(self):
        '''Returns the unit vector normal to the plane.
        We use of the repiprocal lattice to compute the normal to the plane
        and return a normalised vector.
        '''
        n = self.scattering_vector()
        return n / np.linalg.norm(n)

    def scattering_vector(self):
        '''Calculate the scattering vector of this `HklPlane`.
        The scattering vector (or reciprocal lattice vector) is normal to
        this `HklPlane` and its length is equal to the inverse of the
        interplanar spacing. In the cartesian coordinate system of the
        crystal, it is given by:
        ..math
          G_c = h.a^* + k.b^* + l.c^*
        :returns: a numpy vector expressed in the cartesian coordinate system of the crystal.
        '''
        [astar, bstar, cstar] = self._lattice.reciprocal_lattice()
        (h, k, l) = self.miller_indices()
        # express (h, k, l) in the cartesian crystal CS
        Gc = h * astar + k * bstar + l * cstar
        return Gc

    def friedel_pair(self):
        """Create the Friedel pair of the HklPlane."""
        (h, k, l) = self.miller_indices()
        pair = HklPlane(-h, -k, -l, self._lattice)
        return pair

    def interplanar_spacing(self):
        '''
        Compute the interplanar spacing.
        For cubic lattice, it is:
        .. math::
           d = a / \sqrt{h^2 + k^2 + l^2}
        The general formula comes from 'Introduction to Crystallography'
        p. 68 by Donald E. Sands.
        '''
        (a, b, c) = self._lattice._lengths
        (h, k, l) = self.miller_indices()
        (alpha, beta, gamma) = radians(self._lattice._angles)
        # d = a / np.sqrt(h**2 + k**2 + l**2) # for cubic structure only
        d = self._lattice.volume() / np.sqrt(h ** 2 * b ** 2 * c ** 2 * np.sin(alpha) ** 2 + \
                                             k ** 2 * a ** 2 * c ** 2 * np.sin(
                                                 beta) ** 2 + l ** 2 * a ** 2 * b ** 2 * np.sin(gamma) ** 2 + \
                                             2 * h * l * a * b ** 2 * c * (
                                                 np.cos(alpha) * np.cos(gamma) - np.cos(beta)) + \
                                             2 * h * k * a * b * c ** 2 * (
                                                 np.cos(alpha) * np.cos(beta) - np.cos(gamma)) + \
                                             2 * k * l * a ** 2 * b * c * (
                                                 np.cos(beta) * np.cos(gamma) - np.cos(alpha)))
        return d

    @staticmethod
    def four_to_three_indices(U, V, T, W):
        """Convert four to three index representation of a slip plane (used for hexagonal crystal lattice)."""
        return U, V, W

    @staticmethod
    def three_to_four_indices(u, v, w):
        """Convert three to four index representation of a slip plane (used for hexagonal crystal lattice)."""
        return u, v, -(u + v), w

    def is_in_list(self, hkl_planes, friedel_pair=False):
        """Check if the hkl plane is in the given list.
        By default this relies on the built in in test from the list type which in turn calls in the __eq__ method.
        This means it will return True if a plane with the exact same miller indices (and same lattice) is in the list.
        Turning on the friedel_pair flag will allow to test also the Friedel pair (-h, -k, -l) and return True if it is
        in the list.
        For instance (0,0,1) and (0,0,-1) are in general considered as the same lattice plane.
        """
        if not friedel_pair:
            return self in hkl_planes
        else:
            return self in hkl_planes or self.friedel_pair() in hkl_planes

    @staticmethod
    def is_same_family(hkl1, hkl2, crystal_structure=Symmetry.cubic):
        """Static mtd to test if both lattice planes belongs to same family.
        A family {hkl} is composed by all planes that are equivalent to (hkl)
        using the symmetry of the lattice. The lattice assoiated with `hkl2`
        is not taken into account here.
        """
        return hkl1.is_in_list(HklPlane.get_family(hkl2.miller_indices(), lattice=hkl1._lattice,
                                                   crystal_structure=crystal_structure))

    @staticmethod
    def get_family(hkl, lattice=None, include_friedel_pairs=False, crystal_structure=Symmetry.cubic):
        """Static method to obtain a list of the different crystallographic
        planes in a particular family.
        :param str hkl: a sequence of 3 (4 for hexagonal) numbers corresponding to the miller indices.
        :param Lattice lattice: The reference crystal lattice (default None).
        :param bool include_friedel_pairs: Flag to include the Friedel pairs in the list (False by default).
        :param str crystal_structure: A string descibing the crystal structure (cubic by default).
        :raise ValueError: if the given string does not correspond to a supported family.
        :returns list: a list of the :py:class:`~HklPlane` in the given hkl family.
        .. note::
          The method account for the lattice symmetry to create a list of equivalent lattice plane from the point
          of view of the point group symmetry. A flag can be used to include or not the Friedel pairs. If not, the
          family is contstructed using the miller indices limited the number of minus signs. For instance  (1,0,0)
          will be in the list and not (-1,0,0).
        """
        if not (len(hkl) == 3 or (len(hkl) == 4 and crystal_structure == Symmetry.hexagonal)):
            raise ValueError('warning, family not supported: {}'.format(hkl))
        # handle hexagonal case
        if len(hkl) == 4:
            h = int(hkl[0])
            k = int(hkl[1])
            i = int(hkl[2])
            l = int(hkl[3])
            (h, k, l) = HklPlane.four_to_three_indices(h, k, i, l)  # useless as it just drops i
        else:  # 3 indices
            h = int(hkl[0])
            k = int(hkl[1])
            l = int(hkl[2])
            if crystal_structure == Symmetry.hexagonal:
                i = -(h + k)
        family = []
        # construct lattice plane family from the symmetry operators
        if crystal_structure == Symmetry.hexagonal:
          syms = Lattice.symmetry(crystal_structure, use_miller_bravais=True)
        else:
          syms = Lattice.symmetry(crystal_structure)
        for sym in syms:
            if crystal_structure == Symmetry.hexagonal:
                n_sym = np.dot(sym, np.array([h, k, i, l]))
                n_sym = HklPlane.four_to_three_indices(*n_sym)
            else:  # 3 indices
                n_sym = np.dot(sym, np.array([h, k, l]))
            hkl_sym = HklPlane(*n_sym, lattice=lattice)
            if not hkl_sym.is_in_list(family, friedel_pair=True):
                family.append(hkl_sym)
            if include_friedel_pairs:
                hkl_sym = HklPlane(-n_sym[0], -n_sym[1], -n_sym[2], lattice=lattice)
                if not hkl_sym.is_in_list(family, friedel_pair=False):
                    family.append(hkl_sym)
        if not include_friedel_pairs:
            # for each hkl plane chose between (h, k, l) and (-h, -k, -l) to have the less minus signs
            for i in range(len(family)):
                hkl = family[i]
                (h, k, l) = hkl.miller_indices()
                if np.where(np.array([h, k, l]) < 0)[0].size > 0 and np.where(np.array([h, k, l]) <= 0)[0].size >= 2:
                    family[i] = hkl.friedel_pair()
                    #print('replacing plane (%d%d%d) by its pair: (%d%d%d)' % (h, k, l, -h, -k, -l))
        return family

    def multiplicity(self, symmetry=Symmetry.cubic):
        """compute the general multiplicity for this `HklPlane` and the given `Symmetry`.
        :param Symmetry symmetry: The crystal symmetry to take into account.
        :return: the number of equivalent planes in the family.
        """
        return len(HklPlane.get_family(self.miller_indices(), include_friedel_pairs=True, crystal_structure=symmetry))        

class PoleFigure:
    """A class to handle pole figures.

    A pole figure is a popular tool to plot multiple crystal orientations,
    either in the sample coordinate system (direct pole figure) or
    alternatively plotting a particular direction in the crystal
    coordinate system (inverse pole figure).
    """
    def __init__(self, lattice=None, axis='Z', hkl='111', proj='stereo'):
        """
        Create an empty PoleFigure object associated with an empty Microstructure.
        :param microstructure: the :py:class:`~pymicro.crystal.microstructure.Microstructure` containing the collection of orientations to plot (None by default).
        :param lattice: the crystal :py:class:`~pymicro.crystal.lattice.Lattice`.
        :param str axis: the pole figure axis ('Z' by default), vertical axis in the direct pole figure and direction plotted on the inverse pole figure.
        .. warning::
           Any crystal structure is now supported (you have to set the proper
           crystal lattice) but it has only really be tested for cubic.
        :param str hkl: slip plane family ('111' by default)
        :param str proj: projection type, can be either 'stereo' (default) or 'flat'
        """
        self.proj = proj
        self.axis = axis
        
        if self.axis == 'Z':
            self.axis_crystal = np.array([0, 0, 1])
        elif self.axis == 'Y':
            self.axis_crystal = np.array([0, 1, 0])
        else:
            self.axis_crystal = np.array([1, 0, 0])

        if lattice:
            self.lattice = lattice
        else:
            self.lattice = Lattice.cubic(1.0)
        self.family = None
        self.poles = []
        self.set_hkl_poles(hkl)
        self.mksize = 50
        self.x = np.array([1., 0., 0.])
        self.y = np.array([0., 1., 0.])
        self.z = np.array([0., 0., 1.])

    def set_hkl_poles(self, hkl='111'):
        """Set the pole (aka hkl planes) list to to use in the `PoleFigure`.

        The list of poles can be given by the family type or directly by a list of `HklPlanes` objects.

        :params str/list hkl: slip plane family ('111' by default)
        """
        if type(hkl) is str:
            self.family = hkl  # keep a record of this
            hkl_planes = self.lattice.get_hkl_family(self.family)
        elif type(hkl) is list:
            self.family = None
            hkl_planes = hkl
        self.poles = hkl_planes  #[p.normal() for p in hkl_planes]

    def plot_line_between_crystal_dir(self, c1, c2, ax=None, steps=25, col='k'):
        '''Plot a curve between two crystal directions.

        The curve is actually composed of several straight lines segments to
        draw from direction 1 to direction 2.

        :param c1: vector describing crystal direction 1
        :param c2: vector describing crystal direction 2
        :param ax: a reference to a pyplot ax to draw the line
        :param int steps: number of straight lines composing the curve (11 by default)
        :param col: line color (black by default)
        '''
        path = np.zeros((steps, 2), dtype=float)
        for j, i in enumerate(np.linspace(0., 1., steps)):
            ci = i * c1 + (1 - i) * c2
            ci /= np.linalg.norm(ci)
            if self.proj == 'stereo':
                ci += self.z
                ci /= ci[2]
            path[j, 0] = ci[0]
            path[j, 1] = ci[1]
        ax.plot(path[:, 0], path[:, 1], color=col, markersize=self.mksize, linewidth=0.5, zorder=0)
        plt.axis("off")
        
    def plot_pf_background(self, ax, labels=True):
        '''Function to plot the background of the pole figure.
        :param ax: a reference to a pyplot ax to draw the backgroud.
        :param bool labels: add lables to axes (True by default).
        '''
        an = np.linspace(0, 2 * np.pi, 100)
        ax.plot(np.cos(an), np.sin(an), 'k-', zorder=0)
        ax.plot([-1, 1], [0, 0], 'k-', zorder=0)
        ax.plot([0, 0], [-1, 1], 'k-', zorder=0)
        axe_labels = ['X', 'Y', 'Z']
        if self.axis == 'Z':
            (h, v, _) = (0, 1, 2)
        elif self.axis == 'Y':
            (h, v, _) = (0, 2, 1)
        else:
            (h, v, _) = (1, 2, 0)
        if labels:
            ax.annotate(axe_labels[h], (1.01, 0.0), xycoords='data', fontsize=8,
                        horizontalalignment='left', verticalalignment='center')
            ax.annotate(axe_labels[v], (0.0, 1.01), xycoords='data', fontsize=8,
                        horizontalalignment='center', verticalalignment='bottom')

    def sst_symmetry(self, v):
        """Transform a given vector according to the lattice symmetry associated
        with the pole figure.

        This function transform a vector so that it lies in the smallest
        symmetry equivalent zone.

        :param v: the vector to transform.
        :return: the transformed vector.
        """
        # get the symmetry from the lattice associated with the pole figure
        symmetry = self.lattice._symmetry
        if symmetry == symmetry.cubic:
            return PoleFigure.sst_symmetry_cubic(v)
        elif symmetry == symmetry.hexagonal:
            syms = symmetry.symmetry_operators()
            for i in range(syms.shape[0]):
                sym = syms[i]
                v_sym = np.dot(sym, v)
                # look at vectors pointing up
                if v_sym[2] < 0:
                    v_sym *= -1
                # now evaluate if projection is in the sst
                if v_sym[1] < 0 or v_sym[0] < 0:
                    continue
                elif v_sym[1] / v_sym[0] > np.tan(np.pi / 6):
                    continue
                else:
                    break
            return v_sym
        else:
            print('unsupported symmetry: %s' % symmetry)
            return None

    @staticmethod
    def sst_symmetry_cubic(z_rot):
        '''Transform a given vector according to the cubic symmetry.

        This function transform a vector so that it lies in the unit SST triangle.

        :param z_rot: vector to transform.
        :return: the transformed vector.
        '''
        if z_rot[0] < 0: z_rot[0] = -z_rot[0]
        if z_rot[1] < 0: z_rot[1] = -z_rot[1]
        if z_rot[2] < 0: z_rot[2] = -z_rot[2]
        if (z_rot[2] > z_rot[1]):
            z_rot[1], z_rot[2] = z_rot[2], z_rot[1]
        if (z_rot[1] > z_rot[0]):
            z_rot[0], z_rot[1] = z_rot[1], z_rot[0]
        if (z_rot[2] > z_rot[1]):
            z_rot[1], z_rot[2] = z_rot[2], z_rot[1]
        return np.array([z_rot[1], z_rot[2], z_rot[0]])
        
    def plot_pf(self, col, orient_data, ax=None, mk='o', ann=False, ftsize=6):
        """Create the direct pole figure.

        :param ax: a reference to a pyplot ax to draw the poles.
        :param mk: marker used to plot the poles (disc by default).
        :param bool ann: Annotate the pole with the coordinates of the vector
            if True (False by default).
            
        """
        self.plot_pf_background(ax)
        cp_0, cp_1 = [], []
        colors = []
        for igr, g in enumerate(orient_data):
            if np.isnan(g).all() or np.all(g==0):
                continue
            
            gt = g.transpose()
            for i, hkl_plane in enumerate(self.poles):
                c = hkl_plane.normal()
                c_rot = gt.dot(c)
                color = col[igr]
                
                if self.axis == 'Z':
                    (h, v, u) = (0, 1, 2)
                elif self.axis == 'Y':
                    (h, v, u) = (0, 2, 1)
                else:
                    (h, v, u) = (1, 2, 0)
                    
                axis_rot = c_rot[[h, v, u]]
                # the direction to plot is given by c_dir[h,v,u]
                
                if axis_rot[2] < 0:
                    axis_rot *= -1  # make unit vector have z>0
                if self.proj == 'flat':
                    cp = axis_rot
                elif self.proj == 'stereo':
                    c = axis_rot + self.z
                    c /= c[2]  # SP'/SP = r/z with r=1
                    cp = c
                    # cp = np.cross(c, self.z)
                else:
                    raise ValueError('Error, unsupported projection type', self.proj)
                
                cp_0.append(cp[0])
                cp_1.append(cp[1])
                colors.append(color)
                # Next 3 lines are necessary in case c_dir[2]=0, as for Euler angles [45, 45, 0]
                if axis_rot[2] < 0.000001:
                    cp_0.append(-cp[0])
                    cp_1.append(-cp[1])
                    colors.append(color)
                    # ax.scatter(-cp[0], -cp[1], linewidth=0, c=color, marker='o', s=axis_rot)
        ax.scatter(cp_0, cp_1, c=colors, s=self.mksize, zorder=2)
                
        ax.axis([-1.1, 1.1, -1.1, 1.1])
        ax.axis('off')
        ax.set_title('{%s} direct %s projection' % (self.family, self.proj), fontsize = ftsize)
        
    def plot_sst_color(self, col, orient_data, ax=None, mk='s', \
                          ann=False, ftsize=6, phase = 0):
        """ Create the inverse pole figure in the unit standard triangle.
        :param ax: a reference to a pyplot ax to draw the poles.
        :param mk: marker used to plot the poles (square by default).
        :param bool ann: Annotate the pole with the coordinates of the vector if True (False by default).
        """
        system = None
        symmetry = self.lattice._symmetry
        if phase==0:
            sst_poles = [(0, 0, 1), (1, 0, 1), (1, 1, 1)]
            ax.axis([-0.05, 0.45, -0.05, 0.40])
            system = 'cubic'
        elif phase==1:
            sst_poles = [(0, 0, 1), (2, -1, 0), (1, 0, 0)]
            ax.axis([-0.05, 1.05, -0.05, 0.6])
            system = 'hexa'
        else:
            print('unssuported symmetry: %s' % symmetry)
        A = HklPlane(*sst_poles[0], lattice=self.lattice)
        B = HklPlane(*sst_poles[1], lattice=self.lattice)
        C = HklPlane(*sst_poles[2], lattice=self.lattice)
        if system == 'cubic':
            self.plot_line_between_crystal_dir(A.normal(), B.normal(), ax=ax, steps=int(1+(45/5)), col='k')
            self.plot_line_between_crystal_dir(B.normal(), C.normal(), ax=ax, steps=int(1+(35/5)), col='k')
            self.plot_line_between_crystal_dir(C.normal(), A.normal(), ax=ax, steps=int(1+(55/5)), col='k')
        elif system == 'hexa':
            self.plot_line_between_crystal_dir(A.normal(), B.normal(), ax=ax, steps=int(1+(90/5)), col='k')
            self.plot_line_between_crystal_dir(B.normal(), C.normal(), ax=ax, steps=int(1+(30/5)), col='k')
            self.plot_line_between_crystal_dir(C.normal(), A.normal(), ax=ax, steps=int(1+(90/5)), col='k')
        else:
            self.plot_line_between_crystal_dir(A.normal(), B.normal(), ax=ax, col='k')
            self.plot_line_between_crystal_dir(B.normal(), C.normal(), ax=ax, col='k')
            self.plot_line_between_crystal_dir(C.normal(), A.normal(), ax=ax, col='k')
        # display the 3 crystal axes
        poles = [A, B, C]
        v_align = ['top', 'top', 'bottom']
        for i in range(3):
            hkl = poles[i]
            c_dir = hkl.normal()
            c = c_dir + self.z
            c /= c[2]  # SP'/SP = r/z with r=1
            pole_str = '%d%d%d' % hkl.miller_indices()
            if phase==1:
                pole_str = '%d%d%d%d' % HklPlane.three_to_four_indices(*hkl.miller_indices())
            ax.annotate(pole_str, (c[0], c[1] - (2 * (i < 2) - 1) * 0.01), xycoords='data',
                        fontsize=8, horizontalalignment='center', verticalalignment=v_align[i])
        # now plot the sample axis
        cp_0, cp_1 = [], []
        colors = []
        for igr, g in enumerate(orient_data):
            if np.isnan(g).all() or np.all(g==0):
                continue
            # compute axis and apply SST symmetry
            if self.axis == 'Z':
                axis = self.z
            elif self.axis == 'Y':
                axis = self.y
            else:
                axis = self.x
                
            axis_rot = self.sst_symmetry(g.dot(axis))
            color = np.round(col[igr],5)
            if axis_rot[2] < 0:
                axis_rot *= -1  # make unit vector have z>0
            if self.proj == 'flat':
                cp = axis_rot
            elif self.proj == 'stereo':
                c = axis_rot + self.z
                c /= c[2]  # SP'/SP = r/z with r=1
                cp = c
                # cp = np.cross(c, self.z)
            else:
                raise ValueError('Error, unsupported projection type', self.proj)
            
            cp_0.append(cp[0])
            cp_1.append(cp[1])
            colors.append(color)
            # Next 3 lines are necessary in case c_dir[2]=0, as for Euler angles [45, 45, 0]
            if axis_rot[2] < 0.000001:
                cp_0.append(-cp[0])
                cp_1.append(-cp[1])
                colors.append(color)
                # ax.scatter(-cp[0], -cp[1], linewidth=0, c=color, marker='o', s=axis_rot)
        ax.scatter(cp_0, cp_1, c=colors, s=self.mksize, zorder=2)        
        ax.set_title('%s-axis SST inverse %s projection' % (self.axis, self.proj), fontsize = ftsize)
        plt.axis("off")
# =============================================================================
# Plot functions
# =============================================================================
def rot_mat_to_euler(rot_mat): 
    r = R.from_matrix(rot_mat)
    return r.as_euler('zxz')* 180/np.pi

def global_plots(lim_x, lim_y, strain_matrix, strain_matrixs, col, colx, coly,
                 match_rate, mat_global, spots_len, iR_pix, fR_pix,
                 model_direc, material_, material1_, match_rate_threshold=5, bins=30):
    if material_ == material1_:
        mu_sd = []
        mu_sdc = []
        for index in range(len(spots_len)):
            ### index for nans
            nan_index = np.where(match_rate[index][0] <= match_rate_threshold)[0]
            if index == 0:
                spots_len_plot = np.copy(spots_len[index][0])
                mr_plot = np.copy(match_rate[index][0])
                iR_pix_plot = np.copy(iR_pix[index][0])
                fR_pix_plot = np.copy(fR_pix[index][0])
                strain_matrix_plot = np.copy(strain_matrix[index][0])
                e11c = strain_matrix_plot[:,0,0]#.reshape((lim_x, lim_y))
                e22c = strain_matrix_plot[:,1,1]#.reshape((lim_x, lim_y))
                e33c = strain_matrix_plot[:,2,2]#.reshape((lim_x, lim_y))
                e12c = strain_matrix_plot[:,0,1]#.reshape((lim_x, lim_y))
                e13c = strain_matrix_plot[:,0,2]#.reshape((lim_x, lim_y))
                e23c = strain_matrix_plot[:,1,2]#.reshape((lim_x, lim_y))
                strain_matrixs_plot = np.copy(strain_matrixs[index][0])
                e11s = strain_matrixs_plot[:,0,0]#.reshape((lim_x, lim_y))
                e22s = strain_matrixs_plot[:,1,1]#.reshape((lim_x, lim_y))
                e33s = strain_matrixs_plot[:,2,2]#.reshape((lim_x, lim_y))
                e12s = strain_matrixs_plot[:,0,1]#.reshape((lim_x, lim_y))
                e13s = strain_matrixs_plot[:,0,2]#.reshape((lim_x, lim_y))
                e23s = strain_matrixs_plot[:,1,2]#.reshape((lim_x, lim_y))
                spots_len_plot[nan_index] = np.nan 
                mr_plot[nan_index] = np.nan 
                iR_pix_plot[nan_index] = np.nan 
                fR_pix_plot[nan_index] = np.nan 
                e11c[nan_index] = np.nan 
                e22c[nan_index] = np.nan 
                e33c[nan_index] = np.nan 
                e12c[nan_index] = np.nan 
                e13c[nan_index] = np.nan 
                e23c[nan_index] = np.nan 
                e11s[nan_index] = np.nan 
                e22s[nan_index] = np.nan 
                e33s[nan_index] = np.nan 
                e12s[nan_index] = np.nan 
                e13s[nan_index] = np.nan 
                e23s[nan_index] = np.nan 
                
            else:
                temp = np.copy(spots_len[index][0])
                temp[nan_index] = np.nan
                spots_len_plot = np.vstack((spots_len_plot,temp))
                
                temp = np.copy(match_rate[index][0])
                temp[nan_index] = np.nan
                mr_plot = np.vstack((mr_plot,temp))
                
                temp = np.copy(iR_pix[index][0])
                temp[nan_index] = np.nan
                iR_pix_plot = np.vstack((iR_pix_plot,temp))
        
                temp = np.copy(fR_pix[index][0])
                temp[nan_index] = np.nan
                fR_pix_plot = np.vstack((fR_pix_plot,temp))
                
                strain_matrix_plot = np.copy(strain_matrix[index][0])
                temp = np.copy(strain_matrix_plot[:,0,0])
                temp[nan_index] = np.nan
                e11c = np.vstack((e11c,temp))
                temp = np.copy(strain_matrix_plot[:,1,1])
                temp[nan_index] = np.nan
                e22c = np.vstack((e22c,temp))
                temp = np.copy(strain_matrix_plot[:,2,2])
                temp[nan_index] = np.nan
                e33c = np.vstack((e33c,temp))
                temp = np.copy(strain_matrix_plot[:,0,1])
                temp[nan_index] = np.nan
                e12c = np.vstack((e12c,temp))
                temp = np.copy(strain_matrix_plot[:,0,2])
                temp[nan_index] = np.nan
                e13c = np.vstack((e13c,temp))
                temp = np.copy(strain_matrix_plot[:,1,2])
                temp[nan_index] = np.nan
                e23c = np.vstack((e23c,temp))
                ##
                strain_matrixs_plot = np.copy(strain_matrixs[index][0])
                temp = np.copy(strain_matrixs_plot[:,0,0])
                temp[nan_index] = np.nan
                e11s = np.vstack((e11s,temp))
                temp = np.copy(strain_matrixs_plot[:,1,1])
                temp[nan_index] = np.nan
                e22s = np.vstack((e22s,temp))
                temp = np.copy(strain_matrixs_plot[:,2,2])
                temp[nan_index] = np.nan
                e33s = np.vstack((e33s,temp))
                temp = np.copy(strain_matrixs_plot[:,0,1])
                temp[nan_index] = np.nan
                e12s = np.vstack((e12s,temp))
                temp = np.copy(strain_matrixs_plot[:,0,2])
                temp[nan_index] = np.nan
                e13s = np.vstack((e13s,temp))
                temp = np.copy(strain_matrixs_plot[:,1,2])
                temp[nan_index] = np.nan
                e23s = np.vstack((e23s,temp))
        
        spots_len_plot = spots_len_plot.flatten()
        mr_plot = mr_plot.flatten()
        iR_pix_plot = iR_pix_plot.flatten()
        fR_pix_plot = fR_pix_plot.flatten() 
        e11c = e11c.flatten()
        e22c = e22c.flatten()
        e33c = e33c.flatten()
        e12c = e12c.flatten()
        e13c = e13c.flatten()
        e23c = e23c.flatten()
        e11s = e11s.flatten()
        e22s = e22s.flatten()
        e33s = e33s.flatten()
        e12s = e12s.flatten()
        e13s = e13s.flatten()
        e23s = e23s.flatten()
        
        spots_len_plot = spots_len_plot[~np.isnan(spots_len_plot)]
        mr_plot = mr_plot[~np.isnan(mr_plot)]
        iR_pix_plot = iR_pix_plot[~np.isnan(iR_pix_plot)]
        fR_pix_plot = fR_pix_plot[~np.isnan(fR_pix_plot)]
        e11c = e11c[~np.isnan(e11c)]
        e22c = e22c[~np.isnan(e22c)]
        e33c = e33c[~np.isnan(e33c)]
        e12c = e12c[~np.isnan(e12c)]
        e13c = e13c[~np.isnan(e13c)]
        e23c = e23c[~np.isnan(e23c)]
        e11s = e11s[~np.isnan(e11s)]
        e22s = e22s[~np.isnan(e22s)]
        e33s = e33s[~np.isnan(e33s)]
        e12s = e12s[~np.isnan(e12s)]
        e13s = e13s[~np.isnan(e13s)]
        e23s = e23s[~np.isnan(e23s)]
        
        try:
            title = "Number of spots and matching rate"
            fig = plt.figure()
            axs = fig.subplots(1, 2)
            axs[0].set_title("Number of spots", loc='center', fontsize=8)
            axs[0].hist(spots_len_plot, bins=bins)
            axs[0].set_ylabel('Frequency', fontsize=8)
            axs[0].tick_params(axis='both', which='major', labelsize=8)
            axs[0].tick_params(axis='both', which='minor', labelsize=8)
            axs[1].set_title("matching rate", loc='center', fontsize=8)
            axs[1].hist(mr_plot, bins=bins)
            axs[1].set_ylabel('Frequency', fontsize=8)
            axs[1].tick_params(axis='both', which='major', labelsize=8)
            axs[1].tick_params(axis='both', which='minor', labelsize=8)
            plt.tight_layout()
            plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
            plt.close(fig)
        except:
            pass
        try:
            title = "Initial and Final residues"
            fig = plt.figure()
            axs = fig.subplots(1, 2)
            axs[0].set_title("Initial residues", loc='center', fontsize=8)
            axs[0].hist(iR_pix_plot, bins=bins)
            axs[0].set_ylabel('Frequency', fontsize=8)
            axs[0].tick_params(axis='both', which='major', labelsize=8)
            axs[0].tick_params(axis='both', which='minor', labelsize=8)
            axs[1].set_title("Final residues", loc='center', fontsize=8)
            axs[1].hist(fR_pix_plot, bins=bins)
            axs[1].set_ylabel('Frequency', fontsize=8)
            axs[1].tick_params(axis='both', which='major', labelsize=8)
            axs[1].tick_params(axis='both', which='minor', labelsize=8)
            plt.tight_layout()
            plt.savefig(model_direc+ "//"+title+'.png',format='png', dpi=1000) 
            plt.close(fig)
        except:
            pass
        try:
            title = "strain Crystal reference"
            fig = plt.figure()
            fig.suptitle(title, fontsize=10)
            axs = fig.subplots(2, 3)
            axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
            logdata = e11c #np.log(e11c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[0, 0].axvline(x=estimated_mu, c="k")
            axs[0, 0].plot(x1, pdf, 'r')
            axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
            mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            axs[0, 0].set_ylabel('Frequency', fontsize=8)
            axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
            axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
            
            axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
            logdata = e22c #np.log(e22c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[0, 1].axvline(x=estimated_mu, c="k")
            axs[0, 1].plot(x1, pdf, 'r')
            axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
            mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            # axs[0, 1].hist(e22c, bins=bins)
            axs[0, 1].set_ylabel('Frequency', fontsize=8)
            axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
            axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
            
            axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
            logdata = e33c #np.log(e33c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[0, 2].axvline(x=estimated_mu, c="k")
            axs[0, 2].plot(x1, pdf, 'r')
            axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
            mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            # axs[0, 2].hist(e33c, bins=bins)
            axs[0, 2].set_ylabel('Frequency', fontsize=8)
            axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
            axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
            
            axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
            logdata = e12c#np.log(e12c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[1, 0].axvline(x=estimated_mu, c="k")
            axs[1, 0].plot(x1, pdf, 'r')
            axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
            mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            # axs[1, 0].hist(e12c, bins=bins)
            axs[1, 0].set_ylabel('Frequency', fontsize=8)
            axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
            axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
            
            axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
            logdata = e13c#np.log(e13c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[1, 1].axvline(x=estimated_mu, c="k")
            axs[1, 1].plot(x1, pdf, 'r')
            axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
            mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            # axs[1, 1].hist(e13c, bins=bins)
            axs[1, 1].set_ylabel('Frequency', fontsize=8)
            axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
            axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
            
            axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
            logdata = e23c#np.log(e23c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[1, 2].axvline(x=estimated_mu, c="k")
            axs[1, 2].plot(x1, pdf, 'r')
            axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
            mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            # axs[1, 2].hist(e23c, bins=bins)
            axs[1, 2].set_ylabel('Frequency', fontsize=8)
            axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
            axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
            plt.tight_layout()
            plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
            plt.close(fig)
        except:
            pass
    
        try:
            title = "strain Sample reference"
            fig = plt.figure()
            fig.suptitle(title, fontsize=10)
            axs = fig.subplots(2, 3)
            axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
            logdata = e11s #np.log(e11c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[0, 0].axvline(x=estimated_mu, c="k")
            axs[0, 0].plot(x1, pdf, 'r')
            axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
            # axs[0, 0].hist(e11s, bins=bins)
            axs[0, 0].set_ylabel('Frequency', fontsize=8)
            axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
            axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
            
            mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            
            axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
            logdata = e22s #np.log(e22c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[0, 1].axvline(x=estimated_mu, c="k")
            axs[0, 1].plot(x1, pdf, 'r')
            axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
            # axs[0, 1].hist(e22s, bins=bins)
            axs[0, 1].set_ylabel('Frequency', fontsize=8)
            axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
            axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
            
            mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            
            axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
            logdata = e33s #np.log(e33c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[0, 2].axvline(x=estimated_mu, c="k")
            axs[0, 2].plot(x1, pdf, 'r')
            axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
            # axs[0, 2].hist(e33s, bins=bins)
            axs[0, 2].set_ylabel('Frequency', fontsize=8)
            axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
            axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
            
            mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            
            axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
            logdata = e12s#np.log(e12c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[1, 0].axvline(x=estimated_mu, c="k")
            axs[1, 0].plot(x1, pdf, 'r')
            axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
            # axs[1, 0].hist(e12s, bins=bins)
            axs[1, 0].set_ylabel('Frequency', fontsize=8)
            axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
            axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
            
            mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            
            axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
            logdata = e13s#np.log(e13c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[1, 1].axvline(x=estimated_mu, c="k")
            axs[1, 1].plot(x1, pdf, 'r')
            axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
            # axs[1, 1].hist(e13s, bins=bins)
            axs[1, 1].set_ylabel('Frequency', fontsize=8)
            axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
            axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
            
            mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            
            axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
            logdata = e23s#np.log(e23c)
            xmin = logdata.min()
            xmax = logdata.max()
            x1 = np.linspace(xmin, xmax, 1000)
            estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
            pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
            axs[1, 2].axvline(x=estimated_mu, c="k")
            axs[1, 2].plot(x1, pdf, 'r')
            axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
            # axs[1, 2].hist(e23s, bins=bins)
            axs[1, 2].set_ylabel('Frequency', fontsize=8)
            axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
            axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
            
            mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
            
            plt.tight_layout()
            plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
            plt.close(fig)  
        except:
            pass
        
    else:
        mu_sd = []
        mu_sdc = []
        material_id = [material_, material1_]
        for matid in range(2):
            for index in range(len(spots_len)):
                ### index for nans
                nan_index1 = np.where(match_rate[index][0] <= match_rate_threshold)[0]
                mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
                nan_index = np.hstack((mat_id_index,nan_index1))
                nan_index = np.unique(nan_index)
                
                if index == 0:
                    spots_len_plot = np.copy(spots_len[index][0])
                    mr_plot = np.copy(match_rate[index][0])
                    iR_pix_plot = np.copy(iR_pix[index][0])
                    fR_pix_plot = np.copy(fR_pix[index][0])
                    strain_matrix_plot = np.copy(strain_matrix[index][0])
                    e11c = strain_matrix_plot[:,0,0]#.reshape((lim_x, lim_y))
                    e22c = strain_matrix_plot[:,1,1]#.reshape((lim_x, lim_y))
                    e33c = strain_matrix_plot[:,2,2]#.reshape((lim_x, lim_y))
                    e12c = strain_matrix_plot[:,0,1]#.reshape((lim_x, lim_y))
                    e13c = strain_matrix_plot[:,0,2]#.reshape((lim_x, lim_y))
                    e23c = strain_matrix_plot[:,1,2]#.reshape((lim_x, lim_y))
                    strain_matrixs_plot = np.copy(strain_matrixs[index][0])
                    e11s = strain_matrixs_plot[:,0,0]#.reshape((lim_x, lim_y))
                    e22s = strain_matrixs_plot[:,1,1]#.reshape((lim_x, lim_y))
                    e33s = strain_matrixs_plot[:,2,2]#.reshape((lim_x, lim_y))
                    e12s = strain_matrixs_plot[:,0,1]#.reshape((lim_x, lim_y))
                    e13s = strain_matrixs_plot[:,0,2]#.reshape((lim_x, lim_y))
                    e23s = strain_matrixs_plot[:,1,2]#.reshape((lim_x, lim_y))
                    spots_len_plot[nan_index] = np.nan 
                    mr_plot[nan_index] = np.nan 
                    iR_pix_plot[nan_index] = np.nan 
                    fR_pix_plot[nan_index] = np.nan 
                    e11c[nan_index] = np.nan 
                    e22c[nan_index] = np.nan 
                    e33c[nan_index] = np.nan 
                    e12c[nan_index] = np.nan 
                    e13c[nan_index] = np.nan 
                    e23c[nan_index] = np.nan 
                    e11s[nan_index] = np.nan 
                    e22s[nan_index] = np.nan 
                    e33s[nan_index] = np.nan 
                    e12s[nan_index] = np.nan 
                    e13s[nan_index] = np.nan 
                    e23s[nan_index] = np.nan 
                    
                else:
                    temp = np.copy(spots_len[index][0])
                    temp[nan_index] = np.nan
                    spots_len_plot = np.vstack((spots_len_plot,temp))
                    
                    temp = np.copy(match_rate[index][0])
                    temp[nan_index] = np.nan
                    mr_plot = np.vstack((mr_plot,temp))
                    
                    temp = np.copy(iR_pix[index][0])
                    temp[nan_index] = np.nan
                    iR_pix_plot = np.vstack((iR_pix_plot,temp))
            
                    temp = np.copy(fR_pix[index][0])
                    temp[nan_index] = np.nan
                    fR_pix_plot = np.vstack((fR_pix_plot,temp))
                    
                    strain_matrix_plot = np.copy(strain_matrix[index][0])
                    temp = np.copy(strain_matrix_plot[:,0,0])
                    temp[nan_index] = np.nan
                    e11c = np.vstack((e11c,temp))
                    temp = np.copy(strain_matrix_plot[:,1,1])
                    temp[nan_index] = np.nan
                    e22c = np.vstack((e22c,temp))
                    temp = np.copy(strain_matrix_plot[:,2,2])
                    temp[nan_index] = np.nan
                    e33c = np.vstack((e33c,temp))
                    temp = np.copy(strain_matrix_plot[:,0,1])
                    temp[nan_index] = np.nan
                    e12c = np.vstack((e12c,temp))
                    temp = np.copy(strain_matrix_plot[:,0,2])
                    temp[nan_index] = np.nan
                    e13c = np.vstack((e13c,temp))
                    temp = np.copy(strain_matrix_plot[:,1,2])
                    temp[nan_index] = np.nan
                    e23c = np.vstack((e23c,temp))
                    ##
                    strain_matrixs_plot = np.copy(strain_matrixs[index][0])
                    temp = np.copy(strain_matrixs_plot[:,0,0])
                    temp[nan_index] = np.nan
                    e11s = np.vstack((e11s,temp))
                    temp = np.copy(strain_matrixs_plot[:,1,1])
                    temp[nan_index] = np.nan
                    e22s = np.vstack((e22s,temp))
                    temp = np.copy(strain_matrixs_plot[:,2,2])
                    temp[nan_index] = np.nan
                    e33s = np.vstack((e33s,temp))
                    temp = np.copy(strain_matrixs_plot[:,0,1])
                    temp[nan_index] = np.nan
                    e12s = np.vstack((e12s,temp))
                    temp = np.copy(strain_matrixs_plot[:,0,2])
                    temp[nan_index] = np.nan
                    e13s = np.vstack((e13s,temp))
                    temp = np.copy(strain_matrixs_plot[:,1,2])
                    temp[nan_index] = np.nan
                    e23s = np.vstack((e23s,temp))
            
            spots_len_plot = spots_len_plot.flatten()
            mr_plot = mr_plot.flatten()
            iR_pix_plot = iR_pix_plot.flatten()
            fR_pix_plot = fR_pix_plot.flatten() 
            e11c = e11c.flatten()
            e22c = e22c.flatten()
            e33c = e33c.flatten()
            e12c = e12c.flatten()
            e13c = e13c.flatten()
            e23c = e23c.flatten()
            e11s = e11s.flatten()
            e22s = e22s.flatten()
            e33s = e33s.flatten()
            e12s = e12s.flatten()
            e13s = e13s.flatten()
            e23s = e23s.flatten()
            
            spots_len_plot = spots_len_plot[~np.isnan(spots_len_plot)]
            mr_plot = mr_plot[~np.isnan(mr_plot)]
            iR_pix_plot = iR_pix_plot[~np.isnan(iR_pix_plot)]
            fR_pix_plot = fR_pix_plot[~np.isnan(fR_pix_plot)]
            e11c = e11c[~np.isnan(e11c)]
            e22c = e22c[~np.isnan(e22c)]
            e33c = e33c[~np.isnan(e33c)]
            e12c = e12c[~np.isnan(e12c)]
            e13c = e13c[~np.isnan(e13c)]
            e23c = e23c[~np.isnan(e23c)]
            e11s = e11s[~np.isnan(e11s)]
            e22s = e22s[~np.isnan(e22s)]
            e33s = e33s[~np.isnan(e33s)]
            e12s = e12s[~np.isnan(e12s)]
            e13s = e13s[~np.isnan(e13s)]
            e23s = e23s[~np.isnan(e23s)]
            
            try:
                title = "Number of spots and matching rate"
                fig = plt.figure()
                axs = fig.subplots(1, 2)
                axs[0].set_title("Number of spots", loc='center', fontsize=8)
                axs[0].hist(spots_len_plot, bins=bins)
                axs[0].set_ylabel('Frequency', fontsize=8)
                axs[0].tick_params(axis='both', which='major', labelsize=8)
                axs[0].tick_params(axis='both', which='minor', labelsize=8)
                axs[1].set_title("matching rate", loc='center', fontsize=8)
                axs[1].hist(mr_plot, bins=bins)
                axs[1].set_ylabel('Frequency', fontsize=8)
                axs[1].tick_params(axis='both', which='major', labelsize=8)
                axs[1].tick_params(axis='both', which='minor', labelsize=8)
                plt.tight_layout()
                plt.savefig(model_direc+ "//"+title+"_"+material_id[matid]+'.png', format='png', dpi=1000) 
                plt.close(fig)
            except:
                pass
            
            try:
                title = "Initial and Final residues"
                fig = plt.figure()
                axs = fig.subplots(1, 2)
                axs[0].set_title("Initial residues", loc='center', fontsize=8)
                axs[0].hist(iR_pix_plot, bins=bins)
                axs[0].set_ylabel('Frequency', fontsize=8)
                axs[0].tick_params(axis='both', which='major', labelsize=8)
                axs[0].tick_params(axis='both', which='minor', labelsize=8)
                axs[1].set_title("Final residues", loc='center', fontsize=8)
                axs[1].hist(fR_pix_plot, bins=bins)
                axs[1].set_ylabel('Frequency', fontsize=8)
                axs[1].tick_params(axis='both', which='major', labelsize=8)
                axs[1].tick_params(axis='both', which='minor', labelsize=8)
                plt.tight_layout()
                plt.savefig(model_direc+ "//"+title+"_"+material_id[matid]+'.png',format='png', dpi=1000) 
                plt.close(fig)
            except:
                pass            
            
            try:
                title = "strain Crystal reference"+" "+material_id[matid]
                fig = plt.figure()
                fig.suptitle(title, fontsize=10)
                axs = fig.subplots(2, 3)
                axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
                logdata = e11c #np.log(e11c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[0, 0].axvline(x=estimated_mu, c="k")
                axs[0, 0].plot(x1, pdf, 'r')
                axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
                mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                axs[0, 0].set_ylabel('Frequency', fontsize=8)
                axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
                axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
                
                axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
                logdata = e22c #np.log(e22c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[0, 1].axvline(x=estimated_mu, c="k")
                axs[0, 1].plot(x1, pdf, 'r')
                axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
                mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                # axs[0, 1].hist(e22c, bins=bins)
                axs[0, 1].set_ylabel('Frequency', fontsize=8)
                axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
                axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
                
                axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
                logdata = e33c #np.log(e33c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[0, 2].axvline(x=estimated_mu, c="k")
                axs[0, 2].plot(x1, pdf, 'r')
                axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
                mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                # axs[0, 2].hist(e33c, bins=bins)
                axs[0, 2].set_ylabel('Frequency', fontsize=8)
                axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
                axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
                
                axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
                logdata = e12c#np.log(e12c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[1, 0].axvline(x=estimated_mu, c="k")
                axs[1, 0].plot(x1, pdf, 'r')
                axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
                mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                # axs[1, 0].hist(e12c, bins=bins)
                axs[1, 0].set_ylabel('Frequency', fontsize=8)
                axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
                axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
                
                axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
                logdata = e13c#np.log(e13c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[1, 1].axvline(x=estimated_mu, c="k")
                axs[1, 1].plot(x1, pdf, 'r')
                axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
                mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                # axs[1, 1].hist(e13c, bins=bins)
                axs[1, 1].set_ylabel('Frequency', fontsize=8)
                axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
                axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
                
                axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
                logdata = e23c#np.log(e23c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[1, 2].axvline(x=estimated_mu, c="k")
                axs[1, 2].plot(x1, pdf, 'r')
                axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[1, 2].hist(e23c, bins=bins)
                axs[1, 2].set_ylabel('Frequency', fontsize=8)
                axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
                axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
                mu_sdc.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                plt.tight_layout()
                plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
                plt.close(fig)
            except:
                pass
        
            try:
                title = "strain Sample reference"+" "+material_id[matid]
                fig = plt.figure()
                fig.suptitle(title, fontsize=10)
                axs = fig.subplots(2, 3)
                axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
                logdata = e11s #np.log(e11c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[0, 0].axvline(x=estimated_mu, c="k")
                axs[0, 0].plot(x1, pdf, 'r')
                axs[0, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[0, 0].hist(e11s, bins=bins)
                axs[0, 0].set_ylabel('Frequency', fontsize=8)
                axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
                axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
                
                mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                
                axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
                logdata = e22s #np.log(e22c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[0, 1].axvline(x=estimated_mu, c="k")
                axs[0, 1].plot(x1, pdf, 'r')
                axs[0, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[0, 1].hist(e22s, bins=bins)
                axs[0, 1].set_ylabel('Frequency', fontsize=8)
                axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
                axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
                
                mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                
                axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
                logdata = e33s #np.log(e33c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[0, 2].axvline(x=estimated_mu, c="k")
                axs[0, 2].plot(x1, pdf, 'r')
                axs[0, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[0, 2].hist(e33s, bins=bins)
                axs[0, 2].set_ylabel('Frequency', fontsize=8)
                axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
                axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
                
                mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                
                axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
                logdata = e12s#np.log(e12c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[1, 0].axvline(x=estimated_mu, c="k")
                axs[1, 0].plot(x1, pdf, 'r')
                axs[1, 0].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[1, 0].hist(e12s, bins=bins)
                axs[1, 0].set_ylabel('Frequency', fontsize=8)
                axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
                axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
                
                mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                
                axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
                logdata = e13s#np.log(e13c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[1, 1].axvline(x=estimated_mu, c="k")
                axs[1, 1].plot(x1, pdf, 'r')
                axs[1, 1].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[1, 1].hist(e13s, bins=bins)
                axs[1, 1].set_ylabel('Frequency', fontsize=8)
                axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
                axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
                
                mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                
                axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
                logdata = e23s#np.log(e23c)
                xmin = logdata.min()
                xmax = logdata.max()
                x1 = np.linspace(xmin, xmax, 1000)
                estimated_mu, estimated_sigma = scipy.stats.norm.fit(logdata)
                pdf = scipy.stats.norm.pdf(x1, loc=estimated_mu, scale=estimated_sigma)
                axs[1, 2].axvline(x=estimated_mu, c="k")
                axs[1, 2].plot(x1, pdf, 'r')
                axs[1, 2].hist(logdata, bins=bins, density=True, alpha=0.8)
                # axs[1, 2].hist(e23s, bins=bins)
                axs[1, 2].set_ylabel('Frequency', fontsize=8)
                axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
                axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
                
                mu_sd.append((estimated_mu-estimated_sigma, estimated_mu+estimated_sigma))
                
                plt.tight_layout()
                plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
                plt.close(fig)  
            except:
                pass
    
    if material_ == material1_:
        matid = 0
        for index in range(len(strain_matrix)):
            nan_index = np.where(match_rate[index][0] <= match_rate_threshold)[0]
        
            strain_matrix_plot = np.copy(strain_matrixs[index][0])
            strain_matrix_plot[nan_index,:,:] = np.nan             
        
            fig = plt.figure(figsize=(11.69,8.27), dpi=100)
            bottom, top = 0.1, 0.9
            left, right = 0.1, 0.8
            fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
            
            vmin, vmax = mu_sd[matid*6]
            axs = fig.subplots(2, 3)
            axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
            im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[0, 0].set_xticks([])
            axs[0, 0].set_yticks([])
            divider = make_axes_locatable(axs[0,0])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sd[matid*6+1]
            axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
            im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            divider = make_axes_locatable(axs[0,1])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sd[matid*6+2]
            axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
            im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            divider = make_axes_locatable(axs[0,2])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sd[matid*6+3]
            axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
            im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[1, 0].set_xticks([])
            axs[1, 0].set_yticks([])
            divider = make_axes_locatable(axs[1,0])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sd[matid*6+4]
            axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
            im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[1, 1].set_xticks([])
            divider = make_axes_locatable(axs[1,1])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sd[matid*6+5]
            axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
            im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[1, 2].set_xticks([]) 
            divider = make_axes_locatable(axs[1,2])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
        
            for ax in axs.flat:
                ax.label_outer()
        
            plt.savefig(model_direc+ '//figure_strain_UBsample_UB'+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
            plt.close(fig)
               
            strain_matrix_plot = np.copy(strain_matrix[index][0])
            strain_matrix_plot[nan_index,:,:] = np.nan             
        
            fig = plt.figure(figsize=(11.69,8.27), dpi=100)
            bottom, top = 0.1, 0.9
            left, right = 0.1, 0.8
            fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
            
            vmin, vmax = mu_sdc[matid*6]
            axs = fig.subplots(2, 3)
            axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
            im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[0, 0].set_xticks([])
            axs[0, 0].set_yticks([])
            divider = make_axes_locatable(axs[0,0])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sdc[matid*6+1]
            axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
            im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            divider = make_axes_locatable(axs[0,1])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sdc[matid*6+2]
            axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
            im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            divider = make_axes_locatable(axs[0,2])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sdc[matid*6+3]
            axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
            im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[1, 0].set_xticks([])
            axs[1, 0].set_yticks([])
            divider = make_axes_locatable(axs[1,0])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sdc[matid*6+4]
            axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
            im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[1, 1].set_xticks([])
            divider = make_axes_locatable(axs[1,1])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
            
            vmin, vmax = mu_sdc[matid*6+5]
            axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
            im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
            axs[1, 2].set_xticks([]) 
            divider = make_axes_locatable(axs[1,2])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
            cbar.ax.tick_params(labelsize=8) 
        
            for ax in axs.flat:
                ax.label_outer()
        
            plt.savefig(model_direc+ '//figure_strain_UBcrystal_UB'+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
            plt.close(fig)
            
            col_plot = np.copy(col[index][0])
            col_plot[nan_index,:] = 0,0,0
            col_plot = col_plot.reshape((lim_x, lim_y, 3))
        
            colx_plot = np.copy(colx[index][0])
            colx_plot[nan_index,:] = 0,0,0
            colx_plot = colx_plot.reshape((lim_x, lim_y,3))
            
            coly_plot = np.copy(coly[index][0])
            coly_plot[nan_index,:] = 0,0,0
            coly_plot = coly_plot.reshape((lim_x, lim_y,3))
            
            fig = plt.figure(figsize=(11.69,8.27), dpi=100)
            bottom, top = 0.1, 0.9
            left, right = 0.1, 0.8
            fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
        
            axs = fig.subplots(1, 3)
            axs[0].set_title(r"IPF Z map", loc='center', fontsize=8)
            axs[0].imshow(col_plot, origin='lower')
            axs[0].set_xticks([])
            axs[0].set_yticks([])
            
            axs[1].set_title(r"IPF Y map", loc='center', fontsize=8)
            axs[1].imshow(coly_plot, origin='lower')
            axs[1].set_xticks([])
            axs[1].set_yticks([])
            
            axs[2].set_title(r"IPF X map", loc='center', fontsize=8)
            im = axs[2].imshow(colx_plot, origin='lower')
            axs[2].set_xticks([])
            axs[2].set_yticks([])
        
            for ax in axs.flat:
                ax.label_outer()
        
            plt.savefig(model_direc+ '//IPF_map_UB'+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
            plt.close(fig)
            
            
            col_plot = np.copy(col[index][0])
            col_plot[nan_index,:] = 0,0,0
            col_plot = col_plot.reshape((lim_x, lim_y, 3))
        
            mr_plot = np.copy(match_rate[index][0])
            mr_plot[nan_index,:] = 0
            mr_plot = mr_plot.reshape((lim_x, lim_y))
            
            mat_glob = np.copy(mat_global[index][0])
            mat_glob[nan_index,:] = 0
            mat_glob = mat_glob.reshape((lim_x, lim_y))
            
            fig = plt.figure(figsize=(11.69,8.27), dpi=100)
            bottom, top = 0.1, 0.9
            left, right = 0.1, 0.8
            fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
        
            axs = fig.subplots(1, 3)
            axs[0].set_title(r"IPF Z map", loc='center', fontsize=8)
            axs[0].imshow(col_plot, origin='lower')
            axs[0].set_xticks([])
            axs[0].set_yticks([])
            
            axs[1].set_title(r"Material Index", loc='center', fontsize=8)
            im = axs[1].imshow(mat_glob, origin='lower', vmin=0, vmax=1)
            axs[1].set_xticks([])
            axs[1].set_yticks([])
            
            divider = make_axes_locatable(axs[1])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.colorbar(im, cax=cax, orientation='vertical')
            
            axs[2].set_title(r"Matching rate", loc='center', fontsize=8)
            im = axs[2].imshow(mr_plot, origin='lower', cmap=plt.cm.jet, vmin=0, vmax=100)
            axs[2].set_xticks([])
            axs[2].set_yticks([])
            
            divider = make_axes_locatable(axs[2])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.colorbar(im, cax=cax, orientation='vertical')
        
            for ax in axs.flat:
                ax.label_outer()
        
            plt.savefig(model_direc+ "//figure_global_UB"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
            plt.close(fig)
            
            spots_len_plot = np.copy(spots_len[index][0])
            spots_len_plot[nan_index,:] = 0
            spots_len_plot = spots_len_plot.reshape((lim_x, lim_y))
            
            iR_pix_plot = np.copy(iR_pix[index][0])
            iR_pix_plot[nan_index,:] = 0
            iR_pix_plot = iR_pix_plot.reshape((lim_x, lim_y))
            
            fR_pix_plot = np.copy(fR_pix[index][0])
            fR_pix_plot[nan_index,:] = 0
            fR_pix_plot = fR_pix_plot.reshape((lim_x, lim_y))
            
            fig = plt.figure(figsize=(11.69,8.27), dpi=100)
            bottom, top = 0.1, 0.9
            left, right = 0.1, 0.8
            fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
        
            axs = fig.subplots(1, 3)
            axs[0].set_title(r"Number of spots detected", loc='center', fontsize=8)
            im = axs[0].imshow(spots_len_plot, origin='lower', cmap=plt.cm.jet)
            axs[0].set_xticks([])
            axs[0].set_yticks([])
            
            divider = make_axes_locatable(axs[0])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.colorbar(im, cax=cax, orientation='vertical')
        
            axs[1].set_title(r"Initial pixel residues", loc='center', fontsize=8)
            im = axs[1].imshow(iR_pix_plot, origin='lower', cmap=plt.cm.jet)
            axs[1].set_xticks([])
            axs[1].set_yticks([])
            
            divider = make_axes_locatable(axs[1])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.colorbar(im, cax=cax, orientation='vertical')
        
            axs[2].set_title(r"Final pixel residues", loc='center', fontsize=8)
            im = axs[2].imshow(fR_pix_plot, origin='lower', cmap=plt.cm.jet)
            axs[2].set_xticks([])
            axs[2].set_yticks([])
            
            divider = make_axes_locatable(axs[2])
            cax = divider.append_axes('right', size='5%', pad=0.05)
            fig.colorbar(im, cax=cax, orientation='vertical')
        
            for ax in axs.flat:
                ax.label_outer()
        
            plt.savefig(model_direc+'//figure_mr_ir_fr_UB'+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
            plt.close(fig)
    else:    
    
        for matid in range(2):
            for index in range(len(strain_matrix)):
                nan_index1 = np.where(match_rate[index][0] <= match_rate_threshold)[0]
                mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
                nan_index = np.hstack((mat_id_index,nan_index1))
                nan_index = np.unique(nan_index)
            
                strain_matrix_plot = np.copy(strain_matrixs[index][0])
                strain_matrix_plot[nan_index,:,:] = np.nan             
            
                fig = plt.figure(figsize=(11.69,8.27), dpi=100)
                bottom, top = 0.1, 0.9
                left, right = 0.1, 0.8
                fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
                
                vmin, vmax = mu_sd[matid*6]
                axs = fig.subplots(2, 3)
                axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
                im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[0, 0].set_xticks([])
                axs[0, 0].set_yticks([])
                divider = make_axes_locatable(axs[0,0])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sd[matid*6+1]
                axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
                im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                divider = make_axes_locatable(axs[0,1])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sd[matid*6+2]
                axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
                im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                divider = make_axes_locatable(axs[0,2])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sd[matid*6+3]
                axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
                im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[1, 0].set_xticks([])
                axs[1, 0].set_yticks([])
                divider = make_axes_locatable(axs[1,0])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sd[matid*6+4]
                axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
                im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[1, 1].set_xticks([])
                divider = make_axes_locatable(axs[1,1])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sd[matid*6+5]
                axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
                im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[1, 2].set_xticks([]) 
                divider = make_axes_locatable(axs[1,2])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
            
                for ax in axs.flat:
                    ax.label_outer()
            
                plt.savefig(model_direc+ '//figure_strain_UBsample_mat'+str(matid)+"_UB"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
                plt.close(fig)
                   
                strain_matrix_plot = np.copy(strain_matrix[index][0])
                strain_matrix_plot[nan_index,:,:] = np.nan             
            
                fig = plt.figure(figsize=(11.69,8.27), dpi=100)
                bottom, top = 0.1, 0.9
                left, right = 0.1, 0.8
                fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
                
                vmin, vmax = mu_sdc[matid*6]
                axs = fig.subplots(2, 3)
                axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
                im=axs[0, 0].imshow(strain_matrix_plot[:,0,0].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[0, 0].set_xticks([])
                axs[0, 0].set_yticks([])
                divider = make_axes_locatable(axs[0,0])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sdc[matid*6+1]
                axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
                im=axs[0, 1].imshow(strain_matrix_plot[:,1,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                divider = make_axes_locatable(axs[0,1])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sdc[matid*6+2]
                axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
                im=axs[0, 2].imshow(strain_matrix_plot[:,2,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                divider = make_axes_locatable(axs[0,2])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sdc[matid*6+3]
                axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
                im=axs[1, 0].imshow(strain_matrix_plot[:,0,1].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[1, 0].set_xticks([])
                axs[1, 0].set_yticks([])
                divider = make_axes_locatable(axs[1,0])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sdc[matid*6+4]
                axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
                im=axs[1, 1].imshow(strain_matrix_plot[:,0,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[1, 1].set_xticks([])
                divider = make_axes_locatable(axs[1,1])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                
                vmin, vmax = mu_sdc[matid*6+5]
                axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
                im = axs[1, 2].imshow(strain_matrix_plot[:,1,2].reshape((lim_x, lim_y)), origin='lower', cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
                axs[1, 2].set_xticks([]) 
                divider = make_axes_locatable(axs[1,2])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = fig.colorbar(im, cax=cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
            
                for ax in axs.flat:
                    ax.label_outer()
            
                plt.savefig(model_direc+ '//figure_strain_UBcrystal_mat'+str(matid)+"_UB"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
                plt.close(fig)
            
                col_plot = np.copy(col[index][0])
                col_plot[nan_index,:] = 0,0,0
                col_plot = col_plot.reshape((lim_x, lim_y, 3))
            
                colx_plot = np.copy(colx[index][0])
                colx_plot[nan_index,:] = 0,0,0
                colx_plot = colx_plot.reshape((lim_x, lim_y,3))
                
                coly_plot = np.copy(coly[index][0])
                coly_plot[nan_index,:] = 0,0,0
                coly_plot = coly_plot.reshape((lim_x, lim_y,3))
                
                fig = plt.figure(figsize=(11.69,8.27), dpi=100)
                bottom, top = 0.1, 0.9
                left, right = 0.1, 0.8
                fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
            
                axs = fig.subplots(1, 3)
                axs[0].set_title(r"IPF Z map", loc='center', fontsize=8)
                axs[0].imshow(col_plot, origin='lower')
                axs[0].set_xticks([])
                axs[0].set_yticks([])
                
                axs[1].set_title(r"IPF Y map", loc='center', fontsize=8)
                axs[1].imshow(coly_plot, origin='lower')
                axs[1].set_xticks([])
                axs[1].set_yticks([])
                
                axs[2].set_title(r"IPF X map", loc='center', fontsize=8)
                im = axs[2].imshow(colx_plot, origin='lower')
                axs[2].set_xticks([])
                axs[2].set_yticks([])
            
                for ax in axs.flat:
                    ax.label_outer()
            
                plt.savefig(model_direc+ '//IPF_map_mat'+str(matid)+"_UB"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
                plt.close(fig)

                col_plot = np.copy(col[index][0])
                col_plot[nan_index,:] = 0,0,0
                col_plot = col_plot.reshape((lim_x, lim_y, 3))
            
                mr_plot = np.copy(match_rate[index][0])
                mr_plot[nan_index,:] = 0
                mr_plot = mr_plot.reshape((lim_x, lim_y))
                
                mat_glob = np.copy(mat_global[index][0])
                mat_glob[nan_index,:] = 0
                mat_glob = mat_glob.reshape((lim_x, lim_y))
                
                fig = plt.figure(figsize=(11.69,8.27), dpi=100)
                bottom, top = 0.1, 0.9
                left, right = 0.1, 0.8
                fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
            
                axs = fig.subplots(1, 3)
                axs[0].set_title(r"IPF Z map", loc='center', fontsize=8)
                axs[0].imshow(col_plot, origin='lower')
                axs[0].set_xticks([])
                axs[0].set_yticks([])
                
                axs[1].set_title(r"Material Index", loc='center', fontsize=8)
                im = axs[1].imshow(mat_glob, origin='lower', vmin=0, vmax=2)
                axs[1].set_xticks([])
                axs[1].set_yticks([])
                
                divider = make_axes_locatable(axs[1])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                fig.colorbar(im, cax=cax, orientation='vertical')
                
                axs[2].set_title(r"Matching rate", loc='center', fontsize=8)
                im = axs[2].imshow(mr_plot, origin='lower', cmap=plt.cm.jet, vmin=0, vmax=100)
                axs[2].set_xticks([])
                axs[2].set_yticks([])
                
                divider = make_axes_locatable(axs[2])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                fig.colorbar(im, cax=cax, orientation='vertical')
            
                for ax in axs.flat:
                    ax.label_outer()
            
                plt.savefig(model_direc+ "//figure_global_mat"+str(matid)+"_UB"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
                plt.close(fig)
                
                spots_len_plot = np.copy(spots_len[index][0])
                spots_len_plot[nan_index,:] = 0
                spots_len_plot = spots_len_plot.reshape((lim_x, lim_y))
                
                iR_pix_plot = np.copy(iR_pix[index][0])
                iR_pix_plot[nan_index,:] = 0
                iR_pix_plot = iR_pix_plot.reshape((lim_x, lim_y))
                
                fR_pix_plot = np.copy(fR_pix[index][0])
                fR_pix_plot[nan_index,:] = 0
                fR_pix_plot = fR_pix_plot.reshape((lim_x, lim_y))
                
                fig = plt.figure(figsize=(11.69,8.27), dpi=100)
                bottom, top = 0.1, 0.9
                left, right = 0.1, 0.8
                fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right, hspace=0.15, wspace=0.25)
            
                axs = fig.subplots(1, 3)
                axs[0].set_title(r"Number of spots detected", loc='center', fontsize=8)
                im = axs[0].imshow(spots_len_plot, origin='lower', cmap=plt.cm.jet)
                axs[0].set_xticks([])
                axs[0].set_yticks([])
                
                divider = make_axes_locatable(axs[0])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                fig.colorbar(im, cax=cax, orientation='vertical')
            
                axs[1].set_title(r"Initial pixel residues", loc='center', fontsize=8)
                im = axs[1].imshow(iR_pix_plot, origin='lower', cmap=plt.cm.jet)
                axs[1].set_xticks([])
                axs[1].set_yticks([])
                
                divider = make_axes_locatable(axs[1])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                fig.colorbar(im, cax=cax, orientation='vertical')
            
                axs[2].set_title(r"Final pixel residues", loc='center', fontsize=8)
                im = axs[2].imshow(fR_pix_plot, origin='lower', cmap=plt.cm.jet)
                axs[2].set_xticks([])
                axs[2].set_yticks([])
                
                divider = make_axes_locatable(axs[2])
                cax = divider.append_axes('right', size='5%', pad=0.05)
                fig.colorbar(im, cax=cax, orientation='vertical')
            
                for ax in axs.flat:
                    ax.label_outer()
            
                plt.savefig(model_direc+'//figure_mr_ir_fr_mat'+str(matid)+"_UB"+str(index)+'.png', bbox_inches='tight',format='png', dpi=1000) 
                plt.close(fig)
                
def sst_texture(orient_data=None, col_array=None, direc="", symmetry=None, symmetry_name=None, lattice=None,
                axis="Z", fn=""):
    
    print("symmetry of the current phase is : "+symmetry_name)
    
    if np.max(col_array) > 1:
        col_array[np.where(col_array>1)]=1
        
    fig = plt.figure(1)
    if symmetry_name == "cubic":
        pole_hkls = ['111','110','100']            
        ax1 = fig.add_subplot(221, aspect='equal')
        ax2 = fig.add_subplot(222, aspect='equal')
        ax3 = fig.add_subplot(223, aspect='equal')
        ax4 = fig.add_subplot(224, aspect='equal')
    elif symmetry_name == "hexagonal":
        pole_hkls = ['001','100','101','102','110']
        ax1 = fig.add_subplot(231, aspect='equal')
        ax2 = fig.add_subplot(232, aspect='equal')
        ax3 = fig.add_subplot(233, aspect='equal')
        ax4 = fig.add_subplot(234, aspect='equal')
        ax5 = fig.add_subplot(235, aspect='equal')
        ax6 = fig.add_subplot(236, aspect='equal')
    else:
        print("PF and IPF plots are only supported for Cubic and Hexagonal systems for now")
        return
    
    for pfs in range(len(pole_hkls)):
        pf1 = PoleFigure(hkl=pole_hkls[pfs], proj='stereo', lattice=lattice, axis=axis)     
        pf1.mksize = 1.
        if pfs == 0:
            pf1.plot_pf(col_array, orient_data, ax=ax1, ftsize=6)
        elif pfs == 1:
            pf1.plot_pf(col_array, orient_data, ax=ax2, ftsize=6)
        elif pfs == 2:
            pf1.plot_pf(col_array, orient_data, ax=ax3, ftsize=6)                    
        elif pfs == 3:
            pf1.plot_pf(col_array, orient_data, ax=ax4, ftsize=6)
        elif pfs == 4:
            pf1.plot_pf(col_array, orient_data, ax=ax5, ftsize=6)                    
    if symmetry_name == "cubic":
        pf1.plot_sst_color(col_array, orient_data, ax=ax4, ftsize=6, phase=0)
    elif symmetry_name == "hexagonal":
        pf1.plot_sst_color(col_array, orient_data, ax=ax6, ftsize=6, phase=1)
    plt.savefig(direc+"//PF_IPF_"+fn+".png", bbox_inches='tight',format='png', dpi=1000)
    plt.close() 
    
def save_sst(lim_x, lim_y, strain_matrix, strain_matrixs, col, colx, coly,
                      match_rate, mat_global, spots_len, iR_pix, fR_pix,
                      model_direc, material_, material1_, lattice_, lattice1_, 
                      symmetry_, symmetry1_, rotation_matrix1, symmetry_name, symmetry1_name,
                      mac_axis = [0., 0., 1.],axis_text="Z",match_rate_threshold = 5):

    rotation_matrix_sst = [[] for i in range(len(rotation_matrix1))]
    for i in range(len(rotation_matrix1)):
        rotation_matrix_sst[i].append(np.zeros((lim_x*lim_y,3,3)))
        
    for i in range(len(rotation_matrix1)):
        temp_mat = rotation_matrix1[i][0]
        for j in range(len(temp_mat)):
            orientation_matrix123 = temp_mat[j,:,:]
            # ## rotate orientation by 40degrees to bring in Sample RF
            omega = np.deg2rad(-40.0)
            # rotation de -omega autour de l'axe x (or Y?) pour repasser dans Rsample
            cw = np.cos(omega)
            sw = np.sin(omega)
            mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]])
            orientation_matrix123 = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix123)
            if np.linalg.det(orientation_matrix123) < 0:
                orientation_matrix123 = -orientation_matrix123
            rotation_matrix_sst[i][0][j,:,:] = orientation_matrix123
    
    rangeval = len(match_rate)
    if material_ == material1_:
        for index in range(rangeval):
            ### index for nans
            nan_index = np.where(match_rate[index][0] <= match_rate_threshold)[0]
            if index == 0:
                rotation_matrix_plot = np.copy(rotation_matrix_sst[index][0])
                col_plot = np.copy(col[index][0])
                col_plot[nan_index,:] = np.nan 
                rotation_matrix_plot[nan_index,:,:] = np.nan 
                
                sst_texture(orient_data=rotation_matrix_plot, 
                            col_array=col_plot, 
                            direc=model_direc, 
                            symmetry=symmetry_, 
                            symmetry_name = symmetry_name,
                            lattice=lattice_, axis=axis_text, fn="UB_"+str(index))
            else:
                tempori = np.copy(rotation_matrix_sst[index][0])
                tempori[nan_index,:,:] = np.nan
                rotation_matrix_plot = np.vstack((rotation_matrix_plot,tempori))
                tempcol = np.copy(col[index][0])
                tempcol[nan_index,:] = np.nan
                col_plot = np.vstack((col_plot,tempcol))   
                
                sst_texture(orient_data=tempori, 
                            col_array=tempcol, 
                            direc=model_direc, 
                            symmetry=symmetry_, 
                            symmetry_name = symmetry_name,
                            lattice=lattice_, axis=axis_text, fn="UB_"+str(index))
        ### Plot pole figures and IPF (cubic and hexagonal are supported for now)
        sst_texture(orient_data=rotation_matrix_plot, 
                    col_array=col_plot, 
                    direc=model_direc, 
                    symmetry=symmetry_, 
                    symmetry_name = symmetry_name,
                    lattice=lattice_, axis=axis_text, fn="all_UBs")
    else:
        for matid in range(2):
            if matid == 0:
                symmetry_name_plot = symmetry_name
                symmetry_plot = symmetry_
                lattice_plot = lattice_
            else:
                symmetry_name_plot = symmetry1_name
                symmetry_plot = symmetry1_
                lattice_plot = lattice1_
            
            for index in range(rangeval):
                ### index for nans
                nan_index1 = np.where(match_rate[index][0] <= match_rate_threshold)[0]
                mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
                nan_index = np.hstack((mat_id_index,nan_index1))
                nan_index = np.unique(nan_index)
                if index == 0:
                    rotation_matrix_plot = np.copy(rotation_matrix_sst[index][0])
                    rotation_matrix_plot[nan_index,:,:] = np.nan 
                    col_plot = np.copy(col[index][0])
                    col_plot[nan_index,:] = np.nan
                    
                    sst_texture(orient_data=rotation_matrix_plot, 
                                col_array=col_plot, 
                                direc=model_direc, 
                                symmetry=symmetry_plot, 
                                symmetry_name = symmetry_name_plot,
                                lattice=lattice_plot, axis=axis_text, fn="mat_"+str(matid)+"_UB_"+str(index))
                else:
                    tempori = np.copy(rotation_matrix_sst[index][0])
                    tempori[nan_index,:,:] = np.nan
                    rotation_matrix_plot = np.vstack((rotation_matrix_plot,tempori))
                    tempcol = np.copy(col[index][0])
                    tempcol[nan_index,:] = np.nan
                    col_plot = np.vstack((col_plot,tempcol))
                    
                    sst_texture(orient_data=tempori, 
                                col_array=tempcol, 
                                direc=model_direc, 
                                symmetry=symmetry_plot, 
                                symmetry_name = symmetry_name_plot,
                                lattice=lattice_plot, axis=axis_text, fn="mat_"+str(matid)+"_UB_"+str(index))
                    
            sst_texture(orient_data=rotation_matrix_plot, 
                            col_array=col_plot, 
                            direc=model_direc, 
                            symmetry=symmetry_plot, 
                            symmetry_name = symmetry_name_plot,
                            lattice=lattice_plot, axis=axis_text, fn="mat_"+str(matid)+"_all_UBs")

# =============================================================================
# IN DEVELOPMENT
# =============================================================================
# def calculate_subsets(orient_matrix, lattice, hkls_list, angle=5., mac_axis = [0., 0., 1.]):      
#     e_omega = np.cos(np.deg2rad(angle)) # Dispersion en degres (cone:1/2 angle)    
#     vectdiff = mac_axis  ## macroscopic axis  
#     hkls = hkls_list
#     phaseu = lattice
#     ngrain = len(orient_matrix)
#     # =============================================================================
#     indices_grains = {}
#     ############# INTEGRATION
#     for iipol in range(len(hkls)):
#         poles = phaseu.get_hkl_family(hkls[iipol])
#         nplan = len(poles)
#         normale_cx = np.zeros((3,nplan))
#         normale = np.zeros((3,nplan,ngrain))       
#         for i, hkl_plane in enumerate(poles):
#             normale_cx[:,i] = hkl_plane.normal()
            
#         ind_temp = []
#         for ig in range(ngrain):
#             Qt = orient_matrix[ig,:,:]
#             if np.any(np.isnan(Qt)):
#                 continue
#             for ip in range(nplan):
#                 normale[:,ip,ig] = np.dot(Qt,normale_cx[:,ip])
#                 prodscal = np.dot(normale[:,ip,ig], vectdiff[:])
#                 if (abs(prodscal) >= e_omega):
#                     ind_temp.append(ig)
#         indices_grains[str(hkls[iipol])] = list(np.unique(ind_temp))
#     return indices_grains

# def save_hkl_stats(lim_x, lim_y, strain_matrix, strain_matrixs, col, colx, coly,
#                       match_rate, mat_global, spots_len, iR_pix, fR_pix,
#                       model_direc, material_, material1_, lattice_, lattice1_, 
#                       symmetry_, symmetry1_, rotation_matrix1,
#                       hkls_list=None, angle=5., mac_axis = [0., 0., 1.],axis_text="Z"):
    
#     rotation_matrix = [[] for i in range(len(rotation_matrix1))]
#     for i in range(len(rotation_matrix1)):
#         rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
        
#     for i in range(len(rotation_matrix1)):
#         temp_mat = rotation_matrix1[i][0]
#         for j in range(len(temp_mat)):
#             orientation_matrix = temp_mat[j,:,:]
#             # ## rotate orientation by 40degrees to bring in Sample RF
#             omega = np.deg2rad(-40.0)
#             # rotation de -omega autour de l'axe x (or Y?) pour repasser dans Rsample
#             cw = np.cos(omega)
#             sw = np.sin(omega)
#             mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]])
#             orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
#             if np.linalg.det(orientation_matrix) < 0:
#                 orientation_matrix = -orientation_matrix
#             rotation_matrix[i][0][j,:,:] = orientation_matrix
    
#     rangeval = len(match_rate)
#     material_id = [material_, material1_]
#     if material_ == material1_:
#         for index in range(rangeval):
#             ### index for nans
#             nan_index = np.where(match_rate[index][0] == 0)[0]
#             if index == 0:
#                 rotation_matrix_plot = np.copy(rotation_matrix[index][0])
#                 col_plot = np.copy(col[index][0])
#                 col_plot[nan_index] = np.nan 
#                 rotation_matrix_plot[nan_index] = np.nan 
#             else:
#                 temp = np.copy(rotation_matrix[index][0])
#                 temp[nan_index] = np.nan
#                 rotation_matrix_plot = np.vstack((rotation_matrix_plot,temp))
#                 temp = np.copy(col[index][0])
#                 temp[nan_index] = np.nan
#                 col_plot = np.vstack((col_plot,temp))
#         index_list = calculate_subsets(rotation_matrix_plot, lattice_, hkls_list, angle=angle, mac_axis = mac_axis)
#     else:
#         for matid in range(2):
#             for index in range(rangeval):
#                 ### index for nans
#                 nan_index1 = np.where(match_rate[index][0] == 0)[0]
#                 mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
#                 nan_index = np.hstack((mat_id_index,nan_index1))
#                 nan_index = np.unique(nan_index)
#                 if index == 0:
#                     rotation_matrix_plot = np.copy(rotation_matrix[index][0])
#                     rotation_matrix_plot[nan_index] = np.nan 
#                     col_plot = np.copy(col[index][0])
#                     col_plot[nan_index] = np.nan 
#                 else:
#                     temp = np.copy(rotation_matrix[index][0])
#                     temp[nan_index] = np.nan
#                     rotation_matrix_plot = np.vstack((rotation_matrix_plot,temp))
#                     temp = np.copy(col[index][0])
#                     temp[nan_index] = np.nan
#                     col_plot = np.vstack((col_plot,temp))
#             if matid == 0:
#                 index_list = calculate_subsets(rotation_matrix_plot, lattice_, hkls_list, angle=angle, mac_axis = mac_axis)
#             elif matid == 1:
#                 index_list1 = calculate_subsets(rotation_matrix_plot, lattice1_, hkls_list, angle=angle, mac_axis = mac_axis)
    
#     for hkl_ind in index_list:    
#         if material_ == material1_:
#             index_allowed = index_list[hkl_ind]
#             if len(index_allowed) == 0:
#                 continue
            
#             count = 0
#             for index in range(rangeval):            
#                 bins = 20
#                 ### index for nans
#                 nan_index = np.where(match_rate[index][0] == 0)[0]
#                 if count == 0:
#                     spots_len_plot = np.copy(spots_len[index][0])
#                     mr_plot = np.copy(match_rate[index][0])
#                     iR_pix_plot = np.copy(iR_pix[index][0])
#                     fR_pix_plot = np.copy(fR_pix[index][0])
#                     strain_matrix_plot = np.copy(strain_matrix[index][0])
#                     e11c = strain_matrix_plot[:,0,0]#.reshape((lim_x, lim_y))
#                     e22c = strain_matrix_plot[:,1,1]#.reshape((lim_x, lim_y))
#                     e33c = strain_matrix_plot[:,2,2]#.reshape((lim_x, lim_y))
#                     e12c = strain_matrix_plot[:,0,1]#.reshape((lim_x, lim_y))
#                     e13c = strain_matrix_plot[:,0,2]#.reshape((lim_x, lim_y))
#                     e23c = strain_matrix_plot[:,1,2]#.reshape((lim_x, lim_y))
#                     strain_matrixs_plot = np.copy(strain_matrixs[index][0])
#                     e11s = strain_matrixs_plot[:,0,0]#.reshape((lim_x, lim_y))
#                     e22s = strain_matrixs_plot[:,1,1]#.reshape((lim_x, lim_y))
#                     e33s = strain_matrixs_plot[:,2,2]#.reshape((lim_x, lim_y))
#                     e12s = strain_matrixs_plot[:,0,1]#.reshape((lim_x, lim_y))
#                     e13s = strain_matrixs_plot[:,0,2]#.reshape((lim_x, lim_y))
#                     e23s = strain_matrixs_plot[:,1,2]#.reshape((lim_x, lim_y))
#                     spots_len_plot[nan_index] = np.nan 
#                     mr_plot[nan_index] = np.nan 
#                     iR_pix_plot[nan_index] = np.nan 
#                     fR_pix_plot[nan_index] = np.nan 
#                     e11c[nan_index] = np.nan 
#                     e22c[nan_index] = np.nan 
#                     e33c[nan_index] = np.nan 
#                     e12c[nan_index] = np.nan 
#                     e13c[nan_index] = np.nan 
#                     e23c[nan_index] = np.nan 
#                     e11s[nan_index] = np.nan 
#                     e22s[nan_index] = np.nan 
#                     e33s[nan_index] = np.nan 
#                     e12s[nan_index] = np.nan 
#                     e13s[nan_index] = np.nan 
#                     e23s[nan_index] = np.nan 
#                     count = 1
                    
#                 else:
#                     temp = np.copy(spots_len[index][0])
#                     temp[nan_index] = np.nan
#                     spots_len_plot = np.vstack((spots_len_plot,temp))
                    
#                     temp = np.copy(match_rate[index][0])
#                     temp[nan_index] = np.nan
#                     mr_plot = np.vstack((mr_plot,temp))
                    
#                     temp = np.copy(iR_pix[index][0])
#                     temp[nan_index] = np.nan
#                     iR_pix_plot = np.vstack((iR_pix_plot,temp))
            
#                     temp = np.copy(fR_pix[index][0])
#                     temp[nan_index] = np.nan
#                     fR_pix_plot = np.vstack((fR_pix_plot,temp))
                    
#                     strain_matrix_plot = np.copy(strain_matrix[index][0])
#                     temp = np.copy(strain_matrix_plot[:,0,0])
#                     temp[nan_index] = np.nan
#                     e11c = np.vstack((e11c,temp))
#                     temp = np.copy(strain_matrix_plot[:,1,1])
#                     temp[nan_index] = np.nan
#                     e22c = np.vstack((e22c,temp))
#                     temp = np.copy(strain_matrix_plot[:,2,2])
#                     temp[nan_index] = np.nan
#                     e33c = np.vstack((e33c,temp))
#                     temp = np.copy(strain_matrix_plot[:,0,1])
#                     temp[nan_index] = np.nan
#                     e12c = np.vstack((e12c,temp))
#                     temp = np.copy(strain_matrix_plot[:,0,2])
#                     temp[nan_index] = np.nan
#                     e13c = np.vstack((e13c,temp))
#                     temp = np.copy(strain_matrix_plot[:,1,2])
#                     temp[nan_index] = np.nan
#                     e23c = np.vstack((e23c,temp))
#                     ##
#                     strain_matrixs_plot = np.copy(strain_matrixs[index][0])
#                     temp = np.copy(strain_matrixs_plot[:,0,0])
#                     temp[nan_index] = np.nan
#                     e11s = np.vstack((e11s,temp))
#                     temp = np.copy(strain_matrixs_plot[:,1,1])
#                     temp[nan_index] = np.nan
#                     e22s = np.vstack((e22s,temp))
#                     temp = np.copy(strain_matrixs_plot[:,2,2])
#                     temp[nan_index] = np.nan
#                     e33s = np.vstack((e33s,temp))
#                     temp = np.copy(strain_matrixs_plot[:,0,1])
#                     temp[nan_index] = np.nan
#                     e12s = np.vstack((e12s,temp))
#                     temp = np.copy(strain_matrixs_plot[:,0,2])
#                     temp[nan_index] = np.nan
#                     e13s = np.vstack((e13s,temp))
#                     temp = np.copy(strain_matrixs_plot[:,1,2])
#                     temp[nan_index] = np.nan
#                     e23s = np.vstack((e23s,temp))
            
#             spots_len_plot = spots_len_plot.flatten()
#             mr_plot = mr_plot.flatten()
#             iR_pix_plot = iR_pix_plot.flatten()
#             fR_pix_plot = fR_pix_plot.flatten() 
#             e11c = e11c.flatten()
#             e22c = e22c.flatten()
#             e33c = e33c.flatten()
#             e12c = e12c.flatten()
#             e13c = e13c.flatten()
#             e23c = e23c.flatten()
#             e11s = e11s.flatten()
#             e22s = e22s.flatten()
#             e33s = e33s.flatten()
#             e12s = e12s.flatten()
#             e13s = e13s.flatten()
#             e23s = e23s.flatten()
            
#             spots_len_plot = spots_len_plot[index_allowed]
#             mr_plot = mr_plot[index_allowed]
#             iR_pix_plot = iR_pix_plot[index_allowed]
#             fR_pix_plot = fR_pix_plot[index_allowed]
#             e11c = e11c[index_allowed]
#             e22c = e22c[index_allowed]
#             e33c = e33c[index_allowed]
#             e12c = e12c[index_allowed]
#             e13c = e13c[index_allowed]
#             e23c = e23c[index_allowed]
#             e11s = e11s[index_allowed]
#             e22s = e22s[index_allowed]
#             e33s = e33s[index_allowed]
#             e12s = e12s[index_allowed]
#             e13s = e13s[index_allowed]
#             e23s = e23s[index_allowed]
            
#             try:
#                 title = "Number of spots and matching rate "+hkl_ind
#                 fig = plt.figure()
#                 axs = fig.subplots(1, 2)
#                 axs[0].set_title("Number of spots", loc='center', fontsize=8)
#                 axs[0].hist(spots_len_plot, bins=bins)
#                 axs[0].set_ylabel('Frequency', fontsize=8)
#                 axs[0].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0].tick_params(axis='both', which='minor', labelsize=8)
#                 axs[1].set_title("matching rate", loc='center', fontsize=8)
#                 axs[1].hist(mr_plot, bins=bins)
#                 axs[1].set_ylabel('Frequency', fontsize=8)
#                 axs[1].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1].tick_params(axis='both', which='minor', labelsize=8)
#                 plt.tight_layout()
#                 plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
#                 plt.close(fig)
#             except:
#                 pass
#             try:
#                 title = "Initial and Final residues "+hkl_ind
#                 fig = plt.figure()
#                 axs = fig.subplots(1, 2)
#                 axs[0].set_title("Initial residues", loc='center', fontsize=8)
#                 axs[0].hist(iR_pix_plot, bins=bins)
#                 axs[0].set_ylabel('Frequency', fontsize=8)
#                 axs[0].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0].tick_params(axis='both', which='minor', labelsize=8)
#                 axs[1].set_title("Final residues", loc='center', fontsize=8)
#                 axs[1].hist(fR_pix_plot, bins=bins)
#                 axs[1].set_ylabel('Frequency', fontsize=8)
#                 axs[1].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1].tick_params(axis='both', which='minor', labelsize=8)
#                 plt.tight_layout()
#                 plt.savefig(model_direc+ "//"+title+'.png',format='png', dpi=1000) 
#                 plt.close(fig)
#             except:
#                 pass
#             try:
#                 title = "strain Crystal reference "+hkl_ind
#                 fig = plt.figure()
#                 axs = fig.subplots(2, 3)
#                 axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
#                 axs[0, 0].hist(e11c, bins=bins)
#                 axs[0, 0].set_ylabel('Frequency', fontsize=8)
#                 axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
#                 axs[0, 1].hist(e22c, bins=bins)
#                 axs[0, 1].set_ylabel('Frequency', fontsize=8)
#                 axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
#                 axs[0, 2].hist(e33c, bins=bins)
#                 axs[0, 2].set_ylabel('Frequency', fontsize=8)
#                 axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
#                 axs[1, 0].hist(e12c, bins=bins)
#                 axs[1, 0].set_ylabel('Frequency', fontsize=8)
#                 axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
#                 axs[1, 1].hist(e13c, bins=bins)
#                 axs[1, 1].set_ylabel('Frequency', fontsize=8)
#                 axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
#                 axs[1, 2].hist(e23c, bins=bins)
#                 axs[1, 2].set_ylabel('Frequency', fontsize=8)
#                 axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
#                 plt.tight_layout()
#                 plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
#                 plt.close(fig)
#             except:
#                 pass
#             try:
#                 title = "strain Sample reference "+hkl_ind
#                 fig = plt.figure()
#                 axs = fig.subplots(2, 3)
#                 axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
#                 axs[0, 0].hist(e11s, bins=bins)
#                 axs[0, 0].set_ylabel('Frequency', fontsize=8)
#                 axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
#                 axs[0, 1].hist(e22s, bins=bins)
#                 axs[0, 1].set_ylabel('Frequency', fontsize=8)
#                 axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
#                 axs[0, 2].hist(e33s, bins=bins)
#                 axs[0, 2].set_ylabel('Frequency', fontsize=8)
#                 axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
#                 axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
#                 axs[1, 0].hist(e12s, bins=bins)
#                 axs[1, 0].set_ylabel('Frequency', fontsize=8)
#                 axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
#                 axs[1, 1].hist(e13s, bins=bins)
#                 axs[1, 1].set_ylabel('Frequency', fontsize=8)
#                 axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
                
#                 axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
#                 axs[1, 2].hist(e23s, bins=bins)
#                 axs[1, 2].set_ylabel('Frequency', fontsize=8)
#                 axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
#                 axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
#                 plt.tight_layout()
#                 plt.savefig(model_direc+ "//"+title+'.png', format='png', dpi=1000) 
#                 plt.close(fig)  
#             except:
#                 pass
            
#         else:
#             material_id = [material_, material1_]
#             for matid in range(2):
#                 if matid == 0:
#                     index_allowed = index_list[hkl_ind]
#                     if len(index_allowed) == 0:
#                         continue
#                 elif matid == 1:
#                     index_allowed = index_list1[hkl_ind]
#                     if len(index_allowed) == 0:
#                         continue
                    
#                 count = 0
#                 for index in range(rangeval):
#                     bins = 20
#                     ### index for nans
#                     nan_index1 = np.where(match_rate[index][0] == 0)[0]
#                     mat_id_index = np.where(mat_global[index][0] != matid+1)[0]
#                     nan_index = np.hstack((mat_id_index,nan_index1))
#                     nan_index = np.unique(nan_index)
                    
#                     if count == 0:
#                         spots_len_plot = np.copy(spots_len[index][0])
#                         mr_plot = np.copy(match_rate[index][0])
#                         iR_pix_plot = np.copy(iR_pix[index][0])
#                         fR_pix_plot = np.copy(fR_pix[index][0])
#                         strain_matrix_plot = np.copy(strain_matrix[index][0])
#                         e11c = strain_matrix_plot[:,0,0]#.reshape((lim_x, lim_y))
#                         e22c = strain_matrix_plot[:,1,1]#.reshape((lim_x, lim_y))
#                         e33c = strain_matrix_plot[:,2,2]#.reshape((lim_x, lim_y))
#                         e12c = strain_matrix_plot[:,0,1]#.reshape((lim_x, lim_y))
#                         e13c = strain_matrix_plot[:,0,2]#.reshape((lim_x, lim_y))
#                         e23c = strain_matrix_plot[:,1,2]#.reshape((lim_x, lim_y))
#                         strain_matrixs_plot = np.copy(strain_matrixs[index][0])
#                         e11s = strain_matrixs_plot[:,0,0]#.reshape((lim_x, lim_y))
#                         e22s = strain_matrixs_plot[:,1,1]#.reshape((lim_x, lim_y))
#                         e33s = strain_matrixs_plot[:,2,2]#.reshape((lim_x, lim_y))
#                         e12s = strain_matrixs_plot[:,0,1]#.reshape((lim_x, lim_y))
#                         e13s = strain_matrixs_plot[:,0,2]#.reshape((lim_x, lim_y))
#                         e23s = strain_matrixs_plot[:,1,2]#.reshape((lim_x, lim_y))
#                         spots_len_plot[nan_index] = np.nan 
#                         mr_plot[nan_index] = np.nan 
#                         iR_pix_plot[nan_index] = np.nan 
#                         fR_pix_plot[nan_index] = np.nan 
#                         e11c[nan_index] = np.nan 
#                         e22c[nan_index] = np.nan 
#                         e33c[nan_index] = np.nan 
#                         e12c[nan_index] = np.nan 
#                         e13c[nan_index] = np.nan 
#                         e23c[nan_index] = np.nan 
#                         e11s[nan_index] = np.nan 
#                         e22s[nan_index] = np.nan 
#                         e33s[nan_index] = np.nan 
#                         e12s[nan_index] = np.nan 
#                         e13s[nan_index] = np.nan 
#                         e23s[nan_index] = np.nan 
#                         count = 1
                        
#                     else:
#                         temp = np.copy(spots_len[index][0])
#                         temp[nan_index] = np.nan
#                         spots_len_plot = np.vstack((spots_len_plot,temp))
                        
#                         temp = np.copy(match_rate[index][0])
#                         temp[nan_index] = np.nan
#                         mr_plot = np.vstack((mr_plot,temp))
                        
#                         temp = np.copy(iR_pix[index][0])
#                         temp[nan_index] = np.nan
#                         iR_pix_plot = np.vstack((iR_pix_plot,temp))
                
#                         temp = np.copy(fR_pix[index][0])
#                         temp[nan_index] = np.nan
#                         fR_pix_plot = np.vstack((fR_pix_plot,temp))
                        
#                         strain_matrix_plot = np.copy(strain_matrix[index][0])
#                         temp = np.copy(strain_matrix_plot[:,0,0])
#                         temp[nan_index] = np.nan
#                         e11c = np.vstack((e11c,temp))
#                         temp = np.copy(strain_matrix_plot[:,1,1])
#                         temp[nan_index] = np.nan
#                         e22c = np.vstack((e22c,temp))
#                         temp = np.copy(strain_matrix_plot[:,2,2])
#                         temp[nan_index] = np.nan
#                         e33c = np.vstack((e33c,temp))
#                         temp = np.copy(strain_matrix_plot[:,0,1])
#                         temp[nan_index] = np.nan
#                         e12c = np.vstack((e12c,temp))
#                         temp = np.copy(strain_matrix_plot[:,0,2])
#                         temp[nan_index] = np.nan
#                         e13c = np.vstack((e13c,temp))
#                         temp = np.copy(strain_matrix_plot[:,1,2])
#                         temp[nan_index] = np.nan
#                         e23c = np.vstack((e23c,temp))
#                         ##
#                         strain_matrixs_plot = np.copy(strain_matrixs[index][0])
#                         temp = np.copy(strain_matrixs_plot[:,0,0])
#                         temp[nan_index] = np.nan
#                         e11s = np.vstack((e11s,temp))
#                         temp = np.copy(strain_matrixs_plot[:,1,1])
#                         temp[nan_index] = np.nan
#                         e22s = np.vstack((e22s,temp))
#                         temp = np.copy(strain_matrixs_plot[:,2,2])
#                         temp[nan_index] = np.nan
#                         e33s = np.vstack((e33s,temp))
#                         temp = np.copy(strain_matrixs_plot[:,0,1])
#                         temp[nan_index] = np.nan
#                         e12s = np.vstack((e12s,temp))
#                         temp = np.copy(strain_matrixs_plot[:,0,2])
#                         temp[nan_index] = np.nan
#                         e13s = np.vstack((e13s,temp))
#                         temp = np.copy(strain_matrixs_plot[:,1,2])
#                         temp[nan_index] = np.nan
#                         e23s = np.vstack((e23s,temp))
                
#                 spots_len_plot = spots_len_plot.flatten()
#                 mr_plot = mr_plot.flatten()
#                 iR_pix_plot = iR_pix_plot.flatten()
#                 fR_pix_plot = fR_pix_plot.flatten() 
#                 e11c = e11c.flatten()
#                 e22c = e22c.flatten()
#                 e33c = e33c.flatten()
#                 e12c = e12c.flatten()
#                 e13c = e13c.flatten()
#                 e23c = e23c.flatten()
#                 e11s = e11s.flatten()
#                 e22s = e22s.flatten()
#                 e33s = e33s.flatten()
#                 e12s = e12s.flatten()
#                 e13s = e13s.flatten()
#                 e23s = e23s.flatten()
                
#                 spots_len_plot = spots_len_plot[index_allowed]
#                 mr_plot = mr_plot[index_allowed]
#                 iR_pix_plot = iR_pix_plot[index_allowed]
#                 fR_pix_plot = fR_pix_plot[index_allowed]
#                 e11c = e11c[index_allowed]
#                 e22c = e22c[index_allowed]
#                 e33c = e33c[index_allowed]
#                 e12c = e12c[index_allowed]
#                 e13c = e13c[index_allowed]
#                 e23c = e23c[index_allowed]
#                 e11s = e11s[index_allowed]
#                 e22s = e22s[index_allowed]
#                 e33s = e33s[index_allowed]
#                 e12s = e12s[index_allowed]
#                 e13s = e13s[index_allowed]
#                 e23s = e23s[index_allowed]
#                 try:
#                     title = "Number of spots and matching rate "+hkl_ind
#                     fig = plt.figure()
#                     axs = fig.subplots(1, 2)
#                     axs[0].set_title("Number of spots", loc='center', fontsize=8)
#                     axs[0].hist(spots_len_plot, bins=bins)
#                     axs[0].set_ylabel('Frequency', fontsize=8)
#                     axs[0].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0].tick_params(axis='both', which='minor', labelsize=8)
#                     axs[1].set_title("matching rate", loc='center', fontsize=8)
#                     axs[1].hist(mr_plot, bins=bins)
#                     axs[1].set_ylabel('Frequency', fontsize=8)
#                     axs[1].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1].tick_params(axis='both', which='minor', labelsize=8)
#                     plt.tight_layout()
#                     plt.savefig(model_direc+ "//"+title+"_"+material_id[matid]+'.png', format='png', dpi=1000) 
#                     plt.close(fig)
#                 except:
#                     pass
#                 try:
#                     title = "Initial and Final residues "+hkl_ind
#                     fig = plt.figure()
#                     axs = fig.subplots(1, 2)
#                     axs[0].set_title("Initial residues", loc='center', fontsize=8)
#                     axs[0].hist(iR_pix_plot, bins=bins)
#                     axs[0].set_ylabel('Frequency', fontsize=8)
#                     axs[0].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0].tick_params(axis='both', which='minor', labelsize=8)
#                     axs[1].set_title("Final residues", loc='center', fontsize=8)
#                     axs[1].hist(fR_pix_plot, bins=bins)
#                     axs[1].set_ylabel('Frequency', fontsize=8)
#                     axs[1].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1].tick_params(axis='both', which='minor', labelsize=8)
#                     plt.tight_layout()
#                     plt.savefig(model_direc+ "//"+title+"_"+material_id[matid]+'.png',format='png', dpi=1000) 
#                     plt.close(fig)
#                 except:
#                     pass
#                 try:
#                     title = "strain Crystal reference "+hkl_ind
#                     fig = plt.figure()
#                     axs = fig.subplots(2, 3)
#                     axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
#                     axs[0, 0].hist(e11c, bins=bins)
#                     axs[0, 0].set_ylabel('Frequency', fontsize=8)
#                     axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
#                     axs[0, 1].hist(e22c, bins=bins)
#                     axs[0, 1].set_ylabel('Frequency', fontsize=8)
#                     axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
#                     axs[0, 2].hist(e33c, bins=bins)
#                     axs[0, 2].set_ylabel('Frequency', fontsize=8)
#                     axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
#                     axs[1, 0].hist(e12c, bins=bins)
#                     axs[1, 0].set_ylabel('Frequency', fontsize=8)
#                     axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
#                     axs[1, 1].hist(e13c, bins=bins)
#                     axs[1, 1].set_ylabel('Frequency', fontsize=8)
#                     axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
#                     axs[1, 2].hist(e23c, bins=bins)
#                     axs[1, 2].set_ylabel('Frequency', fontsize=8)
#                     axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
#                     plt.tight_layout()
#                     plt.savefig(model_direc+ "//"+title+"_"+material_id[matid]+'.png', format='png', dpi=1000) 
#                     plt.close(fig)
#                 except:
#                     pass
#                 try:
#                     title = "strain Sample reference "+hkl_ind
#                     fig = plt.figure()
#                     axs = fig.subplots(2, 3)
#                     axs[0, 0].set_title(r"$\epsilon_{11}$", loc='center', fontsize=8)
#                     axs[0, 0].hist(e11s, bins=bins)
#                     axs[0, 0].set_ylabel('Frequency', fontsize=8)
#                     axs[0, 0].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0, 0].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[0, 1].set_title(r"$\epsilon_{22}$", loc='center', fontsize=8)
#                     axs[0, 1].hist(e22s, bins=bins)
#                     axs[0, 1].set_ylabel('Frequency', fontsize=8)
#                     axs[0, 1].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0, 1].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[0, 2].set_title(r"$\epsilon_{33}$", loc='center', fontsize=8)
#                     axs[0, 2].hist(e33s, bins=bins)
#                     axs[0, 2].set_ylabel('Frequency', fontsize=8)
#                     axs[0, 2].tick_params(axis='both', which='major', labelsize=8)
#                     axs[0, 2].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[1, 0].set_title(r"$\epsilon_{12}$", loc='center', fontsize=8)
#                     axs[1, 0].hist(e12s, bins=bins)
#                     axs[1, 0].set_ylabel('Frequency', fontsize=8)
#                     axs[1, 0].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1, 0].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[1, 1].set_title(r"$\epsilon_{13}$", loc='center', fontsize=8)
#                     axs[1, 1].hist(e13s, bins=bins)
#                     axs[1, 1].set_ylabel('Frequency', fontsize=8)
#                     axs[1, 1].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1, 1].tick_params(axis='both', which='minor', labelsize=8)
                    
#                     axs[1, 2].set_title(r"$\epsilon_{23}$", loc='center', fontsize=8)
#                     axs[1, 2].hist(e23s, bins=bins)
#                     axs[1, 2].set_ylabel('Frequency', fontsize=8)
#                     axs[1, 2].tick_params(axis='both', which='major', labelsize=8)
#                     axs[1, 2].tick_params(axis='both', which='minor', labelsize=8)
#                     plt.tight_layout()
#                     plt.savefig(model_direc+ "//"+title+"_"+material_id[matid]+'.png', format='png', dpi=1000) 
#                     plt.close(fig)  
#                 except:
#                     pass

def start():
    """ start of GUI for module launch"""
    app = QApplication(sys.argv)
    
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))
    
    win = Window(rect.width()//3, rect.height()//2)
    win.show()
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    start()