from enum import Enum, IntEnum, Flag, IntFlag, auto, unique
from collections import OrderedDict
from io import TextIOWrapper

import numpy as np
import torch as th
from torch.nn import Parameter
from tables import File
from PySide2 import QtCore
from PySide2.QtCore import QLocale, QPoint, QPointF, QSize, QSizeF, QRect, QRectF, QMutex
from PySide2.QtGui import QCursor, QColor, QFont, QKeySequence
from PySide2.QtWidgets import QSizePolicy
from tables import Group, CArray

from sknrf.widget.propertybrowser.view.enums import DISPLAY, PropertyID
from sknrf.app.dataviewer.model.dataset import WCArray
from sknrf.utilities.numeric import Info, Domain


type_id_map = OrderedDict((
    (bool, PropertyID.BOOL),
    (IntFlag, PropertyID.FLAG),
    (Flag, PropertyID.FLAG),
    (IntEnum, PropertyID.ENUM),
    (Enum, PropertyID.ENUM),
    (int, PropertyID.INT_EDIT),
    (np.int, PropertyID.INT_EDIT),
    (np.int16, PropertyID.INT_EDIT),
    (np.int32, PropertyID.INT_EDIT),
    (np.int64, PropertyID.INT_EDIT),
    (float, PropertyID.DOUBLE_EDIT),
    (np.float16, PropertyID.DOUBLE_EDIT),
    (np.float32, PropertyID.DOUBLE_EDIT),
    (np.float64, PropertyID.DOUBLE_EDIT),
    (complex, PropertyID.COMPLEX_EDIT),
    (np.complex64, PropertyID.COMPLEX_EDIT),
    (np.complex128, PropertyID.COMPLEX_EDIT),
    (WCArray, PropertyID.TF_FILE_EDIT),
    (str, PropertyID.STRING),
    (File, PropertyID.TB_FILE),
    (TextIOWrapper, PropertyID.FILE),
    (QLocale, PropertyID.LOCALE),
    (QPoint, PropertyID.POINT),
    (QPointF, PropertyID.POINTF),
    (QSize, PropertyID.SIZE),
    (QSizeF, PropertyID.SIZEF),
    (QRect, PropertyID.RECT),
    (QRectF, PropertyID.RECTF),
    (QCursor, PropertyID.CURSOR),
    (QColor, PropertyID.COLOR),
    (QFont, PropertyID.FONT),
    (QKeySequence, PropertyID.KEY_SEQUENCE),
    (QSizePolicy, PropertyID.SIZE_POLICY),
    (th.Tensor, PropertyID.LIST),
    (Parameter, PropertyID.LIST),
    (np.ndarray, PropertyID.LIST),
    (list, PropertyID.LIST),
    (tuple, PropertyID.TUPLE),
    (object, PropertyID.PY_OBJECT)
))

domain_id_map = OrderedDict((
    (Domain.TH, PropertyID.LIST),
    (Domain.TF, PropertyID.TF_EDIT),
    (Domain.FF, PropertyID.LIST),
    (Domain.FT, PropertyID.LIST),
    (Domain.TT, PropertyID.LIST),
))

unsupported_types = (QMutex, QtCore.Signal, QtCore.QMetaObject, Info)


def get_attr(model, attribute):
    attribute = int(attribute[1:-1]) if isinstance(model, (list, tuple)) else attribute
    if isinstance(model, Group):  # Database
        return model._f_get_child(attribute)
    elif hasattr(model, "__getitem__"):  # Sequence
        return model.__getitem__(attribute)
    else:  # Object
        return getattr(model, attribute)


def set_attr(model, attribute, value):
    attribute = int(attribute[1:-1]) if isinstance(model, (list, tuple)) else attribute
    if isinstance(model, Group): # Database
        model._f_set_child(attribute, value)
    elif hasattr(model, "__getitem__"):  # Sequence
        model.__setitem__(attribute, value)
    else:  # Object
        setattr(model, attribute, value)


def get_attr_info(model, attribute):
    try:
        info = model.info[attribute]
    except AttributeError:
        ResourceWarning("Attempting to get properties of object type: %s, which does not include Attribute Info"
                        % (type(model),))
        return Info("untitled", write=True)
    except KeyError:
        ResourceWarning("Attempting to get property %s of object type: %s, which does not include Attribute Info"
                        % (attribute, type(model)))
        return Info("untitled", write=True)
    else:
        return info


def model_generator(model, display=DISPLAY.READ):
    # Create a generator based on the model

    def is_check(display_, attribute_, attribute_info_, default_info_):
        return not attribute_.startswith("_") and attribute_info_.get(attribute_, default_info_).check \
            if display_ & DISPLAY.CHECK else False

    def is_public(display_, attribute_, attribute_info_, default_info_):
        return not attribute_.startswith("_") and attribute_info_.get(attribute_, default_info_).read \
            if display_ & DISPLAY.PUBLIC else False

    def is_read(display_, attribute_, attribute_info_, default_info_):
        return attribute_info_.get(attribute_, default_info_).read \
            if display_ & DISPLAY.READ else False

    default_info = Info("???", write=True, check=True)
    if isinstance(model, Group):
        dict_, attribute_info = model._v_children, {}
    elif isinstance(model, dict):
        dict_, attribute_info = model, {}
    else:  # object
        if hasattr(model, "info"):
            default_info = Info("???", read=False, write=False, check=False)
            dict_, attribute_info = model.info, model.info
        else:
            dict_, attribute_info = model.__dict__, {}
    generator = (k for k in dict_.keys()
                 if is_check(display, k, attribute_info, default_info)
                 or is_public(display, k, attribute_info, default_info)
                 or is_read(display, k, attribute_info, default_info))
    return generator
