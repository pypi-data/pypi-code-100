import unittest
import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification

from src.dataset.germeval_2018_dataset import GermEval2018Dataset
from src.dataset.utils import TokenizerType, DatasetType
from src.models.roberta_cnn import get_roberta_cnn_model
from src.models.utils import huggingface_predict_sample


class TestRoBERTaCNNModel(unittest.TestCase):

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

    def test_compile(self):
        roberta_cnn = get_roberta_cnn_model('FabianGroeger/HotelBERT')
        roberta_cnn.compile(optimizer='adam',
                            loss='binary_crossentropy',
                            metrics=['accuracy'])
        roberta_cnn.summary()

        self.assertIsNotNone(roberta_cnn)

    def test_fit(self):
        roberta_cnn = get_roberta_cnn_model('FabianGroeger/HotelBERT')
        acc = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        roberta_cnn.compile(optimizer='adam', loss=loss, metrics=[acc])
        roberta_cnn.fit(self.train_data, epochs=1)


if __name__ == '__main__':
    unittest.main()
