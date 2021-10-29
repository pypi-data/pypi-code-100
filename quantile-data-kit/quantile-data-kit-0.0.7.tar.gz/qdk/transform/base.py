import pandas as pd
import dask.dataframe as dd
from typing import Union
from dagster import InputDefinition, OutputDefinition
from qdk.base import BaseComponent
from qdk.dagster_types import DataFrameType


class TransformComponent(BaseComponent):
    compute_function = "transform"
    tags = {"kind": "transform"}
    input_defs = [InputDefinition("df", DataFrameType)]
    output_defs = [OutputDefinition(DataFrameType, "df")]

    @staticmethod
    def _get_text_column_name(df: Union[pd.DataFrame, dd.DataFrame]) -> str:
        text_column_name = df.attrs.get("text_column", "text")
        return text_column_name

    @classmethod
    def transform(cls, df: DataFrameType, **config) -> DataFrameType:
        raise NotImplementedError(
            'Make sure you added a "transform" function to the component'
        )
