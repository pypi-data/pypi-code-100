class InvalidApiKeyException(Exception):
    '''No API key has been set or it is malformed.'''
    def __init__(self):
        super().__init__('[ERROR]: No API key has been set or it is malformed.')

class BadRequestException(Exception):
    '''Client has sent a bad request.'''
    def __init__(self, msg = 'Validation has failed.'):
        super().__init__(f'[ERROR]: {msg}')

class NotFoundException(Exception):
    """Cannot find that resource."""
    def __init__(self):
        super().__init__("[ERROR]: Cannot find that resource.")

class AuthenticationException(Exception):
    """The request could not be authenticated."""
    def __init__(self):
        super().__init__("[ERROR]: The request could not be authenticated.")

class AuthorizationException(Exception):
    """The request could not be authorized."""
    def __init__(self):
        super().__init__("[ERROR]: The request could not be authorized.")

class ServerErrorException(Exception):
    """An internal server error occurred."""
    def __init__(self):
        super().__init__("[ERROR]: An internal server error occurred.")

class RequestException(Exception):
    '''A generic error occured making the request, e.g. timeout, network not available, etc.'''
    def __init__(self):
        super().__init__('[ERROR]: An unknown error occurred sending the request.')

