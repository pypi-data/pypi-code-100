from enum import Enum

import torch as th
import numpy as np
from numpy.linalg import norm
from statsmodels.tools import eval_measures


class ErrorType(Enum):
    Ratio = 1
    Abs = 2
    Rel = 3


def delta_rel(val, ref):
    return th.abs(val - ref)/th.abs(ref)


def delta_abs(val, ref):
    return th.abs(val - ref)


def delta_sub(val, ref):
    return val - ref


def delta_ratio(val, ref):
    return val / ref


def rmse(val, ref, axis=0):
    return eval_measures.rmse(val, ref, axis=axis)


def nrmse(val, ref, axis=0):
    val = np.asanyarray(val)
    ref = np.asanyarray(ref)
    return norm(ref - val, 2, axis=axis)/norm(ref - np.mean(ref, axis=axis, keepdims=True), 2, axis=axis)


def maxabs(val, ref, axis=0):
    return eval_measures.maxabs(val, ref, axis=axis)


def meanabs(val, ref, axis=0):
    return eval_measures.meanabs(val, ref, axis=axis)


def medianabs(val, ref, axis=0):
    return eval_measures.medianabs(val, ref, axis=axis)


def bias(val, ref, axis=0):
    return eval_measures.bias(val, ref, axis=axis)


def medianbias(val, ref, axis=0):
    return eval_measures.medianbias(val, ref, axis=axis)


def vare(val, ref, axis=0):
    return eval_measures.vare(val, ref, axis=axis)


def stde(val, ref, axis=0):
    return eval_measures.stde(val, ref, axis=axis)


def g_t(data, z_s=np.array(50+0j), z_l=np.array(50+0j)):
    if isinstance(data, rf.Network):
        return s2sp(data.s, z_s, z_l)[:, 1, 0]
    elif isinstance(data, DatasetModel):
        values = data.values
        v_1, i_1, _ = baz2viz(values["B_1_1"], values["A_1_1"], 50)
        v_2, i_2, _ = baz2viz(values["B_2_1"], values["A_2_1"], 50)
        _, ap_1, _ = viz2baz(values["V_1_1"], values["I_1_1"], z_s)
        bp_2, _, _ = viz2baz(values["V_2_1"], values["I_2_1"], z_l)
        return bp_2/ap_1


def delta_g_t(ref, val, z_s=np.array(50+0j), z_l=np.array(50+0j), error_type=ErrorType.Ratio):
    ref_gt = G_T(ref, z_s=z_s, z_l=z_l)
    val_gt = G_T(val, z_s=z_s, z_l=z_l).reshape(ref_gt.shape)
    if error_type == ErrorType.Ratio:
        return delta_ratio(ref_gt, val_gt)
    elif error_type == ErrorType.Rel:
        return delta_rel(ref_gt, val_gt)
    else:
        raise NotImplementedError()
