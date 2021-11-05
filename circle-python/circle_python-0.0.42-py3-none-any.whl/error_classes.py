from circle import error

ERROR_CLASSES = {
    error.UnknownError.code: error.UnknownError,
    error.MalformedAuthorizationError.code: error.MalformedAuthorizationError,
    error.InvalidEntity.code: error.InvalidEntity,
    error.ForbiddenError.code: error.ForbiddenError,
    error.CardAccountNumberError.code: error.CardAccountNumberError,
    error.PaymentNotFound.code: error.PaymentNotFound,
    error.PaymentAmountInvalid.code: error.PaymentAmountInvalid,
    error.InvalidPaymentCurrency.code: error.InvalidPaymentCurrency,
    error.IdempotencyAlreadyBound.code: error.IdempotencyAlreadyBound,
    error.InvalidSourceAmount.code: error.InvalidSourceAmount,
    error.SourceNotFound.code: error.SourceNotFound,
    error.InvalidWireRoutingNumber.code: error.InvalidWireRoutingNumber,
}
