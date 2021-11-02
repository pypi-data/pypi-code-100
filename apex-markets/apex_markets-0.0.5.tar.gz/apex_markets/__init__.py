import requests
import pandas as pd
import json
from io import BytesIO


class SerumDataApiClient(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://serum-data-api-ir6rjs3zyq-ue.a.run.app/'
        # self.api_url = 'http://localhost:8080/'

    def get_market_names(self, level='level1'):
        url = self.api_url + 'markets'
        headers = {
            'INSTRUCTION': '0',
            'API-KEY': self.api_key,
            'SERUM-MARKET-LEVEL': level}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return json.loads(response.content)
        return

    def get_market_by_level(self, level, market):
        url = self.api_url + 'markets'
        headers = {
            'INSTRUCTION': '1',
            'API-KEY': self.api_key,
            'SERUM-MARKET-NAME': market,
            'SERUM-MARKET-LEVEL': level}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            df = pd.read_csv(BytesIO(response.content),
                             sep=",", lineterminator='\n')
            df.set_index('Unnamed: 0', inplace=True)
            return df
        return


    def get_market(self, market):
        results = {}
        for level in ['level1', 'level2', 'level3']:
            results[level1] = self.get_market_by_level(level, market)
        return results 