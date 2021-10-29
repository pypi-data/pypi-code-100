import abc
import sys
from typing import Iterator

from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_renderer.renderer import Renderer
from gpx_renderer.terminal_colors import TerminalColors


class STDOUTRenderer(Renderer, abc.ABC):
    def __init__(self, running: float, walking: float, destination: str):
        super().__init__(running=running, walking=walking, destination=destination)
        self._running_color = TerminalColors.OKCYAN
        self._walking_color = TerminalColors.WARNING
        self._standing_color = TerminalColors.FAIL

    def render(self, intervals: Iterator[GPXInterval]) -> None:
        self._render_legend()
        self._render_graph(intervals)

    def _color_from_pace(self, pace: float) -> str:
        if pace < self._running:
            return self._running_color
        if pace < self._walking:
            return self._walking_color
        return self._standing_color

    def _render_legend(self) -> None:
        sys.stdout.write(
            f"{self._standing_color}█{TerminalColors.ENDC}: Standing (pace is slower than {self._walking} min/km)\n",  # noqa: WPS411,E501
        )
        sys.stdout.write(
            f"{self._walking_color}█{TerminalColors.ENDC}: Walking  (pace is between {self._walking} min/km and {self._running} min/km)\n",  # noqa: WPS411,E501,WPS221
        )
        sys.stdout.write(
            f"{self._running_color}█{TerminalColors.ENDC}: Running  (pace is faster than {self._running} min/km)\n",
        )

    @abc.abstractmethod
    def _generate_points(self, intervals: Iterator[GPXInterval]) -> Iterator[str]:
        raise NotImplementedError()

    def _render_graph(self, intervals: Iterator[GPXInterval]) -> None:
        for point in self._generate_points(intervals):
            sys.stdout.write(point)
