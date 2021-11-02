import unittest
import dg_sdk
from tests.conftest import *


class TestRequestTools(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_request_post(self):
        request_params = {
            "trade_type": "A_NATIVE",
            "trans_amt": "0.01","："""
            "goods_desc": "goods_desc"
        }
        result = dg_sdk.request_post("https://api.huifu.com/v2/trade/payment/jspay", request_params)
        assert result["resp_code"] == "00000100"

    def test_request_post_v1(self):
        # dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key_v1, public_key_v1, sys_id_v1, product_id_v1,
        #                                               huifu_id_v1)
        request_params = {
            "huifu_id": huifu_id ,
            "trade_type": "A_NATIVE",
            "mer_ord_id": dg_sdk.generate_mer_order_id(),
            "trans_amt": "0.01",
            "goods_desc": "goods_desc",
            "notify_url": "virgo://http://www.xxx.com/getResp"
        }

        result = dg_sdk.request_post_v1("https://spin.cloudpnr.com/top/trans/pullPayInfo", request_params)
        assert result["resp_code"] == "00000100"
