import json
from dataclasses import dataclass

import requests
import requests_http_signature
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from fedeproxy.activitypub import ActivitypubResponse

from ..domain.activitypub import ActivityPub


def verified_signature_active():
    return True


def verified_signature_decorator(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not verified_signature_active():
            return view_func(request, *args, **kwargs)

        def key_resolver(key_id, algorithm):
            r = requests.get(key_id)
            r.raise_for_status()
            public = r.json()["publicKey"]["publicKeyPem"].encode()
            return public

        @dataclass
        class R:
            headers: dict
            url: str
            method: str

        headers = {**request.headers}
        for header in ("Date", "Digest"):
            if header in headers:
                headers[header.lower()] = headers[header]

        r = R(
            headers=headers,
            url=request.get_raw_uri(),
            method=request.method,
        )

        try:
            requests_http_signature.HTTPSignatureAuth.verify(r, key_resolver=key_resolver, scheme="Signature")

        except Exception as e:
            return HttpResponseBadRequest(f"{type(e)}{e.args}")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def verified_signature(function=None):
    if function:
        return verified_signature_decorator(function)
    return verified_signature_decorator


@csrf_exempt
@verified_signature
@require_POST
def inbox(request, username=None):

    try:
        activity_json = json.loads(request.body)
    except json.decoder.JSONDecodeError as e:
        return HttpResponseBadRequest(f"{type(e)}{e.args}")

    if "type" not in activity_json:
        return HttpResponseBadRequest(f'No "type" field in {request.body}')

    request.fedeproxy.inbox(username, ActivityPub().inbox(activity_json))

    return HttpResponse()


@require_POST
def outbox(request):
    return HttpResponse()


@require_GET
def user(request, username):
    url = f"{request.scheme}://{request.get_host()}"
    return ActivitypubResponse(ActivityPub().person_get(request.fedeproxy.base_directory, url, username))
