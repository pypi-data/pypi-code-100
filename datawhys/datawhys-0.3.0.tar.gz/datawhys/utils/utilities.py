import json
from typing import Dict, List, Union

import numpy as np
import pandas as pd
import scipy.stats
from sklearn.metrics import (
    accuracy_score,
    log_loss,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    recall_score,
)
from sklearn.model_selection import KFold

from datawhys.core.frame import DataWhysFrame
from datawhys.core.series import DataWhysSeries
from datawhys.dd_transformer import DDTransformer

from .constants import MIN_SOLVER_SIZE, RULE_PREFIX
from .data import is_discrete


def has_enough_values(df, target_class, target_variable):
    col = df[target_variable]

    if is_discrete(col.dtype):
        size = col[col == target_class].shape[0]
    else:
        if col.std() == 0:
            return False
        size = col.shape[0]

    return size >= MIN_SOLVER_SIZE


def one_hot_encode(df: DataWhysFrame, cols: List[str]) -> DataWhysFrame:
    if cols is None:
        cols = []
    cols = [c for c in cols if len(df[c].unique()) <= 12]

    if cols:
        return DataWhysFrame(pd.get_dummies(df, columns=cols))
    else:
        return df


def encode_column(col: DataWhysSeries, encoder: DDTransformer) -> DataWhysSeries:
    encoded, encoded_col_label = encoder.original_to_encoded(col.name, col)
    ms_encoded = DataWhysSeries(encoded, name=encoded_col_label)

    # Need to change encoded nulls back to nulls
    ms_encoded.where(~col.reset_index(drop=True).isnull(), np.nan, inplace=True)

    return ms_encoded


def encode_value(
    dwf: DataWhysFrame, outcome: str, value: any, encoder: DDTransformer
) -> str:
    if not np.issubdtype(dwf[outcome].dtype, np.number):
        value_encoded = encode_column(DataWhysSeries([value], name=outcome), encoder)[0]
    else:
        value_encoded = value

    return value_encoded


def encode_dataframe(dfw: DataWhysFrame, encoder: DDTransformer) -> DataWhysFrame:
    """
    DOCSTRING
    :return: encoded DataWhysFrame,
    """
    encoded_dict = dict()

    for column, values in dfw.iteritems():
        encoded_col = encode_column(values, encoder)
        encoded_dict[encoded_col.name] = encoded_col

    encoded_dataframe = DataWhysFrame.from_dict(encoded_dict)

    return encoded_dataframe


def decode_column(col: DataWhysSeries, encoder: DDTransformer) -> DataWhysSeries:
    numeric_col_label = encoder._column_decoder[col.name]
    ms_decoded = encoder.encoded_to_original(numeric_col_label, col)

    return ms_decoded


def decode_value(
    col: DataWhysSeries, value: any, encoder: DDTransformer
) -> DataWhysSeries:
    numeric_col_label = encoder._column_decoder[col.name]
    ms_decoded = encoder.encoded_to_original(numeric_col_label, np.array([value]))

    return ms_decoded[0]


def decode_dataframe(dwf: DataWhysFrame, encoder: DDTransformer):
    decoded_dict = dict()
    for col, ser in dwf.iteritems():
        numeric_col_label = encoder._column_decoder[col]
        decoded_col = encoder.encoded_to_original_column(numeric_col_label)
        decoded_dict[decoded_col] = decode_column(ser, encoder)

    return DataWhysFrame.from_dict(decoded_dict)


def sample_if_needed(df, target_class, target_variable, random_state=1337):

    SAMPLING_SIZE = 2500
    SAMPLING_CAP = 3500

    if df.shape[0] > SAMPLING_CAP:

        was_sampled = True

        # if the outcome is not numeric, we might use oversampled outcomes and
        # the total number of points are less than 0.15 of the overall
        if not np.issubdtype(df[target_variable], np.number):
            # uniform stratified sampling across the outcome column
            # if no target class is specified
            if not target_class:
                df = (
                    df.groupby(target_variable, group_keys=False)
                    .apply(
                        lambda x: x.sample(
                            int(np.rint(SAMPLING_SIZE * x.shape[0] / df.shape[0]))
                        )
                    )
                    .sample(frac=1)
                    .reset_index(drop=True)
                )
            elif df[target_variable].value_counts()[target_class] / df.shape[0] < 0.15:
                # If they are, we will over sample them
                df = oversampled_result(
                    df, target_variable, target_class, SAMPLING_SIZE
                )
            elif df[target_variable].value_counts().shape[0] == 2:
                target_classes = df[target_variable].value_counts().index
                alternate_class = target_classes[
                    ~np.in1d(target_classes, target_class)
                ][0]
                if (
                    df[target_variable].value_counts()[alternate_class] / df.shape[0]
                    < 0.15
                ):
                    # If they are, we will over sample them
                    df = oversampled_result(
                        df, target_variable, alternate_class, SAMPLING_SIZE
                    )
                else:
                    df = df.sample(
                        SAMPLING_SIZE, random_state=random_state
                    ).reset_index(drop=True)
            else:
                df = df.sample(SAMPLING_SIZE, random_state=random_state).reset_index(
                    drop=True
                )
        else:
            df = df.sample(SAMPLING_SIZE, random_state=random_state).reset_index(
                drop=True
            )

    else:
        was_sampled = False

    return df, was_sampled


def oversampled_result(df, outcome, target_class, sampling_size):
    target_prob = 1 - (df[outcome] == target_class).sum() / df.shape[0]
    opposing_prob = 1 - target_prob
    pick_probabilities = np.where(
        df[outcome] == target_class, target_prob, opposing_prob
    )
    pick_probabilities = pick_probabilities / pick_probabilities.sum()
    # this sampling approach will choose every value of the underrepresented
    # class until they are all chosen
    df_sample = df.sample(
        sampling_size, random_state=1337, weights=pick_probabilities
    ).reset_index(drop=True)
    return df_sample


def decode_rule(rule: dict, encoder: DDTransformer) -> dict:
    rule_decoded = dict()

    for key, condition in rule.items():
        if key.startswith(RULE_PREFIX):
            # MetaWhys condition
            key_decoded = key
            condition_decoded = condition["lo"]
        elif isinstance(condition, str):
            # Discrete condition
            col_label = encoder._column_decoder[key]
            values_encoded = DataWhysSeries([condition])
            values_decoded = encoder.encoded_to_original(col_label, values_encoded)

            key_decoded = values_decoded.name
            condition_decoded = values_decoded[0]
        else:
            # Continuous condition
            col_label = encoder._column_decoder[key]
            values_encoded = DataWhysSeries(list(condition.values()))
            values_decoded = encoder.encoded_to_original(col_label, values_encoded)
            bounds_decoded = values_decoded.values.tolist()

            key_decoded = values_decoded.name
            condition_decoded = {"lo": bounds_decoded[0], "hi": bounds_decoded[1]}

        rule_decoded[key_decoded] = condition_decoded

    return rule_decoded


def encode_rule(rule: dict, encoder: DDTransformer) -> dict:
    rule_encoded = dict()

    for key, condition in rule.items():
        if isinstance(condition, str):
            # Discrete condition
            values = DataWhysSeries([condition])
            values_encoded = encoder.original_to_encoded(key, values)

            key_encoded = values_encoded[1]
            condition_encoded = values_encoded[0][0]
        else:
            # Continuous condition
            values = DataWhysSeries(list(condition.values()))
            values_encoded = encoder.original_to_encoded(key, values)

            bounds_encoded = values_encoded[0].tolist()

            key_encoded = values_encoded[1]
            condition_encoded = {"lo": bounds_encoded[0], "hi": bounds_encoded[1]}

        rule_encoded[key_encoded] = condition_encoded

    return rule_encoded


def apply_rule_to_df(df: pd.DataFrame, rule: dict):
    """
    fn that enables applying a rule learned on another database
    onto a database with the same column names

    rule: format {variable: {'low': low_value, 'high': high_value}}
    """

    def get_mask(df: pd.DataFrame, key: str, condition: Union[str, dict]):
        if isinstance(condition, dict):
            # Continuous condition
            try:
                lo = condition["lo"]
                hi = condition["hi"]

                mask = (df[key] >= lo) & (df[key] <= hi)
            except TypeError:
                raise TypeError(
                    """Attempted to apply a numerical condition to a
                        non-numerical dataframe column"""
                )
        else:
            # Discrete condition
            mask = df[key] == condition

        return mask

    if not rule:
        return df.drop(df.index)

    masks = np.all(
        np.array([get_mask(df, key, cond) for key, cond in rule.items()]), axis=0
    )
    return df[masks]


def get_stats(df: pd.DataFrame, outcome, target) -> dict:
    if df[outcome].dtype == np.object:
        values = (df[outcome] == target).astype(np.int)
    else:
        values = df[outcome].copy()
        if target == "min":
            values *= -1

    stats = {
        "mean": values.mean(),
        "std": values.std(ddof=0),
        "size": int(values.size),
        "size_above_mean": 0,
    }

    if values.mean() > 0:
        stats["size_above_mean"] = int((values >= values.mean()).sum())

    return stats


def calculate_score(sample_stats, pop_stats):
    if sample_stats["size"] == 0 or pop_stats["size"] == 0:
        score = 0
    else:
        score = (
            np.sqrt(sample_stats["size"])
            * (sample_stats["mean"] - pop_stats["mean"])
            / pop_stats["std"]
        )

    return score


def score_rule(dataset, rule, outcome: str, target: str):
    pop_stats = get_stats(dataset, outcome, target)
    df_rule = apply_rule_to_df(dataset, rule)
    sample_stats = get_stats(df_rule, outcome, target)

    return calculate_score(sample_stats, pop_stats)


def cross_validate_rule(rule, m_X, m_y, cv=3, score=None):
    if isinstance(cv, int) or isinstance(cv, float):
        cv = KFold(n_splits=cv, shuffle=True)

    val_scores = []
    val_sizes = []

    for val_index, _ in cv.split(m_X, m_y):
        X_val = m_X.iloc[val_index]
        y_val = m_y.iloc[val_index]
        dwf_val = DataWhysFrame(pd.concat((DataWhysFrame(y_val), X_val), axis=1))

        outcome = m_y.name
        target = m_y.target_class

        df_applied = apply_rule_to_df(dwf_val, rule)
        sample_stats = get_stats(df_applied, outcome, target)
        val_score = score_rule(dwf_val, rule, outcome, target)
        val_size = sample_stats["size"]

        val_scores.append(val_score)
        val_sizes.append(val_size)

    if score is not None:
        mse = np.mean((np.array(val_scores) - np.array(score)) ** 2)
    else:
        mse = None

    validation = {
        "scores": val_scores,
        "sizes": val_sizes,
        "avg_loss": mse,
    }

    return validation


def prettify_rule(ugly_rule, dataset):
    pretty_rule = dict()
    for col, bounds in ugly_rule.items():
        if is_discrete(dataset[col].dtype):
            pretty_rule[col] = {"discrete": bounds["low"]}
        else:
            pretty_rule[col] = bounds

    return pretty_rule


def model_report(y_true, y_pred):
    model_dict = {}
    # MAE and MSE are for numeric (float or int) loss functions
    if np.issubdtype(y_true.dtype, np.float64) or np.issubdtype(y_true.dtype, np.int64):
        try:
            model_dict["mean_abs_error"] = mean_absolute_error(y_true, y_pred)
        except Exception:
            model_dict["mean_abs_error"] = None
        try:
            model_dict["mean_sq_error"] = mean_squared_error(y_true, y_pred)
        except Exception:
            model_dict["mean_sq_error"] = None
    # log_loss is more for binary (either 0,1 or True, False (boolean))
    elif np.issubdtype(y_true.dtype, np.bool):
        try:
            model_dict["log_loss"] = log_loss(y_true, y_pred)
        except Exception:
            model_dict["log_loss"] = None
        try:
            model_dict["accuracy_score"] = accuracy_score(y_true, y_pred)
        except Exception:
            model_dict["accuracy_score"] = None
        try:
            model_dict["precision_score"] = precision_score(y_true, y_pred)
        except Exception:
            model_dict["precision_score"] = None
        try:
            model_dict["recall_score"] = recall_score(y_true, y_pred)
        except Exception:
            model_dict["recall_score"] = None
    # labeled or discrete data
    else:
        try:
            model_dict["precision_score"] = precision_score(
                y_true, y_pred, average=None
            )
        except Exception:
            model_dict["precision_score"] = None
        try:
            model_dict["recall_score"] = recall_score(y_true, y_pred, average=None)
        except Exception:
            model_dict["recall_score"] = None
    return model_dict


def write_rule_tree(dict_type_tree, file_handle):
    new_tree = dict()
    counter = 1
    for node, rule in dict_type_tree.items():
        if node == (0, "IN", 0, "IN"):
            rule["mapping"] = node
            new_tree["root"] = rule
        else:
            rule["mapping"] = node
            new_tree[counter] = rule
            counter += 1

    with open(file_handle, mode="w") as write_file:
        json.dump(new_tree, write_file)


def read_rule_tree(file_handle):
    with open(file_handle, "r") as read_file:
        return json.load(read_file)


def get_not_target(s: pd.Series, target: str) -> pd.Series:
    if s.dtype == np.object:
        not_target = np.where(s != target, "not_target", "target")
    else:
        not_target = s * -1.0

    return not_target


def get_readable_rules(
    rules: List[Dict], scores: List[float], sizes: List[int], outcome: str, target: str
):
    from IPython.display import display, Markdown

    for rule, score, size in zip(rules, scores, sizes):
        get_readable_rule(rule, score, size, outcome, target)
        display(Markdown("***"))


def get_readable_rule(rule: dict, score: float, size: int, outcome: str, target: str):
    from IPython.display import display, Markdown

    if not all((rule, score, size, outcome, target)):
        raise ValueError(
            """One or more required paramaters not provided.
                    - rule
                    - score
                    - size
                    - outcome
                    - target"""
        )

    rule = {"rule": rule, "score": score, "size": size}

    if outcome == "error":
        description = (
            f"The model is "
            f"{'least' if target == 'max' else 'most'} trustworthy when:"
        )
        closing = f"""In situations where these conditions are true
            the model does worse at predicting the outcome
            {(1 - scipy.stats.norm.sf(rule['score'])) * 100}% of the time."""
    else:
        description = f"**{outcome}** targeting **{target}** is most significant when:"
        closing = f"""In situations where these conditions are true,
            *{outcome}* is *{'maximized' if target == 'max' else "minimized"
        if target == "min" else target}*
            {(1 - scipy.stats.norm.sf(rule['score'])) * 100}% of the time."""
    display(Markdown(f"#### {description}"))
    cnt = 1
    for cond, interval in rule["rule"].items():
        if type(interval) == str:
            display(
                Markdown(
                    f"* **{cond}** is **{interval}** "
                    f"{'and' if cnt < len(rule['rule']) else ''}"
                )
            )
        elif type(interval) == dict and interval["lo"] == interval["hi"]:
            display(
                Markdown(
                    f"* **{cond}** is **{interval['lo']}** "
                    f"{'and' if cnt < len(rule['rule']) else ''}"
                )
            )
        else:
            display(
                Markdown(
                    f"* **{cond}** is between **{round(interval['lo'], 2)}** and "
                    f"**{round(interval['hi'], 2)}** "
                    f"{'and' if cnt < len(rule['rule']) else ''}"
                )
            )
        cnt += 1
    display(Markdown(closing))
    display(
        Markdown(
            f"`Details: Rule Z-Score="
            f"{round(rule['score'], 2)}, Rule Size={rule['size']}`"
        )
    )
