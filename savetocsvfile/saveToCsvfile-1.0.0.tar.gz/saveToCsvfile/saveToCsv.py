import pandas as pd

def insertTo(*Args):
    try:
        data = pd.DataFrame([Args])
        data.to_csv('data.csv', mode='a', index=False, header=False)
        return "Success"
    except Exception as E:
        return E


def fetchAll():
    try:
        data = pd.read_csv('data.csv')
        print(data.head())
    except Exception as E:
        return E


def fetch_N(n):
    try:
        data = pd.read_csv('data.csv')
        data.index = data.index + 1
        return data.head(n-1)
    except Exception as E:
        return E
