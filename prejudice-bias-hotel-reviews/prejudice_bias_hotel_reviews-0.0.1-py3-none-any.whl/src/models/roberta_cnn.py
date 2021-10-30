import tensorflow as tf
from transformers import TFRobertaModel


class RoBERTaCNN(tf.keras.Model):
    def __init__(self, model_name, dropout=0.3, weight_regularization=0.001):
        super(RoBERTaCNN, self).__init__()
        # define the encoder
        self.encoder = TFRobertaModel.from_pretrained(
            model_name, output_hidden_states=True)

        # classification head
        self.conv = tf.keras.layers.Conv2D(
            filters=7,
            kernel_size=(3, 768),
            padding='valid',
            activation='relu',
            kernel_regularizer=tf.keras.regularizers.l2(weight_regularization))
        self.dropout = tf.keras.layers.Dropout(dropout)
        self.flatten = tf.keras.layers.Flatten()
        self.out_proj = tf.keras.layers.Dense(2)

    def call(self, inputs):
        # get the inputs
        input_ids = inputs['input_ids']
        token_type_ids = inputs['token_type_ids']
        attention_mask = inputs['attention_mask']

        # pass through the roberta encoder
        embedding = self.encoder(input_ids,
                                 token_type_ids=token_type_ids,
                                 attention_mask=attention_mask)
        # get the hidden states from all the encoder blocks
        hidden_states = tf.stack(embedding.hidden_states)
        # reshape to fit the shape for conv
        hidden_states = tf.einsum('ij...->j...i', hidden_states)

        # classification head
        x = self.dropout(hidden_states)
        x = self.conv(x)
        x = self.dropout(x)
        x = self.flatten(x)
        x = self.dropout(x)
        x = self.out_proj(x)

        return x


def get_roberta_cnn_model(model_name,
                          dropout=0.3,
                          weight_regularization=0.001,
                          max_len=128):
    # create instance of model
    roberta_cnn = RoBERTaCNN(model_name,
                             dropout=dropout,
                             weight_regularization=weight_regularization)

    # define the inputs
    input_ids = tf.keras.layers.Input(shape=(max_len, ), dtype=tf.int32)
    token_type_ids = tf.keras.layers.Input(shape=(max_len, ), dtype=tf.int32)
    attention_mask = tf.keras.layers.Input(shape=(max_len, ), dtype=tf.int32)

    # build the model with the correct input shapes
    roberta_cnn({
        'input_ids': input_ids,
        'token_type_ids': token_type_ids,
        'attention_mask': attention_mask
    })

    return roberta_cnn
