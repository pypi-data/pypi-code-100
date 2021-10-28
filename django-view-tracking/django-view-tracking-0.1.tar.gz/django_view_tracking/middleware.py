import re

from django.conf import settings
from django.urls import reverse

from .models import ViewTrack


class ViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if self.should_log_view_track(request, response):
            self.log_view_track(request, response)

        return response

    def should_log_view_track(self, request, response):
        if not getattr(settings, "DJANGO_VIEW_TRACKING_ENABLED", True):
            return False

        allow_anonymous = getattr(settings, "DJANGO_VIEW_TRACKING_ANONYMOUS_USER", True)

        blacklist = getattr(
            settings,
            "DJANGO_VIEW_TRACKING_BLACKLIST",
            [
                reverse("admin:index"),
            ],
        )

        if allow_anonymous or not request.user.is_anonymous:
            if blacklist and re.match(
                rf"({'|'.join([re.escape(_prefix) for _prefix in blacklist])})",
                request.path,
            ):
                return False

            return True

        return False

    def log_view_track(self, request, response):
        ViewTrack.objects.create(
            user=None if request.user.is_anonymous else request.user,
            request_method=request.method,
            request_url=request.get_full_path(),
            response_status_code=response.status_code,
        )
