from typing import List, Optional, Union

import torch
from torch import Tensor
from torch.distributions import Transform, constraints

from .. import Parameter
from .abstractparameter import AbstractParameter
from .model import Model
from .utils import process_object, register_class


@register_class
class ConvexCombinationTransform(Transform):
    r"""Transform from unconstrained space to constrained space via
    :math:`y = \frac{x}{\sum_{i=1}^K \alpha_i x_i}` in order to satisfy
    :math:`\sum_{i=1}^K \alpha_i y_i = 1` where :math:`\alpha_i \geq 0` and
    :math:`\sum_{i=1}^K \alpha_i = 1`.

    :param weights: weights (sum to 1)
    """
    domain = constraints.simplex
    codomain = constraints.positive

    def __init__(self, weights: AbstractParameter, cache_size=0) -> None:
        super(ConvexCombinationTransform, self).__init__(cache_size=cache_size)
        self._weights = weights

    def _call(self, x):
        return x / (x * self._weights.tensor).sum(axis=-1, keepdims=True)

    def _inverse(self, y):
        raise NotImplementedError

    def log_abs_det_jacobian(self, x, y):
        return torch.tensor(0.0)


@register_class
class ConvexCombination(Model):
    r"""Convex combination of x satisfying

    :math:`\sum_{i=1}^K w_i x_i = 1` and :math:`\sum_{i=1}^K w_i = 1`

    :param id_: ID of object
    :param y: unscaled parameter
    :param weights: weights (sum to 1)
    """

    def __init__(self, id_, y: AbstractParameter, weights: AbstractParameter):
        super(ConvexCombination, self).__init__(id_)
        self._weights = weights
        self._y = y
        self.need_update = False
        self._tensor = self.transform()
        self.listeners = []

    @property
    def x(self) -> Tensor:
        if self.need_update:
            self._tensor = self.transform()
            self.need_update = False
        return self._tensor

    @property
    def weights(self) -> Tensor:
        return self._weights.tensor

    def transform(self):
        return self._y.tensor / (self._y.tensor * self.weights).sum(
            axis=-1, keepdims=True
        )

    def add_parameter_listener(self, listener) -> None:
        self.listeners.append(listener)

    def fire_parameter_changed(self, index=None, event=None) -> None:
        for listener in self.listeners:
            listener.handle_parameter_changed(self, index, event)

    def handle_model_changed(self, model, obj, index) -> None:
        pass

    def handle_parameter_changed(
        self, variable: AbstractParameter, index, event
    ) -> None:
        self.need_update = True
        self.fire_parameter_changed()

    @property
    def sample_shape(self) -> torch.Size:
        return self.tensor.shape[:-1]

    def to(self, *args, **kwargs) -> None:
        for param in self._parameters:
            param.to(*args, **kwargs)
        self.need_update = True

    def cuda(self, device: Optional[Union[int, torch.device]] = None):
        for param in self._parameters:
            param.cuda(device)
        self.need_update = True

    def cpu(self):
        for param in self._parameters:
            param.cpu()
        self.need_update = True

    @staticmethod
    def json_factory(id_: str, y, w):
        return {'id': id_, 'type': 'ConvexCombination', 'y': y, 'weights': w}

    @classmethod
    def from_json(cls, data, dic):
        id_ = data['id']
        if isinstance(data['weights'], list):
            weights = torch.tensor([float(x) for x in data['weights']])
            weights = Parameter(None, weights)
        else:
            weights = process_object(data['weights'], dic)
        y = process_object(data['y'], dic)

        return cls(id_, y, weights)
