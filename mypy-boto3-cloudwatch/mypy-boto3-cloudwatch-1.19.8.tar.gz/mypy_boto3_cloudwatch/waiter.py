"""
Type annotations for cloudwatch service client waiters.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/waiters.html)

Usage::

    ```python
    import boto3

    from mypy_boto3_cloudwatch import CloudWatchClient
    from mypy_boto3_cloudwatch.waiter import (
        AlarmExistsWaiter,
        CompositeAlarmExistsWaiter,
    )

    client: CloudWatchClient = boto3.client("cloudwatch")

    alarm_exists_waiter: AlarmExistsWaiter = client.get_waiter("alarm_exists")
    composite_alarm_exists_waiter: CompositeAlarmExistsWaiter = client.get_waiter("composite_alarm_exists")
    ```
"""
from typing import Sequence

from botocore.waiter import Waiter as Boto3Waiter

from .literals import AlarmTypeType, StateValueType
from .type_defs import WaiterConfigTypeDef

__all__ = ("AlarmExistsWaiter", "CompositeAlarmExistsWaiter")


class AlarmExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.8/reference/services/cloudwatch.html#CloudWatch.Waiter.AlarmExists)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/waiters.html#alarmexistswaiter)
    """

    def wait(
        self,
        *,
        AlarmNames: Sequence[str] = ...,
        AlarmNamePrefix: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        ChildrenOfAlarmName: str = ...,
        ParentsOfAlarmName: str = ...,
        StateValue: StateValueType = ...,
        ActionPrefix: str = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.8/reference/services/cloudwatch.html#CloudWatch.Waiter.AlarmExists.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/waiters.html#alarmexistswaiter)
        """


class CompositeAlarmExistsWaiter(Boto3Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.8/reference/services/cloudwatch.html#CloudWatch.Waiter.CompositeAlarmExists)
    [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/waiters.html#compositealarmexistswaiter)
    """

    def wait(
        self,
        *,
        AlarmNames: Sequence[str] = ...,
        AlarmNamePrefix: str = ...,
        AlarmTypes: Sequence[AlarmTypeType] = ...,
        ChildrenOfAlarmName: str = ...,
        ParentsOfAlarmName: str = ...,
        StateValue: StateValueType = ...,
        ActionPrefix: str = ...,
        MaxRecords: int = ...,
        NextToken: str = ...,
        WaiterConfig: WaiterConfigTypeDef = ...
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.19.8/reference/services/cloudwatch.html#CloudWatch.Waiter.CompositeAlarmExists.wait)
        [Show boto3-stubs documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_cloudwatch/waiters.html#compositealarmexistswaiter)
        """
