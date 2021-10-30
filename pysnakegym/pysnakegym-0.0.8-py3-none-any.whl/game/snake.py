import numpy as np
import pygame

from pysnakegym.game.core.direction import Direction
from pysnakegym.game.core.point import Point
from pysnakegym.game import colour
from pysnakegym.game.core.grid import Grid


class SnakeGame(object):
    """
    Class for holding the game mechanics for the game of snake.
    """

    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        """
        Constructor for the SnakeGame class.
        :param screen_width: The width of the screen the snake game
        :param screen_height: The height of the screen of the snake game
        :param snake_size: The size of a single snake element.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.snake_size = snake_size
        self._direction = Direction.STRAIGHT
        self._absolute_direction = "UP"
        self._game_over = False
        self.running = False
        self.ate_food = False

        self._n_steps = 0
        self._n_food_eaten = 0
        self._n_steps_without_food = 0

        self._max_food = (screen_width / snake_size) * (screen_height / snake_size) - 1

        self.grid = Grid(int(screen_width / snake_size), int(screen_height / snake_size))

    def start(self) -> None:
        """
        Starts the game of snake.
        :return: None
        """
        self._game_over = False
        self.running = True
        self._n_steps = 0
        self._n_food_eaten = 0
        self._n_steps_without_food = 0
        self.grid = Grid(int(self.screen_width / self.snake_size), int(self.screen_height / self.snake_size))

    def move(self, direction: np.array) -> (Point, bool, bool):
        """
        Moves the snake in the specified direction by one grid slot.
        :param direction: The direction the snake will be moved in.
        :return: A triplet containing the new location of the snake's head, whether the snake ate food, and whether the game
        is over.
        """
        snake_head = self.grid.move_snake(direction, self.ate_food)
        self._n_steps += 1

        if self.grid.snake().touches_tail() or self.grid.snake_is_touching_wall():
            self.game_over()
            return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

        # check if the snake touches food
        if self.grid.snake_is_touching_food():
            self.ate_food = True
            self._n_food_eaten += 1
            self._n_steps_without_food = 0

            # game is won
            if self._n_food_eaten == self._max_food:
                print("Game Won!")
                self.game_over()
                return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()
            self.grid.move_food(self.grid.random_food())
        else:
            self.ate_food = False
            self._n_steps_without_food += 1

        if self._n_steps_without_food > 1000:
            self.game_over()

        return Point.from_numpy(snake_head), self.ate_food, self.is_game_over()

    def game_over(self) -> None:
        """
        Sets the game to game over.
        :return: None
        """
        self._game_over = True

    def is_game_over(self) -> bool:
        """
        Returns whether the game is over or not. The game is over
        :return: True if the game is over, false if it is not.
        """
        return self._game_over

    def snake_head(self) -> Point:
        """
        Gets the position of the snake's head.
        :return: The location of the snake's head as a 2D point.
        """
        return Point.from_numpy(self.grid.snake().head())

    def snake_head_vicinity(self) -> np.array:
        """
        Gets the grid positions in the immediate vicinity of the snake's head. Immediate vicinity means the square to the
        left, straight, right of the snake's head.
        :return: a numpy array of shape (3, 2)
        """
        return self.grid.snake_head_vicinity()

    def is_outside(self, coordinates: np.array) -> bool:
        """
        Checks whether a single x-y coordinate is inside the grid
        :param coordinates: a numpy array of shape (1, 2)
        :return: true if the x-y coordinate is in the grid, false if not
        """
        return self.grid.is_outside_grid(coordinates)

    def in_snake_body(self, coordinates: np.array) -> bool:
        """
        Checks whether a single x-y coordinate is inside the snake's body.
        :param coordinates: a numpy array of shape (1, 2)
        :return: true if the x-y coordinate is in the snake's body, false if not
        """
        return any(np.equal(coordinates, self.snake_position()).all(1))

    def snake_position(self) -> np.array:
        """
        Gets the position of the entire snake.
        :return: A numpy array containing the position of all elements of the snake.
        """
        return self.grid.snake().position()

    def direction(self) -> np.array:
        """
        Gets the current relative direction of the snake.
        :return: The current direction of the snake.
        """
        return self._direction

    def absolute_direction(self) -> np.array:
        """
        Gets the current absolute direction of the snake, left, right, up, or down.
        :return: a numpy array
        """

    def food_position(self) -> Point:
        """
        Gets the current position of the food.
        :return: The current position of the food as a 2D point.
        """
        return Point.from_numpy(self.grid.food().position())

    def dimensions(self) -> (int, int):
        """
        Gets the dimensions of the snake game as a tuple.
        :return: An int tuple (width, height) of the game's dimensions.
        """
        return self.screen_width, self.screen_height

    def start_position(self) -> Point:
        """
        Gets the starting position of the snake.
        :return: The starting position of the snake as a 2D point.
        """
        start_x = self.screen_width / 2
        start_y = self.screen_height / 2
        return Point(start_x, start_y)

    def n_steps(self) -> int:
        """
        Gets the number of steps the snake has taken in the game so far.
        :return: An int for the number of steps taken by the snake in the game up until now.
        """
        return self._n_steps

    def n_food_eaten(self):
        """
        Gets the number of food eaten by the snake in the game so far
        :return: An int for the number of food eaten by the snake in the game up until now.
        """
        return self._n_food_eaten

    def score(self):
        """
        Gets the current score of the game.
        :return: The current score of the game.
        """
        return self.n_food_eaten()

    def n_steps_without_food(self):
        """
        The number of steps since the last food was eaten by the snake.
        :return: An int for the number of steps the snake has taken since it last ate food.
        """
        return self._n_steps_without_food



class PyGameSnakeGame(SnakeGame):
    """
    Subclass of SnakeGame where the game is visible on the screen.
    """
    def __init__(self, screen_width: int, screen_height: int, snake_size: int):
        super().__init__(screen_width, screen_height, snake_size)
        pygame.init()
        self.clock = pygame.time.Clock()

    def start(self) -> None:
        super().start()

        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        # 0,0 is in the top left corner

        self.__draw_snake()
        self.__draw_food()
        self.__display_score()

    def move(self, direction: Direction) -> (Point, bool, bool):

        snake_head, ate_food, game_over = super().move(direction)

        self.__draw_snake()
        self.__draw_food()
        self.__display_score()
        self.clock.tick(40)
        return snake_head, ate_food, game_over


    def __draw_food(self):
        food_coords = Grid.scale(self.grid.food().position(), self.snake_size)
        food_rect = pygame.Rect(food_coords[0], food_coords[1], self.snake_size, self.snake_size)
        pygame.draw.rect(self.window, colour.green, food_rect)
        pygame.display.flip()

    def __draw_snake(self):
        self.window.fill(colour.black)
        snake_segments = self.grid.snake().position()
        index = 0
        for segment in snake_segments:
            segment = Grid.scale(segment, self.snake_size)
            segment_colour = colour.blue
            # the head of the snake is a different colour than the rest
            if index == 0:
                segment_colour = colour.red
            index += 1

            rect = pygame.Rect(segment[0], segment[1], self.snake_size, self.snake_size)
            pygame.draw.rect(self.window, segment_colour, rect)
            pygame.display.flip()


    def __display_score(self):
        score_font = pygame.font.SysFont(None, 30)
        label = score_font.render(str(self.score()), 1, (255, 255, 255))
        self.window.blit(label, (1, 1))
        pygame.display.flip()
