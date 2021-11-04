import abc
from littlenn.optimizers.sgd_factory import SGDFactory
from littlenn.optimizers.rmsprop_factory import RMSPropFactory
from littlenn.optimizers.adam_factory import AdamFactory
from littlenn.losses.categorical_crossentropy_with_logits import CategoricalCrossEntropyWithLogits
from littlenn.losses.binary_crossentropy import BinaryCrossEntropy
from littlenn.metrics.binary_accuracy import BinaryAccuracy
from littlenn.metrics.categorical_accuracy import CategoricalAccuracy

class Model(abc.ABC):
    def __init__(self):
        self.optimizers = {"sgd" : SGDFactory(), "rmsprop" : RMSPropFactory(),
                           "adam" : AdamFactory()}
        self.losses = {"binary_crossentropy" : BinaryCrossEntropy(), "categorical_crossentropy_with_logits" : CategoricalCrossEntropyWithLogits()}
        self.metrics = {"binary_crossentropy" : BinaryAccuracy(), "categorical_crossentropy_with_logits" : CategoricalAccuracy()}