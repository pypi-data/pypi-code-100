
from .. import helper
from . import Exception
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from ..management.setting import Massage, Base as BaseSetting


def handler(request, message="", status=500, save_exception=True):
    if save_exception:
        helper.cPrint('//============')
        helper.cPrint('🚨Redj Log', 'error')
        saveException(request, "http_exception", "", [], message)

    helper.cPrint(message, 'OKCYAN')
    helper.cPrint('============//')
    helper.cPrint('', 'ENDC')

    if BaseSetting.response_type == 'url':
        return redirect(BaseSetting.response_url+'?status='+str(status)+'&message='+message)
    else:
        response = {}
        try:
            if BaseSetting.message_key:
                response[BaseSetting.message_key] = message
            if BaseSetting.status_key:
                response[BaseSetting.status_key] = status
        except:
            pass
        return JsonResponse(response, status=status)


class Base(MiddlewareMixin):
    def process_exception(self, request, exception):
        helper.cPrint('//============')
        if request == None:
            helper.cPrint('⚠️ Redj Log', 'OKBLUE')
        else:
            helper.cPrint('🚨Redj Log', 'error')
        helper.cPrint('', 'ENDC')

        type = 'Other'
        tracebacks = []
        exception_str = ''

        try:
            exception_str = str(exception)
            if exception_str:
                helper.cPrint(exception_str, 'OKCYAN')
                helper.cPrint('', 'ENDC')
        except:
            pass

        try:
            tb = exception.__traceback__
            while tb is not None:
                if "env" not in tb.tb_frame.f_code.co_filename:
                    tracebacks.append({
                        "name": tb.tb_frame.f_code.co_name,
                        "filename": tb.tb_frame.f_code.co_filename,
                        "lineno": tb.tb_lineno
                    })
                tb = tb.tb_next
            if BaseSetting.debug:
                print(tracebacks)
        except:
            pass

        status = 500
        message = Massage.other_massage
        if(isinstance(exception, Exception.DateException)):
            type = 'DateException'
            message = Massage.date_massage
        if(isinstance(exception, Exception.AuthException)):
            status = 401
            type = 'AuthException'
            message = Massage.auth_massage
        if(isinstance(exception, Exception.OtherException)):
            type = 'OtherException'
            message = str(exception)
        if(isinstance(exception, Exception.UploadException)):
            type = 'UploadException'
            message = Massage.upload_massage
        if(isinstance(exception, Exception.BlockIpException)):
            status = 403
            type = 'BlockIpException'
            message = Massage.block_massage
        if(isinstance(exception, Exception.ValidatorException)):
            status = 412
            type = 'ValidatorException'
            message = Massage.validator_massage
        if(isinstance(exception, Exception.PermissionException)):
            status = 403
            message = "Access denied"
            type = Massage.permission_massage
        if(isinstance(exception, Exception.DuplicateException)):
            status = 412
            type = 'DuplicateException'
            message = Massage.duplicate_massage
        if(isinstance(exception, Exception.NotFoundException)):
            status = 404
            message = "Not Found"
            type = Massage.not_found_massage

        saveException(request, type, exception_str, tracebacks, message)
        return handler(request, message, status, False)


def saveException(request, type, exception, tracebacks, message):
    data = {
        'path': '',
        'method': '',
        'user_id': 0,
        'type': type,
        'file_path': '',
        'user_agent': '',
        'line_number': 0,
        'base_url': None,
        'full_path': None,
        'message': message,
        'remote_address': '',
        'exception': exception
    }

    try:
        if len(tracebacks) > 0:
            data['file_path'] = tracebacks[len(tracebacks)-1]['filename']
            data['line_number'] = tracebacks[len(tracebacks)-1]['lineno']
    except:
        pass

    try:
        data['method'] = request.method
        data['full_path'] = request.get_full_path()
        data['base_url'] = "{0}://{1}{2}".format(
            request.scheme, request.get_host(), request.path)

        meta = request.META.copy()
        data['user_agent'] = meta.pop('HTTP_USER_AGENT', None)
        data['remote_address'] = meta.pop('REMOTE_ADDR', None)
    except:
        pass

    try:
        if hasattr(request, 'user'):
            if request.user.is_authenticated:
                data['user_id'] = request.user.id
        else:
            data['user_id'] = 0
    except:
        pass

    try:
        data['client_key'] = request.redjlog['request_id']
    except:
        pass

    try:
        helper.sendToServer(data, 'exception')
    except:
        helper.cPrint('Bad Error')
        pass


def catch(ex):
    try:
        handl = Base()
        handl.process_exception(None, ex)
    except:
        pass
