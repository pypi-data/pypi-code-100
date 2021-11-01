import enum

__all__ = ["ExceptionCode", "WinhyeException"]


# exception codes
class ExceptionCode(enum.Enum):
    DB = 1
    OSS = 2
    mqtt = 3


class WinhyeException(Exception):
    def __init__(self, code: ExceptionCode, message: str):
        self.code = code.value
        self.message = message

    def __str__(self):
        return "{exception}: winhye-common error code={code}, message={message}".format(
            exception=self.__class__.__name__,
            code=self.code,
            message=self.message
        )
