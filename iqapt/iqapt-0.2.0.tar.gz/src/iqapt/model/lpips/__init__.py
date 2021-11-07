from .alex_net import AlexNet
from .vgg16 import Vgg16
from .squeeze_net import SqueezeNet

models = {'alex': AlexNet, 'vgg16': Vgg16, 'squeeze': SqueezeNet}
channels = {
    'alex': [63, 192, 384, 256, 256],
    'vgg16': [64, 128, 256, 512, 512],
    'squeeze': [64, 128, 256, 384, 384, 512, 512]
}

__all__ = ['AlexNet', 'Vgg16', 'SqueezeNet']
