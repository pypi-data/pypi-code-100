#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__author__ = 'andy.hu'
__mtime__ = '2021/07/09'

"""
import datetime
import random
import re
import time
import threading
import json
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Set,
    Union,
)

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request as HttpRequest
from starlette.responses import Response as HttpResponse
from clife_svc.disconf import Disconf
from clife_svc.errors.error_code import ApiException, ParameterException
from clife_svc.libs.http_request import ClientRequest
from clife_svc.libs.log import init_conf_log
from clife_svc.libs.log import init_svc_log
from clife_svc.libs.log import klogger

local = threading.local()


class AiServiceRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            # local.reqId = tid_maker_1()
            # klogger.info('Request({}) url:{} {}'.format(local.reqId, request.method, request.url))
            body = await request.body()
            # print(request.headers.get('Content-Type'))
            # req_dict = await request.json()
            klogger.info('Request({}) params: {}'.format(local.reqId, request.query_params))
            klogger.info('Request({}) body: {}'.format(local.reqId, body.decode('utf-8')))
            before = time.time()
            # 这里可以获取的我们的请求的体的信息----
            response: Response = await original_route_handler(request)

            # 下面可以处理我们的响应体的报文信息，未被异常处理器拦截的请求将继续执行
            duration = time.time() - before
            klogger.info('Request({}) cost: {}s'.format(local.reqId, round(duration, 2)))
            klogger.info('Response({}) content: {}'.format(local.reqId, response.body.decode('utf-8')))
            # response.headers["X-Response-Time"] = str(duration)
            return response

        return custom_route_handler


class App(object):
    '''
    http接口服务上下文对象，单实例对象
    '''
    __instance = None
    __conf_item = None
    __fast_api = FastAPI(title='ai-service', default_response_class=ORJSONResponse)
    __ai_router = APIRouter(route_class=AiServiceRoute)
    __ClientRequest = None
    __app_name = None
    __log_path = None

    def __new__(cls, app_name: str, log_root_path: str, *conf: str):
        '''
        构造函数
        :param app_name 项目名称
        :param log_root_path 项目输出的日志根路径，推荐使用/www/logs，便于线上统一采集日志
        :param conf: 配置文件名称列表
        '''

        # app_name参数校验

        if not re.match(r'^(\w+-?\w+)+$', app_name):
            raise ParameterException(error_code=9982, msg='app_name can only be letters, numbers, or strike-through!')
        if app_name.count('_') > 0:
            raise ParameterException(error_code=9982, msg='app_name can only be letters, numbers, or strike-through!')

        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            cls.__log_path = log_root_path + '/' + app_name + '/'
            init_conf_log(cls.__log_path)
            cls.__conf_item = Disconf('clife-ai', '0.0.1-SNAPSHOT', conf).get_config_dict()
            cls.__ClientRequest = ClientRequest(cls.__conf_item)
            cls.__app_name = app_name
            init_svc_log(cls.__log_path, log_level='DEBUG')
        return cls.__instance

    def init_api(self) ->FastAPI:
        '''
        在App中初始化服务接口
        :return: FastAPI，作为服务器运行入口对象
        '''
        init_middlewares(self.__fast_api)
        self.__fast_api.add_exception_handler(ApiException, api_exception_handler)
        self.__fast_api.add_exception_handler(Exception, app_exception)
        self.__ai_router.add_api_route('/time', endpoint=index, methods=['GET'])
        self.__fast_api.include_router(self.__ai_router)
        return self.__fast_api

    def get_conf(self, key: str):
        '''
        获取配置数据
        :param key:配置项的key（"="左边的部分，当配置项包含多个"="时，）
        :return:
        '''
        try:
            return self.__conf_item[key]
        except KeyError:
            klogger.warning('config key not exist:{}'.format(key))
            return ''

    def get_all_conf(self) ->dict:
        '''
        获取所有配置数据
        :return:
        '''
        return self.__conf_item

    def add_api(self, path: str, endpoint: Callable[..., Any], methods: Optional[Union[Set[str], List[str]]] = None):
        '''
        增加服务接口，此函数需要在init_api前调用
        :param path:接口访问路径
        :param endpoint:接口实现函数
        :param methods:接口访问方式，如GET、POST等
        :return:
        '''
        self.__ai_router.add_api_route(path, endpoint, methods=methods)

    async def download_file(self, file_url, retry=2, timeout=None):
        '''
        下载文件
        :param timeout:
        :param file_url:文件地址
        :param retry:失败重试次数，默认为2次，建议不大于3次
        :param timeout: 文件下载超时时间（秒），默认为配置文件ai-commons.properties中http.timeout，目前为15秒
        :return:文件数据字节数组
        '''

        '''
        cos_cli = self.__ClientRequest.create_txy_client()
        buckets_list = cos_cli.list_buckets()
        for bucket in buckets_list['Buckets']['Bucket']:
            print(bucket)
            acl = cos_cli.get_bucket_acl(bucket['Name'])
            print(acl)
        '''
        return await self.__ClientRequest.download_file(file_url, retry, timeout)

    async def upload_file(self, file_path: str, retry=2):
        '''

        :param file_path:本地文件路径
        :param retry:失败重试次数，默认为2次，建议不大于3次
        :return: 文件url
        '''
        return await self.__ClientRequest.upload_file(self.__app_name, file_path, retry)


class Interceptor(BaseHTTPMiddleware):
    '''
    拦截所有请求
    '''
    async def dispatch(self, request: HttpRequest, call_next: RequestResponseEndpoint) -> HttpResponse:
        # 生成请求标识
        local.reqId = tid_maker_1()
        # 记录客户端请求的URL，包括未定义的URL，
        # 拦截器中不能获取request中body内容，会导致请求阻塞
        klogger.info('Request({}) URL: {} {}'.format(local.reqId, request.method, request.url))
        response = await call_next(request)
        klogger.info('Response({}) HTTP Status Code: {}'.format(local.reqId, response.status_code))
        return response


def init_middlewares(app: FastAPI):
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)
    app.add_middleware(Interceptor)


async def index(q: Optional[str] = None):
    '''k8s 探针 http监控服务请求地址'''
    if q:
        return {'code': 0, 'msg': 'success',
                'data': {'time': time.strftime('%Y-%m-%d-%H-%M', time.localtime()), 'q': q}}
    return {'code': 0, 'msg': 'success', 'data': {'time': time.strftime('%Y-%m-%d-%H-%M', time.localtime())}}


async def api_exception_handler(request: Request, exc: ApiException) -> JSONResponse:
    '''拦截接口抛出的所有自定义的HTTPException 异常'''
    # klogger.error('Request exception:{}'.format(traceback.format_exc()))
    klogger.exception('Request({}) exception'.format(local.reqId))
    response = JSONResponse({
        "code": exc.error_code,
        "msg": exc.msg,
        "data": exc.data
    }, status_code=exc.status_code)
    klogger.info('Response({}) content:{}'.format(local.reqId, response.body.decode('utf-8')))
    klogger.info('Response({}) HTTP Status Code: {}'.format(local.reqId, response.status_code))
    return response


async def app_exception(request: Request, exc: Exception):
    '''拦截接口抛出的所有未知非HTTPException 异常'''
    # klogger.error('Request exception:{}'.format(traceback.format_exc()))
    klogger.exception('Request({}) exception'.format(local.reqId))
    response = JSONResponse({
        "code": 10024,
        "msg": 'Unknown error',
        "data": {},
    }, status_code=500)
    klogger.info('Response({}) content:{}'.format(local.reqId, response.body.decode('utf-8')))
    klogger.info('Response({}) HTTP Status Code: {}'.format(local.reqId, response.status_code))
    return response


def tid_maker_1():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now())


def tid_maker_2():
    return '{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()) + ''.join(
        [str(random.randint(1, 10)) for i in range(5)])
