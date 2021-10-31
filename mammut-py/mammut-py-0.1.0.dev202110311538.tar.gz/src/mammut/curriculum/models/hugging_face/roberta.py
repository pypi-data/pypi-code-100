from mammut.curriculum.models.hugging_face.pre_trained_model import (
    HuggingFacePreTrainedModel,
)
import mammut.curriculum.report as report
from transformers import (
    Trainer,
    TrainingArguments,
    RobertaForTokenClassification,
    RobertaForQuestionAnswering,
    DataCollatorForTokenClassification,
    RobertaForSequenceClassification,
    RobertaConfig,
    RobertaTokenizer,
    RobertaTokenizerFast,
)
from datasets import *
from pandas import DataFrame
from typing import Dict
import logging
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from mammut.common.corpus.corpus_map import CorpusMap

from mammut.curriculum.core.mammut_session_context import MammutSessionContext
from mammut.curriculum.models.hugging_face.preprocess_data import (
    TokenClassificationPreprocess,
    HFPreprocessForQuestionAnswering,
    HFPreprocessForParaphraseClassification,
)

log = logging.getLogger(__name__)


class HuggingFaceRobertaTokenClassificationModel(
    HuggingFacePreTrainedModel, TokenClassificationPreprocess
):
    """This is a wrapper for the Roberta Model transformer.

    https://huggingface.co/transformers/model_doc/roberta.html#robertamodel

    """

    def __init__(
        self,
        parameters: Dict,
        course_id: int,
        lesson_id: int,
        mammut_session_context: MammutSessionContext,
        corpus_id: int,
        corpus_map: CorpusMap,
    ):
        """
       Args:
          parameters: The parameters parsed JSON included the parameters required:
                - specific parameters for the current model.
                - tokenizer_parameters(Dict): include the tokenizer parameters to forward to this model.
                - preprocess_parameters(Dict): include the preprocess parameters to forward to this model.
                - task(str): concrete task in token classification model ("ner", "pos" or "chunk").
          course_id (int): the course ID to which this model belongs.
          lesson_id (int): the lesson ID to which this model belongs.
          mammut_session_context: Mammut session context with general information about
               current curriculum instance.
          corpus_id(str): 'corpus_id' value in datasource retrieved data.
       """
        tokenizer_parameters: Dict = parameters["tokenizer_parameters"]
        preprocess_parameters: Dict = parameters["preprocess_parameters"]
        task: str = parameters["task"]
        HuggingFacePreTrainedModel.__init__(
            self,
            parameters,
            course_id,
            lesson_id,
            mammut_session_context,
            corpus_id,
            corpus_map,
        )
        TokenClassificationPreprocess.__init__(
            self, tokenizer_parameters, preprocess_parameters, task
        )
        self.labels = self._load_labels(self.get_corpus(corpus_id, corpus_map))

    def load_pretrained_models(self):
        """Load the pretrained model for this ROBERTA wrapper. """

        config = RobertaConfig.from_pretrained(self._name_or_path)
        config.num_labels = len(self.labels)
        self._model = RobertaForTokenClassification(config)

    def _load_tokenizer(self):
        tokenizer = RobertaTokenizerFast.from_pretrained(
            self._name_or_path, **self.tokenizer_parameters
        )
        return tokenizer

    def _load_labels(self, dataset):
        """To train a model we will need to specify the number of labels
        in the data source. This method receives the corpus
        (Dataset, DataDict or DataFrame) and returns a list with the labels.
        """

        if type(dataset) == DatasetDict:
            labels = (
                dataset["train"].features[f"{self.task}_tags"].feature.names
            )
            return labels
        elif type(dataset) == Dataset:
            labels = dataset.features[f"{self.task}_tags"].feature.names
            return labels
        elif type(dataset) == DataFrame:
            labels = sorted(
                list(
                    set(
                        [
                            lbls
                            for sublist in dataset.tags.tolist()
                            for lbls in sublist
                        ]
                    )
                )
            )
            return [labels]
        else:
            raise ValueError(
                "The data format should be Dataset, DictDataset or Dataframe. Verify your data format"
            )

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train the Roberta base model in the lesson.
        Args:
            ** mammut_session_context
            ** num_epochs(float): total number of training epochs to perform, defaults to 3.0.
                If not an integer, will perform the decimal part percents of the last epoch
                before stopping training.
            ** training_batch_size(int): batch size per device during training, defaults to 8.
            ** eval_batch_size(int): batch size for evaluation, defaults to 8.
        """

        corpus = kwargs["corpus"]

        if len(corpus.keys()) > 1:
            train_dataset = corpus["train"]
            eval_dataset = corpus["validation"]

            num_epochs = self.parameters["num_epochs"]
            training_batch_size = self.parameters["train_batch_size"]
            evaluation_batch_size = self.parameters["eval_batch_size"]
            warmup_steps = 500
            weight_decay = 0.01

            def compute_metrics(pred):
                labels = pred.label_ids
                preds = pred.predictions.argmax(-1)
                precision, recall, f1, _ = precision_recall_fscore_support(
                    labels, preds, average="micro"
                )
                acc = accuracy_score(labels, preds)
                return {
                    "accuracy": acc,
                    "f1": f1,
                    "precision": precision,
                    "recall": recall,
                }

            data_collator = DataCollatorForTokenClassification(self._tokenizer)
            training_args = TrainingArguments(
                output_dir="./results",
                num_train_epochs=num_epochs,
                per_device_train_batch_size=training_batch_size,
                per_device_eval_batch_size=evaluation_batch_size,
                warmup_steps=warmup_steps,
                weight_decay=weight_decay,
                logging_dir="./logs",
            )
            trainer = Trainer(
                model=self._model,
                tokenizer=self._tokenizer,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
                data_collator=data_collator,
                compute_metrics=compute_metrics,
            )
            return trainer.train()
        else:
            raise ValueError(
                "The model can not to train with only one dataset. Verify that your DictDataset contains at least two datasets."
            )


class HuggingFaceRobertaQuestionAnsweringModel(
    HuggingFacePreTrainedModel, HFPreprocessForQuestionAnswering
):
    """This is a wrapper for the RobertaForQuestionAnswering model
    """

    def __init__(
        self,
        parameters: Dict,
        course_id: int,
        lesson_id: int,
        mammut_session_context: MammutSessionContext,
        corpus_id: int,
        corpus_map: CorpusMap,
    ):
        """
        Args:
          parameters: The model parameters parsed JSON.
          course_id (int): the course ID to which this model belongs.
          lesson_id (int): the lesson ID to which this model belongs.
          mammut_session_context: Mammut session context with general information about
               current curriculum instance.
       """
        tokenizer_parameters: Dict = parameters["tokenizer_parameters"]
        preprocess_parameters: Dict = parameters["preprocess_parameters"]

        HuggingFacePreTrainedModel.__init__(
            self,
            parameters,
            course_id,
            lesson_id,
            mammut_session_context,
            corpus_id,
            corpus_map,
        )

        HFPreprocessForQuestionAnswering.__init__(
            self, tokenizer_parameters, preprocess_parameters
        )

    def _load_tokenizer(self):
        self._tokenizer = RobertaTokenizerFast.from_pretrained(
            self._name_or_path, padding_side=self.tokenizer_parameters['padding_side']
        )
        return self._tokenizer

    def load_pretrained_models(self):
        """Load the pretrained model for this Roberta wrapper. """
        self._model = RobertaForQuestionAnswering.from_pretrained(
            self._name_or_path
        )

    def train(self,  mammut_session_context: MammutSessionContext, **kwargs):
        """Train this QuestionAnswering model in the lesson.
        Note: nothing to train yet.
        Todo: Collaboration between Mammut Corpus (or other data source) and
            this model needs to be defined.
        """
        corpus = kwargs["corpus"]

        if len(corpus.keys()) > 1:
            train_dataset = corpus["train"]
            eval_dataset = corpus["validation"]

            epochs = self.parameters["num_train_epochs"]
            train_batch = self.parameters["train_batch_size"]
            eval_batch = self.parameters["eval_batch_size"]
            warmup_steps = self.parameters["warmup_steps"]
            weight_decay = self.parameters["weight_decay"]

            training_args = TrainingArguments(
                output_dir='./results',
                num_train_epochs=epochs,
                per_device_train_batch_size=train_batch,
                per_device_eval_batch_size=eval_batch,
                warmup_steps=warmup_steps,
                weight_decay=weight_decay,
                logging_dir="./logs",
            )

            trainer = Trainer(
                model=self._model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
            )

            training = trainer.train()

            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    "Training HuggingFaceRobertaQuestionAnsweringModel model"
                )
            )
            return training
        else:
            raise ValueError(
                "The model can not to train with only one dataset. Verify that your DictDataset contains at least two datasets."
            )


class HuggingFaceRobertaSequenceClassificationModel(
    HuggingFacePreTrainedModel, HFPreprocessForParaphraseClassification
):
    """This is a wrapper for the RobertaForSequenceClassification model
    https://huggingface.co/transformers/model_doc/bert.html#bertfortokenclassification
    """

    def __init__(
        self,
        parameters: Dict,
        course_id: int,
        lesson_id: int,
        mammut_session_context: MammutSessionContext,
        corpus_id: int,
        corpus_map: CorpusMap,
    ):
        """
        Args:
          parameters: The model parameters parsed JSON.
          course_id (int): the course ID to which this model belongs.
          lesson_id (int): the lesson ID to which this model belongs.
          mammut_session_context: Mammut session context with general information about
               current curriculum instance.
       """
        preprocess_parameters: Dict = parameters["preprocess_parameters"]
        tokenizer_parameters: Dict = parameters["tokenizer_parameters"]
        HuggingFacePreTrainedModel.__init__(
            self,
            parameters,
            course_id,
            lesson_id,
            mammut_session_context,
            corpus_id,
            corpus_map,
        )

        HFPreprocessForParaphraseClassification.__init__(
            self, tokenizer_parameters, preprocess_parameters
        )

    def _load_tokenizer(self):
        self._tokenizer = RobertaTokenizer.from_pretrained(
            self._name_or_path, use_fast=True,
        )
        return self._tokenizer

    def load_pretrained_models(self):
        """Load the pretrained model for this Roberta wrapper. """
        label = self.parameters["num_labels"]
        self._model = RobertaForSequenceClassification.from_pretrained(
            self._name_or_path, num_labels=label
        )

    def train(self, mammut_session_context: MammutSessionContext, **kwargs):
        """Train this classification model in the lesson.
        Note: nothing to train yet.
        Todo: Collaboration between Mammut Corpus (or other data source) and
            this model needs to be defined.
        """
        corpus = kwargs["corpus"]

        if len(corpus.keys()) > 1:
            train_dataset = corpus["train"]
            eval_dataset = corpus["validation"]

            epochs = self.parameters["num_train_epochs"]
            train_batch = self.parameters["train_batch_size"]
            eval_batch = self.parameters["eval_batch_size"]
            warmup_steps = self.parameters["warmup_steps"]
            weight_decay = self.parameters["weight_decay"]

            training_args = TrainingArguments(
                output_dir='./results',
                num_train_epochs=epochs,
                per_device_train_batch_size=train_batch,
                per_device_eval_batch_size=eval_batch,
                warmup_steps=warmup_steps,
                weight_decay=weight_decay,
                logging_dir="./logs",
            )

            trainer = Trainer(
                model=self._model,
                args=training_args,
                train_dataset=train_dataset,
                eval_dataset=eval_dataset,
            )

            training = trainer.train()

            report.send_message(
                report.CurriculumGeneralDebugMessage(
                    "Training HuggingFaceRobertasequenceClassificationModel model"
                )
            )
            return training
        else:
            raise ValueError(
                "The model can not to train with only one dataset. Verify that your DictDataset contains at least two datasets."
            )
