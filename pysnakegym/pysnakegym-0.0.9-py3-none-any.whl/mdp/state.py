import numpy as np
from pysnakegym.game.core.direction import Direction
from pysnakegym.game.core.point import Point
from pysnakegym.game.snake import SnakeGame


class State(object):

    def get_state(self) -> np.array:
        pass

    def dims(self) -> (int, int):
        pass


class SnakeState(State):

    def __init__(self, game: SnakeGame):
        self.game = game

    def get_state(self) -> np.array:
        pass

    def dims(self) -> (int, int):
        pass


class GridState(SnakeState):
    """
    A class where the state is the entire grid as a matrix.
    """

    def __init__(self, game: SnakeGame):
        super().__init__(game)
        self.game = game

    def get_state(self) -> np.array:
        grid = self.game.grid.grid.copy()
        np.place(grid, grid == -1, 0)

        snake_head_x, snake_head_y = int(self.game.snake_head().x), int(self.game.snake_head().y)
        snake_body = self.game.snake_position()
        food_x, food_y = int(self.game.food_position().x), int(self.game.food_position().y)

        for segment in snake_body[1:]:
            x = int(segment[0])
            y = int(segment[1])
            grid[y][x] = 191

        if not self.is_outside(snake_head_x) and not self.is_outside(snake_head_y):
            grid[snake_head_y][snake_head_x] = 255
        grid[food_y][food_x] = 127

        return grid

    def dims(self) -> (int, int):
        return 10, 10

    def is_outside(self, n):
        return n < 0 or n > 9

class BooleanState(SnakeState):
    """
    Use a model that does not use distances but boolean values to say whether there is a danger (left, right, up, down),
    which direction we are going in (left, right, up, down), and which direction the food is in (left, right, up, down)
    https://www.youtube.com/watch?v=PJl4iabBEz0
    """

    def __init__(self, game: SnakeGame):
        super().__init__(game)
        self.game = game
        self._dims = None
        self.previous_head = Point(game.snake_head().x, game.snake_head().y + 1)

    def get_state(self) -> np.array:
        snake_head = self.game.snake_head()
        snake_body = self.game.snake_position()[1:, :]

        game_direction = self.get_game_direction(snake_head)

        self.previous_head = snake_head

        vicinity = self.game.snake_head_vicinity()

        danger = self.get_danger(vicinity, snake_body)

        food_position = self.get_food_position(self.game.food_position(), snake_head)

        return np.concatenate([game_direction, danger, food_position])

    def dims(self) -> (int, int):
        return (11, 1)

    def is_danger(self, distance: float) -> int:
        if distance <= 1:
            return 1
        return 0

    def get_danger(self, snake_vicinity: np.array, snake_body: np.array) -> np.array:

        danger_straight = 0
        danger_left = 0
        danger_right = 0

        if self.game.is_outside(snake_vicinity[0]) or self.game.in_snake_body(snake_vicinity[0]):
            danger_straight = 1
        if self.game.is_outside(snake_vicinity[1]) or self.game.in_snake_body(snake_vicinity[1]):
            danger_left = 1
        if self.game.is_outside(snake_vicinity[2]) or self.game.in_snake_body(snake_vicinity[2]):
            danger_right = 1

        return np.array([danger_left, danger_straight, danger_right])

    def get_food_position(self, food: Point, snake_head: Point):
        food_left = 0
        food_right = 0
        food_up = 0
        food_down = 0

        if food.x > snake_head.x:
            food_right = 1

        elif food.x < snake_head.x:
            food_left = 1

        elif food.x == snake_head.x:
            food_left = 0
            food_right = 0

        if food.y > snake_head.y:
            food_down = 1

        elif food.y < snake_head.y:
            food_up = 1

        elif food.y == snake_head.y:
            food_up = 0
            food_down = 0

        else:
            food_left = 1
            food_right = 1
            food_up = 1
            food_down = 1

        return np.array([food_up, food_down, food_left, food_right])

    def get_game_direction(self, snake_head: Point):
        direction_left = 0
        direction_right = 0
        direction_up = 0
        direction_down = 0

        if self.previous_head.x > snake_head.x:
            direction_left = 1
        elif self.previous_head.x < snake_head.x:
            direction_right = 1

        if self.previous_head.y > snake_head.y:
            direction_up = 1
        elif self.previous_head.y < snake_head.y:
            direction_down = 1

        if self.previous_head.x > snake_head.x:
            direction_left = 1
        elif self.previous_head.x < snake_head.x:
            direction_right = 1

        if self.previous_head.y > snake_head.y:
            direction_up = 1
        elif self.previous_head.y < snake_head.y:
            direction_down = 1

        return np.array([direction_up, direction_down, direction_left, direction_right])



