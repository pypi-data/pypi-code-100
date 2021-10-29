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
from sani_nlu.constants import THRESHOLD
    
logger = logging.getLogger(__name__)

class OverlapExtractor(EntityExtractor):
    name = "OverlapExtractor"

    def __init__(
        self,
        component_config: Optional[Dict[Text, Any]] = None,
        learner = None,
    ) -> None:
        super(OverlapExtractor, self).__init__(component_config)

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
            old_entities = message.get("entities", [])
            regex_extractor = [x for x in old_entities if x.get("extractor") == "RegexEntityExtractor"]
            flair_extractor = [x for x in old_entities if x.get("extractor") == "FlairExtractor"]
            diet_classifier = [x for x in old_entities if x.get("extractor") == "DIETClassifier"]
            new_entities = []

            # regex_extractor priority 1
            new_entities += regex_extractor

            # flair_extractor priority 2
            for e1 in flair_extractor:
                ok = True
                for e2 in new_entities:
                    if is_duplicated(e1, e2) or is_overlap(e1, e2):
                        ok = False
                        break
                if ok and e1.get("confidence") >= THRESHOLD:
                    new_entities.append(e1)

            # diet_classifier priority 2
            for e1 in diet_classifier:
                ok = True
                for e2 in new_entities:
                    if is_duplicated(e1, e2) or is_overlap(e1, e2):
                        ok = False
                        break
                if ok and e1.get("confidence_entity") >= THRESHOLD:
                    new_entities.append(e1)
                    
            message.set("entities", new_entities, add_to_output=True)
        

    def persist(self, file_name: Text, model_dir: Text) -> Optional[Dict[Text, Any]]:
        """Persist this component to disk for future loading."""

        pass




