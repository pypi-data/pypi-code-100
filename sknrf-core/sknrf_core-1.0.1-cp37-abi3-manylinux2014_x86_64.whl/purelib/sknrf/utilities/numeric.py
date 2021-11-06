"""Numeric Input/Output Utility Functions
"""
import sys
import inspect
import collections
import re

import math as mt
import cmath as ct
import torch as th
import numpy as np
from functools import reduce

from sknrf.widget.propertybrowser.view import Scale, Format, PkAvg, Domain

__author__ = 'dtbespal'


scale_map = {
             Scale.T: 'T',
             Scale.G: 'G',
             Scale.M: 'M',
             Scale.K: 'K',
             Scale._: ' ',
             Scale.m: 'm',
             Scale.u: 'u',
             Scale.n: 'n',
             Scale.p: 'p',
             }

scale_value_map = {
             Scale.T: 12,
             Scale.G: 9,
             Scale.M: 6,
             Scale.K: 3,
             Scale._: 0,
             Scale.m: -3,
             Scale.u: -6,
             Scale.n: -9,
             Scale.p: -12,
             }


def camel2underscore(camel):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class bounded_property(property):
    """Emulate PyProperty_Type() in Objects/descrobject.c
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super(bounded_property, self).__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            return
        max_limit = min(obj.info[self.fset.__name__].max, th.finfo(value.dtype).max)
        min_limit = max(obj.info[self.fset.__name__].min, th.finfo(value.dtype).eps)
        value_abs = value.abs()
        value_angle = value.angle()
        if value.is_complex():
            value = th.where(value_abs > max_limit, max_limit*th.exp(1j*value_angle), value)
            value = th.where(value_abs < min_limit, min_limit*th.exp(1j*value_angle), value)
        else:
            value = th.where(value_abs > max_limit, max_limit, value)
            value = th.where(value_abs < min_limit, min_limit, value)
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Info(object):
    """Container of Object Property information.

    Parameters
    ----------
    name : str
        Name of attribute.
    read : bool
        Read permission flag, default is True.
    write : bool
        Write permission flag, default is False.
    check : bool
        Check permission flag, default is False.
    label : str
        Display name of attribute, default is name.
    scale : Scale
        SI scale unit prefix, default is " ".
    precision : int
        number of significant digits, default is 3.
    unit : str
        SI unit, default is "" (unitless).
    pk_avg : PkAvg
        peak/average signal value, default is PkAvg.PK.
    format_ : Format
        complex number format, default is Format.RE_IM.
    step : float
        incremental step, default is 1.
    min_ : float
        minimum limit, default is 0.
    max_ : float
        maximum limit, default is 1e100.
    abs_tol : float
        absolute numerical tolerance, default is sys.float_info.epsilon.
    rel_tol : float
        absolute numerical tolerance, default is sys.float_info.epsilon.
                
    See Also
    --------
        AttributeInfo
                
    """

    def __init__(self, name, read=True, write=False, check=False, label="",
                 scale=Scale._, precision=3, unit="", pk_avg=PkAvg.PK, rms=True, format_=Format.RE,
                 step=1, min_=sys.float_info.epsilon, max_=1.0e100,
                 abs_tol=sys.float_info.epsilon, rel_tol=sys.float_info.epsilon,
                 domain=Domain.TH):

        self.name = name
        self.read = read
        self.write = write
        self.check = check
        self._label = label
        self.format = format_
        self.scale = scale
        self.precision = precision
        self.unit = unit
        self.rms = rms
        self.pk_avg = pk_avg
        self.step = step*10**scale_value_map[self.scale]
        self.min = min_
        self.max = max_
        self.abs_tol = abs_tol
        self.rel_tol = rel_tol
        self.domain = domain

    def __getstate__(self, state={}):
        """ Saves the model state in a dictionary
        :return state:
        """
        state = self.__dict__.copy()
        state["scale"] = int(self.scale)
        state["pk_avg"] = int(self.pk_avg)
        state["format"] = int(self.format)
        state["domain"] = int(self.domain)
        return state

    def __setstate__(self, state):
        """ Loads the model state of a saved model object
        :param state:
        :return:
        """
        for k, v in state.items():
            setattr(self, k, v)
        self.scale = Scale(state["scale"])
        self.pk_avg = PkAvg(state["pk_avg"])
        self.format = Format(state["format"])
        self.domain = Domain(state["domain"])

    @property
    def label(self):
        return self.name if len(self._label) == 0 else self._label

    def copy(self):
        return Info(self.name, self.read, self.write, self.check, self.label,
                    self.scale, self.precision, self.unit, self.pk_avg, self.rms, self.format,
                    self.step, self.min, self.max,
                    self.abs_tol, self.rel_tol)


class AttributeInfo(collections.OrderedDict):
    """OrderedDict of Object Property information.

    See Also
    --------
    Info

    """
    def __int__(self):
        super(AttributeInfo, self).__init__()

    @classmethod
    def initialize(cls, parent, key_order=()):
        if hasattr(parent, "info") and parent.info is not None:
            return parent.info

        self = AttributeInfo()
        attribute_dict = parent.__dict__.copy()
        attribute_dict.update(parent.__class__.__dict__)
        base_classes = parent.__class__.__bases__
        attribute_dict = AttributeInfo.search_base_dict(attribute_dict, base_classes)
        attribute_info = {}
        for k, v in attribute_dict.items():
            if k[0:2] == "__" or inspect.isroutine(v):
                pass
            elif k[0] == "_":
                attribute_info[k] = Info(k, read=False, write=False)
            elif isinstance(v, property):
                attribute_info[k] = Info(k, read=True, write=v.fset is not None)
            else:
                attribute_info[k] = Info(k, read=True, write=True)
        self.update(attribute_info)
        for k in reversed(key_order):
            self.move_to_end(k, last=False)
        return self

    @staticmethod
    def search_base_dict(dict_, base_classes):
        for base_class in base_classes:
            if base_class is object:
                pass
            else:
                dict_.update(base_class.__dict__)
                AttributeInfo.search_base_dict(dict_, base_class.__bases__)
        return dict_


def num2str_re(num, info=Info("untitled", write=True, check=True)):
    return "%0.*g" % (info.precision, num.real)


def num2str_re_im(num, info=Info("untitled", write=True, check=True)):
    return "%0.*g %+0.*gj" % (info.precision, num.real, info.precision, num.imag)


def num2str_lin_deg(num, info=Info("untitled", write=True, check=True)):
    return "%0.*g ∠ %0.*g" % (info.precision, abs(num), info.precision, ct.phase(num) * 180 / ct.pi)


def num2str_log_deg(num, info=Info("untitled", write=True, check=True)):
    return "%0.*g ∠ %0.*g" % (info.precision, 20 * mt.log10(abs(num) * mt.sqrt(10**scale_value_map[info.scale])),
                              info.precision, ct.phase(num) * 180 / ct.pi)


def num2str(num, info=Info("untitled", write=True, check=True)):
    """Converts a complex number in scientific mode (shortest representation) to a string representation
    """
    num /= 10**scale_value_map[info.scale]
    switch = {Format.RE: num2str_re,
              Format.RE_IM: num2str_re_im,
              Format.LIN_DEG: num2str_lin_deg,
              Format.LOG_DEG: num2str_log_deg
              }
    return switch[info.format](num, info)
    # unit_prefix = "dB" if settings.format == "Log<Deg" else ""
    # return str_ + " " + unit_prefix + settings.scale + settings.unit


def str2num_re(str_, info=Info("untitled", write=True, check=True)):
    pattern = re.compile(r"""
        \s*                                     # Skip leading whitespace
        ([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)       # +/- Real float
        (?:[eE][+-]?[0-9]+)?)?                  # Optional Scientific Notation
        .*                                      # Trailing whitespace to end-of-line
    """, re.VERBOSE)
    match = pattern.search(str_)
    if match:
        num = float(match.group(1))
    else:
        raise ValueError("Unrecognized Float Number User Input (Re Format)")
    return num


def str2num_re_im(str_, info=Info("untitled", write=True, check=True)):
    pattern = re.compile(r"""
        \s*                                     # Skip leading whitespace
        ([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)       # +/- Real float
        (?:[eE][+-]?[0-9]+)?)?                  # Optional Scientific Notation
        \s*([+-]?)\s*
        (?:([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)    # +/- Imag float
        (?:[eE][+-]?[0-9]+)?)                   # Optional Scientific Notation
        [JjIi])?                                # Imaginary Sign
        .*                                      # Trailing whitespace to end-of-line
    """, re.VERBOSE)
    match = pattern.search(str_)
    if match:
        if match.start(3) > 0:
            num = complex(float(match.group(1)), float(match.group(2)+match.group(3)))
        else:
            num = complex(float(match.group(1)), 0)
    else:
        raise ValueError("Unrecognized Complex Number User Input (Re+Imj Format)")
    return num


def str2num_lin_deg(str_, info=Info("untitled", write=True, check=True)):
    pattern = re.compile(r"""
        \s*                                     # Skip leading whitespace
        ([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)       # +/- Mag float
        (?:[eE][+-]?[0-9]+)?)                   # Optional Scientific Notation
        (\s*[<∠]\s*)?                           # Angle Sign
        ([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)       # +/- Phase float
        (?:[eE][+-]?[0-9]+)?)?                  # Optional Scientific Notation
        .*                                      # Trailing whitespace to end-of-line
    """, re.VERBOSE)
    match = pattern.search(str_)
    if match:
        if match.start(3) > 0:
            num = complex(float(match.group(1)), 0)*ct.exp(complex(0, float(match.group(3)))*ct.pi/180)
        else:
            num = complex(float(match.group(1)), 0)
    else:
        raise ValueError("Unrecognized Complex Number User Input (Lin<Deg Format)")
    return num


def str2num_log_deg(str_, info=Info("untitled", write=True, check=True)):
    pattern = re.compile(r"""
        \s*                                     # Skip leading whitespace
        ([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)       # +/- Mag float
        (?:[eE][+-]?[0-9]+)?)                   # Optional Scientific Notation
        (\s*[<∠]\s*)?                           # Angle Sign
        ([+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)       # +/- Phase float
        (?:[eE][+-]?[0-9]+)?)?                  # Optional Scientific Notation
        .*                                      # Trailing whitespace to end-of-line
    """, re.VERBOSE)
    match = pattern.search(str_)
    if match:
        if match.start(3) > 0:
            num = 10**((complex(float(match.group(1)), 0))/20)*ct.exp(complex(0, float(match.group(3)))*ct.pi/180)/ct.sqrt(10**scale_value_map[info.scale])
        else:
            num = 10**((complex(float(match.group(1)), 0))/20)/ct.sqrt(10 ** scale_value_map[info.scale])
    else:
        raise ValueError("Unrecognized Complex Number User Input (Log<Deg Format)")
    return num


def str2num(str_, info=Info("untitled", write=True, check=True)):
    """Converts a string representation to a complex number in scientific notation (shortest representation)
    """
    switch = {Format.RE: str2num_re,
              Format.RE_IM: str2num_re_im,
              Format.LIN_DEG: str2num_lin_deg,
              Format.LOG_DEG: str2num_log_deg
              }
    num = switch[info.format](str_, info)
    return num*10**scale_value_map[info.scale]


def re_im2re_im(re_im):
    return (re_im)


def re_im2lin_deg(re_im):
    return np.abs(re_im) + 1j*np.angle(re_im, deg=True)


def re_im2log_deg(re_im):
    return 20*np.log10(np.abs(re_im))*1j*np.angle(re_im, deg=True)


def lin_deg2re_im(lin_deg):
    return lin_deg.real*np.exp(1j*lin_deg.imag*np.pi/180)


def lin_deg2log_deg(lin_deg):
    return 20*np.log10(lin_deg.real) + lin_deg.imag


def log_deg2re_im(log_deg):
    return 10**(log_deg.real/20)*np.exp(1j*log_deg.imag*np.pi/180)


def log_deg2lin_deg(log_deg):
    return 10**(log_deg.real / 20) + log_deg.imag


def factors(n):
    return set(reduce(list.__add__,
                ([i, n//i] for i in range(1, int(pow(n, 0.5) + 1)) if n % i == 0)))


def diff(x, axis=0):
    size = x.shape[axis] - 1
    return x.narrow(axis, 1, size) - x.narrow(axis, 0, size)

def gradient(f, *X, axis=None):
    gradient = np.zeros((len(X),) + f.shape, dtype=np.complex_)
    for sweep_index in range(f.shape[-1]):
        X_vars = [x[:, sweep_index] for x in X]
        f_vars = f[..., sweep_index]
        gradient[..., sweep_index] = np.gradient(f_vars, *X_vars, axis=axis)
    return gradient


def jacobian(F, *X, axis=None):
    return np.stack([gradient(f, *X, axis=axis) for f in F])


def hessian(f, *X, axis=None):
    return np.swapaxes(jacobian(gradient(f, *X, axis=axis), *X, axis=axis), 0, 1)


def gaussian2tol(mean, std, n=1):
    # mean, std, n
    se = std/mt.sqrt(n)
    rse = se/mean
    return rse, se


def unravel_index(index, shape):
    out = []
    for dim in reversed(shape):
        out.append(index % dim)
        index = index // dim
    return tuple(reversed(out))
