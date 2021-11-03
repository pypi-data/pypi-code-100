import re
import unicodedata
from typing import Any


def replace_all(s: str, obj: dict) -> str:
    """複数のreplace
    Example:
        >>> _obj = {"円": ".", "銭": ""}
        >>> replace_all("3円00銭", _obj)
        '3.00'
        >>> _obj = {"[△▲]": "-", "[,、]": ""}
        >>> replace_all('▲12,345', _obj)
        '-12345'
        >>> replace_all('△12、345', _obj)
        '-12345'
    """
    for key in obj:
        val = obj[key]
        s = re.sub(key, val, s)
    return s


def to_half_string(s: str) -> str:
    """normalize
    Example:
        >>> to_half_string('１２３ＸＹＺ')
        '123XYZ'
    """
    return unicodedata.normalize("NFKC", s)


def to_number(s: str, default: Any = float('NAN')) -> Any:
    """文字列を数値化
    Example:
        >>> to_number('△12,345')
        -12345
        >>> to_number('１２，３４５')
        12345
        >>> to_number('12円34銭')
        12.34
        >>> to_number('98%')
        98
        >>> to_number('abc')
        nan
        >>> to_number('abc', '123')
        '123'
    """
    rep_dict = {
        '[△▲Δ]': '-',
        '[,、銭%％]': '',
        '[円]': '.'
    }
    s = to_half_string(s)
    s = replace_all(s, rep_dict)
    try:
        float(s)
    except ValueError:
        return default
    else:
        if float(s).is_integer():
            return int(float(s))
        return float(s)


def to_date(s: str) -> Any:
    """日付表記を統一する
    Example:
        >>> to_date('２０１８年５月２７日')
        '2018-05-27'
        >>> to_date('令和 元年 5月12日')
        '2019-05-12'
        >>> to_date('大３年５月２７日')
        '1914-05-27'
        >>> to_date('20211010')
        '2021-10-10'
    """
    meiji = 'meiji'
    taisyou = 'taisyou'
    syouwa = 'syouwa'
    heisei = 'heisei'
    reiwa = 'reiwa'
    s = to_half_string(s)
    s = replace_all(s, {
        '[年月/]': '-',
        r'[日\s]': '',
        '[元]': '1',
        r'(明治|明)': meiji,
        r'(大正|大)': taisyou,
        r'(昭和|昭)': syouwa,
        r'(平成|平)': heisei,
        r'(令和|令)': reiwa,
    })
    # 数字8桁ならハイフン挿入
    m = re.match(r'^\d{8}$', s)
    if m:
        s = re.sub(r'(\d{4})(\d{2})(\d{2})', r'\1-\2-\3', s)
    m = re.match(r'(\D*)(\d*)-(\d*)-(\d*)', s)
    if m:
        era, year, month, day = m.groups()
        if era:
            if era == meiji:
                year = int(year) + 1868 - 1
            elif era == taisyou:
                year = int(year) + 1912 - 1
            elif era == syouwa:
                year = int(year) + 1926 - 1
            elif era == heisei:
                year = int(year) + 1989 - 1
            elif era == reiwa:
                year = int(year) + 2019 - 1
            year = str(year)
        month = f'0{month}' if len(month) == 1 else month
        day = f'0{day}' if len(day) == 1 else day
        return f'{year}-{month}-{day}'
    return None


def split_uppercase(s: str) -> list:
    """UpperCaseを分割
    Example:
        >>> split_uppercase('NextAccumulatedQ2Duration')
        ['Next', 'Accumulated', 'Q2', 'Duration']
    """
    return re.findall(r'[A-Z]+[a-z0-9]*', s)
