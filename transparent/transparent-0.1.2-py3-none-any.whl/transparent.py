import os
import sys
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import tensorflow as tf
import keras
import torch, torchvision, torchsummary
import warnings
warnings.filterwarnings("ignore")


class TransparentAI:
    """

    """
    def __init__(self, model, model_backend, data):
        """

        :param model:
        :param model_backend:
        :param data:
        """
        assert model_backend in ["tf", "torch"], "model_backend: tf or torch"
        self.model = model
        self.model_backend = model_backend
        self.data = data

    def _preprocess(self):
        pass

    def _load_data(self):
        pass

    def explain_instance(self, explainer, input_img):
        pass


class TransparentAI_CV(TransparentAI):
    """

    """
    def __init__(self, model, model_backend, data, img_size, labels):
        """

        :param model:
        :param model_backend:
        :param data:
        :param img_size:
        :param labels:
        """
        super().__init__(model, model_backend, data)
        self.img_size = img_size
        self.labels = labels
        self.num_classes = len(np.unique(self.labels))


class TransparentAI_NLP(TransparentAI):
    """

    """
    def __init__(self, model, model_backend, data, labels):
        """

        :param model:
        :param model_backend:
        :param data:
        :param labels:
        """
        super().__init__(model, model_backend, data)
        self.labels = labels
        self.num_classes = len(np.unique(self.labels))
