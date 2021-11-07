import torch
import torch.nn as nn
from abc import abstractclassmethod
from . import utils


class Metric(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    @torch.no_grad()
    def forward(self, input_a, input_b):
        input_size = utils.check_img_size(input_a, input_b)

        if input_size != None:
            if len(input_size) == 4:
                N, C, H, W = input_size
                results = [None] * N
                paired_img_set = [
                    (index, img_a, img_b)
                    for index, (img_a,
                                img_b) in enumerate(zip(input_a, input_b))
                ]

                # TODO: optimized by multithreads
                for n in range(N):
                    index, img_a, img_b = paired_img_set[n]
                    results[index] = self.calc(img_a, img_b)
            elif len(input_size) == 3:
                C, H, W = input_size
                results = [None]
                img_a, img_b = input_a, input_b
                results[0] = self.calc(img_a, img_b)
            elif len(input_size) == 2:
                H, W = input_size
                img_a, img_b = torch.unsqueeze(input_a,
                                               0), torch.unsqueeze(input_b, 0)
                results = [None]
                results[0] = self.calc(img_a, img_b)
            else:
                msg = 'the shape of input_a{} and input_b{} should be N,C,H,W or C,H,W or H,W.'.format(
                    tuple(input_a.shape), tuple(input_b.shape))
                raise ValueError(msg)
        else:
            msg = 'the shape of input_a{} and input_b{} should be the same.'.format(
                tuple(input_a.shape), tuple(input_b.shape))
            raise ValueError(msg)

        return torch.stack(results)

    @abstractclassmethod
    def calc(self, img_a: torch.Tensor, img_b: torch.Tensor):
        '''
        implemented by sub class.
        '''
        msg = 'calc should be implemented by subclass.'
        raise NotImplementedError(msg)
