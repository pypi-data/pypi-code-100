import typing as t

import pandas as pd

from model import __version__ as _version
from model.config.core import config
from model.processing.data_manager import load_pipeline
from model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"

_price_pipe = load_pipeline(file_name=pipeline_file_name)
print("Loaded the trained model")


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        predictions = _price_pipe.predict(
            X=validated_data[config.model_config.features]
        )
        results = {
            "predictions": [predictions],  # type: ignore
            "version": _version,
            "errors": errors,
        }

    return results
