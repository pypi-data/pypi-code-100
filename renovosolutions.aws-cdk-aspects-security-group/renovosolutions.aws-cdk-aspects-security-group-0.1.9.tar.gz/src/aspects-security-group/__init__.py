'''
# cdk-aspects-library-security-group

A CDK library containing EC2 security group related [CDK Aspects](https://docs.aws.amazon.com/cdk/latest/guide/aspects.html) and the ability to define custom aspects.

## Features

* Utilize built in aspects for common cases:

  * Disallow public access to any port
  * Disallow public access to AWS Restricted Common ports ([per the AWS Config rule](https://docs.aws.amazon.com/config/latest/developerguide/restricted-common-ports.html))
  * Disallow public access to SSH or RDP per CIS Benchmark guidelines and general good practice
  * Disallow public or ALL access to common management ports like SSH, RDP, WinRM, WinRM over HTTPS
  * Disallow public or ALL access common relational DB ports like MSSQL, MySQL, PostgreSQL, and Oracle
  * Disallow public or ALL common web ports like HTTP (80, 8080) and HTTPS (443, 8443)
* Create any other aspect using the base security group aspect class.
* By default aspects generate errors in the CDK metadata which the deployment or synth process will find, but this can be changed with the `annotationType` property
* All default provided aspects restrict based on the public access CIDRs (`0.0.0.0/0` and `::/0`) but you can also defined aspects with any set of restricted CIDRs or security group IDs you like

## API Doc

See [API](API.md)

## Examples

### Typescript

```
// Add an existing aspect to your stack
Aspects.of(stack).add(new NoPublicIngressAspect());

// Add a custom aspect to your stack
Aspects.of(stack).add(new SecurityGroupAspectBase({
  annotationText: 'This is a custom message warning you how you should not do what you are doing.',
  annotationType: AnnotationType.WARNING,
  ports: [5985],
  restrictedCidrs: ['10.1.0.0/16'],
}));

// Change an existing aspects message and type
Aspects.of(stack).add(new NoPublicIngressAspect(
  annotationText: 'This is custom text.',
  annotationType: AnnotationType.WARNING
));
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

import aws_cdk.core


@jsii.enum(
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.AnnotationType"
)
class AnnotationType(enum.Enum):
    '''The supported annotation types.

    Only error will stop deployment of restricted resources.
    '''

    WARNING = "WARNING"
    ERROR = "ERROR"
    INFO = "INFO"


@jsii.interface(
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.IAspectPropsBase"
)
class IAspectPropsBase(typing_extensions.Protocol):
    '''The base aspect properties available to any aspect.

    JSII doesn't support an Omit when extending interfaces, so we create a base class to extend from.
    This base class meets the needed properties for all non-base aspects.
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="annotationText")
    def annotation_text(self) -> typing.Optional[builtins.str]:
        '''The annotation text to use for the annotation.'''
        ...

    @annotation_text.setter
    def annotation_text(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="annotationType")
    def annotation_type(self) -> typing.Optional[AnnotationType]:
        '''The annotation type to use for the annotation.'''
        ...

    @annotation_type.setter
    def annotation_type(self, value: typing.Optional[AnnotationType]) -> None:
        ...


class _IAspectPropsBaseProxy:
    '''The base aspect properties available to any aspect.

    JSII doesn't support an Omit when extending interfaces, so we create a base class to extend from.
    This base class meets the needed properties for all non-base aspects.
    '''

    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-aspects-library-security-group.IAspectPropsBase"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="annotationText")
    def annotation_text(self) -> typing.Optional[builtins.str]:
        '''The annotation text to use for the annotation.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotationText"))

    @annotation_text.setter
    def annotation_text(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "annotationText", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="annotationType")
    def annotation_type(self) -> typing.Optional[AnnotationType]:
        '''The annotation type to use for the annotation.'''
        return typing.cast(typing.Optional[AnnotationType], jsii.get(self, "annotationType"))

    @annotation_type.setter
    def annotation_type(self, value: typing.Optional[AnnotationType]) -> None:
        jsii.set(self, "annotationType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspectPropsBase).__jsii_proxy_class__ = lambda : _IAspectPropsBaseProxy


@jsii.interface(
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.IAspectPropsExtended"
)
class IAspectPropsExtended(IAspectPropsBase, typing_extensions.Protocol):
    '''The extended aspect properties available only to the base security aspects.

    These additional properties shouldn't be changed in aspects that already have clearly defined goals.
    So, this extended properties interface is applied selectively to the base aspects.
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="anySource")
    def any_source(self) -> typing.Optional[builtins.bool]:
        '''Whether any source is valid.

        This will ignore all other restrictions and only check the port.

        :default: false
        '''
        ...

    @any_source.setter
    def any_source(self, value: typing.Optional[builtins.bool]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The restricted port.

        Defaults to restricting all ports and only checking sources.

        :default: undefined
        '''
        ...

    @ports.setter
    def ports(self, value: typing.Optional[typing.List[jsii.Number]]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictedCidrs")
    def restricted_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The restricted CIDRs for the given port.

        :default: ['0.0.0.0/0', '::/0']
        '''
        ...

    @restricted_cidrs.setter
    def restricted_cidrs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictedSGs")
    def restricted_s_gs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The restricted source security groups for the given port.

        :default: undefined
        '''
        ...

    @restricted_s_gs.setter
    def restricted_s_gs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        ...


class _IAspectPropsExtendedProxy(
    jsii.proxy_for(IAspectPropsBase) # type: ignore[misc]
):
    '''The extended aspect properties available only to the base security aspects.

    These additional properties shouldn't be changed in aspects that already have clearly defined goals.
    So, this extended properties interface is applied selectively to the base aspects.
    '''

    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-aspects-library-security-group.IAspectPropsExtended"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="anySource")
    def any_source(self) -> typing.Optional[builtins.bool]:
        '''Whether any source is valid.

        This will ignore all other restrictions and only check the port.

        :default: false
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "anySource"))

    @any_source.setter
    def any_source(self, value: typing.Optional[builtins.bool]) -> None:
        jsii.set(self, "anySource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The restricted port.

        Defaults to restricting all ports and only checking sources.

        :default: undefined
        '''
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.Optional[typing.List[jsii.Number]]) -> None:
        jsii.set(self, "ports", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictedCidrs")
    def restricted_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The restricted CIDRs for the given port.

        :default: ['0.0.0.0/0', '::/0']
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedCidrs"))

    @restricted_cidrs.setter
    def restricted_cidrs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "restrictedCidrs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictedSGs")
    def restricted_s_gs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The restricted source security groups for the given port.

        :default: undefined
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedSGs"))

    @restricted_s_gs.setter
    def restricted_s_gs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "restrictedSGs", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspectPropsExtended).__jsii_proxy_class__ = lambda : _IAspectPropsExtendedProxy


@jsii.interface(
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.IRuleCheckArgs"
)
class IRuleCheckArgs(IAspectPropsExtended, typing_extensions.Protocol):
    '''The arguments for the checkRules function.

    Extends the IAspectPropsBase interface which includes additional properties that can be used as args.
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> aws_cdk.core.IConstruct:
        '''The node to check.'''
        ...

    @node.setter
    def node(self, value: aws_cdk.core.IConstruct) -> None:
        ...


class _IRuleCheckArgsProxy(
    jsii.proxy_for(IAspectPropsExtended) # type: ignore[misc]
):
    '''The arguments for the checkRules function.

    Extends the IAspectPropsBase interface which includes additional properties that can be used as args.
    '''

    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-aspects-library-security-group.IRuleCheckArgs"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> aws_cdk.core.IConstruct:
        '''The node to check.'''
        return typing.cast(aws_cdk.core.IConstruct, jsii.get(self, "node"))

    @node.setter
    def node(self, value: aws_cdk.core.IConstruct) -> None:
        jsii.set(self, "node", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRuleCheckArgs).__jsii_proxy_class__ = lambda : _IRuleCheckArgsProxy


@jsii.implements(aws_cdk.core.IAspect)
class SecurityGroupAspectBase(
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.SecurityGroupAspectBase",
):
    '''The base class for all security group aspects in the library.

    By default this will not restrict anything.
    '''

    def __init__(self, props: typing.Optional[IAspectPropsExtended] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="annotationText")
    def annotation_text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotationText"))

    @annotation_text.setter
    def annotation_text(self, value: builtins.str) -> None:
        jsii.set(self, "annotationText", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="annotationType")
    def annotation_type(self) -> AnnotationType:
        return typing.cast(AnnotationType, jsii.get(self, "annotationType"))

    @annotation_type.setter
    def annotation_type(self, value: AnnotationType) -> None:
        jsii.set(self, "annotationType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="anySource")
    def any_source(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "anySource"))

    @any_source.setter
    def any_source(self, value: builtins.bool) -> None:
        jsii.set(self, "anySource", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.Optional[typing.List[jsii.Number]]) -> None:
        jsii.set(self, "ports", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictedCidrs")
    def restricted_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedCidrs"))

    @restricted_cidrs.setter
    def restricted_cidrs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "restrictedCidrs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="restrictedSGs")
    def restricted_s_gs(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "restrictedSGs"))

    @restricted_s_gs.setter
    def restricted_s_gs(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "restrictedSGs", value)


class NoIngressCommonManagementPortsAspect(
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoIngressCommonManagementPortsAspect",
):
    '''Aspect to restrict any access to common management ports.

    22 - SSH
    3389 - RDP
    5985 - WinRM
    5986 - WinRM HTTPS
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoIngressCommonRelationalDBPortsAspect(
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoIngressCommonRelationalDBPortsAspect",
):
    '''Aspect to restrict any access to common relational DB ports.

    3306 - MySQL
    5432 - PostgreSQL
    1521 - Oracle
    1433 - SQL Server
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoIngressCommonWebPortsAspect(
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoIngressCommonWebPortsAspect",
):
    '''Aspect to restrict any access to common web ports.

    80 - HTTP
    443 - HTTPS
    8080 - HTTP
    8443 - HTTPS
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


@jsii.implements(aws_cdk.core.IAspect)
class NoPublicIngressAspectBase(
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressAspectBase",
):
    '''The base aspect to determine if a security group allows inbound traffic from the public internet to any port.

    This inherits everything from the base SecurityGroupAspectBase class and sets a default set of CIDRS that match allowing all IPs on AWS.
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoPublicIngressCommonManagementPortsAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressCommonManagementPortsAspect",
):
    '''Aspect to restrict public access to common management ports.

    22 - SSH
    3389 - RDP
    5985 - WinRM
    5986 - WinRM HTTPS
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoPublicIngressCommonRelationalDBPortsAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressCommonRelationalDBPortsAspect",
):
    '''Aspect to restrict public access to common relational DB ports.

    3306 - MySQL
    5432 - PostgreSQL
    1521 - Oracle
    1433 - SQL Server
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoPublicIngressCommonWebPortsAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressCommonWebPortsAspect",
):
    '''Aspect to restrict public access to common web ports.

    80 - HTTP
    443 - HTTPS
    8080 - HTTP
    8443 - HTTPS
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoPublicIngressRDPAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressRDPAspect",
):
    '''Aspect to determine if a security group allows inbound traffic from the public internet to the RDP port.'''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoPublicIngressSSHAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressSSHAspect",
):
    '''Aspect to determine if a security group allows inbound traffic from the public internet to the SSH port.'''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class AWSRestrictedCommonPortsAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.AWSRestrictedCommonPortsAspect",
):
    '''Restricted common ports based on AWS Config rule https://docs.aws.amazon.com/config/latest/developerguide/restricted-common-ports.html.'''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class CISAwsFoundationBenchmark4Dot1Aspect(
    NoPublicIngressSSHAspect,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.CISAwsFoundationBenchmark4Dot1Aspect",
):
    '''CIS AWS Foundations Benchmark 4.1.

    CIS recommends that no security group allow unrestricted ingress access to port 22. Removing unfettered connectivity to remote console services, such as SSH, reduces a server's exposure to risk.

    This aspect uses the NoPublicIngressSSHAspect with an alternate annotation text.
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class CISAwsFoundationBenchmark4Dot2Aspect(
    NoPublicIngressRDPAspect,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.CISAwsFoundationBenchmark4Dot2Aspect",
):
    '''CIS AWS Foundations Benchmark 4.2.

    CIS recommends that no security group allow unrestricted ingress access to port 3389. Removing unfettered connectivity to remote console services, such as RDP, reduces a server's exposure to risk.

    This aspect uses the NoPublicIngressRDPAspect with an alternate annotation text.
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


@jsii.implements(aws_cdk.core.IAspect)
class NoPublicIngressAspect(
    NoPublicIngressAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressAspect",
):
    '''The same as the base NoPublicIngressAspectBase but with a more descriptive annotation.

    Blocks the ANY port from the public internet.
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


__all__ = [
    "AWSRestrictedCommonPortsAspect",
    "AnnotationType",
    "CISAwsFoundationBenchmark4Dot1Aspect",
    "CISAwsFoundationBenchmark4Dot2Aspect",
    "IAspectPropsBase",
    "IAspectPropsExtended",
    "IRuleCheckArgs",
    "NoIngressCommonManagementPortsAspect",
    "NoIngressCommonRelationalDBPortsAspect",
    "NoIngressCommonWebPortsAspect",
    "NoPublicIngressAspect",
    "NoPublicIngressAspectBase",
    "NoPublicIngressCommonManagementPortsAspect",
    "NoPublicIngressCommonRelationalDBPortsAspect",
    "NoPublicIngressCommonWebPortsAspect",
    "NoPublicIngressRDPAspect",
    "NoPublicIngressSSHAspect",
    "SecurityGroupAspectBase",
]

publication.publish()
