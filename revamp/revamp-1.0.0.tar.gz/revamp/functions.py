from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
scaler_mm = MinMaxScaler()
le = LabelEncoder()
enc = OneHotEncoder(handle_unknown='ignore')

class DataPreperation:
      
    def __init__(self):
      print("")

    def Transform(self,X,cleansing_step):
        
        """
       Instantiate data preparation.
    
       Method Transform will accept data frame (X) and cleansing_step(missing_values, encoding, one_hot_encoding, scaling, and all) as arguments.

       :param X: DataFrame.
       :type DataFrame: dataframe
       
       :param cleansing_step: Operations(missing_value_imputation, encoding, one_hot_encoding, scaling, all).
       :type Operation: str

        """

        if cleansing_step=='missing_value_imputation':
            return  self.missing_values(X)
        elif cleansing_step=='encoding':
            return self.encoding(X)
        elif cleansing_step=='one_hot_encoding':
            return self.one_hot_encoding(X)
        elif cleansing_step=='scaling':
            return self.scaling(X)
        else:
            return self.all(X)
      
    #Missing_values
    def missing_values(self,X):
      cat_cols=[i for i in X.columns if X.dtypes[i]=='object']
      num_cols=[i for i in X.columns if ( X.dtypes[i]=='float64' or  X.dtypes[i]=='int64')]
      X[cat_cols] = X[cat_cols].fillna(X[cat_cols].mode().iloc[0])
      X[num_cols] = X[num_cols].fillna(X[num_cols].mean().iloc[0])
      return X

    #encoding
    def encoding(self,X):
      cat_cols=[i for i in X.columns if X.dtypes[i]=='object']
      X[cat_cols] = X[cat_cols].astype(str).apply(lambda x: le.fit_transform(x))  
      return X

    #one-hot encoding
    def one_hot_encoding(self,X):
        after_dummy=pd.get_dummies(X)
        return after_dummy
     
    #Scaling
    def scaling(self,X):
        X_scaled=(X-X.mean())/ X.std()
        return X_scaled

    #all
    def all(self,X):
        cat_cols=[i for i in X.columns if X.dtypes[i]=='object']
        num_cols=[i for i in X.columns if ( X.dtypes[i]=='float64' or  X.dtypes[i]=='int64')]
        X[cat_cols] = X[cat_cols].fillna(X[cat_cols].mode().iloc[0])
        X[num_cols] = X[num_cols].fillna(X[num_cols].mean().iloc[0])
        after_dummy=pd.get_dummies(X)
        X_final=(after_dummy-after_dummy.mean())/ after_dummy.std()
        return X_final