'''
Created with love by Sigmoid

@Author - Păpăluță Vasile - vpapaluta06@gmail.com
@Author - Stojoc Vladimir - stojoc.vladimir@gmail.com
'''
import pandas as pd
from sklearn.decomposition import PCA
from .errors import NonNumericDataError, NoSuchColumnError, MissingDataError, DifferentColumnsError

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

class PCAFilter():
    def __init__(self, n_components : int = None):
        '''
            Setting the algorithm
        :param n_components: integer, by default = None
            Number of components to keep
        '''
        self.n_components = n_components

    def filter(self, dataframe : pd.DataFrame, target : str):
        '''
            Creating filter to new data and reducing the dimensionality of the data
        :param dataframe: pandas DataFrame
             Data Frame on which the algorithm is applied
        :param target: string
             The column name of the value that we have to predict
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
        #Splitting dataframe
        self.dataframe = dataframe.copy()
        self.target = target
        self.X_columns = [col for col in self.dataframe.columns if col != self.target]
        self.X = self.dataframe[self.X_columns].values
        self.y = self.dataframe[target].values

        #Creating filter
        self.pca = PCA(n_components = self.n_components)
        self.pca.fit(self.X)

        #Creating new data based on the filter
        X_pca = self.pca.transform(self.X)
        X_new = self.pca.inverse_transform(X_pca)
        X_new = pd.DataFrame(X_new, columns=self.X_columns)

        #Create and return new Dataframe
        X_new[target] = self.y
        return X_new

    def apply(self, dataframe : pd.DataFrame):
        '''
            Reducing the dimensionality of the data
            based on an already existed filter
        :param dataframe: pandas DataFrame
             Data Frame on which the algorithm is applied
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

        # Checking if the names of the columns are different for the both dataframes.
        if list(self.dataframe.columns) != list(dataframe.columns):
            raise DifferentColumnsError('The passed dataframe has different columns from the one passed to filter function.')

        #Splitting data
        self.dataframe = dataframe.copy()
        X_columns = [col for col in self.dataframe.columns if col != self.target]
        X = self.dataframe[X_columns].values
        y = self.dataframe[self.target].values

        #Applying filter to the new dataframe
        X_pca = self.pca.transform(X)
        X_new = self.pca.inverse_transform(X_pca)
        X_new = pd.DataFrame(X_new, columns=self.X_columns)

        #Create and return new Dataframe
        X_new[self.target] = y
        return X_new