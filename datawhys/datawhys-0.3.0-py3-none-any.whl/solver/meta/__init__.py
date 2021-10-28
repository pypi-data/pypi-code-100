"""
The :mod:`datawhys.solver.meta` submodule contains solve methods for
meta solves.
"""

from ._solve import class_exploration_solve, exclusion_set_solve

__all__ = ["class_exploration_solve", "exclusion_set_solve"]
