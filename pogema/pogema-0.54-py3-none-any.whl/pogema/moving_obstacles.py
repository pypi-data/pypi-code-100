from queue import PriorityQueue

import gym
from pogema.animation import MarlSvgVisualization
from pogema.grid import Grid
from pogema.grid_config import GridConfig

import numpy as np
from pydantic import BaseModel


class MovingObstaclesConfig(BaseModel):
    density: float = 1.0
    shake_r: int = 0
    num_obstacles: int = 0
    show_range: list = [1, 1]
    hide_range: list = [1, 1]
    size_range: list = [2, 5]


class MovingObstacle:
    def __init__(self, x, y, size, rnd=None, mo_config=MovingObstaclesConfig()):
        if rnd is None:
            rnd = np.random.default_rng()
        self.rnd = rnd

        self.size = size
        self.mo_config: MovingObstaclesConfig = mo_config
        self.obstacle = self.rnd.binomial(1, self.mo_config.density, (self.size, self.size))

        self.x, self.y = x, y
        self.dx, self.dy = None, None
        self.shake_xy()

    def __lt__(self, other):
        return self.x < other.x and self.y < other.x

    def randint(self, low, high=None):
        if low == high:
            return low
        return self.rnd.integers(low=low, high=high)

    def get_xy(self):
        return self.x + self.dx, self.y + self.dy

    def shake_xy(self):
        r = self.mo_config.shake_r
        self.dx = self.randint(-r, r + 1)
        self.dy = self.randint(-r, r + 1)


class MovingObstaclesWrapper(gym.Wrapper):
    INF = 2 ** 20

    def __init__(self, env, mo_config=MovingObstaclesConfig(), rnd=None):
        super().__init__(env)

        if rnd is None:
            rnd = np.random.default_rng(self.env.config.seed)
        self.rnd = rnd

        self.mo_config: MovingObstaclesConfig = mo_config

        # noinspection PyTypeChecker
        self.hide_queue: PriorityQueue = None
        # noinspection PyTypeChecker
        self.show_queue: PriorityQueue = None
        self._t = None

        self._moving_obstacles = None

    def randint(self, low, high=None):
        if low == high:
            return low
        return self.rnd.integers(low=low, high=high)

    def reset(self):
        grid_config: GridConfig = self.env.config

        self.hide_queue: PriorityQueue = PriorityQueue()
        self.show_queue: PriorityQueue = PriorityQueue()
        self._t = 0

        observations = self.env.reset()
        grid: Grid = self.env.grid

        for _ in range(self.mo_config.num_obstacles):
            obstacle_size = self.randint(*self.mo_config.size_range)
            place_range = grid_config.obs_radius, grid_config.size + grid_config.obs_radius - obstacle_size + 1

            x, y = self.randint(*place_range), self.randint(*place_range)
            obstacle = MovingObstacle(x, y, obstacle_size, mo_config=self.mo_config, rnd=self.rnd)

            r = obstacle.size
            # lets make 100 attempts to place moving obstacle properly
            for _ in range(100):
                x, y = self.randint(*place_range), self.randint(*place_range)
                overlap = grid.obstacles[x:x + r, y:y + r].astype(int)
                overlap[overlap > 0] += 1
                intersection = overlap + obstacle.obstacle
                if np.count_nonzero(intersection == 1):
                    obstacle.x, obstacle.y = x, y
                    break

            self.show_queue.put((self.randint(*self.mo_config.show_range), obstacle))

        # create copy of the obstacles array with int type
        self._moving_obstacles = self.env.grid.obstacles.astype(int)
        self._moving_obstacles[self._moving_obstacles == grid_config.OBSTACLE] = self.INF
        return observations

    def update_overlap(self, x, y, r):
        g: Grid = self.grid
        overlap = self._moving_obstacles[x:x + r, y:y + r].copy()

        overlap[overlap > 0] = 1
        overlap[overlap <= 0] = 0

        # deal with obstacles on agents positions
        positions_overlap = g.positions[x:x + r, y:y + r].astype(int)
        overlap -= positions_overlap
        g.obstacles[x:x + r, y:y + r] = overlap.astype(float)

    def show_obstacle(self, o: MovingObstacle):
        o.shake_xy()
        x, y = o.get_xy()
        r = o.size
        self._moving_obstacles[x:x + r, y:y + r] += o.obstacle
        self.update_overlap(x, y, r)

    def hide_obstacle(self, o: MovingObstacle):
        x, y = o.get_xy()
        r = o.size
        self._moving_obstacles[x:x + r, y:y + r] -= o.obstacle
        self.update_overlap(x, y, r)

    @staticmethod
    def transfuse_queues(from_q, to_q, t, t_delta_func, process_func):

        while from_q.qsize() > 0:
            timer, obstacle = from_q.get()

            obstacle: MovingObstacle = obstacle
            if timer <= t:
                process_func(obstacle)
                new_time = t + max(1, t_delta_func())
                to_q.put((new_time, obstacle))
            else:
                from_q.put((timer, obstacle))
                return

    def step(self, actions):
        self._t += 1
        # show obstacles and schedule hiding
        self.transfuse_queues(from_q=self.show_queue, to_q=self.hide_queue, t=self._t,
                              t_delta_func=lambda: self.randint(*self.mo_config.show_range),
                              process_func=self.show_obstacle)

        # hide obstacles and schedule showing
        self.transfuse_queues(from_q=self.hide_queue, to_q=self.show_queue, t=self._t,
                              t_delta_func=lambda: self.randint(*self.mo_config.hide_range),
                              process_func=self.hide_obstacle)

        # self.fix_walls(self.env.grid.obstacles, self.env.config)

        observation, rewards, dones, infos = self.env.step(actions)

        # for x, y in self.env.grid.positions_xy:
        #     self.grid.obstacles[x, y] = self.env.config.FREE
        # for x, y in self.env.grid.finishes_xy:
        #     self.grid.obstacles[x, y] = self.env.config.FREE

        return observation, rewards, dones, infos


def main():
    grid_config = GridConfig(num_agents=1, size=32, obs_radius=5, density=0.0, seed=None)
    env = gym.make('Pogema-v0', config=grid_config)
    # env = AnimationMonitor(env)
    mo_config = MovingObstaclesConfig(
        num_obstacles=32,
        shake_r=5,
        size_range=(5, 10),
        density=0.7,
        hide_range=[8, 16],
        show_range=[8, 16],
    )
    env = MovingObstaclesWrapper(env, mo_config)
    obs = env.reset()

    done = [False, ...]
    for index in range(100):
        env.render()
        obs, reward, done, info = env.step([env.action_space.sample() for _ in range(env.config.num_agents)])
        MarlSvgVisualization.draw_frame(
            env.grid.obstacles,
            env.grid.positions_xy,
            env.grid.finishes_xy, f'animations/{index}.svg', env.config.obs_radius)
        if all(done):
            break
    env.reset()


if __name__ == '__main__':
    main()
