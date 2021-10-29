"""API views for the notices app"""
from django.conf import settings
from edx_rest_framework_extensions.auth.jwt.authentication import JwtAuthentication
from edx_rest_framework_extensions.auth.session.authentication import SessionAuthenticationAllowInactiveUser
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView


try:
    from openedx.core.lib.api.authentication import BearerAuthenticationAllowInactiveUser
except ImportError:
    BearerAuthenticationAllowInactiveUser = None

from notices.api import get_unacknowledged_notices_for_user
from notices.data import AcknowledgmentResponseTypes
from notices.models import AcknowledgedNotice, Notice
from notices.toggles import ENABLE_NOTICES


# Pulling this out so tests can ignore Bearer auth since we won't have platform importable in tests
COMMON_AUTH_CLASSES = [JwtAuthentication, SessionAuthentication, SessionAuthenticationAllowInactiveUser]
if BearerAuthenticationAllowInactiveUser is not None:
    COMMON_AUTH_CLASSES.append(BearerAuthenticationAllowInactiveUser)


class ListUnacknowledgedNotices(APIView):
    """
    Read only view to list all notices that the user hasn't acknowledged.

    If `mobile=true` is in the query text, it will append `mobile=true` to the render links.

    Path: `/notices/api/v1/unacknowledged`

    Returns:
      * 200: OK - Contains a list of active unacknowledged notices the user still needs to see
      * 401: The requesting user is not authenticated.
      * 404: This app is not installed

    Example:
    {
        "results": [
            "http://localhost:18000/notices/render/1/",
            "http://localhost:18000/notices/render/2/",
        ]
    }
    """

    authentication_classes = COMMON_AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        Return a list of all active unacknowledged notices for the user
        """
        # If feature isn't enabled for request, return empty list so the user doesn't get
        # forwarded anywhere client side
        if not ENABLE_NOTICES.is_enabled():
            return Response({"results": []}, status=HTTP_200_OK)

        in_app = request.query_params.get("mobile") == "true"
        unacknowledged_active_notices = get_unacknowledged_notices_for_user(
            request.user, in_app=in_app, request=request
        )

        return Response({"results": unacknowledged_active_notices}, status=HTTP_200_OK)


class AcknowledgeNotice(APIView):
    """
    POST-only view to acknowledge a single notice for a user

    Path: `/api/notices/v1/acknowledge`

    Returns:
      * 204: OK - Acknowledgment successfully save
      * 400: The requested notice does not exist, or the request didn't include notice data
      * 401: The requesting user is not authenticated.
      * 404: This app is not installed,

    Example request:
    POST /api/notices/v1/acknowledge
    post data: {"notice_id": 10, "acknowledgment_type": "confirmed"}
    """

    authentication_classes = COMMON_AUTH_CLASSES
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        """
        Acknowledges the notice for the requesting user
        """
        notice_id = request.data.get("notice_id")
        acknowledgment_type = request.data.get("acknowledgment_type")

        if not notice_id:
            raise ValidationError({"notice_id": "notice_id field required"})

        if not AcknowledgmentResponseTypes.includes_value(acknowledgment_type):
            valid_types = [e.value for e in AcknowledgmentResponseTypes]
            raise ValidationError(
                {"acknowledgment_type": f"acknowledgment_type must be one of the following: {valid_types}"}
            )

        try:
            notice = Notice.objects.get(id=notice_id, active=True)
        except Notice.DoesNotExist as exc:
            raise ValidationError({"notice_id": "notice_id field does not match an existing active notice"}) from exc

        (acknowledged_notice, _) = AcknowledgedNotice.objects.update_or_create(
            user=request.user, notice=notice, defaults={"response_type": acknowledgment_type}
        )
        snooze_limit = settings.FEATURES.get("NOTICES_SNOOZE_COUNT_LIMIT")
        if snooze_limit is not None and acknowledgment_type == AcknowledgmentResponseTypes.DISMISSED:
            acknowledged_notice.snooze_count = acknowledged_notice.snooze_count + 1
            acknowledged_notice.save()

        # Since this is just an acknowledgment API, we can just return a 204 without any response data.
        return Response(status=HTTP_204_NO_CONTENT)
