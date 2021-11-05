class BaseSDKException(Exception):
    def __init__(self, message):
        super().__init__(message)

class ResourceException(BaseSDKException):

    def __init__(self, message):
        super().__init__(message)


class AuthException(BaseSDKException):
    def __init__(self, reason=''):
        if reason != '':
            super().__init__(reason)
        super().__init__('invalid token')



