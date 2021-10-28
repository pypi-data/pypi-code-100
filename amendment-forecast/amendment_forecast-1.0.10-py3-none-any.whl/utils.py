import pandas as pd
from sklearn import metrics

from amendment_forecast.models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME
# from models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME


def create_time_series_from_records(df: pd.DataFrame, column_name: str, operation: str, period_format: str = None):
    if period_format:
        df[DATE_COLUMN_NAME] = df[DATE_COLUMN_NAME].dt.strftime(period_format)
        if period_format == "%Y-%W":
            df[DATE_COLUMN_NAME] = pd.to_datetime(df[DATE_COLUMN_NAME].map(lambda x: str(x) + "-0"), format="%Y-%W-%w")
        else:
            df[DATE_COLUMN_NAME] = pd.to_datetime(df[DATE_COLUMN_NAME])
    time_series_df = df.groupby(DATE_COLUMN_NAME, as_index=False).agg({column_name: operation})
    time_series_df.rename(columns={column_name: VALUE_COLUMN_NAME}, inplace=True)

    return time_series_df


def get_model_statistics(y: pd.Series, yhat: pd.Series):
    scores = {
        "mape": metrics.mean_absolute_percentage_error(y, yhat),
        "mae": metrics.mean_absolute_error(y, yhat),
        "mse": metrics.mean_squared_error(y, yhat),
        "rmse": metrics.mean_squared_error(y, yhat, squared=False),
        "r2": metrics.r2_score(y, yhat),
        "medae": metrics.median_absolute_error(y, yhat)
    }

    return scores


def consolidate_scores(metrics: dict, average_actual: float):
    metrics["accuracy_mape"] = 1 - metrics["mape"]
    metrics["accuracy_rmse"] = 1 - (metrics["rmse"] / average_actual)
    metrics["accuracy_mae"] = 1 - (metrics["mae"] / average_actual)
    metrics["accuracy_medae"] = 1 - (metrics["medae"] / average_actual)

    metrics["ae_composite"] = (metrics["accuracy_mae"] + metrics["accuracy_medae"]) / 2
    metrics["accuracy"] = (metrics["ae_composite"] + metrics["accuracy_mape"] + metrics["accuracy_rmse"]) / 3

    r2 = metrics["r2"]
    if r2 > 0.75:
        confidence = "High"
    elif r2 > 0.5:
        confidence = "Medium"
    else:
        confidence = "Low"
    metrics["confidence"] = confidence

    return_metrics = ["accuracy_mape", "accuracy_rmse", "accuracy_mae", "accuracy_medae", "accuracy", "confidence"]

    return {metric: metrics[metric] for metric in return_metrics}
