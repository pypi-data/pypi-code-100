"""
常量
"""
import enum


class MbEnum(enum.Enum):
    """
    1.通过value，获取枚举对象的方法是 SomeStatusEnum(0)
    2.如果存储到数据库，或者返回到前端等外部环境，用SomeStatusEnum.SOMESTATUS.value
    """

    @classmethod
    def to_tuple(cls):
        """
        枚举类的value转成tuple
        """
        return (e.value for e in cls)


class ValidType(MbEnum):
    INT = 0
    FLOAT = 1
    STR = 2
    LIST = 3
    DICT = 4
    URL = 5
    UUID = 6
    IPV4 = 7
    EMAIL = 8
    BOOL = 9


class ErrorType(MbEnum):
    WEB_OPTIONS_ERROR = "WEB_OPTIONS_ERROR"
    BIZ_ERROR = 'BIZ_ERROR'  # 业务错误
    INPUT_PARAMS_MISS = 'INPUT_PARAMS_MISS'  # 入参缺失
    NOT_EXIST_DEVICE = 'NOT_EXIST_DEVICE'  # 该代理商无设备
    DIFFER_BOOKING = 'DIFFER_BOOKING'  # 与预约设备不符
    BOOKING_OUT_TIME = 'BOOKING_OUT_TIME'  # 预约过期
    DEVICE_IN_USING = 'DEVICE_IN_USING'  # 该车辆正在使用
    DEVICE_BROKEN = 'DEVICE_BROKEN'  # 设备异常
    LOCK_FAIL = 'LOCK_FAIL'  # 锁车失败
    UNLOCK_FAIL = 'UNLOCK_FAIL'  # 解锁失败
    TEMP_PARKING_LOCK_FAIL = 'TEMP_PARKING_LOCK_FAIL'  # 临时停车失败
    NO_UNPAY_ORDER = 'NO_UNPAY_ORDER'  # 无未支付订单
    BALANCE_IS_NOT_ENOUGH = 1001  # 钱包余额不足
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'  # 不在服务区
    LOGIN_ON_OTHER_DEVICE = 'LOGIN_ON_OTHER_DEVICE'  # 帐号在其他设备登录
    USER_IS_FORBIDDEN = 'USER_IS_FORBIDDEN'  # 禁止用户登录和进行其他操作（黑名单）
    OUT_OF_PARKING = 'OUT_OF_PARKING'  # 不在停车区

    EBIKE_STATE_ERROR = 'EBIKE_STATE_ERROR'  # 车辆状态异常
    USER_STATE_ERROR = 'USER_STATE_ERROR'  # 用户状态异常
    END_FAIIL = 'END_FAIIL'  # 结束行程失败
    HAS_NOT_BOOKING = 'HAS_NOT_BOOKING'  # 该用户没有预约车辆或者预约已过期
    NOT_MATCH = 'NOT_MATCH'  # 与预约车辆不符
    DEVICE_OFFLINE = 'DEVICE_OFFLINE'  # 设备离线
    TICKETNO_FORMAT_ERROR = 'TICKETNO_FORMAT_ERROR'  # 工单号格式错误

    SEND_CMD_FAIL = 'SEND_CMD_FAIL'  # 发送命令失败
    NO_SIGN_UP = 'NO_SIGN_UP'  # 用户没有注册
    CLOSE_BATBOX_FAIL = 'CLOSE_BATBOX_FAIL'  # 电池仓关闭失败
    OPEN_BATBOX_FAIL = 'OPEN_BATBOX_FAIL'  # 电池仓开启失败
    UPLOAD_FILE_TYPE_ERROR = 'UPLOAD_FILE_TYPE_ERROR'  # 上传文件格式出错
    UPLOAD_CARINFO_ERROR = 'UPLOAD_CARINFO_ERROR'  # 上传车辆信息出错
    PERMISSION_INFO_NOT_EXIST = 'PERMISSION_INFO_NOT_EXIST'  # 权限信息不存在
    PERMISSION_INFO_EXISTED = 'PERMISSION_INFO_EXISTED'  # 权限信息已存在，无法再次加入
    CAR_SEARCHING_FAILED = 'CAR_SEARCHING_FAILED'  # 寻车音播放失败
    CLOSE_TICKET_FAILED = 'CLOSE_TICKET_FAILED'  # 关闭工单失败
    COMPLAINT_FAILED = 'COMPLAINT_FAILED'  # 申述工单失败
    CARID_NO_BINDING = 'CARID_NO_BINDING'  # 车辆未绑定
    CREATE_ALLY_FAILED = 'CREATE_ALLY_FAILED'  # 创建加盟商失败
    UPDATE_ALLY_FAILED = 'UPDATE_ALLY_FAILED'  # 更新加盟商失败
    DELETE_ALLY_FAILED = 'DELETE_ALLY_FAILED'  # 删除加盟商失败
    GET_DEV_INFO_FAILED = 'GET_DEV_INFO_FAILED'  # 获取设备信息失败
    CAR_BINDING_FAILED = 'CAR_BINDING_FAILED'  # 车辆绑定失败
    CAR_UNBINDING_FAILED = 'CAR_UNBINDING_FAILED'  # 车辆解绑失败
    JUDGE_ALLY_INFO_FAILED = 'JUDGE_ALLY_INFO_FAILED'  # 判断加盟商信息失败
    ONLINE_IN_OTHER_SERVICE = 'ONLINE_IN_OTHER_SERVICE'  # 设备已经在其他服务区上架
    AUTH_FAILED = 'AUTH_FAILED'  # 中间件验签鉴权错误
    BIKE_RIDING = 'BIKE_RIDING'  # 用户预约或骑行中，无法上架
    NOT_IN_OPERA_TIME = 'NOT_IN_OPERA_TIME'  # 用户预约或骑行中，无法上架
    CAR_NOT_PUT_ON_SHELF = 'CAR_NOT_PUT_ON_SHELF'  # 车辆未上架
