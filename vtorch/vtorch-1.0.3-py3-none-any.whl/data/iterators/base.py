from typing import Dict, Iterable, Iterator, Sequence, Tuple

import torch

from ..entity import InstanceFeatureVectors


class DataIterator(object):
    def __call__(
        self, instances: Iterable[InstanceFeatureVectors], shuffle: bool = True
    ) -> Iterator[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]:
        raise NotImplementedError()

    def get_num_batches(self, instances: Iterable[InstanceFeatureVectors]) -> int:
        """
        Returns the number of batches that ``dataset`` will be split into; if you want to track
        progress through the batch with the generator produced by ``__call__``, this could be
        useful.
        """
        raise NotImplementedError()
