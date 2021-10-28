import json


class DroneSecret:
    __attr__ = ('name', 'data', 'pull_request')

    def __init__(self, data: dict):
        self._data = data

    @property
    def name(self):
        return self._data.get('name')

    @name.setter
    def name(self, new_name: str):
        self._data['name'] = new_name

    @property
    def data(self):
        return self._data.get('data')

    @data.setter
    def data(self, new_data):
        self._data['data'] = new_data

    @property
    def pull_request(self):
        return self._data.get('pull_request', True)

    @pull_request.setter
    def pull_request(self, pull_request: str):
        self._data['pull_request'] = pull_request

    @property
    def repo_id(self):
        return self._data.get('repo_id')

    def update_secret(self, new_cron: dict):
        self.name = new_cron.get('name')
        self.data = new_cron.get('data')

    def to_dict(self):
        return {key: self.__getattribute__(key) for key in DroneSecret.__attr__}

    def to_json(self):
        return json.dumps(self.to_dict())
