import torch
from . import metric

__all__ = ['MSE']


class MSE(metric.Metric):
    def __init__(self) -> None:
        super().__init__()

    def calc(self, img_a: torch.Tensor, img_b: torch.Tensor) -> torch.Tensor:
        return torch.mean((img_a - img_b)**2)
