'''
# Actions for AWS IoT Rule

This library contains integration classes to send data to any number of
supported AWS Services. Instances of these classes should be passed to
`TopicRule` defined in `@aws-cdk/aws-iot`.

Currently supported are:

* Invoke a Lambda function

## Invoke a Lambda function

The code snippet below creates an AWS IoT Rule that invoke a Lambda function
when it is triggered.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk import aws_iot as iot
from aws_cdk import aws_iot_actions as actions
from aws_cdk import aws_lambda as lambda_


func = lambda_.Function(self, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("""
            exports.handler = (event) => {
              console.log("It is test for lambda action of AWS IoT Rule.", event);
            };""")
)

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
    actions=[actions.LambdaFunctionAction(func)]
)
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

from .._jsii import *

from ..aws_iot import (
    ActionConfig as _ActionConfig_9dc7cb16,
    IAction as _IAction_25dbea23,
    ITopicRule as _ITopicRule_96d74f80,
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e


@jsii.implements(_IAction_25dbea23)
class LambdaFunctionAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.LambdaFunctionAction",
):
    '''(experimental) The action to invoke an AWS Lambda function, passing in an MQTT message.

    :stability: experimental
    '''

    def __init__(self, func: _IFunction_6e14f09e) -> None:
        '''
        :param func: The lambda function to be invoked by this action.

        :stability: experimental
        '''
        jsii.create(self.__class__, self, [func])

    @jsii.member(jsii_name="bind")
    def bind(self, topic_rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param topic_rule: -

        :stability: experimental
        '''
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [topic_rule]))


__all__ = [
    "LambdaFunctionAction",
]

publication.publish()
