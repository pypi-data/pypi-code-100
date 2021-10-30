import time
import logging
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout

from .utils import get_ip
from .configs import app_configs
from .permissions import is_suspended

logger = logging.getLogger(app_configs.LOGGER_NAME)


class Benchmark:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        start = time.time()
        response = self.get_response(request)
        # Elapsed time.
        delta = int((time.time() - start) * 1000)
        msg = f"time={delta}ms for path={request.path}"
        if delta > 1000:
            ip = get_ip(request)
            uid = request.user.profile.uid if request.user.is_authenticated else "0"
            # agent = request.META.get('HTTP_USER_AGENT', None)
            logger.warning(f"SLOW: {msg} IP:{ip} uid:{uid}")
        elif settings.DEBUG:
            logger.info(f"{msg}")

        return response


class UserStats:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        # Views for anonymous users are not analzed further.
        if user.is_anonymous:
            return self.get_response(request)

        # Banned and suspended will be logged out.
        if is_suspended(user=user):
            messages.error(request, f"Account is {user.profile.get_state_display()}")
            logout(request)

        response = self.get_response(request)

        return response
