"""
helper data structures and functions for shuffle (alltoall).
"""
import os
from collections import namedtuple
import numba
import numpy as np
from numba import generated_jit
from numba.core import types
from numba.extending import overload
import bodo
from bodo.libs.array_item_arr_ext import offset_type
from bodo.libs.binary_arr_ext import binary_array_type, bytes_type
from bodo.libs.bool_arr_ext import BooleanArrayType, boolean_array
from bodo.libs.int_arr_ext import IntegerArrayType
from bodo.libs.str_arr_ext import convert_len_arr_to_offset, convert_len_arr_to_offset32, get_bit_bitmap, get_data_ptr, get_null_bitmap_ptr, get_offset_ptr, get_str_arr_item_length, num_total_chars, print_str_arr, set_bit_to, string_array_type
from bodo.libs.str_ext import string_type
from bodo.libs.timsort import getitem_arr_tup, setitem_arr_tup
from bodo.utils.utils import alloc_arr_tup, get_ctypes_ptr, numba_to_c_type
PreShuffleMeta = namedtuple('PreShuffleMeta',
    'send_counts, send_counts_char_tup, send_arr_lens_tup, send_arr_nulls_tup')
ShuffleMeta = namedtuple('ShuffleMeta',
    'send_counts, recv_counts, n_send, n_out, send_disp, recv_disp, send_disp_nulls, recv_disp_nulls, tmp_offset, send_buff_tup, out_arr_tup, send_counts_char_tup, recv_counts_char_tup, send_arr_lens_tup, send_arr_nulls_tup, send_arr_chars_tup, send_disp_char_tup, recv_disp_char_tup, tmp_offset_char_tup, send_arr_chars_arr_tup'
    )


def alloc_pre_shuffle_metadata(arr, data, n_pes, is_contig):
    return PreShuffleMeta(np.zeros(n_pes, np.int32), ())


@overload(alloc_pre_shuffle_metadata, no_unliteral=True)
def alloc_pre_shuffle_metadata_overload(key_arrs, data, n_pes, is_contig):
    mwnv__woqcz = 'def f(key_arrs, data, n_pes, is_contig):\n'
    mwnv__woqcz += '  send_counts = np.zeros(n_pes, np.int32)\n'
    jtwic__xhlrk = len(key_arrs.types)
    ygxja__hyui = jtwic__xhlrk + len(data.types)
    for i, efsk__xuqrq in enumerate(key_arrs.types + data.types):
        mwnv__woqcz += '  arr = key_arrs[{}]\n'.format(i
            ) if i < jtwic__xhlrk else """  arr = data[{}]
""".format(i -
            jtwic__xhlrk)
        if efsk__xuqrq in [string_array_type, binary_array_type]:
            mwnv__woqcz += (
                '  send_counts_char_{} = np.zeros(n_pes, np.int32)\n'.format(i)
                )
            mwnv__woqcz += ('  send_arr_lens_{} = np.empty(0, np.uint32)\n'
                .format(i))
            mwnv__woqcz += '  if is_contig:\n'
            mwnv__woqcz += (
                '    send_arr_lens_{} = np.empty(len(arr), np.uint32)\n'.
                format(i))
        else:
            mwnv__woqcz += '  send_counts_char_{} = None\n'.format(i)
            mwnv__woqcz += '  send_arr_lens_{} = None\n'.format(i)
        if is_null_masked_type(efsk__xuqrq):
            mwnv__woqcz += ('  send_arr_nulls_{} = np.empty(0, np.uint8)\n'
                .format(i))
            mwnv__woqcz += '  if is_contig:\n'
            mwnv__woqcz += '    n_bytes = (len(arr) + 7) >> 3\n'
            mwnv__woqcz += (
                '    send_arr_nulls_{} = np.full(n_bytes + 2 * n_pes, 255, np.uint8)\n'
                .format(i))
        else:
            mwnv__woqcz += '  send_arr_nulls_{} = None\n'.format(i)
    unk__lgjfs = ', '.join('send_counts_char_{}'.format(i) for i in range(
        ygxja__hyui))
    uaqzr__dmd = ', '.join('send_arr_lens_{}'.format(i) for i in range(
        ygxja__hyui))
    rde__gvj = ', '.join('send_arr_nulls_{}'.format(i) for i in range(
        ygxja__hyui))
    ufdm__jjlsj = ',' if ygxja__hyui == 1 else ''
    mwnv__woqcz += (
        '  return PreShuffleMeta(send_counts, ({}{}), ({}{}), ({}{}))\n'.
        format(unk__lgjfs, ufdm__jjlsj, uaqzr__dmd, ufdm__jjlsj, rde__gvj,
        ufdm__jjlsj))
    qxrlk__atgw = {}
    exec(mwnv__woqcz, {'np': np, 'PreShuffleMeta': PreShuffleMeta}, qxrlk__atgw
        )
    xonod__tujky = qxrlk__atgw['f']
    return xonod__tujky


def update_shuffle_meta(pre_shuffle_meta, node_id, ind, key_arrs, data,
    is_contig=True, padded_bits=0):
    pre_shuffle_meta.send_counts[node_id] += 1


@overload(update_shuffle_meta, no_unliteral=True)
def update_shuffle_meta_overload(pre_shuffle_meta, node_id, ind, key_arrs,
    data, is_contig=True, padded_bits=0):
    yfh__ckhkg = 'BODO_DEBUG_LEVEL'
    mxb__booxq = 0
    try:
        mxb__booxq = int(os.environ[yfh__ckhkg])
    except:
        pass
    mwnv__woqcz = """def f(pre_shuffle_meta, node_id, ind, key_arrs, data, is_contig=True, padded_bits=0):
"""
    mwnv__woqcz += '  pre_shuffle_meta.send_counts[node_id] += 1\n'
    if mxb__booxq > 0:
        mwnv__woqcz += ('  if pre_shuffle_meta.send_counts[node_id] >= {}:\n'
            .format(bodo.libs.distributed_api.INT_MAX))
        mwnv__woqcz += "    print('large shuffle error')\n"
    jtwic__xhlrk = len(key_arrs.types)
    for i, efsk__xuqrq in enumerate(key_arrs.types + data.types):
        if efsk__xuqrq in (string_type, string_array_type, bytes_type,
            binary_array_type):
            arr = 'key_arrs[{}]'.format(i
                ) if i < jtwic__xhlrk else 'data[{}]'.format(i - jtwic__xhlrk)
            mwnv__woqcz += ('  n_chars = get_str_arr_item_length({}, ind)\n'
                .format(arr))
            mwnv__woqcz += (
                '  pre_shuffle_meta.send_counts_char_tup[{}][node_id] += n_chars\n'
                .format(i))
            if mxb__booxq > 0:
                mwnv__woqcz += (
                    '  if pre_shuffle_meta.send_counts_char_tup[{}][node_id] >= {}:\n'
                    .format(i, bodo.libs.distributed_api.INT_MAX))
                mwnv__woqcz += "    print('large shuffle error')\n"
            mwnv__woqcz += '  if is_contig:\n'
            mwnv__woqcz += (
                '    pre_shuffle_meta.send_arr_lens_tup[{}][ind] = n_chars\n'
                .format(i))
        if is_null_masked_type(efsk__xuqrq):
            mwnv__woqcz += '  if is_contig:\n'
            mwnv__woqcz += (
                '    out_bitmap = pre_shuffle_meta.send_arr_nulls_tup[{}].ctypes\n'
                .format(i))
            if i < jtwic__xhlrk:
                mwnv__woqcz += (
                    '    bit_val = get_mask_bit(key_arrs[{}], ind)\n'.format(i)
                    )
            else:
                mwnv__woqcz += ('    bit_val = get_mask_bit(data[{}], ind)\n'
                    .format(i - jtwic__xhlrk))
            mwnv__woqcz += (
                '    set_bit_to(out_bitmap, padded_bits + ind, bit_val)\n')
    qxrlk__atgw = {}
    exec(mwnv__woqcz, {'set_bit_to': set_bit_to, 'get_bit_bitmap':
        get_bit_bitmap, 'get_null_bitmap_ptr': get_null_bitmap_ptr,
        'getitem_arr_tup': getitem_arr_tup, 'get_mask_bit': get_mask_bit,
        'get_str_arr_item_length': get_str_arr_item_length}, qxrlk__atgw)
    uwr__emwc = qxrlk__atgw['f']
    return uwr__emwc


@numba.njit
def calc_disp_nulls(arr):
    pjv__szts = np.empty_like(arr)
    pjv__szts[0] = 0
    for i in range(1, len(arr)):
        xgz__rcmz = arr[i - 1] + 7 >> 3
        pjv__szts[i] = pjv__szts[i - 1] + xgz__rcmz
    return pjv__szts


def finalize_shuffle_meta(arrs, data, pre_shuffle_meta, n_pes, is_contig,
    init_vals=()):
    return ShuffleMeta()


@overload(finalize_shuffle_meta, no_unliteral=True)
def finalize_shuffle_meta_overload(key_arrs, data, pre_shuffle_meta, n_pes,
    is_contig, init_vals=()):
    mwnv__woqcz = (
        'def f(key_arrs, data, pre_shuffle_meta, n_pes, is_contig, init_vals=()):\n'
        )
    mwnv__woqcz += '  send_counts = pre_shuffle_meta.send_counts\n'
    mwnv__woqcz += '  recv_counts = np.empty(n_pes, np.int32)\n'
    mwnv__woqcz += '  tmp_offset = np.zeros(n_pes, np.int32)\n'
    mwnv__woqcz += (
        '  bodo.libs.distributed_api.alltoall(send_counts, recv_counts, 1)\n')
    mwnv__woqcz += '  n_out = recv_counts.sum()\n'
    mwnv__woqcz += '  n_send = send_counts.sum()\n'
    mwnv__woqcz += '  send_disp = bodo.ir.join.calc_disp(send_counts)\n'
    mwnv__woqcz += '  recv_disp = bodo.ir.join.calc_disp(recv_counts)\n'
    mwnv__woqcz += '  send_disp_nulls = calc_disp_nulls(send_counts)\n'
    mwnv__woqcz += '  recv_disp_nulls = calc_disp_nulls(recv_counts)\n'
    jtwic__xhlrk = len(key_arrs.types)
    ygxja__hyui = len(key_arrs.types + data.types)
    for i, efsk__xuqrq in enumerate(key_arrs.types + data.types):
        mwnv__woqcz += '  arr = key_arrs[{}]\n'.format(i
            ) if i < jtwic__xhlrk else """  arr = data[{}]
""".format(i -
            jtwic__xhlrk)
        if efsk__xuqrq in [string_array_type, binary_array_type]:
            if efsk__xuqrq == string_array_type:
                ume__enhs = 'bodo.libs.str_arr_ext.pre_alloc_string_array'
            else:
                ume__enhs = 'bodo.libs.binary_arr_ext.pre_alloc_binary_array'
            mwnv__woqcz += '  send_buff_{} = None\n'.format(i)
            mwnv__woqcz += (
                '  send_counts_char_{} = pre_shuffle_meta.send_counts_char_tup[{}]\n'
                .format(i, i))
            mwnv__woqcz += (
                '  recv_counts_char_{} = np.empty(n_pes, np.int32)\n'.format(i)
                )
            mwnv__woqcz += (
                """  bodo.libs.distributed_api.alltoall(send_counts_char_{}, recv_counts_char_{}, 1)
"""
                .format(i, i))
            mwnv__woqcz += ('  n_all_chars = recv_counts_char_{}.sum()\n'.
                format(i))
            mwnv__woqcz += '  out_arr_{} = {}(n_out, n_all_chars)\n'.format(i,
                ume__enhs)
            mwnv__woqcz += (
                '  send_disp_char_{} = bodo.ir.join.calc_disp(send_counts_char_{})\n'
                .format(i, i))
            mwnv__woqcz += (
                '  recv_disp_char_{} = bodo.ir.join.calc_disp(recv_counts_char_{})\n'
                .format(i, i))
            mwnv__woqcz += (
                '  tmp_offset_char_{} = np.zeros(n_pes, np.int32)\n'.format(i))
            mwnv__woqcz += (
                '  send_arr_lens_{} = pre_shuffle_meta.send_arr_lens_tup[{}]\n'
                .format(i, i))
            mwnv__woqcz += ('  send_arr_chars_arr_{} = np.empty(0, np.uint8)\n'
                .format(i))
            mwnv__woqcz += (
                '  send_arr_chars_{} = get_ctypes_ptr(get_data_ptr(arr))\n'
                .format(i))
            mwnv__woqcz += '  if not is_contig:\n'
            mwnv__woqcz += (
                '    send_arr_lens_{} = np.empty(n_send, np.uint32)\n'.
                format(i))
            mwnv__woqcz += ('    s_n_all_chars = send_counts_char_{}.sum()\n'
                .format(i))
            mwnv__woqcz += (
                '    send_arr_chars_arr_{} = np.empty(s_n_all_chars, np.uint8)\n'
                .format(i))
            mwnv__woqcz += (
                '    send_arr_chars_{} = get_ctypes_ptr(send_arr_chars_arr_{}.ctypes)\n'
                .format(i, i))
        else:
            assert isinstance(efsk__xuqrq, (types.Array, IntegerArrayType,
                BooleanArrayType, bodo.CategoricalArrayType))
            mwnv__woqcz += (
                '  out_arr_{} = bodo.utils.utils.alloc_type(n_out, arr)\n'.
                format(i))
            mwnv__woqcz += '  send_buff_{} = arr\n'.format(i)
            mwnv__woqcz += '  if not is_contig:\n'
            if i >= jtwic__xhlrk and init_vals != ():
                mwnv__woqcz += (
                    """    send_buff_{} = bodo.utils.utils.full_type(n_send, init_vals[{}], arr)
"""
                    .format(i, i - jtwic__xhlrk))
            else:
                mwnv__woqcz += (
                    '    send_buff_{} = bodo.utils.utils.alloc_type(n_send, arr)\n'
                    .format(i))
            mwnv__woqcz += '  send_counts_char_{} = None\n'.format(i)
            mwnv__woqcz += '  recv_counts_char_{} = None\n'.format(i)
            mwnv__woqcz += '  send_arr_lens_{} = None\n'.format(i)
            mwnv__woqcz += '  send_arr_chars_{} = None\n'.format(i)
            mwnv__woqcz += '  send_disp_char_{} = None\n'.format(i)
            mwnv__woqcz += '  recv_disp_char_{} = None\n'.format(i)
            mwnv__woqcz += '  tmp_offset_char_{} = None\n'.format(i)
            mwnv__woqcz += '  send_arr_chars_arr_{} = None\n'.format(i)
        if is_null_masked_type(efsk__xuqrq):
            mwnv__woqcz += (
                '  send_arr_nulls_{} = pre_shuffle_meta.send_arr_nulls_tup[{}]\n'
                .format(i, i))
            mwnv__woqcz += '  if not is_contig:\n'
            mwnv__woqcz += '    n_bytes = (n_send + 7) >> 3\n'
            mwnv__woqcz += (
                '    send_arr_nulls_{} = np.full(n_bytes + 2 * n_pes, 255, np.uint8)\n'
                .format(i))
        else:
            mwnv__woqcz += '  send_arr_nulls_{} = None\n'.format(i)
    fobha__rnsl = ', '.join('send_buff_{}'.format(i) for i in range(
        ygxja__hyui))
    uody__bbz = ', '.join('out_arr_{}'.format(i) for i in range(ygxja__hyui))
    kqsk__anld = ',' if ygxja__hyui == 1 else ''
    yre__zjuv = ', '.join('send_counts_char_{}'.format(i) for i in range(
        ygxja__hyui))
    ming__xpieq = ', '.join('recv_counts_char_{}'.format(i) for i in range(
        ygxja__hyui))
    carss__tidiz = ', '.join('send_arr_lens_{}'.format(i) for i in range(
        ygxja__hyui))
    ziqa__stosu = ', '.join('send_arr_nulls_{}'.format(i) for i in range(
        ygxja__hyui))
    vjmi__kbe = ', '.join('send_arr_chars_{}'.format(i) for i in range(
        ygxja__hyui))
    dattp__fozti = ', '.join('send_disp_char_{}'.format(i) for i in range(
        ygxja__hyui))
    gzu__gwy = ', '.join('recv_disp_char_{}'.format(i) for i in range(
        ygxja__hyui))
    lyz__lwqj = ', '.join('tmp_offset_char_{}'.format(i) for i in range(
        ygxja__hyui))
    bggo__rgoqx = ', '.join('send_arr_chars_arr_{}'.format(i) for i in
        range(ygxja__hyui))
    mwnv__woqcz += (
        """  return ShuffleMeta(send_counts, recv_counts, n_send, n_out, send_disp, recv_disp, send_disp_nulls, recv_disp_nulls, tmp_offset, ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), ({}{}), )
"""
        .format(fobha__rnsl, kqsk__anld, uody__bbz, kqsk__anld, yre__zjuv,
        kqsk__anld, ming__xpieq, kqsk__anld, carss__tidiz, kqsk__anld,
        ziqa__stosu, kqsk__anld, vjmi__kbe, kqsk__anld, dattp__fozti,
        kqsk__anld, gzu__gwy, kqsk__anld, lyz__lwqj, kqsk__anld,
        bggo__rgoqx, kqsk__anld))
    qxrlk__atgw = {}
    exec(mwnv__woqcz, {'np': np, 'bodo': bodo, 'num_total_chars':
        num_total_chars, 'get_data_ptr': get_data_ptr, 'ShuffleMeta':
        ShuffleMeta, 'get_ctypes_ptr': get_ctypes_ptr, 'calc_disp_nulls':
        calc_disp_nulls}, qxrlk__atgw)
    ytemk__tgo = qxrlk__atgw['f']
    return ytemk__tgo


def alltoallv_tup(arrs, shuffle_meta, key_arrs):
    return arrs


@overload(alltoallv_tup, no_unliteral=True)
def alltoallv_tup_overload(arrs, meta, key_arrs):
    jtwic__xhlrk = len(key_arrs.types)
    mwnv__woqcz = 'def f(arrs, meta, key_arrs):\n'
    if any(is_null_masked_type(t) for t in arrs.types):
        mwnv__woqcz += (
            '  send_counts_nulls = np.empty(len(meta.send_counts), np.int32)\n'
            )
        mwnv__woqcz += '  for i in range(len(meta.send_counts)):\n'
        mwnv__woqcz += (
            '    send_counts_nulls[i] = (meta.send_counts[i] + 7) >> 3\n')
        mwnv__woqcz += (
            '  recv_counts_nulls = np.empty(len(meta.recv_counts), np.int32)\n'
            )
        mwnv__woqcz += '  for i in range(len(meta.recv_counts)):\n'
        mwnv__woqcz += (
            '    recv_counts_nulls[i] = (meta.recv_counts[i] + 7) >> 3\n')
        mwnv__woqcz += (
            '  tmp_null_bytes = np.empty(recv_counts_nulls.sum(), np.uint8)\n')
    mwnv__woqcz += '  lens = np.empty(meta.n_out, np.uint32)\n'
    for i, efsk__xuqrq in enumerate(arrs.types):
        if isinstance(efsk__xuqrq, (types.Array, IntegerArrayType,
            BooleanArrayType, bodo.CategoricalArrayType)):
            mwnv__woqcz += (
                """  bodo.libs.distributed_api.alltoallv(meta.send_buff_tup[{}], meta.out_arr_tup[{}], meta.send_counts,meta.recv_counts, meta.send_disp, meta.recv_disp)
"""
                .format(i, i))
        else:
            assert efsk__xuqrq in [string_array_type, binary_array_type]
            mwnv__woqcz += (
                '  offset_ptr_{} = get_offset_ptr(meta.out_arr_tup[{}])\n'.
                format(i, i))
            if offset_type.bitwidth == 32:
                mwnv__woqcz += (
                    """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_lens_tup[{}].ctypes, offset_ptr_{}, meta.send_counts.ctypes, meta.recv_counts.ctypes, meta.send_disp.ctypes, meta.recv_disp.ctypes, int32_typ_enum)
"""
                    .format(i, i))
            else:
                mwnv__woqcz += (
                    """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_lens_tup[{}].ctypes, lens.ctypes, meta.send_counts.ctypes, meta.recv_counts.ctypes, meta.send_disp.ctypes, meta.recv_disp.ctypes, int32_typ_enum)
"""
                    .format(i))
            mwnv__woqcz += (
                """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_chars_tup[{}], get_data_ptr(meta.out_arr_tup[{}]), meta.send_counts_char_tup[{}].ctypes,meta.recv_counts_char_tup[{}].ctypes, meta.send_disp_char_tup[{}].ctypes,meta.recv_disp_char_tup[{}].ctypes, char_typ_enum)
"""
                .format(i, i, i, i, i, i))
            if offset_type.bitwidth == 32:
                mwnv__woqcz += (
                    '  convert_len_arr_to_offset32(offset_ptr_{}, meta.n_out)\n'
                    .format(i))
            else:
                mwnv__woqcz += (
                    """  convert_len_arr_to_offset(lens.ctypes, offset_ptr_{}, meta.n_out)
"""
                    .format(i))
        if is_null_masked_type(efsk__xuqrq):
            mwnv__woqcz += (
                '  null_bitmap_ptr_{} = get_arr_null_ptr(meta.out_arr_tup[{}])\n'
                .format(i, i))
            mwnv__woqcz += (
                """  bodo.libs.distributed_api.c_alltoallv(meta.send_arr_nulls_tup[{}].ctypes, tmp_null_bytes.ctypes, send_counts_nulls.ctypes, recv_counts_nulls.ctypes, meta.send_disp_nulls.ctypes, meta.recv_disp_nulls.ctypes, char_typ_enum)
"""
                .format(i))
            mwnv__woqcz += (
                """  copy_gathered_null_bytes(null_bitmap_ptr_{}, tmp_null_bytes, recv_counts_nulls, meta.recv_counts)
"""
                .format(i))
    mwnv__woqcz += '  return ({}{})\n'.format(','.join([
        'meta.out_arr_tup[{}]'.format(i) for i in range(arrs.count)]), ',' if
        arrs.count == 1 else '')
    dvlnx__int = np.int32(numba_to_c_type(types.int32))
    cogym__yjnx = np.int32(numba_to_c_type(types.uint8))
    qxrlk__atgw = {}
    exec(mwnv__woqcz, {'np': np, 'bodo': bodo, 'get_offset_ptr':
        get_offset_ptr, 'get_data_ptr': get_data_ptr, 'int32_typ_enum':
        dvlnx__int, 'char_typ_enum': cogym__yjnx,
        'convert_len_arr_to_offset': convert_len_arr_to_offset,
        'convert_len_arr_to_offset32': convert_len_arr_to_offset32,
        'copy_gathered_null_bytes': bodo.libs.distributed_api.
        copy_gathered_null_bytes, 'get_arr_null_ptr': get_arr_null_ptr,
        'print_str_arr': print_str_arr}, qxrlk__atgw)
    deld__phi = qxrlk__atgw['f']
    return deld__phi


def shuffle_with_index_impl(key_arrs, node_arr, data):
    n_pes = bodo.libs.distributed_api.get_size()
    pre_shuffle_meta = alloc_pre_shuffle_metadata(key_arrs, data, n_pes, False)
    htrm__gxjg = len(key_arrs[0])
    orig_indices = np.arange(htrm__gxjg)
    bdkgq__keuok = np.empty(htrm__gxjg, np.int32)
    for i in range(htrm__gxjg):
        val = getitem_arr_tup_single(key_arrs, i)
        node_id = node_arr[i]
        bdkgq__keuok[i] = node_id
        update_shuffle_meta(pre_shuffle_meta, node_id, i, key_arrs, data, False
            )
    shuffle_meta = finalize_shuffle_meta(key_arrs, data, pre_shuffle_meta,
        n_pes, False)
    for i in range(htrm__gxjg):
        val = getitem_arr_tup_single(key_arrs, i)
        node_id = bdkgq__keuok[i]
        vge__lnbbn = bodo.ir.join.write_send_buff(shuffle_meta, node_id, i,
            key_arrs, data)
        orig_indices[vge__lnbbn] = i
        shuffle_meta.tmp_offset[node_id] += 1
    recvs = alltoallv_tup(key_arrs + data, shuffle_meta, key_arrs)
    xffjk__qumyx = _get_keys_tup(recvs, key_arrs)
    glki__cyamo = _get_data_tup(recvs, key_arrs)
    return xffjk__qumyx, glki__cyamo, orig_indices, shuffle_meta


@generated_jit(nopython=True, cache=True)
def shuffle_with_index(key_arrs, node_arr, data):
    return shuffle_with_index_impl


@numba.njit(cache=True)
def reverse_shuffle(data, orig_indices, shuffle_meta):
    uody__bbz = alloc_arr_tup(shuffle_meta.n_send, data)
    buw__gnqqj = ShuffleMeta(shuffle_meta.recv_counts, shuffle_meta.
        send_counts, shuffle_meta.n_out, shuffle_meta.n_send, shuffle_meta.
        recv_disp, shuffle_meta.send_disp, shuffle_meta.recv_disp_nulls,
        shuffle_meta.send_disp_nulls, shuffle_meta.tmp_offset, data,
        uody__bbz, shuffle_meta.recv_counts_char_tup, shuffle_meta.
        send_counts_char_tup, shuffle_meta.send_arr_lens_tup, shuffle_meta.
        send_arr_nulls_tup, shuffle_meta.send_arr_chars_tup, shuffle_meta.
        recv_disp_char_tup, shuffle_meta.send_disp_char_tup, shuffle_meta.
        tmp_offset_char_tup, shuffle_meta.send_arr_chars_arr_tup)
    uody__bbz = alltoallv_tup(data, buw__gnqqj, ())
    ofb__moale = alloc_arr_tup(shuffle_meta.n_send, data)
    for i in range(len(orig_indices)):
        setitem_arr_tup(ofb__moale, orig_indices[i], getitem_arr_tup(
            uody__bbz, i))
    return ofb__moale


def _get_keys_tup(recvs, key_arrs):
    return recvs[:len(key_arrs)]


@overload(_get_keys_tup, no_unliteral=True)
def _get_keys_tup_overload(recvs, key_arrs):
    jtwic__xhlrk = len(key_arrs.types)
    mwnv__woqcz = 'def f(recvs, key_arrs):\n'
    kcehl__nremh = ','.join('recvs[{}]'.format(i) for i in range(jtwic__xhlrk))
    mwnv__woqcz += '  return ({}{})\n'.format(kcehl__nremh, ',' if 
        jtwic__xhlrk == 1 else '')
    qxrlk__atgw = {}
    exec(mwnv__woqcz, {}, qxrlk__atgw)
    xnn__zbdtz = qxrlk__atgw['f']
    return xnn__zbdtz


def _get_data_tup(recvs, key_arrs):
    return recvs[len(key_arrs):]


@overload(_get_data_tup, no_unliteral=True)
def _get_data_tup_overload(recvs, key_arrs):
    jtwic__xhlrk = len(key_arrs.types)
    ygxja__hyui = len(recvs.types)
    oifi__dwwwi = ygxja__hyui - jtwic__xhlrk
    mwnv__woqcz = 'def f(recvs, key_arrs):\n'
    kcehl__nremh = ','.join('recvs[{}]'.format(i) for i in range(
        jtwic__xhlrk, ygxja__hyui))
    mwnv__woqcz += '  return ({}{})\n'.format(kcehl__nremh, ',' if 
        oifi__dwwwi == 1 else '')
    qxrlk__atgw = {}
    exec(mwnv__woqcz, {}, qxrlk__atgw)
    xnn__zbdtz = qxrlk__atgw['f']
    return xnn__zbdtz


def getitem_arr_tup_single(arrs, i):
    return arrs[0][i]


@overload(getitem_arr_tup_single, no_unliteral=True)
def getitem_arr_tup_single_overload(arrs, i):
    if len(arrs.types) == 1:
        return lambda arrs, i: arrs[0][i]
    return lambda arrs, i: getitem_arr_tup(arrs, i)


def val_to_tup(val):
    return val,


@overload(val_to_tup, no_unliteral=True)
def val_to_tup_overload(val):
    if isinstance(val, types.BaseTuple):
        return lambda val: val
    return lambda val: (val,)


def is_null_masked_type(t):
    return t in (string_type, string_array_type, bytes_type,
        binary_array_type, boolean_array) or isinstance(t, IntegerArrayType)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_mask_bit(arr, i):
    if arr in [string_array_type, binary_array_type]:
        return lambda arr, i: get_bit_bitmap(get_null_bitmap_ptr(arr), i)
    assert isinstance(arr, IntegerArrayType) or arr == boolean_array
    return lambda arr, i: bodo.libs.int_arr_ext.get_bit_bitmap_arr(arr.
        _null_bitmap, i)


@numba.generated_jit(nopython=True, no_cpython_wrapper=True)
def get_arr_null_ptr(arr):
    if arr in [string_array_type, binary_array_type]:
        return lambda arr: get_null_bitmap_ptr(arr)
    assert isinstance(arr, IntegerArrayType) or arr == boolean_array
    return lambda arr: arr._null_bitmap.ctypes
