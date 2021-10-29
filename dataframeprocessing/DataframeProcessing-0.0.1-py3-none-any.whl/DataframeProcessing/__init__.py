import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class Alter:

    def fill_na(self, dataframe, central_tendency='mean'):
        """
        fill_na method replaces all the NaN values in a Dataframe

        Parameters:

        ->dataframe: pd.Dataframe
        ->central_tendency(optional): mean/median/mode
        """

        try:
            if type(dataframe) == pd.DataFrame:
                if central_tendency.lower() == 'mean':
                    for i in dataframe._get_numeric_data().columns:
                        dataframe[i].fillna(dataframe[i].mean(), inplace=True)
                    return pd.DataFrame(dataframe)

                if central_tendency.lower() == 'mode':
                    for i in dataframe._get_numeric_data().columns:
                        dataframe[i].fillna(dataframe[i].mode(), inplace=True)
                    return pd.DataFrame(dataframe)

                if central_tendency.lower() == 'median':
                    for i in dataframe._get_numeric_data().columns:
                        dataframe[i].fillna(dataframe[i].median(), inplace=True)
                    return pd.DataFrame(dataframe)
            else:
                print(f'Type should be pd.Dataframe and not {type(dataframe)}')

        except Exception as e:
            print(f"Error : {str(e)}")

    def standard_scaling(self, dataframe):
        """
        standard_scaling method standardize all the values by removing the mean and scaling to unit variance

        Parameters:

        ->dataframe: pandas.Dataframe/numpy.ndarray
        """
        try:
            if type(dataframe) == pd.DataFrame:
                check = 0
                for i in dataframe.isna().sum():
                    check += i
                if check == 0:
                    return pd.DataFrame(StandardScaler().fit_transform(dataframe._get_numeric_data()),
                                        columns=[i for i in dataframe._get_numeric_data().columns])
                else:
                    print('Dataframe contains NaN values')
            elif type(dataframe) == np.ndarray:
                dataframe = pd.DataFrame(dataframe)
                a = Alter().standard_scaling(dataframe)
                return a
        except Exception as e:
            print(f"Error : {str(e)}")
