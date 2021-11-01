# Simple neural net implementing a GLM

import actuarial_loss_functions
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf


def basic_glm_model(num_features=None,
                    name=None,
                    kernel_regularizer=None,
                    optimizer=None,
                    loss=None,
                    exposure=False,
                    learning_rate_decay=True,
                    decay_steps=10000,
                    ):
    if optimizer is None:
        if learning_rate_decay:
            lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
                initial_learning_rate=0.001,
                decay_steps=decay_steps,
                decay_rate=0.95,
            )
        else:
            lr_schedule = .001
        optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

    metrics = []
    if (loss == 'Poisson'):
        # "output_dim" = "how many numbers do we predict?"
        output_dim = 1
        if not exposure:
            loss = actuarial_loss_functions.Poisson_link
        else:
            loss = actuarial_loss_functions.Poisson_link_with_exposure
            metrics += [
                actuarial_loss_functions.mse_poisson_exposure,
                actuarial_loss_functions.gini_poisson_exposure]
    elif loss == 'Negative Binomial':
        output_dim = 2
        if not exposure:
            loss = actuarial_loss_functions.Negative_binomial_link
        else:
            loss = actuarial_loss_functions.Negative_binomial_link_with_exposure  # noqa: E501

    model = Sequential()
    # Note: bias=False, i.e., no constant term; if you want a constant term,
    # you need to explicit add an "all-ones" feature.
    model.add(Dense(
        output_dim,
        input_dim=num_features,
        activation='linear',
        kernel_regularizer=kernel_regularizer,
        use_bias=False,
        name='betas',
    ))

    model.compile(loss=loss, optimizer=optimizer, metrics=metrics)
    return(model)


def build_and_train_basic_glm(
    loss=None,
    model=None,
    min_stopping_delta=0.001,
    x_train=None, y_train=None,
    x_valid=None, y_valid=None,
    x_test=None, y_test=None,
    batch_size=None,
    epochs=400,
    verbose=1,
    exposure=False,
    learning_rate_decay=False,
    random_seed=None,
):
    num_features = np.shape(x_train)[1]

    if random_seed is not None:
        tf.random.set_seed(random_seed)

    if batch_size is None:
        # If output counts are, e.g., mostly zero, try to make batch_size
        # larger.
        if len(np.shape(y_train)) == 1:
            principal_output = y_train
        elif len(np.shape(y_train)) == 2:
            principal_output = np.reshape(y_train[:, 0], (-1,))
        else:
            raise ValueError('Wrong y_test shape: %s' % (np.shape(y_train)))

        median = np.median(principal_output)
        common_count = np.sum(principal_output == median)
        common_fraction = common_count / len(principal_output)
        if common_fraction < .9 or common_fraction == 1.0:
            batch_size = 256
        else:
            batch_size = int(2 / (1-common_fraction))
        max_batch_size = 16 * 1024
        batch_size = min(batch_size, max_batch_size)
        print('Setting batch_size=%d' % batch_size)

    if model is None:
        model = basic_glm_model(
            loss=loss, num_features=num_features, exposure=exposure,
            learning_rate_decay=learning_rate_decay,
            decay_steps=int(len(y_train)/batch_size)
        )

    callbacks = []
    if (x_valid is not None) and (y_valid is not None):
        validation_data = (x_valid, y_valid)
        if min_stopping_delta > 0:
            callbacks += [keras.callbacks.EarlyStopping(
                monitor='val_loss',
                min_delta=min_stopping_delta,
                patience=5,
            )]
    else:
        validation_data = None

    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=epochs,
                        verbose=verbose,
                        validation_data=validation_data,
                        callbacks=callbacks,
                        )
    if (x_valid is not None) and (y_valid is not None):
        val_score = model.evaluate(x_valid, y_valid, verbose=0)
    else:
        val_score = None

    if (x_test is not None) and (y_test is not None):
        score = model.evaluate(x_test, y_test, verbose=0)
    else:
        score = None

    betas = model.get_layer(name='betas').get_weights()[0]

    results = {}
    results['model'] = model
    results['score'] = score
    results['val_score'] = val_score
    results['history'] = history
    results['betas'] = betas
    results['batch_size'] = batch_size

    return(results)
