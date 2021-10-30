import unittest
import tensorflow as tf

from src.models.fasttext_model import FastTextModel
from src.dataset.utils import DatasetType, TokenizerType
from src.dataset.natio_dataset import NationalityDataset


class TestFastTextModel(unittest.TestCase):

    def setUp(self):
        self.dataset_path = '/media/gengar/vm01-prejudice-bias-hotel-reviews/data/natio_df.csv'

    def test_compile_linear(self):
        tf.keras.backend.clear_session()
        fasttext_model = FastTextModel.create_linear()
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.assertIsNotNone(fasttext_model)

    def test_fit_linear(self):
        tf.keras.backend.clear_session()
        dataset = NationalityDataset(dataset_path=self.dataset_path,
                                     tokenizer_name=None,
                                     tokenizer_type=TokenizerType.NONE)
        train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN, batch_size=16)
        fasttext_model = FastTextModel.create_linear()
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        fasttext_model.fit(train_data, epochs=1, verbose=0)

    def test_compile_lstm(self):
        tf.keras.backend.clear_session()
        fasttext_model = FastTextModel.create_lstm()
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.assertIsNotNone(fasttext_model)

    def test_fit_lstm(self):
        tf.keras.backend.clear_session()
        dataset = NationalityDataset(dataset_path=self.dataset_path,
                                     tokenizer_name=None,
                                     tokenizer_type=TokenizerType.TOKENS)
        train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN, batch_size=16)
        fasttext_model = FastTextModel.create_lstm()
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        fasttext_model.fit(train_data, epochs=1, verbose=0)

    def test_fit_lstm_fasttext(self):
        tf.keras.backend.clear_session()
        dataset = NationalityDataset(dataset_path=self.dataset_path,
                                     tokenizer_name=None,
                                     tokenizer_type=TokenizerType.TOKENS)
        train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN, batch_size=16)
        fasttext_model = FastTextModel.create_lstm(embedding_type='fasttext',
                                                   word_index=dataset.tokenizer.word_index)
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        fasttext_model.fit(train_data, epochs=1, verbose=0)

    def test_compile_bilstm(self):
        tf.keras.backend.clear_session()
        fasttext_model = FastTextModel.create_bilstm()
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.assertIsNotNone(fasttext_model)

    def test_fit_bilstm(self):
        tf.keras.backend.clear_session()
        dataset = NationalityDataset(dataset_path=self.dataset_path,
                                     tokenizer_name=None,
                                     tokenizer_type=TokenizerType.TOKENS)
        train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN, batch_size=16)
        fasttext_model = FastTextModel.create_bilstm()
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        fasttext_model.fit(train_data, epochs=1, verbose=0)

    def test_fit_bilstm_fasttext(self):
        tf.keras.backend.clear_session()
        dataset = NationalityDataset(dataset_path=self.dataset_path,
                                     tokenizer_name=None,
                                     tokenizer_type=TokenizerType.TOKENS)
        train_data = dataset.get_dataset(dataset_type=DatasetType.TRAIN, batch_size=16)
        fasttext_model = FastTextModel.create_bilstm(embedding_type='fasttext',
                                                     word_index=dataset.tokenizer.word_index)
        fasttext_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        fasttext_model.fit(train_data, epochs=1, verbose=0)


if __name__ == '__main__':
    unittest.main()
