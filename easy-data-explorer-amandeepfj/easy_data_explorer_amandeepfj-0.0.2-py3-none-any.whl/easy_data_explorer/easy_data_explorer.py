import pandas as pd
import numpy as np


def add_one(number):
    return number + 1

def get_categorical_and_boolean_columns_summary_statistics(df_to_process):
    '''
    Return summary stats for all categorical columns.
    Parameters:
        df_to_process
        
    Returns:
        pd.DataFrame: Return summary stats for all categorical columns.   
    '''
    categoricals = ['object', 'bool']

    string_cols_summary_stats = ['count', pd.Series.nunique, pd.Series.unique]

    df_result = df_to_process.select_dtypes(include=categoricals).agg(string_cols_summary_stats).transpose()
    df_result = df_result.round(2)
    
    return(df_result)


def get_float_and_int_columns_summary_statistics(df_to_process):
    '''
    Return summary stats for all numeric columns.
    Parameters:
        df_to_process
        
    Returns:
        pd.DataFrame: Return summary stats for all numeric columns.   
    '''

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    
    float_and_int_cols_summary_stats = ['count', 'min', 'max', 'median', 'std', 'mean', 'skew', pd.Series.nunique, 'sum']

    df_result = df_to_process.select_dtypes(include=numerics).agg(float_and_int_cols_summary_stats).transpose()
    df_result = df_result.round(2)

    return(df_result)