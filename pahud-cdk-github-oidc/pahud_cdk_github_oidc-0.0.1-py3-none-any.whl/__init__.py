'''
[![npm version](https://badge.fury.io/js/@pahud%2Fcdk-github-oidc.svg)](https://badge.fury.io/js/@pahud%2Fcdk-github-oidc)
[![PyPI version](https://badge.fury.io/py/pahud-cdk-github-oidc.svg)](https://badge.fury.io/py/pahud-cdk-github-oidc)
[![release](https://github.com/pahud/cdk-github-oidc/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdk-github-oidc/actions/workflows/release.yml)

# cdk-github-oidc

Inspired by [aripalo/aws-cdk-github-oidc](https://github.com/aripalo/aws-cdk-github-oidc), this repository allows you to create a `Github OpenID Connect Identity Provider` with the `OpenIdConnectProvider` CDK construct and generate federated IAM roles from this provider used in one or multiple Github repositories.

# Sample

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from cdk_github_oidc import OpenIdConnectProvider

# create the provider
provider = OpenIdConnectProvider(stack, "GithubOpenIdConnectProvider")
# create an IAM role from this provider
provider.create_role("demo-role", [owner="pahud", repo="gitpod-workspace", owner="pahud", repo="github-codespace", owner="pahud", repo="vscode"
])
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_iam
import aws_cdk.core


class OpenIdConnectProvider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pahud/cdk-github-oidc.OpenIdConnectProvider",
):
    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="createRole")
    def create_role(
        self,
        id: builtins.str,
        repo: typing.Sequence["RepositoryConfig"],
        *,
        assumed_by: aws_cdk.aws_iam.IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> aws_cdk.aws_iam.Role:
        '''
        :param id: -
        :param repo: -
        :param assumed_by: The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.
        '''
        role_props = aws_cdk.aws_iam.RoleProps(
            assumed_by=assumed_by,
            description=description,
            external_id=external_id,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        return typing.cast(aws_cdk.aws_iam.Role, jsii.invoke(self, "createRole", [id, repo, role_props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="issuer")
    def ISSUER(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "issuer"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="thumbprint")
    def THUMBPRINT(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "thumbprint"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="provider")
    def provider(self) -> aws_cdk.aws_iam.IOpenIdConnectProvider:
        return typing.cast(aws_cdk.aws_iam.IOpenIdConnectProvider, jsii.get(self, "provider"))


@jsii.data_type(
    jsii_type="@pahud/cdk-github-oidc.RepositoryConfig",
    jsii_struct_bases=[],
    name_mapping={"owner": "owner", "repo": "repo", "filter": "filter"},
)
class RepositoryConfig:
    def __init__(
        self,
        *,
        owner: builtins.str,
        repo: builtins.str,
        filter: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param owner: 
        :param repo: 
        :param filter: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "owner": owner,
            "repo": repo,
        }
        if filter is not None:
            self._values["filter"] = filter

    @builtins.property
    def owner(self) -> builtins.str:
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo(self) -> builtins.str:
        result = self._values.get("repo")
        assert result is not None, "Required property 'repo' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "OpenIdConnectProvider",
    "RepositoryConfig",
]

publication.publish()
