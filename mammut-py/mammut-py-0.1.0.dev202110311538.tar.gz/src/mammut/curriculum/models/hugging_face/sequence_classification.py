from typing import Optional
from mammut.curriculum.models.model_base import ModelBase
from transformers import (
    pipeline,
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TFAutoModelForSequenceClassification,
)
from abc import abstractmethod
import torch
import tensorflow as tf
from mammut.curriculum.core.mammut_session_context import MammutSessionContext


class HuggingFaceSequenceClassificationModel(ModelBase):
    """Downloads and caches a HuggingFace pretrained model and its tokenizer.

    This is a base API for 'sequence classification' in Hugging Face models.
    Sequence classification is the task of classifying sequences according to a
    given number of classes.

    ..  _Hugging Face Docs Sequence Classification:
        https://huggingface.co/transformers/task_summary.html#sequence-classification
    """

    def __init__(self):
        ModelBase.__init__(self)
        self.pt_model: Optional[AutoModelForSequenceClassification] = None
        self.tf_model: Optional[TFAutoModelForSequenceClassification] = None
        self.tokenizer: Optional[AutoTokenizer] = None

    @property
    @abstractmethod
    def hf_model_name(self) -> str:
        """Returns a Hugging Face's model name.

        This method is used to provide main class a Hugging Face's model name
        to be downloaded and cached locally.

        ..  _Hugging Face Docs summary of the models:
            https://huggingface.co/transformers/model_summary.html
        """
        pass

    @property
    @abstractmethod
    def task(self) -> str:
        """Returns a task name for Hugging Face models.

        Hugging Face models allow for Natural Language Understanding (NLU) tasks
        such as question answering, sequence classification, named entity
        recognition and others.

        ..  _Hugging Face Docs summary of the tasks:
            https://huggingface.co/transformers/task_summary.html
        """
        pass

    @abstractmethod
    def paraphrase_identification(self, input_1: str, input_2: str) -> int:
        """ It performs a comparison between two inputs to determine
        how close they are to be a paraphrase one another.
        """
        pass

    def sentiment_analysis(self, text_input):
        """Hugging Face's pipeline task.

        Args:
            text_input(str): input text to perform analysis.

        Return:
            Returns a label alongside a score.
        """
        results = self.classifier(text_input)
        return results

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Passes ModelBase's train method.

        Train method passes since class uses a pretrained model.
        """
        pass

    def save(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Models persistence hasn't been implemented"""
        pass


class TorchHuggingFaceSequenceClassification(
    HuggingFaceSequenceClassificationModel
):
    """Allows to perform text classification tasks in Hugging Face models using PyTorch Framework.

    Text classification is the task of classifying text according to
    different criteria. An example can be comparing two inputs to see
    if they're paraphrases one another.
    """

    def __init__(self):
        HuggingFaceSequenceClassificationModel.__init__(self)
        self.pt_model = AutoModelForSequenceClassification.from_pretrained(
            self.hf_model_name
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.hf_model_name)
        self.classifier = pipeline(
            task=self.task, model=self.pt_model, tokenizer=self.tokenizer
        )

    def hf_model_name(self) -> str:
        pass

    @property
    def task(self) -> str:
        """Provides a Hugging Face's pipeline task name.

        Returns:
            Returns task name.
        """
        return "sentiment-analysis"

    def paraphrase_identification(self, input_1: str, input_2: str) -> int:
        """It performs a comparison between two inputs to determine
        how close they are to be a paraphrase one another.

        Args:
            input_1(str): first input text.
            input_2(str): second input text.

        Returns:
            Returns a classification score.
        """
        paraphrase = self.tokenizer(input_1, input_2, return_tensors="pt")
        paraphrase_classification_logits = self.pt_model(**paraphrase).logits
        paraphrase_results = torch.softmax(
            paraphrase_classification_logits, dim=1
        ).tolist()[0][1]
        return paraphrase_results


class TensorFlowHuggingFaceSequenceClassification(
    HuggingFaceSequenceClassificationModel
):
    """Allows to perform text classification tasks in Hugging Face models using TensorFlow Framework.

    Text classification is the task of classifying text according to
    different criteria. An example can be comparing two inputs to see
    if they're paraphrases one another.
    """

    def __init__(self):
        HuggingFaceSequenceClassificationModel.__init__(self)
        self.tf_model = TFAutoModelForSequenceClassification.from_pretrained(
            self.hf_model_name, from_pt=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.hf_model_name)
        self.classifier = pipeline(
            task=self.task, model=self.pt_model, tokenizer=self.tokenizer
        )

    def hf_model_name(self) -> str:
        pass

    @property
    def task(self) -> str:
        """Provides a Hugging Face's pipeline task name.

        Returns:
            Returns task name.
        """
        return "sentiment-analysis"

    def paraphrase_identification(self, input_1: str, input_2: str) -> int:
        """It performs a comparison between two inputs to determine
        how close they are to be a paraphrase one another.

        Args:
            input_1(str): first input text.
            input_2(str): second input text.

        Returns:
            Returns a classification score.
        """
        paraphrase = self.tokenizer(input_1, input_2, return_tensors="tf")
        paraphrase_classification_logits = self.tf_model(paraphrase).logits
        paraphrase_results = tf.nn.softmax(
            paraphrase_classification_logits, axis=1
        ).numpy()[0][1]
        return paraphrase_results


class TorchRuperta(TorchHuggingFaceSequenceClassification):
    """Hugging Face model 'Ruperta' integration.
    """

    def __init__(self):
        TorchHuggingFaceSequenceClassification.__init__(self)

    @property
    def hf_model_name(self) -> str:
        """Provides a Hugging Face's model name.

        Returns:
            Returns model name.

        ..  _Hugging Face RuPERTa-base-finetuned-pawsx-es:
            https://huggingface.co/mrm8488/RuPERTa-base-finetuned-pawsx-es
        """
        return "mrm8488/RuPERTa-base-finetuned-pawsx-es"


class TensorFlowRuperta(TensorFlowHuggingFaceSequenceClassification):
    """Hugging Face model 'Ruperta' integration.

    RuPERTa is a paraphrase identification model.

    ..  _Hugging Face RuPERTa-base-finetuned-pawsx-es:
        https://huggingface.co/mrm8488/RuPERTa-base-finetuned-pawsx-es
    """

    def __init__(self):
        TensorFlowHuggingFaceSequenceClassification.__init__(self)

    @property
    def hf_model_name(self) -> str:
        """Provides a Hugging Face's model name.

        Returns:
            Returns model name.
        """
        return "mrm8488/RuPERTa-base-finetuned-pawsx-es"
