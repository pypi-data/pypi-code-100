import json
import logging

SUCCESS = 0

log = logging.getLogger(__name__)


class StateError(Exception):
    def __init__(self, error):
        super(error)
        self.error = error


class Result:
    def __init__(self, status, value):
        self.logger = log
        self.status = status
        self.value = value

    @classmethod
    def success(cls, value):
        log.debug(f"create success value of result[{value}]")
        return Result(SUCCESS, value)

    @classmethod
    def failed(cls, error):
        log.debug(f"create failure error of [{error}]")
        return Result(error, None)

    def map(self, func):
        if self.isSuccess():
            self.logger.debug(f"call map function with value [{self.value}]")
            call = result(func)
            return call(self.value)
        else:
            self.logger.debug(f"ignore map call because result failure [{self.status}]")
            return self

    def flatMap(self, func):
        if self.isSuccess():
            self.logger.debug(f"call flatmap function with value [{self.value}]")
            return func(self.value)
        else:
            self.logger.debug(f"ignore flatmap call because result failure [{self.status}]")
            return self

    def isSuccess(self):
        return self.status == SUCCESS

    def isFailed(self):
        return self.status != SUCCESS

    def get(self):
        if self.isSuccess():
            return self.value
        else:
            raise StateError(self.status)

    def json(self):
        """
        生成 json 对象，要求 value 本身是可以被 json 库处理的数据结构，或者提供了 json 方法。
        :return:生成的 json 字符串。包含状态和数据。
        """
        if self.isSuccess():
            status = "ok"
        else:
            status = self.status

        if hasattr(self.value, "json"):
            data = self.value.json()
        else:
            data = self.value

        return json.dumps({
            "state": status,
            "result": data
        })


def success(result):
    return Result(SUCCESS, result)


def failed(error):
    return Result(error, None)


def result(func):
    def call(*args, **argv):
        try:
            value = func(*args, **argv)
            return success(value)
        except Exception as error:
            return failed(error)

    return call


def either(func):
    def call(*args, **argv):
        try:
            error, value = func(*args, **argv)
            status = SUCCESS if error is None else error
            return Result(status, value)
        except Exception as error:
            return failed(error)

    return call
