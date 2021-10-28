"""
The :mod:`datawhys.solver` module includes pure solves, ensemble-like solves
and meta solve capabilities
"""

from ._solver import exhaustive_solve, solve

__all__ = ["exhaustive_solve", "solve"]
