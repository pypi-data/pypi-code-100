import numpy as np
from scipy.spatial import distance

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def offset(self, x_offset, y_offset) -> None:
        self.x += x_offset
        self.y += y_offset

    def as_numpy(self) -> np.array:
        return np.array([self.x, self.y])

    @staticmethod
    def from_numpy(coordinates: np.array):
        return Point(coordinates[0], coordinates[1])

    def distance(self, point, metric=distance.cityblock) -> float:
        p1_array = self.as_numpy()
        p2_array = point.as_numpy()

        return metric(p1_array, p2_array)

    def __eq__(self, other):
        if not isinstance(other, Point):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"x: {self.x}. y: {self.y}"
