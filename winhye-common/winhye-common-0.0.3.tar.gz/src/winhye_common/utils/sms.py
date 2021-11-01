# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
# 阿里云短信  todo 未测试
import sys
import json
from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(access_key_id: str, access_key_secret: str, ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    # 同步发送
    @staticmethod
    def main(args: List[str], ) -> None:
        # 分别为 AccessKey ID AccessKey Secret
        client = Sample.create_client('LTAI5tG9WoZ4CQpdfEHhfVCb', 'FuOX7YpIG3sqPVENmb6ryYdhFubVJl')
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers="13032643571",  # 要发送的手机号  必填
            sign_name="北京云汉通航科技有限公司",  # 短信签名名称  必填
            template_code="SMS_223060267",  # 短信模板ID  必填
            template_param='{"code":"1111"}',  # 短信模板变量对应的实际值
            # sms_up_extend_code='',  # 上行短信扩展码
            # out_id=''  # 外部流水扩展字段
        )
        # 复制代码运行请自行打印 API 的返回值
        result = client.send_sms(send_sms_request)
        print(result)

    # 异步发送
    @staticmethod
    async def main_async(args: List[str], ) -> None:
        # 分别为 AccessKey ID AccessKey Secret
        client = Sample.create_client('LTAI5tG9WoZ4CQpdfEHhfVCb', 'FuOX7YpIG3sqPVENmb6ryYdhFubVJl')
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers="13032643571",  # 要发送的手机号  必填
            sign_name="验证码短信",  # 短信签名名称  必填
            template_code="SMS_223060267",  # 短信模板ID  必填
            template_param='{"code":"1111"}',  # 短信模板变量对应的实际值
            # sms_up_extend_code='',  # 上行短信扩展码
            # out_id=''  # 外部流水扩展字段
        )
        # 复制代码运行请自行打印 API 的返回值
        await client.send_sms_async(send_sms_request)


if __name__ == '__main__':
    Sample.main([])
