import math

import numpy as np

from pysnakegym.game.core.direction import Direction


class Food(object):
    """
    This class represents a food object on the grid.
    """

    def __init__(self, screen_width: int, screen_height: int, position: np.array):
        """
        Constructor for the Food class.
        :param screen_width:
        :param screen_height:
        :param position: The initial position of the food.
        """
        self._position = position
        self.screen_width = screen_width
        self.screen_height = screen_height

    def move(self, position: np.array) -> None:
        """
        Sets the new position of the food.
        :param position: A numpy array that is the new position of the food.
        :return: None
        """
        self._position = position

    def position(self) -> np.array:
        """
        Getter for the currently set position of the snake.
        :return: A numpy array that is the current position of the food.
        """
        return self._position


class Snake(object):
    """
    Class that represents the snake on the grid.
    """

    def __init__(self, start_position: np.array, direction: Direction, snake_size: int, grid_slots: int):
        """
        Constructor for the Snake class.
        :param start_position: A numpy array that is the starting position of the Snake.
        :param direction: The direction that the snake will face at the start.
        :param snake_size: The size of the snake.
        :param grid_slots: The number of grid slots that are available to the snake.
        """
        self.snake_size = snake_size
        self.grid_slots = grid_slots
        self.segments = np.zeros((grid_slots, 2))
        self.segments[0] = start_position
        self.tail_index = 1
        self.direction = direction
        self.previous_delta = np.array([0, -1])
        self.head_vicinity = np.zeros((3, 2))
        self.head_straight = start_position + self.previous_delta
        self.head_left = start_position + self.__rotate_90_deg(self.previous_delta, False)
        self.head_right = start_position + self.__rotate_90_deg(self.previous_delta, True)

    def head(self) -> np.array:
        """
        Getter for the current position of the head of the snake.
        :return: A numpy array that contains the x,y coordinates of the current position of the snake's head.
        """
        return self.segments[0]

    def move(self, direction: np.array, add_tail: bool = False) -> np.array:
        """
        Moves the snake in the specified direction and returns the new position of the head of the snake.
        :param direction: The direction that the snake will be moved in
        :param add_tail: boolean for specifying for whether to add a new section to the snake or not
        :return: Returns a numpy array that contains the coordinates of the snake's head.
        """
        self.__set_direction(direction=direction)

        # remove last value, shift all values down by one, insert new value at top
        # copy the segments matrix
        new_segments = np.copy(self.segments)

        # shift values down by one
        new_segments = np.roll(new_segments, 1, axis=0)

        # copy the head back to the first row so that it can be moved
        new_segments[0] = new_segments[1]

        if Direction.is_straight(direction):
            new_segments[0] += self.previous_delta
        elif Direction.is_left(direction):
            new_delta = self.__rotate_90_deg(self.previous_delta, False)
            new_segments[0] += new_delta
            self.previous_delta = new_delta
        elif Direction.is_right(direction):
            new_delta = self.__rotate_90_deg(self.previous_delta, True)
            new_segments[0] += new_delta
            self.previous_delta = new_delta

        self.head_straight = new_segments[0] + self.previous_delta
        self.head_left = new_segments[0] + self.__rotate_90_deg(self.previous_delta, False)
        self.head_right = new_segments[0] + self.__rotate_90_deg(self.previous_delta, True)

        if add_tail:
            self.tail_index += 1
        else:
            new_segments[self.tail_index] = np.array([-1, -1])

        self.segments = new_segments

        return self.segments[0]

    def length(self) -> int:
        """
        Gets the current length of the snake which is the number of elements it has including the head.
        :return: An int for the length of the snake.
        """
        return self.tail_index

    def position(self) -> np.array:
        """
        Returns the position of all elements of the snake including head and tail.
        :return: A numpy array of x,y coordinates for the snake's elements.
        """
        return self.segments[:self.tail_index]

    def vicinity(self) -> np.array:
        """
        Gets the coordinates of the slot that is straight ahead, to the left, and to the right of the head of the snake.
        :return: a numpy array of shape (3, 2) where the indeces are [straight, left, right]
        """
        return np.array([self.head_straight, self.head_left, self.head_right])

    def __set_direction(self, direction: np.array):
        """
        Sets the direction of the snake. The new direction cannot be the opposite of the current direction, e.g.
        if the snake is moving up right now, you cannot set the direction to down. In this case, the old direction
        is kept.
        :param direction: The new direction of the snake.
        :return: None
        """

        if Direction.is_left(direction) and not Direction.is_right(self.direction):
            self.direction = direction
        elif Direction.is_right(direction) and not Direction.is_left(self.direction):
            self.direction = direction
        else:
            self.direction = direction

    def __rotate_90_deg(self, position: np.array, clockwise: bool) -> np.array:
        """
        Rotates a given vector 90 degrees clockwise or anti-clockwise
        :param position: the 2D vector that will be rotated by 90 degrees
        :param clockwise: true if the vector is to be rotated clockwise, false if not
        :return: a new vector which is the old vector rotated by 90 degrees
        """
        if clockwise:
            return np.array([-position[1], position[0]])
        return np.array([position[1], -position[0]])


    def touches_tail(self) -> bool:
        """
        Returns whether the snake is currently touching its own tail.
        :return: True if the snake's head is currently touching a tail element, false if not.
        """
        # how do I know if the snake touches its own tail?
        # if I have duplicates in the matrix
        # unique is the sorted unique segments
        # counts is the number of times each of the unique values comes up in the segments matrix
        unique, counts = np.unique(self.segments[:self.tail_index], return_counts=True, axis=0)

        # if the count is greater than 1, it means we have duplicates and the snake touches its tail
        return len(unique[counts > 1]) > 0


class Grid(object):
    """
    This class represents the grid that the snake lives on. The grid is a 2 dimensional array on which the snake can
    be moved.
    """

    def __init__(self, width: int, height: int):
        """
        Constructor for the grid.
        :param width: width of the grid.
        :param height: height of the grid.
        """
        self.width = width
        self.height = height
        self.grid = np.full((width, height), -1)
        self._snake = Snake(start_position=self.start_position(), direction=Direction.STRAIGHT, snake_size=1, grid_slots=self.grid.size)
        self.set_snake_in_grid()
        self._food = Food(screen_width=width, screen_height=height, position=self.random_food())
        self.set_food_in_grid()
        self._touched_wall = False
        self.legal_coordinates = self.compute_legal_coordinates(width, height).tolist()

    def reset(self):
        """
        Resets the grid. This will move the snake to the starting position and generate a food at a random position
        in the grid as well as resetting the flag that indicates whether the snake touched a wall with a previous move.
        :return:
        """
        self._food = Food(screen_width=self.width, screen_height=self.height, position=self.random_food())
        self._snake = Snake(start_position=self.start_position(), direction=Direction.UP, snake_size=1,
                            grid_slots=self.grid.size)

        self.update_grid()
        self._touched_wall = False

    def random_food(self) -> np.array:
        """
        Returns the x,y coordinates of a randomly generated piece of food on the grid as a numpy array. The x,y coordinates
        of the food will never match those of the snake.
        :return: The x,y coordinates of the food
        """
        available_slots = self.available_slots()
        if available_slots.size == 0:
            return self._food.position()
        index = np.random.randint(available_slots.shape[0], size=1)
        new_food = available_slots[index]
        return new_food[0]

    def move_snake(self, direction: np.array, ate_food: bool) -> np.array:
        """
        Moves the snake one grid space in the specified direction and returns the new coordinates of the head.
        :param direction: The direction that the Snake will be moved in
        :param ate_food: Indicates whether the snake ate food in the previous move, in which the case the snake will be
        extended.
        :return: The x,y coordinates of the new position of the head of the snake as a numpy array.
        """
        if ate_food and self._snake.length() == self.grid.size:
            return self._snake.head()
        self._snake.move(direction, ate_food)
        self.update_grid()
        return self._snake.head()

    def move_food(self, location: np.array) -> np.array:
        if self.is_outside_grid(location) or location.size != 2:
            return self._food.position()
        self._food.move(location)
        self.update_grid()
        return self._food.position()

    def update_grid(self):
        """
        Updates the grid array with current snake and food positions. Should be called everytime the food or snake
        position change.
        :return: None
        """
        self.grid = np.full((self.width, self.height), -1)
        self.set_food_in_grid()
        self.set_snake_in_grid()


    def set_snake_in_grid(self):
        """
        Draws the snake on the grid.
        :return: None
        """
        for segment in self._snake.position():
            new_x = int(segment[0])
            new_y = int(segment[1])

            if new_x < 0 or new_x >= self.width or new_y < 0 or new_y >= self.height:
                self._touched_wall = True
            else:
                self.grid[new_y][new_x] = 1
                self._touched_wall = False

    def set_food_in_grid(self):
        """
        Draws the food on the grid
        :return:
        """
        food_x = int(self._food.position()[0])
        food_y = int(self._food.position()[1])
        self.grid[food_y][food_x] = 2 # invert y and x because the x axis is the columns and the y axis is the rows

    def food(self) -> Food:
        """
        Getter function for getting the food
        :return:
        """
        return self._food

    def snake(self) -> Snake:
        """
        Getter function for getting the snake
        :return:
        """
        return self._snake

    def snake_head_vicinity(self) -> np.array:
        """
        Getter method for the vicinity radar of the snake
        :return: a numpy array
        """
        return self._snake.vicinity()

    def available_slots(self) -> np.array:
        """
        Calculates the x,y coordinates of all available slots in the grid and returns them as a numpy array. An available
        slot is defined as grid slot which is neither occupied by the snake nor the food.
        :return: A numpy array of shape (2, n) where n is the number of available slots.
        """
        indeces = np.argwhere(self.grid == -1)
        indeces[:, [0, 1]] = indeces[:,[1, 0]]
        return indeces

    def snake_is_touching_food(self) -> bool:
        """
        Checks whether the snake's head is currently in the same grid slot as the food.
        :return: True if the snake's head is in the same grid slot as the food, false if not.
        """
        return (self._snake.head() == self._food.position()).all()

    def snake_is_touching_wall(self) -> bool:
        """
        Checks whether the snake is currently touching the wall
        :return: True if the snake is currently touching the wall, false if not.
        """
        return self._touched_wall

    def snake_is_touching_tail(self) -> bool:
        """
        Checks whether the snake is currently touching its own tail.
        :return: True if the snake is currently touching its own tail, false if not.
        """
        return self._snake.touches_tail()

    def start_position(self) -> np.array:
        """
        Calculates and returns the starting position of the snake which is defined as being in the middle of the grid.
        :return: The coordinates of the starting position of the snake as a numpy array.
        """
        start_x = math.floor(self.width / 2)
        start_y = math.floor(self.height / 2)
        return np.array([start_x, start_y])

    def is_outside_grid(self, coordinates: np.array) -> bool:
        """
        Checks whether a single x-y coordinate is inside the grid
        :param coordinates: a numpy array of shape (1, 2)
        :return: true if the x-y coordinate is in the grid, false if not
        """
        return coordinates.tolist() not in self.legal_coordinates


    def compute_legal_coordinates(self, width: int, height: int) -> np.array:
        """
        Computes the set of legal coordinates within the grid
        :param width: the width of the grid
        :param height: the height of the grid
        :return: a numpy array of shape (width * height, 2) with the legal coordinates of the grid
        """
        legal_coordinates = np.zeros((width * height, 2), dtype=np.int)
        index = 0
        for row in range(width):
            for col in range(height):
                legal_coordinates[index] = np.array([row, col])
                index += 1

        return legal_coordinates

    @staticmethod
    def scale(coordinates: np.array, slot_size: int) -> np.array:
        return coordinates * slot_size

    @staticmethod
    def scale_to_grid(coordinates: np.array, slot_size: int) -> np.array:
        return coordinates / slot_size