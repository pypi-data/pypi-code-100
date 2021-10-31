import logging
from mammut.common.corpus.hugging_face_corpus import HuggingFaceDatasetCorpus
from typing import Union
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
from abc import ABC, abstractmethod
from typing import Dict
import datasets

log = logging.getLogger(__name__)


class HFPreprocessBase(ABC):
    """HFPreprocessBase class models a unit of preprocessing
    and formatting HuggingFace data.

    A HFPreprocessBase encapsulates:
    - A HuggingFace tokenizer instance, specific for the concrete model
    - Parameters for the tokenizer.

    The concept behind this common preprocessing class is to
    encapsulate task-specific preprocessing of a dataset in a mixin class that
    can be inherited by the curriculum wrapper classes for the models.
    """

    def __init__(self, tokenizer_parameters: Dict, preprocess_parameters: Dict):
        """
        Each preprocessing will receive the parameters for the tokenizer and the parameters
        for the preprocessing operations.

        Tokenizer parameters are the one received by the tokenizer __init__ method:
            https://huggingface.co/transformers/main_classes/tokenizer.html#transformers.PreTrainedTokenizer

        Preprocess parameters are named parameters used in the preprocessing operations, that are not
        constructor parameters of the tokenizer. For example, parameters of the __call__ method:
            https://huggingface.co/transformers/internal/tokenization_utils.html#transformers.tokenization_utils_base.PreTrainedTokenizerBase.__call__

        Args:
            tokenizer_parameters: Dictionary with tokenizer parameters to forward to this preprocess.
            preprocess_parameters: Dictionary with preprocess parameters.
        """
        self.tokenizer_parameters: Dict = tokenizer_parameters
        self.preprocess_parameters: Dict = preprocess_parameters
        self._tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast] = self._load_tokenizer()

    @abstractmethod
    def _load_tokenizer(self) -> Union[PreTrainedTokenizer, PreTrainedTokenizerFast]:
        """Factory method to return the tokenizer required by the model.

        Users of this class decides which type of tokenizer suits better for them.

        # TODO: research the differences between fast and normal tokenizers.
        """
        pass

    @abstractmethod
    def tokenize_corpus(self, dataset: datasets.Dataset) -> datasets.Dataset:
        """Tokenizes the passed Dataset wrapped by the HuggingFaceDatasetCorpus class,
        and returns the encoded Dataset.

        Return:
            Returns the encoded Dataset required in the model train.
        """
        pass


class TokenClassificationPreprocess(HFPreprocessBase):
    def __init__(self,
                 tokenizer_parameters: Dict,
                 preprocess_parameters: Dict,
                 task: str):
        """
        Args:
            tokenizer_parameters: Dictionary with tokenizer parameters to forward to this preprocess.
            task: task specification in token classification model. i.e.: "ner", "pos" or "chunk".
        """
        self.task = task
        HFPreprocessBase.__init__(self, tokenizer_parameters, preprocess_parameters)

    def _tokenize_and_align_labels(self, examples):
        """Tokenizes the dataset. And aligns the labels with the word_ids in the tokenization results.
        In special tokens have a word id that is None. We set the label to
         -100 so they are automatically ignored in the loss function.
         We set the label for the first token of each word.
         For the other tokens in a word, we set the label to either
         the current label or -100, depending on the label_all_tokens flag.
            Args:
                examples: HuggingFace Dataset for the training.
                """
        tokenized_inputs = self._tokenizer(
            examples["tokens"], **self.preprocess_parameters
        )
        label_all_tokens = True
        labels = []
        for i, label in enumerate(examples[f"{self.task}_tags"]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                if word_idx is None:
                    label_ids.append(-100)
                elif word_idx is not None:
                    label_ids.append(label[word_idx])
                else:
                    label_ids.append(
                        label[word_idx] if label_all_tokens else -100
                    )
                    previous_word_idx = word_idx

            labels.append(label_ids)

        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    def tokenize_corpus(self, dataset: datasets.Dataset) -> datasets.Dataset:
        """This method tokenizes some features of the loaded dataset in method get_corpus in the LessonBase class.

        Return:
            Returns encoding data required in the model train.
        """
        preprocessed_data = dataset.map(
            self._tokenize_and_align_labels, batched=True
        )
        return preprocessed_data


class HFPreprocessForQuestionAnswering(HFPreprocessBase):
    """This abstract class encapsulates the preprocessing of a question-answering task.
    """

    def __init__(
            self,
            tokenizer_parameters: Dict,
            preprocess_parameters: Dict
    ):
        """
        For a detailed explanation of the difference between tokenizer parameters and preprocess paratemeters,
        check the super class docstring of __init__.

        Args:
            tokenizer_parameters: Dictionary with tokenizer parameters to forward to this preprocess.
            preprocess_parameters: Dictionary with preprocess parameters.
        """
        HFPreprocessBase.__init__(
            self,
            tokenizer_parameters,
            preprocess_parameters
        )

    def _preprocessing(self, dataset):

        """ The method adds two values to the encoding data:
        'start_positions' and 'end_positions'.
        These values indicate the beginning and the end
        of the answer located in the value 'context'.

        Args:
            dataset: non-tokenized data.

        Return:
            Returns encoding data with the features 'start_positions'
            and 'end_positions'.
        """

        pad_on_right = (
            self._tokenizer.padding_side
        )

        encodings = self._tokenizer(
            dataset["question" if pad_on_right else "context"],
            dataset["context" if pad_on_right else "question"],
            truncation="only_second" if pad_on_right else "only_first",
            max_length=self.preprocess_parameters["max_length"],
            stride=self.preprocess_parameters["stride"],
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length",
        )

        sample_mapping = encodings.pop("overflow_to_sample_mapping")
        offset_mapping = encodings.pop("offset_mapping")

        encodings["start_positions"] = []
        encodings["end_positions"] = []

        for i, offsets in enumerate(offset_mapping):
            input_ids = encodings["input_ids"][i]
            cls_index = input_ids.index(self._tokenizer.cls_token_id)
            sequence_ids = encodings.sequence_ids(i)
            sample_index = sample_mapping[i]
            answers_index = dataset["answers"][sample_index]

            if len(answers_index["answer_start"]) == 0:
                encodings["start_positions"].append(cls_index)
                encodings["end_positions"].append(cls_index)

            else:
                start_char = answers_index["answer_start"][0]
                end_char = start_char + len(answers_index["text"][0])

                token_start_index = 0
                while sequence_ids[token_start_index] != (1 if pad_on_right else 0):
                    token_start_index += 1

                token_end_index = len(input_ids) - 1
                while sequence_ids[token_end_index] != (1 if pad_on_right else 0):
                    token_end_index -= 1

                if not (offsets[token_start_index][0] <= start_char and offsets[token_end_index][1] >= end_char):
                    encodings["start_positions"].append(cls_index)
                    encodings["end_positions"].append(cls_index)
                else:
                    while token_start_index < len(offsets) and offsets[token_start_index][0] <= start_char:
                        token_start_index += 1
                    encodings["start_positions"].append(token_start_index - 1)
                    while offsets[token_end_index][1] >= end_char:
                        token_end_index -= 1
                    encodings["end_positions"].append(token_end_index + 1)

        return encodings

    def tokenize_corpus(self, dataset: datasets.Dataset) -> datasets.Dataset:
        """This method tokenizes some features of the loaded dataset in method get_corpus in the LessonBase class.

        Return:
            Returns encoding data required in the model train.
        """
        selected_split = self.preprocess_parameters["split"]
        preprocessed_data = dataset.map(
                self._preprocessing,
                batched=True,
                remove_columns=dataset[selected_split].column_names
            )
        return preprocessed_data


class HFPreprocessForParaphraseClassification(HFPreprocessBase):
    """ This subclass encapsulates the preprocessing of a sequence classification task.

    """

    def __init__(self, tokenizer_parameters: Dict, preprocess_parameters: Dict):
        HFPreprocessBase.__init__(
            self,
            tokenizer_parameters,
            preprocess_parameters,
        )

    def _token_function(self, dataset):
        encodings = self._tokenizer(
            dataset['sentence1'],
            dataset['sentence2'],
            dataset['label'],
            padding=True,
            truncation=self.preprocess_parameters['truncation'],
        )
        return encodings

    def tokenize_corpus(self, dataset: datasets.Dataset) -> datasets.Dataset:
        """This method implements a mapping on the input corpus.
        Tokenize loaded dataset in method get_corpus in the LessonBase class.

        Return:
            Returns encoding data required in the model train.
        """
        tokenized_data = dataset.map(self._token_function, batched=True,)
        preprocessed_data = tokenized_data.map(
                lambda examples: {"labels": examples["label"]}, batched=True
            )
        return preprocessed_data
