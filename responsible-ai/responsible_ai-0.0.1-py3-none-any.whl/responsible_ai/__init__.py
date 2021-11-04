import math

import torch as tr
from torch.optim import Adam
from torch.utils.data import DataLoader

import pytorch_lightning as pl
from hydra_zen import builds, just, make_config, make_custom_builds_fn, instantiate


from typing import Callable, Type

import pytorch_lightning as pl
import torch as tr
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from hydra_zen.typing import Partial


def single_layer_nn(num_neurons: int) -> nn.Module:
    """y = sum(V sigmoid(X W + b))"""
    return nn.Sequential(
        nn.Linear(1, num_neurons),
        nn.Sigmoid(),
        nn.Linear(num_neurons, 1, bias=False),
    )


class UniversalFuncModule(pl.LightningModule):
    def __init__(
        self,
        model: nn.Module,
        optim: Partial[optim.Adam],
        dataloader: Type[DataLoader],
        target_fn: Callable[[tr.Tensor], tr.Tensor],
        training_domain: tr.Tensor,
    ):
        super().__init__()
        self.optim = optim
        self.dataloader = dataloader
        self.training_domain = training_domain
        self.target_fn = target_fn

        self.model = model

    def forward(self, x):
        return self.model(x)

    def configure_optimizers(self):
        # provide optimizer with model parameters
        return self.optim(self.parameters())

    def training_step(self, batch, batch_idx):
        x, y = batch
        # compute |cos(x) - model(x)|^2
        return F.mse_loss(self.model(x), y)

    def train_dataloader(self):
        # generate dataset: x, cos(x)
        x = self.training_domain.reshape(-1, 1)
        y = self.target_fn(x)
        return self.dataloader(TensorDataset(x, y))


pbuilds = make_custom_builds_fn(zen_partial=True, populate_full_signature=True)

OptimConf = pbuilds(Adam)

LoaderConf = pbuilds(
    DataLoader, batch_size=25, shuffle=True, drop_last=True, zen_partial=True
)

ModelConf = builds(single_layer_nn, num_neurons=10)

# configure our lightning module
LitConf = pbuilds(
    UniversalFuncModule,
    model=ModelConf,
    target_fn=just(tr.cos),
    training_domain=builds(
        tr.linspace, start=-2 * math.pi, end=2 * math.pi, steps=1000
    ),
)

TrainerConf = builds(
    pl.Trainer, max_epochs=100, gpus=0, progress_bar_refresh_rate=0, zen_partial=False
)

ExperimentConfig = make_config(
    optim=OptimConf,
    dataloader=LoaderConf,
    lit_module=LitConf,
    trainer=TrainerConf,
    seed=1,
)


def task_function(cfg: ExperimentConfig):
    pl.seed_everything(cfg.seed)

    obj = instantiate(cfg)

    # finish instantiating the lightning module, data-loader, and optimizer
    lit_module = obj.lit_module(dataloader=obj.dataloader, optim=obj.optim)

    # train the model
    obj.trainer.fit(lit_module)

    # evaluate the model over the domain to assess the fit
    data = lit_module.training_domain
    final_fit = lit_module.forward(data.reshape(-1, 1))

    # return the trained model instance and the final fit
    return (
        lit_module,
        final_fit.detach().numpy().ravel(),
    )
