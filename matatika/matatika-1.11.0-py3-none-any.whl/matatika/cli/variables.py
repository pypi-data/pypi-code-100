# pylint: disable=too-few-public-methods

"""variables module"""

from enum import Enum
import os
from matatika.exceptions import NoDefaultContextSetError
from matatika.context import MatatikaContext


class VariableType(Enum):
    """Possible variable types"""
    AUTH_TOKEN = "auth_token"
    CLIENT_ID = "client_id"
    CLIENT_SECRET = "client_secret"
    ENDPOINT_URL = "endpoint_url"
    WORKSPACE_ID = "workspace_id"

    def label(self):
        """Format as a CLI label"""
        return self.name.replace('_', ' ')  # pylint: disable=no-member


class VariableSource(Enum):
    """Possible variable sources"""
    COMMAND = "command"
    ENV = "env"
    CONTEXT = "context"
    DEFAULT = "default"


class BaseVariable():
    """Handles resolution of variable values"""

    def __init__(self, variable_type: VariableType):
        self.name = variable_type.name
        self.default = None

    def _from_command(self, ctx) -> str:
        return ctx.obj.get(self.name.lower())

    def _from_env(self) -> str:
        return os.getenv(self.name)

    def _from_context(self) -> str:
        try:
            context = MatatikaContext().get_default_context()[1]
            return context.get(self.name.lower())

        except NoDefaultContextSetError:
            return None

    def get(self, ctx):
        """Returns a value and source for the variable from the command, system environment, or
        context file"""
        value = self._from_command(ctx)
        if value:
            return value, VariableSource.COMMAND

        value = self._from_env()
        if value:
            return value, VariableSource.ENV

        value = self._from_context()
        if value:
            return value, VariableSource.CONTEXT

        return self.default, VariableSource.DEFAULT if self.default else None


class AuthTokenVariable(BaseVariable):
    """Auth token variable"""

    def __init__(self):
        super().__init__(VariableType.AUTH_TOKEN)


class ClientIdVariable(BaseVariable):
    """Client ID variable"""

    def __init__(self):
        super().__init__(VariableType.CLIENT_ID)


class ClientSecretVariable(BaseVariable):
    """Client secret variable"""

    def __init__(self):
        super().__init__(VariableType.CLIENT_SECRET)


class EndpointUrlVariable(BaseVariable):
    """Endpoint URL variable"""

    def __init__(self):
        super().__init__(VariableType.ENDPOINT_URL)
        self.default = "https://catalog.matatika.com/api"


class WorkspaceIdVariable(BaseVariable):
    """Workspace ID variable"""

    def __init__(self):
        super().__init__(VariableType.WORKSPACE_ID)
