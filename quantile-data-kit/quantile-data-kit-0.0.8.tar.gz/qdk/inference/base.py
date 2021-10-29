from dagster import InputDefinition, OutputDefinition, Output, Any
import pandas as pd
from typing import Dict
from qdk.base import BaseComponent


class InferenceComponent(BaseComponent):
    compute_function = "predict"
    tags = {"kind": "inference"}
    input_defs = [InputDefinition("data", pd.DataFrame), InputDefinition("model", Any)]
    output_defs = [OutputDefinition(pd.DataFrame, "predictions")]

    @classmethod
    def predict(cls, data: Dict[str, pd.DataFrame], model: Any):
        raise NotImplementedError(
            'Make sure you added a "predict" function to the component'
        )
