import numpy as np
import pandas as pd


def target_metrics(s: pd.Series, target: str = None) -> dict:
    """Get metrics for a target within a column

    Parameters
    ----------
    s : pd.Series
        The series to calculate metrics for

    target: str, default=None
        The class in s to calculate metrics for. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    Examples
    --------
    >>> from datawhys.datasets import load_titanic
    >>> from datawhys import metrics
    >>> df = load_titanic()
    >>> series = df['survived']
    >>> target = "Died"
    >>> metrics.target_metrics(series, target)
    {
        'mean': 0.617737003058104,
        'std': 0.48594032361072487,
        'size': 1308,
        'size_above_mean': 808
    }
    """
    if target is None:
        target = s[0] if s.dtype == np.object else "max"

    if s.dtype == np.object:
        values = (s == target).astype(np.int)
    else:
        values = s
        if target == "min":
            values *= -1

    mean = values.mean() if values.size > 0 else 0
    above_mean = int((values >= mean).sum()) if mean > 0 else 0

    return {
        "mean": mean,
        "std": values.std(ddof=0) if values.size > 0 else 0,
        "size": int(values.size),
        "size_above_mean": above_mean,
    }
