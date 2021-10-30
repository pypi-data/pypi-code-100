import numpy as np
from pysnakegym.mdp.state import BooleanState
from pysnakegym.game.snake import PyGameSnakeGame
from pysnakegym.game.snake import SnakeGame
from pysnakegym.mdp.mdp import MDP


class SnakeMDP(MDP):

    def __init__(self, screen_width: int = 200, screen_height: int = 200, snake_size: int = 20, show_game: bool = False):
        super().__init__()
        if show_game:
            self.environment = PyGameSnakeGame(screen_width=screen_width, screen_height=screen_height, snake_size=snake_size)
        else:
            self.environment = SnakeGame(screen_width=screen_width, screen_height=screen_height, snake_size=snake_size)
        self.state_representation = BooleanState(self.environment)
        self.current_state = None

    def reset(self) -> (np.array, float, bool):
        self.environment.start()
        self._reward_sum = 0
        self._n_steps = 0
        self._score = 0
        self.current_state = self.state_representation.get_state()
        return self.state_representation.get_state(), 0, False

    def step(self, action: np.array) -> (np.array, float, bool):

        _, ate_food, is_game_over = self.environment.move(action)
        reward = 0

        if ate_food:
            self._score += 1
            reward = 10

        if is_game_over:
            reward = -10
            self._reward_sum += reward
            self._n_steps += 1
            return self.current_state, reward, is_game_over

        self._reward_sum += reward
        self._n_steps += 1

        self.current_state = self.state_representation.get_state()
        return self.state_representation.get_state(), reward, is_game_over

    def state_dims(self) -> (int, int):
        return self.state_representation.dims()

    def n_actions(self):
        return 3
