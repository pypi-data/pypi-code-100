import pandas as pd

def simpleColor(data: pd.DataFrame, color) -> pd.DataFrame:
    """Marks all points as being the color inputted"""
    data['Color'] = [color] * len(data)
    return data

def binaryColor(data: pd.DataFrame, highcontrast:bool=False, truecolor=None, falsecolor=None,
                cutoff:float=0.5, outputkey: str = 'Output') -> pd.DataFrame:
    """
    Colors grid based on whether the value is higher than the cutoff. Default colors are green for true and red
    for false. Black will appear if an error occurs.

    :param data: Input data
    :param highcontrast: Switches default colors to blue for true and orange for false
    :param truecolor: Manually specify truecolor
    :param falsecolor: Manually specify falsecolor
    :param cutoff: Cutoff value, higher is true
    :param outputkey: Key to grab values from
    """
    if truecolor is None:
        if not highcontrast:
            truecolor = "green"
        else:
            truecolor = "blue"
    if falsecolor is None:
        if not highcontrast:
            falsecolor = "red"
        else:
            falsecolor = "orange"

    #grid['Color'] = 'black' * len(grid)
    data.loc[data[outputkey] > cutoff, 'Color'] = truecolor
    data.loc[data[outputkey] <= cutoff, 'Color'] = falsecolor

    return data
