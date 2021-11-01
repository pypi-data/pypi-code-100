import numpy as np
import pandas as pd
import numba
from numba.extending import overload
from bodo.utils.utils import alloc_arr_tup
MIN_MERGE = 32


@numba.njit(no_cpython_wrapper=True, cache=True)
def sort(key_arrs, lo, hi, data):
    uipvj__kkxen = hi - lo
    if uipvj__kkxen < 2:
        return
    if uipvj__kkxen < MIN_MERGE:
        ixgy__ujsny = countRunAndMakeAscending(key_arrs, lo, hi, data)
        binarySort(key_arrs, lo, hi, lo + ixgy__ujsny, data)
        return
    stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop = (
        init_sort_start(key_arrs, data))
    wixmd__ldjct = minRunLength(uipvj__kkxen)
    while True:
        iuty__hfx = countRunAndMakeAscending(key_arrs, lo, hi, data)
        if iuty__hfx < wixmd__ldjct:
            onqfx__owi = (uipvj__kkxen if uipvj__kkxen <= wixmd__ldjct else
                wixmd__ldjct)
            binarySort(key_arrs, lo, lo + onqfx__owi, lo + iuty__hfx, data)
            iuty__hfx = onqfx__owi
        stackSize = pushRun(stackSize, runBase, runLen, lo, iuty__hfx)
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeCollapse(
            stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
            tmp_data, minGallop)
        lo += iuty__hfx
        uipvj__kkxen -= iuty__hfx
        if uipvj__kkxen == 0:
            break
    assert lo == hi
    stackSize, tmpLength, tmp, tmp_data, minGallop = mergeForceCollapse(
        stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
        tmp_data, minGallop)
    assert stackSize == 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def binarySort(key_arrs, lo, hi, start, data):
    assert lo <= start and start <= hi
    if start == lo:
        start += 1
    while start < hi:
        bvi__rly = getitem_arr_tup(key_arrs, start)
        jymmp__gzjbb = getitem_arr_tup(data, start)
        blk__mps = lo
        xlgdz__edj = start
        assert blk__mps <= xlgdz__edj
        while blk__mps < xlgdz__edj:
            feui__uul = blk__mps + xlgdz__edj >> 1
            if bvi__rly < getitem_arr_tup(key_arrs, feui__uul):
                xlgdz__edj = feui__uul
            else:
                blk__mps = feui__uul + 1
        assert blk__mps == xlgdz__edj
        n = start - blk__mps
        copyRange_tup(key_arrs, blk__mps, key_arrs, blk__mps + 1, n)
        copyRange_tup(data, blk__mps, data, blk__mps + 1, n)
        setitem_arr_tup(key_arrs, blk__mps, bvi__rly)
        setitem_arr_tup(data, blk__mps, jymmp__gzjbb)
        start += 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def countRunAndMakeAscending(key_arrs, lo, hi, data):
    assert lo < hi
    gaqq__pbe = lo + 1
    if gaqq__pbe == hi:
        return 1
    if getitem_arr_tup(key_arrs, gaqq__pbe) < getitem_arr_tup(key_arrs, lo):
        gaqq__pbe += 1
        while gaqq__pbe < hi and getitem_arr_tup(key_arrs, gaqq__pbe
            ) < getitem_arr_tup(key_arrs, gaqq__pbe - 1):
            gaqq__pbe += 1
        reverseRange(key_arrs, lo, gaqq__pbe, data)
    else:
        gaqq__pbe += 1
        while gaqq__pbe < hi and getitem_arr_tup(key_arrs, gaqq__pbe
            ) >= getitem_arr_tup(key_arrs, gaqq__pbe - 1):
            gaqq__pbe += 1
    return gaqq__pbe - lo


@numba.njit(no_cpython_wrapper=True, cache=True)
def reverseRange(key_arrs, lo, hi, data):
    hi -= 1
    while lo < hi:
        swap_arrs(key_arrs, lo, hi)
        swap_arrs(data, lo, hi)
        lo += 1
        hi -= 1


@numba.njit(no_cpython_wrapper=True, cache=True)
def minRunLength(n):
    assert n >= 0
    rsa__ctu = 0
    while n >= MIN_MERGE:
        rsa__ctu |= n & 1
        n >>= 1
    return n + rsa__ctu


MIN_GALLOP = 7
INITIAL_TMP_STORAGE_LENGTH = 256


@numba.njit(no_cpython_wrapper=True, cache=True)
def init_sort_start(key_arrs, data):
    minGallop = MIN_GALLOP
    cwn__iaog = len(key_arrs[0])
    tmpLength = (cwn__iaog >> 1 if cwn__iaog < 2 *
        INITIAL_TMP_STORAGE_LENGTH else INITIAL_TMP_STORAGE_LENGTH)
    tmp = alloc_arr_tup(tmpLength, key_arrs)
    tmp_data = alloc_arr_tup(tmpLength, data)
    stackSize = 0
    omgl__vzk = (5 if cwn__iaog < 120 else 10 if cwn__iaog < 1542 else 19 if
        cwn__iaog < 119151 else 40)
    runBase = np.empty(omgl__vzk, np.int64)
    runLen = np.empty(omgl__vzk, np.int64)
    return stackSize, runBase, runLen, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def pushRun(stackSize, runBase, runLen, runBase_val, runLen_val):
    runBase[stackSize] = runBase_val
    runLen[stackSize] = runLen_val
    stackSize += 1
    return stackSize


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeCollapse(stackSize, runBase, runLen, key_arrs, data, tmpLength,
    tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n >= 1 and runLen[n - 1] <= runLen[n] + runLen[n + 1
            ] or n >= 2 and runLen[n - 2] <= runLen[n] + runLen[n - 1]:
            if runLen[n - 1] < runLen[n + 1]:
                n -= 1
        elif runLen[n] > runLen[n + 1]:
            break
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeForceCollapse(stackSize, runBase, runLen, key_arrs, data,
    tmpLength, tmp, tmp_data, minGallop):
    while stackSize > 1:
        n = stackSize - 2
        if n > 0 and runLen[n - 1] < runLen[n + 1]:
            n -= 1
        stackSize, tmpLength, tmp, tmp_data, minGallop = mergeAt(stackSize,
            runBase, runLen, key_arrs, data, tmpLength, tmp, tmp_data,
            minGallop, n)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeAt(stackSize, runBase, runLen, key_arrs, data, tmpLength, tmp,
    tmp_data, minGallop, i):
    assert stackSize >= 2
    assert i >= 0
    assert i == stackSize - 2 or i == stackSize - 3
    base1 = runBase[i]
    len1 = runLen[i]
    base2 = runBase[i + 1]
    len2 = runLen[i + 1]
    assert len1 > 0 and len2 > 0
    assert base1 + len1 == base2
    runLen[i] = len1 + len2
    if i == stackSize - 3:
        runBase[i + 1] = runBase[i + 2]
        runLen[i + 1] = runLen[i + 2]
    stackSize -= 1
    xvi__fgaz = gallopRight(getitem_arr_tup(key_arrs, base2), key_arrs,
        base1, len1, 0)
    assert xvi__fgaz >= 0
    base1 += xvi__fgaz
    len1 -= xvi__fgaz
    if len1 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    len2 = gallopLeft(getitem_arr_tup(key_arrs, base1 + len1 - 1), key_arrs,
        base2, len2, len2 - 1)
    assert len2 >= 0
    if len2 == 0:
        return stackSize, tmpLength, tmp, tmp_data, minGallop
    if len1 <= len2:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len1)
        minGallop = mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    else:
        tmpLength, tmp, tmp_data = ensureCapacity(tmpLength, tmp, tmp_data,
            key_arrs, data, len2)
        minGallop = mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1,
            len1, base2, len2)
    return stackSize, tmpLength, tmp, tmp_data, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopLeft(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    spj__wsoxo = 0
    ora__vqrq = 1
    if key > getitem_arr_tup(arr, base + hint):
        bjbrz__erbm = _len - hint
        while ora__vqrq < bjbrz__erbm and key > getitem_arr_tup(arr, base +
            hint + ora__vqrq):
            spj__wsoxo = ora__vqrq
            ora__vqrq = (ora__vqrq << 1) + 1
            if ora__vqrq <= 0:
                ora__vqrq = bjbrz__erbm
        if ora__vqrq > bjbrz__erbm:
            ora__vqrq = bjbrz__erbm
        spj__wsoxo += hint
        ora__vqrq += hint
    else:
        bjbrz__erbm = hint + 1
        while ora__vqrq < bjbrz__erbm and key <= getitem_arr_tup(arr, base +
            hint - ora__vqrq):
            spj__wsoxo = ora__vqrq
            ora__vqrq = (ora__vqrq << 1) + 1
            if ora__vqrq <= 0:
                ora__vqrq = bjbrz__erbm
        if ora__vqrq > bjbrz__erbm:
            ora__vqrq = bjbrz__erbm
        tmp = spj__wsoxo
        spj__wsoxo = hint - ora__vqrq
        ora__vqrq = hint - tmp
    assert -1 <= spj__wsoxo and spj__wsoxo < ora__vqrq and ora__vqrq <= _len
    spj__wsoxo += 1
    while spj__wsoxo < ora__vqrq:
        fzwcm__vzr = spj__wsoxo + (ora__vqrq - spj__wsoxo >> 1)
        if key > getitem_arr_tup(arr, base + fzwcm__vzr):
            spj__wsoxo = fzwcm__vzr + 1
        else:
            ora__vqrq = fzwcm__vzr
    assert spj__wsoxo == ora__vqrq
    return ora__vqrq


@numba.njit(no_cpython_wrapper=True, cache=True)
def gallopRight(key, arr, base, _len, hint):
    assert _len > 0 and hint >= 0 and hint < _len
    ora__vqrq = 1
    spj__wsoxo = 0
    if key < getitem_arr_tup(arr, base + hint):
        bjbrz__erbm = hint + 1
        while ora__vqrq < bjbrz__erbm and key < getitem_arr_tup(arr, base +
            hint - ora__vqrq):
            spj__wsoxo = ora__vqrq
            ora__vqrq = (ora__vqrq << 1) + 1
            if ora__vqrq <= 0:
                ora__vqrq = bjbrz__erbm
        if ora__vqrq > bjbrz__erbm:
            ora__vqrq = bjbrz__erbm
        tmp = spj__wsoxo
        spj__wsoxo = hint - ora__vqrq
        ora__vqrq = hint - tmp
    else:
        bjbrz__erbm = _len - hint
        while ora__vqrq < bjbrz__erbm and key >= getitem_arr_tup(arr, base +
            hint + ora__vqrq):
            spj__wsoxo = ora__vqrq
            ora__vqrq = (ora__vqrq << 1) + 1
            if ora__vqrq <= 0:
                ora__vqrq = bjbrz__erbm
        if ora__vqrq > bjbrz__erbm:
            ora__vqrq = bjbrz__erbm
        spj__wsoxo += hint
        ora__vqrq += hint
    assert -1 <= spj__wsoxo and spj__wsoxo < ora__vqrq and ora__vqrq <= _len
    spj__wsoxo += 1
    while spj__wsoxo < ora__vqrq:
        fzwcm__vzr = spj__wsoxo + (ora__vqrq - spj__wsoxo >> 1)
        if key < getitem_arr_tup(arr, base + fzwcm__vzr):
            ora__vqrq = fzwcm__vzr
        else:
            spj__wsoxo = fzwcm__vzr + 1
    assert spj__wsoxo == ora__vqrq
    return ora__vqrq


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base1, tmp, 0, len1)
    copyRange_tup(arr_data, base1, tmp_data, 0, len1)
    cursor1 = 0
    cursor2 = base2
    dest = base1
    setitem_arr_tup(arr, dest, getitem_arr_tup(arr, cursor2))
    copyElement_tup(arr_data, cursor2, arr_data, dest)
    cursor2 += 1
    dest += 1
    len2 -= 1
    if len2 == 0:
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
        return minGallop
    if len1 == 1:
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
        return minGallop
    len1, len2, cursor1, cursor2, dest, minGallop = mergeLo_inner(key_arrs,
        data, tmp_data, len1, len2, tmp, cursor1, cursor2, dest, minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len1 == 1:
        assert len2 > 0
        copyRange_tup(arr, cursor2, arr, dest, len2)
        copyRange_tup(arr_data, cursor2, arr_data, dest, len2)
        copyElement_tup(tmp, cursor1, arr, dest + len2)
        copyElement_tup(tmp_data, cursor1, arr_data, dest + len2)
    elif len1 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len2 == 0
        assert len1 > 1
        copyRange_tup(tmp, cursor1, arr, dest, len1)
        copyRange_tup(tmp_data, cursor1, arr_data, dest, len1)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeLo_inner(arr, arr_data, tmp_data, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        ptq__pjvka = 0
        vfet__ufu = 0
        while True:
            assert len1 > 1 and len2 > 0
            if getitem_arr_tup(arr, cursor2) < getitem_arr_tup(tmp, cursor1):
                copyElement_tup(arr, cursor2, arr, dest)
                copyElement_tup(arr_data, cursor2, arr_data, dest)
                cursor2 += 1
                dest += 1
                vfet__ufu += 1
                ptq__pjvka = 0
                len2 -= 1
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor1, arr, dest)
                copyElement_tup(tmp_data, cursor1, arr_data, dest)
                cursor1 += 1
                dest += 1
                ptq__pjvka += 1
                vfet__ufu = 0
                len1 -= 1
                if len1 == 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            if not ptq__pjvka | vfet__ufu < minGallop:
                break
        while True:
            assert len1 > 1 and len2 > 0
            ptq__pjvka = gallopRight(getitem_arr_tup(arr, cursor2), tmp,
                cursor1, len1, 0)
            if ptq__pjvka != 0:
                copyRange_tup(tmp, cursor1, arr, dest, ptq__pjvka)
                copyRange_tup(tmp_data, cursor1, arr_data, dest, ptq__pjvka)
                dest += ptq__pjvka
                cursor1 += ptq__pjvka
                len1 -= ptq__pjvka
                if len1 <= 1:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor2, arr, dest)
            copyElement_tup(arr_data, cursor2, arr_data, dest)
            cursor2 += 1
            dest += 1
            len2 -= 1
            if len2 == 0:
                return len1, len2, cursor1, cursor2, dest, minGallop
            vfet__ufu = gallopLeft(getitem_arr_tup(tmp, cursor1), arr,
                cursor2, len2, 0)
            if vfet__ufu != 0:
                copyRange_tup(arr, cursor2, arr, dest, vfet__ufu)
                copyRange_tup(arr_data, cursor2, arr_data, dest, vfet__ufu)
                dest += vfet__ufu
                cursor2 += vfet__ufu
                len2 -= vfet__ufu
                if len2 == 0:
                    return len1, len2, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor1, arr, dest)
            copyElement_tup(tmp_data, cursor1, arr_data, dest)
            cursor1 += 1
            dest += 1
            len1 -= 1
            if len1 == 1:
                return len1, len2, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not ptq__pjvka >= MIN_GALLOP | vfet__ufu >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi(key_arrs, data, tmp, tmp_data, minGallop, base1, len1, base2, len2
    ):
    assert len1 > 0 and len2 > 0 and base1 + len1 == base2
    arr = key_arrs
    arr_data = data
    copyRange_tup(arr, base2, tmp, 0, len2)
    copyRange_tup(arr_data, base2, tmp_data, 0, len2)
    cursor1 = base1 + len1 - 1
    cursor2 = len2 - 1
    dest = base2 + len2 - 1
    copyElement_tup(arr, cursor1, arr, dest)
    copyElement_tup(arr_data, cursor1, arr_data, dest)
    cursor1 -= 1
    dest -= 1
    len1 -= 1
    if len1 == 0:
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
        return minGallop
    if len2 == 1:
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
        return minGallop
    len1, len2, tmp, cursor1, cursor2, dest, minGallop = mergeHi_inner(key_arrs
        , data, tmp_data, base1, len1, len2, tmp, cursor1, cursor2, dest,
        minGallop)
    minGallop = 1 if minGallop < 1 else minGallop
    if len2 == 1:
        assert len1 > 0
        dest -= len1
        cursor1 -= len1
        copyRange_tup(arr, cursor1 + 1, arr, dest + 1, len1)
        copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1, len1)
        copyElement_tup(tmp, cursor2, arr, dest)
        copyElement_tup(tmp_data, cursor2, arr_data, dest)
    elif len2 == 0:
        raise ValueError('Comparison method violates its general contract!')
    else:
        assert len1 == 0
        assert len2 > 0
        copyRange_tup(tmp, 0, arr, dest - (len2 - 1), len2)
        copyRange_tup(tmp_data, 0, arr_data, dest - (len2 - 1), len2)
    return minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def mergeHi_inner(arr, arr_data, tmp_data, base1, len1, len2, tmp, cursor1,
    cursor2, dest, minGallop):
    while True:
        ptq__pjvka = 0
        vfet__ufu = 0
        while True:
            assert len1 > 0 and len2 > 1
            if getitem_arr_tup(tmp, cursor2) < getitem_arr_tup(arr, cursor1):
                copyElement_tup(arr, cursor1, arr, dest)
                copyElement_tup(arr_data, cursor1, arr_data, dest)
                cursor1 -= 1
                dest -= 1
                ptq__pjvka += 1
                vfet__ufu = 0
                len1 -= 1
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            else:
                copyElement_tup(tmp, cursor2, arr, dest)
                copyElement_tup(tmp_data, cursor2, arr_data, dest)
                cursor2 -= 1
                dest -= 1
                vfet__ufu += 1
                ptq__pjvka = 0
                len2 -= 1
                if len2 == 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            if not ptq__pjvka | vfet__ufu < minGallop:
                break
        while True:
            assert len1 > 0 and len2 > 1
            ptq__pjvka = len1 - gallopRight(getitem_arr_tup(tmp, cursor2),
                arr, base1, len1, len1 - 1)
            if ptq__pjvka != 0:
                dest -= ptq__pjvka
                cursor1 -= ptq__pjvka
                len1 -= ptq__pjvka
                copyRange_tup(arr, cursor1 + 1, arr, dest + 1, ptq__pjvka)
                copyRange_tup(arr_data, cursor1 + 1, arr_data, dest + 1,
                    ptq__pjvka)
                if len1 == 0:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(tmp, cursor2, arr, dest)
            copyElement_tup(tmp_data, cursor2, arr_data, dest)
            cursor2 -= 1
            dest -= 1
            len2 -= 1
            if len2 == 1:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            vfet__ufu = len2 - gallopLeft(getitem_arr_tup(arr, cursor1),
                tmp, 0, len2, len2 - 1)
            if vfet__ufu != 0:
                dest -= vfet__ufu
                cursor2 -= vfet__ufu
                len2 -= vfet__ufu
                copyRange_tup(tmp, cursor2 + 1, arr, dest + 1, vfet__ufu)
                copyRange_tup(tmp_data, cursor2 + 1, arr_data, dest + 1,
                    vfet__ufu)
                if len2 <= 1:
                    return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            copyElement_tup(arr, cursor1, arr, dest)
            copyElement_tup(arr_data, cursor1, arr_data, dest)
            cursor1 -= 1
            dest -= 1
            len1 -= 1
            if len1 == 0:
                return len1, len2, tmp, cursor1, cursor2, dest, minGallop
            minGallop -= 1
            if not ptq__pjvka >= MIN_GALLOP | vfet__ufu >= MIN_GALLOP:
                break
        if minGallop < 0:
            minGallop = 0
        minGallop += 2
    return len1, len2, tmp, cursor1, cursor2, dest, minGallop


@numba.njit(no_cpython_wrapper=True, cache=True)
def ensureCapacity(tmpLength, tmp, tmp_data, key_arrs, data, minCapacity):
    rpk__poe = len(key_arrs[0])
    if tmpLength < minCapacity:
        dwwuj__qpi = minCapacity
        dwwuj__qpi |= dwwuj__qpi >> 1
        dwwuj__qpi |= dwwuj__qpi >> 2
        dwwuj__qpi |= dwwuj__qpi >> 4
        dwwuj__qpi |= dwwuj__qpi >> 8
        dwwuj__qpi |= dwwuj__qpi >> 16
        dwwuj__qpi += 1
        if dwwuj__qpi < 0:
            dwwuj__qpi = minCapacity
        else:
            dwwuj__qpi = min(dwwuj__qpi, rpk__poe >> 1)
        tmp = alloc_arr_tup(dwwuj__qpi, key_arrs)
        tmp_data = alloc_arr_tup(dwwuj__qpi, data)
        tmpLength = dwwuj__qpi
    return tmpLength, tmp, tmp_data


def swap_arrs(data, lo, hi):
    for arr in data:
        wlcw__xgkgk = arr[lo]
        arr[lo] = arr[hi]
        arr[hi] = wlcw__xgkgk


@overload(swap_arrs, no_unliteral=True)
def swap_arrs_overload(arr_tup, lo, hi):
    bpbtb__haiz = arr_tup.count
    yrldt__ixwhc = 'def f(arr_tup, lo, hi):\n'
    for i in range(bpbtb__haiz):
        yrldt__ixwhc += '  tmp_v_{} = arr_tup[{}][lo]\n'.format(i, i)
        yrldt__ixwhc += '  arr_tup[{}][lo] = arr_tup[{}][hi]\n'.format(i, i)
        yrldt__ixwhc += '  arr_tup[{}][hi] = tmp_v_{}\n'.format(i, i)
    yrldt__ixwhc += '  return\n'
    sgn__usti = {}
    exec(yrldt__ixwhc, {}, sgn__usti)
    wrj__esu = sgn__usti['f']
    return wrj__esu


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyRange(src_arr, src_pos, dst_arr, dst_pos, n):
    dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


def copyRange_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos:dst_pos + n] = src_arr[src_pos:src_pos + n]


@overload(copyRange_tup, no_unliteral=True)
def copyRange_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):
    bpbtb__haiz = src_arr_tup.count
    assert bpbtb__haiz == dst_arr_tup.count
    yrldt__ixwhc = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos, n):\n'
    for i in range(bpbtb__haiz):
        yrldt__ixwhc += (
            '  copyRange(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos, n)\n'
            .format(i, i))
    yrldt__ixwhc += '  return\n'
    sgn__usti = {}
    exec(yrldt__ixwhc, {'copyRange': copyRange}, sgn__usti)
    ixz__wivg = sgn__usti['f']
    return ixz__wivg


@numba.njit(no_cpython_wrapper=True, cache=True)
def copyElement(src_arr, src_pos, dst_arr, dst_pos):
    dst_arr[dst_pos] = src_arr[src_pos]


def copyElement_tup(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    for src_arr, dst_arr in zip(src_arr_tup, dst_arr_tup):
        dst_arr[dst_pos] = src_arr[src_pos]


@overload(copyElement_tup, no_unliteral=True)
def copyElement_tup_overload(src_arr_tup, src_pos, dst_arr_tup, dst_pos):
    bpbtb__haiz = src_arr_tup.count
    assert bpbtb__haiz == dst_arr_tup.count
    yrldt__ixwhc = 'def f(src_arr_tup, src_pos, dst_arr_tup, dst_pos):\n'
    for i in range(bpbtb__haiz):
        yrldt__ixwhc += (
            '  copyElement(src_arr_tup[{}], src_pos, dst_arr_tup[{}], dst_pos)\n'
            .format(i, i))
    yrldt__ixwhc += '  return\n'
    sgn__usti = {}
    exec(yrldt__ixwhc, {'copyElement': copyElement}, sgn__usti)
    ixz__wivg = sgn__usti['f']
    return ixz__wivg


def getitem_arr_tup(arr_tup, ind):
    bebd__mks = [arr[ind] for arr in arr_tup]
    return tuple(bebd__mks)


@overload(getitem_arr_tup, no_unliteral=True)
def getitem_arr_tup_overload(arr_tup, ind):
    bpbtb__haiz = arr_tup.count
    yrldt__ixwhc = 'def f(arr_tup, ind):\n'
    yrldt__ixwhc += '  return ({}{})\n'.format(','.join(['arr_tup[{}][ind]'
        .format(i) for i in range(bpbtb__haiz)]), ',' if bpbtb__haiz == 1 else
        '')
    sgn__usti = {}
    exec(yrldt__ixwhc, {}, sgn__usti)
    cnjb__hkj = sgn__usti['f']
    return cnjb__hkj


def setitem_arr_tup(arr_tup, ind, val_tup):
    for arr, aac__teugs in zip(arr_tup, val_tup):
        arr[ind] = aac__teugs


@overload(setitem_arr_tup, no_unliteral=True)
def setitem_arr_tup_overload(arr_tup, ind, val_tup):
    bpbtb__haiz = arr_tup.count
    yrldt__ixwhc = 'def f(arr_tup, ind, val_tup):\n'
    for i in range(bpbtb__haiz):
        if isinstance(val_tup, numba.core.types.BaseTuple):
            yrldt__ixwhc += '  arr_tup[{}][ind] = val_tup[{}]\n'.format(i, i)
        else:
            assert arr_tup.count == 1
            yrldt__ixwhc += '  arr_tup[{}][ind] = val_tup\n'.format(i)
    yrldt__ixwhc += '  return\n'
    sgn__usti = {}
    exec(yrldt__ixwhc, {}, sgn__usti)
    cnjb__hkj = sgn__usti['f']
    return cnjb__hkj


def test():
    import time
    pux__lihn = time.time()
    izh__bonjh = np.ones(3)
    data = np.arange(3), np.ones(3)
    sort((izh__bonjh,), 0, 3, data)
    print('compile time', time.time() - pux__lihn)
    n = 210000
    np.random.seed(2)
    data = np.arange(n), np.random.ranf(n)
    jflya__kycg = np.random.ranf(n)
    htwo__klhi = pd.DataFrame({'A': jflya__kycg, 'B': data[0], 'C': data[1]})
    pux__lihn = time.time()
    jcuxj__qwt = htwo__klhi.sort_values('A', inplace=False)
    mzevj__ufdcj = time.time()
    sort((jflya__kycg,), 0, n, data)
    print('Bodo', time.time() - mzevj__ufdcj, 'Numpy', mzevj__ufdcj - pux__lihn
        )
    np.testing.assert_almost_equal(data[0], jcuxj__qwt.B.values)
    np.testing.assert_almost_equal(data[1], jcuxj__qwt.C.values)


if __name__ == '__main__':
    test()
