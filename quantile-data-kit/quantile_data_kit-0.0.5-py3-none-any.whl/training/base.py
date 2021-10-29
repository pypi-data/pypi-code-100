from dagster import InputDefinition, OutputDefinition
import pandas as pd
import dask.dataframe as dd
from typing import Union
from sklearn.base import BaseEstimator

from qdk.base import BaseComponent
from qdk.dagster_types import DataFrameType, SeriesType, ModelType


class TrainingComponent(BaseComponent):
    compute_function = "train"
    tags = {"kind": "training"}
    input_defs = [
        InputDefinition("X", DataFrameType),
        InputDefinition("y", SeriesType),
        InputDefinition("model", ModelType),
    ]
    output_defs = [OutputDefinition(ModelType, "model")]

    @classmethod
    def train(
        cls,
        X: Union[pd.DataFrame, dd.DataFrame],
        y: Union[pd.Series, dd.Series],
        model: Union[BaseEstimator],
    ) -> Union[BaseEstimator]:
        raise NotImplementedError(
            'Make sure you added a "train" function to the component'
        )
