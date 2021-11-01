from dg_sdk.module.request_tools import request_post, request_post_without_seq_id, account_payment_create, \
    account_payment_query, account_payment_query_refund, account_payment_refund, account_balance_query


class AcctPayment(object):
    """
    余额支付相关接口，绑卡，支付，退款，交易查询等
    """

    @classmethod
    def create(cls, ord_amt, **kwargs):
        """
        余额支付订单
        :param ord_amt: 交易金额，单位为元，（例如：100.00）
        :param kwargs:  非必填额外参数
        :return: 支付对象
        """

        required_params = {
            "ord_amt": ord_amt,
        }
        required_params.update(kwargs)
        return request_post(account_payment_create, required_params)

    @classmethod
    def query(cls, org_req_date, *, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        余额支付查询
        :param org_req_date: 原始订单请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param org_req_seq_id: 原始请求流水号
        :param kwargs: 非必填额外参数
        :return: 支付对象
        """

        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id,
        }

        required_params.update(kwargs)
        return request_post_without_seq_id(account_payment_query, required_params)

    @classmethod
    def refund(cls, ord_amt, org_req_date, org_req_seq_id="", org_hf_seq_id="", **kwargs):
        """
        余额支付退款
        :param ord_amt: 退款金额
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始订单请求时间
        :param org_hf_seq_id: 交易返回的全局流水号
        :param kwargs: 非必填额外参数
        """
        required_params = {
            "ord_amt": ord_amt,
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
            "org_hf_seq_id": org_hf_seq_id

        }
        required_params.update(kwargs)
        return request_post(account_payment_refund, required_params)

    @classmethod
    def refund_query(cls, org_req_date, *, org_req_seq_id="", **kwargs):
        """
        余额支付退款查询
        :param org_req_seq_id: 原始请求流水号
        :param org_req_date: 原始退款请求时间
        :param kwargs: 非必填额外参数
        :return: 退款对象
        """
        required_params = {
            "org_req_date": org_req_date,
            "org_req_seq_id": org_req_seq_id,
        }
        required_params.update(kwargs)
        return request_post_without_seq_id(account_payment_query_refund, required_params)

    @classmethod
    def balance_query(cls, **kwargs):
        """
        余额信息查询
        :param kwargs: 非必填额外参数
        :return: 余额信息查询返回报文
        """
        return request_post(account_balance_query, kwargs)
