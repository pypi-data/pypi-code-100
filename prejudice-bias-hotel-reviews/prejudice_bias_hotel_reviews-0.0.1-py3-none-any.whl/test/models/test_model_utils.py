import unittest
import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification

from src.dataset.germeval_2018_dataset import GermEval2018Dataset
from src.dataset.utils import TokenizerType, DatasetType
from src.models.roberta_cnn import get_roberta_cnn_model
from src.models.utils import huggingface_predict_sample
from src.models.utils import huggingface_predict_batch


class TestModelUtils(unittest.TestCase):

    def setUp(self):
        self.dataset = GermEval2018Dataset(
            'data/GermEval-2018/',
            tokenizer_name='FabianGroeger/HotelBERT',
            tokenizer_type=TokenizerType.HUGGINGFACE,
            model_path='models/')
        # here we use the validation set to fit the model on,
        # only so that the training process is faster then when using
        # the entire training set
        self.train_data = self.dataset.get_dataset(DatasetType.VAL)
        # reset the keras session
        tf.keras.backend.clear_session()

    def test_predict_sample_custom_model(self):
        model = get_roberta_cnn_model('FabianGroeger/HotelBERT')
        acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        model.compile(optimizer='adam', loss=loss, metrics=[acc])

        pred_label = huggingface_predict_sample('Das ist ein Test',
                                                self.dataset.tokenizer,
                                                model,
                                                self.dataset.labelencoder)
        self.assertIsNotNone(pred_label)

    def test_predict_sample_hf_model(self):
        model = TFAutoModelForSequenceClassification.from_pretrained('FabianGroeger/HotelBERT')
        acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        model.compile(optimizer='adam', loss=loss, metrics=[acc])

        pred_label = huggingface_predict_sample('Das ist ein Test',
                                                self.dataset.tokenizer,
                                                model,
                                                self.dataset.labelencoder)
        self.assertIsNotNone(pred_label)

    def test_predict_batch_custom_model(self):
        model = get_roberta_cnn_model('FabianGroeger/HotelBERT')
        acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        model.compile(optimizer='adam', loss=loss, metrics=[acc])

        pred_label = huggingface_predict_batch(
            ['Das ist ein Test', 'Weiterer Test'], self.dataset.tokenizer,
            model, self.dataset.labelencoder)
        self.assertIsNotNone(pred_label)

    def test_predict_batch_hf_model(self):
        model = TFAutoModelForSequenceClassification.from_pretrained('FabianGroeger/HotelBERT')
        acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        model.compile(optimizer='adam', loss=loss, metrics=[acc])

        pred_label = huggingface_predict_batch(
            ['Das ist ein Test', 'Weiterer Test'], self.dataset.tokenizer,
            model, self.dataset.labelencoder)
        self.assertIsNotNone(pred_label)


if __name__ == '__main__':
    unittest.main()
