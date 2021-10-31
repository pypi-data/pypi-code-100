# coding=utf-8
"""
This file contains implementations related to the Gumbel Distribution

1.- Continuos aproximations to the Gumbel Max Trick: the implementation was taken from the blog post
 http://blog.evjang.com/2016/11/tutorial-categorical-variational.html. Which is a short presentations of the
 main results of the paper https://arxiv.org/pdf/1611.01144.pdf
 A introductory explanation of the trick can be found in
 -  https://laurent-dinh.github.io/2016/11/22/gumbel-max.html
 -  https://hips.seas.harvard.edu/blog/2013/04/06/the-gumbel-max-trick-for-discrete-distributions/
"""

import tensorflow as tf


def sample_gumbel(shape, eps=1e-20):
    """Sample from Gumbel(0, 1)"""
    #TODO: Use memoization to avoid calls to log
    u = tf.random_uniform(shape, minval=0, maxval=1)
    return -tf.log(-tf.log(u + eps) + eps)


def gumbel_softmax_sample(logits, temperature):
    """ Draw a sample from the Gumbel-Softmax distribution"""
    y = logits + sample_gumbel(tf.shape(logits))
    return tf.nn.softmax(y / temperature)


def gumbel_softmax(logits, temperature, hard=False):
    """Sample from the Gumbel-Softmax distribution and optionally discretize.
    Args:
      options_probabilities: [batch_size, probability] unnormalized log-probs
      temperature: non-negative scalar
      hard: if True, take argmax, but differentiate w.r.t. soft sample y
    Returns:
      [batch_size, n_class] sample from the Gumbel-Softmax distribution.
      If hard=True, then the returned sample will be one-hot, otherwise it will
      be a probabilitiy distribution that sums to 1 across classes
    """
    y = gumbel_softmax_sample(logits, temperature)
    if hard:
        # k = tf.shape(logits)[-1]
        # y_hard = tf.cast(tf.one_hot(tf.argmax(y,1),k), y.dtype)
        y_hard = tf.cast(tf.equal(y, tf.reduce_max(y, 1, keepdims=True)), y.dtype)
        y = tf.stop_gradient(y_hard - y) + y
    return y


def gumbel_softmax_option(logits, temperature, options):
    """Sample from the Gumbel-Softmax distribution and get the option index.
    Args:
      options_probabilities: [batch_size, probability] unnormalized log-probs
      temperature: non-negative scalar
    Returns:
      [batch_size, n_class_id] sample from the Gumbel-Softmax distribution.
    """
    y = gumbel_softmax(logits, temperature, hard=True)
    y = tf.reduce_sum(options * y, 1)
    return y