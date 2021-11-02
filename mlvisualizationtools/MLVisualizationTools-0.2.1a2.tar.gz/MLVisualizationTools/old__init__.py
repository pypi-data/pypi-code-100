from MLVisualizationTools.modelanalytics import analyzeTFModel, analyzeTFModelRaw
from MLVisualizationTools.modelinterface import TFModelPredictionGrid, TFModelPredictionGridRaw
from MLVisualizationTools.modelinterface import TFModelPredictionAnimation, TFModelPredictionAnimationRaw
from MLVisualizationTools.graphinterface import plotlyGrid, plotlyAnimation, matplotlibGrid
from enum import Enum as enum

#Don't use these, __init__ is better

#A bunch of wrapper functions to make calling various tools easier

class Enum(enum):
    def __contains__(self, item):
        return item in [v.value for v in self.__members__.values()]

class ModelTypes(Enum):
    Tensorflow = "tf"

class InterfaceTypes(Enum):
    Grid = "grid"
    Animation = "animation"

class DataTypes(Enum):
    Grid = "grid"
    Animation = "animation"

class OutputTypes(Enum):
    Plotly = "Plotly"
    Matplotlib = "Matplotlib"

class Analytics:
    Tensorflow = analyzeTFModel
    TensorflowRaw = analyzeTFModelRaw

class Interfaces:
    TensorflowGrid = TFModelPredictionGrid
    TensorflowGridRaw = TFModelPredictionGridRaw
    TensorflowAnimation = TFModelPredictionAnimation
    TensorflowAnimationRaw = TFModelPredictionAnimationRaw

class Graphs:
    PlotlyGrid = plotlyGrid
    PlotlyAnimation = plotlyAnimation
    MatplotlibGrid = matplotlibGrid

class Mode:
    def __init__(self, modeltype = ModelTypes.Tensorflow, outputtype = OutputTypes.Plotly, useraw=False):
        if modeltype not in ModelTypes:
            raise Exception("Model type not found! (Try using the enum!)")
        if outputtype not in OutputTypes:
            raise Exception("Output type not found! (Try using the enum!)")
        self.modeltype = modeltype
        self.outputtype = outputtype
        self.useraw = useraw

    def analyzer(self):
        """Get an analyzer based on mode settings"""
        if self.modeltype == ModelTypes.Tensorflow:
            if self.useraw:
                return Analytics.TensorflowRaw
            else:
                return Analytics.Tensorflow

        else:
            raise Exception("No analytics found for this mode!")

    def interface(self, interface):
        """Get an ml model interface based on mode settings"""
        if interface not in InterfaceTypes:
            raise Exception("Interface type not found! (Try using the enum!)")

        if self.modeltype == ModelTypes.Tensorflow and interface == InterfaceTypes.Grid:
            if self.useraw:
                return Interfaces.TensorflowGridRaw
            else:
                return Interfaces.TensorflowGrid

        elif self.modeltype == ModelTypes.Tensorflow and interface == InterfaceTypes.Animation:
            if self.useraw:
                return Interfaces.TensorflowAnimationRaw
            else:
                return Interfaces.TensorflowAnimation
        else:
            raise Exception("No interface found for this mode!")

    def graph(self, datatype):
        """
        Get a graph based on mode settings
        """
        if datatype not in DataTypes:
            raise Exception("Data type not found! (Try using the enum!)")
        if self.outputtype == OutputTypes.Plotly and datatype == DataTypes.Grid:
            return Graphs.PlotlyGrid
        elif self.outputtype == OutputTypes.Plotly and datatype == DataTypes.Animation:
            return Graphs.PlotlyAnimation
        elif self.outputtype == OutputTypes.Matplotlib and datatype == DataTypes.Grid:
            return Graphs.MatplotlibGrid
        else:
            raise Exception("No graph found for this mode!")