from typing import Dict, Any

import requests as requests

from telebotify.models import Body
from telebotify.utils import ModelMapper


class HttpClient:
    base_url = 'https://api.telegram.org/bot'

    def __init__(self, api_key: str):
        self.base_url += api_key

    def get(self, url, cls):
        r = requests.get(f'{self.base_url}/{url}')
        body: Body = ModelMapper.map(r.json(), Body)
        if body.ok:
            return ModelMapper.map(body.result, cls)
        else:
            raise Exception(r)

    def post(self, url, data: Dict[str, Any] = None, cls=None):
        r = requests.post(f'{self.base_url}/{url}', data)
        body: Body = ModelMapper.map(r.json(), Body)
        if body.ok:
            return ModelMapper.map(body.result, cls) if cls is not None else None
        else:
            print(r.reason)
            raise Exception(r)
