"""
Utility functions for conversion of data such as list to array.
Need to be inlined for better optimization.
"""
import numba
import numpy as np
import pandas as pd
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.binary_arr_ext import bytes_type
from bodo.libs.decimal_arr_ext import Decimal128Type, DecimalArrayType
from bodo.utils.indexing import add_nested_counts, init_nested_counts
from bodo.utils.typing import BodoError, dtype_to_array_type, get_overload_const_list, get_overload_const_str, is_heterogeneous_tuple_type, is_overload_constant_list, is_overload_constant_str, is_overload_none, is_overload_true, to_nullable_type
NS_DTYPE = np.dtype('M8[ns]')
TD_DTYPE = np.dtype('m8[ns]')


def coerce_to_ndarray(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_ndarray)
def overload_coerce_to_ndarray(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import DatetimeIndexType, NumericIndexType, RangeIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, bodo.libs.int_arr_ext.IntegerArrayType
        ) and not is_overload_none(use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.int_arr_ext.
            get_int_arr_data(data))
    if data == bodo.libs.bool_arr_ext.boolean_array and not is_overload_none(
        use_nullable_array):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.bool_arr_ext.
            get_bool_arr_data(data))
    if isinstance(data, types.Array):
        if not is_overload_none(use_nullable_array) and isinstance(data.
            dtype, (types.Boolean, types.Integer)):
            if data.dtype == types.bool_:
                if data.layout != 'C':
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(np.
                        ascontiguousarray(data), np.full(len(data) + 7 >> 3,
                        255, np.uint8)))
                else:
                    return (lambda data, error_on_nonarray=True,
                        use_nullable_array=None, scalar_to_arr_len=None:
                        bodo.libs.bool_arr_ext.init_bool_array(data, np.
                        full(len(data) + 7 >> 3, 255, np.uint8)))
            elif data.layout != 'C':
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(np.
                    ascontiguousarray(data), np.full(len(data) + 7 >> 3, 
                    255, np.uint8)))
            else:
                return (lambda data, error_on_nonarray=True,
                    use_nullable_array=None, scalar_to_arr_len=None: bodo.
                    libs.int_arr_ext.init_integer_array(data, np.full(len(
                    data) + 7 >> 3, 255, np.uint8)))
        if data.layout != 'C':
            return (lambda data, error_on_nonarray=True, use_nullable_array
                =None, scalar_to_arr_len=None: np.ascontiguousarray(data))
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)):
        qcr__jxaa = data.dtype
        if isinstance(qcr__jxaa, types.Optional):
            qcr__jxaa = qcr__jxaa.type
            if bodo.utils.typing.is_scalar_type(qcr__jxaa):
                use_nullable_array = True
        if isinstance(qcr__jxaa, (types.Boolean, types.Integer, Decimal128Type)
            ) or qcr__jxaa in [bodo.hiframes.pd_timestamp_ext.
            pd_timestamp_type, bodo.hiframes.datetime_date_ext.
            datetime_date_type, bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type]:
            noc__atk = dtype_to_array_type(qcr__jxaa)
            if not is_overload_none(use_nullable_array):
                noc__atk = to_nullable_type(noc__atk)

            def impl(data, error_on_nonarray=True, use_nullable_array=None,
                scalar_to_arr_len=None):
                akfae__jybv = len(data)
                A = bodo.utils.utils.alloc_type(akfae__jybv, noc__atk, (-1,))
                bodo.utils.utils.tuple_list_to_array(A, data, qcr__jxaa)
                return A
            return impl
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.asarray(data))
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, RangeIndexType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data._start, data._stop,
            data._step))
    if isinstance(data, types.RangeType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.arange(data.start, data.stop,
            data.step))
    if not is_overload_none(scalar_to_arr_len):
        if isinstance(data, Decimal128Type):
            erqij__odj = data.precision
            vmi__awvi = data.scale

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                akfae__jybv = scalar_to_arr_len
                A = bodo.libs.decimal_arr_ext.alloc_decimal_array(akfae__jybv,
                    erqij__odj, vmi__awvi)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    A[frs__opvw] = data
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
            ivgp__vinlp = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                akfae__jybv = scalar_to_arr_len
                A = np.empty(akfae__jybv, ivgp__vinlp)
                lmku__lkaw = (bodo.hiframes.pd_timestamp_ext.
                    datetime_datetime_to_dt64(data))
                jwt__yhoyh = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    lmku__lkaw)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    A[frs__opvw] = jwt__yhoyh
                return A
            return impl_ts
        if (data == bodo.hiframes.datetime_timedelta_ext.
            datetime_timedelta_type):
            jxh__ppu = np.dtype('timedelta64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                akfae__jybv = scalar_to_arr_len
                A = np.empty(akfae__jybv, jxh__ppu)
                lna__pyjij = (bodo.hiframes.pd_timestamp_ext.
                    datetime_timedelta_to_timedelta64(data))
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    A[frs__opvw] = lna__pyjij
                return A
            return impl_ts
        if data == bodo.hiframes.datetime_date_ext.datetime_date_type:

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                akfae__jybv = scalar_to_arr_len
                A = bodo.hiframes.datetime_date_ext.alloc_datetime_date_array(
                    akfae__jybv)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    A[frs__opvw] = data
                return A
            return impl_ts
        if data == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
            ivgp__vinlp = np.dtype('datetime64[ns]')

            def impl_ts(data, error_on_nonarray=True, use_nullable_array=
                None, scalar_to_arr_len=None):
                akfae__jybv = scalar_to_arr_len
                A = np.empty(scalar_to_arr_len, ivgp__vinlp)
                lmku__lkaw = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data.value)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    A[frs__opvw] = lmku__lkaw
                return A
            return impl_ts
        dtype = types.unliteral(data)
        if not is_overload_none(use_nullable_array) and isinstance(dtype,
            types.Integer):

            def impl_null_integer(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                akfae__jybv = scalar_to_arr_len
                qlvvl__jzuo = bodo.libs.int_arr_ext.alloc_int_array(akfae__jybv
                    , dtype)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    qlvvl__jzuo[frs__opvw] = data
                return qlvvl__jzuo
            return impl_null_integer
        if not is_overload_none(use_nullable_array) and dtype == types.bool_:

            def impl_null_bool(data, error_on_nonarray=True,
                use_nullable_array=None, scalar_to_arr_len=None):
                numba.parfors.parfor.init_prange()
                akfae__jybv = scalar_to_arr_len
                qlvvl__jzuo = bodo.libs.bool_arr_ext.alloc_bool_array(
                    akfae__jybv)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    qlvvl__jzuo[frs__opvw] = data
                return qlvvl__jzuo
            return impl_null_bool

        def impl_num(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            numba.parfors.parfor.init_prange()
            akfae__jybv = scalar_to_arr_len
            qlvvl__jzuo = np.empty(akfae__jybv, dtype)
            for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
                qlvvl__jzuo[frs__opvw] = data
            return qlvvl__jzuo
        return impl_num
    if isinstance(data, types.BaseTuple) and all(isinstance(pllz__hhvze, (
        types.Float, types.Integer)) for pllz__hhvze in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: np.array(data))
    if bodo.utils.utils.is_array_typ(data, False):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if is_overload_true(error_on_nonarray):
        raise BodoError(f'cannot coerce {data} to array')
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: data)


def coerce_to_array(data, error_on_nonarray=True, use_nullable_array=None,
    scalar_to_arr_len=None):
    return data


@overload(coerce_to_array, no_unliteral=True)
def overload_coerce_to_array(data, error_on_nonarray=True,
    use_nullable_array=None, scalar_to_arr_len=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, StringIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    data = types.unliteral(data)
    if isinstance(data, types.Optional) and bodo.utils.typing.is_scalar_type(
        data.type):
        data = data.type
        use_nullable_array = True
    if isinstance(data, SeriesType):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_series_ext.
            get_series_data(data))
    if isinstance(data, (StringIndexType, BinaryIndexType,
        CategoricalIndexType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.hiframes.pd_index_ext.
            get_index_data(data))
    if isinstance(data, types.List) and data.dtype in (bodo.string_type,
        bodo.bytes_type):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if isinstance(data, types.UniTuple) and isinstance(data.dtype, (types.
        UnicodeType, types.StringLiteral)) or isinstance(data, types.BaseTuple
        ) and all(isinstance(pllz__hhvze, types.StringLiteral) for
        pllz__hhvze in data.types):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: bodo.libs.str_arr_ext.
            str_arr_from_sequence(data))
    if data in (bodo.string_array_type, bodo.binary_array_type, bodo.libs.
        bool_arr_ext.boolean_array, bodo.hiframes.datetime_date_ext.
        datetime_date_array_type, bodo.hiframes.datetime_timedelta_ext.
        datetime_timedelta_array_type, bodo.hiframes.split_impl.
        string_array_split_view_type) or isinstance(data, (bodo.libs.
        int_arr_ext.IntegerArrayType, DecimalArrayType, bodo.libs.
        interval_arr_ext.IntervalArrayType, bodo.libs.tuple_arr_ext.
        TupleArrayType, bodo.libs.struct_arr_ext.StructArrayType, bodo.
        hiframes.pd_categorical_ext.CategoricalArrayType, bodo.libs.
        csr_matrix_ext.CSRMatrixType)):
        return (lambda data, error_on_nonarray=True, use_nullable_array=
            None, scalar_to_arr_len=None: data)
    if isinstance(data, (types.List, types.UniTuple)) and isinstance(data.
        dtype, types.BaseTuple):
        unps__hhb = tuple(dtype_to_array_type(pllz__hhvze) for pllz__hhvze in
            data.dtype.types)

        def impl_tuple_list(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            akfae__jybv = len(data)
            arr = bodo.libs.tuple_arr_ext.pre_alloc_tuple_array(akfae__jybv,
                (-1,), unps__hhb)
            for frs__opvw in range(akfae__jybv):
                arr[frs__opvw] = data[frs__opvw]
            return arr
        return impl_tuple_list
    if isinstance(data, types.List) and (bodo.utils.utils.is_array_typ(data
        .dtype, False) or isinstance(data.dtype, types.List)):
        pmqb__iknh = dtype_to_array_type(data.dtype.dtype)

        def impl_array_item_arr(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            akfae__jybv = len(data)
            pxl__gmaor = init_nested_counts(pmqb__iknh)
            for frs__opvw in range(akfae__jybv):
                drhro__rfzan = bodo.utils.conversion.coerce_to_array(data[
                    frs__opvw], use_nullable_array=True)
                pxl__gmaor = add_nested_counts(pxl__gmaor, drhro__rfzan)
            qlvvl__jzuo = (bodo.libs.array_item_arr_ext.
                pre_alloc_array_item_array(akfae__jybv, pxl__gmaor, pmqb__iknh)
                )
            uag__oglsn = bodo.libs.array_item_arr_ext.get_null_bitmap(
                qlvvl__jzuo)
            for jdgq__zkhqu in range(akfae__jybv):
                drhro__rfzan = bodo.utils.conversion.coerce_to_array(data[
                    jdgq__zkhqu], use_nullable_array=True)
                qlvvl__jzuo[jdgq__zkhqu] = drhro__rfzan
                bodo.libs.int_arr_ext.set_bit_to_arr(uag__oglsn, jdgq__zkhqu, 1
                    )
            return qlvvl__jzuo
        return impl_array_item_arr
    if not is_overload_none(scalar_to_arr_len) and isinstance(data, (types.
        UnicodeType, types.StringLiteral)):

        def impl_str(data, error_on_nonarray=True, use_nullable_array=None,
            scalar_to_arr_len=None):
            akfae__jybv = scalar_to_arr_len
            A = bodo.libs.str_arr_ext.pre_alloc_string_array(akfae__jybv, -1)
            for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
                A[frs__opvw] = data
            return A
        return impl_str
    if isinstance(data, types.List) and data.dtype == bodo.pd_timestamp_type:

        def impl_list_timestamp(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            akfae__jybv = len(data)
            A = np.empty(akfae__jybv, np.dtype('datetime64[ns]'))
            for frs__opvw in range(akfae__jybv):
                A[frs__opvw] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                    data[frs__opvw].value)
            return A
        return impl_list_timestamp
    if isinstance(data, types.List) and data.dtype == bodo.pd_timedelta_type:

        def impl_list_timedelta(data, error_on_nonarray=True,
            use_nullable_array=None, scalar_to_arr_len=None):
            akfae__jybv = len(data)
            A = np.empty(akfae__jybv, np.dtype('timedelta64[ns]'))
            for frs__opvw in range(akfae__jybv):
                A[frs__opvw
                    ] = bodo.hiframes.pd_timestamp_ext.integer_to_timedelta64(
                    data[frs__opvw].value)
            return A
        return impl_list_timedelta
    if not is_overload_none(scalar_to_arr_len) and data in [bodo.
        pd_timestamp_type, bodo.pd_timedelta_type]:
        rjf__jbng = ('datetime64[ns]' if data == bodo.pd_timestamp_type else
            'timedelta64[ns]')

        def impl_timestamp(data, error_on_nonarray=True, use_nullable_array
            =None, scalar_to_arr_len=None):
            akfae__jybv = scalar_to_arr_len
            A = np.empty(akfae__jybv, rjf__jbng)
            data = bodo.utils.conversion.unbox_if_timestamp(data)
            for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
                A[frs__opvw] = data
            return A
        return impl_timestamp
    return (lambda data, error_on_nonarray=True, use_nullable_array=None,
        scalar_to_arr_len=None: bodo.utils.conversion.coerce_to_ndarray(
        data, error_on_nonarray, use_nullable_array, scalar_to_arr_len))


def _is_str_dtype(dtype):
    return isinstance(dtype, bodo.libs.str_arr_ext.StringDtype) or isinstance(
        dtype, types.Function) and dtype.key[0
        ] == str or is_overload_constant_str(dtype) and get_overload_const_str(
        dtype) == 'str'


def fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True, from_series=
    False):
    return data


@overload(fix_arr_dtype, no_unliteral=True)
def overload_fix_arr_dtype(data, new_dtype, copy=None, nan_to_str=True,
    from_series=False):
    yln__fujma = not is_overload_none(copy)
    if is_overload_none(new_dtype):
        if yln__fujma:
            return (lambda data, new_dtype, copy=None, nan_to_str=True,
                from_series=False: data.copy())
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if _is_str_dtype(new_dtype):
        if isinstance(data.dtype, types.Integer):

            def impl_int_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                akfae__jybv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(akfae__jybv,
                    -1)
                for xmlzr__bscv in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, xmlzr__bscv):
                        if nan_to_str:
                            bodo.libs.str_arr_ext.str_arr_setitem_NA_str(A,
                                xmlzr__bscv)
                        else:
                            bodo.libs.array_kernels.setna(A, xmlzr__bscv)
                    else:
                        bodo.libs.str_arr_ext.str_arr_setitem_int_to_str(A,
                            xmlzr__bscv, data[xmlzr__bscv])
                return A
            return impl_int_str
        if data.dtype == bytes_type:

            def impl_binary(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                akfae__jybv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(akfae__jybv,
                    -1)
                for xmlzr__bscv in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, xmlzr__bscv):
                        bodo.libs.array_kernels.setna(A, xmlzr__bscv)
                    else:
                        A[xmlzr__bscv] = ''.join([chr(uqpr__xbj) for
                            uqpr__xbj in data[xmlzr__bscv]])
                return A
            return impl_binary
        if is_overload_true(from_series) and data.dtype in (bodo.
            datetime64ns, bodo.timedelta64ns):

            def impl_str_dt_series(data, new_dtype, copy=None, nan_to_str=
                True, from_series=False):
                numba.parfors.parfor.init_prange()
                akfae__jybv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(akfae__jybv,
                    -1)
                for xmlzr__bscv in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, xmlzr__bscv):
                        if nan_to_str:
                            A[xmlzr__bscv] = 'NaT'
                        else:
                            bodo.libs.array_kernels.setna(A, xmlzr__bscv)
                        continue
                    A[xmlzr__bscv] = str(box_if_dt64(data[xmlzr__bscv]))
                return A
            return impl_str_dt_series

            def impl_str_series(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                akfae__jybv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(akfae__jybv,
                    -1)
                for xmlzr__bscv in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, xmlzr__bscv):
                        if nan_to_str:
                            A[xmlzr__bscv] = '<NA>'
                        else:
                            bodo.libs.array_kernels.setna(A, xmlzr__bscv)
                        continue
                    A[xmlzr__bscv] = str(box_if_dt64(data[xmlzr__bscv]))
                return A
            return impl_str_series
        else:

            def impl_str_array(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                numba.parfors.parfor.init_prange()
                akfae__jybv = len(data)
                A = bodo.libs.str_arr_ext.pre_alloc_string_array(akfae__jybv,
                    -1)
                for xmlzr__bscv in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, xmlzr__bscv):
                        if nan_to_str:
                            A[xmlzr__bscv] = 'nan'
                        else:
                            bodo.libs.array_kernels.setna(A, xmlzr__bscv)
                        continue
                    A[xmlzr__bscv] = str(data[xmlzr__bscv])
                return A
            return impl_str_array
    if isinstance(new_dtype, bodo.hiframes.pd_categorical_ext.
        PDCategoricalDtype):

        def impl_cat_dtype(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            akfae__jybv = len(data)
            numba.parfors.parfor.init_prange()
            mgt__huqlz = (bodo.hiframes.pd_categorical_ext.
                get_label_dict_from_categories(new_dtype.categories.values))
            A = bodo.hiframes.pd_categorical_ext.alloc_categorical_array(
                akfae__jybv, new_dtype)
            hwm__pao = (bodo.hiframes.pd_categorical_ext.
                get_categorical_arr_codes(A))
            for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
                if bodo.libs.array_kernels.isna(data, frs__opvw):
                    bodo.libs.array_kernels.setna(A, frs__opvw)
                    continue
                val = data[frs__opvw]
                if val not in mgt__huqlz:
                    bodo.libs.array_kernels.setna(A, frs__opvw)
                    continue
                hwm__pao[frs__opvw] = mgt__huqlz[val]
            return A
        return impl_cat_dtype
    if is_overload_constant_str(new_dtype) and get_overload_const_str(new_dtype
        ) == 'category':

        def impl_category(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            cfnx__tnnap = bodo.libs.array_kernels.unique(data)
            cfnx__tnnap = bodo.allgatherv(cfnx__tnnap, False)
            cfnx__tnnap = pd.Series(cfnx__tnnap).dropna().sort_values().values
            fqii__okt = bodo.hiframes.pd_categorical_ext.init_cat_dtype(bodo
                .utils.conversion.index_from_array(cfnx__tnnap, None), 
                False, None)
            return bodo.utils.conversion.fix_arr_dtype(data, fqii__okt, copy)
        return impl_category
    nb_dtype = bodo.utils.typing.parse_dtype(new_dtype)
    if yln__fujma and data.dtype == nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.copy())
    if data.dtype == nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data)
    if isinstance(nb_dtype, bodo.libs.int_arr_ext.IntDtype):
        rjf__jbng = nb_dtype.dtype
        if isinstance(data.dtype, types.Float):

            def impl_float(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                akfae__jybv = len(data)
                numba.parfors.parfor.init_prange()
                xpyj__nduqb = bodo.libs.int_arr_ext.alloc_int_array(akfae__jybv
                    , rjf__jbng)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, frs__opvw):
                        bodo.libs.array_kernels.setna(xpyj__nduqb, frs__opvw)
                    else:
                        xpyj__nduqb[frs__opvw] = int(data[frs__opvw])
                return xpyj__nduqb
            return impl_float
        else:

            def impl(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                akfae__jybv = len(data)
                numba.parfors.parfor.init_prange()
                xpyj__nduqb = bodo.libs.int_arr_ext.alloc_int_array(akfae__jybv
                    , rjf__jbng)
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, frs__opvw):
                        bodo.libs.array_kernels.setna(xpyj__nduqb, frs__opvw)
                    else:
                        xpyj__nduqb[frs__opvw] = np.int64(data[frs__opvw])
                return xpyj__nduqb
            return impl
    if nb_dtype == bodo.libs.bool_arr_ext.boolean_dtype:

        def impl_bool(data, new_dtype, copy=None, nan_to_str=True,
            from_series=False):
            akfae__jybv = len(data)
            numba.parfors.parfor.init_prange()
            xpyj__nduqb = bodo.libs.bool_arr_ext.alloc_bool_array(akfae__jybv)
            for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
                if bodo.libs.array_kernels.isna(data, frs__opvw):
                    bodo.libs.array_kernels.setna(xpyj__nduqb, frs__opvw)
                else:
                    xpyj__nduqb[frs__opvw] = bool(data[frs__opvw])
            return xpyj__nduqb
        return impl_bool
    if nb_dtype == bodo.datetime64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_dt64_astype(
                    data)
            return impl_str
        if data == bodo.datetime_date_array_type:

            def impl_date(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return (bodo.hiframes.pd_timestamp_ext.
                    datetime_date_arr_to_dt64_arr(data))
            return impl_date
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            timedelta64ns, types.bool_]:

            def impl_numeric(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                akfae__jybv = len(data)
                numba.parfors.parfor.init_prange()
                qlvvl__jzuo = np.empty(akfae__jybv, dtype=np.dtype(
                    'datetime64[ns]'))
                for frs__opvw in numba.parfors.parfor.internal_prange(
                    akfae__jybv):
                    if bodo.libs.array_kernels.isna(data, frs__opvw):
                        bodo.libs.array_kernels.setna(qlvvl__jzuo, frs__opvw)
                    else:
                        qlvvl__jzuo[frs__opvw
                            ] = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(
                            np.int64(data[frs__opvw]))
                return qlvvl__jzuo
            return impl_numeric
    if nb_dtype == bodo.timedelta64ns:
        if data.dtype == bodo.string_type:

            def impl_str(data, new_dtype, copy=None, nan_to_str=True,
                from_series=False):
                return bodo.hiframes.pd_timestamp_ext.series_str_td64_astype(
                    data)
            return impl_str
        if isinstance(data.dtype, types.Number) or data.dtype in [bodo.
            datetime64ns, types.bool_]:
            if yln__fujma:

                def impl_numeric(data, new_dtype, copy=None, nan_to_str=
                    True, from_series=False):
                    akfae__jybv = len(data)
                    numba.parfors.parfor.init_prange()
                    qlvvl__jzuo = np.empty(akfae__jybv, dtype=np.dtype(
                        'timedelta64[ns]'))
                    for frs__opvw in numba.parfors.parfor.internal_prange(
                        akfae__jybv):
                        if bodo.libs.array_kernels.isna(data, frs__opvw):
                            bodo.libs.array_kernels.setna(qlvvl__jzuo,
                                frs__opvw)
                        else:
                            qlvvl__jzuo[frs__opvw] = (bodo.hiframes.
                                pd_timestamp_ext.integer_to_timedelta64(np.
                                int64(data[frs__opvw])))
                    return qlvvl__jzuo
                return impl_numeric
            else:
                return (lambda data, new_dtype, copy=None, nan_to_str=True,
                    from_series=False: data.view('int64'))
    if nb_dtype == types.int64 and data.dtype in [bodo.datetime64ns, bodo.
        timedelta64ns]:

        def impl_datelike_to_integer(data, new_dtype, copy=None, nan_to_str
            =True, from_series=False):
            akfae__jybv = len(data)
            numba.parfors.parfor.init_prange()
            A = np.empty(akfae__jybv, types.int64)
            for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
                if bodo.libs.array_kernels.isna(data, frs__opvw):
                    bodo.libs.array_kernels.setna(A, frs__opvw)
                else:
                    A[frs__opvw] = np.int64(data[frs__opvw])
            return A
        return impl_datelike_to_integer
    if data.dtype != nb_dtype:
        return (lambda data, new_dtype, copy=None, nan_to_str=True,
            from_series=False: data.astype(nb_dtype))
    raise BodoError(f'Conversion from {data} to {new_dtype} not supported yet')


def array_type_from_dtype(dtype):
    return dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))


@overload(array_type_from_dtype)
def overload_array_type_from_dtype(dtype):
    arr_type = dtype_to_array_type(bodo.utils.typing.parse_dtype(dtype))
    return lambda dtype: arr_type


@numba.jit
def flatten_array(A):
    bne__egf = []
    akfae__jybv = len(A)
    for frs__opvw in range(akfae__jybv):
        czlb__pmzj = A[frs__opvw]
        for binxp__rltmy in czlb__pmzj:
            bne__egf.append(binxp__rltmy)
    return bodo.utils.conversion.coerce_to_array(bne__egf)


def parse_datetimes_from_strings(data):
    return data


@overload(parse_datetimes_from_strings, no_unliteral=True)
def overload_parse_datetimes_from_strings(data):
    assert data == bodo.string_array_type

    def parse_impl(data):
        numba.parfors.parfor.init_prange()
        akfae__jybv = len(data)
        akbyk__ffv = np.empty(akfae__jybv, bodo.utils.conversion.NS_DTYPE)
        for frs__opvw in numba.parfors.parfor.internal_prange(akfae__jybv):
            akbyk__ffv[frs__opvw
                ] = bodo.hiframes.pd_timestamp_ext.parse_datetime_str(data[
                frs__opvw])
        return akbyk__ffv
    return parse_impl


def convert_to_dt64ns(data):
    return data


@overload(convert_to_dt64ns, no_unliteral=True)
def overload_convert_to_dt64ns(data):
    if data == bodo.hiframes.datetime_date_ext.datetime_date_array_type:
        return (lambda data: bodo.hiframes.pd_timestamp_ext.
            datetime_date_arr_to_dt64_arr(data))
    if data == types.Array(types.int64, 1, 'C'):
        return lambda data: data.view(bodo.utils.conversion.NS_DTYPE)
    if data == types.Array(types.NPDatetime('ns'), 1, 'C'):
        return lambda data: data
    if data == bodo.string_array_type:
        return lambda data: bodo.utils.conversion.parse_datetimes_from_strings(
            data)
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_td64ns(data):
    return data


@overload(convert_to_td64ns, no_unliteral=True)
def overload_convert_to_td64ns(data):
    if data == types.Array(types.int64, 1, 'C'):
        return lambda data: data.view(bodo.utils.conversion.TD_DTYPE)
    if data == types.Array(types.NPTimedelta('ns'), 1, 'C'):
        return lambda data: data
    if data == bodo.string_array_type:
        raise BodoError('conversion to timedelta from string not supported yet'
            )
    raise BodoError(f'invalid data type {data} for dt64 conversion')


def convert_to_index(data, name=None):
    return data


@overload(convert_to_index, no_unliteral=True)
def overload_convert_to_index(data, name=None):
    from bodo.hiframes.pd_index_ext import BinaryIndexType, CategoricalIndexType, DatetimeIndexType, NumericIndexType, RangeIndexType, StringIndexType, TimedeltaIndexType
    if isinstance(data, (RangeIndexType, NumericIndexType,
        DatetimeIndexType, TimedeltaIndexType, StringIndexType,
        BinaryIndexType, CategoricalIndexType, types.NoneType)):
        return lambda data, name=None: data

    def impl(data, name=None):
        boxer__fdlem = bodo.utils.conversion.coerce_to_array(data)
        return bodo.utils.conversion.index_from_array(boxer__fdlem, name)
    return impl


def force_convert_index(I1, I2):
    return I2


@overload(force_convert_index, no_unliteral=True)
def overload_force_convert_index(I1, I2):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I2, RangeIndexType):
        return lambda I1, I2: pd.RangeIndex(len(I1._data))
    return lambda I1, I2: I1


def index_from_array(data, name=None):
    return data


@overload(index_from_array, no_unliteral=True)
def overload_index_from_array(data, name=None):
    if data in [bodo.string_array_type, bodo.binary_array_type]:
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_binary_str_index(data, name))
    if (data == bodo.hiframes.datetime_date_ext.datetime_date_array_type or
        data.dtype == types.NPDatetime('ns')):
        return lambda data, name=None: pd.DatetimeIndex(data, name=name)
    if data.dtype == types.NPTimedelta('ns'):
        return lambda data, name=None: pd.TimedeltaIndex(data, name=name)
    if isinstance(data.dtype, (types.Integer, types.Float, types.Boolean)):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_numeric_index(data, name))
    if isinstance(data, bodo.libs.interval_arr_ext.IntervalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_interval_index(data, name))
    if isinstance(data, bodo.hiframes.pd_categorical_ext.CategoricalArrayType):
        return (lambda data, name=None: bodo.hiframes.pd_index_ext.
            init_categorical_index(data, name))
    raise BodoError(f'cannot convert {data} to Index')


def index_to_array(data):
    return data


@overload(index_to_array, no_unliteral=True)
def overload_index_to_array(I):
    from bodo.hiframes.pd_index_ext import RangeIndexType
    if isinstance(I, RangeIndexType):
        return lambda I: np.arange(I._start, I._stop, I._step)
    return lambda I: bodo.hiframes.pd_index_ext.get_index_data(I)


def false_if_none(val):
    return False if val is None else val


@overload(false_if_none, no_unliteral=True)
def overload_false_if_none(val):
    if is_overload_none(val):
        return lambda val: False
    return lambda val: val


def extract_name_if_none(data, name):
    return name


@overload(extract_name_if_none, no_unliteral=True)
def overload_extract_name_if_none(data, name):
    from bodo.hiframes.pd_index_ext import CategoricalIndexType, DatetimeIndexType, NumericIndexType, PeriodIndexType, TimedeltaIndexType
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(name):
        return lambda data, name: name
    if isinstance(data, (NumericIndexType, DatetimeIndexType,
        TimedeltaIndexType, PeriodIndexType, CategoricalIndexType)):
        return lambda data, name: bodo.hiframes.pd_index_ext.get_index_name(
            data)
    if isinstance(data, SeriesType):
        return lambda data, name: bodo.hiframes.pd_series_ext.get_series_name(
            data)
    return lambda data, name: name


def extract_index_if_none(data, index):
    return index


@overload(extract_index_if_none, no_unliteral=True)
def overload_extract_index_if_none(data, index):
    from bodo.hiframes.pd_series_ext import SeriesType
    if not is_overload_none(index):
        return lambda data, index: index
    if isinstance(data, SeriesType):
        return (lambda data, index: bodo.hiframes.pd_series_ext.
            get_series_index(data))
    return lambda data, index: bodo.hiframes.pd_index_ext.init_range_index(
        0, len(data), 1, None)


def box_if_dt64(val):
    return val


@overload(box_if_dt64, no_unliteral=True)
def overload_box_if_dt64(val):
    if val == types.NPDatetime('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_datetime64_to_timestamp(val))
    if val == types.NPTimedelta('ns'):
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            convert_numpy_timedelta64_to_pd_timedelta(val))
    return lambda val: val


def unbox_if_timestamp(val):
    return val


@overload(unbox_if_timestamp, no_unliteral=True)
def overload_unbox_if_timestamp(val):
    if val == bodo.hiframes.pd_timestamp_ext.pd_timestamp_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(val
            .value)
    if val == bodo.hiframes.datetime_datetime_ext.datetime_datetime_type:
        return lambda val: bodo.hiframes.pd_timestamp_ext.integer_to_dt64(pd
            .Timestamp(val).value)
    if val == bodo.hiframes.datetime_timedelta_ext.pd_timedelta_type:
        return (lambda val: bodo.hiframes.pd_timestamp_ext.
            integer_to_timedelta64(val.value))
    if val == types.Optional(bodo.hiframes.pd_timestamp_ext.pd_timestamp_type):

        def impl_optional(val):
            if val is None:
                pab__lyc = None
            else:
                pab__lyc = bodo.hiframes.pd_timestamp_ext.integer_to_dt64(bodo
                    .utils.indexing.unoptional(val).value)
            return pab__lyc
        return impl_optional
    if val == types.Optional(bodo.hiframes.datetime_timedelta_ext.
        pd_timedelta_type):

        def impl_optional_td(val):
            if val is None:
                pab__lyc = None
            else:
                pab__lyc = (bodo.hiframes.pd_timestamp_ext.
                    integer_to_timedelta64(bodo.utils.indexing.unoptional(
                    val).value))
            return pab__lyc
        return impl_optional_td
    return lambda val: val


def to_tuple(val):
    return val


@overload(to_tuple, no_unliteral=True)
def overload_to_tuple(val):
    if not isinstance(val, types.BaseTuple) and is_overload_constant_list(val):
        wjsi__mbh = len(val.types if isinstance(val, types.LiteralList) else
            get_overload_const_list(val))
        ohec__jrlp = 'def f(val):\n'
        npvxf__qsi = ','.join(f'val[{frs__opvw}]' for frs__opvw in range(
            wjsi__mbh))
        ohec__jrlp += f'  return ({npvxf__qsi},)\n'
        ejzwq__bhili = {}
        exec(ohec__jrlp, {}, ejzwq__bhili)
        impl = ejzwq__bhili['f']
        return impl
    assert isinstance(val, types.BaseTuple), 'tuple type expected'
    return lambda val: val


def get_array_if_series_or_index(data):
    return data


@overload(get_array_if_series_or_index)
def overload_get_array_if_series_or_index(data):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(data, SeriesType):
        return lambda data: bodo.hiframes.pd_series_ext.get_series_data(data)
    if bodo.hiframes.pd_index_ext.is_pd_index_type(data):
        return lambda data: bodo.utils.conversion.coerce_to_array(data)
    if isinstance(data, bodo.hiframes.pd_index_ext.HeterogeneousIndexType):
        if not is_heterogeneous_tuple_type(data.data):

            def impl(data):
                muziv__vex = bodo.hiframes.pd_index_ext.get_index_data(data)
                return bodo.utils.conversion.coerce_to_array(muziv__vex)
            return impl

        def impl(data):
            return bodo.hiframes.pd_index_ext.get_index_data(data)
        return impl
    return lambda data: data


def extract_index_array(A):
    return np.arange(len(A))


@overload(extract_index_array, no_unliteral=True)
def overload_extract_index_array(A):
    from bodo.hiframes.pd_series_ext import SeriesType
    if isinstance(A, SeriesType):

        def impl(A):
            index = bodo.hiframes.pd_series_ext.get_series_index(A)
            ytkc__rykfr = bodo.utils.conversion.coerce_to_array(index)
            return ytkc__rykfr
        return impl
    return lambda A: np.arange(len(A))


def ensure_contig_if_np(arr):
    return np.ascontiguousarray(arr)


@overload(ensure_contig_if_np, no_unliteral=True)
def overload_ensure_contig_if_np(arr):
    if isinstance(arr, types.Array):
        return lambda arr: np.ascontiguousarray(arr)
    return lambda arr: arr


def struct_if_heter_dict(values, names):
    return {odvgo__ttlf: lmku__lkaw for odvgo__ttlf, lmku__lkaw in zip(
        names, values)}


@overload(struct_if_heter_dict, no_unliteral=True)
def overload_struct_if_heter_dict(values, names):
    if not types.is_homogeneous(*values.types):
        return lambda values, names: bodo.libs.struct_arr_ext.init_struct(
            values, names)
    wyjfg__xkmz = len(values.types)
    ohec__jrlp = 'def f(values, names):\n'
    npvxf__qsi = ','.join("'{}': values[{}]".format(get_overload_const_str(
        names.types[frs__opvw]), frs__opvw) for frs__opvw in range(wyjfg__xkmz)
        )
    ohec__jrlp += '  return {{{}}}\n'.format(npvxf__qsi)
    ejzwq__bhili = {}
    exec(ohec__jrlp, {}, ejzwq__bhili)
    impl = ejzwq__bhili['f']
    return impl
