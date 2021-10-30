import numpy as np

class Direction():
    STRAIGHT = np.array([0, 1, 0])
    RIGHT = np.array([0, 0, 1])
    LEFT = np.array([1, 0, 0])

    @staticmethod
    def one_hot(direction) -> np.array:
        as_list = list(Direction)
        one_hot = np.zeros(3)
        index = as_list.index(direction)
        one_hot[index] = 1
        return one_hot

    @staticmethod
    def n_actions():
        return 3#len(list(Direction))

    @staticmethod
    def is_straight(direction: np.array) -> bool:
        return (direction == np.array([0, 1, 0])).all()

    @staticmethod
    def is_left(direction: np.array) -> bool:
        return (direction == np.array([1, 0, 0])).all()

    @staticmethod
    def is_right(direction: np.array) -> bool:
        return (direction == np.array([0, 0, 1])).all()

