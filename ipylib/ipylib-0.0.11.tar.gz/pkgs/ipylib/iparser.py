# -*- coding: utf-8 -*-
from idebug import *
from ipylib.inumber import *
from ipylib.idatetime import *


__all__ = [
    'ValueDtypeParser',
]

def ValueDtypeParser(v, dtype, ndigits=4):
    params = locals()
    info1 = f'params: {params}'
    info2 = f'v: {v} {type(v)}'
    try:
        if dtype == 'int':
            return iNumber(v)
        elif dtype == 'int_abs':
            return abs(iNumber(v))
        elif dtype == 'float':
            return iNumber(v, prec=ndigits, sosujeom='.')
        elif dtype == 'pct':
            return Percent(v, prec=2, sosujeom='.').num
        elif dtype in ['date','time','dt','datetime']:
            return DatetimeParser(v)
        elif dtype == 'str':
            return str(v)
        else:
            msg = f"정의되지 않은 데이타-타입({dtype})을 입력하면, 입력된 값을 그대로 반환한다."
            logger.warning(f'{msg}-->\n{info1}\n{info2}')
            return v
    except Exception as e:
        msg = '파싱 에러가 발생하면, 입력된 값을 그대로 반환한다.'
        logger.error(f'{msg}-->\n{info1}\n{info2}')
        return v
