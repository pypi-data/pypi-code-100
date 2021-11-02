from copy import deepcopy
from itertools import chain
from typing import Any, Callable, Dict, Iterable, List, Optional

import torch
from torch import nn

from vtorch.data.iterators import DataIterator
from vtorch.data.transform import AbstractLabelIndexer, Vectorizer
from vtorch.postprocessing.default import PredictionPostprocessor
from vtorch.predictors import ModelPredictor
from vtorch.predictors.predictor import MultitaskModelPredictor

LANGUAGE = "other"  # if language is not provided, we will return empty list


class MultipleLanguagePredictor(ModelPredictor):
    def __init__(
        self,
        model: torch.nn.Module,
        vectorizer: Vectorizer,
        label_indexer: AbstractLabelIndexer,
        iterator: DataIterator,
        language_post_processors: Dict[str, PredictionPostprocessor],
        missing_language: str = LANGUAGE,
    ) -> None:
        super().__init__(model=model, vectorizer=vectorizer, iterator=iterator)
        self.label_indexer = label_indexer
        self._missing_language = missing_language
        self._language_post_processors = language_post_processors
        self._supported_languages = set(processors for processors in self._language_post_processors.keys())

    def predict_labels(self, inputs: List[Dict[str, Any]]) -> List[Any]:
        supported_indices = [i for i, mention in enumerate(inputs) if self._mention_supported(mention)]
        supported_mentions = [inputs[i] for i in supported_indices]
        predictions = [deepcopy(self.default_value) for _ in inputs]
        if len(supported_mentions) > 0:
            prediction_probabilities = self.predict(supported_mentions)

            supported_mentions_languages = [
                mention.get("language", mention.get("lang", self._missing_language)) for mention in supported_mentions
            ]

            prediction_labels = self._post_process_predictions_by_language(
                prediction_probabilities, supported_mentions_languages
            )

            for i, prediction in zip(supported_indices, prediction_labels):
                predictions[i] = prediction
        return predictions

    def _make_predictions(self, batch: Dict[str, torch.Tensor]) -> torch.Tensor:
        return self._model(**batch)[0]

    def languages(self) -> Iterable[str]:
        return self._supported_languages

    def _mention_supported(self, mention: Dict[str, Any]) -> bool:
        return mention.get("language", mention.get("lang", self._missing_language)) in self._supported_languages

    def _post_process_predictions_by_language(self, raw_predictions: torch.Tensor, languages: List[str]) -> List[Any]:
        raise NotImplementedError()

    @property
    def labels(self) -> List[str]:
        return self.label_indexer.vocab

    @property
    def default_value(self) -> Any:
        raise NotImplementedError()


class MultipleLanguageMultilabelPredictor(MultipleLanguagePredictor):
    def predict_labels(self, inputs: List[Dict[str, Any]]) -> List[List[str]]:
        return super(MultipleLanguageMultilabelPredictor, self).predict_labels(inputs=inputs)

    def _post_process_predictions_by_language(
        self, raw_predictions: torch.Tensor, languages: List[str]
    ) -> List[List[str]]:
        predictions = torch.zeros_like(raw_predictions)
        for post_processor_language, post_processor in self._language_post_processors.items():
            serial_indices = [
                serial_index for serial_index, language in enumerate(languages) if language == post_processor_language
            ]
            if len(serial_indices) == 0:
                continue
            predictions[serial_indices] = post_processor.postprocess(raw_predictions[serial_indices])

        labels_predictions: List[List[str]] = [[] for _ in predictions]
        for mention_serial_number, label_index in predictions.nonzero().tolist():  # type: ignore
            labels_predictions[mention_serial_number].append(self.labels[label_index])
        return labels_predictions

    @property
    def default_value(self) -> List[str]:
        return []


class MultipleLanguageMultitaskPredictor(MultitaskModelPredictor):
    def __init__(
        self,
        model: nn.Module,
        vectorizer: Vectorizer,
        label_indexer: Dict[str, AbstractLabelIndexer],
        iterator: DataIterator,
        language_post_processors: Dict[str, Dict[str, PredictionPostprocessor]],  # firstly namespace, then language
        missing_language: str = LANGUAGE,
    ) -> None:

        super().__init__(model=model, vectorizer=vectorizer, iterator=iterator)
        self.label_indexer = label_indexer
        self._torchscript_inference: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None
        self._language_post_processors = language_post_processors
        self._missing_language = missing_language
        self._supported_languages = set(
            chain.from_iterable(processors.keys() for processors in self._language_post_processors.values())
        )

    def predict_labels(self, inputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        supported_indices = [i for i, mention in enumerate(inputs) if self._mention_supported(mention)]
        supported_mentions = [inputs[i] for i in supported_indices]
        predictions = [deepcopy(self.default_value) for _ in inputs]
        if len(supported_mentions) > 0:
            prediction_probabilities = self.predict(supported_mentions)

            supported_mentions_languages = [
                mention.get("language", mention.get("lang", self._missing_language)) for mention in supported_mentions
            ]

            namespace_prediction_labels = self._post_process_predictions_by_language(
                prediction_probabilities, supported_mentions_languages
            )
            for namespace, prediction_labels in namespace_prediction_labels.items():
                for i, prediction in zip(supported_indices, prediction_labels):
                    predictions[i][namespace] = prediction
        return predictions

    def _make_predictions(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        preds: Dict[str, torch.Tensor] = self._model(namespaces=self._language_post_processors.keys(), **batch)[0]
        return preds

    def _mention_supported(self, mention: Dict[str, Any]) -> bool:
        return mention.get("language", mention.get("lang", self._missing_language)) in self._supported_languages

    def _post_process_predictions_by_language(
        self, raw_predictions: Dict[str, torch.Tensor], languages: List[str]
    ) -> Dict[str, List[Any]]:
        raise NotImplementedError()

    @property
    def default_value(self) -> Dict[str, Any]:
        raise NotImplementedError()


class MultipleLanguageMultitaskMultilabelPredictor(MultipleLanguageMultitaskPredictor):
    def predict_labels(self, inputs: List[Dict[str, Any]]) -> List[Dict[str, List[str]]]:
        return super(MultipleLanguageMultitaskMultilabelPredictor, self).predict_labels(inputs=inputs)

    def _post_process_predictions_by_language(
        self, raw_predictions: Dict[str, torch.Tensor], languages: List[str]
    ) -> Dict[str, List[List[str]]]:
        post_processed_predictions = {}
        for namespace, predictions in raw_predictions.items():
            for post_processor_language, post_processor in self._language_post_processors[namespace].items():
                serial_indices = [
                    serial_index
                    for serial_index, language in enumerate(languages)
                    if language == post_processor_language
                ]
                if len(serial_indices) == 0:
                    continue
                predictions[serial_indices] = post_processor.postprocess(predictions[serial_indices])

            labels_predictions: List[List[str]] = [[] for _ in predictions]
            for mention_serial_number, label_index in predictions.nonzero().tolist():  # type: ignore
                labels_predictions[mention_serial_number].append(self.label_indexer[namespace].vocab[label_index])
            post_processed_predictions[namespace] = labels_predictions
        return post_processed_predictions

    @property
    def default_value(self) -> Dict[str, List[str]]:
        return {}
