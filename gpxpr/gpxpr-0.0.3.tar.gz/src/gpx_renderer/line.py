from dataclasses import dataclass

from gpx_renderer.vector import Vector


@dataclass
class Line:
    start: Vector
    end: Vector
    color: str
