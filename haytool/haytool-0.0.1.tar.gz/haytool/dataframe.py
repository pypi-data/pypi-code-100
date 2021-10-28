import pandas as pd


def custompivot(in_info):
    """Summarize series or dataframe. Returns count and percent distribution

    Args:
        in_info (Series or DataFrame): [description]

    Returns:
        [type]: [description]
    """
    if type(in_info) == pd.core.series.Series:
        if (type(in_info.iloc[0]) == int or type(in_info.iloc[0]) == float) and len(in_info.index) > 10:
            counts = in_info.value_counts(dropna=False, bins=10)
        else:
            counts = in_info.value_counts(dropna=False)
    elif type(in_info) == pd.core.frame.DataFrame:
        counts = in_info.groupby(list(in_info.columns)).size()
    else:
        counts = 0
    percent = counts / counts.sum()
    fmt = '{:.2%}'.format
    output = pd.DataFrame({'counts': counts, 'percent': percent.map(fmt)})
    return output
