import unittest

from src.dataset.hate_dataset import HateDataset
from src.dataset.utils import DatasetType, TokenizerType


class TestHateDataset(unittest.TestCase):
    def setUp(self):
        self.data_path = 'data/'

    def test_train_iterator(self):
        dataset = HateDataset(self.data_path,
                              tokenizer_name='bert-base-german-cased',
                              tokenizer_type=TokenizerType.HUGGINGFACE)
        dataset = dataset.get_dataset(dataset_type=DatasetType.TRAIN)
        for row in dataset.take(3):
            self.assertIsNotNone(row[0])
            self.assertIsNotNone(row[1])

    def test_val_iterator(self):
        dataset = HateDataset(self.data_path,
                              tokenizer_name='bert-base-german-cased',
                              tokenizer_type=TokenizerType.HUGGINGFACE)
        dataset = dataset.get_dataset(dataset_type=DatasetType.VAL)
        for row in dataset.take(3):
            self.assertIsNotNone(row[0])
            self.assertIsNotNone(row[1])

    def test_test_iterator(self):
        dataset = HateDataset(self.data_path,
                              tokenizer_name='bert-base-german-cased',
                              tokenizer_type=TokenizerType.HUGGINGFACE)
        dataset = dataset.get_dataset(dataset_type=DatasetType.TEST)
        for row in dataset.take(3):
            self.assertIsNotNone(row[0])
            self.assertIsNotNone(row[1])

    def test_none_tokenizer(self):
        dataset = HateDataset(self.data_path,
                              tokenizer_name=None,
                              tokenizer_type=TokenizerType.NONE)
        dataset = dataset.get_dataset(dataset_type=DatasetType.TRAIN)
        for row in dataset.take(3):
            self.assertIsNotNone(row[0])
            self.assertIsNotNone(row[1])

    def test_token_tokenizer(self):
        dataset = HateDataset(self.data_path,
                              tokenizer_name=None,
                              tokenizer_type=TokenizerType.TOKENS)
        dataset = dataset.get_dataset(dataset_type=DatasetType.TRAIN)
        for row in dataset.take(3):
            self.assertIsNotNone(row[0])
            self.assertIsNotNone(row[1])


if __name__ == '__main__':
    unittest.main()
