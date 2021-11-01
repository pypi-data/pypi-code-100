import plotly
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def GraphMakerBase(graph_func, df, *args, to_html = True, show=False,  **kwargs):
    '''
    Base class for making graphs from dataframes.
    :param graph_func: A function that returns a plotly figure.
    :param df: A dataframe (or dictionary) passed as the first argument to the graph_func
    :param *args: Arguments to be passed to the graph function.
    :param to_html: Whether or not to return the HTML string.
    :param show: Whether or not to display the graph.
    :param **kwargs: Keyword arguments for the graphing function.
    :returns: Returns the html for teh graph if it exists, and None otherwise.
    '''
    fig = graph_func(df, *args, **kwargs)
    html_str = None
    if to_html:
        html_str = plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)
    if show:
        fig.show()
    return html_str

def ClasswisePlots(df, callback, go_kwargs={}, callback_kwargs={}):
    '''
    Used to make plots with different traces for each class if such functionality is not readily available via plotly.express.
    :param df: Dataframe.
    :param callback: A single callback function which returns a trace object.
    :param go_kwargs: A dictionary of keyword arguments to be passed to the graph object figure.
    :param callback_kwargs: A dictionary of keyword arguments to be passed to the callback function.
    '''
    traces = []
    classes = df['class_name'].unique().tolist()
    for class_name in classes:
        sub_df = df[df['class_name']==class_name]
        graph_object = callback(sub_df, **callback_kwargs)
        traces.append(graph_object)
    fig = go.Figure(data=traces, **go_kwargs)
    return fig