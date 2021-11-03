"""exceptions module"""

from dataclasses import dataclass


class MatatikaException(Exception):
    """Class to handle custom Matatika exceptions"""

    def __init__(self, message=None):

        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class NoDefaultContextSetError(MatatikaException):
    """Error to raise when no default context is set"""

    def __str__(self):

        return "No default context is set\n" \
            "Set one using 'matatika context use' " \
            "(see 'matatika context use --help')"


@dataclass
class ContextExistsError(MatatikaException):
    """Error to raise when a context exists"""

    name: str

    def __str__(self):
        return f"Context '{self.name}' already exists"


@dataclass
class ContextDoesNotExistError(MatatikaException):
    """Error to raise when a context does not exists"""

    name: str

    def __str__(self):
        return f"Context '{self.name}' does not exist"


@dataclass
class VariableNotSetError(MatatikaException):
    """Error to raise when a variable is not set in the default context"""

    name: str

    def __post_init__(self):
        command_option = self.name.lower().replace('_', '-')

        self.set_command_help = f"--{command_option}"
        self.set_env_help = f"export {self.name}=$VALUE"
        self.set_context_help = f"matatika context update --{command_option} ${self.name}"

    def __str__(self):
        return f"Variable '{self.name}' is not set\n" \
            f"Use '{self.set_command_help}' to provide a one-time command override\n" \
            f"Use '{self.set_env_help}' to set the variable in the system environment\n" \
            f"Use '{self.set_context_help}' to set the variable in the default context"


class ResourceNotFoundError(MatatikaException):
    """Class to raise an exception when a resource is not found"""

    def __init__(self, resource_type: str, resource_id, endpoint_url):

        super().__init__()
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.endpoint_url = endpoint_url

    def __str__(self):
        return f"{self.resource_type.title()} {self.resource_id} does not exist within the " \
            f"current authorisation context: {self.endpoint_url}"


class WorkspaceNotFoundError(ResourceNotFoundError):
    """Class to raise an exception when a workspace is not found"""

    def __init__(self, workspace_id, endpoint_url):

        super().__init__('workspace', workspace_id, endpoint_url)


class DatasetNotFoundError(ResourceNotFoundError):
    """Class to raise an exception when a dataset is not found"""

    def __init__(self, dataset_id, endpoint_url):

        super().__init__('dataset', dataset_id, endpoint_url)

class ChannelExistsError(MatatikaException):
    """Class to raise an exception when a dataset is not found"""

    def __init__(self, message):

        super().__init__(message)
