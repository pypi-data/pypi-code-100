from .encoder2 import Encoder
import pandas as pd
from sklearn.impute import SimpleImputer
class MissingValues:
    '''MissingValues is dessigned to make correcting missing values alot more accesable.
    MissingValues(df)
    df: is the inputted pandas dataframe what will have corrections made to it
    check is the method used to tell the module to start the corrections, this method will return the corrected dataframe
    if you wish to get the original dataframe call the copy variable.
    currently you are only able to use the median stratagy however other methods are in the work'''
    def __init__(self, df):
        self.copy = df
        data = Encoder(df = df)
        data.check()
        self.df = data.df

    def check(self):
        self.isnull = []
        for i in self.df.columns:
            if (self.df[i].isnull().values.any()):
                self.isnull.append(i)
        if (len(self.isnull) >0):
            self.Imputer()
        return self.df
    def Imputer(self):
        imputer = SimpleImputer(strategy="median")
        new_data = imputer.fit_transform(self.df)
        convert = pd.DataFrame(new_data, columns=self.df.columns,index=self.df.index)
        self.df = convert