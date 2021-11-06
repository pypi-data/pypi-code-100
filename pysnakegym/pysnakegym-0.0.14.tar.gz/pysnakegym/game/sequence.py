from abc import ABC

from dataclasses import dataclass

from pysnakegym.game import PyGameSnakeGame
from pysnakegym.game.core import Snake, Food


@dataclass
class GameSequence(ABC):
    pass


@dataclass
class SnakeGameSequence(GameSequence):
    snake: Snake
    food: Food


class GameSequencePlayer(ABC):
    sequences = []

    def add(self, sequence: GameSequence):
        pass

    def play(self):
        pass

    def reset(self):
        self.sequences = []


class SnakeGameSequencePlayer(GameSequencePlayer):

    def add(self, sequence: SnakeGameSequence):
        self.sequences.append(sequence)

    def play(self):
        game = PyGameSnakeGame(screen_width=800, screen_height=800, snake_size=80)
        game.start()
        for sequence in self.sequences:
            game.grid.snake = sequence.snake
            game.grid.food = sequence.food
            game.draw_snake()
            game.draw_food()
            game.display_score()
            game.clock.tick(40)
