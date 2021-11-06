"""
This package implements the Entropy Method for estimating the number of clusters in a data set.
"""

from .core import (
    compute_prob_mat,
    entropy_score,
    find_k,
)

from .repeated import *
from .model_selection import *