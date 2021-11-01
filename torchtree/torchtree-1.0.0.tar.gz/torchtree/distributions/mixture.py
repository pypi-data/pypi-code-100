from typing import List, Union

import torch.distributions

from .. import Parameter
from ..core.model import Model
from ..core.utils import process_object, process_objects
from ..typing import ID
from .distributions import DistributionModel


class MixtureDistributionModel(DistributionModel):
    """Mixture of distributions.

    :param id_: ID of joint distribution
    :param distributions: list of distributions of type DistributionModel or
        CallableModel
    :param weights: mixture weights
    """

    def __init__(
        self, id_: ID, distributions: List[DistributionModel], weights: Parameter
    ) -> None:
        super().__init__(id_)
        for distr in distributions:
            setattr(self, distr.id, distr)
        self.weights = weights

    def log_prob(self, x: Union[List[Parameter], Parameter] = None) -> torch.Tensor:
        log_p = []
        for distr in self._models:
            log_p_component = distr()
            sample_shape = distr.sample_shape
            if log_p_component.shape == sample_shape:
                log_p.append(log_p_component.unsqueeze(-1))
            elif log_p_component.shape == torch.Size([]):
                log_p.append(log_p_component.unsqueeze(0))
            elif log_p_component.shape[-1] != 1:
                log_p.append(log_p_component.sum(-1, keepdim=True))
            elif log_p_component.dim() == 1:
                log_p.append(log_p_component.expand(self.sample_shape + (1,)))
            else:
                log_p.append(log_p_component)
        return torch.logsumexp(torch.cat(log_p, -1) + self.weights.tensor.log(), -1)

    def _call(self, *args, **kwargs) -> torch.Tensor:
        return self.log_prob()

    def rsample(self, sample_shape=torch.Size()) -> None:
        raise NotImplementedError

    def sample(self, sample_shape=torch.Size()) -> None:
        raise NotImplementedError

    def handle_model_changed(self, model: Model, obj, index) -> None:
        self.fire_model_changed()

    def handle_parameter_changed(self, variable: Parameter, index, event) -> None:
        self.fire_model_changed()

    @property
    def sample_shape(self) -> torch.Size:
        shape = self.weights.shape
        for distr in self._models:
            if len(distr.sample_shape) > len(shape):
                shape = distr.sample_shape
        return shape

    @classmethod
    def from_json(cls, data, dic):
        id_ = data['id']
        distributions = process_objects(data['distributions'], dic)
        weights = process_object(data['weights'], dic)
        return cls(id_, distributions, weights)
