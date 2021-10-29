from dagster import DagsterType
from qdk.utils.typing import is_dataframe, is_series, is_model, is_mlflow_run


DataFrameType = DagsterType(
    name="DataFrameType",
    type_check_fn=lambda _, value: is_dataframe(value),
    description="Can represent either a pandas or dask dataframe.",
)
SeriesType = DagsterType(
    name="SeriesType",
    type_check_fn=lambda _, value: is_series(value),
    description="Can represent either a pandas or dask series.",
)
ModelType = DagsterType(
    name="ModelType",
    type_check_fn=lambda _, value: is_model(value),
    description="Generic typing for machine learning models.",
)
MLFlowRunType = DagsterType(
    name="MLFlowRunType",
    type_check_fn=lambda _, value: is_mlflow_run(value),
    description="A type that represents a qdk.MLFlowRun class.",
)
