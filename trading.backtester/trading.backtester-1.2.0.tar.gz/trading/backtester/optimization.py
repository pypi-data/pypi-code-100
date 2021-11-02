from __future__ import annotations

from typing import Any
import itertools
import multiprocessing
import os

import pandas as pd


def _optimize_run(self, parameters):
    self.exchange.reset()
    self.set_strategy(self._strat_class, parameters)
    self.run()

    parameters["sortino"] = self.metrics.sortino()

    return parameters


def optimize(self, start: str, end: str, parameters: dict[Any]) -> dict[Any]:
    """Optimizes the attached strategy and returns the optimized params."""

    parameter_keys = parameters.keys()
    parameter_values = parameters.values()

    parameter_list = []
    for parameter_products in itertools.product(*parameter_values):
        parameter_list.append(parameter_products)

    with multiprocessing.Pool(processes=os.cpu_count()) as pool:
        result = pool.imap_unordered(_optimize_run, parameter_list)

    return pd.DataFrame(result)
