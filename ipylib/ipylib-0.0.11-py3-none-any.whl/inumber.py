# -*- coding: utf-8 -*-
import re
import numbers
import math

from idebug import *


__all__ = [
    'math',
    'iNumber',
    'Percent',
    'to_koreaNumSys','to_koreaNumSys_inDF',
    'convert_timeunit',
]



class iNumberParser:
    # 'str-dtype'Number(문자형숫자)
    # 파싱 불가능한 입력값은 그대로 리턴한다
    def __init__(self, s, prec=4, sosujeom='.'):
        # PartGubun('입력값 전처리')
        # 입력값 문자형숫자
        self._input = s
        # 소수점 이하 자리수
        self._prec = prec
        # 소수점 기호
        self._sosujeom = sosujeom
        # 소수점 기호 표기방식
        self.__NumSystem = '국제표준' if self._sosujeom == '.' else '스페인식'
        # 정수 부분 천단위 구분 기호
        self._int_fmt = ',' if self.__NumSystem == '국제표준' else '.'

        if isinstance(s, str):
            if len(s.strip()) == 0:
                logger.warning(f"{self} | 입력값 오류(input: {self._input} [{len(self._input)}])")
                self._v = math.nan
            else:
                self._parse(s)
        else:
            msg = "'str-dtype'Number(문자형숫자)가 아니면, "
            # logger.info(f"{self} | {msg} | s --> {s} {type(s)}")
            if isinstance(self._input, numbers.Number):
                self._v = self._input
            else:
                self._v = math.nan

    def _parse(self, s):
        p_fmt = '\.' if self._int_fmt == '.' else self._int_fmt
        p_jeom = '\.' if self._sosujeom == '.' else self._sosujeom
        # 앞에 '0' 안붙이고 소수점으로 시작하는 경우 예외처리
        if re.search(f'^{p_jeom}', s) is not None:
            s = s.zfill(len(s)+1)
        # 공통 파싱
        m = re.search(f'([-\+])*([{p_fmt}|\d]+|[\d]+)({p_jeom})*(\d+)*(%$)*', s)
        # print(m.groups())
        sign, i, jeom, sosu, pct = m[1], m[2], m[3], m[4], m[5]

        # PartGubun('Attrs 결정')
        # 양/음수 기호
        self._sign = +1 if sign in [None,'+'] else -1
        # 정수 부분
        self._int = int(i.replace(self._int_fmt, ''))
        # 정수인지 아닌지 여부
        self._is_int = True if sosu is None else False
        # 소수점을 '.'으로 표준화
        jeom = '.' if jeom == ',' else jeom
        sosu = f'{jeom}{sosu}' if jeom != None and sosu != None else None
        self._sosu = .0 if sosu is None else float(sosu)
        # 퍼센트 기호 처리
        self._is_pct = True if pct == '%' else False
        # 최종값 결정
        v = self._int + self._sosu
        v = int(v) if self._is_int else float(v)
        self._v = self._sign * v
        if self._is_pct:
            self._v = round(self._v / 100, self._prec)

    @property
    def is_pct(self):
        return self._is_pct

    @property
    def num(self):
        return self._v

    @property
    def numstr(self):
        try:
            return str(self._v).format("{:,}")
        except Exception as e:
            return None


def iNumber(s, prec=4, sosujeom='.'):
    return iNumberParser(s, prec, sosujeom).num


class Percent:

    # @funcIdentity
    def __init__(self, s, prec=2, sosujeom='.'):
        self._input = s
        # 퍼센트 소수점이하 자릿수(Percent Precision)
        self._p_prec = prec
        # 퍼센트를 숫자로 변환시 소수점이하 자릿수(Number Precision)
        self._n_prec = self._p_prec + 2
        # 소수점 기호
        self._sosujeom = sosujeom
        # 문자열이든 숫자든 모두 %기호를 포함한 문자열로 변환
        if isinstance(self._input, str):
            if '%' not in s:
                s = s+'%'
        elif isinstance(self._input, int) or isinstance(self._input, float):
            if math.isnan(s): raise
            s = str(s) + '%'
        else:
            raise

        self.parser = iNumberParser(s, self._n_prec, self._sosujeom)

    @property
    def input(self):
        return self._input

    @property
    def value(self):
        # 퍼센트 단위의 숫자
        return round(self.parser.num * 100, self._p_prec)

    @property
    def to_float(self):
        return round(self.parser.num, self._n_prec)

    @property
    def to_str(self):
        # 소수점이하 자릿수를 예쁘지 채워주기
        # 소수점이하 수를 문자열로 변경하고, 소수점으로 분리한 후, 소수점이하 자릿수를 조정한다
        _int, prec = str(self.value).split('.')
        _sosu_str = prec.ljust(self._p_prec, '0')
        return _int + self._sosujeom + _sosu_str + '%'


def to_koreaNumSys(n):
    if n < pow(10,4):
        unit = ''
    else:
        for i in range(1,10,1):
            n = n/pow(10,4)
            if n < pow(10,4):
                break
        if i == 1:
            unit = '만'
        elif i == 2:
            unit = '억'
        elif i == 3:
            unit = '조'
        elif i == 4:
            unit = '경'
        else:
            print("\n 경 이상의 단위는 다룰 필요가 없다.")
    return f"{round(n,1)}{unit}"

def to_koreaNumSys_inDF(df, 컬럼_승수_dic):
    df1 = df.copy()
    승수명칭_dic = {4:'_만', 8:'_억', 12:'_조', 16:'_경'}
    for col in 컬럼_승수_dic:
        승수 = 컬럼_승수_dic[col]
        df1[col] = df1[col].apply(lambda x: x/pow(10, 승수))
        #df1 = df1.rename( columns={col: col+승수명칭_dic[승수]} )
    return df1

def convert_datasize_unit(val, type='count'):
    """데이터크기 단위 변환."""
    KiB = pow(2,10)
    MiB = pow(2,20)
    GiB = pow(2,30)
    TiB = pow(2,40)
    K = pow(10,3)
    M = pow(10,6)
    G = pow(10,9)
    T = pow(10,12)

    if type == 'count':
        if val < K:
            unit = 'decimal'
        elif K <= val < M:
            val = val / K
            unit = 'K'
        elif M <= val < G:
            val = val / M
            unit = 'M'
        elif G <= val < T:
            val = val / G
            unit = 'G'
        else:
            val =  val / T
            unit = 'T'

    elif type == 'byte':
        if val < KiB:
            unit = 'B'
        elif KiB <= val < MiB:
            val = val / KiB
            unit = 'KiB'
        elif MiB <= val < GiB:
            val = val / MiB
            unit = 'MiB'
        elif GiB <= val < TiB:
            val = val / GiB
            unit = 'GiB'
        else:
            val =  val / TiB
            unit = 'TiB'
    else: print('\n 다른 환산 단위는 또 뭐냐\n')

    return (val, unit)

def convert_timeunit(seconds):
    sec = 1
    msec = sec / 1000
    min = sec * 60
    hour = min * 60

    t = seconds
    if t < sec:
        unit = 'msec'
        t = t / msec
    elif sec <= t <= min:
        unit = 'secs'
    elif min < t <= hour:
        unit = 'mins'
        t = t / min
    else:
        unit = 'hrs'
        t = t / hour

    return round(t, 1), unit
