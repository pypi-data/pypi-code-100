# url path 统一管理 花括号中变量代表待替换值
from dg_sdk.core.api_request import ApiRequest

from dg_sdk.core.api_request_v1 import ApiRequest as ApiRequestV1
from dg_sdk.dg_client import DGClient
from dg_sdk.common_util import generate_mer_order_id
import datetime

# ---------- 聚合正扫----------
scan_payment_create = '/v2/trade/payment/jspay'  # 聚合正扫
scan_payment_close = '/v2/trade/payment/scanpay/close'  # 交易关单
scan_payment_close_query = '/v2/trade/payment/scanpay/closequery'  # 交易关单查询
scan_payment_query = '/v2/trade/payment/scanpay/query'  # 交易查询
scan_payment_refund = '/v2/trade/payment/scanpay/refund'  # 交易退款
scan_payment_refund_query = '/v2/trade/payment/scanpay/refundquery'  # 退款查询

payment_confirm = "/v2/trade/payment/delaytrans/confirm"  # 交易确认
payment_confirm_query = "/v2/trade/payment/delaytrans/confirmquery"  # 交易确认查询
payment_confirm_refund = "/v2/trade/payment/delaytrans/confirmrefund"  # 交易确认退款

payment_confirm_list = "/topqur/payConfirmListQuery"  # 交易确认列表查询

withhold_pay = "/v2/trade/onlinepayment/withholdpay"  # 代扣

# ---------- 反扫----------
offline_payment_scan = '/v2/trade/payment/micropay'  # 聚合反扫
union_user_id = '/v2/trade/payment/usermark/query'  # 获取银联用户标识

# ---------------快捷支付-------------------

card_payment_page_pay = '/v2/trade/onlinepayment/quickpay/pageinfo'  # 快捷支付页面版
card_bind_apply = '/ssproxy/verifyCardApply'  # 快捷绑卡申请
card_bind_confirm = '/ssproxy/verifyCardConfirm'  # 快捷绑卡确认
card_un_bind = ''  # 快捷卡解绑

card_payment_apply = '/v2/trade/onlinepayment/quickpay/apply'  # 快捷支付申请
card_payment_confirm = '/v2/trade/onlinepayment/quickpay/confirm'  # 快捷支付确认
card_payment_sms = ''  # 短信重发

# ---------------线上交易-------------------
union_app_pay = '/v2/trade/onlinepayment/unionpay'  # 银联APP 支付
wap_pay = '/v2/trade/onlinepayment/wappay'  # 手机网页支付

online_payment_query = '/v2/trade/onlinepayment/query'  # 查询
online_payment_refund = '/v2/trade/onlinepayment/refund'  # 退款
online_payment_refund_query = '/v2/trade/onlinepayment/refund/query'  # 退款查询

# ------------------余额支付----------------
account_payment_create = '/v2/trade/acctpayment/pay'  # 余额支付创建
account_payment_query = '/v2/trade/acctpayment/pay/query'  # 余额支付查询
account_payment_refund = '/v2/trade/acctpayment/refund'  # 余额支付退款
account_payment_query_refund = '/v2/trade/acctpayment/refund/query'  # 余额支付退款查询
account_balance_query = '/v2/trade/acctpayment/balance/query'  # 余额信息查询

# ------------------取现--------------------

drawcash_create = '/v2/trade/settlement/enchashment'  # 创建取现
drawcash_query = '/v2/trade/settlement/query'  # 出金交易查询

# ------------------代发--------------------

surrogate_create = '/v2/trade/settlement/surrogate'  # 创建代发

# ------------------银行卡分期支付--------------------

bank_credit_sign = '/v2/trade/installment/bccredit/sign'  # 银行卡分期支付签约
bank_credit_payment = '/trade/installment/bccredit/pay'  # 一段式分期支付
bank_credit_payment_apply = '/v2/trade/installment/bccredit/apply'  # 二段式分期支付申请
bank_credit_payment_confirm = '/v2/trade/installment/bccredit/confirm'  # 二段式分期支付确认
bank_credit_refund = '/v2/trade/installment/bccredit/refund'  # 银行卡分期退款
bank_credit_query = '/v2/trade/installment/bccredit/query'  # 银行卡分期查询



# 调用域名
BASE_URL = 'https://api.huifu.com'
BASE_URL_V1 = 'https://spin.cloudpnr.com'


def __request_init(url, request_params, base_url=BASE_URL):
    mer_config = DGClient.mer_config

    if mer_config is None:
        raise RuntimeError('SDK 未初始化')

    if "huifu_id" not in request_params:
        request_params['huifu_id'] = mer_config.huifu_id

    if BASE_URL in url:
        ApiRequest.base_url = url
        url = ""
    else:
        ApiRequest.base_url = base_url

    ApiRequest.build(mer_config.product_id, mer_config.sys_id, mer_config.private_key, mer_config.public_key, url,
                     request_params, DGClient.connect_timeout)


def request_post(url, request_params, files=None, base_url=None):
    """
    网络请求方法
    :param url: 请求地址
    :param request_params: 请求参数
    :param files: 附带文件，可为空
    :param base_url: 请求地址基本域名，可为空，默认为 https://api.huifu.com
    :return: 网络请求返回内容
    """

    if base_url is None:
        base_url = BASE_URL
    ApiRequest.sdk_version = DGClient.__version__

    if not request_params.get('req_seq_id'):
        request_params['req_seq_id'] = generate_mer_order_id()

    if not request_params.get('req_date'):
        request_params['req_date'] = datetime.datetime.now().strftime('%Y%m%d')

    __request_init(url, request_params, base_url)
    return ApiRequest.post(files)


def request_post_without_seq_id(url, request_params, files=None, base_url=None):
    if base_url is None:
        base_url = BASE_URL
    ApiRequest.sdk_version = DGClient.__version__
    __request_init(url, request_params, base_url)
    return ApiRequest.post(files)


def request_post_v1(url, request_params, files=None, base_url=None):
    """
    网络请求方法，V1 版本接口
    :param url: 请求地址
    :param request_params: 请求参数
    :param files: 附带文件，可为空
    :param base_url: 请求地址基本域名，可为空，默认为 https://spin.cloudpnr.com
    :return: 网络请求返回内容
    """
    if not request_params.get('req_seq_id'):
        request_params['req_seq_id'] = generate_mer_order_id()

    if not request_params.get('req_date'):
        request_params['req_date'] = datetime.datetime.now().strftime('%Y%m%d')
    if base_url is None:
        base_url = BASE_URL_V1

    mer_config = DGClient.mer_config

    if mer_config is None:
        raise RuntimeError('SDK 未初始化')

    if "huifu_id" not in request_params:
        request_params['huifu_id'] = mer_config.huifu_id

    if BASE_URL_V1 in url:
        ApiRequestV1.base_url = url
        url = ""
    else:
        ApiRequestV1.base_url = base_url
    ApiRequestV1.sdk_version = DGClient.__version__
    ApiRequestV1.build(mer_config.product_id, mer_config.sys_id, mer_config.private_key, mer_config.public_key, url,
                       request_params, DGClient.connect_timeout)
    return ApiRequestV1.post(files)
