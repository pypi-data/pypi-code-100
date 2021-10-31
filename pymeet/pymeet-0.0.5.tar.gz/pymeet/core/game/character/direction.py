from enum import Enum

from pymeet.core.game.math import Vector

_DIAGONAL_DIM_LENGTH = 1 / 2 ** 0.5


class Direction(str, Enum):
    RIGHT = 'RIGHT'
    UP_RIGHT = 'UP_RIGHT'
    UP = 'UP'
    UP_LEFT = 'UP_LEFT'
    LEFT = 'LEFT'
    DOWN_LEFT = 'DOWN_LEFT'
    DOWN = 'DOWN'
    DOWN_RIGHT = 'DOWN_RIGHT'

    def is_up(self) -> bool:
        return self == Direction.UP

    def is_down(self) -> bool:
        return self == Direction.DOWN

    def is_left(self) -> bool:
        return self == Direction.LEFT

    def is_right(self) -> bool:
        return self == Direction.RIGHT

    def is_up_left(self) -> bool:
        return self == Direction.UP_LEFT

    def is_up_right(self) -> bool:
        return self == Direction.UP_RIGHT

    def is_down_left(self) -> bool:
        return self == Direction.DOWN_LEFT

    def is_down_right(self) -> bool:
        return self == Direction.DOWN_RIGHT

    @classmethod
    def to_unit_vector(cls, direction: 'Direction') -> Vector:
        mapper = {
            Direction.RIGHT: Vector(1.0, 0.0),
            Direction.UP_RIGHT: Vector(_DIAGONAL_DIM_LENGTH, -_DIAGONAL_DIM_LENGTH),
            Direction.UP: Vector(0.0, -1.0),
            Direction.UP_LEFT: Vector(-_DIAGONAL_DIM_LENGTH, -_DIAGONAL_DIM_LENGTH),
            Direction.LEFT: Vector(-1.0, 0.0),
            Direction.DOWN_LEFT: Vector(-_DIAGONAL_DIM_LENGTH, _DIAGONAL_DIM_LENGTH),
            Direction.DOWN: Vector(0.0, 1.0),
            Direction.DOWN_RIGHT: Vector(_DIAGONAL_DIM_LENGTH, _DIAGONAL_DIM_LENGTH),
        }
        return mapper[direction]
