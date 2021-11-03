import itertools
import logging
import math
import random
from collections import defaultdict
from typing import Dict, Iterable, Iterator, List, Optional, Sequence, Tuple, Union

import torch

from vtorch.common.utils import ensure_list, is_lazy
from vtorch.data.entity import InstanceFeatureVectors
from vtorch.data.iterators.base import DataIterator
from vtorch.data.iterators.batch import Batch

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BaseDataIterator(DataIterator):
    """
    An abstract ``DataIterator`` class. ``DataIterators`` must override ``_create_batches()``.
    Parameters
    ----------
    batch_size : ``int``, optional, (default = 32)
        The size of each batch of instances yielded when calling the iterators.
    instances_per_epoch : ``int``, optional, (default = None)
        If specified, each epoch will consist of precisely this many instances.
        If not specified, each epoch will consist of a single pass through the dataset.
    cache_instances : ``bool``, optional, (default = False)
        If true, the iterators will cache the tensorized instances in memory.
        If false, it will do the tensorization anew each iteration.
    maximum_samples_per_batch : ``Tuple[str, int]``, (default = None)
        If specified, then is a tuple (padding_key, limit) and we will ensure
        that every batch is such that batch_size * sequence_length <= limit
        where sequence_length is given by the padding_key. This is done by
        moving excess instances to the next batch (as opposed to dividing a
        large batch evenly) and should result in a fairly tight packing.
    """

    default_implementation = "bucket"

    def __init__(
        self,
        batch_size: int,
        instances_per_epoch: Optional[int] = None,
        cache_instances: bool = True,
        maximum_samples_per_batch: Optional[Tuple[Tuple[str, str], int]] = None,
        num_epochs_per_instances: Union[int, None] = 1,
        shuffle_random: Optional[random.Random] = None,
    ) -> None:
        self._batch_size = batch_size
        self._instances_per_epoch = instances_per_epoch
        self._maximum_samples_per_batch = maximum_samples_per_batch
        self._num_epochs_per_instances = num_epochs_per_instances
        self.shuffle_random = shuffle_random or random.Random()
        # We might want to cache the instances in memory.
        self._cache_instances = cache_instances
        self._cache: Dict[int, List[Tuple[Dict[str, Dict[str, torch.Tensor]], List[int]]]] = defaultdict(list)

        # We also might want to add the epoch number to each instance.
        self._epochs: Dict[int, int] = defaultdict(int)

        # We also might want to keep track of cursors;
        # for example, if each epoch represents less than one pass through the dataset,
        # we want to remember where we left off. As `Iterator`s are not necessarily hashable,
        # we use their id() as the key.
        self._cursors: Dict[int, Iterator[InstanceFeatureVectors]] = {}

    def restore(
        self, instances: Iterable[InstanceFeatureVectors], sequence: Iterable[int]
    ) -> Iterable[InstanceFeatureVectors]:
        pass

    def set_num_epochs_per_instances(self, num_epochs_per_instances: Union[int, None]) -> None:
        self._num_epochs_per_instances = num_epochs_per_instances

    def __call__(
        self, instances: Iterable[InstanceFeatureVectors], shuffle: bool = True
    ) -> Iterator[Tuple[Dict[str, Dict[str, torch.Tensor]], Sequence[int]]]:
        """
        Returns a generator that yields batches over the given dataset
        for the given number of epochs. If ``num_epochs`` is not specified,
        it will yield batches forever.
        Parameters
        ----------
        instances : ``Iterable[InstanceFeatureVectors]``
            The instances in the dataset. IMPORTANT: this must be able to be
            iterated over *multiple times*. That is, it must be either a List
            or some other object whose ``__iter__`` method returns a fresh iterators
            each time it's called.
        num_epochs : ``int``, optional (default=``None``)
            How times should we iterate over this dataset?  If ``None``, we will iterate over it
            forever.
        shuffle : ``bool``, optional (default=``True``)
            If ``True``, we will shuffle the instances in ``dataset`` before constructing batches
            and iterating over the instances.
        """
        # Instances is likely to be a list, which cannot be used as a key,
        # so we take the object id instead.
        key = id(instances)
        starting_epoch = self._epochs[key]

        if self._num_epochs_per_instances is None:
            epochs: Iterable[int] = itertools.count(starting_epoch)
        else:
            epochs = range(starting_epoch, starting_epoch + self._num_epochs_per_instances)

        for epoch in epochs:
            if self._cache_instances and key in self._cache:
                # Serve the results from the cache.
                cache = self._cache[key]
                tensor_dicts = [example[0] for example in cache]
                batched_instance_ids = [example[1] for example in cache]

                if shuffle:
                    batch_ids = list(range(len(tensor_dicts)))
                    self.shuffle_random.shuffle(batch_ids)
                    tensor_dicts = [tensor_dicts[i] for i in batch_ids]
                    batched_instance_ids = [batched_instance_ids[i] for i in batch_ids]

                for tensor_dict, instance_ids in zip(tensor_dicts, batched_instance_ids):
                    yield tensor_dict, instance_ids
            else:
                batches = self._create_batches(instances, shuffle)

                # Should we add the instances to the cache this epoch?
                add_to_cache = self._cache_instances and key not in self._cache

                for example in batches:

                    batch: Batch = example[0]
                    instance_ids: List[int] = example[1]  # type: ignore

                    tensor_dict: Dict[str, Dict[str, torch.Tensor]] = batch.as_tensor_dict()  # type: ignore

                    if add_to_cache:
                        self._cache[key].append((tensor_dict, instance_ids))

                    yield tensor_dict, instance_ids

            # Increment epoch tracker
            self._epochs[key] = epoch + 1

    def _take_instances(
        self, instances: Iterable[InstanceFeatureVectors], max_instances: Optional[int] = None
    ) -> Iterator[InstanceFeatureVectors]:
        """
        Take the next `max_instances` instances from the given dataset.
        If `max_instances` is `None`, then just take all instances from the dataset.
        If `max_instances` is not `None`, each call resumes where the previous one
        left off, and when you get to the end of the dataset you start again from the beginning.
        """
        # If max_instances isn't specified, just iterate once over the whole dataset
        if max_instances is None:
            yield from iter(instances)
        else:
            # If we don't have a cursor for this dataset, create one. We use ``id()``
            # for the key because ``instances`` could be a list, which can't be used as a key.
            key = id(instances)
            iterator = self._cursors.get(key, iter(instances))

            while max_instances > 0:
                try:
                    # If there are instances left on this iterators,
                    # yield one and decrement max_instances.
                    yield next(iterator)
                    max_instances -= 1
                except StopIteration:
                    # None left, so start over again at the beginning of the dataset.
                    iterator = iter(instances)

            # We may have a new iterators, so update the cursor.
            self._cursors[key] = iterator

    def get_num_batches(self, instances: Iterable[InstanceFeatureVectors]) -> int:
        """
        Returns the number of batches that ``dataset`` will be split into; if you want to track
        progress through the batch with the generator produced by ``__call__``, this could be
        useful.
        """
        if is_lazy(instances) and self._instances_per_epoch is None:
            # Unable to compute num batches, so just return 1.
            return 1
        elif self._instances_per_epoch is not None:
            return math.ceil(self._instances_per_epoch / self._batch_size)
        else:
            # Not lazy, so can compute the list length.
            return math.ceil(len(ensure_list(instances)) / self._batch_size)

    def _create_batches(
        self, instances: Iterable[InstanceFeatureVectors], shuffle: bool
    ) -> Iterable[Tuple[Batch, List[int]]]:
        """
        This method should return one epoch worth of batches.
        """
        raise NotImplementedError
