"""Common model generation functions for tests."""
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from tensorflow.keras.models import (
        Model,
    )

# pylint: disable=import-outside-toplevel


def setup_keras_model_functional(spatial_dims: Tuple[int, int] = (128, 128)) -> "Model":
    """Returns a Keras model.

    Generates a simple Keras model using the functional API with three convolutional layers and an additional
    InputLayer as input node.

    Args:
        spatial_dims: Specifies the spatial dimensions of the input and output node.
    """
    from tensorflow.keras.layers import (
        Conv2D,
        Input,
    )
    from tensorflow.keras.models import (
        Model,
    )

    inputs = Input(shape=spatial_dims + (3,), name="first_input_tensor")
    model = Conv2D(3, 1, activation="relu", padding="same")(inputs)
    model = Conv2D(3, 1, activation="relu", padding="same")(model)
    model = Conv2D(3, 1, activation="softmax", padding="same")(model)
    model = Model(inputs=inputs, outputs=model)
    model.compile(optimizer="adam", loss="categorical_crossentropy")
    return model
