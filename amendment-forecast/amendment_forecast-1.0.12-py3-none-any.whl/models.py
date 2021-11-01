# Class to extend for each model

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

from fbprophet import Prophet
from greykite.framework.templates.autogen.forecast_config import ForecastConfig, MetadataParam, ModelComponentsParam, EvaluationPeriodParam
from greykite.framework.templates.forecaster import Forecaster
from greykite.framework.templates.model_templates import ModelTemplateEnum
from xgboost import XGBRegressor
from sklearn.ensemble import RandomForestRegressor
from statsmodels.tsa.statespace.sarimax import SARIMAX

from amendment_forecast import utils
# import utils

# TODO Define loss_functions enum
LOSS_FUNCTIONS = [
    "MSE",
    "MAE",
    "MedAE",
    "MAPE",
    "MedAPE",
    "R2"
]
DATE_COLUMN_NAME = "period"
VALUE_COLUMN_NAME = "y"


class BaseModel:
    """Base class for models to run as part of ensemble"""

    def __init__(self) -> None:
        pass

    def run(self, dataframe: pd.DataFrame, **kwargs) -> tuple:
        pass

    def evaluate(self, dataframe: pd.DataFrame, train_end_date: datetime, frequency: str,
                 forecast_period_list: list) -> dict:
        """Function to evaluate the performance of the model against a particular dataset"""
        actual, predicted, forecast = self.run(
            dataframe=dataframe,
            train_end=train_end_date,
            frequency=frequency,
            forecast_period_list=forecast_period_list)
        result_package = utils.get_model_statistics(y=actual, yhat=predicted)
        result_package.update(utils.consolidate_scores(result_package, actual.mean()))
        result_package["name"] = self.__name__
        result_package["forecast_dataframe"] = pd.DataFrame(
                index=pd.Series(forecast.index),
                data={f"forecast_values_{self.__name__}": pd.Series(forecast).values})
        result_package["train_dataframe"] = pd.DataFrame(
                index=pd.Series(actual.index),
                data={
                    f"actual_values_{self.__name__}": actual.values,
                    f"predicted_values_{self.__name__}": predicted
                })

        return result_package


class GreyKite(BaseModel):

    def __init__(self):
        """Initializes greykite model"""
        super().__init__()
        self.__name__ = "GreyKite"
        self.metadata = MetadataParam(
            time_col=DATE_COLUMN_NAME,
            value_col=VALUE_COLUMN_NAME)

    def run(self, dataframe: pd.DataFrame, train_end: datetime, frequency: str, forecast_period_list: list) -> tuple:
        """Runs rolling prediction using the model to return actual and predicted values

        Args:
            dataframe: time series dataframe to evaluate the model on

        Returns:
            dataframes with actual and predicted values
        """
        forecaster = Forecaster()
        self.metadata.freq = frequency
        forecast_horizon=len(forecast_period_list)
        if forecast_horizon >= (len(dataframe) / 3):
            test_horizon = (len(dataframe) / 3) - 1
        else:
            test_horizon = forecast_horizon
        result = forecaster.run_forecast_config(  # result is also stored as `forecaster.forecast_result`.
            df=dataframe,
            config=ForecastConfig(
                model_components_param=ModelComponentsParam(seasonality={"yearly_seasonality": 40}),
                evaluation_period_param=EvaluationPeriodParam(test_horizon=test_horizon),
                model_template=ModelTemplateEnum.SILVERKITE.name,
                coverage=0.95,
                metadata_param=self.metadata,
                forecast_horizon=len(forecast_period_list)
            )
        )
        backtest = result.backtest.df_test[~result.backtest.df_test["actual"].isnull()]
        backtest = backtest[backtest[DATE_COLUMN_NAME] > train_end]
        backtest = backtest.set_index("period")
        forecast_df = result.forecast.df
        forecast_df = forecast_df.set_index("period")
        mask = forecast_df["actual"].isnull()
        forecast = forecast_df.loc[mask, "forecast"]

        return backtest["actual"], backtest["forecast"], forecast


class FBProphet(BaseModel):

    def __init__(self):
        """Initializes prophet model"""
        super().__init__()
        self.__name__ = "FBProphet"

    def run(self, dataframe: pd.DataFrame, train_end: datetime, frequency: str, forecast_period_list: list) -> tuple:
        """Runs rolling prediction using the model to return actual and predicted values

        Args:
            dataframe: time series dataframe to evaluate the model on

        Returns:
            dataframes with actual and predicted values
        """
        df = dataframe.rename(columns={DATE_COLUMN_NAME: "ds", VALUE_COLUMN_NAME: "y"})

        model = Prophet(yearly_seasonality=20)
        model.fit(df, iter=100)

        future = model.make_future_dataframe(periods=len(forecast_period_list), freq=frequency)
        forecast = model.predict(future)
        forecast = forecast.rename(columns={"ds": DATE_COLUMN_NAME}).set_index(DATE_COLUMN_NAME)

        df_forecast = pd.merge(dataframe.set_index(DATE_COLUMN_NAME), forecast, how="outer", left_index=True, right_index=True)
        df_train = df_forecast[~df_forecast[VALUE_COLUMN_NAME].isnull()]
        df_forecast = df_forecast[df_forecast[VALUE_COLUMN_NAME].isnull()]

        return df_train[VALUE_COLUMN_NAME], df_train["yhat"], df_forecast["yhat"]


class Naive(BaseModel):

    def __init__(self):
        """Initializes naive model"""
        super().__init__()
        self.__name__ = "Naive"
        self.growth_comparison_period_in_years = 1
        self.minimum_training_years = 2

    def run(self, dataframe: pd.DataFrame, train_end: datetime, frequency: str, forecast_period_list: list) -> tuple:
        # Determine training and testing periods to create test and training dataframes
        comparison_period_relativedelta = relativedelta(years=self.growth_comparison_period_in_years)
        train_mask = dataframe[DATE_COLUMN_NAME] <= train_end
        dataframe_test = dataframe[~train_mask]

        def run_prediction(prediction_date, frequency):
            base_growth_period_start = prediction_date - (2 * comparison_period_relativedelta)
            comparison_growth_period_start = prediction_date - comparison_period_relativedelta

            # Calculate base period totals
            base_growth_period_mask = \
                (dataframe[DATE_COLUMN_NAME] >= base_growth_period_start) & \
                (dataframe[DATE_COLUMN_NAME] < comparison_growth_period_start)
            base_growth_period_sum = dataframe.loc[base_growth_period_mask, VALUE_COLUMN_NAME].sum()

            # Calculate comparison period totals
            comparison_growth_period_mask = \
                (dataframe[DATE_COLUMN_NAME] >= comparison_growth_period_start) & \
                (dataframe[DATE_COLUMN_NAME] < prediction_date)
            comparison_growth_period_sum = dataframe.loc[comparison_growth_period_mask, VALUE_COLUMN_NAME].sum()
            # Determine growth_rate as the total change in volume from the base period to the comparison period
            growth_rate = comparison_growth_period_sum / base_growth_period_sum

            # Determine value to use as the base for the estimation
            if frequency == "W-MON":
                comparison_growth_period_start = comparison_growth_period_start - relativedelta(days=(comparison_growth_period_start.weekday()))
            previous_value_mask = dataframe[DATE_COLUMN_NAME] == comparison_growth_period_start
            previous_value = dataframe.loc[previous_value_mask, VALUE_COLUMN_NAME].sum()

            return previous_value * growth_rate

        # Loop through individual values
        actual = []
        predicted = []
        for index, row in dataframe_test.iterrows():
            # Determine window to evaluate against for the test datapoint
            prediction_date = row[DATE_COLUMN_NAME]
            predicted_value = run_prediction(prediction_date, frequency)

            # Save prediction
            actual.append(dataframe.loc[index, VALUE_COLUMN_NAME])
            predicted.append(predicted_value)

        forecast = []
        for timestamp in forecast_period_list:
            forecast_value = run_prediction(timestamp, frequency)
            forecast.append(forecast_value)
            new_row = pd.DataFrame({DATE_COLUMN_NAME: [timestamp], "yhat": [forecast_value]})
            dataframe = pd.concat([dataframe, new_row]).reset_index(drop=True)
            mask = dataframe[VALUE_COLUMN_NAME].isnull()
            dataframe.loc[mask, VALUE_COLUMN_NAME] = dataframe.loc[mask, "yhat"]

        dataframe_test["predicted"] = predicted
        dataframe_test = dataframe_test.set_index("period")
        dataframe_test = dataframe_test[np.isfinite(dataframe_test).all(axis=1)]

        dataframe = dataframe.set_index("period")

        return dataframe_test[VALUE_COLUMN_NAME], dataframe_test["predicted"], dataframe["yhat"]


class XGBoost(BaseModel):
    OBJECTIVE = "reg:squarederror"
    N_ESTIMATORS = 100
    PREVIOUS_PERIODS = 0

    def __init__(self):
        """Initializes xgboost model"""
        super().__init__()
        self.__name__ = "XGBoost"

    def create_time_series_features(self, time_series_df):
        result_df = time_series_df.copy()
        # # Add previous year values for yearly seasonality
        # previous_year_df = result_df.reset_index()
        # previous_year_df = previous_year_df.drop(columns="period")
        # previous_year_df["year"] = previous_year_df["year"] + 1
        # result_df = pd.merge(result_df, previous_year_df, how="left", on=["year", "period_number"], suffixes=("", "_previous"))
        for ii in range(1, self.PREVIOUS_PERIODS):
            # Create recent lag periods
            result_df[f"{VALUE_COLUMN_NAME}_{ii}"] = time_series_df[VALUE_COLUMN_NAME].shift(ii)
        result_df.dropna(inplace=True)

        return result_df

    def step_forecast(self, train_df: pd.DataFrame, test_x: pd.DataFrame, feature_columns: list):
        # fit a xgboost model and make a one step prediction
        # split into input and output columns
        train_x = train_df[feature_columns]
        train_y = train_df[VALUE_COLUMN_NAME]
        # fit model
        model = XGBRegressor(objective=self.OBJECTIVE, n_estimators=self.N_ESTIMATORS)
        model.fit(train_x, train_y)

        # make a one-step prediction
        yhat = model.predict(test_x)

        return yhat[0]

    def full_forecast(self, train_df, feature_columns, forecast_period_list, frequency):
        # fit an xgboost model and make a prediction for the full forecast_horizon
        # split into input and output columns
        train_x = train_df[feature_columns]
        train_y = train_df[VALUE_COLUMN_NAME]

        # fit model
        model = XGBRegressor(objective=self.OBJECTIVE, n_estimators=self.N_ESTIMATORS)
        model.fit(train_x, train_y)

        cc = 0
        previous_record = train_df.rename(columns={"y": "y_0"}).iloc[-1]
        predictions = {}
        for period in forecast_period_list:
            # Initialize previous period
            if cc == 0:
                test_record = previous_record.copy()
                # Update period IDs
                period_id_columns = [col for col in previous_record.index.values if "_" not in col]
                test_record[period_id_columns] = 0
                if frequency == "W-MON":
                    period_id = forecast_period_list[cc].isocalendar()[1]
                else:
                    period_id = forecast_period_list[cc].month
                test_record[str(period_id)] = 1
            else:
                # Copy previous record and update period_id
                previous_record = test_record.copy()
                # Update period IDs
                test_record[str(period_id)] = 0
                if frequency == "W-MON":
                    period_id = forecast_period_list[cc].isocalendar()[1]
                else:
                    period_id = forecast_period_list[cc].month
                test_record[str(period_id)] = 1
            # Update previous values
            for ii in range(0, self.PREVIOUS_PERIODS):
                test_record[f"y_{ii + 1}"] = previous_record[f"y_{ii}"]

            test_x = pd.DataFrame(test_record[feature_columns]).T

            # Run Forecast
            prediction = model.predict(test_x)
            test_record["y_0"] = prediction
            predictions[period] = prediction[0]

            cc += 1
        predictions = pd.Series(predictions)

        return predictions

    def run(self, dataframe: pd.DataFrame, train_end: datetime, frequency: str,
            forecast_period_list: pd.DataFrame) -> tuple:
        dataframe = dataframe.copy()

        # Prepare dataframe
        if frequency == "W-MON":
            self.PREVIOUS_PERIODS = 53
            dataframe.set_index("period", inplace=True)
            dataframe = dataframe.asfreq(frequency)
            dataframe["year"] = dataframe.index.year
            dataframe["period_number"] = dataframe.index.isocalendar().week.astype(str)
            dataframe = self.create_time_series_features(dataframe)
        else:
            self.PREVIOUS_PERIODS = 3
            dataframe.set_index("period", inplace=True)
            dataframe = dataframe.asfreq(frequency)
            dataframe["period_number"] = dataframe.index.month.astype(str)
            dataframe = self.create_time_series_features(dataframe)
        period_indexes = pd.get_dummies(dataframe.period_number)
        dataframe = pd.concat([dataframe, period_indexes], axis=1).drop(columns=["period_number"])

        predicted = []
        # Split into train and test
        train_mask = dataframe.index <= train_end
        train = dataframe[train_mask]
        test = dataframe[~train_mask]
        feature_columns = list(set(dataframe.columns) - set(VALUE_COLUMN_NAME))

        # Step over each time period and get result
        for index, row in test.iterrows():
            # split test row into input and output columns
            X, y = pd.DataFrame(row[feature_columns]).T, row[VALUE_COLUMN_NAME]

            # fit model on history and make a prediction
            yhat = self.step_forecast(train, X, feature_columns)

            # store forecast in list of predictions
            predicted.append(yhat)

            # add actual observation to history for the next loop
            train = pd.concat([train, pd.DataFrame(row).T])

        # Run full forecast
        forecast_predictions = self.full_forecast(dataframe, feature_columns, forecast_period_list, frequency)

        return test[VALUE_COLUMN_NAME], predicted, forecast_predictions


class RandomForest(BaseModel):
    N_ESTIMATORS = 100
    PREVIOUS_PERIODS = 0

    def __init__(self):
        """Initializes random forest model"""
        super().__init__()
        self.__name__ = "RandomForest"

    def create_time_series_features(self, time_series_df):
        result_df = time_series_df.copy()
        # # Add previous year values for yearly seasonality
        # previous_year_df = result_df.reset_index()
        # previous_year_df = previous_year_df.drop(columns="period")
        # previous_year_df["year"] = previous_year_df["year"] + 1
        # result_df = pd.merge(result_df, previous_year_df, how="left", on=["year", "period_number"], suffixes=("", "_previous"))
        for ii in range(1, self.PREVIOUS_PERIODS):
            # Create recent lag periods
            result_df[f"{VALUE_COLUMN_NAME}_{ii}"] = time_series_df[VALUE_COLUMN_NAME].shift(ii)
        result_df.dropna(inplace=True)

        return result_df

    def step_forecast(self, train_df: pd.DataFrame, test_x: pd.DataFrame, feature_columns: list):
        # fit a rf model and make a one step prediction
        # split into input and output columns
        train_x = train_df[feature_columns]
        train_y = train_df[VALUE_COLUMN_NAME]
        # fit model
        model = RandomForestRegressor(n_estimators=self.N_ESTIMATORS)
        model.fit(train_x, train_y)

        # make a one-step prediction
        yhat = model.predict(test_x)

        return yhat[0]

    def full_forecast(self, train_df, feature_columns, forecast_period_list, frequency):
        # fit an xgboost model and make a prediction for the full forecast_horizon
        # split into input and output columns
        train_x = train_df[feature_columns]
        train_y = train_df[VALUE_COLUMN_NAME]

        # fit model
        model = RandomForestRegressor(n_estimators=self.N_ESTIMATORS)
        model.fit(train_x, train_y)

        cc = 0
        previous_record = train_df.rename(columns={"y": "y_0"}).iloc[-1]
        predictions = {}
        for period in forecast_period_list:
            # Initialize previous period
            if cc == 0:
                test_record = previous_record.copy()
                # Update period IDs
                period_id_columns = [col for col in previous_record.index.values if "_" not in col]
                test_record[period_id_columns] = 0
                if frequency == "W-MON":
                    period_id = forecast_period_list[cc].isocalendar()[1]
                else:
                    period_id = forecast_period_list[cc].month
                test_record[str(period_id)] = 1
            else:
                # Copy previous record and update period_id
                previous_record = test_record.copy()
                # Update period IDs
                test_record[str(period_id)] = 0
                if frequency == "W-MON":
                    period_id = forecast_period_list[cc].isocalendar()[1]
                else:
                    period_id = forecast_period_list[cc].month
                test_record[str(period_id)] = 1
            # Update previous values
            for ii in range(0, self.PREVIOUS_PERIODS):
                test_record[f"y_{ii + 1}"] = previous_record[f"y_{ii}"]

            test_x = pd.DataFrame(test_record[feature_columns]).T

            # Run Forecast
            prediction = model.predict(test_x)
            test_record["y_0"] = prediction
            predictions[period] = prediction[0]

            cc += 1
        predictions = pd.Series(predictions)

        return predictions

    def run(self, dataframe: pd.DataFrame, train_end: datetime, frequency: str,
            forecast_period_list: pd.DataFrame) -> tuple:
        dataframe = dataframe.copy()

        # Prepare dataframe
        if frequency == "W-MON":
            self.PREVIOUS_PERIODS = 53
            dataframe.set_index("period", inplace=True)
            dataframe = dataframe.asfreq(frequency)
            dataframe["year"] = dataframe.index.year
            dataframe["period_number"] = dataframe.index.isocalendar().week.astype(str)
            dataframe = self.create_time_series_features(dataframe)
        else:
            self.PREVIOUS_PERIODS = 3
            dataframe.set_index("period", inplace=True)
            dataframe = dataframe.asfreq(frequency)
            dataframe["period_number"] = dataframe.index.month.astype(str)
            dataframe = self.create_time_series_features(dataframe)
        period_indexes = pd.get_dummies(dataframe.period_number)
        dataframe = pd.concat([dataframe, period_indexes], axis=1)

        predicted = []
        # Split into train and test
        train_mask = dataframe.index <= train_end
        train = dataframe[train_mask]
        test = dataframe[~train_mask]
        feature_columns = list(set(dataframe.columns) - set(VALUE_COLUMN_NAME))

        # Step over each time period and get result
        for index, row in test.iterrows():
            # split test row into input and output columns
            X, y = pd.DataFrame(row[feature_columns]).T, row[VALUE_COLUMN_NAME]

            # fit model on history and make a prediction
            yhat = self.step_forecast(train, X, feature_columns)

            # store forecast in list of predictions
            predicted.append(yhat)

            # add actual observation to history for the next loop
            train = pd.concat([train, pd.DataFrame(row).T])

        # Run full forecast
        forecast_predictions = self.full_forecast(dataframe, feature_columns, forecast_period_list, frequency)

        return test[VALUE_COLUMN_NAME], predicted, forecast_predictions


class SARIMA(BaseModel):

    def __init__(self):
        """Initializes SARIMA model"""
        super().__init__()
        self.__name__ = "SARIMA"

    def run(self, dataframe: pd.DataFrame, train_end: datetime, frequency: str, forecast_period_list: list) -> tuple:
        dataframe = dataframe.copy()
        # Prepare dataframe
        dataframe.set_index("period", inplace=True)
        dataframe = dataframe.asfreq(frequency)
        if frequency == "W-MON":
            m = 52.5
        elif frequency == "MS":
            m = 12

        # Split into train and test
        train_mask = dataframe.index <= train_end
        train = dataframe[train_mask]
        test = dataframe[~train_mask]

        # Create step-forward validation
        predicted = pd.DataFrame()
        previous_index = 0
        period_horizon = len(forecast_period_list)
        for ii in range(period_horizon, len(test), period_horizon):
            model = SARIMAX(train, order=(1, 1, 2), seasonal_order=(1, 1, 2, m))
            results = model.fit(method='powell')

            # Identify subset of test to forecast against
            test_subset = test.iloc[previous_index:ii]
            previous_index = ii

            # Create predictions and add to list
            predictions = pd.DataFrame(index=test_subset.index, data=results.forecast(steps=period_horizon).values)
            predicted = pd.concat([predicted, predictions])

            # Update training dataset
            train = pd.concat([train, test_subset])

            # Handle final test records
            if (len(test) - ii) < period_horizon:
                model = SARIMAX(train, order=(1, 1, 2), seasonal_order=(1, 1, 2, m))
                results = model.fit(method='powell')

                # Identify subset of test to forecast against
                test_subset = test.iloc[ii:]
                train = pd.concat([train, test_subset])

                # Create predictions and add to list
                predictions = pd.DataFrame(index=test_subset.index,
                                           data=results.forecast(steps=len(test_subset)).values)
                predicted = pd.concat([predicted, predictions])

        # Create future forecast
        model = SARIMAX(dataframe, order=(1, 1, 2), seasonal_order=(1, 1, 2, m))
        results = model.fit(method='powell')
        predictions = results.forecast(steps=len(forecast_period_list))

        forecast = pd.Series(index=forecast_period_list, data=predictions)

        return test[VALUE_COLUMN_NAME], predicted[0].values, forecast


def initialize_model(model_name: str):
    named_model = [model for model in BaseModel.__subclasses__() if model_name == model.__name__][0]
    model = named_model()

    return model
