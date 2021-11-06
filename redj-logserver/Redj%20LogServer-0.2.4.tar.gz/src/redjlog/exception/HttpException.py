from .ExceptionHandler import handler
from ..management.setting import Massage


def handler400(request, exception):
    message = Massage.auth_massage
    return handler(request, message, 400)


def handler403(request, exception):
    message = Massage.permission_massage
    return handler(request, message, 403)


def handler404(request, exception):
    message = Massage.not_found_massage
    return handler(request, message, 404)


def handler500(request):
    message = Massage.other_massage
    return handler(request, message)
