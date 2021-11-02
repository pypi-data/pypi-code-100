import logging
import os
from itertools import chain
from typing import Iterable, Iterator

import jsonpickle

from vtorch.common import Tqdm
from vtorch.data.entity import InstanceFeatureVectors


class InstanceFeatureProvider(object):
    def __iter__(self) -> Iterator[InstanceFeatureVectors]:
        raise NotImplementedError()


class Chain(InstanceFeatureProvider):
    def __init__(self, providers: Iterable[InstanceFeatureProvider]) -> None:
        self.providers = providers

    def __iter__(self) -> Iterator[InstanceFeatureVectors]:
        return chain.from_iterable(self.providers)


class CachingSampleFeaturesProvider(InstanceFeatureProvider):
    def __init__(self, instance_provider: InstanceFeatureProvider, cache_path: str, rewrite: bool = False) -> None:
        super().__init__()
        self.instance_provider = instance_provider
        self.cache_path = cache_path
        self.rewrite = rewrite

    def __iter__(self) -> Iterator[InstanceFeatureVectors]:
        cache_dir, cache_file = os.path.split(self.cache_path)
        os.makedirs(cache_dir, exist_ok=True)
        if not os.path.exists(cache_file) or self.rewrite:
            logging.info(f"Caching instances to {self.cache_path}")
            with open(self.cache_path, "w") as cache_file_stream:
                for instance in Tqdm.tqdm(self.instance_provider, desc="Caching instances"):
                    cache_file_stream.write(self.serialize_instance(instance))
                    cache_file_stream.write("\n")
                    yield instance
        else:
            with open(self.cache_path, "r") as cache_file_stream:
                for line in cache_file_stream.readlines():
                    yield self.deserialize_instance(line.strip())

    def serialize_instance(self, instance: InstanceFeatureVectors) -> str:
        """
        Serializes an ``InstanceFeatureVectors`` to a string.  We use this for caching the processed instances.
        The default implementation is to use ``jsonpickle``.  If you would like some other format
        for your pre-processed instances, override this method.
        """
        # pylint: disable=no-self-use
        string: str = jsonpickle.dumps(instance)
        return string

    def deserialize_instance(self, string: str) -> InstanceFeatureVectors:
        """
        Deserializes an ``InstanceFeatureVectors`` from a string.  We use this when reading processed instances from a
        cache.
        The default implementation is to use ``jsonpickle``.  If you would like some other format
        for your pre-processed instances, override this method.
        """
        # pylint: disable=no-self-use
        return jsonpickle.loads(string)  # type: ignore
