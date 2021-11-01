import os
from urllib.parse import parse_qsl
from typing import List

def parse_func_kwargs(s:str):
    this_stem = os.path.splitext(s)[0]
    these_args = this_stem.split('?')[1]
    function = this_stem.split('?')[0]
    kwargs = dict(parse_qsl(these_args))
    converted_kwargs = convert_hints_nested(kwargs)
    return function, converted_kwargs


def parse_kwargs(s:str):
    return parse_func_kwargs(s)[1]


def convert_hints_nested(o):
    if isinstance(o,str):
        o = o.strip(' ')
        if o[0]=='[' and o[-1]==']':
            elems = o[1:-1].split(',')
            return [convert_hints_nested(elem) for elem in elems]
        return convert_hints(o)
    elif isinstance(o,dict):
        return dict([ (k,convert_hints_nested(v)) for k,v in o.items()])
    elif isinstance(o,List):
        return [ convert_hints_nested(elem) for elem in o]
    else:
        return o


def convert_hints(s:str):
    if len(s)>=4 and s[:4]=='int:':
        return int(s[4:])
    elif len(s)>=6 and s[:6]=='float:':
        return float(s[6:])
    elif len(s)>=4 and s[:4]=='str:':
        return str(s[4:])
    else:
        return s
