# https://medium.com/technology-invention-and-more/how-to-build-a-multi-layered-neural-network-in-python-53ec3d1d326a
from typing import List
from numpy import exp, random, dot, ndarray, array
from json import load


class NeuronLayer:
    def __init__(self, number_of_neurons: int = 0, number_of_inputs_per_neuron: int = 0, weights: ndarray = None):
        if weights:
            self.synaptic_weights = array(weights)
        else:
            self.synaptic_weights: ndarray = 2 * random.random((number_of_inputs_per_neuron, number_of_neurons)) - 1
    
    def __str__(self):
        return str(self.synaptic_weights)


class NeuralNetwork:
    def __init__(self, layers: List[int] = None, file_name: str = None):
        self.layers: List[NeuronLayer] = []
        if layers:
            for i in range(1, len(layers)):
                self.layers.append(NeuronLayer(layers[i], layers[i - 1]))
        elif file_name:
            with open(file_name) as file:
                for layer in load(file):
                    self.layers.append(NeuronLayer(weights = layer))
        else:
            raise ValueError('Provide exactly one argument')
    
    def __sigmoid(self, x: ndarray) -> ndarray:
        return 1 / (1 + exp(-x))
    
    def __sigmoid_derivative(self, x: ndarray) -> ndarray:
        return x * (1 - x)
    
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            outputs = self.think(training_set_inputs)
            
            last_layer_error = training_set_outputs - outputs[-1]
            last_layer_delta = last_layer_error * self.__sigmoid_derivative(outputs[-1])
            deltas: List[ndarray] = [None for _ in range(len(self.layers))]
            deltas[-1] = last_layer_delta
            
            for i in reversed(range(0, len(self.layers) - 1)):
                layer_error = deltas[i + 1].dot(self.layers[i + 1].synaptic_weights.T)
                layer_delta = layer_error * self.__sigmoid_derivative(outputs[i])
                deltas[i] = layer_delta
            
            first_layer_adjustment = training_set_inputs.T.dot(deltas[0])
            adjustments = [first_layer_adjustment]
            for i in range(1, len(self.layers)):
                adjustments.append(outputs[i - 1].T.dot(deltas[i]))
            
            for i, layer in enumerate(self.layers):
                layer.synaptic_weights += adjustments[i]
    
    def think(self, inputs: ndarray) -> List[ndarray]:
        output_layer = [self.__sigmoid(dot(inputs, self.layers[0].synaptic_weights))]
        for i in range(1, len(self.layers)):
            output_layer.append(self.__sigmoid(dot(output_layer[-1], self.layers[i].synaptic_weights)))
        return output_layer
    
    def print_weights(self):
        for layer in self.layers:
            print(layer.synaptic_weights)
    
    def __str__(self):
        return '\n'.join(map(str, self.layers))
