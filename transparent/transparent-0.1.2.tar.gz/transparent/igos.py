import os
import numpy as np
import torch
from torch.autograd import Variable
from utils.igos_utils import *


def IGOS(
        model,
        images,
        baselines,
        labels,
        L1=1,
        L2=20,
        size=28,
        ig_iter=15,
        iterations=20,
        alpha=8,
        softmax=True,
        **kwargs
):

    """
        Generates explanation by optimizing a mask with integrated gradient.
        Paper title:  Visualizing Deep Networks by Optimizing with Integrated Gradients, AAAI 2020
        Link to the paper: https://aaai.org/ojs/index.php/AAAI/article/view/6863/6717
    :param model:
    :param images:
    :param baselines:
    :param labels:
    :param L1:
    :param L2:
    :param size:
    :param ig_iter:
    :param iterations:
    :param alpha:
    :param softmax:
    :param kwargs:
    :return:
    """

    def regularization_loss(masks):
        return L1 * torch.mean(torch.abs(1 - masks).view(masks.shape[0], -1), dim=1) + \
               L2 * tv_norm(masks)

        # Define loss function for regularization terms

    def loss_function(up_masks, masks, indices, noise=True):
        losses = interval_score(
            model,
            images[indices],
            baselines[indices],
            labels[indices],
            up_masks,
            ig_iter,
            output_func,
            noise
            )
        return losses.sum(dim=1).view(-1) + regularization_loss(masks)

    # Create initial masks
    masks = torch.ones((images.shape[0], 1, size, size), dtype=torch.float32, device='cuda')
    masks = Variable(masks, requires_grad=True)

    if softmax:
        output_func = softmax_output
    else:
        logit_output.original = torch.gather(torch.nn.Sigmoid()(model(images)), 1, labels.view(-1, 1))
        output_func = logit_output

    for i in range(iterations):

        up_masks = upscale(masks)

        losses = regularization_loss(masks)
        losses.sum().backward()
        total_grads = masks.grad.clone()
        masks.grad.zero_()

        # Computer the integrated gradient
        integrated_gradient(model, images, baselines, labels, up_masks, ig_iter, output_func)
        total_grads += masks.grad.clone()
        masks.grad.zero_()

        # Compute step
        alphas = line_search(masks, total_grads, loss_function, alpha)

        # Update the mask
        masks.data -= total_grads * alphas
        masks.grad.zero_()
        masks.data.clamp_(0, 1)

    return masks
