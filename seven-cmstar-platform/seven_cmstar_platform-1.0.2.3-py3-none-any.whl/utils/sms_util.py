# -*- coding:utf-8 -*-
"""
:Author: SunYiTan
:Date: 2021/5/14 17:01
:LastEditTime: 2021/5/14 17:01
:LastEditors: SunYiTan
:Description: 发放短信
"""
import logging
import sys

import baidubce.services.sms.sms_client as sms
import baidubce.exception as ex
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.bce_client_configuration import BceClientConfiguration

from seven_cmstar_platform.utils.json_util import JsonUtil


class SmsUtil:
    __HOST = "smsv3.bj.baidubce.com"
    __AK = "e3c23bd302c74c98a1d9fa15a68d9e94"
    __SK = "6b6c6143476748a988321f227422a493"

    @classmethod
    def send_message(cls, telephone: str, code: str):
        """
        发送端口，百度云短信接口：https://cloud.baidu.com/doc/SMS/s/3kipnj5wy
        :param telephone: 手机号
        :param code: 验证码
        :return:
        国际签名：sms-sign-wwUrTf25461（萌萌天降），sms-sign-HiUUNh29125（厘米星球）
        国际模板：sms-tmpl-QNNbdj03873
        国内签名：sms-sign-HeqOud39874（萌萌天降），sms-sign-IIKPSL48159（厘米星球）
        国内模板：sms-tmpl-yFCOzU65414
        """
        try:
            sms_client = sms.SmsClient(BceClientConfiguration(credentials=BceCredentials(cls.__AK, cls.__SK),
                                                              endpoint=cls.__HOST))
            sms_sign = "sms-sign-IIKPSL48159"  # 厘米星球
            # if "--production" in sys.argv:
            #     sms_sign = "sms-sign-HeqOud39874"  # 萌萌天降

            # 验证码${code}，您正在注册成为新用户，感谢您的支持！
            response = sms_client.send_message(signature_id=sms_sign,
                                               template_id='sms-tmpl-yFCOzU65414',
                                               mobile=telephone,
                                               content_var_dict={'code': code, 'time': "5"})
            print(response)

            if response.code == "1000":
                return True
            else:
                logging.getLogger("log_error").error(f"send sms fail, code: {response.code}, msg: {response.message}")
                return False

        except ex.BceHttpClientError as e:
            if isinstance(e.last_error, ex.BceServerError):
                logging.getLogger("log_error").error('send sms failed. Response %s, code: %s, request_id: %s'
                                                     % (e.last_error.status_code, e.last_error.code,
                                                        e.last_error.request_id))
            else:
                logging.getLogger("log_error").error('send sms failed. Unknown exception: %s' % e)
            return False

        except Exception as e:
            logging.getLogger("log_error").error('send sms failed. Unknown exception: %s' % e)
            return False

    @classmethod
    def send_message_new(cls, telephone: str, sms_sign, template_id, content_var_dict):
        """
        发送端口，百度云短信接口：https://cloud.baidu.com/doc/SMS/s/3kipnj5wy
        :param telephone: 手机号，多个手机号之间以英文逗号分隔，一次请求最多支持200个手机号
        :param code: 验证码
        :return:
        国际签名：sms-sign-wwUrTf25461（萌萌天降），sms-sign-HiUUNh29125（厘米星球）
        国际模板：sms-tmpl-QNNbdj03873
        国内签名：sms-sign-HeqOud39874（萌萌天降），sms-sign-IIKPSL48159（厘米星球）
        国内模板：sms-tmpl-yFCOzU65414
        """
        try:
            sms_client = sms.SmsClient(BceClientConfiguration(credentials=BceCredentials(cls.__AK, cls.__SK),
                                                              endpoint=cls.__HOST))
            response = sms_client.send_message(signature_id=sms_sign,
                                               template_id=template_id,
                                               mobile=telephone,
                                               content_var_dict=content_var_dict)
            print(JsonUtil.dumps(response))

            if response.code == "1000":
                return True
            else:
                logging.getLogger("log_error").error(f"send sms fail, code: {response.code}, msg: {response.message}")
                return False

        except ex.BceHttpClientError as e:
            if isinstance(e.last_error, ex.BceServerError):
                logging.getLogger("log_error").error('send sms failed. Response %s, code: %s, request_id: %s'
                                                     % (e.last_error.status_code, e.last_error.code,
                                                        e.last_error.request_id))
            else:
                logging.getLogger("log_error").error('send sms failed. Unknown exception: %s' % e)
            return False

        except Exception as e:
            logging.getLogger("log_error").error('send sms failed. Unknown exception: %s' % e)
            return False
