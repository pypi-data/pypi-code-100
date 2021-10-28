import json

import requests


class Session:
    def __init__(self, host: str, token: str, repo: str = ''):
        self.repo = repo
        self.__host = f"{host.replace('/api', '')}/api"
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def request(self, method: str, url: str, add_repo: bool = True, data: dict = None, params: dict = None, **kwargs):
        host = f"{self.__host}/repos/{self.repo}" if add_repo else self.__host
        data = json.dumps(data) if data else ''
        response = self._session.request(method=method, url=f'{host}{url}', data=data, params=params, **kwargs)
        if response.status_code in (200, 201):
            return response.json()
        else:
            return f'Error: {response.status_code}: {response.reason} ({response.text})'
