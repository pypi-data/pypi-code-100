"""
Helper functions to enable typing.
"""
import itertools
import operator
import types as pytypes
from inspect import getfullargspec
import numba
import numba.cpython.unicode
import numpy as np
import pandas as pd
from numba.core import ir, ir_utils, types
from numba.core.errors import NumbaError
from numba.core.registry import CPUDispatcher
from numba.core.typing.templates import AbstractTemplate, signature
from numba.extending import NativeValue, infer, intrinsic, lower_builtin, lower_cast, models, overload, overload_method, register_jitable, register_model, unbox
import bodo
CONST_DICT_SENTINEL = '$_bodo_const_dict_$'
list_cumulative = {'cumsum', 'cumprod', 'cummin', 'cummax'}


def is_timedelta_type(in_type):
    return in_type in [bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type, bodo.hiframes.datetime_date_ext.
        datetime_timedelta_type]


def is_dtype_nullable(in_dtype):
    return isinstance(in_dtype, (types.Float, types.NPDatetime, types.
        NPTimedelta))


def is_nullable(typ):
    return bodo.utils.utils.is_array_typ(typ, False) and (not isinstance(
        typ, types.Array) or is_dtype_nullable(typ.dtype))


class BodoError(NumbaError):

    def __init__(self, msg, loc=None, locs_in_msg=None):
        if locs_in_msg is None:
            self.locs_in_msg = []
        else:
            self.locs_in_msg = locs_in_msg
        ndlh__uyrq = numba.core.errors.termcolor().errmsg
        super(BodoError, self).__init__(ndlh__uyrq(msg), loc)


class BodoException(Exception):
    pass


class BodoNotConstError(Exception):
    pass


class BodoConstUpdatedError(Exception):
    pass


def raise_const_error(msg):
    if bodo.transforms.typing_pass.in_partial_typing:
        bodo.transforms.typing_pass.typing_transform_required = True
        raise BodoNotConstError(msg)
    else:
        raise BodoError(msg)


def raise_bodo_error(msg, loc=None):
    if bodo.transforms.typing_pass.in_partial_typing:
        bodo.transforms.typing_pass.typing_transform_required = True
        raise BodoException(msg)
    else:
        lqec__jeqvw = [] if loc is None else [loc]
        raise BodoError(msg, locs_in_msg=lqec__jeqvw)


class BodoWarning(Warning):
    pass


def get_udf_error_msg(context_str, error):
    msg = ''
    if hasattr(error, 'msg'):
        msg = str(error.msg)
    if hasattr(error, 'args') and error.args:
        msg = str(error.args[0])
    loc = ''
    if hasattr(error, 'loc') and error.loc is not None:
        loc = error.loc.strformat()
    return f'{context_str}: user-defined function not supported: {msg}\n{loc}'


class FileInfo(object):

    def get_schema(self, fname):
        raise NotImplementedError


class FilenameType(types.StringLiteral):

    def __init__(self, fname, finfo):
        self.fname = fname
        self.schema = finfo.get_schema(fname)
        super(FilenameType, self).__init__(self.fname)

    def __hash__(self):
        return 37

    def __eq__(self, other):
        if isinstance(other, types.FilenameType):
            assert self.schema is not None
            assert other.schema is not None
            return self.schema == other.schema
        else:
            return False


types.FilenameType = FilenameType
register_model(types.FilenameType)(numba.cpython.unicode.UnicodeModel)
unbox(types.FilenameType)(numba.cpython.unicode.unbox_unicode_str)


@lower_cast(types.FilenameType, types.unicode_type)
def cast_filename_to_unicode(context, builder, fromty, toty, val):
    return val


class NotConstant:
    pass


NOT_CONSTANT = NotConstant()


def is_overload_none(val):
    return val is None or val == types.none or getattr(val, 'value', False
        ) is None


def is_overload_constant_bool(val):
    return isinstance(val, bool) or isinstance(val, types.BooleanLiteral
        ) or isinstance(val, types.Omitted) and isinstance(val.value, bool)


def is_overload_bool(val):
    return isinstance(val, types.Boolean) or is_overload_constant_bool(val)


def is_overload_constant_str(val):
    return isinstance(val, str) or isinstance(val, types.StringLiteral
        ) and isinstance(val.literal_value, str) or isinstance(val, types.
        Omitted) and isinstance(val.value, str)


def is_overload_constant_bytes(val):
    return isinstance(val, bytes) or isinstance(val, types.Omitted
        ) and isinstance(val.value, bytes)


def is_overload_constant_list(val):
    return isinstance(val, (list, tuple)) or isinstance(val, types.Omitted
        ) and isinstance(val.value, tuple) or is_initial_value_list_type(val
        ) or isinstance(val, types.LiteralList) or isinstance(val, bodo.
        utils.typing.ListLiteral) or isinstance(val, types.BaseTuple) and all(
        is_literal_type(t) for t in val.types) and (not val.types or val.
        types[0] != types.StringLiteral(CONST_DICT_SENTINEL))


def is_overload_constant_tuple(val):
    return isinstance(val, tuple) or isinstance(val, types.Omitted
        ) and isinstance(val.value, tuple) or isinstance(val, types.BaseTuple
        ) and all(get_overload_const(t) is not NOT_CONSTANT for t in val.types)


def is_initial_value_type(t):
    if not isinstance(t, types.InitialValue) or t.initial_value is None:
        return False
    vrsf__shhwn = t.initial_value
    if isinstance(vrsf__shhwn, dict):
        vrsf__shhwn = vrsf__shhwn.values()
    return not any(isinstance(rcuve__qdph, (types.Poison, numba.core.
        interpreter._UNKNOWN_VALUE)) for rcuve__qdph in vrsf__shhwn)


def is_initial_value_list_type(t):
    return isinstance(t, types.List) and is_initial_value_type(t)


def is_initial_value_dict_type(t):
    return isinstance(t, types.DictType) and is_initial_value_type(t)


def is_overload_constant_dict(val):
    return isinstance(val, types.LiteralStrKeyDict) and all(is_literal_type
        (rcuve__qdph) for rcuve__qdph in val.types
        ) or is_initial_value_dict_type(val) or isinstance(val, DictLiteral
        ) or isinstance(val, types.BaseTuple) and val.types and val.types[0
        ] == types.StringLiteral(CONST_DICT_SENTINEL)


def is_overload_constant_number(val):
    return is_overload_constant_int(val) or is_overload_constant_float(val)


def is_overload_constant_nan(val):
    return is_overload_constant_float(val) and np.isnan(
        get_overload_const_float(val))


def is_overload_constant_float(val):
    return isinstance(val, float) or isinstance(val, types.Omitted
        ) and isinstance(val.value, float)


def is_overload_int(val):
    return is_overload_constant_int(val) or isinstance(val, types.Integer)


def is_overload_constant_int(val):
    return isinstance(val, int) or isinstance(val, types.IntegerLiteral
        ) and isinstance(val.literal_value, int) or isinstance(val, types.
        Omitted) and isinstance(val.value, int)


def is_overload_bool_list(val):
    return is_overload_constant_list(val) and all(is_overload_constant_bool
        (rcuve__qdph) for rcuve__qdph in get_overload_const_list(val))


def is_overload_true(val):
    return val == True or val == types.BooleanLiteral(True) or getattr(val,
        'value', False) is True


def is_overload_false(val):
    return val == False or val == types.BooleanLiteral(False) or getattr(val,
        'value', True) is False


def is_overload_zero(val):
    return val == 0 or val == types.IntegerLiteral(0) or getattr(val,
        'value', -1) == 0


def is_overload_str(val, const):
    return val == const or val == types.StringLiteral(const) or getattr(val,
        'value', -1) == const


def get_overload_const(val):
    if isinstance(val, types.TypeRef):
        val = val.instance_type
    if val == types.none:
        return None
    if val is None or isinstance(val, (bool, int, float, str, tuple, types.
        Dispatcher)):
        return val
    if isinstance(val, types.Omitted):
        return val.value
    if isinstance(val, types.LiteralList):
        return [get_overload_const(rcuve__qdph) for rcuve__qdph in val.
            literal_value]
    if isinstance(val, types.Literal):
        return val.literal_value
    if isinstance(val, types.Dispatcher):
        return val
    if isinstance(val, types.BaseTuple):
        return tuple(get_overload_const(rcuve__qdph) for rcuve__qdph in val
            .types)
    if is_initial_value_list_type(val):
        return val.initial_value
    if is_literal_type(val):
        return get_literal_value(val)
    return NOT_CONSTANT


def element_type(val):
    if isinstance(val, (types.List, types.ArrayCompatible)):
        if isinstance(val.dtype, bodo.hiframes.pd_categorical_ext.
            PDCategoricalDtype):
            return val.dtype.elem_type
        if val == bodo.bytes_type:
            return bodo.bytes_type
        return val.dtype
    return types.unliteral(val)


def can_replace(to_replace, value):
    return is_common_scalar_dtype([to_replace, value]) and not (isinstance(
        to_replace, types.Integer) and isinstance(value, types.Float)
        ) and not (isinstance(to_replace, types.Boolean) and isinstance(
        value, (types.Integer, types.Float)))


_const_type_repr = {str: 'string', bool: 'boolean', int: 'integer'}


def ensure_constant_arg(fname, arg_name, val, const_type):
    iwedn__mmv = get_overload_const(val)
    kpou__piiiv = _const_type_repr.get(const_type, str(const_type))
    if not isinstance(iwedn__mmv, const_type):
        raise BodoError(
            f"{fname}(): argument '{arg_name}' should be a constant {kpou__piiiv} not {val}"
            )


def ensure_constant_values(fname, arg_name, val, const_values):
    iwedn__mmv = get_overload_const(val)
    if iwedn__mmv not in const_values:
        raise BodoError(
            f"{fname}(): argument '{arg_name}' should be a constant value in {const_values} not '{iwedn__mmv}'"
            )


def check_unsupported_args(fname, args_dict, arg_defaults_dict,
    package_name='pandas'):
    assert len(args_dict) == len(arg_defaults_dict)
    qrdfc__xomme = ''
    bja__ntof = False
    for tcye__aeps in args_dict:
        wqtsd__iwtwy = get_overload_const(args_dict[tcye__aeps])
        bbla__vtpd = arg_defaults_dict[tcye__aeps]
        if (wqtsd__iwtwy is NOT_CONSTANT or wqtsd__iwtwy is not None and 
            bbla__vtpd is None or wqtsd__iwtwy is None and bbla__vtpd is not
            None or wqtsd__iwtwy != bbla__vtpd):
            qrdfc__xomme = (
                f'{fname}(): {tcye__aeps} parameter only supports default value {bbla__vtpd}'
                )
            bja__ntof = True
            break
    if bja__ntof and package_name == 'pandas':
        qrdfc__xomme += """
Please check supported Pandas operations here (https://docs.bodo.ai/latest/source/pandas.html).
"""
    elif bja__ntof and package_name == 'ml':
        qrdfc__xomme += """
Please check supported ML operations here (https://docs.bodo.ai/latest/source/ml.html).
"""
    elif bja__ntof and package_name == 'numpy':
        qrdfc__xomme += """
Please check supported Numpy operations here (https://docs.bodo.ai/latest/source/numpy.html).
"""
    if bja__ntof:
        raise BodoError(qrdfc__xomme)


def get_overload_const_tuple(val):
    if isinstance(val, tuple):
        return val
    if isinstance(val, types.Omitted):
        assert isinstance(val.value, tuple)
        return val.value
    if isinstance(val, types.BaseTuple):
        return tuple(get_overload_const(t) for t in val.types)


def get_overload_constant_dict(val):
    if isinstance(val, types.LiteralStrKeyDict):
        return {get_literal_value(vgyev__kaer): get_literal_value(
            rcuve__qdph) for vgyev__kaer, rcuve__qdph in val.literal_value.
            items()}
    if isinstance(val, DictLiteral):
        return val.literal_value
    assert is_initial_value_dict_type(val) or isinstance(val, types.BaseTuple
        ) and val.types and val.types[0] == types.StringLiteral(
        CONST_DICT_SENTINEL), 'invalid const dict'
    if isinstance(val, types.DictType):
        assert val.initial_value is not None, 'invalid dict initial value'
        return val.initial_value
    xtvs__ymkbd = [get_overload_const(rcuve__qdph) for rcuve__qdph in val.
        types[1:]]
    return {xtvs__ymkbd[2 * ojad__tnha]: xtvs__ymkbd[2 * ojad__tnha + 1] for
        ojad__tnha in range(len(xtvs__ymkbd) // 2)}


def get_overload_const_str_len(val):
    if isinstance(val, str):
        return len(val)
    if isinstance(val, types.StringLiteral) and isinstance(val.
        literal_value, str):
        return len(val.literal_value)
    if isinstance(val, types.Omitted) and isinstance(val.value, str):
        return len(val.value)


def get_overload_const_list(val):
    if isinstance(val, (list, tuple)):
        return val
    if isinstance(val, types.Omitted) and isinstance(val.value, tuple):
        return val.value
    if is_initial_value_list_type(val):
        return val.initial_value
    if isinstance(val, types.LiteralList):
        return [get_literal_value(rcuve__qdph) for rcuve__qdph in val.
            literal_value]
    if isinstance(val, bodo.utils.typing.ListLiteral):
        return val.literal_value
    if isinstance(val, types.Omitted):
        return [val.value]
    if isinstance(val, types.Literal):
        return [val.literal_value]
    if isinstance(val, types.BaseTuple) and all(is_literal_type(t) for t in
        val.types):
        return tuple(get_literal_value(t) for t in val.types)


def get_overload_const_str(val):
    if isinstance(val, str):
        return val
    if isinstance(val, types.Omitted):
        assert isinstance(val.value, str)
        return val.value
    if isinstance(val, types.StringLiteral):
        assert isinstance(val.literal_value, str)
        return val.literal_value
    raise BodoError('{} not constant string'.format(val))


def get_overload_const_bytes(val):
    if isinstance(val, bytes):
        return val
    if isinstance(val, types.Omitted):
        assert isinstance(val.value, bytes)
        return val.value
    raise BodoError('{} not constant binary'.format(val))


def get_overload_const_int(val):
    if isinstance(val, int):
        return val
    if isinstance(val, types.Omitted):
        assert isinstance(val.value, int)
        return val.value
    if isinstance(val, types.IntegerLiteral):
        assert isinstance(val.literal_value, int)
        return val.literal_value
    raise BodoError('{} not constant integer'.format(val))


def get_overload_const_float(val):
    if isinstance(val, float):
        return val
    if isinstance(val, types.Omitted):
        assert isinstance(val.value, float)
        return val.value
    raise BodoError('{} not constant float'.format(val))


def get_overload_const_bool(val):
    if isinstance(val, bool):
        return val
    if isinstance(val, types.Omitted):
        assert isinstance(val.value, bool)
        return val.value
    if isinstance(val, types.BooleanLiteral):
        assert isinstance(val.literal_value, bool)
        return val.literal_value
    raise BodoError('{} not constant boolean'.format(val))


def is_const_func_type(t):
    return isinstance(t, (types.MakeFunctionLiteral, bodo.utils.typing.
        FunctionLiteral, types.Dispatcher))


def get_overload_const_func(val, func_ir):
    if isinstance(val, (types.MakeFunctionLiteral, bodo.utils.typing.
        FunctionLiteral)):
        func = val.literal_value
        if isinstance(func, ir.Expr) and func.op == 'make_function':
            assert func_ir is not None, 'Function expression is make_function but there is no existing IR'
            func = numba.core.ir_utils.convert_code_obj_to_function(func,
                func_ir)
        return func
    if isinstance(val, types.Dispatcher):
        return val.dispatcher.py_func
    if isinstance(val, CPUDispatcher):
        return val.py_func
    raise BodoError("'{}' not a constant function type".format(val))


def is_heterogeneous_tuple_type(t):
    if is_overload_constant_list(t):
        if isinstance(t, types.LiteralList):
            t = types.BaseTuple.from_types(t.types)
        else:
            t = bodo.typeof(tuple(get_overload_const_list(t)))
    return isinstance(t, types.BaseTuple) and not isinstance(t, types.UniTuple)


def parse_dtype(dtype, func_name=None):
    if isinstance(dtype, types.TypeRef):
        return dtype.instance_type
    if isinstance(dtype, types.Function):
        if dtype.key[0] == float:
            dtype = types.StringLiteral('float')
        elif dtype.key[0] == int:
            dtype = types.StringLiteral('int')
        elif dtype.key[0] == bool:
            dtype = types.StringLiteral('bool')
        elif dtype.key[0] == str:
            dtype = bodo.string_type
    if isinstance(dtype, types.DTypeSpec):
        return dtype.dtype
    if isinstance(dtype, types.Number) or dtype == bodo.string_type:
        return dtype
    try:
        oxyur__wey = get_overload_const_str(dtype)
        if oxyur__wey.startswith('Int') or oxyur__wey.startswith('UInt'):
            return bodo.libs.int_arr_ext.typeof_pd_int_dtype(pd.api.types.
                pandas_dtype(oxyur__wey), None)
        if oxyur__wey == 'boolean':
            return bodo.libs.bool_arr_ext.boolean_dtype
        return numba.np.numpy_support.from_dtype(np.dtype(oxyur__wey))
    except:
        pass
    if func_name is not None:
        raise BodoError(f'{func_name}(): invalid dtype {dtype}')
    else:
        raise BodoError(f'invalid dtype {dtype}')


def is_list_like_index_type(t):
    from bodo.hiframes.pd_index_ext import NumericIndexType, RangeIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    from bodo.libs.bool_arr_ext import boolean_array
    return isinstance(t, types.List) or isinstance(t, types.Array
        ) and t.ndim == 1 or isinstance(t, (NumericIndexType, RangeIndexType)
        ) or isinstance(t, SeriesType) or t == boolean_array


def is_tuple_like_type(t):
    return isinstance(t, types.BaseTuple) or is_heterogeneous_tuple_type(t
        ) or isinstance(t, bodo.hiframes.pd_index_ext.HeterogeneousIndexType)


def get_index_names(t, func_name, default_name):
    from bodo.hiframes.pd_multi_index_ext import MultiIndexType
    jul__sokqm = '{}: index name should be a constant string'.format(func_name)
    if isinstance(t, MultiIndexType):
        xra__bumy = []
        for ojad__tnha, nrt__ghn in enumerate(t.names_typ):
            if nrt__ghn == types.none:
                xra__bumy.append('level_{}'.format(ojad__tnha))
                continue
            if not is_overload_constant_str(nrt__ghn):
                raise BodoError(jul__sokqm)
            xra__bumy.append(get_overload_const_str(nrt__ghn))
        return tuple(xra__bumy)
    if t.name_typ == types.none:
        return default_name,
    if not is_overload_constant_str(t.name_typ):
        raise BodoError(jul__sokqm)
    return get_overload_const_str(t.name_typ),


def get_index_data_arr_types(t):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_multi_index_ext import MultiIndexType
    if isinstance(t, MultiIndexType):
        return tuple(t.array_types)
    if isinstance(t, (RangeIndexType, PeriodIndexType)):
        return types.Array(types.int64, 1, 'C'),
    if isinstance(t, (NumericIndexType, StringIndexType, BinaryIndexType,
        DatetimeIndexType, TimedeltaIndexType, CategoricalIndexType)):
        return t.data,
    raise BodoError(f'Invalid index type {t}')


def get_index_type_from_dtype(t):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, StringIndexType, TimedeltaIndexType
    if t in [bodo.hiframes.pd_timestamp_ext.pd_timestamp_type, bodo.
        datetime64ns]:
        return DatetimeIndexType(types.none)
    if t in [bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type, bodo.
        timedelta64ns]:
        return TimedeltaIndexType(types.none)
    if t == bodo.string_type:
        return StringIndexType(types.none)
    if t == bodo.bytes_type:
        return BinaryIndexType(types.none)
    if isinstance(t, (types.Integer, types.Float, types.Boolean)):
        return NumericIndexType(t, types.none)
    if isinstance(t, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        return CategoricalIndexType(bodo.CategoricalArrayType(t))
    raise BodoError(f'Cannot convert dtype {t} to index type')


def get_val_type_maybe_str_literal(value):
    t = numba.typeof(value)
    if isinstance(value, str):
        t = types.StringLiteral(value)
    return t


def get_index_name_types(t):
    from bodo.hiframes.pd_multi_index_ext import MultiIndexType
    if isinstance(t, MultiIndexType):
        return t.names_typ
    return t.name_typ,


class ListLiteral(types.Literal):
    pass


types.Literal.ctor_map[list] = ListLiteral
register_model(ListLiteral)(models.OpaqueModel)


@unbox(ListLiteral)
def unbox_list_literal(typ, obj, c):
    return NativeValue(c.context.get_dummy_value())


@lower_cast(ListLiteral, types.List)
def list_literal_to_list(context, builder, fromty, toty, val):
    list_vals = tuple(fromty.literal_value)
    ivnud__odsh = types.List(toty.dtype)
    return context.compile_internal(builder, lambda : list(list_vals),
        ivnud__odsh(), [])


class DictLiteral(types.Literal):
    pass


types.Literal.ctor_map[dict] = DictLiteral
register_model(DictLiteral)(models.OpaqueModel)


@unbox(DictLiteral)
def unbox_dict_literal(typ, obj, c):
    return NativeValue(c.context.get_dummy_value())


class FunctionLiteral(types.Literal, types.Opaque):
    pass


types.Literal.ctor_map[pytypes.FunctionType] = FunctionLiteral
register_model(FunctionLiteral)(models.OpaqueModel)


@unbox(FunctionLiteral)
def unbox_func_literal(typ, obj, c):
    return NativeValue(obj)


types.MakeFunctionLiteral._literal_type_cache = types.MakeFunctionLiteral(
    lambda : 0)


class MetaType(types.Type):

    def __init__(self, meta):
        self.meta = meta
        super(MetaType, self).__init__('MetaType({})'.format(meta))

    def can_convert_from(self, typingctx, other):
        return True

    @property
    def key(self):
        return tuple(self.meta)


register_model(MetaType)(models.OpaqueModel)


def is_literal_type(t):
    if isinstance(t, types.TypeRef):
        t = t.instance_type
    return isinstance(t, (types.Literal, types.Omitted)) and not isinstance(t,
        types.LiteralStrKeyDict) or t == types.none or isinstance(t, types.
        Dispatcher) or isinstance(t, types.BaseTuple) and all(
        is_literal_type(rcuve__qdph) for rcuve__qdph in t.types
        ) or is_initial_value_type(t) or isinstance(t, (types.DTypeSpec,
        types.Function)) or isinstance(t, bodo.libs.int_arr_ext.IntDtype
        ) or t in (bodo.libs.bool_arr_ext.boolean_dtype, bodo.libs.
        str_arr_ext.string_dtype) or isinstance(t, types.Function
        ) or is_overload_constant_index(t) or is_overload_constant_series(t)


def is_overload_constant_index(t):
    from bodo.hiframes.pd_index_ext import HeterogeneousIndexType
    return isinstance(t, HeterogeneousIndexType) and is_literal_type(t.data
        ) and is_literal_type(t.name_type)


def get_overload_constant_index(t):
    assert is_overload_constant_index(t)
    return pd.Index(get_literal_value(t.data), name=get_literal_value(t.
        name_type))


def is_overload_constant_series(t):
    from bodo.hiframes.pd_series_ext import HeterogeneousSeriesType, SeriesType
    return isinstance(t, (SeriesType, HeterogeneousSeriesType)
        ) and is_literal_type(t.data) and is_literal_type(t.index
        ) and is_literal_type(t.name_typ)


def get_overload_constant_series(t):
    assert is_overload_constant_series(t)
    return pd.Series(get_literal_value(t.data), get_literal_value(t.index),
        name=get_literal_value(t.name_typ))


def get_literal_value(t):
    if isinstance(t, types.TypeRef):
        t = t.instance_type
    assert is_literal_type(t)
    if t == types.none:
        return None
    if isinstance(t, types.Literal):
        if isinstance(t, types.LiteralStrKeyDict):
            return {get_literal_value(vgyev__kaer): get_literal_value(
                rcuve__qdph) for vgyev__kaer, rcuve__qdph in t.
                literal_value.items()}
        if isinstance(t, types.LiteralList):
            return [get_literal_value(rcuve__qdph) for rcuve__qdph in t.
                literal_value]
        return t.literal_value
    if isinstance(t, types.Omitted):
        return t.value
    if isinstance(t, types.BaseTuple):
        return tuple(get_literal_value(rcuve__qdph) for rcuve__qdph in t.types)
    if isinstance(t, types.Dispatcher):
        return t
    if is_initial_value_type(t):
        return t.initial_value
    if isinstance(t, (types.DTypeSpec, types.Function)):
        return t
    if isinstance(t, bodo.libs.int_arr_ext.IntDtype):
        return getattr(pd, str(t)[:-2])()
    if t == bodo.libs.bool_arr_ext.boolean_dtype:
        return pd.BooleanDtype()
    if t == bodo.libs.str_arr_ext.string_dtype:
        return pd.StringDtype()
    if is_overload_constant_index(t):
        return get_overload_constant_index(t)
    if is_overload_constant_series(t):
        return get_overload_constant_series(t)


def can_literalize_type(t, pyobject_to_literal=False):
    return t in (bodo.string_type, types.bool_) or isinstance(t, (types.
        Integer, types.List, types.SliceType, types.DictType)
        ) or pyobject_to_literal and t == types.pyobject


def dtype_to_array_type(dtype):
    dtype = types.unliteral(dtype)
    if isinstance(dtype, types.List):
        dtype = dtype_to_array_type(dtype.dtype)
    rszuk__dmxk = False
    if isinstance(dtype, types.Optional):
        dtype = dtype.type
        rszuk__dmxk = True
    if dtype == bodo.string_type:
        return bodo.string_array_type
    if dtype == bodo.bytes_type:
        return bodo.binary_array_type
    if bodo.utils.utils.is_array_typ(dtype, False):
        return bodo.ArrayItemArrayType(dtype)
    if isinstance(dtype, bodo.hiframes.pd_categorical_ext.PDCategoricalDtype):
        return bodo.CategoricalArrayType(dtype)
    if isinstance(dtype, bodo.libs.int_arr_ext.IntDtype):
        return bodo.IntegerArrayType(dtype.dtype)
    if dtype == types.bool_:
        return bodo.boolean_array
    if dtype == bodo.datetime_date_type:
        return bodo.hiframes.datetime_date_ext.datetime_date_array_type
    if isinstance(dtype, bodo.Decimal128Type):
        return bodo.DecimalArrayType(dtype.precision, dtype.scale)
    if isinstance(dtype, bodo.libs.struct_arr_ext.StructType):
        return bodo.StructArrayType(tuple(dtype_to_array_type(t) for t in
            dtype.data), dtype.names)
    if isinstance(dtype, types.BaseTuple):
        return bodo.TupleArrayType(tuple(dtype_to_array_type(t) for t in
            dtype.types))
    if isinstance(dtype, types.DictType):
        return bodo.MapArrayType(dtype_to_array_type(dtype.key_type),
            dtype_to_array_type(dtype.value_type))
    if dtype in (bodo.pd_timestamp_type, bodo.hiframes.
        datetime_datetime_ext.datetime_datetime_type):
        return types.Array(bodo.datetime64ns, 1, 'C')
    if dtype in (bodo.pd_timedelta_type, bodo.hiframes.
        datetime_timedelta_ext.datetime_timedelta_type):
        return types.Array(bodo.timedelta64ns, 1, 'C')
    if isinstance(dtype, (types.Number, types.Boolean, types.NPDatetime,
        types.NPTimedelta)):
        vmay__pcmfp = types.Array(dtype, 1, 'C')
        if rszuk__dmxk:
            return to_nullable_type(vmay__pcmfp)
        return vmay__pcmfp
    raise BodoError(f'dtype {dtype} cannot be stored in arrays')


def get_udf_out_arr_type(f_return_type, return_nullable=False):
    if isinstance(f_return_type, types.Optional):
        f_return_type = f_return_type.type
        return_nullable = True
    if f_return_type == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        f_return_type = types.NPDatetime('ns')
    if f_return_type == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        f_return_type = types.NPTimedelta('ns')
    pdvo__enbll = dtype_to_array_type(f_return_type)
    pdvo__enbll = to_nullable_type(pdvo__enbll
        ) if return_nullable else pdvo__enbll
    return pdvo__enbll


def equality_always_false(t1, t2):
    string_types = types.UnicodeType, types.StringLiteral, types.UnicodeCharSeq
    return isinstance(t1, string_types) and not isinstance(t2, string_types
        ) or isinstance(t2, string_types) and not isinstance(t1, string_types)


def types_equality_exists(t1, t2):
    mmkoc__oiiv = numba.core.registry.cpu_target.typing_context
    try:
        mmkoc__oiiv.resolve_function_type(operator.eq, (t1, t2), {})
        return True
    except:
        return False


def is_hashable_type(t):
    whitelist_types = (types.UnicodeType, types.StringLiteral, types.
        UnicodeCharSeq, types.Number)
    vrz__xwp = (types.bool_, bodo.datetime64ns, bodo.timedelta64ns, bodo.
        pd_timestamp_type, bodo.pd_timedelta_type)
    if isinstance(t, whitelist_types) or t in vrz__xwp:
        return True
    mmkoc__oiiv = numba.core.registry.cpu_target.typing_context
    try:
        mmkoc__oiiv.resolve_function_type(hash, (t,), {})
        return True
    except:
        return False


def to_nullable_type(t):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(t, DataFrameType):
        xohx__httng = tuple(to_nullable_type(t) for t in t.data)
        return DataFrameType(xohx__httng, t.index, t.columns)
    if isinstance(t, SeriesType):
        return SeriesType(t.dtype, to_nullable_type(t.data), t.index, t.
            name_typ)
    if isinstance(t, types.Array):
        if t.dtype == types.bool_:
            return bodo.libs.bool_arr_ext.boolean_array
        if isinstance(t.dtype, types.Integer):
            return bodo.libs.int_arr_ext.IntegerArrayType(t.dtype)
    return t


def is_nullable_type(t):
    return t == to_nullable_type(t)


def is_iterable_type(t):
    from bodo.hiframes.pd_dataframe_ext import DataFrameType
    from bodo.hiframes.pd_series_ext import SeriesType
    return bodo.utils.utils.is_array_typ(t, False) or isinstance(t, (
        SeriesType, DataFrameType, types.List, types.BaseTuple, types.
        LiteralList)) or bodo.hiframes.pd_index_ext.is_pd_index_type(t)


def is_scalar_type(t):
    return isinstance(t, (types.Boolean, types.Number, types.StringLiteral)
        ) or t in (bodo.datetime64ns, bodo.timedelta64ns, bodo.string_type,
        bodo.bytes_type, bodo.datetime_date_type, bodo.
        datetime_datetime_type, bodo.datetime_timedelta_type, bodo.
        pd_timestamp_type, bodo.pd_timedelta_type, bodo.month_end_type,
        bodo.week_type, bodo.date_offset_type, types.none)


def is_common_scalar_dtype(scalar_types):
    scalar_types = [types.unliteral(tcye__aeps) for tcye__aeps in scalar_types]
    if len(scalar_types) == 0:
        return True
    try:
        iugm__ztla = np.find_common_type([numba.np.numpy_support.as_dtype(t
            ) for t in scalar_types], [])
        if iugm__ztla != object:
            return True
    except NotImplementedError as jihu__zobj:
        pass
    if scalar_types[0] in (bodo.datetime64ns, bodo.pd_timestamp_type):
        for typ in scalar_types[1:]:
            if typ not in (bodo.datetime64ns, bodo.pd_timestamp_type):
                return False
        return True
    if scalar_types[0] in (bodo.timedelta64ns, bodo.pd_timedelta_type):
        for typ in scalar_types[1:]:
            if scalar_types[0] not in (bodo.timedelta64ns, bodo.
                pd_timedelta_type):
                return False
        return True
    jfjz__onrrr = itertools.groupby(scalar_types)
    return next(jfjz__onrrr, True) and not next(jfjz__onrrr, False)


def find_common_np_dtype(arr_types):
    return numba.np.numpy_support.from_dtype(np.find_common_type([numba.np.
        numpy_support.as_dtype(t.dtype) for t in arr_types], []))


def is_immutable_array(typ):
    return isinstance(typ, (bodo.ArrayItemArrayType, bodo.MapArrayType))


def get_nullable_and_non_nullable_types(array_of_types):
    bspo__bgcd = []
    for typ in array_of_types:
        if typ == bodo.libs.bool_arr_ext.boolean_array:
            bspo__bgcd.append(types.Array(types.bool_, 1, 'C'))
        elif isinstance(typ, bodo.libs.int_arr_ext.IntegerArrayType):
            bspo__bgcd.append(types.Array(typ.dtype, 1, 'C'))
        elif isinstance(typ, types.Array):
            if typ.dtype == types.bool_:
                bspo__bgcd.append(bodo.libs.bool_arr_ext.boolean_array)
            if isinstance(typ.dtype, types.Integer):
                bspo__bgcd.append(bodo.libs.int_arr_ext.IntegerArrayType(
                    typ.dtype))
        bspo__bgcd.append(typ)
    return bspo__bgcd


def _gen_objmode_overload(func, output_type, method_name=None, single_rank=
    False):
    tltu__fwj = getfullargspec(func)
    assert tltu__fwj.varargs is None, 'varargs not supported'
    assert tltu__fwj.varkw is None, 'varkw not supported'
    defaults = [] if tltu__fwj.defaults is None else tltu__fwj.defaults
    sqkw__jmbz = len(tltu__fwj.args) - len(defaults)
    args = tltu__fwj.args[1:] if method_name else tltu__fwj.args[:]
    ajjq__vtgv = []
    for ojad__tnha, qyudr__delyg in enumerate(tltu__fwj.args):
        if ojad__tnha < sqkw__jmbz:
            ajjq__vtgv.append(qyudr__delyg)
        elif str(defaults[ojad__tnha - sqkw__jmbz]
            ) != '<deprecated parameter>':
            ajjq__vtgv.append(qyudr__delyg + '=' + str(defaults[ojad__tnha -
                sqkw__jmbz]))
        else:
            args.remove(qyudr__delyg)
    if tltu__fwj.kwonlyargs is not None:
        for qyudr__delyg in tltu__fwj.kwonlyargs:
            args.append(f'{qyudr__delyg}={qyudr__delyg}')
            ajjq__vtgv.append(
                f'{qyudr__delyg}={str(tltu__fwj.kwonlydefaults[qyudr__delyg])}'
                )
    sig = ', '.join(ajjq__vtgv)
    args = ', '.join(args)
    gfck__ivxlx = str(output_type)
    if not hasattr(types, gfck__ivxlx):
        gfck__ivxlx = f'objmode_type{ir_utils.next_label()}'
        setattr(types, gfck__ivxlx, output_type)
    if not method_name:
        func_name = func.__module__.replace('.', '_'
            ) + '_' + func.__name__ + '_func'
    xsw__iwto = f'self.{method_name}' if method_name else f'{func_name}'
    qnyau__pegs = f'def overload_impl({sig}):\n'
    qnyau__pegs += f'    def impl({sig}):\n'
    if single_rank:
        qnyau__pegs += f'        if bodo.get_rank() == 0:\n'
        vybcv__kmzk = '    '
    else:
        vybcv__kmzk = ''
    qnyau__pegs += (
        f"        {vybcv__kmzk}with numba.objmode(res='{gfck__ivxlx}'):\n")
    qnyau__pegs += f'            {vybcv__kmzk}res = {xsw__iwto}({args})\n'
    qnyau__pegs += f'        return res\n'
    qnyau__pegs += f'    return impl\n'
    kdpb__ddvj = {}
    tlb__jkx = globals()
    if not method_name:
        tlb__jkx[func_name] = func
    exec(qnyau__pegs, tlb__jkx, kdpb__ddvj)
    qlwv__ghnx = kdpb__ddvj['overload_impl']
    return qlwv__ghnx


def gen_objmode_func_overload(func, output_type=None, single_rank=False):
    try:
        qlwv__ghnx = _gen_objmode_overload(func, output_type, single_rank=
            single_rank)
        overload(func, no_unliteral=True)(qlwv__ghnx)
    except Exception as jihu__zobj:
        pass


def gen_objmode_method_overload(obj_type, method_name, method, output_type=
    None, single_rank=False):
    try:
        qlwv__ghnx = _gen_objmode_overload(method, output_type, method_name,
            single_rank)
        overload_method(obj_type, method_name, no_unliteral=True)(qlwv__ghnx)
    except Exception as jihu__zobj:
        pass


@infer
class NumTypeStaticGetItem(AbstractTemplate):
    key = 'static_getitem'

    def generic(self, args, kws):
        val, icn__wxqhp = args
        if isinstance(icn__wxqhp, slice) and (isinstance(val, types.
            NumberClass) or isinstance(val, types.TypeRef) and isinstance(
            val.instance_type, (types.NPDatetime, types.NPTimedelta))):
            return signature(types.TypeRef(val.instance_type[icn__wxqhp]),
                *args)


@lower_builtin('static_getitem', types.NumberClass, types.SliceLiteral)
def num_class_type_static_getitem(context, builder, sig, args):
    return context.get_dummy_value()


@overload(itertools.chain, no_unliteral=True)
def chain_overload():
    return lambda : [0]


@register_jitable
def from_iterable_impl(A):
    return bodo.utils.conversion.flatten_array(bodo.utils.conversion.
        coerce_to_array(A))


@intrinsic
def unliteral_val(typingctx, val=None):

    def codegen(context, builder, signature, args):
        return args[0]
    return types.unliteral(val)(val), codegen


def create_unsupported_overload(fname):

    def overload_f(*a, **kws):
        raise BodoError('{} not supported yet'.format(fname))
    return overload_f


def is_numpy_ufunc(func):
    return isinstance(func, types.Function) and isinstance(func.typing_key,
        np.ufunc)


def is_builtin_function(func):
    return isinstance(func, types.Function) and isinstance(func.typing_key,
        pytypes.BuiltinFunctionType)


def get_builtin_function_name(func):
    return func.typing_key.__name__


def construct_pysig(arg_names, defaults):
    qnyau__pegs = f'def stub('
    for qyudr__delyg in arg_names:
        qnyau__pegs += qyudr__delyg
        if qyudr__delyg in defaults:
            if isinstance(defaults[qyudr__delyg], str):
                qnyau__pegs += f"='{defaults[qyudr__delyg]}'"
            else:
                qnyau__pegs += f'={defaults[qyudr__delyg]}'
        qnyau__pegs += ', '
    qnyau__pegs += '):\n'
    qnyau__pegs += '    pass\n'
    kdpb__ddvj = {}
    exec(qnyau__pegs, {}, kdpb__ddvj)
    sxzi__heh = kdpb__ddvj['stub']
    return numba.core.utils.pysignature(sxzi__heh)


def fold_typing_args(func_name, args, kws, arg_names, defaults,
    unsupported_arg_names=()):
    kws = dict(kws)
    gvmwb__mtsg = len(arg_names)
    bszc__fasyc = len(args) + len(kws)
    if bszc__fasyc > gvmwb__mtsg:
        rpcvx__voi = 'argument' if gvmwb__mtsg == 1 else 'arguments'
        jyfri__dpbio = 'was' if bszc__fasyc == 1 else 'were'
        raise BodoError(
            f'{func_name}(): Too many arguments specified. Function takes {gvmwb__mtsg} {rpcvx__voi}, but {bszc__fasyc} {jyfri__dpbio} provided.'
            )
    xqcu__hcnp = bodo.utils.typing.construct_pysig(arg_names, defaults)
    try:
        ufxda__hzxlm = bodo.utils.transform.fold_argument_types(xqcu__hcnp,
            args, kws)
    except Exception as wxuvs__mtjbc:
        raise_bodo_error(f'{func_name}(): {wxuvs__mtjbc}')
    if unsupported_arg_names:
        zeyxu__ewwhh = {}
        mxo__alqn = {}
        for ojad__tnha, arg_name in enumerate(arg_names):
            if arg_name in unsupported_arg_names:
                assert arg_name in defaults, f"{func_name}(): '{arg_name}' is unsupported but no default is provided"
                zeyxu__ewwhh[arg_name] = ufxda__hzxlm[ojad__tnha]
                mxo__alqn[arg_name] = defaults[arg_name]
        check_unsupported_args(func_name, zeyxu__ewwhh, mxo__alqn)
    return xqcu__hcnp, ufxda__hzxlm


def _is_pandas_numeric_dtype(dtype):
    return isinstance(dtype, types.Number) or dtype == types.bool_


def type_col_to_index(col_names):
    if all(isinstance(tcye__aeps, str) for tcye__aeps in col_names):
        return bodo.StringIndexType(None)
    elif all(isinstance(tcye__aeps, bytes) for tcye__aeps in col_names):
        return bodo.BinaryIndexType(None)
    elif all(isinstance(tcye__aeps, (int, float)) for tcye__aeps in col_names):
        if any(isinstance(tcye__aeps, float) for tcye__aeps in col_names):
            return bodo.NumericIndexType(types.float64)
        else:
            return bodo.NumericIndexType(types.int64)
    else:
        return bodo.hiframes.pd_index_ext.HeterogeneousIndexType(col_names)
