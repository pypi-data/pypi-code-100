'''
# cdk-aspects-library-security-group

A CDK library containing EC2 security group related [CDK Aspects](https://docs.aws.amazon.com/cdk/latest/guide/aspects.html) and the ability to define custom aspects.

## Features

* Utilize built in aspects for common cases:

  * Disallow public access to any port
  * Disallow public access to AWS Restricted Common ports ([per the AWS Config rule](https://docs.aws.amazon.com/config/latest/developerguide/restricted-common-ports.html))
  * Disallow public access to SSH or RDP per CIS Benchmark guidelines and general good practice
* Create any other aspect using the base security group aspect class.
* By default aspects generate errors in the CDK metadata which the deployment or synth process will find, but this can be changed with the `annotationType` property

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
    '''The extended aspect properties available only to the SecurityGroupAspectBase.

    These additional properties shouldn't be changed in aspects that already have clearly defined goals.
    So, this extended properties interface is applied selectively to the SecurityGroupAspectBase.
    '''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The restricted port.

        Defaults to all ports.

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


class _IAspectPropsExtendedProxy(
    jsii.proxy_for(IAspectPropsBase) # type: ignore[misc]
):
    '''The extended aspect properties available only to the SecurityGroupAspectBase.

    These additional properties shouldn't be changed in aspects that already have clearly defined goals.
    So, this extended properties interface is applied selectively to the SecurityGroupAspectBase.
    '''

    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-aspects-library-security-group.IAspectPropsExtended"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''The restricted port.

        Defaults to all ports.

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

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAspectPropsExtended).__jsii_proxy_class__ = lambda : _IAspectPropsExtendedProxy


@jsii.implements(aws_cdk.core.IAspect)
class SecurityGroupAspectBase(
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.SecurityGroupAspectBase",
):
    '''The base class for all security group aspects in the library.

    By default this will restrict all ports that use the typical "any" CIDRs on AWS (0.0.0.0/0 and ::/0) and
    will generate an error in the CDK metadata with a generic error about a blocked security group rule.
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
    @jsii.member(jsii_name="restrictedCidrs")
    def restricted_cidrs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "restrictedCidrs"))

    @restricted_cidrs.setter
    def restricted_cidrs(self, value: typing.List[builtins.str]) -> None:
        jsii.set(self, "restrictedCidrs", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.Optional[typing.List[jsii.Number]]) -> None:
        jsii.set(self, "ports", value)


class AWSRestrictedCommonPortsAspect(
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.AWSRestrictedCommonPortsAspect",
):
    '''Restricted common ports based on AWS Config rule https://docs.aws.amazon.com/config/latest/developerguide/restricted-common-ports.html.'''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


@jsii.implements(aws_cdk.core.IAspect)
class NoPublicIngressAspect(
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressAspect",
):
    '''Aspect to determine if a security group allows inbound traffic from the public internet to any port.

    This inherits everything from the base SecurityGroupAspectBase class and modifies the default annotation text.
    '''

    def __init__(self, props: typing.Optional[IAspectPropsBase] = None) -> None:
        '''
        :param props: -
        '''
        jsii.create(self.__class__, self, [props])


class NoPublicIngressRDPAspect(
    SecurityGroupAspectBase,
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
    SecurityGroupAspectBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-aspects-library-security-group.NoPublicIngressSSHAspect",
):
    '''Aspect to determine if a security group allows inbound traffic from the public internet to the SSH port.'''

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


__all__ = [
    "AWSRestrictedCommonPortsAspect",
    "AnnotationType",
    "CISAwsFoundationBenchmark4Dot1Aspect",
    "CISAwsFoundationBenchmark4Dot2Aspect",
    "IAspectPropsBase",
    "IAspectPropsExtended",
    "NoPublicIngressAspect",
    "NoPublicIngressRDPAspect",
    "NoPublicIngressSSHAspect",
    "SecurityGroupAspectBase",
]

publication.publish()
