import textwrap

import circle


class CircleError(Exception):
    """
    The base class for Circle API response errors
    https://developers.circle.com/docs/api-errors
    """

    def __init__(
        self,
        message=None,
        body=None,
        status_code=None,
        headers=None,
        code=None,
    ):
        # self.message, self.detail = self._parse_message_body(message_body)
        self._message = message

        self._body = body
        self.status_code = status_code
        self.headers = headers or {}
        self.request_id = self.headers.get("X-Request-Id", None)

        self.message = self.construct_message()
        self.errors = self.construct_error_object()

    def construct_message(self):
        if (
            self._body is None
            or "message" not in self._body
            or not isinstance(self._body["message"], str)
        ):
            return self._message

        return self._body["message"]

    def construct_error_object(self):
        if (
            self._body is None
            or "errors" not in self._body
            or not isinstance(self._body["errors"], list)
        ):
            return None
        errors = []
        for error in self._body["errors"]:
            errors.append(
                circle.resources.error_object.ErrorObject.construct_from(
                    error, circle.api_key
                )
            )
        return errors

    def __str__(self):
        msg = self.message
        if self.request_id:
            return f"Request {self.request_id}: {msg}"
        else:
            return msg

    def __repr__(self):
        return f"{self.__class__.__name__}(message={self.message}, status_code={self.status_code}, request_id={self.request_id})"


class APIError(CircleError):
    pass


class AuthenticationError(CircleError):
    pass


class APIConnectionError(CircleError):
    def __init__(
        self,
        message_body,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        # This exception contains a multi line message that shouldn't parse to the usual short message body
        message_body = textwrap.fill(message_body)
        # super().__init__(message, http_body, http_status, json_body, headers, code)
        super().__init__(message_body, http_body, http_status, headers, code)
        self.should_retry = should_retry


# Entity Errors:

# TODO: this might not actually be suited as an exception. Will come back to it.
class CircleEntityErrors(CircleError):

    """
    https://developers.circle.com/docs/api-errors
    """

    pass


class UnknownError(CircleError):
    code = -1

    # def __init__(self, *args, **kwargs):
    #     message = kwargs.get("message", "Unknown error.")
    #     super().__init__(message, *args, **kwargs)


class MalformedAuthorizationError(CircleError):
    """API Key is missing or malformed"""

    code = 1


class InvalidEntity(CircleError):
    code = 2

    # def __init__(self, message=None, *args, **kwargs):
    #     if not message:
    #         message = "Invalid entity"
    #     super().__init__(message, *args, **kwargs)


class ForbiddenError(CircleError):
    code = 3


class CardAccountNumberError(CircleError):
    """The card account number is invalid or missing"""

    code = 1032


class PaymentNotFound(CircleError):
    code = 1051


class PaymentAmountInvalid(CircleError):
    code = 1077


class InvalidPaymentCurrency(CircleError):
    """
    An invalid currency value was used when making a payment
    """

    code = 1077


class IdempotencyAlreadyBound(CircleError):
    code = 1083


class InvalidSourceAmount(CircleError):
    code = 1088


class SourceNotFound(CircleError):
    code = 1089


class InvalidWireRoutingNumber(CircleError):
    code = 1091
