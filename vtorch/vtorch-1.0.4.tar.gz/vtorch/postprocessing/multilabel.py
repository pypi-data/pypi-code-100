import torch
from overrides import overrides

from .default import PredictionPostprocessor, PredictionPostprocessorI


class MultilabelPostprocessor(PredictionPostprocessor):
    @overrides  # type: ignore
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        thresholds_with_logits_shape = torch.ones_like(logits) * self.thresholds
        predictions: torch.Tensor = torch.where(  # type: ignore
            logits >= thresholds_with_logits_shape, torch.tensor([1.0]), torch.tensor([0.0])
        )
        return predictions


class MultilabelPostprocessorWithLogits(PredictionPostprocessor):
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        logits = logits.sigmoid()
        thresholds_with_logits_shape = torch.ones_like(logits) * self.thresholds
        predictions: torch.Tensor = torch.where(  # type: ignore
            logits >= thresholds_with_logits_shape, torch.tensor([1.0]), torch.tensor([0.0])
        )
        return predictions


class RawLogitsMultilabelPostprocessor(PredictionPostprocessorI):
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        return (logits > 0).float()  # type: ignore
