import json
import logging
import os
from typing import Iterable, List, Optional, Tuple, Union

from vtorch.data.entity import InstanceFeatureVectors

from ...common.checks import ConfigurationError
from ...data.iterators import BucketIterator
from .batch import Batch
from .bucket_iterator import get_batch_lengths

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class BucketIteratorOptimized(BucketIterator):
    """
    An iterators which by default, pads batches with respect to the maximum input lengths `per
    batch`. Additionally, you can provide a list of field names and padding keys which the dataset
    will be sorted by before doing this batching, causing inputs with similar length to be batched
    together, making computation more efficient (as less time is wasted on padded elements of the
    batch).
    Parameters
    ----------
    sorting_keys : List[Tuple[str, str]]
        To bucket inputs into batches, we want to group the instances by padding length, so that we
        minimize the amount of padding necessary per batch. In order to do this, we need to know
        which fields need what type of padding, and in what order.
        For example, ``[("sentence1", "num_tokens"), ("sentence2", "num_tokens"), ("sentence1",
        "num_token_characters")]`` would sort a dataset first by the "num_tokens" of the
        "sentence1" field, then by the "num_tokens" of the "sentence2" field, and finally by the
        "num_token_characters" of the "sentence1" field.
        documentation somewhere that gives the standard padding keys used by different fields.
    biggest_batch_first : bool, optional (default=False)
        This is largely for testing, to see how large of a batch you can safely use with your GPU.
        This will let you try out the largest batch that you have in the instances `first`, so that if
        you're going to run out of memory, you know it early, instead of waiting through the whole
        epoch to find out at the end that you're going to crash.
        Note that if you specify ``max_instances_in_memory``, the first batch will only be the
        biggest from among the first "max instances in memory" instances.
    batch_size : int, optional, (default = 32)
        The size of each batch of instances yielded when calling the iterators.
    instances_per_epoch : int, optional, (default = None)
        See :class:`BasicIterator`.
    maximum_samples_per_batch : ``Tuple[str, int]``, (default = None)
        See :class:`BasicIterator`.
    """

    MAX_BATCH_SIZE = 150

    def __init__(
        self,
        sorting_keys: List[str],
        biggest_batch_first: bool = False,
        batch_size: int = 32,
        instances_per_epoch: Optional[int] = None,
        cache_instances: bool = False,
        maximum_samples_per_batch: Optional[Tuple[Tuple[str, str], int]] = None,
        batch_optimization_step_size: int = 10,
        batch_reverse_sort: bool = False,
        num_epochs_per_instances: Union[int, None] = 1,
    ) -> None:
        if not sorting_keys:
            raise ConfigurationError("BucketIterator requires field_keys to be specified")

        super().__init__(
            sorting_keys=sorting_keys,
            biggest_batch_first=biggest_batch_first,
            batch_size=batch_size,
            instances_per_epoch=instances_per_epoch,
            cache_instances=cache_instances,
            maximum_samples_per_batch=maximum_samples_per_batch,
            num_epochs_per_instances=num_epochs_per_instances,
            batch_reverse_sort=batch_reverse_sort,
        )

        self._batch_optimization_step_size = batch_optimization_step_size
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "length_bs_time.json")), "r") as fp:
            self._length_bs_time = json.load(fp)

    def _get_new_batch(
        self, current_batch: List[InstanceFeatureVectors], left_data: List[InstanceFeatureVectors]
    ) -> Tuple[List[InstanceFeatureVectors], List[InstanceFeatureVectors], List[InstanceFeatureVectors]]:
        # batch could not be bigger then maximum batch size
        if len(current_batch) >= self.MAX_BATCH_SIZE - self._batch_optimization_step_size:
            return (
                current_batch,
                left_data[: self._batch_optimization_step_size],
                left_data[self._batch_optimization_step_size :],
            )
        # add to current batch left instances, if its size smaller then _batch_optimization_step_size
        if len(left_data) < self._batch_optimization_step_size + 1:
            return current_batch + left_data, [], []

        # we will consider first vector length here, assuming that first key is `self._sorting_keys` has max priority
        current_batch_lengths = [
            field_vector_length[0]
            for field_vector_length in get_batch_lengths(instances=current_batch, field_keys=self._sorting_keys)
        ]
        batch_max_length = max(current_batch_lengths)
        contender_max_length = max(current_batch_lengths[: self._batch_optimization_step_size])
        if (
            self._length_bs_time[f"{contender_max_length}"][
                f"{len(current_batch) + self._batch_optimization_step_size}"
            ]
            > self._length_bs_time[f"{batch_max_length}"][f"{len(current_batch)}"]
            + self._length_bs_time[f"{contender_max_length}"][f"{self._batch_optimization_step_size}"]
        ):
            return (
                current_batch,
                left_data[: self._batch_optimization_step_size],
                left_data[self._batch_optimization_step_size :],
            )
        return self._get_new_batch(
            current_batch + left_data[: self._batch_optimization_step_size],
            left_data[self._batch_optimization_step_size :],
        )

    def _form_batches(self, instances: Iterable[InstanceFeatureVectors]) -> List[Batch]:
        # as parent's method, this method doesn't change instance order
        instances = list(instances)
        if len(instances) <= self._batch_optimization_step_size:
            return [Batch(instances)]

        batches = []
        current_batch = instances[: self._batch_optimization_step_size]
        left_data = instances[self._batch_optimization_step_size :]
        while len(current_batch) > 0:
            final_batch, current_batch, left_data = self._get_new_batch(current_batch, left_data)
            batches.append(Batch(final_batch))

        return batches
