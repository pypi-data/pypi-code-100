import json
import re
import time
import traceback
from datetime import datetime, timedelta, date as dt
from typing import Optional, Awaitable, Dict, List
from urllib import parse

from tornado.gen import coroutine
from tornado.web import RequestHandler, MissingArgumentError, Finish

from mbutils import DefaultMaker, MbException, ARG_DEFAULT, logger
from mbutils.constant import ErrorType, ValidType


class MBHandler(RequestHandler):
    """
    调用顺序
    set_default_headers()
    initialize()
    prepare()
    HTTP方法,get,post
    set_default_headers()
    write_error()
    on_finish()
    """

    def set_default_headers(self) -> None:
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Headers", "content-type,token,id, Authorization");
        self.set_header("Access-Control-Request-Headers",
                        " Origin, X-Requested-With, content-Type, Accept, Authorization");
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')

    def _get_arguments(
            self, name: str, source: Dict[str, List[bytes]], strip: bool = True
    ) -> List[str]:
        """
            目的是为了支持body是json的写法
        """
        values = []
        if self.request.body:
            values = self.request.arguments.get(name, [])
        else:
            values = super(MBHandler, self)._get_arguments(name, source, strip)
        return values

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self):
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    @staticmethod
    def quote_2_json(body: str):
        """
        gmt_create=2021-07-23+18:58:47&charset=utf-8&seller_email=qiyiqikeji@163.com&subject=骑币充值&sign=kfFjvEu8S7E/ya4xC4KXx5lJvUsa+fxtho7WD+Glxws1+t8QEGt/h/5P05LkDMGrn3gbzmJONVNmDk6LuR7j6Jkj1DgqgQggnfkO0jRg50oZlrr/cAhpc3DVbwpjV9Lx55UGrNIvYuNGRMaVYRrTEqsgyx+c9gHjLYvs2PZGcHEFBEp/dgEGpNgEbPgw+gFRAeRiZlQyfGsRLDjkwcfaByXXzU7zVPOEx11KqE8fo9QbkB9nPgoY1OkyYv+jFGUCAIftX9rr0ZbZPYQfrI5Zy2r0LLuCqZDboFuErG2MjG8YI5vqGsJB3aDlNVjXeQM2qp8b2LGTqUv1UQujiLKwDw==&buyer_id=2088212826576182&invoice_amount=0.01&notify_id=2021072300222185848076181411022901&fund_bill_list=[{"amount":"0.01","fundChannel":"ALIPAYACCOUNT"}]&notify_type=trade_status_sync&trade_status=TRADE_SUCCESS&receipt_amount=0.01&app_id=2019022263253609&buyer_pay_amount=0.01&sign_type=RSA2&seller_id=2088431218818781&gmt_payment=2021-07-23+18:58:48&notify_time=2021-07-23+18:58:48&passback_params={"objectId":"60fa5522f69486000112ef90"}&version=1.0&out_trade_no=20210723389188091214502781970036&total_amount=0.01&trade_no=2021072322001476181451511504&auth_app_id=2019022263253609&buyer_logon_id=158****5754&point_amount=0.00
        """
        json_body = {}
        data_list = body.split('&')
        for data in data_list:
            key_value_list = data.split('=', maxsplit=1)
            json_body[key_value_list[0]] = key_value_list[1]
        return json_body

    @coroutine
    def prepare(self):
        for middleware in self.application.middle_ware_list:
            try:
                yield middleware.before(self)
            except MbException as mb:
                raise mb
            except Finish:
                raise Finish()
            except Exception as ex:
                raise MbException(promt=str(middleware))
        if self.request.body:
            try:
                if self.request.headers.get("Content-Type") == "text/xml":
                    pass
                elif self.request.headers.get("Content-Type") == "application/xml; charset=utf-8":
                    pass
                elif self.request.headers.get("Content-Type").split(";")[0] == "application/x-www-form-urlencoded":
                    # 统一处理 把表单的数据改成json
                    body = self.request.body.decode('utf8')
                    body = parse.unquote_plus(body)
                    self.request.quote_body = body
                    json_body = self.quote_2_json(body)
                    self.request.body = json_body
                    self.request.arguments.update({k: [v] for k, v in json_body.items()})
                else:
                    json_body = json.loads(self.request.body)
                    self.request.arguments.update({k: [v] for k, v in json_body.items()})
            except Exception as ex:
                raise MbException(promt=f'body is not json，Content-Type：{self.request.headers.get("Content-Type")}')

    @coroutine
    def on_finish(self):
        reverse_list = self.application.middle_ware_list[::-1]
        if self.request.method == 'HEAD' or self.request.method == 'OPTIONS':
            return
        for middleware in reverse_list:
            try:
                yield middleware.after(self)
            except MbException as mb:
                raise mb
            except Exception as ex:
                raise MbException(promt=str(middleware))

    def valid_data_all(self, rules: list):
        """
        验证多个数据,用法如下：
        self.valid_data_all([('A', ValidType.INT, {"funcs":[lambda x: x > 4, la]}),
                             ("B", ValidType.STR, {"funcs":[lambda x: isinstance(x, UserState)]} ),
                             ("C", ValidType.URL, {"must":True, "default":0})])
        说明：
            1.对于没有给默认值的参数，给了默认值""
            2.对于配置funcs并且不为空，可以不配置must
            3.对于dict和list的内部结构，暂不支持解析
        :param rules: [(name, tp, {"must":True, "funcs":[], "default"=20, "strip":True})],
            name表示请求参数的名称，必填
            tp 是 ValidType，必填
            {"must":True, "funcs":[], "default"=20, "strip":True} 选填，分别表示：must请求参数不可缺失，
            funcs是lambda表达式列表， default是默认值， strip是是否字符去空格
        :return: () 验证后的所有参数
        :except: MbException('params {} invalid'.format(name), ErrorType.INPUT_PARAMS_MISS)
        """
        res = []
        for rule in rules:
            if not (1 <= len(rule) <= 3):
                raise MbException('The number of parameters received by the valid_data_all is 2 to 3')
            params = {
                "must": False,
                "funcs": [],
                "default": ARG_DEFAULT,
                "strip": True
            }
            length = len(rule)
            if length == 1:
                name, = rule
                value = self.get_argument(name, ARG_DEFAULT)
            if length == 2:
                name, tp = rule
                value = self.get_argument(name, ARG_DEFAULT)
                flag, value = self.validate(value, tp)
                if not flag:
                    raise MbException('params {} invalid'.format(name), ErrorType.INPUT_PARAMS_MISS)
            if length == 3:
                name, tp, optional = rule
                if optional:
                    params.update(optional)
                if params["must"]:
                    try:
                        value = self.get_argument(name, strip=params["strip"])
                    except MissingArgumentError:
                        raise MbException('params {} miss'.format(name), ErrorType.INPUT_PARAMS_MISS)
                else:
                    value = self.get_argument(name, params["default"], params["strip"])
                flag, value = self.validate(value, tp, params["funcs"])
                if not flag:
                    raise MbException('params {} invalid'.format(name), ErrorType.INPUT_PARAMS_MISS)
            res.append(value)
        return tuple(res)

    def valid_data(self, name: str, tp: ValidType = ValidType.STR, **optional):
        """
        验证单个数据, 参考valid_data_all

        """
        params = {
            "must": False,
            "funcs": [],
            "default": "",
            "strip": True
        }
        if optional:
            params.update(optional)
        if params["must"]:
            try:
                value = self.get_argument(name, params["strip"])
            except MissingArgumentError:
                raise MbException('params {} miss'.format(name), ErrorType.INPUT_PARAMS_MISS)
        else:
            value = self.get_argument(name, ARG_DEFAULT, params["strip"])  #
        flag, value = self.validate(value, tp, params["funcs"])
        if not flag:
            raise MbException('params {} invalid'.format(name), ErrorType.INPUT_PARAMS_MISS)
        return value

    def origin_write(self, data=""):
        self.write(data)
        self.request.response = data

    def success(self, chunk=""):
        """
        success和error方法是用来格式化返回的
        :param chunk: str, dict, list, int
        """
        data = {"suc": True, "data": chunk}
        self.write(data)
        self.request.response = data

    def error(self, promt: str = "", tp: ErrorType = ErrorType.BIZ_ERROR):
        """
        错误兼容node的写法

        :param tp: 错误类型
        :param promt: 错误提示语句
        :return:
        """
        data = {"suc": False, "error": {
            "err": self.request.uri,
            "errType": tp.name,
            "promt": promt,
            "ErrMessage": tp.value
        }}
        self.write(data)
        self.request.response = data
        logger.error(data)

    def write_error(self, status_code, **kwargs) -> None:
        """
        全局捕获异常的地方,一般不修改
        """
        self.set_status(200)
        etype, value, _ = kwargs.get("exc_info")
        if etype == MbException:
            promt, tp = value.promt, value.error_type
            data = {"suc": False, "error": {
                "err": self.request.uri,
                "errType": tp.name,
                "promt": promt,
                "promot": promt,
                "ErrMessage": tp.value
            }}
            self.finish(data)
            self.request.response = data
        else:
            error_list = traceback.format_exception(*kwargs.get("exc_info"))
            self.set_header("Content-Type", "text/plain")
            for line in error_list:
                self.write(line)
            self.finish()
            one_line_error = (''.join(error_list)).replace("\n", "")
            logger.error(one_line_error)  # value直接的异常类型无法打印
            self.request.response = one_line_error

    @staticmethod
    def validate(value, tp: ValidType = ValidType.STR, funcs=[]):
        """
        基础的验证器函数
        :param value:参数
        :param tp: "INT", "FLOAT", "STR", "LIST", "DICT", "URL", "UUID", "IPV4", "EMAIL"
        :param funcs: lambda函数列表，可以为空，
            例如：
            大小范围，lambda x：1<x<10
            是否是真， lambda x: x==True
            在某个范围， lambda x: x in ['0', '1']
            枚举类型对象，lambda x: isinstance(x, User_State),
            长度限制， lambda x: len(x)<10
        :return:bool, value
        """
        if isinstance(value, DefaultMaker):
            return True, value
        if isinstance(value, bytes):
            value = value.decode()
        if tp == ValidType.INT:
            try:
                value = int(value)
            except Exception:
                return False, None
        elif tp == ValidType.FLOAT:
            try:
                value = float(value)
            except Exception:
                return False, None
        elif tp == ValidType.STR:
            if not isinstance(value, str):
                return False, None
        elif tp == ValidType.LIST:
            if not isinstance(value, list):
                return False, None
        elif tp == ValidType.DICT:
            if not isinstance(value, dict):
                return False, None
        elif tp == ValidType.URL:
            patterns = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
            if not patterns.fullmatch(value):
                return False, None
        elif tp == ValidType.UUID:
            patterns = re.compile(r"\w{8}(-\w{4}){3}-\w{12}")
            if not patterns.fullmatch(value):
                return False, None
        elif tp == ValidType.IPV4:
            patterns = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
            if not patterns.fullmatch(value):
                return False, None
        elif tp == ValidType.EMAIL:
            patterns = re.compile(r"^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$")
            if not patterns.fullmatch(value):
                return False, None
        elif tp == ValidType.BOOL:
            value = True if value else False  # 广义上的bool
        else:
            return False, None
        for f in funcs:
            if not f(value):
                return False, None
        return True, value

    @staticmethod
    def amount_accuracy(num: float):
        return float("{:.2f}".format(num))

    def get_everyday_list(self, begin_time: int, end_time: int):
        begin_time = self.int_to_datetime(begin_time)
        end_time = self.int_to_datetime(end_time)
        return [(begin_time + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_time - begin_time).days + 1)]

    @staticmethod
    def int_to_datetime(time_int: int):
        # 目前系统查询数据不会早于2001-09-09 09:46:39，所以可以根据长度判断是毫秒（13）还是秒（10），如果有数据进来，则将直接返回
        time_length = len(str(time_int))
        if time_length == 13 or time_length == 10:
            if time_length == 13:
                time_int = time_int / 1000
            return datetime.fromtimestamp(time_int)
        else:
            return False

    #  获取今天零点，昨天零点的时间，昨天23点59分59秒的时间
    @staticmethod
    def acquire_time():
        day_time_zero = int(time.mktime(dt.today().timetuple())) * 1000  # 今天零点的时间
        day_time_end = day_time_zero + 24 * 60 * 60 * 1000 - 1  # 今天零点的时间
        yesterday_time_zero = day_time_zero - 24 * 60 * 60 * 1000  # 昨天零点的时间
        yesterday_time_end = day_time_zero - 1  # 昨天23点59分59秒的时间
        before_yesterday_time_end = yesterday_time_zero - 1  # 前天23点59分59秒的时间
        return day_time_zero, day_time_end, yesterday_time_zero, yesterday_time_end, before_yesterday_time_end

    @staticmethod
    def dict_and_add(dict1, dict2):
        """
        @param dict1: 字典，value为可相加的对象
        @param dict2: 字典，value为可相加的对象
        @return: 将两个相同的字典合并，相同的建值相加
        """
        for key, value in dict2.items():
            if key in dict1:
                dict1[key] += value
            else:
                dict1[key] = value
        return dict1

    def json4biz(self, tp: int):
        authorization = self.request.xc_basic_info
        ROUTER_MAP = {
            '121001': 'tools-openBatBox',  # 开始换电
            '121002': 'tools-closeBatBox',  # 完成换电

            '122001': 'moveVehicle-start',  # 单台开始挪车
            '122002': 'moveVehicle-end',  # 单台结束挪车
            "122003": "moveVehicle-batchStart",  # 批量开始挪车
            '122004': 'moveVehicle-batchEnd',  # 批量结束挪车

            '125001': 'tools-getDevStatus',  # 获取车辆状态
            '125002': 'tools-moveEbike-start',  # 开始挪车
            '125003': 'tools-moveEbike-end',  # 结束挪车
            '129001': 'tools-repair',
            '130001': 'tools-sneak',

        }
        logger.json({
            "lat": authorization.get("gcj02Lat", 0),
            "lng": authorization.get("gcj02Lng", 0),
            "routeEnume": tp,
            "router": ROUTER_MAP[str(tp)],
            "opman": authorization.get("phone", ""),
            "type": "opmanTrajectory",
        })
