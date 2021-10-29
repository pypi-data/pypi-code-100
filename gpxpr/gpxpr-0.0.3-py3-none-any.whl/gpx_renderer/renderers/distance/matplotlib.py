from typing import Any, Iterator, Optional

from gpx_parser.parser.gpx_track_interval import GPXInterval
from gpx_renderer.line import Line
from gpx_renderer.renderers.matplotlib import MatplotLibRenderer
from gpx_renderer.vector import Vector


class MatplotLibDistanceRenderer(MatplotLibRenderer):
    def __init__(self, running: float, walking: float, destination: str):
        super().__init__(
            running=running,
            walking=walking,
            destination=destination,
            xlabel="Distance (meters)",
        )

    def _compute_lines(  # noqa: WPS210
        self,
        intervals: Iterator[GPXInterval],
    ) -> Iterator[Line]:  # noqa: WPS210
        current_distance: float = 0
        last_vector: Optional[Vector] = None
        for interval in intervals:
            x1 = current_distance  # noqa: WPS121,WPS111
            x2 = current_distance + interval.distance_m  # noqa: WPS121,WPS111
            x = x2 - abs(x1 - x2) / 2  # noqa: WPS121,WPS111
            y = min(interval.speed_kmtime, self._walking)  # noqa: WPS121,WPS111
            color = self._color_from_pace(interval.speed_kmtime)
            current_vector = Vector(x, y)
            current_distance += 1
            yield Line(
                start=last_vector or current_vector,
                end=current_vector,
                color=color,
            )
            current_distance += interval.distance_m
            last_vector = current_vector

    def _x_axis_formatter(self, units: int, _: Any) -> str:
        return str(units)
