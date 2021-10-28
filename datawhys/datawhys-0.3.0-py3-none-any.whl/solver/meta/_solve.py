import json
from typing import List

import pandas as pd

from datawhys import datautils
from datawhys.api import meta_class_start, meta_exclusion_set_start, meta_result
from datawhys.dd_transformer import DDTransformer
from datawhys.utils import meta as meta_utils, utilities


def _prepare_data(
    df: pd.DataFrame,
    outcome: str,
    classes: List[str],
    encode: bool,
    sample: bool,
    random_state,
):
    if outcome is None:
        outcome = df.columns[0]

    if encode:
        df_orig = df.copy()
        outcome_orig = outcome

        encoder = DDTransformer(df)
        df = utilities.encode_dataframe(df, encoder)
        outcome = encoder.original_to_encoded_column(outcome)

        if classes:
            classes = [
                utilities.encode_value(df_orig, outcome_orig, c, encoder)
                for c in classes
            ]
    else:
        encoder = None

    if sample:
        df = datautils.sample(
            df, 2500, outcome=outcome, floor=3500, random_state=random_state,
        )

    return df, outcome, classes, encoder


def _postprocess_data(
    df: pd.DataFrame, outcome: str, encoder: DDTransformer, rules: dict
):
    if encoder:
        rules = meta_utils.decode_meta_rules(rules, df, outcome, encoder)

    return rules


def class_exploration_solve(
    df: pd.DataFrame,
    outcome: str = None,
    classes: List[str] = None,
    encode=True,
    sample=True,
    random_state=None,
    **kwargs,
):
    """Run a solve that learns against itself

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to use for the solve

    outcome : str, default=None
        Which column to use as the outcome for the solve (sometimes referred to as a
        target feature). If None, then the first column is selected

    classes: List[str], default=None
        For discrete outcomes, a list of modalities to explore. For continuous outcomes,
        a list containing 'min' and/or 'max'. If None, explore all classes.

    encode: bool, default=True
        Whether or not the data should be encoded before being sent to the MB API.
        Encoding can result in additional time on client side. Disable if your data is
        largely non-sensitive.

    sample: bool, default=True
        Whether or not the data should be sampled before being sent to the MB API.
        Not pre-sampling the data can cause size limits to be reached and excessive
        solve times

    random_state : int or np.random.RandomStateInstance, default: 0
        Pseudo-random number generator to control the sampling state.
        Use an int for reproducible results across function calls.
        See the sklearn for more details.

    kwargs: any
        Remaining kwargs are sent so api.meta_class_start

    Returns
    -------
    rules: array of dict
        An array of meta_rule dicts that have rules and meta properties
    """
    df, outcome, classes, encoder = _prepare_data(
        df, outcome, classes, encode, sample, random_state
    )

    # Send data OTW and wait for solve to finish
    data = json.loads(df.to_json(orient="records"))
    task = meta_class_start(outcome=outcome, data=data, classes=classes, **kwargs)
    result = meta_result(id=task["id"])

    rules = result["rules"]
    rules = _postprocess_data(df, outcome, encoder, rules)

    return rules


def exclusion_set_solve(
    df: pd.DataFrame,
    outcome: str = None,
    classes: List[str] = None,
    encode=True,
    sample=True,
    random_state=None,
    **kwargs,
):
    """Run a solve that learns against itself

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to use for the solve

    outcome : str, default=None
        Which column to use as the outcome for the solve (sometimes referred to as a
        target feature). If None, then the first column is selected

    classes: List[str], default=None
        For discrete outcomes, a list of modalities to explore. For continuous outcomes,
        a list containing 'min' and/or 'max'. If None, explore all classes.

    encode: bool, default=True
        Whether or not the data should be encoded before being sent to the MB API.
        Encoding can result in additional time on client side. Disable if your data is
        largely non-sensitive.

    sample: bool, default=True
        Whether or not the data should be sampled before being sent to the MB API.
        Not pre-sampling the data can cause size limits to be reached and excessive
        solve times

    random_state : int or np.random.RandomStateInstance, default: 0
        Pseudo-random number generator to control the sampling state.
        Use an int for reproducible results across function calls.
        See the sklearn for more details.

    kwargs: any
        Remaining kwargs are sent so api.meta_exclusion_set_start

    Returns
    -------
    rules: array of dict
        An array of meta_rule dicts that have rules and meta properties
    """
    df, outcome, classes, encoder = _prepare_data(
        df, outcome, classes, encode, sample, random_state
    )

    # Send data OTW and wait for solve to finish
    data = json.loads(df.to_json(orient="records"))
    task = meta_exclusion_set_start(
        outcome=outcome, data=data, classes=classes, **kwargs
    )
    result = meta_result(id=task["id"])

    rules = result["rules"]
    rules = _postprocess_data(df, outcome, encoder, rules)

    return rules
