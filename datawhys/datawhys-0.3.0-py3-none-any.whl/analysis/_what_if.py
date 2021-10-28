from typing import List

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from datawhys.dd_transformer import DDTransformer
from datawhys.solver import solve
from datawhys.utils import utilities
from datawhys.utils.data import is_continuous

__X_COL = "__transform_x"
__Y_COL = "__transform_y"
__DIST_COL = "__point_distance"
__INV_DIST_COL = "__point_inverse_distance"


def find_adjustable_conditions(
    df: pd.DataFrame,
    point: dict,
    adjustable: List[str],
    inverse: bool = True,
    outcome: str = None,
    targets: List[str] = None,
    **kwargs,
):
    """
    Find a rule using What-If Analysis on a given point and a dataset.  Based on the
    point evaluation, finds conditions from the list of adjustable columns for similar
    or different points in the dataset.

    Parameters
    ----------
    df: pd.DataFrame
        The dataset to use for the analysis

    point: dict
        A single point evaluation.  Must have the same shape as the dataset.

    adjustable: List[str]
        A list of columns that can be changed that you wish to analyze.

    inverse: bool, default=True
        If True, find a rule containing data points that have a different outcome from
        the current point evaluation.  Otherwise, find a rule containing data points
        that have a different outcome from the current point evaluation.

    outcome: str, default=None
        See parameter *targets*

    targets: List[str], default=None
        Optionally filters down the dataset to only the targets specified if both
        *outcome* and *targets* are defined.

    kwargs: any
        Remaining kwargs that are used in the solve (see datawhys.solver.solve)

    Returns
    -------
    rule: dict
        The conditions that the What-If Analysis found
    """

    import umap

    # TODO: find a graceful way to handle nulls/NaNs in the data
    if any(pd.isna(x) or pd.isnull(x) for x in point.values()):
        raise Exception("point cannot have any NaN or null values")

    if outcome:
        if outcome not in df.columns:
            raise Exception(f"outcome '{outcome}' does not exist")
        if is_continuous(df[outcome]):
            raise Exception(
                "outcome and targets can only be used with discrete outcomes"
            )

    if targets:
        if not outcome:
            raise Exception("outcome must be specified with targets")

        missing_targets = [x for x in targets if x not in df[outcome].unique()]

        if missing_targets:
            raise Exception(f"targets '{', '.join(missing_targets)}' do not exist")

    df_new = df.copy()
    df_new = df_new.append(point, ignore_index=True)
    df_new = df_new.dropna()
    pt_idx = df_new.shape[0] - 1

    # umap requires the df to be encoded
    encoder = DDTransformer(df_new)
    edf = utilities.encode_dataframe(df_new, encoder)

    # transform the df and add distance information
    scaler = StandardScaler()
    reducer = umap.UMAP()
    edf_scaled = scaler.fit_transform(edf)
    embedding = reducer.fit_transform(edf_scaled)

    df_new[__X_COL] = embedding[:, 0]
    df_new[__Y_COL] = embedding[:, 1]
    df_new[__DIST_COL] = (
        (df_new[__X_COL] - df_new.iloc[pt_idx][__X_COL]) ** 2
        + (df_new[__Y_COL] - df_new.iloc[pt_idx][__Y_COL]) ** 2
    ) ** 0.5
    df_new[__INV_DIST_COL] = (1.0 / df_new[__DIST_COL]).replace(
        [np.inf, -np.inf, np.nan], 0
    )

    # filter targets if given
    if outcome and targets:
        df_new = df_new[df_new[outcome].isin(targets)]

    # solve on new df to find adjustable conditions based proximity to point
    solve_outcome = __INV_DIST_COL
    solve_target = "min" if inverse else "max"
    df_new_adj = df_new[adjustable + [solve_outcome]]

    rule = solve(df_new_adj, outcome=solve_outcome, target=solve_target, **kwargs)

    return rule
