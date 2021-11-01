'''
# cdk-renovo-instance-service
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

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.core
import managed_instance_role


@jsii.interface(
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.IAmiLookup"
)
class IAmiLookup(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name string to use for AMI lookup.'''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="owners")
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The owners to use for AMI lookup.'''
        ...

    @owners.setter
    def owners(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="windows")
    def windows(self) -> typing.Optional[builtins.bool]:
        '''Is this AMI expected to be windows?'''
        ...

    @windows.setter
    def windows(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IAmiLookupProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-renovo-instance-service.IAmiLookup"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name string to use for AMI lookup.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="owners")
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The owners to use for AMI lookup.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "owners"))

    @owners.setter
    def owners(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "owners", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="windows")
    def windows(self) -> typing.Optional[builtins.bool]:
        '''Is this AMI expected to be windows?'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "windows"))

    @windows.setter
    def windows(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "windows", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAmiLookup).__jsii_proxy_class__ = lambda : _IAmiLookupProxy


@jsii.interface(
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.IInstanceServiceProps"
)
class IInstanceServiceProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ami")
    def ami(self) -> aws_cdk.aws_ec2.IMachineImage:
        '''The Amazon Machine Image (AMI) to launch the target instance with.'''
        ...

    @ami.setter
    def ami(self, value: aws_cdk.aws_ec2.IMachineImage) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the service this instance service will host.'''
        ...

    @name.setter
    def name(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''The VPC to launch this service in.'''
        ...

    @vpc.setter
    def vpc(self, value: aws_cdk.aws_ec2.Vpc) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowAllOutbound")
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Allow all outbound traffic for the instances security group.

        :default: true
        '''
        ...

    @allow_all_outbound.setter
    def allow_all_outbound(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disableInlineRules")
    def disable_inline_rules(self) -> typing.Optional[builtins.bool]:
        '''Whether to disable inline ingress and egress rule optimization for the instances security group.

        If this is set to true, ingress and egress rules will not be declared under the SecurityGroup in cloudformation, but will be separate elements.

        Inlining rules is an optimization for producing smaller stack templates.
        Sometimes this is not desirable, for example when security group access is managed via tags.

        The default value can be overriden globally by setting the context variable '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'.

        :default: false
        '''
        ...

    @disable_inline_rules.setter
    def disable_inline_rules(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableCloudwatchLogs")
    def enable_cloudwatch_logs(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable logging to Cloudwatch Logs.

        :default: true
        '''
        ...

    @enable_cloudwatch_logs.setter
    def enable_cloudwatch_logs(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledNoPublicIngressAspect")
    def enabled_no_public_ingress_aspect(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to prevent security group from containing rules that allow access from the public internet: Any rule with a source from 0.0.0.0/0 or ::/0.

        If these sources are used when this is enabled and error will be added to CDK metadata and deployment and synth will fail.
        '''
        ...

    @enabled_no_public_ingress_aspect.setter
    def enabled_no_public_ingress_aspect(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableNoDBPortsAspect")
    def enable_no_db_ports_aspect(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to prevent security group from containing rules that allow access to relational DB ports: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server.

        If these ports are opened when this is enabled an error will be added to CDK metadata and deployment and synth will fail.

        :default: true
        '''
        ...

    @enable_no_db_ports_aspect.setter
    def enable_no_db_ports_aspect(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableNoRemoteManagementPortsAspect")
    def enable_no_remote_management_ports_aspect(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''Whether or not to prevent security group from containing rules that allow access to remote management ports: SSH, RDP, WinRM, WinRM over HTTPs.

        If these ports are opened when this is enabled an error will be added to CDK metadata and deployment and synth will fail.

        :default: true
        '''
        ...

    @enable_no_remote_management_ports_aspect.setter
    def enable_no_remote_management_ports_aspect(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetType]:
        '''The subnet type to launch this service in.

        :default: ec2.SubnetType.PRIVATE
        '''
        ...

    @subnet_type.setter
    def subnet_type(self, value: typing.Optional[aws_cdk.aws_ec2.SubnetType]) -> None:
        ...


class _IInstanceServicePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-renovo-instance-service.IInstanceServiceProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ami")
    def ami(self) -> aws_cdk.aws_ec2.IMachineImage:
        '''The Amazon Machine Image (AMI) to launch the target instance with.'''
        return typing.cast(aws_cdk.aws_ec2.IMachineImage, jsii.get(self, "ami"))

    @ami.setter
    def ami(self, value: aws_cdk.aws_ec2.IMachineImage) -> None:
        jsii.set(self, "ami", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the service this instance service will host.'''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.Vpc:
        '''The VPC to launch this service in.'''
        return typing.cast(aws_cdk.aws_ec2.Vpc, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: aws_cdk.aws_ec2.Vpc) -> None:
        jsii.set(self, "vpc", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="allowAllOutbound")
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Allow all outbound traffic for the instances security group.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "allowAllOutbound"))

    @allow_all_outbound.setter
    def allow_all_outbound(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "allowAllOutbound", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="disableInlineRules")
    def disable_inline_rules(self) -> typing.Optional[builtins.bool]:
        '''Whether to disable inline ingress and egress rule optimization for the instances security group.

        If this is set to true, ingress and egress rules will not be declared under the SecurityGroup in cloudformation, but will be separate elements.

        Inlining rules is an optimization for producing smaller stack templates.
        Sometimes this is not desirable, for example when security group access is managed via tags.

        The default value can be overriden globally by setting the context variable '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'.

        :default: false
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "disableInlineRules"))

    @disable_inline_rules.setter
    def disable_inline_rules(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "disableInlineRules", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableCloudwatchLogs")
    def enable_cloudwatch_logs(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable logging to Cloudwatch Logs.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableCloudwatchLogs"))

    @enable_cloudwatch_logs.setter
    def enable_cloudwatch_logs(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "enableCloudwatchLogs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enabledNoPublicIngressAspect")
    def enabled_no_public_ingress_aspect(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to prevent security group from containing rules that allow access from the public internet: Any rule with a source from 0.0.0.0/0 or ::/0.

        If these sources are used when this is enabled and error will be added to CDK metadata and deployment and synth will fail.
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabledNoPublicIngressAspect"))

    @enabled_no_public_ingress_aspect.setter
    def enabled_no_public_ingress_aspect(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        jsii.set(self, "enabledNoPublicIngressAspect", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableNoDBPortsAspect")
    def enable_no_db_ports_aspect(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to prevent security group from containing rules that allow access to relational DB ports: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server.

        If these ports are opened when this is enabled an error will be added to CDK metadata and deployment and synth will fail.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableNoDBPortsAspect"))

    @enable_no_db_ports_aspect.setter
    def enable_no_db_ports_aspect(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "enableNoDBPortsAspect", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="enableNoRemoteManagementPortsAspect")
    def enable_no_remote_management_ports_aspect(
        self,
    ) -> typing.Optional[builtins.bool]:
        '''Whether or not to prevent security group from containing rules that allow access to remote management ports: SSH, RDP, WinRM, WinRM over HTTPs.

        If these ports are opened when this is enabled an error will be added to CDK metadata and deployment and synth will fail.

        :default: true
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableNoRemoteManagementPortsAspect"))

    @enable_no_remote_management_ports_aspect.setter
    def enable_no_remote_management_ports_aspect(
        self,
        value: typing.Optional[builtins.bool],
    ) -> None:
        jsii.set(self, "enableNoRemoteManagementPortsAspect", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="subnetType")
    def subnet_type(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetType]:
        '''The subnet type to launch this service in.

        :default: ec2.SubnetType.PRIVATE
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetType], jsii.get(self, "subnetType"))

    @subnet_type.setter
    def subnet_type(self, value: typing.Optional[aws_cdk.aws_ec2.SubnetType]) -> None:
        jsii.set(self, "subnetType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInstanceServiceProps).__jsii_proxy_class__ = lambda : _IInstanceServicePropsProxy


@jsii.interface(
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.IManagedLoggingPolicyProps"
)
class IManagedLoggingPolicyProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        '''The OS of the instance this policy is for.'''
        ...

    @os.setter
    def os(self, value: builtins.str) -> None:
        ...


class _IManagedLoggingPolicyPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-renovo-instance-service.IManagedLoggingPolicyProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        '''The OS of the instance this policy is for.'''
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        jsii.set(self, "os", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedLoggingPolicyProps).__jsii_proxy_class__ = lambda : _IManagedLoggingPolicyPropsProxy


class InstanceService(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.InstanceService",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IInstanceServiceProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="instanceProfile")
    def instance_profile(self) -> managed_instance_role.ManagedInstanceRole:
        return typing.cast(managed_instance_role.ManagedInstanceRole, jsii.get(self, "instanceProfile"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> aws_cdk.aws_ec2.SecurityGroup:
        return typing.cast(aws_cdk.aws_ec2.SecurityGroup, jsii.get(self, "securityGroup"))


class ManagedLoggingPolicy(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-renovo-instance-service.ManagedLoggingPolicy",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IManagedLoggingPolicyProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="policy")
    def policy(self) -> aws_cdk.aws_iam.ManagedPolicy:
        return typing.cast(aws_cdk.aws_iam.ManagedPolicy, jsii.get(self, "policy"))


__all__ = [
    "IAmiLookup",
    "IInstanceServiceProps",
    "IManagedLoggingPolicyProps",
    "InstanceService",
    "ManagedLoggingPolicy",
]

publication.publish()
