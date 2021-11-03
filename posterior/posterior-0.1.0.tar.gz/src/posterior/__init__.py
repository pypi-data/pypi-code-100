import random


def set_random(seed: int) -> None:
    """
    Fix random seed to reproduce stochastic experiments
    """
    random.seed(seed)
