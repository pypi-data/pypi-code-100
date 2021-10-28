"""
Rendered views for the notices app.
"""

import logging
from urllib.parse import unquote, urlsplit

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import get_language_from_request
from django.views.generic import DetailView

from notices.api import can_dismiss
from notices.models import Notice


logger = logging.getLogger(__name__)


class RenderNotice(LoginRequiredMixin, DetailView):
    """Notice rendering view."""

    # This base template will include a separate template housing the requested credential body.
    # This allows us to use this one view to render credentials for any number of content types
    # (e.g., courses, programs).
    template_name = "notice.html"
    model = Notice

    def get_context_data(self, **kwargs):
        """
        Add the context for the rendering templates.
        """
        context = super().get_context_data(**kwargs)
        user_language = get_language_from_request(self.request)
        try:
            translated_notice = self.object.translated_notice_content.get(language_code=user_language)
        except ObjectDoesNotExist:
            fallback_language = settings.FEATURES["NOTICES_FALLBACK_LANGUAGE"]
            translated_notice = self.object.translated_notice_content.get(language_code=fallback_language)
        body_content = translated_notice.html_content
        forwarding_url = unquote(self.request.GET.get("next", ""))
        (_, forwarding_url_domain, _, _, _) = urlsplit(forwarding_url)
        if forwarding_url_domain not in settings.FEATURES["NOTICES_REDIRECT_ALLOWLIST"]:
            forwarding_url = settings.FEATURES["NOTICES_DEFAULT_REDIRECT_URL"]

        in_app = self.request.GET.get("mobile") == "true"
        context.update(
            {
                "head_content": self.object.head_content,
                "html_content": body_content,
                "forwarding_url": forwarding_url,
                "notice_id": self.object.id,
                "in_app": in_app,
                "can_dismiss": can_dismiss(self.request.user, self.object),
                "NOTICES_SEGMENT_KEY": settings.FEATURES["NOTICES_SEGMENT_KEY"],
            }
        )
        return context
