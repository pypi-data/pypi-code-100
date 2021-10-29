from os import PathLike
from typing import Union, Dict, Any, Iterable, Tuple

import numpy as np
import pandas as pd
from catboost import Pool
from numpy.typing import NDArray
from sklearn.model_selection import BaseCrossValidator, BaseShuffleSplit

__all__ = (
    'KWARGS',
    'KWARG_ITERABLE',
    'KWARGS_OR_ITERABLE',

    'ARRAY_INDEXER',
    'SPLIT_ITERABLE',
    'SPLITTER',

    'FEATURES',
    'COLUMN',
    'DATASET',

    'PATH'
)

KWARGS = Dict[str, Any]
KWARG_ITERABLE = Iterable[KWARGS]
KWARGS_OR_ITERABLE = Union[KWARGS, KWARG_ITERABLE]

ARRAY_INDEXER = NDArray[np.integer]
SPLIT_ITERABLE = Iterable[Tuple[ARRAY_INDEXER, ARRAY_INDEXER]]
SPLITTER = Union[SPLIT_ITERABLE, BaseCrossValidator, BaseShuffleSplit]

FEATURES = Union[pd.DataFrame, np.ndarray]
COLUMN = Union[pd.Series, np.ndarray]
DATASET = Union[Pool, Tuple[FEATURES, COLUMN]]

PATH = Union[PathLike[str], str]
