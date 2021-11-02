from typing import Optional

import torch
from torch import nn


class LabelSmoothingBCEWithLogitsLoss(nn.Module):
    def __init__(
        self,
        smoothing: float,
        weight: Optional[torch.Tensor] = None,
        reduction: str = "mean",
        pos_weight: Optional[torch.Tensor] = None,
    ):
        super(LabelSmoothingBCEWithLogitsLoss, self).__init__()
        self.bce = nn.BCEWithLogitsLoss(weight=weight, reduction=reduction, pos_weight=pos_weight)
        self.smoothing = smoothing

    def forward(self, output: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return self.bce(output, torch.abs(target - self.smoothing))


class SmoothF1WithLogitsLossLoss(nn.Module):
    def __init__(self, reduction: str = "mean"):
        super(SmoothF1WithLogitsLossLoss, self).__init__()
        self.reduction = reduction

    def forward(self, output: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        output = output.sigmoid()

        true_positives = output * target
        false_positives = output * (torch.ones_like(target) - target)
        false_negatives = (torch.ones_like(target) - output) * target

        soft_f1 = true_positives / (true_positives + 0.5 + (false_positives + false_negatives))
        loss = torch.ones_like(soft_f1) - soft_f1

        if self.reduction == "mean":
            loss = loss.mean()
        elif self.reduction == "sum":
            loss = loss.sum()

        return loss
