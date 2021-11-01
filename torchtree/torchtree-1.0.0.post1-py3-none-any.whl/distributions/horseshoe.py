import torch
from torch import Tensor
from torch.distributions import Cauchy, Normal

from ..core.abstractparameter import AbstractParameter
from ..core.model import CallableModel
from ..core.utils import process_object
from ..evolution.tree_model import TimeTreeModel, parse_tree
from ..typing import ID


class ScaleMixtureGaussian(CallableModel):
    def __init__(
        self,
        id_: ID,
        x: AbstractParameter,
        scale: AbstractParameter,
        gamma: AbstractParameter,
    ) -> None:
        super().__init__(id_)
        self.x = x
        self.gobal_scale = scale
        self.local_scale = gamma

    def _call(self, *args, **kwargs) -> Tensor:
        return Normal(0.0, self.gobal_scale.tensor * self.local_scale.tensor).log_prob(
            self.x
        )

    @property
    def sample_shape(self) -> torch.Size:
        return self.x.tensor.shape[:-1]

    def handle_model_changed(self, model, obj, index) -> None:
        pass

    def handle_parameter_changed(
        self, variable: AbstractParameter, index, event
    ) -> None:
        self.fire_model_changed()

    @classmethod
    def from_json(cls, data, dic):
        id_ = data['id']
        x = process_object(data['x'], dic)
        global_scale = process_object(data['global_scale'], dic)
        local_scale = process_object(data['local_scale'], dic)
        return cls(id_, x, global_scale, local_scale)


class HorseShoePrior(CallableModel):
    def __init__(
        self,
        id_: ID,
        x: AbstractParameter,
        scale: AbstractParameter,
        gamma: AbstractParameter,
        tree_model: TimeTreeModel = None,
    ) -> None:
        super().__init__(id_)
        self.x = x
        self.gobal_scale = scale
        self.local_scale = gamma
        self.tree_model = tree_model

    def _call(self, *args, **kwargs) -> Tensor:
        if self.tree_model is not None:
            x = torch.gather(self.x.tensor, ..., self.tree_model.preorder)
            x = x[1:].log() - x[:-1].log()
        else:
            x = self.x

        return Normal(0.0, self.gobal_scale.tensor * self.local_scale.tensor).log_prob(
            x
        ) + Cauchy(0.0, 1.0).log_prob(self.local_scale.tensor)

    @property
    def sample_shape(self) -> torch.Size:
        return self.x.tensor.shape[:-1]

    def handle_model_changed(self, model, obj, index) -> None:
        pass

    def handle_parameter_changed(
        self, variable: AbstractParameter, index, event
    ) -> None:
        self.fire_model_changed()

    @classmethod
    def from_json(cls, data, dic):
        pass


class FinishHorseShoePrior(HorseShoePrior):
    def __init__(
        self,
        id_: ID,
        x: AbstractParameter,
        scale: AbstractParameter,
        gamma: AbstractParameter,
        tree_model: TimeTreeModel = None,
        c: AbstractParameter = None,
    ):
        super().__init__(id_, x, scale, gamma, tree_model)
        self.c = c

    def _call(self, *args, **kwargs) -> Tensor:
        local_scale_tilde = (
            self.c.tensor ** 2
            * self.local_scale.tensor ** 2
            / (
                self.c.tensor ** 2
                + self.gobal_scale.tensor ** 2 * self.local_scale.tensor ** 2
            )
        ).sqrt()

        if self.tree_model is not None:
            x = torch.gather(self.x.tensor, ..., self.tree_model.preorder)
            x = x[1:].log() - x[:-1].log()
        else:
            x = self.x

        return Normal(0.0, self.gobal_scale.tensor * local_scale_tilde).log_prob(
            x
        ) + Cauchy(0.0, 1.0).log_prob(local_scale_tilde)
