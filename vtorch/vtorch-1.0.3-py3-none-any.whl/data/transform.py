from collections import Counter, defaultdict
from itertools import chain
from os import makedirs
from os.path import exists, join
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence

import jsonpickle
from jsonpickle.handlers import BaseHandler

from vtorch.common.persistance import Persistent

from ..common import Tqdm
from .entity import FeatureVectors, InstanceFeatureVectors, Vector
from .values import StringSequenceExtractor


class FeatureExtractor(Persistent):
    def extract_features(self, instance: Mapping[str, Any]) -> Optional[FeatureVectors]:
        raise NotImplementedError()

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "FeatureExtractor":
        raise NotImplementedError()


class Vectorizer(Persistent):
    def __init__(self, namespace_feature_extractors: Mapping[str, FeatureExtractor]):
        self.namespace_feature_extractors = namespace_feature_extractors

    def vectorize(self, instance: Mapping[str, Any]) -> InstanceFeatureVectors:
        feature_vectors: Dict[str, Dict[str, Vector]] = defaultdict(dict)
        for namespace, feature_extractor in self.namespace_feature_extractors.items():
            features = feature_extractor.extract_features(instance=instance)
            if features is not None:
                feature_vectors[namespace].update(features)
        return dict(feature_vectors)

    @classmethod
    def from_data(
        cls,
        namespace_feature_extractors: MutableMapping[str, FeatureExtractor],
        instances: Sequence[Mapping[str, Any]],
    ) -> "Vectorizer":
        for namespace, feature_extractors in dict(namespace_feature_extractors).items():
            namespace_feature_extractors[namespace] = feature_extractors.fit(instances=instances)
        return cls(namespace_feature_extractors=namespace_feature_extractors)


@jsonpickle.handlers.register(Vectorizer, base=True)
class VectorizerHandler(BaseHandler):
    def flatten(self, obj: Vectorizer, data: Dict[str, Any]) -> Dict[str, Any]:
        for namespace, extractor in obj.namespace_feature_extractors.items():
            extractor_path = join(self.context.folder_path, namespace)
            if not exists(extractor_path):
                makedirs(extractor_path)
            extractor.save(extractor_path)
            data[namespace] = f"{namespace}/"
        return data

    def restore(self, obj: Dict[str, Any]) -> Vectorizer:
        namespace_extractors = dict()
        for namespace, extractor_path in obj.items():
            if namespace != "py/object":
                namespace_extractors[namespace] = FeatureExtractor.load(join(self.context.folder_path, extractor_path))
        return Vectorizer(namespace_feature_extractors=namespace_extractors)


class VocabularyIndexer(FeatureExtractor):
    def __init__(
        self,
        string_sequence_extractor: StringSequenceExtractor,
        oov_token: str = "[UNKNOWN]",
        pad_token: str = "[PAD]",
        min_count: Optional[int] = None,
        max_vocab_size: Optional[int] = None,
        elements_to_add: Optional[Sequence[Any]] = None,
    ) -> None:
        self.mapping = dict()
        self.string_sequence_extractor = string_sequence_extractor
        self.oov_token = oov_token
        self.pad_token = pad_token
        self.oov_index = 1
        self.pad_index = 0
        self.mapping[self.oov_token] = self.oov_index
        self.mapping[self.pad_token] = self.pad_index
        self.min_count = min_count
        self.max_vocab_size = max_vocab_size
        self.elements_to_add = elements_to_add
        super().__init__()

    def extract_features(self, instance: Mapping[str, Any]) -> FeatureVectors:
        return {
            "token_ids": Vector(
                (
                    self.mapping.get(token, self.mapping[self.oov_token])
                    for token in self.string_sequence_extractor.extract(instance)
                ),
                self.pad_index,
            )
        }

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "VocabularyIndexer":
        feature_counter = Counter(
            chain.from_iterable(
                self.string_sequence_extractor.extract(instance)
                for instance in Tqdm.tqdm(instances, desc="Fitting VocabularyIndexer")
            )
        )
        sorted_features = iter(feature_counter.most_common(n=self.max_vocab_size))
        if self.min_count is not None:
            min_count = self.min_count
            sorted_features = filter(lambda t: t[1] < min_count, sorted_features)

        i = len(self.mapping)
        for i, (item, value) in enumerate(sorted_features, start=i):
            self.mapping[item] = i
        if self.elements_to_add is not None:
            for i, item in enumerate(self.elements_to_add, start=i):
                self.mapping[item] = i
        return self


class AbstractLabelIndexer(FeatureExtractor):
    def __init__(self, label_namespace: str = "labels", label_field: str = "label_ids") -> None:
        """
        Abstract class for converting the label from instance into FeatureVectors object
        Parameters
        ----------
        label_namespace: str (default = "labels") the key to retrieve the label from the instance
        label_field: str (default = "label_ids") by this key label's Vector will be written to the FeatureVectors.
            It's the second level key to retrieve the labels tensor from batch
        """
        super().__init__()
        self._mapping: Dict[str, int] = dict()
        self._label_namespace = label_namespace  # TODO: rename "namespace" into "key"?
        self._label_field = label_field

    def extract_features(self, instance: Mapping[str, Any]) -> Optional[FeatureVectors]:
        raise NotImplementedError()

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "AbstractLabelIndexer":
        raise NotImplementedError()

    @property
    def vocab(self) -> List[str]:
        return sorted(self._mapping, key=self._mapping.get)  # type: ignore


class OneHotLabelIndexer(AbstractLabelIndexer):  # TODO: will be incompatible with saved items
    def extract_features(self, instance: Mapping[str, Any]) -> Optional[FeatureVectors]:
        labels = [0.0 for _ in self._mapping]
        if self._label_namespace in instance:
            for label_name in instance[self._label_namespace]:
                labels[self._mapping[label_name]] = 1.0
            return {self._label_field: Vector(labels, None)}
        return None

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "OneHotLabelIndexer":
        for instance in Tqdm.tqdm(instances, desc="Fitting LabelIndexer"):
            for label_name in instance.get(self._label_namespace, []):
                if label_name not in self._mapping:
                    self._mapping[label_name] = len(self._mapping)
        return self


class MultiClassLabelIndexer(AbstractLabelIndexer):
    def extract_features(self, instance: Mapping[str, Any]) -> Optional[FeatureVectors]:
        if self._label_namespace in instance:
            label_name = instance[self._label_namespace]
            label_index = self._mapping[label_name]
            label = [label_index]
            return {self._label_field: Vector(label, None)}
        return None

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "MultiClassLabelIndexer":
        for instance in Tqdm.tqdm(instances, desc="Fitting LabelIndexer"):
            label_name = instance[self._label_namespace]
            if label_name not in self._mapping:
                self._mapping[label_name] = len(self._mapping)
        return self


class SamplingRateFeatureExtractor(FeatureExtractor):
    def __init__(self, sampling_rate_namespace: str = "sampling_rate", sampling_rate_field: str = "sampling_rate"):
        """
        This class is used to extract the sampling rate from the instances and convert in into the FeatureVectors
            object
        Parameters
        ----------
        sampling_rate_namespace: str (default = "sampling_rate") key to retrieve the sampling rate from instance
        sampling_rate_field: str (default = "sampling_rate") by this key sampling_rate's Vector (with length of 1)
            will be written to the FeatureVectors. It could be passed into the `sampling_rate_field` argument of
            `BucketIterator`.
        """
        self._sampling_rate_namespace = sampling_rate_namespace
        self._sampling_rate_field = sampling_rate_field

    def extract_features(self, instance: Mapping[str, Any]) -> Optional[FeatureVectors]:
        if self._sampling_rate_namespace in instance:
            sampling_rate = instance[self._sampling_rate_namespace]
            sampling_rate_vector = [sampling_rate]
            return {self._sampling_rate_field: Vector(sampling_rate_vector, None)}
        return None

    def fit(self, instances: Sequence[Mapping[str, Any]]) -> "SamplingRateFeatureExtractor":
        return self
