import json


class DroneRepo:
    __attr__ = ('id', 'uid', 'user_id', 'namespace', 'name', 'slug', 'scm', 'git_http_url', 'git_ssh_url',
                'link', 'default_branch', 'private', 'visibility', 'active', 'config_path', 'trusted',
                'protected', 'ignore_forks', 'ignore_pull_requests', 'timeout', 'counter', 'synced',
                'created', 'updated', 'version', 'permissions')

    __change__ = ('config_path', 'protected', 'trusted', 'timeout', 'visibility', 'ignore_forks',
                  'ignore_pull_requests')

    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self):
        return self._data.get('id')

    @property
    def uid(self):
        return self._data.get('uid')

    @property
    def user_id(self):
        return self._data.get('user_id')

    @property
    def namespace(self):
        return self._data.get('namespace')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def slug(self):
        return self._data.get('slug')

    @property
    def scm(self):
        return self._data.get('scm')

    @property
    def git_http_url(self):
        return self._data.get('git_http_url')

    @property
    def git_ssh_url(self):
        return self._data.get('git_ssh_url')

    @property
    def link(self):
        return self._data.get('link')

    @property
    def default_branch(self):
        return self._data.get('default_branch')

    @property
    def private(self):
        return self._data.get('private')

    @property
    def visibility(self):
        return self._data.get('visibility')

    @property
    def active(self):
        return self._data.get('active')

    @property
    def config_path(self):
        return self._data.get('config_path')

    @property
    def trusted(self):
        return self._data.get('trusted')

    @property
    def protected(self):
        return self._data.get('protected')

    @property
    def ignore_forks(self):
        return self._data.get('ignore_forks')

    @property
    def ignore_pull_requests(self):
        return self._data.get('ignore_pull_requests')

    @property
    def timeout(self):
        return self._data.get('timeout')

    @property
    def counter(self):
        return self._data.get('counter')

    @property
    def synced(self):
        return self._data.get('synced')

    @property
    def created(self):
        return self._data.get('created')

    @property
    def updated(self):
        return self._data.get('updated')

    @property
    def version(self):
        return self._data.get('version')

    @property
    def permissions(self):
        return self._data.get('permissions')

    def update(self, upd: dict):
        for key, value in upd.items():
            if key in DroneRepo.__change__:
                self._data[key] = value

    def to_dict(self):
        return {key: self.__getattribute__(key) for key in DroneRepo.__attr__}

    def to_json(self):
        return json.dumps(self.to_dict())
