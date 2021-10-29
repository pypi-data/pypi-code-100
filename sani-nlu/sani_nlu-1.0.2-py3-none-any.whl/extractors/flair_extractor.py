import os
import logging
import copy
import torch
from typing import Any, Dict, List, Optional, Text, Tuple, Type, Callable
from sani_nlu.utils import initializeFolder, download_model, is_duplicated, is_overlap

from rasa.nlu.components import Component
from rasa.nlu.extractors.extractor import EntityExtractor
from rasa.nlu.config import RasaNLUModelConfig
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
from flair.models import SequenceTagger
from flair.data import Sentence

if torch.cuda.is_available():
    torch.cuda.empty_cache()
    
logger = logging.getLogger(__name__)

class FlairExtractor(EntityExtractor):
    name = "FlairExtractor"

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        learner = None,
    ) -> None:
        super(FlairExtractor, self).__init__(component_config)
        self.learner = learner
        initializeFolder()

    def train(
        self,
        training_data: TrainingData,
        config: Optional[RasaNLUModelConfig] = None,
        **kwargs: Any,
    ) -> None:
        """Train this component.

        This is the components chance to train itself provided
        with the training data. The component can rely on
        any context attribute to be present, that gets created
        by a call to :meth:`components.Component.pipeline_init`
        of ANY component and
        on any context attributes created by a call to
        :meth:`components.Component.train`
        of components previous to this one."""
        pass

    def process(self, message: Message, **kwargs: Any) -> None:
        """Process an incoming message."""
        text = message.data.get('text')
        #intent = message.data.get('intent')
        if text:
            sentence = Sentence(text)
            self.learner.predict(sentence)
            result = sentence.to_dict(tag_type='ner')
            entities = []
            for e in result.get("entities"):
                if e.get("labels")[0].value == "LOCATION":
                    entity = {}
                    entity["value"] = e.get("text")
                    entity["start"] = e.get("start_pos")
                    entity["end"] = e.get("end_pos")
                    entity["confidence"] = e.get("labels")[0].score
                    entity["entity"] = "location"
                    entity["extractor"] = "FlairExtractor"

                    entities.append(entity)
                    
            message.set("entities", message.get("entities", []) + entities, add_to_output=True)
        

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        pass

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Text,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any,
    ) -> "Component":
        """Load this component from file."""
        MODEL_PATH = download_model()
        if not os.path.isfile(MODEL_PATH):
            logger.error(f"File not found. Cannot load Flair Extractor model: {MODEL_PATH}")
            return cls(component_config=meta)
        else:
            try:
                learner = SequenceTagger.load(MODEL_PATH)
                logger.debug(f"Load Flair Extractor model successfully ")
                return cls(meta, learner)
            except Exception as ex:
                logger.error(f"Cannot load Flair Extractor model: {MODEL_PATH}: error: {ex}")



