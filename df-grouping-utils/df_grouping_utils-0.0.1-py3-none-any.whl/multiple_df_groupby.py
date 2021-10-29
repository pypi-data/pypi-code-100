from typing import Callable, Union, List
import pandas as pd


def groupby_two_df(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    f: Callable,
    df1_group_colname: str = "group",
    df2_group_colname: str = "group",
    **kwargs
) -> Union[pd.Series, pd.DataFrame]:
    """Apply split apply combine to two pandas DataFrames

    Args:
        df1 (pd.DataFrame): First DataFrame
        df2 (pd.DataFrame): Second DataFrame
        f (Callable): Callable that takes two DataFrames as input
        df1_group_colname (str, optional): Label of the group column in df1. Defaults to "group".
        df2_group_colname (str, optional): Label of the group column in df2. Defaults to "group".

    Returns:
        Union[pd.Series, pd.DataFrame]: The results of the group by
    """
    groups_df1 = set(df1[df1_group_colname].unique())
    groups_df2 = set(df2[df2_group_colname].unique())
    groups_shared = groups_df1.intersection(groups_df2)
    results: List[pd.DataFrame] = []
    for group in groups_shared:
        df1_sub = df1.loc[df1[df1_group_colname] == group]
        df2_sub = df2.loc[df2[df2_group_colname] == group]
        group_result = f(df1_sub, df2_sub, **kwargs)
        group_result["group"] = group
        results.append(group_result)
    return pd.concat(results)
