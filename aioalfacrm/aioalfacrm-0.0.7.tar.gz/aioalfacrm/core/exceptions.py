import aiohttp


class AlfaException(Exception):

    def __init__(self, code: int, message: str) -> None:
        self._code = code
        self._message = message

    def __str__(self):
        return f'Code: {self._code} - {self._message}'


class ApiException(AlfaException):
    def __init__(self, code: int, message: str, request_info: aiohttp.RequestInfo):
        super(ApiException, self).__init__(code, message)
        self._request_info = request_info

    def __str__(self):
        return f'Code: {self._code} - {self._message} {self._request_info}'


class NotFound(AlfaException):
    pass
