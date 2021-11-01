import logging
from datetime import datetime, date
from typing import Dict

import requests


logger = logging.getLogger(__name__)


class BancoCentralSeries:
    def __init__(self, response):
        data = response.json()
        if data['Codigo'] != 0:
            logger.warning(f'API returned an error code: {data["Description"]}')
            raise ValueError(f'API Banco Centrao returned error code {data["Codigo"]}')
        series = data['Series']
        self.description_esp: str = series['descripEsp']
        self.description_ing: str = series['descripIng']
        self.series_id: str = series['seriesId']
        logger.info(f'reading time series for {self.description_ing}')
        self.values: Dict[date, float] = {}
        for obs in series['Obs']:
            dt = datetime.strptime(obs['indexDateString'], '%d-%m-%Y').date()
            status = obs['statusCode']
            value = obs['value']
            if status != 'OK':
                logger.debug(f'skipping {dt} with statusCode {status} and value {value}')
                continue
            self.values[dt] = float(value)


class BancoCentralClient(requests.Session):
    def __init__(self, username: str, password: str, base_url=None):
        self.username = username
        self.password = password
        self.base_url = base_url or 'https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx'
        super().__init__()

    def request(self, *args, **kwargs):
        kwargs['params'].setdefault('user', self.username)
        kwargs['params'].setdefault('pass', self.password)
        return super().request(*args, **kwargs)

    def get_series(self, serie_id: str, first_date: date, last_date: date):
        return self.get(
            self.base_url,
            params={
                'timeseries': serie_id,
                'firstdate': first_date.strftime('%Y-%m-%d'),
                'lastdate': last_date.strftime('%Y-%m-%d'),
                'function': 'GetSeries',
            }
        )
