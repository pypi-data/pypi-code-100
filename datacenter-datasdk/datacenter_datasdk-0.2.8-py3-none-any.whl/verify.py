# -*-coding:utf-8 -*-
from functools import wraps
from collections import OrderedDict
from itertools import cycle
import traceback
import datetime


def verify_args(check=None, diy_func=None):
    """
    参数校验，包括类型判断和参数处理

    :param check: dict, 参数类型校验{'a': int, 'b': (list, str)}, value可以为 tuple of type
    :param diy_func:自定义的对某一参数的校验函数格式: {key:func},类似check, diy_func={"a": lambda x: x + "aa"})
    :return:
    """
    def wraps_1(f):
        @wraps(f)
        def wraps_2(*args, **kwargs):
            args_template = f.__code__.co_varnames
            args_dict = OrderedDict()
            try:
                for i, x in enumerate(args):
                    args_dict[args_template[i]] = x
                args_dict.update(kwargs)
                # check
                if check:
                    for p, t in check.items():
                        if not args_dict.get(p):
                            continue
                        if not isinstance(args_dict[p], t):
                            raise Exception(
                                'type of parma(%s) error, should be %s, but %s' % (p, t, type(args_dict[p])))
                # diy_func
                if diy_func:
                    for k in args_dict:
                        if k in diy_func:
                            args_dict[k] = diy_func[k](args_dict[k])
                return f(**args_dict)
            except Exception as e:
                print("verify_args catch err: ", traceback.format_exc())
        return wraps_2
    return wraps_1


def format_date_param(t):
    if isinstance(t, datetime.date) or isinstance(t, str):
        return f"{str(t)} 00:00:00"
    else:
        return t


def crypt(source, key):
    result = ''
    temp = cycle(key)
    for ch in source:
        result = result+chr(ord(ch) ^ ord(next(temp)))
    return result
