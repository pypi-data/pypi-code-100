import numpy as np
import pandas as pd

from datawhys.datautils import apply_rule
from datawhys.dd_transformer import DDTransformer
from datawhys.utils import utilities
from datawhys.utils.data import is_continuous

from ._target import target_metrics


def score(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    rule: dict = None,
    population: pd.DataFrame = None,
):
    """Score a dataframe

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to score. If rule is set, then df should represent the original
        population. If population is set, then df should represent the sample to score.

    outcome : str, default=None
        Which column to use as the outcome for the score (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    rule: dict, default=None
        The solver rule to use for scoring. This or population must be set, but not
        both. If set, df should be the population dataset

    population: pd.DataFrame, default=None
        The population dataset to base the score off of. If set, df should be the sample
        dataset.

    Returns
    -------
    score: float
        The score of the sample and population

    Examples
    --------
    >>> from datawhys.datasets import load_titanic
    >>> from datawhys import metrics
    >>> df = load_titanic()
    >>> outcome = 'survived'
    >>> target = "Died"
    >>> rule = {
        'class': {'lo': 2, 'hi': 3},
        'sex': 'male',
        'parch': {'lo': 0, 'hi': 0},
        'ticketnumber': {'lo': 2151.0, 'hi': 3101280.0}
        }
    >>> metrics.score(df, outcome, target, rule)
    13.001719638805223
    """
    # Quick checks to make sure that one of rule and population is set.
    if rule is None and population is None:
        raise ValueError("one of `rule` or `population` must be set")

    if rule is not None and population is not None:
        raise ValueError("only one of `rule` or `population` may be set")

    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        target = df[outcome].iloc[0] if df[outcome].dtype == np.object else "max"

    if population is not None:
        sample = df

    if rule is not None:
        population = df
        sample = apply_rule(df, rule)

    # Encode our outcome column if the outcome column is continuous
    if is_continuous(population[outcome].dtype):
        encoder = DDTransformer(population)
        population = utilities.encode_dataframe(population, encoder)
        sample = utilities.encode_dataframe(sample, encoder)

        # Encode outcome. Target not needed as this is continuous
        outcome = encoder.original_to_encoded_column(outcome)

    # Get metrics for population and sample
    pop_metrics = target_metrics(population[outcome], target)
    smp_metrics = target_metrics(sample[outcome], target)

    # Return 0 if we our size is 0
    if (
        smp_metrics["size"] == 0
        or pop_metrics["size"] == 0
        or smp_metrics["mean"] == pop_metrics["mean"]
        or pop_metrics["std"] == 0
    ):
        return 0

    return (
        np.sqrt(smp_metrics["size"])
        * (smp_metrics["mean"] - pop_metrics["mean"])
        / pop_metrics["std"]
    )


def _exclude_key(a: dict, key) -> dict:
    return {k: v for k, v in a.items() if k != key}


def partial_scores(
    df: pd.DataFrame, rule: dict, outcome: str = None, target: str = None,
) -> dict:
    """Calculates the partial score for each condition in a rule.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to score. The df should represent the original
        population.

    rule: dict
        The solver rule to use for scoring.

    outcome : str, default=None
        Which column to use as the outcome for the score (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.


    Returns
    -------
    scores: dict
        A dictionary of scores for each key/condition in the rule


    Examples
    --------
    >>> from datawhys.datasets import load_titanic
    >>> from datawhys import metrics
    >>> df = load_titanic()
    >>> outcome = 'sex'
    >>> target = 'male'
    >>> rule = {
            'class': {'lo': 2, 'hi': 3},
            'sex': 'male',
            'parch': {'lo': 0, 'hi': 0},
            'ticketnumber': {'lo': 2151.0, 'hi': 3101280.0}
        }
    >>> metrics.partial_scores(df, rule, outcome, target)
    {
        'class': -2.175216344281214,
        'sex': 11.817078598704317,
        'parch': -1.2967726194944724,
        'ticketnumber': -0.8020530610406418
    }
    """
    if not rule:
        raise ValueError("An empty rule is not permitted")

    base_score = score(df, outcome=outcome, target=target, rule=rule)

    if len(rule.keys()) == 1:
        key = list(rule.keys())[0]
        return {key: base_score}

    scores = {}
    for key, cond in rule.items():
        subrule = _exclude_key(rule, key)
        subscore = score(df, outcome=outcome, target=target, rule=subrule)

        scores[key] = base_score - subscore

    return scores


def feature_signals(
    df: pd.DataFrame, outcome: str = None, target: str = None, **solve_params,
):
    """
    Calculate the signal/strength of each variable in a dataframe.

    Parameters
    ----------
    df: Pandas DataFrame
        Dataframe containing the Outcome Feature and Independent Feature variables.

    outcome: str (optional), default=None
        The label of the dependent variable used for learning.  If None, the first
        column is used.

    target: str (optional), default=None
        The target class of the outcome if discrete.  'min' or 'max' if continuous.

    **solve_params: any
        Parameters to pass on to `solve`

    Returns
    -------
    signals: dict
        A dictionary mapping each variable with their score and condition
        leading to the score.  This is achieved by doing a one dimensional
        solve on each variable.

    Examples
    --------
    >>> from datawhys.datasets import load_titanic
    >>> df = load_titanic()
    >>> metrics.feature_signals(df, 'survived', "Died")
    {
        'sex': {'condition': 'male', 'score': 11.408374681094228},
        'fare': {'condition': {'lo': 0.0, 'hi': 10.4625}, 'score': 7.271397191659396},
        'class': {'condition': {'lo': 3, 'hi': 3}, 'score': 6.932868263529628},
        'ticketnumber': {'condition': {'lo': 345763.0, 'hi': 366713.0},
        'score': 6.411057911385609},
        'embarked': {'condition': 'S', 'score': 3.0651604266866816},
        'parch': {'condition': {'lo': 0, 'hi': 0}, 'score': 3.033943859578286},
        'sibsp': {'condition': {'lo': 0, 'hi': 0}, 'score': 2.153140749023159},
        'age': {'condition': {'lo': 17.0, 'hi': 28.5}, 'score': 0.9015429873144141},
        'name': {'condition': {}, 'score': 0},
        'ticket': {'condition': {}, 'score': 0},
        'ticketcode': {'condition': {}, 'score': 0},
        'cabin': {'condition': {}, 'score': 0},
        'cabinsection': {'condition': {}, 'score': 0},
        'boat': {'condition': {}, 'score': 0},
        'body': {'condition': {}, 'score': 0},
        'homedest': {'condition': {}, 'score': 0}
    }
    """
    from ..solver import solve

    if not outcome:
        outcome = df.columns[0]

    results = {}

    for col in df.columns:
        if col == outcome:
            continue

        df_one_dim = df[[col, outcome]]

        rule = solve(df_one_dim, outcome=outcome, target=target, **solve_params)
        rule_score = score(df, outcome, target, rule) if rule else 0

        results[col] = {"condition": rule[col] if rule else {}, "score": rule_score}

    sorted_results = {
        k: v
        for k, v in sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)
    }

    return sorted_results
