from django.conf import settings
from health_check.backends import BaseHealthCheckBackend


class VersionBackend(BaseHealthCheckBackend):
    #: The status endpoints will respond with a 200 status code
    #: even if the check errors.
    critical_service = False

    def check_status(self):
        pass

    def identifier(self):
        return self.__class__.__name__  # Display name on the endpoint.

    def pretty_status(self):
        # return the string stored in the settings.py VERSION
        return settings.VERSION
