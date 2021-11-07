
import gym_twolinkarm_env.envs.base as base

class NoGravity(base.BaseEnv):
    def __init__(self):
        self.super()
        self.max_torque = 5.0
        self.gravity = 0
        self.random_target = False
        # self.reward = 