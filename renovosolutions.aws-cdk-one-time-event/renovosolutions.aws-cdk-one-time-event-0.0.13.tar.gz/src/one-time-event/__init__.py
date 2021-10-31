'''
# cdk-library-one-time-event

An AWS CDK Construct library to create one time event [schedules](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Schedule.html).

## Features

* Create two types of event [schedules](https://docs.aws.amazon.com/cdk/api/latest/docs/@aws-cdk_aws-events.Schedule.html) easily:

  * On Deployment: An one time event schedule for directly after deployment. Defaults to 10mins after.
  * At: A one time even schedule for any future `Date()`

## API Doc

See [API](API.md)

## Examples

### Typescript - run after deploy, offset 15mins

```
import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as oneTimeEvents from '@renovosolutions/cdk-library-one-time-event';

export class CdkExampleLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const handler = new lambda.Function(this, 'handler', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(functionDir + '/function.zip'),
      handler: 'index.handler',
    });

    new events.Rule(this, 'triggerImmediate', {
      schedule: new oneTimeEvents.OnDeploy(this, 'schedule', {
        offsetMinutes: 15
      }).schedule,
      targets: [new targets.LambdaFunction(this.handler)],
    });
```

### Typescript - run in 24 hours

```
import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as oneTimeEvents from '@renovosolutions/cdk-library-one-time-event';

export class CdkExampleLambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const handler = new lambda.Function(this, 'handler', {
      runtime: lambda.Runtime.PYTHON_3_8,
      code: lambda.Code.fromAsset(functionDir + '/function.zip'),
      handler: 'index.handler',
    });

    var tomorrow = new Date()
    tomorrow.setDate(tomorrow.getDate() + 1)

    new events.Rule(this, 'triggerImmediate', {
      schedule: new oneTimeEvents.At(this, 'schedule', {
        date: tomorrow
      }).schedule,
      targets: [new targets.LambdaFunction(this.handler)],
    });
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

import aws_cdk.aws_events
import aws_cdk.core


class At(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-one-time-event.At",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: "IAtProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> aws_cdk.aws_events.Schedule:
        return typing.cast(aws_cdk.aws_events.Schedule, jsii.get(self, "schedule"))


@jsii.interface(jsii_type="@renovosolutions/cdk-library-one-time-event.IAtProps")
class IAtProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="date")
    def date(self) -> datetime.datetime:
        '''The future date to use for one time event.'''
        ...

    @date.setter
    def date(self, value: datetime.datetime) -> None:
        ...


class _IAtPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-one-time-event.IAtProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="date")
    def date(self) -> datetime.datetime:
        '''The future date to use for one time event.'''
        return typing.cast(datetime.datetime, jsii.get(self, "date"))

    @date.setter
    def date(self, value: datetime.datetime) -> None:
        jsii.set(self, "date", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAtProps).__jsii_proxy_class__ = lambda : _IAtPropsProxy


@jsii.interface(jsii_type="@renovosolutions/cdk-library-one-time-event.IOnDeployProps")
class IOnDeployProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="offsetMinutes")
    def offset_minutes(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes to add to the current time when generating the expression.

        Should exceed the expected time for the appropriate resources to converge.

        :default: 10
        '''
        ...

    @offset_minutes.setter
    def offset_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IOnDeployPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-one-time-event.IOnDeployProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="offsetMinutes")
    def offset_minutes(self) -> typing.Optional[jsii.Number]:
        '''The number of minutes to add to the current time when generating the expression.

        Should exceed the expected time for the appropriate resources to converge.

        :default: 10
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "offsetMinutes"))

    @offset_minutes.setter
    def offset_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "offsetMinutes", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOnDeployProps).__jsii_proxy_class__ = lambda : _IOnDeployPropsProxy


class OnDeploy(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-one-time-event.OnDeploy",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IOnDeployProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> aws_cdk.aws_events.Schedule:
        return typing.cast(aws_cdk.aws_events.Schedule, jsii.get(self, "schedule"))


__all__ = [
    "At",
    "IAtProps",
    "IOnDeployProps",
    "OnDeploy",
]

publication.publish()
