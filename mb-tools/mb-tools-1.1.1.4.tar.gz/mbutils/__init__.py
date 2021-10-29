"""
用于存放web方向的方法
"""
import functools
import json
import socket
from asyncio import Future
from decimal import Decimal
from typing import Any, Callable

import pymysql
from sqlalchemy.exc import *
from sqlalchemy.orm import Session
from tornado.concurrent import chain_future
from tornado.gen import coroutine

from mbutils.constant import ErrorType
from mbutils.log import Logger

pymysql.install_as_MySQLdb()
settings = dict(debug=False,
                autoreload=False)
cfg = dict(port=8600,
           redis_cli={},
           mysql={},
           debug=False,
           is_test_env=0)

try:
    with open('config.json', 'r', encoding="utf-8") as f:
        js_str = f.read()
        cfg.update(json.loads(js_str))
except Exception:
    try:
        with open('./config.json', 'r') as f:
            js_str = f.read()
            cfg.update(json.loads(js_str))
    except Exception:
        with open('./../config.json', 'r') as f:
            js_str = f.read()
            cfg.update(json.loads(js_str))

AGENT_NAME = cfg["OpsConfig"]["CustomerName"]
compute_name = socket.getfqdn(socket.gethostname())
logger = Logger(cfg)


def single_instance(cls):
    """ 单例类的装饰器  """
    instance = {}

    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance


class DAOSession:
    def __init__(self):
        """暴露出session的类型"""
        from mbutils.redis_manager import RedisManager
        self.session = Session
        self.sub_session = Session
        self.async_do = None
        self.redis_session = RedisManager({})

    def initialize(self, app):
        self.session = app.db_session
        if cfg.get("sub_mysql", None):
            self.sub_session = app.sub_db_session
        else:
            self.sub_session = app.db_session
        self.async_do = app.async_do
        self.redis_session = app.redis_session


dao_session = DAOSession()


def scoped_close(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except InvalidRequestError:
            logger.info("scoped_close:InvalidRequestError")
            dao_session.session().rollback()
            dao_session.session().close()
            dao_session.sub_session().rollback()
            dao_session.sub_session.close()
            return ""
        finally:
            # return 前会走finally
            dao_session.session.remove()
            dao_session.sub_session.remove()

    return wrapper


def mb_async(func):
    """
    这个方法只出现在view里面，不要出现在service里面
    在线程池里面执行耗时的操作，线程池里面不能再调线程池操作，否则会报找不到IO_LOOP的错误
    """

    @coroutine
    def wrapper(*args, **argv):
        res = yield dao_session.async_do(scoped_close(func), *args, **argv)

        return res

    return wrapper


# def mb_async(func):
#     @coroutine
#     def wrapper(*args, **argv):
#         res = yield func(*args, **argv)
#         return res
#
#     return wrapper


def mb_on_executor(*args, **kwargs) -> Callable:
    """
    修改自tornado.concurrent.run_on_executor
    """

    # Fully type-checking decorators is tricky, and this one is
    # discouraged anyway so it doesn't have all the generic magic.
    def run_on_executor_decorator(fn: Callable) -> Callable[..., Future]:

        @functools.wraps(fn)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Future:
            async_future = Future()  # type: Future
            conc_future = dao_session.async_do(scoped_close(fn), self, *args, **kwargs)
            chain_future(conc_future, async_future)
            return async_future

        return wrapper

    if args and kwargs:
        raise ValueError("cannot combine positional and keyword args")
    if len(args) == 1:
        return run_on_executor_decorator(args[0])
    elif len(args) != 0:
        raise ValueError("expected 1 argument, got %d", len(args))
    return run_on_executor_decorator


class MbException(Exception):
    def __init__(self, promt, error_type: ErrorType = ErrorType.BIZ_ERROR):
        self.promt = promt
        self.error_type = error_type

    def __str__(self):
        return self.promt + " " + self.error_type.name


class DefaultMaker:
    pass


# 引入默认的类和默认对象，是为了解决参数传入'',[],0不好区分
ARG_DEFAULT = DefaultMaker()


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return json.JSONEncoder.default(self, o)


def api_cache(url: str, params: str, interval: int = 60):
    '''
    用url+params组成的缓存，间隔interval
    :param url: 前缀标识，推荐用url
    :param params:请求参数
    :param interval:单位是秒
    :return:

    #mbutils:
    def f(x):
        return time.time()+x
    res = api_cache(url='/get/list', params=json_str, interval=3)(f)(5)
    '''

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = url + '_' + params + '_'
            value = dao_session.redis_session.r.get(key)
            # 返回缓存值
            if value:
                return json.loads(value)  # json.JSONDecoder
            else:
                # bulid 缓存 response
                response = func(*args, *kwargs)
                cathe_response = json.dumps(response, cls=JSONEncoder) or ''
                dao_session.redis_session.r.set(key, cathe_response, ex=interval)
                return response

        return wrapper

    return decorator
