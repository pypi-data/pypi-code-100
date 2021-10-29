import requests
# import starlette.datastructures
import pydantic

import typing

from . import routing
from . import datastructures

# class Scope(pydantic.BaseModel):
#     method: str
    # name:   str

class Operation(pydantic.BaseModel):
    class Config:
        arbitrary_types_allowed: bool = True

    method: str
    name:   str
    route:  routing.Route

class Request(requests.Request):
    app:    typing.Optional[object] = None
    client: typing.Optional[object] = None
    state:  datastructures.State

    def __init__(self, *args, path_params=None, response=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.path_params = path_params or {}

        self.response = response

        self.state = datastructures.State()

        # self.app = None
        # self.client = None
        # self.url = url

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}({repr(str(self.method))}, {self.url!r})>'

    @property
    def url(self) -> str:
        # print(self, self._url)
        return self._url.format(**self.path_params)

    @url.setter
    def url(self, value: str) -> None:
        self._url = value

    # def prepare(self):
    #     prepared_request = super().prepare()
    #
    #     print(prepared_request.url, self.path_params)
    #
    #     prepared_request.url = prepared_request.url.format(self.path_params)
    #
    #     print(prepared_request.url)
    #
    #     return prepared_request
