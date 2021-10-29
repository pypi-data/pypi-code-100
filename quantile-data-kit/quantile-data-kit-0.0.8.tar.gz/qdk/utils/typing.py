from pandas import DataFrame, Series
from dask.dataframe import DataFrame as DaskDataFrame, Series as DaskSeries
from dask.array.core import Array as DaskArray
from numpy import ndarray
from sklearn.base import BaseEstimator
from mlflow.pyfunc import PyFuncModel
from qdk.mlflow import MLFlowRun


def is_dataframe(value) -> bool:
    """Function to check whether the incoming value is a pandas or dask dataframe.

    Args:
        value (Any): The incoming dagster value.

    Returns:
        bool: Whether the input is a dataframe or not.
    """
    return (
        isinstance(value, DataFrame)
        or isinstance(value, DaskDataFrame)
        or isinstance(value, DaskArray)
        or isinstance(value, ndarray)
    )


def is_series(value) -> bool:
    """Function to check whether the incoming value is a pandas or dask series.

    Args:
        value (Any): The incoming dagster value.

    Returns:
        bool: Whether the input is a series or not.
    """
    return (
        isinstance(value, Series)
        or isinstance(value, DaskSeries)
        or isinstance(value, DaskArray)
        or isinstance(value, ndarray)
    )


def is_pandas_dataframe(value):
    return isinstance(value, DataFrame)


def is_dask_dataframe(value):
    return isinstance(value, DaskDataFrame)


def is_model(value):
    return isinstance(value, BaseEstimator) or isinstance(value, MLFlowRun)


def is_mlflow_run(value):
    return isinstance(value, MLFlowRun)
