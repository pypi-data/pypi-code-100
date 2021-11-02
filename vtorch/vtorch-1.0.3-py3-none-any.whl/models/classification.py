import inspect
import warnings
from typing import Callable, Dict, Optional, Tuple, Union

import torch
from torch import nn
from transformers import DistilBertModel, PreTrainedModel, RobertaModel

from vtorch.common.checks import ConfigurationError
from vtorch.models.model import IModel


class ClassifierWithPreTrainedModel(IModel):
    def __init__(self, base_model: PreTrainedModel):
        super().__init__()
        self._base_model = base_model
        self.dropout = nn.Dropout(self._base_model.config.head_dropout)  # type: ignore
        self.classifier = nn.Linear(
            self._base_model.config.hidden_size,  # type: ignore
            self._base_model.config.num_labels,
        )

    def resize_token_embeddings(self, new_num_tokens: Optional[int] = None) -> None:
        self._base_model.resize_token_embeddings(new_num_tokens)

    def get_input_embeddings(self) -> Union[nn.Embedding, nn.Module]:
        return self._base_model.get_input_embeddings()

    def _get_base_model_output(self, text: Dict[str, torch.Tensor]) -> torch.Tensor:
        forward_kwargs = self._form_input(text)
        model_outputs = self._base_model(**forward_kwargs)
        hidden_states = model_outputs[0][:, 0] if len(model_outputs) == 1 else model_outputs[1]
        return hidden_states

    def _form_input(self, text: Dict[str, torch.Tensor]) -> Dict[str, Optional[torch.Tensor]]:
        if isinstance(self._base_model, (RobertaModel, DistilBertModel)):
            text.pop("token_type_ids", None)  # roberta doesn't support token_type_ids

        forward_kwargs = {"input_ids": text["input_ids"], "attention_mask": text.get("attention_mask")}
        if "token_type_ids" in inspect.signature(self._base_model.forward).parameters.keys():
            forward_kwargs["token_type_ids"] = text.get("token_type_ids")
        return forward_kwargs

    def _get_logits(self, text: Dict[str, torch.Tensor]) -> torch.Tensor:
        hidden_states = self._get_base_model_output(text=text)
        logits = self.classifier(self.dropout(hidden_states))
        return logits


class AutoModelForSequenceClassificationWithCustomLoss(ClassifierWithPreTrainedModel):
    def __init__(
        self,
        base_model: PreTrainedModel,
        loss_function: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None,
    ):
        super().__init__(base_model)
        self.loss_function = loss_function
        if loss_function is None:
            warnings.warn(
                "'loss_function' argument was not provided. "
                "If you will train this model set it via 'set_loss_function(loss_function)'"
            )

    def set_loss_function(self, loss_function: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]]) -> None:
        self.loss_function = loss_function

    def forward(
        self, text: Dict[str, torch.Tensor], labels: Optional[Dict[str, torch.Tensor]] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:

        logits = self._get_logits(text)

        loss = None
        if labels is not None:
            if self.loss_function is None:
                raise ConfigurationError(
                    "The loss function was not set during the initialization. "
                    "You must define it to use model for training"
                )
            loss = self.loss_function(logits, labels["label_ids"])

        return logits, loss


class OldClassificationModel(ClassifierWithPreTrainedModel):
    def __init__(self, base_model: PreTrainedModel):
        super(IModel, self).__init__()  # as the attribute naming differs, we can't initialize first base class

        self._transformer = base_model
        self._head_dropout = nn.Dropout(self._transformer.config.head_dropout)  # type: ignore
        self._classification_head = nn.Linear(
            self._transformer.config.hidden_size,  # type: ignore
            self._transformer.config.num_labels,
        )
        self._activation = nn.Sigmoid()  # will not be used for now

    def forward(
        self, text: Dict[str, torch.Tensor], labels: Optional[Dict[str, torch.Tensor]] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:

        forward_kwargs = self._form_input(text)
        hidden_states = self._transformer(**forward_kwargs)[0][:, 0]
        logits = self._classification_head(self._head_dropout(hidden_states))

        loss = None  # only for inference

        return logits, loss

    def resize_token_embeddings(self, new_num_tokens: Optional[int] = None) -> None:
        self._transformer.resize_token_embeddings(new_num_tokens)

    def get_input_embeddings(self) -> Union[nn.Embedding, nn.Module]:
        return self._transformer.get_input_embeddings()

    def _form_input(self, text: Dict[str, torch.Tensor]) -> Dict[str, Optional[torch.Tensor]]:
        if isinstance(self._transformer, (RobertaModel, DistilBertModel)):
            text.pop("token_type_ids", None)  # roberta doesn't support token_type_ids

        forward_kwargs = {"input_ids": text["input_ids"], "attention_mask": text.get("attention_mask")}
        if "token_type_ids" in inspect.signature(self._transformer.forward).parameters.keys():
            forward_kwargs["token_type_ids"] = text.get("token_type_ids")
        return forward_kwargs
