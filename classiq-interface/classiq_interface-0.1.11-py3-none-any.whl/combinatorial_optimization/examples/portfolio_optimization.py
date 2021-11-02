import itertools
from typing import List

import pyomo.core as pyo


def portfolio_optimization(
    covariances: List[List[float]], returns: List[float], budget: int
) -> pyo.ConcreteModel:
    model = pyo.ConcreteModel()
    num_assets = len(returns)
    model.Assets = pyo.Set(initialize=range(num_assets))

    model.x = pyo.Var(model.Assets, domain=pyo.Binary)

    @model.Constraint()
    def budget_rule(model):
        return sum(model.x[asset] for asset in model.Assets) == budget

    model.profit = sum(returns[asset] * model.x[asset] for asset in model.Assets)

    model.risk = sum(
        covariances[asset1][asset2] * model.x[asset1] * model.x[asset2]
        for asset1, asset2 in itertools.product(model.Assets, model.Assets)
    )

    model.cost = pyo.Objective(expr=model.risk - model.profit, sense=pyo.minimize)

    return model
