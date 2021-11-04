# pylint: disable = import-error
"""Counterfactual explanations"""
from org.kie.kogito.explainability.local.counterfactual import (
    CounterfactualExplainer as _CounterfactualExplainer,
    CounterfactualConfigurationFactory as _CounterfactualConfigurationFactory,
    CounterfactualResult,
)
from org.optaplanner.core.config.solver import SolverConfig
from org.kie.kogito.explainability.model import Prediction, PredictionProvider

CounterfactualConfigurationFactory = _CounterfactualConfigurationFactory

class CounterfactualExplainer:
    def __init__(self, config: SolverConfig) -> None:
        self._explainer = _CounterfactualExplainer.builder().withSolverConfig(config).build()

    def explain(self, prediction: Prediction, model: PredictionProvider) -> CounterfactualResult:
        return self._explainer(prediction, model).get()