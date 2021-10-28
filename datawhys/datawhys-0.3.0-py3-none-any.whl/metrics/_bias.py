import numpy as np
import pandas as pd

from datawhys.datautils import apply_rule


def bias(df: pd.DataFrame, bias_variables: list = None, rule: dict = None,) -> dict:
    """Score a rule to detect bias dataframe. Used to determine potential issues with
    fairness.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to score. If rule is set, then df should represent the original
        population. If population is set, then df should represent the sample to score.

    bias_variables : list, default=None
        Which columns to use as the columns to evaluate for potential bias

    rule: dict, default=None
        The solver rule to use for scoring. This or population must be set, but not
        both. If set, df should be the population dataset.

    Returns
    -------
    bias_scores: dict
        A dictionary of the shift in each of the selected bias variables

        For continuous variables, shows the mean, std, min, max, and percentiles
        For categorical variables, shows the deltas and ratios of classes between
        the population and sample segments

    Examples
    --------
    >>> from datawhys import metrics
    >>> from datawhys.datasets import load_titanic
    >>> df = load_titanic()
    >>> bias_variables = ['sex', 'age']
    >>> rule = {
        'class': {'lo': 2, 'hi': 3}, 'sex': 'male',
        'parch': {'lo': 0, 'hi': 0},
        'ticketnumber': {'lo': 2151.0, 'hi': 3101280.0}
        }
    >>> datawhys.metrics.bias(df, bias_variables, rule)
    {
        "sex": {
            "counts_population": {
                "male": 842,
                "female": 466
            },
            "ratio_population": {
                "male": 0.6437308868501529,
                "female": 0.3562691131498471
            },
            "counts_sample": {
                "male": 513,
                "female": 0
            },
            "ratio_sample": {
                "male": 1,
                "female": 0
            },
            "ratio_difference": {
                "male": 0.3562691131498471,
                "female": -0.3562691131498471
            },
            "ratio_percent_change": {
                "male": 55.344418052256536,
                "female": -100
            }
        },
        "age": {
            "description_population": {
                "count": 1045,
                "mean": 29.881977703349285,
                "std": 14.420375254531496,
                "min": 0.1667,
                "25%": 21,
                "50%": 28,
                "75%": 39,
                "max": 80
            },
            "description_sample": {
                "count": 383,
                "mean": 29.66318537859008,
                "std": 10.92394589950367,
                "min": 11,
                "25%": 22,
                "50%": 27,
                "75%": 34,
                "max": 74
            },
            "description_delta": {
                "count": -662,
                "mean": -0.21879232475920674,
                "std": -3.4964293550278267,
                "min": 10.8333,
                "25%": 1,
                "50%": -1,
                "75%": -5,
                "max": -6
            },
            "description_ratio": {
                "count": -0.6334928229665071,
                "mean": -0.007321882337616659,
                "std": -0.2424645193563253,
                "min": 64.98680263947212,
                "25%": 0.04761904761904767,
                "50%": -0.0357142857142857,
                "75%": -0.1282051282051282,
                "max": -0.07499999999999996
            }
        }
    }

    """
    if rule is not None:
        population = df
        sample = apply_rule(df, rule)
    else:
        return TypeError("Must include a rule")

    ret_dict = {}

    for v in bias_variables:

        # check if bias variable is numeric or not
        if np.issubdtype(population[v].dtype, np.number):
            pop_cont = population[v].describe()
            sample_cont = sample[v].describe()
            # create return dictionary
            ret_dict[v] = {
                "description_population": pop_cont.to_dict(),
                "description_sample": sample_cont.to_dict(),
                "description_delta": (sample_cont - pop_cont).to_dict(),
                # subtract one to have +/- percentages
                "description_ratio": (sample_cont / pop_cont - 1).to_dict(),
            }
        else:
            # create return dataframe and then set column name
            ret_df = pd.DataFrame(population[v].value_counts())
            ret_df.columns = ["counts_population"]

            ret_df["ratio_population"] = (
                ret_df["counts_population"] / ret_df["counts_population"].sum()
            )
            ret_df["counts_sample"] = pd.DataFrame(sample[v].value_counts())
            ret_df["ratio_sample"] = (
                ret_df["counts_sample"] / ret_df["counts_sample"].sum()
            )
            ret_df = ret_df.fillna(0)
            ret_df["ratio_difference"] = (
                ret_df["ratio_sample"] - ret_df["ratio_population"]
            )
            ret_df["ratio_percent_change"] = (
                ret_df["ratio_sample"] / ret_df["ratio_population"] - 1.0
            ) * 100.0

            ret_dict[v] = ret_df.to_dict()

    return ret_dict
