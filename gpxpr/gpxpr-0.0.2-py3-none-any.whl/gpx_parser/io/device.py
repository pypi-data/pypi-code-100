import abc
from typing import Union

from gpx_parser.io.readable import Readable
from gpx_parser.io.writable import Writable


class Device(abc.ABC):
    @abc.abstractmethod
    def __enter__(self) -> Union[Writable, Readable]:  # noqa: D105
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, *_) -> None:  # type: ignore # noqa: D105
        raise NotImplementedError()
