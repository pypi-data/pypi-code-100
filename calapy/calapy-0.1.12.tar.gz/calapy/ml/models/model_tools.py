

import torch as pt
import types

__all__ = ['freeze', 'unfreeze']


def freeze(model: pt.nn.Module):
    # Now set requires_grad to false
    for param_model in model.parameters():
        param_model.requires_grad = False


def unfreeze(model: pt.nn.Module):
    # Now set requires_grad to false
    for param_model in model.parameters():
        param_model.requires_grad = True


dict_locals = locals().copy()
dict_functions = {}

for key_l, value_l in dict_locals.items():
    if isinstance(value_l, types.FunctionType) and (value_l in __all__):
        dict_functions.update({key_l: value_l})


class ModelMethods:

    freeze = freeze
    unfreeze = unfreeze
