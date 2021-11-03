from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from model.config.core import config


def drop_na_inputs(*, input_data: pd.DataFrame) -> pd.DataFrame:
    """Check model inputs for na values and filter."""
    validated_data = input_data.copy()
    return validated_data


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    input_data["Date_first_seen"] = input_data["Date_first_seen"].astype(
        "datetime64[ms]"
    )
    relevant_data = input_data[config.model_config.features].copy()
    validated_data = drop_na_inputs(input_data=relevant_data)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleHouseDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class HouseDataInputSchema(BaseModel):
    week: Optional[str]
    Duration: Optional[float]
    Proto: Optional[str]
    Flag: Optional[str]
    Src_IP_Addr: Optional[str]
    Src_Pt: Optional[int]
    Dst_IP_Addr: Optional[str]
    Dst_Pt: Optional[float]
    Packets: Optional[float]
    Tos: Optional[int]
    Bytes: Optional[float]
    Flags: Optional[str]
    Class: Optional[str]
    attackType: Optional[str]
    hour: Optional[str]
    minute: Optional[str]
    seconds: Optional[str]


class MultipleHouseDataInputs(BaseModel):
    inputs: List[HouseDataInputSchema]
