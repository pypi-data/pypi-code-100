import logging
import random
from collections import deque
from typing import Deque, Iterable, List, Optional, Tuple, Union

from vtorch.common.checks import ConfigurationError
from vtorch.common.utils import argsort, lazy_groups_of
from vtorch.data.entity import InstanceFeatureVectors
from vtorch.data.iterators.batch import Batch
from vtorch.data.iterators.data_iterator import BaseDataIterator

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def get_batch_lengths(instances: Iterable[InstanceFeatureVectors], field_keys: Iterable[str]) -> List[Tuple[int, ...]]:
    lengths = []
    for instance in instances:
        field_lengths = []
        for field_name in field_keys:
            for _, feature_vector in sorted(instance[field_name].items(), key=lambda t: t[0]):
                field_lengths.append(len(feature_vector))
        lengths.append(tuple(field_lengths))
    return lengths


def argsort_by_fields(
    instances: Iterable[InstanceFeatureVectors], sorting_keys: Iterable[str], reverse: bool = False
) -> List[int]:
    """
    Sorts the instances by their padding lengths, using the keys in
    ``sorting_keys`` (in the order in which they are provided).  ``sorting_keys`` is a list of
    ``(field_name)`` tuples.
    """
    instances = list(instances)
    lengths = get_batch_lengths(instances=instances, field_keys=sorting_keys)
    # note that as get_batch_lengths returns List[Tuple[int, ...]] this argsort is not equivalent to the numpy.argsort
    sort_indices = argsort(lengths)[:: -1 if reverse else 1]
    return sort_indices


class BucketIterator(BaseDataIterator):
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
    batch_size : int, optional, (default = 32)
        The size of each batch of instances yielded when calling the iterators.
    biggest_batch_first : bool, optional (default=False)
        This is largely for testing, to see how large of a batch you can safely use with your GPU.
        This will let you try out the largest batch that you have in the instances `first`, so that if
        you're going to run out of memory, you know it early, instead of waiting through the whole
        epoch to find out at the end that you're going to crash.
        Note that if you specify ``max_instances_in_memory``, the first batch will only be the
        biggest from among the first "max instances in memory" instances.
    instances_per_epoch : int, optional, (default = None)
        See :class:`BaseDataIterator`.
    cache_instances : bool, optional, (default = False)
        See :class:`BaseDataIterator`.
    maximum_samples_per_batch : ``Tuple[str, int]``, (default = None)
        See :class:`BasicIterator`.
    num_epochs_per_instances : ``Union[int, None]``, (default = 1)
    batch_reverse_sort: bool, optional  (default = False)
        If True, bigger batches by lengths will go first
    sampling_rate_namespace: str, optional (default = None)
        To use sampling you need to provide `sampling_rate_namespace` and `sampling_rate_field` to retrieve
         sampling rate form Instance
    sampling_rate_field: str, optional (default = None)
        See `sampling_rate_namespace`
    """

    def __init__(
        self,
        sorting_keys: List[str],
        batch_size: int,
        biggest_batch_first: bool = False,
        instances_per_epoch: Optional[int] = None,
        cache_instances: bool = False,
        maximum_samples_per_batch: Optional[Tuple[Tuple[str, str], int]] = None,
        num_epochs_per_instances: Union[int, None] = 1,
        shuffle_random: Optional[random.Random] = None,
        batch_reverse_sort: bool = False,
        sampling_rate_namespace: Optional[str] = None,
        sampling_rate_field: Optional[str] = None,
        sampling_random: Optional[random.Random] = None,
    ) -> None:
        if not sorting_keys:
            raise ConfigurationError("BucketIterator requires field_keys to be specified")

        super().__init__(
            cache_instances=cache_instances,
            batch_size=batch_size,
            instances_per_epoch=instances_per_epoch,
            maximum_samples_per_batch=maximum_samples_per_batch,
            num_epochs_per_instances=num_epochs_per_instances,
            shuffle_random=shuffle_random,
        )
        self._sorting_keys = sorting_keys
        self._biggest_batch_first = biggest_batch_first
        self._batch_reverse_sort = batch_reverse_sort
        self._sampling_rate_namespace = sampling_rate_namespace
        self._sampling_rate_field = sampling_rate_field
        self.sampling_random = sampling_random or random.Random()

    def _create_batches(
        self, instances: Iterable[InstanceFeatureVectors], shuffle: bool
    ) -> Iterable[Tuple[Batch, List[int]]]:
        sampled_instances = []
        if self._sampling_rate_namespace is not None and self._sampling_rate_field is not None:
            for instance in instances:
                sampling_rate = instance[self._sampling_rate_namespace][self._sampling_rate_field][0]  # TODO: .get()?
                if self.sampling_random.random() < sampling_rate:
                    instance_copy = {
                        namespace: feature_vectors
                        for namespace, feature_vectors in instance.items()
                        if namespace != self._sampling_rate_namespace
                    }
                    sampled_instances.append(instance_copy)
        else:
            sampled_instances = [dict(instance) for instance in instances]
        sort_indices = argsort_by_fields(sampled_instances, self._sorting_keys, reverse=self._batch_reverse_sort)
        sampled_instances = [sampled_instances[i] for i in sort_indices]
        batches = self._form_batches(sampled_instances)  # after this step batches can differ in size
        batched_ids = self._batchify_ids(instance_ids=sort_indices, batched_instances=batches)
        batches, batched_ids = self._biggest_batch_first_and_shuffle(batches, shuffle, batched_ids)

        yield from zip(batches, batched_ids)

    @staticmethod
    def _batchify_ids(instance_ids: List[int], batched_instances: List[Batch]) -> List[List[int]]:
        batched_ids: List[List[int]] = []
        for batch in batched_instances:
            num_appended_ids = sum(len(batch_ids) for batch_ids in batched_ids)
            ids_slice = slice(num_appended_ids, num_appended_ids + len(batch.instances))
            batched_ids.append(instance_ids[ids_slice])
        return batched_ids

    def _form_batches(self, instances: Iterable[InstanceFeatureVectors]) -> List[Batch]:
        batches = []
        excess: Deque[InstanceFeatureVectors] = deque()
        for batch_instances in lazy_groups_of(iter(instances), self._batch_size):
            for possibly_smaller_batches in self._ensure_batch_is_sufficiently_small(batch_instances, excess):
                batches.append(Batch(possibly_smaller_batches))
        if excess:
            batches.append(Batch(excess))
        return batches

    def _ensure_batch_is_sufficiently_small(
        self, batch_instances: Iterable[InstanceFeatureVectors], excess: Deque[InstanceFeatureVectors]
    ) -> List[List[InstanceFeatureVectors]]:
        """
        If self._maximum_samples_per_batch is specified, then split the batch
        into smaller sub-batches if it exceeds the maximum size.
        Parameters
        ----------
        batch_instances : ``Iterable[InstanceFeatureVectors]``
            A candidate batch.
        excess : ``Deque[InstanceFeatureVectors]``
            Instances that were not sufficient to form an entire batch
            previously. They will be used as part of the first sub-batch. This
            will be populated with instances from the end of batch_instances
            that do not consist of more than self._maximum_samples_per_batch
            samples or self._batch_size instances. It is the caller's
            responsibility to place these in a batch too, which may, of course,
            be done in part with subsequent calls to this method.
            WARNING: Mutated in place!
        """
        if self._maximum_samples_per_batch is None:
            assert not excess
            return [list(batch_instances)]

        (field_name, vector_name), limit = self._maximum_samples_per_batch

        batches: List[List[InstanceFeatureVectors]] = []
        batch: List[InstanceFeatureVectors] = []

        excess.extend(batch_instances)
        while excess:
            instance = excess.popleft()
            padding_length = len(instance[field_name][vector_name])

            proposed_batch_size = len(batch) + 1

            # Adding the current instance would exceed the batch size or sample size.
            if proposed_batch_size >= self._batch_size or padding_length * proposed_batch_size > limit:
                # Output the already existing batch
                batches.append(batch)

                # Put the current instance back, reset state.
                excess.appendleft(instance)
                batch = []
            else:
                batch.append(instance)

        # Keep the current batch as excess.
        excess.extend(batch)

        return batches

    def _biggest_batch_first_and_shuffle(
        self, batches: List[Batch], shuffle: bool, sort_indices: List[List[int]]
    ) -> Tuple[List[Batch], List[List[int]]]:
        move_to_front = self._biggest_batch_first and len(batches) > 1
        if move_to_front:
            # We'll actually pop the last _two_ batches, because the last one might not be full.
            batches.reverse()
            last_batch = batches.pop()
            penultimate_batch = batches.pop()

            sort_indices.reverse()
            last_batch_instances_ids = sort_indices.pop()
            penultimate_batch_instances_ids = sort_indices.pop()

            if shuffle:
                batch_ids = list(range(len(batches)))
                self.shuffle_random.shuffle(batch_ids)  # type: ignore
                batches = [batches[i] for i in batch_ids]
                sort_indices = [sort_indices[i] for i in batch_ids]

            batches.insert(0, penultimate_batch)  # type: ignore
            batches.insert(0, last_batch)  # type: ignore

            sort_indices.insert(0, penultimate_batch_instances_ids)
            sort_indices.insert(0, last_batch_instances_ids)

        elif shuffle:
            # NOTE: if shuffle is false, the instances will still be in a different order
            # because of the bucket sorting.
            batch_ids = list(range(len(batches)))
            self.shuffle_random.shuffle(batch_ids)  # type: ignore
            batches = [batches[i] for i in batch_ids]
            sort_indices = [sort_indices[i] for i in batch_ids]

        return batches, sort_indices
