class I2AChatApiClientJSONDataException(Exception):

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data

    def __str__(self):
        return str(self.data)


class I2AChatApiClientUnauthorizedException(I2AChatApiClientJSONDataException):
    pass


class I2AChatApiClientValidationError(I2AChatApiClientJSONDataException):
    pass


class I2AChatApiClientNotFoundError(I2AChatApiClientJSONDataException):
    pass
