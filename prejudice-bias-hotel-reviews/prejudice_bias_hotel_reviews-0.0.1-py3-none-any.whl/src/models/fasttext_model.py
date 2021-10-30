import codecs
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


class FastTextModel:

    EMBEDDING_MODULE_PATH = 'models/text_module'

    @staticmethod
    def load_embedding_matrix(path: str, max_features: int, embed_size: int,
                              maxlen: int, word_index):
        # read the embedding file and create an index file
        embeddings_index = {}
        f = codecs.open(path, encoding='utf-8')
        for line in f:
            values = line.rstrip().rsplit(' ')
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()

        # create the embedding matrix
        nb_words = min(max_features, len(word_index) + 1)
        embedding_matrix = np.zeros((nb_words, embed_size))
        for word, i in word_index.items():
            if i >= nb_words:
                continue
            embedding_vector = embeddings_index.get(word)
            if (embedding_vector is not None) and len(embedding_vector) > 0:
                # words not found in embedding index will be all-zeros.
                embedding_matrix[i] = embedding_vector

        embedding_layer = tf.keras.layers.Embedding(nb_words,
                                                    embed_size,
                                                    input_length=maxlen,
                                                    weights=[embedding_matrix],
                                                    trainable=False)

        return embedding_layer

    @staticmethod
    def create_linear(layers: list = [64, 16], **kwargs):
        embedding_layer = hub.KerasLayer(FastTextModel.EMBEDDING_MODULE_PATH,
                                         trainable=False)
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Input(shape=[], dtype=tf.string))
        model.add(embedding_layer)
        for layer in layers:
            model.add(tf.keras.layers.Dense(layer, activation='relu'))

        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        return model

    @staticmethod
    def create_lstm(layers: list = [16, 4],
                    embedding_type=None,
                    max_features=100000,
                    embed_size=300,
                    maxlen=100,
                    word_index=None,
                    dropout=0,
                    recurrent_dropout=0,
                    regularizer_weight=0.0,
                    **kwargs):
        if embedding_type == 'fasttext':
            embedding_layer = FastTextModel.load_embedding_matrix(
                'notebooks/cc.de.300.vec',
                max_features=max_features,
                embed_size=embed_size,
                maxlen=maxlen,
                word_index=word_index)
        else:
            embedding_layer = tf.keras.layers.Embedding(max_features,
                                                        embed_size,
                                                        input_length=maxlen)

        model = tf.keras.Sequential()
        model.add(embedding_layer)
        for i, layer in enumerate(layers):
            if i == len(layers) - 1:
                model.add(
                    tf.keras.layers.LSTM(
                        layer,
                        dropout=dropout,
                        recurrent_dropout=recurrent_dropout,
                        kernel_regularizer=tf.keras.regularizers.l2(
                            regularizer_weight)))
            else:
                model.add(
                    tf.keras.layers.LSTM(
                        layer,
                        dropout=dropout,
                        recurrent_dropout=recurrent_dropout,
                        kernel_regularizer=tf.keras.regularizers.l2(
                            regularizer_weight),
                        return_sequences=True))

        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        return model

    @staticmethod
    def create_bilstm(layers: list = [16, 4],
                      embedding_type=None,
                      max_features=100000,
                      embed_size=300,
                      maxlen=100,
                      word_index=None,
                      dropout=0.0,
                      recurrent_dropout=0.0,
                      regularizer_weight=0.0,
                      **kwargs):
        if embedding_type == 'fasttext':
            embedding_layer = FastTextModel.load_embedding_matrix(
                'notebooks/cc.de.300.vec',
                max_features=max_features,
                embed_size=embed_size,
                maxlen=maxlen,
                word_index=word_index)
        else:
            embedding_layer = tf.keras.layers.Embedding(max_features,
                                                        embed_size,
                                                        input_length=maxlen)

        model = tf.keras.Sequential()
        model.add(embedding_layer)
        for i, layer in enumerate(layers):
            if i == len(layers) - 1:
                model.add(
                    tf.keras.layers.Bidirectional(
                        tf.keras.layers.LSTM(
                            layer,
                            dropout=dropout,
                            recurrent_dropout=recurrent_dropout,
                            kernel_regularizer=tf.keras.regularizers.l2(
                                regularizer_weight))))
            else:
                model.add(
                    tf.keras.layers.Bidirectional(
                        tf.keras.layers.LSTM(
                            layer,
                            dropout=dropout,
                            recurrent_dropout=recurrent_dropout,
                            kernel_regularizer=tf.keras.regularizers.l2(
                                regularizer_weight),
                            return_sequences=True)))

        model.add(tf.keras.layers.Dense(64, activation='relu'))
        model.add(tf.keras.layers.Dense(32, activation='relu'))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

        return model
