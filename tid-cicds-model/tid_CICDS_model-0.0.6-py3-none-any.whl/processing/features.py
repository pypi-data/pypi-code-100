from typing import List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class TemporalVariableTransformer(BaseEstimator, TransformerMixin):
    """Temporal elapsed time transformer."""

    def __init__(self, variables: List[str], reference_variable: str):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables
        self.reference_variable = reference_variable

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[self.reference_variable] - X[feature]

        return X


class Mapper(BaseEstimator, TransformerMixin):
    """Categorical variable mapper."""

    def __init__(self, variables: List[str], mappings: dict):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables
        self.mappings = mappings

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need the fit statement to accomodate the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].map(self.mappings)

        return X


class DateTimeTransformer(BaseEstimator, TransformerMixin):
    """Extracting time variables."""

    def __init__(self, reference_variable):

        self.reference_variable = reference_variable

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()
        X["hour"] = X[self.reference_variable].dt.hour
        X["minute"] = X[self.reference_variable].dt.minute
        X["seconds"] = X[self.reference_variable].dt.second

        return X


class To_category(BaseEstimator, TransformerMixin):
    """Extracting time variables."""

    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        for feature in self.variables:
            X[feature] = X[feature].astype("category")

        return X


class Dropna(BaseEstimator, TransformerMixin):
    """Changing nan values."""

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        X = X.replace({np.nan: None})

        return X


class Dropna_array(BaseEstimator, TransformerMixin):
    """Changing nan values."""

    def fit(self, X: np.ndarray, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:

        # so that we do not over-write the original dataframe
        X = X.copy()
        X = np.nan_to_num(X, copy=True, nan=0.0, posinf=None, neginf=None)

        return X


class Outlier_removal(BaseEstimator, TransformerMixin):
    """Extracting time variables."""

    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        for variable in self.variables:
            quartile1 = X[variable].quantile(0.25)
            quartile3 = X[variable].quantile(0.75)
            interquantile_range = quartile3 - quartile1
            up_limit = quartile3 + 1.5 * interquantile_range
            low_limit = quartile1 - 1.5 * interquantile_range
            X.loc[(X[variable] < low_limit), variable] = low_limit
            X.loc[(X[variable] > up_limit), variable] = up_limit
        return X


class IP_cleaning(BaseEstimator, TransformerMixin):
    """Categorizing the IP Addresses and cleaning."""

    def __init__(self, variables: List[str]):

        if not isinstance(variables, list):
            raise ValueError("variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()

        for variable in self.variables:
            X[variable] = X[variable].str.replace(
                r"(\d*\.){3}\d*", "INTERNAL", regex=True
            )
            X[variable] = X[variable].str.replace(
                r"\A\d*\_\d*", "ANONYMOUS", regex=True
            )
        return X


class Flag_cleaning(BaseEstimator, TransformerMixin):
    """Cleaning the Flag."""

    def __init__(self, variables: str):

        if not isinstance(variables, str):
            raise ValueError("variables should be a string")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        # so that we do not over-write the original dataframe
        X = X.copy()
        variables = self.variables
        X[variables] = X[variables].str.replace(r"0x.{2}", "UNKNOWN", regex=True)
        X[variables] = X[variables].astype("category")

        return X
