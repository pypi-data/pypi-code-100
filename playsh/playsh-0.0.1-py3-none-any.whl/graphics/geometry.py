from enum import Enum
from OpenGL import GL as gl
from dataclasses import dataclass
from glm import vec3, vec2
from typing import Optional


class Topology(Enum):
    TRIANGLES = gl.GL_TRIANGLES
    LINES = gl.GL_LINES


@dataclass(eq=True, frozen=True)
class Geometry:
    topology: Topology
    positions: tuple[vec3]
    normals: Optional[tuple[vec3]] = None
    texcoords: Optional[tuple[vec2]] = None
    indices: Optional[tuple[int]] = None


class ScreenQuad(Geometry):
    def __init__(self):
        topology = Topology.TRIANGLES

        # fmt: off
        positions = (
            vec3(-1.0, 1.0, 0.0), vec3(-1.0, -1.0, 0.0), vec3(1.0, -1.0, 0.0),
            vec3(-1.0, 1.0, 0.0), vec3(1.0, -1.0, 0.0), vec3(1.0, 1.0, 0.0)
        )
        texcoords = (
            vec2(0.0, 1.0), vec2(0.0, 0.0), vec2(1.0, 0.0),
            vec2(0.0, 1.0), vec2(1.0, 0.0), vec2(1.0, 1.0)
        )
        # fmt: on

        super().__init__(topology=topology, positions=positions, texcoords=texcoords)
