'''
Created with love by Sigmoid

@Author - Păpăluță Vasile - vpapaluta06@gmail.com
'''
from functools import reduce
from operator import and_, or_
import pandas as pd
from .errors import NoSuchColumnError, MissingDataError, NonNumericDataError, NoSuchMethodError

class MixerSelector:
    def __init__(self, selectors : list, strategy : str = 'intersection') -> None:
        '''
            Setting up the algorithm.
        :param selectors: list
            The list of initialized selectors.
        :param strategy: str, default = 'intersection'
            If set to 'union' the selector will return union of selected columns returned by selectors
            If set to 'intersection' the selector will return the intersection of columns returned by selectors
        '''
        self.__selectors = selectors
        self.__strategy = strategy

    def select(self, dataframe : pd.DataFrame, target : str) -> list:
        '''
            Selecting the most important columns.
        :param dataframe: pd.DataFrame
            The pandas DataFrame on which we want to apply feature selection
        :param target: str
            The column name of the value that we what to predict. Should be binary.
        :return: list
            The list of selected columns.
        '''
        # Checking if in the passed data are any NaN values.
        if dataframe.isna().values.any():
            raise MissingDataError(
                "The passed data frame contains missing values!"
            )

        # Checking if in the passed data are non-numeric values.
        for col in dataframe:
            if not pd.api.types.is_numeric_dtype(dataframe[col]):
                raise NonNumericDataError('The given DataFrame contains non-numeric values !')

        # Checking if the passed target column name is present in the passed data frame.
        if target not in dataframe:
            raise NoSuchColumnError(
                "The passed target column doesn't exist!"
            )

        # Defining the list where sets of columns for every selector will be stored
        selected_columns = []
        # Filling up the list with the columns selected by every selector
        for selector in self.__selectors:
            selected_columns.append(set(selector.select(dataframe, target)))

        # Applying the chose strategy
        if self.__strategy == 'union':
            # Returning the union of the selected columns
            return list(reduce(or_, selected_columns))
        elif self.__strategy == 'intersection':
            # Returning the intersection of the selected columns
            return list(reduce(and_, selected_columns))
        else:
            # Raising an error if the strategy isn't the union or intersection
            raise NoSuchMethodError(f"No such strategy as {self.__strategy}!")
