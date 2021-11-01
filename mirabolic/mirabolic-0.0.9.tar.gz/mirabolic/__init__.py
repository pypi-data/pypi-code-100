import os

with open(os.path.join(os.path.dirname(__file__), 'version'), mode='r') as fp:
    __version__ = fp.readline().rstrip()

# We import some functions/classes for ease of reference.

# Tensorflow loss functions for count data
from mirabolic.neural_glm.actuarial_loss_functions import (
    Poisson_link,
    Poisson_link_with_exposure,
    Negative_binomial_link,
    Negative_binomial_link_with_exposure,
)
