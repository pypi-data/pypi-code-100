from art import estimators
import torch
import torch.nn as nn
from trojai.estimators.ClassifierBase import TrojClassifier
import torch.nn as nn

"""
Inherits from the troj base class and the ART Pytorch classifier for Pytorch support
Also implements our ComputeLoss function which will be called by each classifier, should implement as abstract method in base class
"""


class TrojPytorchClassifier(
    estimators.classification.PyTorchClassifier, TrojClassifier
):
    """
    Compute loss computes the loss over a batch of target samples

    :param x: inputs
    :param y: labels, either true labels or original unperturbed model labels. y might need to be expanded along
    the first dimension because of art bug.
    :param return_preds: bool to return model predictions with loss
    :return: Loss values and optionally predictions
    """

    def ComputeLoss(self, x, y, return_preds=True, reduction="none"):

        old_reduction = self._loss.reduction
        self._loss.reduction = reduction
        preds = torch.tensor(self.predict(x))
        y = torch.tensor(y)
        loss_val = self._loss(preds, y)
        self._loss.reduction = old_reduction
        if return_preds:
            return loss_val.numpy(), preds.numpy()
        else:
            return loss_val.numpy()


def flatten(t):
    '''

    :param t: Input array of shape [N, d_1, ..., d_m ]
    :return: flattened array of shape [N, d_1*d_2*...d_m]
    '''
    return t.reshape(t.shape[0], -1)

class NetWrapper(nn.Module):
    # Modified from https://github.com/lucidrains/byol-pytorch
    #for extracting latent, layer can either be string or index.

    def __init__(self, net, layer = -2):
        '''
        A wrapper for extracting latent representations from a Pytorch model.
        :param net: Network to pass to the wrapper
        :param layer: Either layer index or layer name to get the latent representations from.b
        '''
        super().__init__()
        if type(net).__name__==TrojPytorchClassifier:
            self.net = net._model
        else:
            self.net = net
        self.layer = layer

        self.hidden = None
        self.hook_registered = False

    def _find_layer(self):
        '''
        Finds the hidden layer given by the layer input argument.
        :return:
        '''
        if type(self.layer) == str:
            modules = dict([*self.net.named_modules()])
            return modules.get(self.layer, None)
        elif type(self.layer) == int:
            children = [*self.net.children()]
            return children[self.layer]
        return None

    def _hook(self, _, __, output):
        '''

        :param _:
        :param __:
        :param output:
        :return:
        '''
        self.hidden = flatten(output)

    def _register_hook(self):
        '''
        Registers the hook given by _hook in the network at the layer given in the input argument.
        :return:
        '''
        layer = self._find_layer()
        assert layer is not None, f'hidden layer ({self.layer}) not found'
        handle = layer.register_forward_hook(self._hook)
        self.hook_registered = True

    def get_representation(self, x):
        '''
        Given an input, return the latent representation of x
        :param x: batched input to network.
        :return: Batch of output representations.
        '''
        if self.layer == -1:
            return self.net(x)

        if not self.hook_registered:
            self._register_hook()

        _ = self.net(x)
        hidden = self.hidden
        self.hidden = None
        assert hidden is not None, f'hidden layer {self.layer} never emitted an output'
        return hidden

    def forward(self, x):
        representation = self.get_representation(x)

        return representation