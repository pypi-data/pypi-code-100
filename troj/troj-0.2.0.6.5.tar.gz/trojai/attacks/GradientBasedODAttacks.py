import torch


class FGSMObjectDetection:
    def __init__(self, model, epsilon, alpha, num_iter):
        '''
        :param model: an instance of a PytorchObjectDetector object.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param num_iter: Number of steps
        '''
        #TODO allow user to pick certain losses from the ,odel loss dictionary to maximize.
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.num_iter = num_iter

    def generate(self, X, Y, return_examples=True, return_losses=True):
        '''
        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial
        loss and final loss)
        :returns: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True
        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            losses = {}
            if y['labels'].shape[0] >0:
                init_loss = self.model.compute_loss([x], [y], grad=False, reduce=True)
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(
                    torch.zeros_like(x, requires_grad=True), mean=0, std=0.001
                )
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, reduce=True)
                    loss.backward()
                    delta.data = (delta + x.shape[0] * self.alpha * delta.grad.data).clamp(
                        -self.epsilon, self.epsilon
                    )
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts

