from typing import List, Dict
from MLVisualizationTools.backend import colinfo
import pandas as pd

#Functions for passing data to ml models

#region Tensorflow
#region grid
def TFModelPredictionGrid(model, x:str, y:str, data:pd.DataFrame,
                          exclude:List[str] = None, steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    """
    return TFModelPredictionGridRaw(model, x, y, colinfo(data, exclude), steps)

def TFModelPredictionGridRaw(model, x:str, y:str, coldata:List[Dict], steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    Call from TFModelPredictionGrid to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A tensorflow model
    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    """
    allcols = []
    for item in coldata:
        allcols.append(item['name'])

    assert x in allcols, "X must be in coldata"
    assert y in allcols, "Y must be in coldata"

    cols = []
    for item in coldata:
        if item not in [x, y]:
            cols.append(item['name'])

    srow = []
    for item in cols:
        for d in coldata:
            if d['name'] == item:
                srow.append(d['mean'])

    srow = [srow] * (steps ** 2)
    preddata = pd.DataFrame(srow, columns=cols)

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == x:
                col.append(pos * (item['max'] - item['min']) / (steps - 1) + item['min'])
    col = col * steps
    preddata[x] = col

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == y:
                col += [pos * (item['max'] - item['min']) / (steps - 1) + item['min']] * steps
    preddata[y] = col

    predictions = model.predict(preddata)
    preddata['Output'] = predictions
    return preddata
#endregion grid

#region animation
def TFModelPredictionAnimation(model, x:str, y:str, anim:str, data: pd.DataFrame,
                               exclude:List[str] = None, steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param anim: Animation axis for graph data
    :param data: A pandas dataframe
    :param exclude: Values to be excluded from data, useful for output values
    :param steps: Resolution to scan model with
    """
    return TFModelPredictionAnimationRaw(model, x, y, anim, colinfo(data, exclude), steps)

def TFModelPredictionAnimationRaw(model, x:str, y:str, anim:str, coldata:List[Dict], steps:int=20) -> pd.DataFrame:
    """
    Creates a dataset from a 2d prediction on a tensorflow model. Wrapper function for TFModelPredictionGridRaw()
    that automatically handles column info generation.

    Call from TFModelPredictionGrid to autogen params.

    Coldata should be formatted with keys 'name', 'min', 'max', 'mean'

    :param model: A tensorflow model
    :param model: A tensorflow model
    :param x: xaxis for graph data
    :param y: yaxis for graph data
    :param anim: Animation axis for graph data
    :param coldata: An ordered list of dicts with col names, min max values, and means
    :param steps: Resolution to scan model with
    """

    allcols = []
    for item in coldata:
        allcols.append(item['name'])

    assert x in allcols, "X must be in coldata"
    assert y in allcols, "Y must be in coldata"
    assert anim in allcols, "Anim must be in coldata"

    cols = []
    for item in coldata:
        if item not in [x, y, anim]:
            cols.append(item['name'])

    srow = []
    for item in cols:
        for d in coldata:
            if d['name'] == item:
                srow.append(d['mean'])

    srow = [srow] * (steps ** 3)
    preddata = pd.DataFrame(srow, columns=cols)

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == x:
                col.append(pos * (item['max'] - item['min']) / (steps - 1) + item['min'])
    col = col * (steps ** 2)
    preddata[x] = col

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == y:
                col += [pos * (item['max'] - item['min']) / (steps - 1) + item['min']] * steps
    col = col * steps
    preddata[y] = col

    col = []
    for pos in range(0, steps):
        for item in coldata:
            if item['name'] == anim:
                col += [pos * (item['max'] - item['min']) / (steps - 1) + item['min']] * (steps ** 2)
    preddata[anim] = col

    predictions = model.predict(preddata)
    preddata['Output'] = predictions
    return preddata

#endregion
#endregion
