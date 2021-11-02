"""
A set of functions and demos to make machine learning projects easier to understand through effective visualizations.
"""

from MLVisualizationTools.modelanalytics import analyzeTFModel, analyzeTFModelRaw
from MLVisualizationTools.modelinterface import TFModelPredictionGrid, TFModelPredictionGridRaw
from MLVisualizationTools.modelinterface import TFModelPredictionAnimation, TFModelPredictionAnimationRaw
from MLVisualizationTools.graphinterface import plotlyGrid, plotlyAnimation, matplotlibGrid
from MLVisualizationTools.colorizer import simpleColor, binaryColor

#A bunch of wrapper functions to make calling various tools easier
class Analytics:
    Tensorflow = analyzeTFModel
    TensorflowRaw = analyzeTFModelRaw

class Interfaces:
    TensorflowGrid = TFModelPredictionGrid
    TensorflowGridRaw = TFModelPredictionGridRaw
    TensorflowAnimation = TFModelPredictionAnimation
    TensorflowAnimationRaw = TFModelPredictionAnimationRaw

class Colorizers:
    Simple = simpleColor
    Binary = binaryColor

class Graphs:
    PlotlyGrid = plotlyGrid
    PlotlyAnimation = plotlyAnimation
    MatplotlibGrid = matplotlibGrid