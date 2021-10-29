"""
Classes for default api/http exceptions
"""

class VkError(Exception):
    """Base class for all errors raised by vk API"""


class VkApiError(VkError):
    """API method Errors"""

    def __init__(self, error):
        super().__init__()

        self.code = error['error_code']
        self.error = error


    def __str__(self):
        return 'VkApi method error[{}]: {}'.format(
            self.error['error_code'],
            self.error['error_msg'])


class VkHttpError(VkError):
    """Basic HTTPErors"""

    def __init__(self, response):
        super().__init__()
        self.response = response
        
    def __str__(self):
        return 'Response code: [{}] Content: {}'.format(self.response.status_code,
                                                        self.response)
    
    
class VkTokenError(VkError):
    """Errors associated with access token.
    (eg. Nonexistent, Expired, Blocked)
    """

    def __init__(self, error):
        super().__init__()
        self.error = error

    def __str__(self):
        return 'Your Token is not valid. Try getting a new one.\
            \nDetails: [{}] {}'.format(self.error['error_code'],
                                       self.error['error_msg'])
