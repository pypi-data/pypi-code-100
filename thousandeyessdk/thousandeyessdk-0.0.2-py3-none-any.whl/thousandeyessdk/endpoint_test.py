# https://developer.thousandeyes.com/v6/endpoint_tests/


class EndpointTest:
    """A single instance for a single endpoint test"""
    def __init__(self, api, data):
        self._api = api
        self._data = data

    @property
    def id(self) -> int:
        """unique test ID of the endpoint test"""
        return self._data.get('testId')

    @property
    def name(self) -> str:
        """unique name of the endpoint test"""
        return self._data.get('testName')

    @property
    def interval(self) -> int:
        """interval of the endpoint test"""
        return self._data.get('interval')

    def __repr__(self):
        return f'<EndpointTest id={self.id} name={self.name}>'
