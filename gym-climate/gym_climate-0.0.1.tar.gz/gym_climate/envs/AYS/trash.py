import ays_environment
import stable_baselines3
from stable_baselines3 import PPO

env = ays_environment.AYSEnvironment()

model = PPO("MlpPolicy", env, verbose=0)

df = env.simulate_mdp(model)
env.plot_mdp(df)
