from pymeet.core.game.math import Vector


class CharacterPosition(Vector):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
