import os

import pandas as pd
import pytest

import datawhys as dw


@pytest.fixture
def datapath():
    """
    Get the path to a data file.
    Parameters
    ----------
    path : str
        Path to the file, relative to ``datawhys/tests/``
    Returns
    -------
    path including ``datawhys/tests``.
    Raises
    ------
    ValueError
        If the path doesn't exist
    """
    BASE_PATH = os.path.join(os.path.dirname(__file__), "tests")

    def deco(*args):
        path = os.path.join(BASE_PATH, *args)
        if not os.path.exists(path):
            raise ValueError(f"Could not find file {path}")
        return path

    return deco


@pytest.fixture
def iris(datapath):
    """
    The iris dataset as a DataWhysFrame.
    """
    df = pd.read_csv(datapath("data", "iris.csv"))
    return dw.DataWhysFrame(df)


@pytest.fixture
def titanic(datapath):
    """
    The titanic dataset as a DataWhysFrame.
    """
    df = pd.read_csv(datapath("data", "titanic.csv"))
    return dw.DataWhysFrame(df)
