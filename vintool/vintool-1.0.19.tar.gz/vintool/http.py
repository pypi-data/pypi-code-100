#! /usr/bin/env python
# -*- coding:utf-8 -*-

import json
import urllib.request
import logging
import traceback
import hashlib
import requests


class HttpClient(object):
    def __init__(self, appid, secret, url):
        self.appId = appid
        self.secret = secret
        self.url = url

    def __call__(self, args, retry=3):
        """
          Summary: http请求
        """
        if not retry: return
        try:
            url = self.url
            logging.getLogger(__name__).info("url: %s params:%s" % (url, args))
            resp = self.post(url, args)
            if resp:
                if 'code' not in resp or resp['code'] != 200:
                    logging.getLogger(__name__).warning(
                        "return status not 200, msg: %s" % json.dumps(resp, ensure_ascii=False))
            return resp
        except HttpException as e:
            logging.getLogger(__name__).error("request error: %s" % e)
            traceback.print_exc()

    def post(self, url, data):
        # logging.getLogger(__name__).info("post %s params:%s" % (url, data))
        try:
            params = json.dumps(data)
        except TypeError as e:
            params = json.dumps(data, cls=Encoder)
        try:
            sign = self._sign(data, self.secret)
            headers = {
                "appid": self.appId,
                "sign": sign,
                "Content-Type": "application/json",
                # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.11",
            }
            res = requests.post(url=url, data=params, headers=headers)
            if res.status_code != 200:
                logging.getLogger(__name__).warning(
                    "HttpClient post:%s failure,params:%s,res:%s" % (url, data, res.text))
                return res
            else:
                return json.loads(res.text)

        except HttpException as e:
            logging.getLogger(__name__).error("HttpClient post error:%s,params:%s Exception:%s" % (url, data, e))
            traceback.print_exc()

    def _sign(self, data, key):
        # 签名函数，参数为签名的数据和密钥
        data['appid'] = self.appId
        params_list = sorted(data.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
        params = []
        for key, val in params_list:
            if val:
                # print("key=>%s val=>%s" % (key, val))
                if isinstance(val, (dict, list)):
                    if isinstance(val, dict):
                        val = sorted(val.items(), key=lambda e: e[0], reverse=False)
                    try:
                        val = json.dumps(val, separators=(',', ':'))
                    except TypeError as e:
                        val = json.dumps(val, cls=Encoder, separators=(',', ':'))
                        # val = val.replace(' ','').replace("\r", '').replace("\n", '').replace("\r\n", '')
                params.append((key, val))
        params_str = urllib.parse.urlencode(params) + self.secret
        # 组织参数字符串并在末尾添加商户交易密钥
        md5 = hashlib.md5()  # 使用MD5加密模式
        md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
        sign = md5.hexdigest().upper()  # 完成加密并转为大写
        return sign


class Encoder(json.JSONEncoder):
    def default(self, obj):
        """
        只要检查到了是bytes类型的数据就把它转为str类型
        :param obj:
        :return:
        """
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


class HttpException(Exception):
    pass
