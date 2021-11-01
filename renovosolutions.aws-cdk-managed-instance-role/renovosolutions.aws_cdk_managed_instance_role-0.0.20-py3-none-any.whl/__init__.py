'''
# cdk-library-managed-instance-role

This CDK Construct Library includes a construct (`ManagedInstanceRole`) which creates an AWS instance profile. By default this instance profile includes the basic policies required for instance management in SSM and the ability to Domain Join the instance.

The purpose of this CDK Construct Library is to ease the creation of instance roles by not needing to code the inclusion of baseline management roles for evey single different role implementation every time. Instance profiles only support a single role so its important the role includes all required access. This construct allows making additions to those baseline policies with ease.

The construct defines an interface (`IManagedInstanceRoleProps`) to configure the managed policies of the role as well as manage the inclusion of the default roles.

## Dev

### Pre-reqs:

You will need

* npm installed on your machine
* AWS CDK installed on your machine
* python installed on your machine
* dotnet installed on your machine
* a github account

This project is managed with `projen`. Modify the `.projenrc.js` file and run `npx projen`. You can also modify this `README` file and the `src` code directory as needed. Github actions take care of publishing utilizing the automatically created workflows from `projen`.
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


@jsii.interface(
    jsii_type="@renovosolutions/cdk-library-managed-instance-role.IManagedInstanceRoleProps"
)
class IManagedInstanceRoleProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainJoinEnabled")
    def domain_join_enabled(self) -> typing.Optional[builtins.bool]:
        '''Should the role include directory service access with SSM.'''
        ...

    @domain_join_enabled.setter
    def domain_join_enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managedPolicies")
    def managed_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.ManagedPolicy]]:
        '''The managed policies to apply to the role in addition to the default policies.'''
        ...

    @managed_policies.setter
    def managed_policies(
        self,
        value: typing.Optional[typing.List[aws_cdk.aws_iam.ManagedPolicy]],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ssmManagementEnabled")
    def ssm_management_enabled(self) -> typing.Optional[builtins.bool]:
        '''Should the role include SSM management.

        By default if domainJoinEnabled is true then this role is always included.
        '''
        ...

    @ssm_management_enabled.setter
    def ssm_management_enabled(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IManagedInstanceRolePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-managed-instance-role.IManagedInstanceRoleProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="domainJoinEnabled")
    def domain_join_enabled(self) -> typing.Optional[builtins.bool]:
        '''Should the role include directory service access with SSM.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "domainJoinEnabled"))

    @domain_join_enabled.setter
    def domain_join_enabled(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "domainJoinEnabled", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="managedPolicies")
    def managed_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.ManagedPolicy]]:
        '''The managed policies to apply to the role in addition to the default policies.'''
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.ManagedPolicy]], jsii.get(self, "managedPolicies"))

    @managed_policies.setter
    def managed_policies(
        self,
        value: typing.Optional[typing.List[aws_cdk.aws_iam.ManagedPolicy]],
    ) -> None:
        jsii.set(self, "managedPolicies", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ssmManagementEnabled")
    def ssm_management_enabled(self) -> typing.Optional[builtins.bool]:
        '''Should the role include SSM management.

        By default if domainJoinEnabled is true then this role is always included.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "ssmManagementEnabled"))

    @ssm_management_enabled.setter
    def ssm_management_enabled(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "ssmManagementEnabled", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedInstanceRoleProps).__jsii_proxy_class__ = lambda : _IManagedInstanceRolePropsProxy


class ManagedInstanceRole(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-managed-instance-role.ManagedInstanceRole",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IManagedInstanceRoleProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceProfile")
    def instance_profile(self) -> aws_cdk.aws_iam.CfnInstanceProfile:
        return typing.cast(aws_cdk.aws_iam.CfnInstanceProfile, jsii.get(self, "instanceProfile"))


__all__ = [
    "IManagedInstanceRoleProps",
    "ManagedInstanceRole",
]

publication.publish()
