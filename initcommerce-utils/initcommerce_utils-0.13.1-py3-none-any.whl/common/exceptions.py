import abc
import re

from graphql import GraphQLError


class InitCommerceBaseException(GraphQLError, metaclass=abc.ABCMeta):
    path = None
    locations = None
    original_error = None
    message = "INIT_COMMERCE_BASE_EXCEPTION"

    code: str = None

    def __init__(self, message=None, *args, **kwargs):
        super().__init__(message=message or self.message, *args, **kwargs)

        if self.code is not None:
            errorcode = self.code.replace(" ", "_").upper()
        else:
            class_name = self.__class__.__name__
            errorcode = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).upper()

        self.extensions = dict(
            code=errorcode,
        )
