'''
<!--
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
-->

# cdk-nag

| Language   | cdk-nag                                                                                   | monocdk-nag                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Python     | [![PyPI version](https://badge.fury.io/py/cdk-nag.svg)](https://badge.fury.io/py/cdk-nag) | [![PyPI version](https://badge.fury.io/py/monocdk-nag.svg)](https://badge.fury.io/py/monocdk-nag) |
| TypeScript | [![npm version](https://badge.fury.io/js/cdk-nag.svg)](https://badge.fury.io/js/cdk-nag)  | [![npm version](https://badge.fury.io/js/monocdk-nag.svg)](https://badge.fury.io/js/monocdk-nag)  |

Check CDK applications for best practices using a combination of available rule packs. Inspired by [cfn_nag](https://github.com/stelligent/cfn_nag)

![](cdk_nag.gif)

## Available Packs

See [RULES](./RULES.md) for more information on all the available packs.

1. [AWS Solutions](./RULES.md#awssolutions)
2. [HIPAA Security](./RULES.md#hipaa-security)
3. [NIST 800-53 rev 4](./RULES.md#nist-800-53-rev-4)
4. [NIST 800-53 rev 5](./RULES.md#nist-800-53-rev-5)
5. [PCI DSS 3.2.1](./RULES.md#pci-dss-321)

## Usage

### cdk

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

### monocdk

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from monocdk import App, Aspects
from ...lib.my_stack import CdkTestStack
from monocdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

## Suppressing a Rule

<details>
  <summary>Example 1) Default Construct</summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ec2 import SecurityGroup, Vpc, Peer, Port
from aws_cdk.core import Construct, Stack, StackProps
from cdk_nag import NagSuppressions

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        test = SecurityGroup(self, "test",
            vpc=Vpc(self, "vpc")
        )
        test.add_ingress_rule(Peer.any_ipv4(), Port.all_traffic())
        NagSuppressions.add_resource_suppressions(test, [id="AwsSolutions-EC23", reason="lorem ipsum"
        ])
```

</details><details>
  <summary>Example 2) Child Constructs</summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_iam import User, PolicyStatement
from aws_cdk.core import Construct, Stack, StackProps
from cdk_nag import NagSuppressions

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        user = User(self, "rUser")
        user.add_to_policy(
            PolicyStatement(
                actions=["s3:PutObject"],
                resources=["arn:aws:s3:::bucket_name/*"]
            ))
        # Enable adding suppressions to child constructs
        NagSuppressions.add_resource_suppressions(user, [{"id": "AwsSolutions-IAM5", "reason": "lorem ipsum"}], True)
```

</details><details>
  <summary>Example 3) Stack Level </summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks, NagSuppressions

app = App()
stack = CdkTestStack(app, "CdkNagDemo")
Aspects.of(app).add(AwsSolutionsChecks())
NagSuppressions.add_stack_suppressions(stack, [id="AwsSolutions-EC23", reason="lorem ipsum"
])
```

</details>

## Rules and Property Overrides

In some cases L2 Constructs do not have a native option to remediate an issue and must be fixed via [Raw Overrides](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html#cfn_layer_raw). Since raw overrides take place after template synthesis these fixes are not caught by the cdk_nag. In this case you should remediate the issue and suppress the issue like in the following example.

<details>
  <summary>Example) Property Overrides</summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_ec2 import Instance, InstanceType, InstanceClass, MachineImage, Vpc, CfnInstance
from aws_cdk.core import Construct, Stack, StackProps
from cdk_nag import NagSuppressions

class CdkTestStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        instance = Instance(self, "rInstance",
            vpc=Vpc(self, "rVpc"),
            instance_type=InstanceType(InstanceClass.T3),
            machine_image=MachineImage.latest_amazon_linux()
        )
        cfn_ins = instance.node.default_child
        cfn_ins.add_property_override("DisableApiTermination", True)
        NagSuppressions.add_resource_suppressions(instance, [
            id="AwsSolutions-EC29",
            reason="Remediated through property override."

        ])
```

</details>

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
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


@jsii.interface(jsii_type="cdk-nag.IApplyRule")
class IApplyRule(typing_extensions.Protocol):
    '''Interface for JSII interoperability for passing parameters and the Rule Callback to @applyRule method.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="explanation")
    def explanation(self) -> builtins.str:
        '''Why the rule exists.'''
        ...

    @explanation.setter
    def explanation(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        '''Why the rule was triggered.'''
        ...

    @info.setter
    def info(self, value: builtins.str) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="level")
    def level(self) -> "NagMessageLevel":
        '''The annotations message level to apply to the rule if triggered.'''
        ...

    @level.setter
    def level(self, value: "NagMessageLevel") -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> aws_cdk.core.CfnResource:
        '''Ignores listed in cdk-nag metadata.'''
        ...

    @node.setter
    def node(self, value: aws_cdk.core.CfnResource) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        '''The id of the rule to ignore.'''
        ...

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        ...

    @jsii.member(jsii_name="rule")
    def rule(self, node: aws_cdk.core.CfnResource) -> builtins.bool:
        '''The callback to the rule.

        :param node: the CfnResource to check.
        '''
        ...


class _IApplyRuleProxy:
    '''Interface for JSII interoperability for passing parameters and the Rule Callback to @applyRule method.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-nag.IApplyRule"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="explanation")
    def explanation(self) -> builtins.str:
        '''Why the rule exists.'''
        return typing.cast(builtins.str, jsii.get(self, "explanation"))

    @explanation.setter
    def explanation(self, value: builtins.str) -> None:
        jsii.set(self, "explanation", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="info")
    def info(self) -> builtins.str:
        '''Why the rule was triggered.'''
        return typing.cast(builtins.str, jsii.get(self, "info"))

    @info.setter
    def info(self, value: builtins.str) -> None:
        jsii.set(self, "info", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="level")
    def level(self) -> "NagMessageLevel":
        '''The annotations message level to apply to the rule if triggered.'''
        return typing.cast("NagMessageLevel", jsii.get(self, "level"))

    @level.setter
    def level(self, value: "NagMessageLevel") -> None:
        jsii.set(self, "level", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="node")
    def node(self) -> aws_cdk.core.CfnResource:
        '''Ignores listed in cdk-nag metadata.'''
        return typing.cast(aws_cdk.core.CfnResource, jsii.get(self, "node"))

    @node.setter
    def node(self, value: aws_cdk.core.CfnResource) -> None:
        jsii.set(self, "node", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> builtins.str:
        '''The id of the rule to ignore.'''
        return typing.cast(builtins.str, jsii.get(self, "ruleId"))

    @rule_id.setter
    def rule_id(self, value: builtins.str) -> None:
        jsii.set(self, "ruleId", value)

    @jsii.member(jsii_name="rule")
    def rule(self, node: aws_cdk.core.CfnResource) -> builtins.bool:
        '''The callback to the rule.

        :param node: the CfnResource to check.
        '''
        return typing.cast(builtins.bool, jsii.invoke(self, "rule", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApplyRule).__jsii_proxy_class__ = lambda : _IApplyRuleProxy


@jsii.enum(jsii_type="cdk-nag.NagMessageLevel")
class NagMessageLevel(enum.Enum):
    '''The level of the message that the rule applies.'''

    WARN = "WARN"
    ERROR = "ERROR"


@jsii.implements(aws_cdk.core.IAspect)
class NagPack(metaclass=jsii.JSIIAbstractClass, jsii_type="cdk-nag.NagPack"):
    '''Base class for all rule sets.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="applyRule")
    def apply_rule(self, params: IApplyRule) -> None:
        '''Create a rule to be used in the NagPack.

        :param params: The.

        :IApplyRule: interface with rule details
        '''
        return typing.cast(None, jsii.invoke(self, "applyRule", [params]))

    @jsii.member(jsii_name="visit") # type: ignore[misc]
    @abc.abstractmethod
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="logIgnores")
    def _log_ignores(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "logIgnores"))

    @_log_ignores.setter
    def _log_ignores(self, value: builtins.bool) -> None:
        jsii.set(self, "logIgnores", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="verbose")
    def _verbose(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "verbose"))

    @_verbose.setter
    def _verbose(self, value: builtins.bool) -> None:
        jsii.set(self, "verbose", value)


class _NagPackProxy(NagPack):
    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, NagPack).__jsii_proxy_class__ = lambda : _NagPackProxy


@jsii.data_type(
    jsii_type="cdk-nag.NagPackProps",
    jsii_struct_bases=[],
    name_mapping={"log_ignores": "logIgnores", "verbose": "verbose"},
)
class NagPackProps:
    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Interface for creating a Nag rule set.

        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if log_ignores is not None:
            self._values["log_ignores"] = log_ignores
        if verbose is not None:
            self._values["verbose"] = verbose

    @builtins.property
    def log_ignores(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to log triggered rules that have been suppressed as informational messages (default: false).'''
        result = self._values.get("log_ignores")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).'''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagPackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-nag.NagPackSuppression",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "reason": "reason"},
)
class NagPackSuppression:
    def __init__(self, *, id: builtins.str, reason: builtins.str) -> None:
        '''Interface for creating a rule suppression.

        :param id: The id of the rule to ignore.
        :param reason: The reason to ignore the rule (minimum 10 characters).
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "id": id,
            "reason": reason,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''The id of the rule to ignore.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reason(self) -> builtins.str:
        '''The reason to ignore the rule (minimum 10 characters).'''
        result = self._values.get("reason")
        assert result is not None, "Required property 'reason' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NagPackSuppression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NagSuppressions(metaclass=jsii.JSIIMeta, jsii_type="cdk-nag.NagSuppressions"):
    '''Helper class with methods to add cdk-nag suppressions to cdk resources.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addResourceSuppressions") # type: ignore[misc]
    @builtins.classmethod
    def add_resource_suppressions(
        cls,
        construct: aws_cdk.core.IConstruct,
        suppressions: typing.Sequence[NagPackSuppression],
        apply_to_children: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Add cdk-nag suppressions to the construct if it is a CfnResource.

        :param construct: the IConstruct to apply the suppression to.
        :param suppressions: a list of suppressions to apply to the resource.
        :param apply_to_children: apply the suppressions to this construct and all of its children if they exist (default:false).
        '''
        return typing.cast(None, jsii.sinvoke(cls, "addResourceSuppressions", [construct, suppressions, apply_to_children]))

    @jsii.member(jsii_name="addResourceSuppressionsByPath") # type: ignore[misc]
    @builtins.classmethod
    def add_resource_suppressions_by_path(
        cls,
        stack: aws_cdk.core.Stack,
        path: builtins.str,
        suppressions: typing.Sequence[NagPackSuppression],
        apply_to_children: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Locate a construct by it's path and add cdk-nag suppressions if it both exists and is a CfnResource.

        :param stack: the Stack the construct belongs to.
        :param path: the path of the construct in the provided stack.
        :param suppressions: a list of suppressions to apply to the resource.
        :param apply_to_children: apply the suppressions to this construct and all of its children if they exist (default:false).
        '''
        return typing.cast(None, jsii.sinvoke(cls, "addResourceSuppressionsByPath", [stack, path, suppressions, apply_to_children]))

    @jsii.member(jsii_name="addStackSuppressions") # type: ignore[misc]
    @builtins.classmethod
    def add_stack_suppressions(
        cls,
        stack: aws_cdk.core.Stack,
        suppressions: typing.Sequence[NagPackSuppression],
    ) -> None:
        '''Add cdk-nag suppressions to the Stack.

        :param stack: the Stack to apply the suppression to.
        :param suppressions: a list of suppressions to apply to the stack.
        '''
        return typing.cast(None, jsii.sinvoke(cls, "addStackSuppressions", [stack, suppressions]))


class PCIDSS321Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.PCIDSS321Checks",
):
    '''Check for PCI DSS 3.2.1 compliance. Based on the PCI DSS 3.2.1 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-pci-dss.html.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class AwsSolutionsChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.AwsSolutionsChecks",
):
    '''Check Best practices based on AWS Solutions Security Matrix.'''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class HIPAASecurityChecks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.HIPAASecurityChecks",
):
    '''Check for HIPAA Security compliance.

    Based on the HIPAA Security AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-hipaa_security.html
    '''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class NIST80053R4Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.NIST80053R4Checks",
):
    '''Check for NIST 800-53 rev 4 compliance.

    Based on the NIST 800-53 rev 4 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_4.html
    '''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


class NIST80053R5Checks(
    NagPack,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-nag.NIST80053R5Checks",
):
    '''Check for NIST 800-53 rev 5 compliance.

    Based on the NIST 800-53 rev 5 AWS operational best practices: https://docs.aws.amazon.com/config/latest/developerguide/operational-best-practices-for-nist-800-53_rev_5.html
    '''

    def __init__(
        self,
        *,
        log_ignores: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param log_ignores: Whether or not to log triggered rules that have been suppressed as informational messages (default: false).
        :param verbose: Whether or not to enable extended explanatory descriptions on warning, error, and logged ignore messages (default: false).
        '''
        props = NagPackProps(log_ignores=log_ignores, verbose=verbose)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="visit")
    def visit(self, node: aws_cdk.core.IConstruct) -> None:
        '''All aspects can visit an IConstruct.

        :param node: -
        '''
        return typing.cast(None, jsii.invoke(self, "visit", [node]))


__all__ = [
    "AwsSolutionsChecks",
    "HIPAASecurityChecks",
    "IApplyRule",
    "NIST80053R4Checks",
    "NIST80053R5Checks",
    "NagMessageLevel",
    "NagPack",
    "NagPackProps",
    "NagPackSuppression",
    "NagSuppressions",
    "PCIDSS321Checks",
]

publication.publish()
