import torch
import torch.nn as nn
from collections import defaultdict
import art.estimators.object_detection.python_object_detector

def ODPredsFormatting(predictions,  keys, new_keys):
    '''
    Takes in output of Pytorch object detection, and converts it to the appropriate dictionary format for postprocessing.
    :param predictions: List of output dictionaries from model.
    :param keys: Keys in the old prediction dictionarys.
    :param new_keys: Keys for the new prediction dictionary.
    '''
    preds_dict = defaultdict(list)
    for preds in predictions:
        for key_idx in range(len(keys)):
            key_vals = preds[keys[key_idx]].detach().cpu().numpy()
            key_vals = key_vals.tolist()
            preds_dict[new_keys[key_idx]].append(key_vals)
    return dict(preds_dict)

class PytorchObjectDetector(nn.Module):
    def __init__(self, model, **art_od_kwargs):
        """

        :param model: Pytorch Object Detection model
        """
        super(PytorchObjectDetector, self).__init__()
        self.model = model
        self.art_model = art.estimators.object_detection.python_object_detector.PyTorchObjectDetector(model, **art_od_kwargs)

    def compute_loss(self, samples, labels, grad=False, reduce=True):
        """
        :param: samples: Samples to make predictions on as list of tensors.
        :param: labels: labels as list of dictionaries
        :param: grad: If true, the gradient is computed.
        :param: reduce: If true, the losses are reduced via summation and a single scalar is returned, otherwise a dictionary is returned.
        """
        self.model.train()
        if grad == False:
            with torch.no_grad():
                losses = self.model(samples, labels)
        else:
            losses = self.model(samples, labels)
        if reduce:
            losses = sum(loss for loss in losses.values())
        return losses

    def predict(self, sample):
        self.model.eval()
        preds = self.model(sample)
        return preds