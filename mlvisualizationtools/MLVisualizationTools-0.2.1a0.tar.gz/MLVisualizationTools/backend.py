from typing import List, Dict
import pandas as pd
from os import path

#Backend functions and classes used by the other scripts

def colinfo(data: pd.DataFrame, exclude:List[str] = None) -> List[Dict]:
    """
    Helper function for generating column info dict for a datframe

    :param data: A pandas Dataframe
    :param exclude: A list of data items to exclude
    """
    if exclude is None:
        exclude = []

    coldata = []
    for item in data.columns:
        if item not in exclude:
            coldata.append({'name': item, 'mean': data[item].mean(),
                            'min': data[item].min(), 'max': data[item].max()})
    return coldata

def fileloader(target: str):
    """Specify a path relative to MLVisualizationTools"""
    return path.dirname(__file__) + '/' + target

def getTheme(theme, folder=None, figtemplate=None):
    """
    Backend function for loading theme css files.

    Theme can be 'light' or 'dark', and that will autoload the theme from dbc
    If folder is none, it is set based on the theme
    If figtemplate is none, it is set based on the theme

    Returns theme, folder

    :param theme: 'light' / 'dark' or a css url
    :param folder: path to assets folder
    :param figtemplate: Used for putting plotly in dark theme
    """
    import dash_bootstrap_components as dbc
    if theme == "light":
        theme = dbc.themes.FLATLY
        if folder is None:
            folder = fileloader('theme_assets/light_assets')
        if figtemplate is None:
            figtemplate = "plotly"

    elif theme == "dark":
        theme = dbc.themes.DARKLY
        if folder is None:
            folder = fileloader('theme_assets/dark_assets')
        if figtemplate is None:
            figtemplate = "plotly_dark"

    return theme, folder, figtemplate