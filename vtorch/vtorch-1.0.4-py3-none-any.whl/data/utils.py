import os
from pathlib import Path
from typing import Any, Dict, Mapping

import jsonpickle
from jsonpickle.handlers import BaseHandler

from vtorch.common.persistance import Persistent
from vtorch.data.transform import Vectorizer


class MultipleVectorizerContainer(Persistent):
    def __init__(self, namespace_to_vectorizer: Mapping[str, Vectorizer]):
        super(MultipleVectorizerContainer, self).__init__()
        self.namespace_to_vectorizer = namespace_to_vectorizer


@jsonpickle.handlers.register(MultipleVectorizerContainer, base=True)
class MultipleVectorizerContainerHandler(BaseHandler):
    def flatten(self, obj: MultipleVectorizerContainer, data: Dict[str, Any]) -> Dict[str, Any]:
        for namespace, vectorizer in obj.namespace_to_vectorizer.items():
            namespace_directory = str(os.path.join(self.context.folder_path, namespace))
            os.makedirs(namespace_directory, exist_ok=True)
            vectorizer.save(namespace_directory)
        return data

    def restore(self, obj: Dict[str, Any]) -> MultipleVectorizerContainer:
        namespace_to_vectorizer = {}
        for path in Path(self.context.folder_path).glob("*"):
            if path.is_dir():
                namespace_to_vectorizer[path.name] = Vectorizer.load(str(path))
        return MultipleVectorizerContainer(namespace_to_vectorizer)
