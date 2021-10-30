import os
import pickle
import sklearn
import sklearn.preprocessing
import pandas as pd
import tensorflow as tf

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
from transformers import AutoTokenizer
from transformers import InputExample, InputFeatures
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from src.dataset.utils import DatasetType, TokenizerType


class BaseDataset(ABC):

    DATA_COLUMN = 'text'
    LABEL_COLUMN = 'prediction'
    OHOT_COLUMN = 'ohot_lbl'

    def __init__(self,
                 dataset_path: str,
                 tokenizer_name: Union[str, None],
                 tokenizer_type: TokenizerType,
                 use_umlaute: bool = False,
                 SEED=42):
        # configs
        self.embed_size = 300
        self.max_features = 50000
        self.max_len = 128
        self.tokenizer_name = tokenizer_name
        self.tokenizer_type = tokenizer_type
        self.use_umlaute = use_umlaute
        self.SEED = SEED

        # create an encoder to transform the targets
        self.labelencoder = sklearn.preprocessing.LabelEncoder()

        # check if the dataset path exists
        self.dataset_path = Path(dataset_path)
        if not self.dataset_path.exists():
            raise ValueError('Dataset path must exist.')

    def _prepare_df(self):
        # preprocess datasets
        self.df_train = self.preprocessor.transform(self.df_train)
        self.df_val = self.preprocessor.transform(self.df_val)
        self.df_test = self.preprocessor.transform(self.df_test)

        # transform the predictions into numeric values
        self.df_train[self.LABEL_COLUMN] = self.labelencoder.fit_transform(
            self.df_train[self.LABEL_COLUMN])
        self.df_val[self.LABEL_COLUMN] = self.labelencoder.transform(
            self.df_val[self.LABEL_COLUMN])
        # check if the label column exists for the test set
        if self.LABEL_COLUMN in self.df_test.columns:
            self.df_test[self.LABEL_COLUMN] = self.labelencoder.transform(
                self.df_test[self.LABEL_COLUMN])

        # create one-hot encodings for labels
        self.df_train[self.OHOT_COLUMN] = list(
            tf.keras.utils.to_categorical(self.df_train[self.LABEL_COLUMN]))
        self.df_val[self.OHOT_COLUMN] = list(
            tf.keras.utils.to_categorical(self.df_val[self.LABEL_COLUMN]))
        # check if the label column exists for the test set
        if self.LABEL_COLUMN in self.df_test.columns:
            self.df_test[self.OHOT_COLUMN] = list(
                tf.keras.utils.to_categorical(self.df_test[self.LABEL_COLUMN]))

    def _get_tokenizer(self):
        if self.tokenizer_type is TokenizerType.HUGGINGFACE:
            tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)
        elif self.tokenizer_type is TokenizerType.TOKENS:
            tokenizer = Tokenizer(num_words=self.max_features)
            tokenizer.fit_on_texts(list(self.df_train[self.DATA_COLUMN]))
        else:
            tokenizer = None

        return tokenizer

    def _convert_data_to_examples(self,
                                  df: pd.DataFrame,
                                  one_hot=False) -> list:
        # check if one hot encoding should be used
        if one_hot:
            lbl_col = self.OHOT_COLUMN
        else:
            lbl_col = self.LABEL_COLUMN

        # check if the label column exists for the dataset
        # (not always the case for the test set)
        if lbl_col in df.columns:
            lbl_exists = True
        else:
            lbl_exists = False

        # guid: globally unique ID for bookkeeping (unused here)
        df_InputExamples = df.apply(
            lambda x: InputExample(guid=None,
                                   text_a=x[self.DATA_COLUMN],
                                   text_b=None,
                                   label=x[lbl_col] if lbl_exists else 0),
            axis=1)

        return list(df_InputExamples)

    def _generate_samples(self, features):
        """
        Method to generate the dataset.

        Used by the tf.data.Dataset.from_generator method to generate a TF Dataset.
        """
        for f in features:
            # create the needed input format for the bert model
            yield ({
                "input_ids": f.input_ids,
                "attention_mask": f.attention_mask,
                "token_type_ids": f.token_type_ids
            }, f.label)

    def _convert_examples_to_tf_dataset(self,
                                        examples,
                                        max_length=128,
                                        one_hot=False) -> tf.data.Dataset:
        # hold the InputFeatures to be converted
        features = []

        for e in examples:
            # use the encode_plus method of the bert model to ensure that the correct encoding was used
            input_dict = self.tokenizer.encode_plus(e.text_a,
                                                    add_special_tokens=True,
                                                    max_length=max_length,
                                                    return_token_type_ids=True,
                                                    return_attention_mask=True,
                                                    pad_to_max_length=True,
                                                    truncation=True)

            input_ids, token_type_ids, attention_mask = (
                input_dict["input_ids"],
                input_dict["token_type_ids"],
                input_dict['attention_mask']
            )

            features.append(
                InputFeatures(input_ids=input_ids,
                              attention_mask=attention_mask,
                              token_type_ids=token_type_ids,
                              label=e.label))

        return tf.data.Dataset.from_generator(
            lambda: self._generate_samples(features),
            ({
                "input_ids": tf.int32,
                "attention_mask": tf.int32,
                "token_type_ids": tf.int32
            }, tf.int64), ({
                "input_ids": tf.TensorShape([None]),
                "attention_mask": tf.TensorShape([None]),
                "token_type_ids": tf.TensorShape([None])
            }, tf.TensorShape([None] if one_hot else [])))

    def _handle_dataframe(self,
                          df: pd.DataFrame,
                          batch_size: int,
                          one_hot=False,
                          **kwargs):
        # check if one hot encoding should be used
        if one_hot:
            lbl_col = self.OHOT_COLUMN
        else:
            lbl_col = self.LABEL_COLUMN

        # transform the dataset according to the tokenizer
        if self.tokenizer_type is TokenizerType.HUGGINGFACE:
            df_input_examples = self._convert_data_to_examples(df,
                                                               one_hot=one_hot)
            tf_data = self._convert_examples_to_tf_dataset(df_input_examples,
                                                           one_hot=one_hot)

        elif self.tokenizer_type is TokenizerType.TOKENS:
            df_seq = self.tokenizer.texts_to_sequences(df[self.DATA_COLUMN])
            df_seq = pad_sequences(df_seq, maxlen=self.max_len)
            tf_data = tf.data.Dataset.from_tensor_slices(
                (df_seq, list(df[lbl_col])))

        elif self.tokenizer_type is TokenizerType.NONE:
            tf_data = tf.data.Dataset.from_tensor_slices(
                (df[self.DATA_COLUMN], list(df[lbl_col])))

        else:
            raise ValueError('Unhandled tokenizer type and tokenizer provide.')

        tf_data = tf_data.shuffle(100).batch(batch_size)

        return tf_data

    def get_dataset(self,
                    dataset_type: DatasetType,
                    batch_size=32,
                    one_hot=False):
        # define the switcher for the different dataset types
        switcher = {
            DatasetType.TRAIN: self.df_train,
            DatasetType.VAL: self.df_val,
            DatasetType.TEST: self.df_test,
        }

        # get the dataset and sanity check
        df_data = switcher.get(dataset_type, None)
        if df_data is None:
            raise ValueError('Invalid dataset type')

        # call the dataset function
        dataset = self._handle_dataframe(df=df_data,
                                         batch_size=batch_size,
                                         one_hot=one_hot)

        return dataset

    def get_class_weights(self):
        neg = self.df_train[self.LABEL_COLUMN].value_counts()[0]
        pos = self.df_train[self.LABEL_COLUMN].value_counts()[1]
        total = len(self.df_train)

        # Scaling by total/2 helps keep the loss to a similar magnitude.
        # The sum of the weights of all examples stays the same.
        weight_for_0 = (1 / neg) * (total / 2.0)
        weight_for_1 = (1 / pos) * (total / 2.0)

        class_weight = {0: weight_for_0, 1: weight_for_1}

        print('Weight for class 0: {:.2f}'.format(weight_for_0))
        print('Weight for class 1: {:.2f}'.format(weight_for_1))

        return class_weight

    def save_tokenizer(self, path: str):
        if self.tokenizer is not None:
            tokenizer_file_name = os.path.join(path, 'tokenizer.pickle')
            tokenizer_file = open(tokenizer_file_name, 'wb')
            pickle.dump(self.tokenizer, tokenizer_file)
            tokenizer_file.close()

    def save_label_encoder(self, path: str):
        if self.labelencoder is not None:
            le_file_name = os.path.join(path, 'label_encoder.pickle')
            le_file = open(le_file_name, 'wb')
            pickle.dump(self.labelencoder, le_file)
            le_file.close()
