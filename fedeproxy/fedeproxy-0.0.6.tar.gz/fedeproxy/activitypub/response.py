from django.http import JsonResponse

from .base_activity import ActivityEncoder


class ActivitypubResponse(JsonResponse):
    def __init__(self, data, encoder=ActivityEncoder, safe=False, json_dumps_params=None, **kwargs):

        if "content_type" not in kwargs:
            kwargs["content_type"] = "application/activity+json"

        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)
