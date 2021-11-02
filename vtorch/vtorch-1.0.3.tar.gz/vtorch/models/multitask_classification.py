import json
import os
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import jsonpickle
import torch
from torch import nn
from transformers import WEIGHTS_NAME, AutoConfig, AutoModel, PreTrainedModel, PreTrainedTokenizer
from transformers.tokenization_utils import PreTrainedTokenizerFast

from vtorch.common.checks import ConfigurationError
from vtorch.common.loading import PreTrainedModelHandler
from vtorch.models.classification import ClassifierWithPreTrainedModel


class AutoModelForIndexLossCounting(ClassifierWithPreTrainedModel):
    def __init__(
        self,
        base_model: PreTrainedModel,
        namespace_to_outputs: Dict[str, torch.Tensor],
        loss_function: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]] = None,
    ):
        super().__init__(base_model=base_model)

        self._namespace_to_outputs = namespace_to_outputs
        self._namespace_to_outputs_moved_to_device = False
        self.loss_function = loss_function
        if loss_function is None:
            warnings.warn(
                "'loss_function' argument was not provided. "
                "If you will train this model set it via 'set_loss_function(loss_function)'"
            )

    def set_loss_function(self, loss_function: Optional[Callable[[torch.Tensor, torch.Tensor], torch.Tensor]]) -> None:
        self.loss_function = loss_function

    def namespace_to_outputs(self) -> Dict[str, torch.Tensor]:
        # not property because of https://github.com/pytorch/pytorch/issues/33934
        if self._namespace_to_outputs_moved_to_device:
            return self._namespace_to_outputs
        self._namespace_to_outputs = {
            namespace: ids.to(self._base_model.device) for namespace, ids in self._namespace_to_outputs.items()
        }
        self._namespace_to_outputs_moved_to_device = True
        return self._namespace_to_outputs

    def forward(
        self,
        text: Dict[str, torch.Tensor],
        namespaces: Optional[List[str]] = None,
        labels: Optional[Dict[str, torch.Tensor]] = None,
    ) -> Tuple[Union[torch.Tensor, Dict[str, torch.Tensor]], Optional[torch.Tensor]]:

        logits = self._get_logits(text)

        loss = None
        if labels is not None and namespaces is not None:
            if len(namespaces) > 1:
                raise ValueError("Just one namespace supported during training")
            if self.loss_function is None:
                raise ConfigurationError(
                    "The loss function was not set during the initialization. "
                    "You must define it to use model for training"
                )
            loss = self.loss_function(
                logits[:, self.namespace_to_outputs()[namespaces[0]]], labels["label_ids"].float()
            )
        else:
            # if not provided, use all namespaces
            if namespaces is None:
                namespaces = list(self._namespace_to_outputs.keys())
            logits = {
                namespace: logits[:, namespace_ids]
                for namespace, namespace_ids in self.namespace_to_outputs().items()
                if namespace in namespaces
            }

        return logits, loss


@jsonpickle.handlers.register(AutoModelForIndexLossCounting, base=True)
class AutoModelForIndexLossCountingHandler(PreTrainedModelHandler):
    def restore(self, obj: Dict[str, Any]) -> AutoModelForIndexLossCounting:
        model_path = os.path.join(self.context.folder_path, self.SAVE_PRETRAINED_FOLDER)
        config = AutoConfig.from_pretrained(model_path)
        base_model = AutoModel.from_config(config=config)
        namespace_to_outputs_path = os.path.join(model_path, "namespace_to_outputs.json")
        with open(namespace_to_outputs_path, "r") as fp:
            namespace_to_outputs = json.load(fp)
        namespace_to_outputs = {namespace: torch.tensor(ids) for namespace, ids in namespace_to_outputs.items()}
        model = AutoModelForIndexLossCounting(base_model=base_model, namespace_to_outputs=namespace_to_outputs)
        model.load_state_dict(torch.load(os.path.join(model_path, WEIGHTS_NAME), map_location=torch.device("cpu")))
        return model

    def flatten(
        self, obj: Union[PreTrainedTokenizerFast, PreTrainedTokenizer, PreTrainedModel], data: Dict[str, Any]
    ) -> Dict[str, Any]:
        data = super(AutoModelForIndexLossCountingHandler, self).flatten(obj, data)
        path = os.path.join(self.context.folder_path, self.SAVE_PRETRAINED_FOLDER, "namespace_to_outputs.json")
        namespace_to_outputs = {
            namespace: ids.detach().cpu().tolist() for namespace, ids in obj.namespace_to_outputs.items()
        }
        with open(path, "w") as fp:
            json.dump(namespace_to_outputs, fp)
        return data


class ModelOutputWrapper(nn.Module):
    def __init__(self, logit_ids: torch.Tensor, model: nn.Module):
        super(ModelOutputWrapper, self).__init__()
        self.logit_ids = logit_ids
        self.model = model

    def forward(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Tuple[Optional[torch.Tensor], ...]:
        model_output = list(self.model(*args, **kwargs))
        model_output[0] = model_output[0][:, self.logit_ids]  # first element is logits, we take just required ids
        return tuple(model_output)
