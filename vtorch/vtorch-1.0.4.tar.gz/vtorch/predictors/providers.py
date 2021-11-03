from abc import ABC
from pathlib import Path
from typing import Dict

from vtorch.data.iterators import DataIterator
from vtorch.data.transform import OneHotLabelIndexer, Vectorizer
from vtorch.data.utils import MultipleVectorizerContainer
from vtorch.models.classification import OldClassificationModel
from vtorch.models.multitask_classification import AutoModelForIndexLossCounting
from vtorch.nn.utils import move_to_device
from vtorch.postprocessing.default import PredictionPostprocessor
from vtorch.postprocessing.multilabel import MultilabelPostprocessorWithLogits
from vtorch.predictors import ModelPredictor
from vtorch.predictors.multiple_language_predictor import (
    MultipleLanguageMultilabelPredictor,
    MultipleLanguageMultitaskMultilabelPredictor,
)
from vtorch.predictors.predictor import MultitaskModelPredictor


class IPredictorProvider(ABC):
    def get(self) -> ModelPredictor:
        raise NotImplementedError()


class IMultitaskPredictorProvider(ABC):
    def get(self) -> MultitaskModelPredictor:
        raise NotImplementedError()


class MultipleLanguageMultilabelPredictorProvider(IPredictorProvider):
    def __init__(
        self,
        serialization_dir: str,
        iterator: DataIterator,
        language_threshold: Dict[str, float],
        text_namespace: str = "text",
        label_namespace: str = "labels",
        cuda_device: int = -1,
    ):
        self.serialization_dir = Path(serialization_dir)
        self.iterator = iterator
        self.text_namespace = text_namespace
        self.label_namespace = label_namespace
        self.cuda_device = cuda_device
        self.language_threshold = language_threshold

    def get(self) -> MultipleLanguageMultilabelPredictor:

        model = OldClassificationModel.load(str(self.serialization_dir / "model"))
        vectorizers = Vectorizer.load(str(self.serialization_dir / "vectorizer"))

        label_indexer: OneHotLabelIndexer = vectorizers.namespace_feature_extractors[self.label_namespace]

        language_post_processors: Dict[str, PredictionPostprocessor] = {
            language: MultilabelPostprocessorWithLogits(
                {label_name: i for i, label_name in enumerate(label_indexer.vocab)}, default_threshold=threshold
            )
            for language, threshold in self.language_threshold.items()
        }

        return MultipleLanguageMultilabelPredictor(
            model=move_to_device(model, self.cuda_device),
            label_indexer=label_indexer,
            iterator=self.iterator,
            language_post_processors=language_post_processors,
            vectorizer=vectorizers,
        )


class MultipleLanguageMultitaskMultilabelPredictorProvider(IMultitaskPredictorProvider):
    def __init__(
        self,
        serialization_dir: str,
        iterator: DataIterator,
        language_threshold: Dict[str, float],
        text_namespace: str = "text",
        label_namespace: str = "labels",
        cuda_device: int = -1,
    ):
        self.serialization_dir = Path(serialization_dir)
        self.iterator = iterator
        self.text_namespace = text_namespace
        self.label_namespace = label_namespace
        self.cuda_device = cuda_device
        self.language_threshold = language_threshold

    def get(self) -> MultipleLanguageMultitaskMultilabelPredictor:

        model = AutoModelForIndexLossCounting.load(str(self.serialization_dir / "model"))
        vectorizers = MultipleVectorizerContainer.load(str(self.serialization_dir / "vectorizer"))

        namespace_to_label_vocab = {
            namespace: vectorizer.namespace_feature_extractors[self.label_namespace].vocab
            for namespace, vectorizer in vectorizers.namespace_to_vectorizer.items()
        }

        label_indexer = {
            namespace: vectorizer.namespace_feature_extractors[self.label_namespace]
            for namespace, vectorizer in vectorizers.namespace_to_vectorizer.items()
        }

        vectorizer = vectorizers.namespace_to_vectorizer[next(iter(vectorizers.namespace_to_vectorizer))]

        language_post_processors: Dict[str, Dict[str, PredictionPostprocessor]] = {
            namespace: {
                language: MultilabelPostprocessorWithLogits(
                    label_to_index={label_name: i for i, label_name in enumerate(vocab)}, default_threshold=threshold
                )
                for language, threshold in self.language_threshold.items()
            }
            for namespace, vocab in namespace_to_label_vocab.items()
        }

        return MultipleLanguageMultitaskMultilabelPredictor(
            model=move_to_device(model, self.cuda_device),
            label_indexer=label_indexer,
            iterator=self.iterator,
            language_post_processors=language_post_processors,
            vectorizer=vectorizer,
        )
