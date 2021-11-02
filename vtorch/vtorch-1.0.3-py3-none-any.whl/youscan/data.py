import pickle
from pathlib import PosixPath
from typing import Iterator, Union

import pickle5

from vtorch.data.entity import InstanceFeatureVectors
from vtorch.data.provider import InstanceFeatureProvider
from vtorch.data.transform import Vectorizer
from vtorch.youscan.entity import Sample


class YSMentionProvider(object):
    def __iter__(self) -> Iterator[Sample]:
        raise NotImplementedError()


class PickledDatasetReader(YSMentionProvider):
    def __init__(self, path: Union[str, PosixPath]) -> None:
        super().__init__()
        self.path = path

    def __iter__(self) -> Iterator[Sample]:
        try:
            return iter(pickle.load(open(self.path, "rb")))
        except ValueError:
            return iter(pickle5.load(open(self.path, "rb")))


class YSMentionSampleFeaturesProvider(InstanceFeatureProvider):
    def __init__(self, mention_provider: YSMentionProvider, vectorizer: Vectorizer):
        self.mention_provider = mention_provider
        self.vectorizer = vectorizer

    def __iter__(self) -> Iterator[InstanceFeatureVectors]:
        yield from map(self.vectorizer.vectorize, self.mention_provider)
