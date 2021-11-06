import time
from .. import helper
from django.utils.deprecation import MiddlewareMixin
from redjlog.management.setting import Base as BaseSetting


class Base(MiddlewareMixin):
    def __call__(self, request):
        start_time = time.time()
        request_id = self.saveRequest(request)
        request.redjlog = {"request_id": request_id}

        response = self.get_response(request)

        exec_time = int((time.time() - start_time)*1000)
        self.updateRequest(response, request, exec_time, request_id)
        return response

    def saveRequest(self, request):
        request_id = helper.randomString()
        data = {
            'ip': None,
            'user_id': 0,
            'method': None,
            'is_ajax': None,
            'base_url': None,
            'full_path': None,
            'user_agent': None,
            'body_request': None,
            'remote_address': None,
            'client_key': request_id
        }

        try:
            data['method'] = request.method
            data['is_ajax'] = request.is_ajax()
            data['full_path'] = request.get_full_path()
            data['base_url'] = "{0}://{1}{2}".format(
                request.scheme,
                request.get_host(),
                request.path
            )

            meta = request.META.copy()
            data['user_agent'] = meta.pop('HTTP_USER_AGENT', None)
            data['remote_address'] = meta.pop('REMOTE_ADDR', None)
        except:
            pass

        try:
            data['ip'] = self.getClientIP(request)
        except:
            pass

        try:
            data['body_request'] = str(request.body)
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
            helper.sendToServer(data, 'request')
        except:
            pass

        return request_id

    def updateRequest(self, response, request, exec_time, request_id):
        data = {
            'user_id': 0,
            'response_code': 0,
            'body_response': None,
            'exec_time': exec_time,
            'client_key': request_id,
        }

        try:
            if BaseSetting.save_body_response:
                data['body_response'] = str(response.content)
        except:
            pass

        try:
            if BaseSetting.save_body_response_exception and response.status_code != 200:
                data['body_response'] = str(response.content)
        except:
            pass

        try:
            data['response_code'] = response.status_code
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
            # send request
            helper.sendToServer(data, 'request_update')
            pass
        except:
            pass

    def getClientIP(self, request):
        client_ip = ''
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                client_ip = x_forwarded_for.split(',')[0]
            else:
                client_ip = request.META.get('REMOTE_ADDR')
        except:
            pass
        return client_ip
