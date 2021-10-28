import json
from datetime import datetime


class DroneUser:
    __attr__ = ('id', 'login', 'email', 'avatar', 'active', 'admin', 'machine', 'syncing', 'synced',
                'created', 'updated', 'last_login')

    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self):
        return self._data.get('id')

    @property
    def login(self):
        return self._data.get('login')

    @property
    def email(self):
        return self._data.get('email')

    @email.setter
    def email(self, new_email: str):
        self._data['email'] = new_email

    @property
    def avatar(self):
        return self._data.get('avatar')

    @avatar.setter
    def avatar(self, link_to_avatar: str):
        self._data['avatar'] = link_to_avatar

    @property
    def active(self):
        return self._data.get('active')

    @property
    def admin(self):
        return self._data.get('admin', False)

    @property
    def machine(self):
        return self._data.get('machine')

    @property
    def syncing(self):
        return self._data.get('syncing')

    @property
    def synced(self):
        return datetime.utcfromtimestamp(self._data['synced']) if self._data.get('synced') else None

    @property
    def created(self):
        return datetime.utcfromtimestamp(self._data['created']) if self._data.get('created') else None

    @property
    def updated(self):
        return datetime.utcfromtimestamp(self._data['updated']) if self._data.get('updated') else None

    @property
    def last_login(self):
        return datetime.utcfromtimestamp(self._data['last_login']) if self._data.get('last_login') else None

    def to_dict(self):
        return {key: self.__getattribute__(key) for key in DroneUser.__attr__}

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_create(self):
        return {key: self.__getattribute__(key) for key in ('login', 'email', 'admin', 'avatar')
                if self.__getattribute__(key) is not None}
