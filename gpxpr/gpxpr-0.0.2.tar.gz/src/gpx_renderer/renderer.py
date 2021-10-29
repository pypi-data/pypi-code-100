import abc
from typing import Iterator

from gpx_parser.parser.gpx_track_interval import GPXInterval


class Renderer(abc.ABC):
    def __init__(self, running: float, walking: float, destination: str):
        self._running: float = running
        self._walking: float = walking
        self._destination: str = destination

    def render(self, _: Iterator[GPXInterval]) -> None:
        raise NotImplementedError()
