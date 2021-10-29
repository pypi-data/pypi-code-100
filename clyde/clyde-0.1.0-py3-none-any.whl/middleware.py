import typing

from . import models

def json(request: models.Request, call_next: typing.Callable):
    return call_next(request).json()
