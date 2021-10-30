import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def hook(request, **kwargs):
    try:
        payload = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        return HttpResponseBadRequest(f"{type(e)}{e.args}")

    request.fedeproxy.hook_receive(payload, **kwargs)

    return HttpResponse()
