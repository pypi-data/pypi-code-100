import pickle
from os import makedirs
from os.path import exists, join
from typing import TYPE_CHECKING, Any, Dict, Union

import torch
from jsonpickle.handlers import BaseHandler
from transformers import AutoModel, AutoTokenizer, PreTrainedModel

if TYPE_CHECKING:
    from vtorch.common.persistance import FolderPickler, FolderUnpickler

# in the old transformers (2.10) there is PreTrainedTokenizerBase that is inherited by PreTrainedTokenizerFast,
# PreTrainedTokenizer also isinstance(PreTrainedTokenizerFast, PreTrainedTokenizer) is False, so for compatibility:
try:
    from transformers.tokenization_utils import PreTrainedTokenizerFast, PreTrainedTokenizer  # 2.10
except ImportError:
    from transformers import PreTrainedTokenizerFast, PreTrainedTokenizer  # 4.6


def save_pickle(d: Any, file_path: str) -> None:
    with open(file_path, "wb") as fp:
        pickle.dump(d, fp, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(file_path: str) -> Any:
    with open(file_path, "rb") as fp:
        return pickle.load(fp)


class PreTrainedSavingMixin:

    context: Union["FolderPickler", "FolderUnpickler"]
    SAVE_PRETRAINED_FOLDER: str

    def flatten(
        self, obj: Union[PreTrainedTokenizerFast, PreTrainedTokenizer, PreTrainedModel], data: Dict[str, Any]
    ) -> Dict[str, Any]:
        path = join(self.context.folder_path, self.SAVE_PRETRAINED_FOLDER)
        if not exists(path):
            makedirs(path)
        obj.save_pretrained(path)
        return data


class PreTrainedTokenizerHandler(PreTrainedSavingMixin, BaseHandler):

    SAVE_PRETRAINED_FOLDER = "tokenizer"

    def restore(self, obj: Dict[str, Any]) -> PreTrainedTokenizer:
        return AutoTokenizer.from_pretrained(
            join(self.context.folder_path, self.SAVE_PRETRAINED_FOLDER), use_fast=False
        )


class PreTrainedTokenizerFastHandler(PreTrainedTokenizerHandler):

    SAVE_PRETRAINED_FOLDER = "tokenizer"

    def restore(self, obj: Dict[str, Any]) -> PreTrainedTokenizerFast:
        return AutoTokenizer.from_pretrained(
            join(self.context.folder_path, self.SAVE_PRETRAINED_FOLDER), use_fast=True
        )


class PreTrainedModelHandler(PreTrainedSavingMixin, BaseHandler):

    SAVE_PRETRAINED_FOLDER = "model"

    def restore(self, obj: Dict[str, Any]) -> PreTrainedModel:
        return AutoModel.from_pretrained(join(self.context.folder_path, self.SAVE_PRETRAINED_FOLDER))


class TorchSaveHandler(BaseHandler):

    MODULE_FILE = "model.pt"

    def flatten(self, obj: torch.nn.Module, data: Dict[str, Any]) -> Dict[str, Any]:
        if not exists(self.context.folder_path):
            makedirs(self.context.folder_path)
        torch.save(obj, str(join(self.context.folder_path, self.MODULE_FILE)))
        return data

    def restore(self, obj: Dict[str, Any]) -> torch.nn.Module:
        return torch.load(str(join(self.context.folder_path, self.MODULE_FILE)))
