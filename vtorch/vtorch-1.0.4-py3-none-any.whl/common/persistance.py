import os
from typing import Any

import jsonpickle
import torch
from jsonpickle import Pickler, Unpickler


class FolderPickler(Pickler):
    def __init__(self, folder_path: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.folder_path = folder_path


class FolderUnpickler(Unpickler):
    def __init__(self, folder_path: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.folder_path = folder_path


class Persistent:

    PICKLE_FILE_NAME = "object.json"

    def save(self, save_directory: str) -> str:
        file_path = os.path.join(save_directory, self.PICKLE_FILE_NAME)
        with open(file_path, "w") as fp:
            fp.write(jsonpickle.encode(self, indent=2, context=FolderPickler(save_directory)))
        return save_directory

    @classmethod
    def load(cls, save_directory: str) -> Any:
        file_path = os.path.join(save_directory, cls.PICKLE_FILE_NAME)
        with open(file_path, "r") as fp:
            return jsonpickle.decode(fp.read(), context=FolderUnpickler(save_directory))


# to register automatically, when Persistent is somewhere used
def jsonpickle_register() -> None:
    from vtorch.common.loading import (
        PreTrainedTokenizer,
        PreTrainedTokenizerFast,
        PreTrainedTokenizerHandler,
        PreTrainedTokenizerFastHandler,
        PreTrainedModel,
        PreTrainedModelHandler,
        TorchSaveHandler,
    )

    for cls, handler in [
        (PreTrainedTokenizerFast, PreTrainedTokenizerFastHandler),
        (PreTrainedTokenizer, PreTrainedTokenizerHandler),
        (PreTrainedModel, PreTrainedModelHandler),
        (torch.nn.Module, TorchSaveHandler),
    ]:
        jsonpickle.handlers.registry.register(cls, handler, base=True)


jsonpickle_register()
