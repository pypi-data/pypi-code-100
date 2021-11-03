from collections import defaultdict
from typing import Any, Dict, List, Optional

import torch

from ..common.utils import argsort
from ..data.iterators.base import DataIterator
from ..data.transform import Vectorizer
from ..nn import utils as nn_util
from ..nn.utils import get_module_device


class ModelPredictor:
    def __init__(self, model: torch.nn.Module, vectorizer: Vectorizer, iterator: DataIterator) -> None:
        self._model = model
        self._model.eval()
        self.vectorizer = vectorizer
        self._iterator = iterator
        self._cuda_device = get_module_device(self._model)

    def predict(
        self, inputs: List[Dict[str, Any]], additional_batch_params: Optional[Dict[str, Any]] = None
    ) -> torch.Tensor:
        instances = [self.vectorizer.vectorize(mention) for mention in inputs]
        data_generator = self._iterator(instances, shuffle=False)
        not_sorted_predictions = []
        serial_indexes: List[int] = []
        with torch.no_grad():
            for batch, ids in data_generator:
                serial_indexes.extend(ids)
                batch = nn_util.move_to_device(batch, self._cuda_device)
                if additional_batch_params is not None:
                    batch.update(additional_batch_params)
                not_sorted_predictions.append(self._make_predictions(batch).cpu())
        not_sorted_predictions_tensor = torch.cat(not_sorted_predictions)
        sorted_predictions = not_sorted_predictions_tensor[argsort(serial_indexes)]
        return sorted_predictions

    def _make_predictions(self, batch: Dict[str, torch.Tensor]) -> torch.Tensor:
        batch_predictions = self._model(**batch)
        return batch_predictions


class MultitaskModelPredictor:
    def __init__(self, model: torch.nn.Module, vectorizer: Vectorizer, iterator: DataIterator) -> None:
        self._model = model
        self._model.eval()
        self.vectorizer = vectorizer
        self._iterator = iterator
        self._cuda_device = get_module_device(self._model)

    def predict(
        self, inputs: List[Dict[str, Any]], additional_batch_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, torch.Tensor]:
        instances = [self.vectorizer.vectorize(mention) for mention in inputs]
        data_generator = self._iterator(instances, shuffle=False)
        not_sorted_predictions: Dict[str, List[torch.Tensor]] = defaultdict(list)
        serial_indexes: List[int] = []
        with torch.no_grad():
            for batch, ids in data_generator:
                serial_indexes.extend(ids)
                batch = nn_util.move_to_device(batch, self._cuda_device)
                if additional_batch_params is not None:
                    batch.update(additional_batch_params)
                for namespace, probabilities in self._make_predictions(batch).items():
                    not_sorted_predictions[namespace].append(probabilities.cpu())

        sorted_predictions = {
            namespace: torch.cat(predictions)[argsort(serial_indexes)]
            for namespace, predictions in not_sorted_predictions.items()
        }

        return sorted_predictions

    def _make_predictions(self, batch: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        batch_predictions: Dict[str, torch.Tensor] = self._model(**batch)
        return batch_predictions
