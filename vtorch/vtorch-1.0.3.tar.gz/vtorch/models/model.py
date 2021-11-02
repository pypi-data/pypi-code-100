from torch.nn import Module

from ..common.persistance import Persistent

# TODO: create MODELS_OUTPUTS_LOGITS_ID, MODELS_OUTPUTS_LOSS_ID to use it everywhere?


class IModel(Module, Persistent):
    pass
