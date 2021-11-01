# Loss functions and metrics corresponding to some popular actuarial
# statistical models.

# Broadly speaking, these loss functions compute the negative log-likelihood
# of some distributions of interest (Poisson, Negative Binomial).  In typical
# fashion, we suppress terms that are constant given the data, since they
# disappear when we take a gradient with respect to the parameters

# We also allow an exposure term, i.e., we are estimating the rate of a
# process, but each observation may have a different (known) amount of
# observed time.

# Except for OLS, GLMs usually do not predict a distribution's parameters
# directly; instead, they predict some "link" function of the parameters.  For
# instance, instead of predicting the "lambda" in a Poisson distribution,
# they predict log(lambda).  The link function is chosen so that the 
# resulting range covers the reals.  Neural nets benefit from this link
# function the same way that GLMs do. Note that to use the output, the 
# inverse link function should be applied.

# Finally, the link function can sometimes produce very large values.  Once
# the neural net is producing moderately decent estimates, this problem is
# minor, but after a random initialization it can be easy for training to
# produce infinite values.  We provide numerically stable versions of these
# loss functions by flattening extreme values.  This corresponds to some
# assumption about the typical (exposure-corrected) rate, namely that we
# should not see more than (say) a thousand events.

import tensorflow as tf
from tensorflow.python.framework.ops import convert_to_tensor
from tensorflow.python.ops.math_ops import cast as tf_cast
from tensorflow.math import minimum, log, lgamma, exp, sigmoid, square


def one_dim(t):
    # Convert tensors of shape (N,1) to (N).
    # Tensors of shape (N) remain unchanged.
    return(tf.reshape(t, (-1,)))


def Poisson_link(y_true, y_pred):
    # "y_pred" predicts the Poisson log(lambda), since "log" is the standard
    # Poisson Regression link function
    y_log_lambda = one_dim(convert_to_tensor(y_pred))
    num_events = one_dim(tf_cast(y_true, y_pred.dtype))

    # Numerically stabilize.  Note: e^10 = 22,026
    max_log_lambda = tf.constant(10.0)
    y_log_lambda_bounded = minimum(y_log_lambda, max_log_lambda)
    excess = tf.nn.relu(y_log_lambda - y_log_lambda_bounded)
    # Make derivative of excess region roughly consistent
    out_of_bound_slope = exp(max_log_lambda)
    out_of_bound_penalty = out_of_bound_slope * excess

    neg_log_likelihood = -(
        num_events*y_log_lambda_bounded - exp(y_log_lambda_bounded))
    neg_log_likelihood += out_of_bound_penalty
    return neg_log_likelihood


def Poisson_link_with_exposure(y_true, y_pred):
    # "y_pred" predicts log(lambda).  "y_true" is a pair of values,
    # consisting of <N, T>, where "N" is the number of events and "T" is the
    # length of exposure.  (So, for the same lambda, if you have twice the
    # exposure, you'd expect to see about twice the events.)  In the case that
    # T=1 for all observations, this loss function reduces to the Poisson()
    # above.
    y_log_lambda = one_dim(convert_to_tensor(y_pred))
    y_observations = tf_cast(y_true, y_pred.dtype)
    num_events = one_dim(y_observations[:, 0])
    exposure = one_dim(y_observations[:, 1])

    # Rescale Lambda to account for exposure
    y_log_lambda = y_log_lambda + log(exposure)

    # Numerically stabilize.  Note: e^10 = 22,026
    max_log_lambda = tf.constant(10.0)
    y_log_lambda_bounded = minimum(y_log_lambda, max_log_lambda)
    excess = tf.nn.relu(y_log_lambda - y_log_lambda_bounded)
    # Make derivative of excess region roughly consistent
    out_of_bound_slope = exp(max_log_lambda)
    out_of_bound_penalty = out_of_bound_slope * excess

    neg_log_likelihood = -(
        num_events*y_log_lambda_bounded - exp(y_log_lambda_bounded))
    neg_log_likelihood += out_of_bound_penalty
    return neg_log_likelihood


def Negative_binomial_link(y_true, y_pred):
    # There are multiple possible link functions for negative binomial
    # regression; we present one here.
    num_events = one_dim(tf_cast(y_true, y_pred.dtype))

    y_pred = convert_to_tensor(y_pred)

    r_link = one_dim(y_pred[:, 0])

    # Numerically stabilize.  Note: e^10 = 22,026
    max_r_link = tf.constant(10.0)
    r_link_bounded = minimum(r_link, max_r_link)
    excess = tf.nn.relu(r_link - r_link_bounded)
    # Make derivative of excess region roughly consistent
    out_of_bound_slope = max_r_link * exp(max_r_link)
    out_of_bound_penalty = out_of_bound_slope * excess

    # (Link function:) Convert from R to R^+
    r_bounded = exp(r_link_bounded)

    p_link = one_dim(y_pred[:, 1])
    # (Link function:) Convert from R to [0,1]
    p = sigmoid(p_link)

    neg_log_likelihood = -(
        lgamma(num_events+r_bounded)
        + num_events*log(1-p)
        - lgamma(r_bounded)
        + r_bounded*log(p))
    neg_log_likelihood += out_of_bound_penalty
    return neg_log_likelihood


def Negative_binomial_link_with_exposure(y_true, y_pred):
    # To handle exposure, we need to interpret our original
    # distribution as the count function of some underlying
    # stochastic process.  For a Poisson distribution, this
    # is easy; we use the Poisson process, with i.i.d.
    # exponentially distributed interarrival times.

    # The situation is not so clear when we have a negative
    # binomial distribution for the count, because there
    # are multiple stochastic processes we can choose from.

    # In practical terms, given an NB(r, p) distribution,
    # if we wish to scale the rate by alpha, we can either
    # treat the rate as r or as (1-p)/p.  If we wish
    # to rescale exposure by alpha, then, we can either do
    #    r  =>  alpha*r
    # or
    #    p  =>  p / [p + alpha*(1-p)]
    # The former situation corresponds to a Negative Binomial
    # Levy Process, which has a few nice theoretical
    # properties, so we choose to do that.
    y_observations = tf_cast(y_true, y_pred.dtype)
    num_events = one_dim(y_observations[:, 0])
    exposure = one_dim(y_observations[:, 1])

    y_pred = convert_to_tensor(y_pred)

    # Account for exposure
    r_link = one_dim(y_pred[:, 0])
    r_link = r_link + log(exposure)

    # Numerically stabilize.  Note: e^10 = 22,026
    max_r_link = tf.constant(10.0)
    r_link_bounded = minimum(r_link, max_r_link)
    excess = tf.nn.relu(r_link - r_link_bounded)
    # Make derivative of excess region roughly consistent
    out_of_bound_slope = max_r_link * exp(max_r_link)
    out_of_bound_penalty = out_of_bound_slope * excess

    # (Link function:) Convert from R to R^+
    r_bounded = exp(r_link_bounded)

    p_link = one_dim(y_pred[:, 1])
    # (Link function:) Convert from R to [0,1]
    p = sigmoid(p_link)

    neg_log_likelihood = -(
        lgamma(num_events+r_bounded)
        + num_events*log(1-p)
        - lgamma(r_bounded)
        + r_bounded*log(p))
    neg_log_likelihood += out_of_bound_penalty
    return neg_log_likelihood

###############################################
# Metrics
# 
# The standard TensorFlow metric functions don't quite work out of the box;
# we provide a few modified versions here for Poisson regression with exposure.


def mse_poisson_exposure(y_true, y_pred):
    y_observations = tf_cast(y_true, y_pred.dtype)
    num_events = one_dim(y_observations[:, 0])
    exposure = one_dim(y_observations[:, 1])
    y_pred = one_dim(y_pred)

    exp_pred = exp(y_pred)
    val = square(exp_pred * exposure - num_events)
    return(val)


def gini_poisson_exposure(y_true, y_pred):
    y_observations = tf_cast(y_true, y_pred.dtype)
    num_events = one_dim(y_observations[:, 0])
    exposure = one_dim(y_observations[:, 1])
    y_pred = one_dim(y_pred)

    total_events = tf.math.reduce_sum(num_events)
    # If no events are present, it's not exactly clear what
    # to do; we return Gini=0, which is arguably correct.
    if total_events == 0:
        return(tf.constant(0.0))
    # Correct for exposure
    y_pred += log(exposure)
    sort_order = tf.argsort(y_pred, direction='DESCENDING')
    fraction_events_sorted = tf.gather(
        num_events / total_events, sort_order)
    cumulative_fractions = tf.math.cumsum(fraction_events_sorted)
    fraction_under_curve = tf.math.reduce_mean(cumulative_fractions)
    gini_coefficient = 2 * (fraction_under_curve - 0.5)
    return(gini_coefficient)
