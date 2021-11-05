import gym
import gym_super_mario_bros
import retro
from einops import rearrange
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace


class RGBObservationWrapper(gym.ObservationWrapper):
    def __init__(self, env, grayscale=False):
        super().__init__(env)
        self.grayscale = grayscale

    def observation(self, obs):
        if len(obs.shape) < 3:
            # does not have rgb obs
            obs = self.env.render(mode="rgb_array")
        # modify obs
        obs = rearrange(obs, "w h c -> c w h")
        return obs


def make_super_mario_bros():
    env = RGBObservationWrapper(gym_super_mario_bros.make("SuperMarioBros-v0"))
    env = JoypadSpace(env, SIMPLE_MOVEMENT)
    return env


def make_sonic():
    env = retro.make(game="SonicTheHedgehog-Genesis", state="GreenHillZone.Act1")
    return env


gym_env_dict = {
    "SuperMarioBros-v0": make_super_mario_bros,
    "SonicTheHedgehog-Genesis": make_sonic,
}
