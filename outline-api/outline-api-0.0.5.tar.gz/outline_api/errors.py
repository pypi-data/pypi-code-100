""" Holds local library error types """

class OutlineException(Exception):
    """ Base class for exceptions in Outline API """
    def __init__(self, error_code=1000, message=''):
        """ Set value of error message """
        super(OutlineException, self).__init__()
        self.message = message
        self.error_code = error_code
    def __str__(self):
        """ Output representation of error """
        return repr(self.message)

class OutlineTimeoutError(OutlineException):
    """ Timeout Error Wrapper """

class DoesNotExistError(OutlineException):
    """ Key does not exist Error Wrapper """
