from django.http import JsonResponse
from django.views.decorators.http import require_GET

from fedeproxy.version import __version__


@require_GET
def nodeinfo_pointer(request):
    return JsonResponse(
        {
            "links": [
                {
                    "rel": "http://nodeinfo.diaspora.software/ns/schema/2.0",
                    "href": request.build_absolute_uri("/nodeinfo/2.0"),
                }
            ]
        }
    )


@require_GET
def nodeinfo(_):
    return JsonResponse(
        {
            "version": "2.0",
            "software": {"name": "fedeproxy", "version": __version__},
            "protocols": ["activitypub"],
            "openRegistrations": False,
        }
    )
