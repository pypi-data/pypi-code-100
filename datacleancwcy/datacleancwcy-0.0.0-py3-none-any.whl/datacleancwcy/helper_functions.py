import pandas as pd

def null_count(df):
    return df.isnull().sum().sum()

def split_dates(date_series):
    months = date_series.apply(lambda x: x[:2])
    days = date_series.apply(lambda x: x[3:5])
    years = date_series.apply(lambda x: x[6:])
    return(pd.DataFrame({'month': months, 'day': days, 'year': years}))


def list_2_series(list_2_series, df):
    df['list'] = list_2_series
    