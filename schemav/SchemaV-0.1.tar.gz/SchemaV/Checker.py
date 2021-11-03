class Checker():

    def __init__(self, is_required, value_validator_func, default_value):
        self.__is_required = is_required  # required field
        self.__value_validator_func = value_validator_func  # optional or None
        self.__default_value = default_value  # optional

    def isRequired(self, ):
        return self.__is_required

    def value_validator_func(self, ):
        return self.__value_validator_func

    def default_value(self):
        return self.__default_value
