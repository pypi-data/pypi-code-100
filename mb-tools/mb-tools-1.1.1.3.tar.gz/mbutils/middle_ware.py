import time

import jwt
from tornado.gen import coroutine
from tornado.web import RequestHandler, Finish

from mbutils import MbException
from mbutils import logger
from mbutils.constant import ErrorType
from . import cfg


class MiddleWare:
    def before(self, handler: RequestHandler):
        pass

    def after(self, handler: RequestHandler):
        pass


class Auth(MiddleWare):
    """
    xc_basic_info = {'opAreaIds': [1, 2, 326, 327, 332, 598, 1075, 1076, 2998, 3179, 5654, 6838, 6900, 6989, 7104],
        'userId': '18668146987',
        'phone': '',
        'agentId': 2,
        'build': '',
        'devId': '',
        'package': '',
        'iat': 1591771298}
    """

    def before(self, handler: RequestHandler):
        if handler.request.method == 'HEAD' or handler.request.method == 'OPTIONS':
            raise Finish('HTTP HEAD or OPTIONS')
        handler.request.xc_basic_info = {}  # 插入数据
        if handler.request.uri.startswith('/anfu/v2/') or handler.request.uri.startswith('/share/anfu/v2/'):
            if handler.request.uri == "/anfu/v2/data_fix/k8s":
                return
            try:
                token = handler.request.headers['authorization'].split(' ')[-1]
                handler.request.xc_basic_info = jwt.decode(token, cfg['apiKey'], algorithms=['HS256'])
            except Exception as e:
                logger.info(f"接口鉴权失败 e:{e}， token:{token}, apikey:{cfg['apiKey']}")
                raise MbException('接口鉴权失败', ErrorType.AUTH_FAILED)


class AccessLog(MiddleWare):
    def before(self, handler: RequestHandler):
        handler.request.access_time = time.time()
        handler.request.response = ''

    def after(self, handler: RequestHandler):
        if handler.request.uri in ["/anfu/v2/data_fix/k8s", "/anfu/v2/data_fix/platform/get_log"]:
            return
        run_time = time.time() - handler.request.access_time if hasattr(handler.request, "access_time") else 0
        logger.biz('accessLog, url: {}, method: {}, basicInfo: {}, params: {}, response: {}, time: {}'.format(
            handler.request.uri, handler.request.method,
            handler.request.xc_basic_info,
            handler.request.arguments,
            handler.request.response,
            run_time
        ))


class CheckLoginDevice(MiddleWare):
    @coroutine
    def before(self, handler: RequestHandler):
        if 'xc-basic-info' not in handler.request.headers:
            return
        # basic_info_str = handler.request.xc_basic_info
        # basic_info = json.loads(basic_info_str)
        # if 'objectId' not in basic_info:
        #     return
        # if handler.request.uri.find('/user/deviceId'):
        #     return
        # ebike_user = yield UserService().query_one2({'objectId': basic_info['objectId']})
        # device_id = ebike_user.deviceId
        # if device_id and 'devId' in basic_info and device_id != basic_info['devId']:
        #     raise Exception('LOGIN_ON_OTHER_DEVICE')


class CheckBlackList(MiddleWare):
    @coroutine
    def before(self, handler: RequestHandler):
        # if 'xc-basic-info' not in handler.request.headers:
        #     return
        # basic_info_str = handler.request.headers['xc-basic-info']
        # basic_info = json.loads(basic_info_str)
        # id = basic_info and basic_info['objectId'] or handler.get_argument('xcBasicInfo') and \
        #      handler.get_argument('xcBasicInfo')['userId']
        # if not id:
        #     return
        if not handler.request.xc_basic_info or 'userId' not in handler.request.xc_basic_info:
            return
        user_id = str(handler.request.xc_basic_info['userId'])
        # to0do 中间件的里面，必须优先用缓存，避免查询mysql
        in_blacklist = False
        # in_blacklist = yield mb_async(UserService().query_one)(
        #     {'userId': user_id})  # user_id "5d7a29cf78c27c4011611d1d"
        if in_blacklist:
            logger.info('user {} in blacklist access'.format(user_id))
            agent_id = 2
            name = 'telephoneSet'
            # cfg_set = ConfigService(agent_id).getRouterContent(name, agent_id)
            cfg_set = {'content': '12345678'}
            black_reason = in_blacklist.blackReason  #
            output_reason = '您已被加入黑名单，请联系客服:{}.拉黑原因:{}'.format(
                cfg_set['content'],
                black_reason) if black_reason else '您已被加入黑名单，请联系客服:{}.'.format(
                cfg_set['content'])
            raise MbException(output_reason)


class BlueDeviceInfo(MiddleWare):
    def before(self, handler: RequestHandler):
        # to0do 蓝牙通道需要存储设备基本信息
        pass


middle_ware_list = [Auth(), AccessLog()]
