from typing import List

import torch as T
import torch.nn as nn
import torch.nn.functional as F


class FFNN(nn.Module):

    def __init__(self, features: List):
        super().__init__()
        # the feature list will be [input, hidden..., output]
        nodes = []
        for i in range(len(features) - 1):
            nodes.append((features[i], features[i + 1]))
        self._layers = [nn.Linear(feature[0], feature[1]) for feature in nodes]
        self.input_layer = self._layers[0]
        self.output_layer = self._layers[-1]
        self.hidden_layers = self._layers[1:-1]
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu:0')

    def forward(self, input) -> T.tensor:
        state = T.Tensor(input).to(self.device)
        x = F.relu(self.input_layer(state))

        for layer in self.hidden_layers:
            x = F.relu(layer(x))

        x = self.output_layer(x)
        return x

    def layers(self) -> List:
        return self._layers

    def layer_sizes(self) -> List:
        return [layer.weight.data.size() for layer in self._layers]

    def set_layer_data(self, layer_data):
        if len(layer_data) == len(self._layers):
            for new_layer, old_layer in zip(layer_data, self._layers):
                if old_layer.weight.data.size() == new_layer.size():
                    old_layer.weight.data = new_layer
                else:
                    raise ValueError(f"Layer dimensions do not match. New: {new_layer.size()} != Old: {old_layer.weight.data.size()}")
        else:
            raise ValueError(f"Number of new layers does not match number of old layers. New: {len(layer_data)} != Old: {len(self._layers)}")
