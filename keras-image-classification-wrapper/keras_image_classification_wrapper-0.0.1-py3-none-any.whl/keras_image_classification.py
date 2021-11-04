__desc__ = "A thin wrapper around keras image classification applications."
__version__ = "0.0.1"

import io
from typing import Tuple, Union

import numpy as np
import PIL as pillow
from tensorflow.keras.applications import *
from tensorflow.keras.preprocessing.image import img_to_array

XCEPTION = "xception"
VGG16 = "vgg16"
VGG19 = "vgg19"
RESNET50 = "resnet50"
RESNET101 = "resnet101"
RESNET152 = "resnet152"
RESNET50V2 = "resnet50v2"
RESNET101V2 = "resnet101v2"
RESNET152V2 = "resnet152v2"
INCEPTIONV3 = "inceptionv3"
INCEPTIONRESNETV2 = "inceptionresnetv2"
MOBILENET = "mobilenet"
MOBILENETV2 = "mobilenetv2"
DENSENET121 = "densenet121"
DENSENET169 = "densenet169"
DENSENET201 = "densenet201"
NASNETMOBILE = "nasnetmobile"
NASNETLARGE = "nasnetlarge"
EFFICIENTNETB0 = "efficientnetb0"
EFFICIENTNETB1 = "efficientnetb1"
EFFICIENTNETB2 = "efficientnetb2"
EFFICIENTNETB3 = "efficientnetb3"
EFFICIENTNETB4 = "efficientnetb4"
EFFICIENTNETB5 = "efficientnetb5"
EFFICIENTNETB6 = "efficientnetb6"
EFFICIENTNETB7 = "efficientnetb7"

MODULES = {
    XCEPTION: xception,
    VGG16: vgg16,
    VGG19: vgg19,
    RESNET50: resnet50,
    RESNET101: resnet,
    RESNET152: resnet,
    RESNET50V2: resnet_v2,
    RESNET101V2: resnet_v2,
    RESNET152V2: resnet_v2,
    INCEPTIONV3: inception_v3,
    INCEPTIONRESNETV2: inception_resnet_v2,
    MOBILENET: mobilenet,
    MOBILENETV2: mobilenet_v2,
    DENSENET121: densenet,
    DENSENET169: densenet,
    DENSENET201: densenet,
    NASNETMOBILE: nasnet,
    NASNETLARGE: nasnet,
    EFFICIENTNETB0: efficientnet,
    EFFICIENTNETB1: efficientnet,
    EFFICIENTNETB2: efficientnet,
    EFFICIENTNETB3: efficientnet,
    EFFICIENTNETB4: efficientnet,
    EFFICIENTNETB5: efficientnet,
    EFFICIENTNETB6: efficientnet,
    EFFICIENTNETB7: efficientnet,
}

MODELS = {
    XCEPTION: Xception,
    VGG16: VGG16,
    VGG19: VGG19,
    RESNET50: ResNet50,
    RESNET101: ResNet101,
    RESNET152: ResNet152,
    RESNET50V2: ResNet50V2,
    RESNET101V2: ResNet101V2,
    RESNET152V2: ResNet152V2,
    INCEPTIONV3: InceptionV3,
    INCEPTIONRESNETV2: InceptionResNetV2,
    MOBILENET: MobileNet,
    MOBILENETV2: MobileNetV2,
    DENSENET121: DenseNet121,
    DENSENET169: DenseNet169,
    DENSENET201: DenseNet201,
    NASNETMOBILE: NASNetMobile,
    NASNETLARGE: NASNetLarge,
    EFFICIENTNETB0: EfficientNetB0,
    EFFICIENTNETB1: EfficientNetB1,
    EFFICIENTNETB2: EfficientNetB2,
    EFFICIENTNETB3: EfficientNetB3,
    EFFICIENTNETB4: EfficientNetB4,
    EFFICIENTNETB5: EfficientNetB5,
    EFFICIENTNETB6: EfficientNetB6,
    EFFICIENTNETB7: EfficientNetB7,
}

_loaded_models = {}


def load_model(model: str) -> None:
    global _loaded_models
    if model not in _loaded_models:
        _loaded_models[model] = MODELS[model](
            include_top=True, weights="imagenet", input_tensor=None, input_shape=None
        )


def get_model_target_size(model: str) -> Tuple[int, int]:
    if model in ("inceptionv3", "xception", "inceptionresnetv2"):
        return (299, 299)
    else:
        return (224, 224)


def preprocess_image(image: pillow.Image.Image, model: str) -> np.ndarray:
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(get_model_target_size(model))
    return MODULES[model].preprocess_input(np.expand_dims(img_to_array(image), axis=0))


def classify(
    image: Union[str, bytes, pillow.Image.Image],
    results: int = 3,
    model: str = INCEPTIONV3,
) -> tuple:
    assert results <= 5, "Keras applications don't give more than five results."

    if not isinstance(image, pillow.Image.Image):
        if isinstance(image, str):
            to_open = image
        else:
            to_open = io.BytesIO(image)
        image = pillow.Image.open(to_open)
    preprocessed_image = preprocess_image(image, model)

    load_model(model)
    model_object = _loaded_models[model]
    predictions = model_object.predict(preprocessed_image)
    prediction_results = MODULES[model].decode_predictions(predictions)[0]

    return tuple(
        {"label": label, "probability": float(probability)}
        for imagenet_id, label, probability in prediction_results[:results]
    )
