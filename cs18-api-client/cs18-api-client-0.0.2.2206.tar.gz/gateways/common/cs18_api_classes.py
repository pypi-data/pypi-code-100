"""
Container for object classes used in cs18-api-client
"""
import abc
import uuid
from typing import List
import dateutil.parser

import json


class AccessLink:
    def __init__(self, protocol: str, link: str):
        self.link = link
        self.protocol = protocol


class Commit:
    def __init__(self, data: dict):
        self.sha = data["sha"]
        self.author = data["commit"]["author"]["name"]
        self.date = dateutil.parser.parse(data["commit"]["author"]["date"])
        self.comment = data["commit"]["message"]

    def __str__(self):
        return "{0}: [{1}] {2}".format(self.date, self.sha[:7], self.comment)


class ColonyAccount:
    def __init__(
            self, account: str, email: str, password: str, first_name: str, last_name: str
    ):
        self.account = account
        self.default_space = "Trial"
        self.sample_space = "Sample"
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name


class BlueprintRepositoryDetails:
    def __init__(self, repository_url: str, access_token: str, repository_type: str, branch: str = None):
        self.repository_url = repository_url
        self.repository_type = repository_type
        self.access_token = access_token
        self.branch = branch


class BitbucketBlueprintRepositoryDetails:
    def __init__(self, auth_code: str, redirect_url: str, blueprint_repository_details: BlueprintRepositoryDetails):
        self.blueprint_repository_details = blueprint_repository_details
        self.auth_code = auth_code
        self.redirect_url = redirect_url


class AddAccountBlueprintRepositoryRequest(abc.ABC):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool):
        self.name = name
        self.repository_url = repository_url
        self.open_access = open_access
        self.allow_sharing = allow_sharing


class AddBlueprintUsingTokenRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, access_token: str, repository_type: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.repository_type = repository_type
        self.access_token = access_token


class AddBlueprintGithubRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, state: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.state = state


class AddBlueprintBitbucketRepositoryRequest(AddAccountBlueprintRepositoryRequest):
    def __init__(self, name: str, repository_url: str, allow_sharing: bool,
                 open_access: bool, code: str, redirection_url: str):
        super().__init__(name, repository_url, allow_sharing, open_access)
        self.code = code
        self.redirection_url = redirection_url


class TerraformModuleInput(abc.ABC):
    def __init__(self, name: str = "name", value: str = "value", description: str = "description",
                 optional: bool = True,
                 overridable: bool = True, display_style: str = "normal"):
        self.display_style = display_style
        self.overridable = overridable
        self.optional = optional
        self.description = description
        self.value = value
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleInput):
            return NotImplemented

        return self.display_style == other.display_style and \
               self.overridable == other.overridable and \
               self.optional == other.optional and \
               self.description == other.description and \
               self.value == other.value and \
               self.name == other.name


class TerraformModuleOutput(abc.ABC):
    def __init__(self, name: str = "name", display_style: str = "normal", description: str = "description"):
        self.description = description
        self.display_style = display_style
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleInput):
            return NotImplemented

        return self.display_style == other.display_style and \
               self.description == other.description and \
               self.name == other.name


class TerraformModuleComputeService(abc.ABC):
    def __init__(self, cloud_account_name: str, compute_service_name: str, permissions: dict):
        self.cloud_account_name = cloud_account_name
        self.compute_service_name = compute_service_name
        self.permissions = permissions

    def init_compute_service(self, cloud_permissions_type: str):
        if cloud_permissions_type == "aws":
            self.permissions = {
                "role_arn": "role_arn",
                "external_id": "external_id"
            }
        else:
            self.permissions = {
                "managed_identity_id": "managed_identity_id"
            }

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleComputeService):
            return NotImplemented

        return self.cloud_account_name == other.cloud_account_name and \
               self.compute_service_name == other.compute_service_name and \
               self.permissions == other.permissions


def __get_guid__():
    return str(uuid.uuid4()).replace("-", "")[0:13]


class TerraformModuleDescriptor:
    def __init__(self, module_name: str = None, module_repo_name: str = None, module_root_path: str = None,
                 description: str = "description", terraform_version: str = "version",
                 enable_auto_tagging: bool = True, exclude_from_tagging: List[str] = None,
                 inputs: List[TerraformModuleInput] = None, outputs: List[TerraformModuleOutput] = None,
                 compute_services: List[TerraformModuleComputeService] = None, allowed_spaces: List[str] = None):
        self.name = module_name if module_name is not None else "module_name_test_" + __get_guid__()
        self.module_repo_name = module_repo_name
        self.module_root_path = module_root_path
        self.description = description
        self.terraform_version = terraform_version
        self.enable_auto_tagging = enable_auto_tagging
        self.exclude_from_tagging = exclude_from_tagging \
            if exclude_from_tagging is not None else ["exclude_from_tagging"]
        self.allowed_spaces = allowed_spaces if allowed_spaces is not None else ["Trial"]
        self.compute_services = compute_services if compute_services is not None else []
        self.outputs = outputs if outputs is not None else []
        self.inputs = inputs if inputs is not None else []

    def __eq__(self, other):
        if not isinstance(other, TerraformModuleDescriptor):
            return NotImplemented

        name = self.name == other.name
        module_repo_name = self.module_repo_name == other.module_repo_name
        module_root_path = self.module_root_path == other.module_root_path
        description = self.description == other.description
        terraform_version = self.terraform_version == other.terraform_version
        enable_auto_tagging = self.enable_auto_tagging == other.enable_auto_tagging
        exclude_from_tagging = self.exclude_from_tagging == other.exclude_from_tagging
        allowed_spaces = self.allowed_spaces == other.allowed_spaces
        compute_services = self.compute_services == other.compute_services
        outputs = self.outputs == other.outputs
        inputs = self.inputs == other.inputs

        return name and module_repo_name and module_root_path and description and terraform_version and \
               enable_auto_tagging and exclude_from_tagging and allowed_spaces and compute_services and \
               outputs and inputs
