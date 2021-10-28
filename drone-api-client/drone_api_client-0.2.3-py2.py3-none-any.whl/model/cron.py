import json
from datetime import datetime


class DroneCron:
    __attr__ = ('name', 'expr', 'branch')

    def __init__(self, data: dict):
        self._data = data

    @property
    def name(self):
        return self._data.get('name')

    @name.setter
    def name(self, new_name: str):
        self._data['name'] = new_name

    @property
    def expr(self):
        return self._data.get('expr')

    @expr.setter
    def expr(self, new_expression: str):
        self._data['expr'] = new_expression

    @property
    def branch(self):
        return self._data.get('branch', 'master')

    @branch.setter
    def branch(self, new_branch: str):
        self._data['branch'] = new_branch

    @property
    def next_execution(self):
        data = self._data.get('next')
        return datetime.utcfromtimestamp(data) if data else 'Next cron execution not set'

    @property
    def repo_id(self):
        return self._data.get('repo_id')

    def update_cron(self, new_cron: dict):
        self.name = new_cron.get('name')
        self.expr = new_cron.get('expr')
        self.branch = new_cron.get('branch')

    def to_dict(self):
        return {key: self.__getattribute__(key) for key in DroneCron.__attr__}

    def to_json(self):
        return json.dumps(self.to_dict())
