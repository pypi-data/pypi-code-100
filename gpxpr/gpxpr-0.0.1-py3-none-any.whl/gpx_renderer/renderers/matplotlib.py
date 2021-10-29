import abc
import datetime
import sys
from typing import Any, Iterator

from matplotlib.lines import Line2D
from matplotlib import pyplot

from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_renderer.line import Line
from gpx_renderer.renderer import Renderer


class MatplotLibRenderer(Renderer, abc.ABC):
    def __init__(self, running: float, walking: float, destination: str, xlabel: str):
        super().__init__(running=running, walking=walking, destination=destination)
        self._running_color: str = "green"
        self._walking_color: str = "orange"
        self._standing_color: str = "red"
        self._xlabel: str = xlabel

    def render(self, intervals: Iterator[GPXInterval]) -> None:
        _, axes = pyplot.subplots(figsize=(30, 5))
        for line in self._compute_lines(intervals):
            p1 = [line.start.x, line.end.x]
            p2 = [line.start.y, line.end.y]
            axes.plot(p1, p2, color=line.color)
        self._set_legend(axes)
        self._set_axes_formatting(axes)
        pyplot.gca().invert_yaxis()
        pyplot.savefig(self._destination or sys.stdout)

    def _color_from_pace(self, pace: float) -> str:
        if pace < self._running:
            return self._running_color
        if pace < self._walking:
            return self._walking_color
        return self._standing_color

    def _set_legend(self, axes: Any) -> None:
        custom_lines = [
            Line2D([0], [0], color=self._running_color, lw=4),
            Line2D([0], [0], color=self._walking_color, lw=4),
            Line2D([0], [0], color=self._standing_color, lw=4),
        ]
        axes.legend(custom_lines, ["Running", "Walking", "Standing"])

    def _set_axes_formatting(self, axes: Any) -> None:
        axes.xaxis.set_major_formatter(self._x_axis_formatter)
        axes.yaxis.grid(True)
        pyplot.xlabel(self._xlabel)
        pyplot.ylabel("Pace (min/km)")

    @abc.abstractmethod
    def _compute_lines(
        self,
        intervals: Iterator[GPXInterval],
    ) -> Iterator[Line]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _x_axis_formatter(self, units: int, _: Any) -> str:
        raise NotImplementedError()
