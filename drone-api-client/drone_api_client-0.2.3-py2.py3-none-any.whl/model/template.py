class DroneTemplate:
    __attr__ = ('id', 'name', 'namespace', 'data')

    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self):
        return self._data.get('id')

    @property
    def name(self):
        return self._data.get('name')

    @property
    def namespace(self):
        return self._data.get('namespace')

    @property
    def data(self):
        return self._data.get('data')
