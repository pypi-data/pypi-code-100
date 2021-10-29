import datetime
from typing import Any, Iterator, Optional

from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_renderer.line import Line
from gpx_renderer.renderers.matplotlib import MatplotLibRenderer
from gpx_renderer.vector import Vector


class MatplotLibTimeRenderer(MatplotLibRenderer):
    def __init__(self, running: float, walking: float, destination: str):
        super().__init__(
            running=running,
            walking=walking,
            destination=destination,
            xlabel="Time (seconds)",
        )

    def _compute_lines(self, intervals: Iterator[GPXInterval]) -> Iterator[Line]:
        last_idx: int = 1
        last_vector: Optional[Vector] = None
        for interval in intervals:
            x1 = last_idx  # noqa: WPS121
            x2 = last_idx + int(interval.duration_s) + 1  # noqa: WPS121
            x = x2 - abs(x1 - x2) / 2  # noqa: WPS121
            y = min(interval.speed_kmtime, self._walking)  # noqa: WPS121
            color = self._color_from_pace(interval.speed_kmtime)
            current_vector = Vector(x, y)
            yield Line(
                start=last_vector or current_vector,
                end=current_vector,
                color=color,
            )
            last_idx = x2
            last_vector = current_vector

    def _x_axis_formatter(self, units: int, _: Any) -> str:
        return str(datetime.timedelta(seconds=units))
