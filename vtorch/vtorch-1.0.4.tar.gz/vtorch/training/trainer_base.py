"""
A :class:`~vtorch.training.trainer.Trainer` is responsible for training a
:class:`~vtorch.models.model.Model`.
Typically you might create a configuration file specifying the model and
training parameters and then use :mod:`~vtorch.commands.train`
rather than instantiating a ``Trainer`` yourself.
"""

import logging
from typing import List, Union

import torch.nn

from ..common.checks import ConfigurationError, check_for_gpu

logger = logging.getLogger(__name__)


class TrainerBase:
    """
    The base class for an AllenNLP trainer. It can do pretty much
    anything you want. Your subclass should implement ``train``
    and also probably ``from_params``.
    """

    def __init__(self, cuda_device: Union[int, List[int]] = -1) -> None:
        # TODO: remove multiple GPU training and use single device instead
        check_for_gpu(cuda_device)

        # Configure GPUs:
        if not isinstance(cuda_device, int) and not isinstance(cuda_device, list):
            raise ConfigurationError("Expected an int or list for cuda_device, got {}".format(cuda_device))

        if isinstance(cuda_device, list):
            self._multiple_gpu = True
            self._cuda_devices = cuda_device
        else:
            self._multiple_gpu = False
            self._cuda_devices = [cuda_device]

    def train(self) -> torch.nn.Module:
        """
        Train a model and return the results.
        """
        raise NotImplementedError
