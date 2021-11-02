from enum import Enum

class ModelFormat(Enum):
    NON_SPECIFIED = 0
    UNKNOWN = 1

    PT_NN_MODULE = 11
    TF_KERAS_MODEL = 12
    KERAS_MODEL = 13

    H5 = 21
    SAVED_MODEL = 22
    PB = 23

    PTH = 31
    ONNX = 32


TF_MODEL_FORMATS = [ModelFormat.TF_KERAS_MODEL,
                    ModelFormat.KERAS_MODEL,
                    ModelFormat.H5,
                    ModelFormat.SAVED_MODEL,
                    ModelFormat.PB]


class ModelDataType(Enum):
    NON_SPECIFIED = 0
    FP32 = 1
    FP16 = 2

    BF16 = 11

    INT8 = 21
