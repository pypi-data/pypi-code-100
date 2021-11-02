from MLVisualizationTools.backend import colinfo
from typing import List, Dict
import copy
import pandas as pd

#Functions for retrieving data about ml model structure

#TODO - nonlinear

class AnalyticsColumnInfo:
    """Wrapper class for holding col info"""
    def __init__(self, name: str, variance: float):
        self.name = name
        self.variance = variance

    def __lt__(self, other):
        return self.variance < other.variance

    def __repr__(self):
        return "Col with name: " + self.name + " and variance " + str(self.variance)

class AnalyticsResult:
    """Wrapper class for holding and processing col info"""
    def __init__(self):
        self.cols: List[AnalyticsColumnInfo] = []

    def append(self, name: str, variance: float):
        self.cols.append(AnalyticsColumnInfo(name, variance))

    def maxVariance(self):
        """Return a list of cols, ordered by maximum variance"""
        cols = copy.copy(self.cols)
        cols.sort(reverse=True)
        return cols

#region Tensorflow
def analyzeTFModel(model, data: pd.DataFrame, exclude: List[str] = None, steps:int=20) -> AnalyticsResult:
    """
    Performs 1d analysis on a tensorflow model. Wrapper function for analyzeTFModelRaw()
    that automatically handles column info generation.

    :param model: A tensorflow model
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    """
    return analyzeTFModelRaw(model, colinfo(data, exclude), steps)

def analyzeTFModelRaw(model, coldata: List[Dict], steps:int=20) -> AnalyticsResult:
    """
    Performs 1d analysis on a tensorflow model. Returns a class with lots of info for graphing.
    Call from anaylyzeTFModel to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A tensorflow model
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    """
    AR = AnalyticsResult()

    predrow = []
    cols = []
    for item in coldata:
        predrow.append(item['mean'])
        cols.append(item['name'])
    predrow = [predrow] * (steps * len(coldata))
    preddata = pd.DataFrame(predrow, columns=cols)

    currentpos = 0
    for item in coldata:
        for i in range(0, steps):
            preddata[item['name']][i + currentpos] = i * (item['max'] - item['min'])/(steps-1) + item['min']
        currentpos += steps

    predictions = model.predict(preddata)

    currentpos = 0
    for item in coldata:
        values = predictions[currentpos:currentpos + steps]
        currentpos += steps
        AR.append(item['name'], values.max() - values.min())
    return AR
#endregion