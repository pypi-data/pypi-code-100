import tensorflow as tf


def recall_score(y_true, y_pred):
    true_positives = tf.math.reduce_sum(tf.math.round(tf.clip_by_value(y_true * y_pred, 0, 1)))
    possible_positives = tf.math.reduce_sum(tf.math.round(tf.clip_by_value(y_true, 0, 1)))
    recall = true_positives / (possible_positives + tf.keras.backend.epsilon())

    return recall


def precision_score(y_true, y_pred):
    true_positives = tf.math.reduce_sum(tf.math.round(tf.clip_by_value(y_true * y_pred, 0, 1)))
    predicted_positives = tf.math.reduce_sum(tf.math.round(tf.clip_by_value(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + tf.keras.backend.epsilon())

    return precision


def f1_score(y_true, y_pred, average=None):

    def _calc_f_score(y_true, y_pred):
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)

        return 2*((precision*recall)/(precision+recall+tf.keras.backend.epsilon()))

    if average is None:
        return _calc_f_score(y_true, y_pred)
    elif average == 'macro':
        f1_pos = _calc_f_score(y_true, y_pred)
        f1_neg = _calc_f_score(1 - y_true, 1 - y_pred)
        f1_macro = tf.reduce_mean([f1_pos, f1_neg])
        return f1_macro


def f1_macro_score(y_true, y_pred):
    f1_pos = f1_score(y_true, y_pred)
    f1_neg = f1_score(1 - y_true, 1 - y_pred)
    f1_macro = tf.reduce_mean([f1_pos, f1_neg])
    return f1_macro
