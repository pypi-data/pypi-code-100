import tensorflow as tf
import numpy as np

from tqdm import tqdm
from enum import Enum


class ModelType(Enum):
    """
    Enum that specifies what model to use.
    They only differ in the classification heads they use.

    DEFAULT: use default huggingface classification head.
    CNN: use 2D CNN as classification head.
    """
    DEFAULT = 0
    CNN = 1


def huggingface_predict_sample(pred,
                               tokenizer,
                               model,
                               labelencoder,
                               max_length=128):
    tf_batch = tokenizer.encode_plus(pred,
                                     add_special_tokens=True,
                                     max_length=max_length,
                                     return_token_type_ids=True,
                                     return_attention_mask=True,
                                     pad_to_max_length=True,
                                     truncation=True,
                                     return_tensors='tf')
    tf_outputs = model(tf_batch)
    if tf.is_tensor(tf_outputs):
        logits = tf_outputs
    else:
        logits = tf_outputs.logits
    tf_predictions = tf.nn.softmax(logits, axis=-1)
    label = tf.argmax(tf_predictions, axis=1)
    label = label.numpy()
    label = labelencoder.inverse_transform(label)[0]

    return label


def huggingface_predict_batch(batch,
                              tokenizer,
                              model,
                              labelencoder,
                              max_length=128,
                              transform_lbls=True):
    tf_batch = tokenizer.batch_encode_plus(batch,
                                           add_special_tokens=True,
                                           max_length=max_length,
                                           return_token_type_ids=True,
                                           return_attention_mask=True,
                                           pad_to_max_length=True,
                                           truncation=True,
                                           return_tensors='tf')
    tf_outputs = model(tf_batch)
    if tf.is_tensor(tf_outputs):
        logits = tf_outputs
    else:
        logits = tf_outputs.logits
    tf_predictions = tf.nn.softmax(logits, axis=-1)
    label = tf.argmax(tf_predictions, axis=1)
    label = label.numpy()
    if transform_lbls:
        label = labelencoder.inverse_transform(label)

    return label.tolist()


def huggingface_predict_df(df,
                           col_name,
                           tokenizer,
                           model,
                           labelencoder,
                           max_length=128,
                           pred_bs=128,
                           transform_lbls=True):
    """
    Use the model to predict the tags of an entire dataframe.
    """
    # create output dataframe
    dataset = df.copy(deep=True)
    dataset = dataset.reset_index(drop=True)

    # create batches for predicting
    pred_batches = np.split(np.array(dataset.text),
                            np.arange(pred_bs, len(dataset), pred_bs),
                            axis=0)

    # predict each batch and add it to the output dataframe
    for i, batch in tqdm(enumerate(pred_batches), total=len(pred_batches)):
        p_batch = huggingface_predict_batch(batch.tolist(),
                                            tokenizer,
                                            model,
                                            labelencoder,
                                            max_length=max_length,
                                            transform_lbls=transform_lbls)
        dataset.loc[i * pred_bs:((i + 1) * pred_bs) - 1, col_name] = p_batch

    return dataset
