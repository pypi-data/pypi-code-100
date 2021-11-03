import logging
from collections import defaultdict
from typing import DefaultDict, Dict, Iterable, Iterator, List

import torch

from vtorch.common.utils import ensure_list
from vtorch.data.entity import InstanceFeatureVectors, Vector

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Batch(Iterable[InstanceFeatureVectors]):
    """
    A batch of Instances. In addition to containing the instances themselves,
    it contains helper functions for converting the instances into tensors.
    """

    def __init__(self, instances: Iterable[InstanceFeatureVectors]) -> None:
        """
        A Batch just takes an iterable of instances in its constructor and hangs onto them
        in a list.
        """
        super().__init__()
        self.instances: List[InstanceFeatureVectors] = ensure_list(instances)

    def get_padding_lengths(self) -> Dict[str, Dict[str, int]]:
        padding_lengths: Dict[str, Dict[str, int]] = defaultdict(dict)
        for instance in self.instances:
            for field_name, feature_vectors in instance.items():
                for feature_name, vector in feature_vectors.items():
                    padding_lengths[field_name][feature_name] = max(
                        padding_lengths[field_name].get(feature_name, 0), len(vector)
                    )
        return padding_lengths

    def as_tensor_dict(self, verbose: bool = False) -> Dict[str, Dict[str, torch.Tensor]]:
        # This complex return type is actually predefined elsewhere as a DataArray,
        # but we can't use it because mypy doesn't like it.
        """
        This method converts this ``Batch`` into a set of pytorch Tensors that can be passed
        through a model.  In order for the tensors to be valid tensors, all ``Instances`` in this
        batch need to be padded to the same lengths wherever padding is necessary, so we do that
        first, then we combine all of the tensors for each field in each instance into a set of
        batched tensors for each field.
        Parameters
        ----------
        batch_first : ``bool`` (default = ``False``)
            For many pytorch implementation batch_first=``False`` is default setting.
            Change it if you need.
        verbose : ``bool``, optional (default=``False``)
            Should we output logging information when we're doing this padding?  If the batch is
            large, this is nice to have, because padding a large batch could take a long time.
            But if you're doing this inside of a instances generator, having all of this output per
            batch is a bit obnoxious (and really slow).
        Returns
        -------
        tensors : ``Dict[str, DataArray]``
            A dictionary of tensors, keyed by field name, suitable for passing as input to a model.
            This is a `batch` of instances, so, e.g., if the instances have a "question" field and
            an "answer" field, the "question" fields for all of the instances will be grouped
            together into a single tensor, and the "answer" fields for all instances will be
            similarly grouped in a parallel set of tensors, for batched computation. Additionally,
            for complex ``Fields``, the value of the dictionary key is not necessarily a single
            tensor.  For example, with the ``TextTokensField``, the output is a dictionary mapping
            ``TokenIndexer`` keys to tensors. The number of elements in this sub-dictionary
            therefore corresponds to the number of ``TokenIndexers`` used to index the
            ``TextTokensField``.  Each ``Field`` class is responsible for batching its own output.
        """
        padding_lengths = self.get_padding_lengths()
        # First we need to decide _how much_ to pad.  To do that, we find the max length for all
        # relevant padding decisions from the instances themselves.  Then we check whether we were
        # given a max length for a particular field and padding key.  If we were, we use that
        # instead of the instance-based one.
        if verbose:
            logger.info("Padding batch of size %d to lengths %s", len(self.instances), str(padding_lengths))
            logger.info("Getting max lengths from instances")
        if verbose:
            logger.info("InstanceFeatureVectors max lengths: %s", str(padding_lengths))

        # Now we actually pad the instances to tensors.
        field_tensors: Dict[str, Dict[str, List[Vector]]] = defaultdict(lambda: defaultdict(list))
        for instance in self.instances:
            for field_name, feature_vectors in instance.items():
                for feature_name, vector in feature_vectors.items():
                    field_tensors[field_name][feature_name].append(
                        vector.padded(padding_lengths[field_name][feature_name])
                    )

        final_fields: DefaultDict[str, Dict[str, torch.Tensor]] = defaultdict(dict)
        for field_name, field_tensor_mapping in field_tensors.items():
            for feature_name, vectors in field_tensor_mapping.items():
                feature_tensor = torch.tensor(vectors)
                # as we wrap scalars into the array with length == 1 it will add redundant dimension
                if len(feature_tensor.shape) == 2 and feature_tensor.shape[1] == 1:
                    feature_tensor = feature_tensor.reshape(-1)
                final_fields[field_name][feature_name] = feature_tensor
        return final_fields

    def __iter__(self) -> Iterator[InstanceFeatureVectors]:
        return iter(self.instances)
