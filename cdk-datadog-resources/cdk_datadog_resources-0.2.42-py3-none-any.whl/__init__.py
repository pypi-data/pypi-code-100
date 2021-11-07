'''
# AWS CDK Datadog Resources

[![npm version](https://badge.fury.io/js/%40nomadblacky%2Fcdk-datadog-resources.svg)](https://badge.fury.io/js/%40nomadblacky%2Fcdk-datadog-resources)

An AWS CDK construct library that wraps [DataDog/datadog-cloudformation-resources](https://github.com/DataDog/datadog-cloudformation-resources).

## Requirements

Before using this library, [register datadog-cloudformation-resources to your AWS account.](https://github.com/DataDog/datadog-cloudformation-resources#datadog-aws-cloudformation)

You need to register the correct version listed in `Supported Resources`.

## Supported CDK Languages

* TypeScript
* Python
* ~~Java~~ Sorry, there is a problem with the release. ([#22](https://github.com/NomadBlacky/cdk-datadog-resources/issues/22))

## Supported Resources

| Supported? | Resource                | Datadog CF Resource Name         | Description                                              | Datadog CF Version |
| :--------: | ----------------------- | -------------------------------- | -------------------------------------------------------- | ------------------ |
|     ✅     | Dashboards              | `Datadog::Dashboards::Dashboard` | [Create, update, and delete Datadog dashboards.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-dashboards-dashboard-handler)      | [1.0.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-dashboards-dashboard-handler/CHANGELOG.md#100--2021-02-16)         |
|     ✅     | Datadog-AWS integration | `Datadog::Integrations::AWS`     | [Manage your Datadog-Amazon Web Service integration.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-integrations-aws-handler) | [1.1.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-integrations-aws-handler/CHANGELOG.md#110--2020-08-04)        |
|     ✅     | Monitors                | `Datadog::Monitors::Monitor`     | [Create, update, and delete Datadog monitors.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-monitor-handler)        | [3.0.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-monitor-handler/CHANGELOG.md#300--2021-02-16)         |
|     ✅     | Downtimes               | `Datadog::Monitors::Downtime`    | [Enable or disable downtimes for your monitors.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-monitors-downtime-handler)      | [2.0.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-monitors-downtime-handler/CHANGELOG.md#200--2021-02-16)         |
|     ✅     | Users                   | `Datadog::IAM::User`             | [Create and manage Datadog users.](https://github.com/DataDog/datadog-cloudformation-resources/tree/master/datadog-iam-user-handler)                    | [1.2.0](https://github.com/DataDog/datadog-cloudformation-resources/blob/master/datadog-iam-user-handler/CHANGELOG.md#120--2021-02-16)         |

## Installation

TypeScript

```shell
npm install @nomadblacky/cdk-datadog-resources
```

Python

```shell
pip install cdk-datadog-resources
```

Java

```xml
<dependency>
    <groupId>dev.nomadblacky</groupId>
    <artifactId>cdk-datadog-resources</artifactId>
    <version>x.y.z</version>
</dependency>
```

## Usage

Below are examples of TypeScript.

### Dashboards

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
import fs as fs
from nomadblacky.cdk_datadog_resources import DatadogDashboard

DatadogDashboard(your_stack, "TestDashboard",
    datadog_credentials={
        "api_key": process.env.DATADOG_API_KEY,
        "application_key": process.env.DATADOG_APP_KEY
    },
    dashboard_definition=fs.read_file_sync(f"{__dirname}/path/to/your/dashboard-definition.json").to_string()
)
```

### Monitors

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogMonitor

DatadogMonitor(your_stack, "TestMonitor",
    datadog_credentials={
        "api_key": process.env.DATADOG_API_KEY,
        "application_key": process.env.DATADOG_APP_KEY
    },
    query="avg(last_1h):sum:system.cpu.system{host:host0} > 100",
    type=MonitorType.QueryAlert,
    name="Test Monitor",
    options={
        "thresholds": {
            "critical": 100,
            "warning": 80,
            "o_k": 90
        },
        "notify_no_data": True,
        "evaluation_delay": 60
    }
)
```

### Downtimes

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogDowntime

DatadogDowntime(stack, "TestMonitor",
    datadog_credentials={
        "api_key": "DATADOG_API_KEY",
        "application_key": "DATADOG_APP_KEY"
    },
    scope=["host:myserver", "service:myservice"],
    start=1624542715,
    end=1624546321
)
```

### Users

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogIAMUser

DatadogIAMUser(stack, "TestUser",
    datadog_credentials={
        "api_key": "DATADOG_API_KEY",
        "application_key": "DATADOG_APP_KEY"
    },
    email="jane.doe@example.com",
    name="name_example",
    handle="title_example",
    disabled=False
)
```

### DataDog Integration

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
from nomadblacky.cdk_datadog_resources import DatadogIntegrationAWS

DatadogIntegrationAWS(self, "DataDogIntegration",
    datadog_credentials={
        "api_key": "DATADOG_API_KEY",
        "application_key": "DATADOG_APP_KEY"
    },
    account_id="ACCOUNT_ID",
    role_name="DatadogIntegrationRole"
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

from ._jsii import *

import aws_cdk.core


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogCredentials",
    jsii_struct_bases=[],
    name_mapping={
        "api_key": "apiKey",
        "application_key": "applicationKey",
        "api_url": "apiURL",
    },
)
class DatadogCredentials:
    def __init__(
        self,
        *,
        api_key: builtins.str,
        application_key: builtins.str,
        api_url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Credentials for the Datadog API.

        :param api_key: Datadog API key.
        :param application_key: Datadog application key.
        :param api_url: Datadog API URL (defaults to https://api.datadoghq.com) Use https://api.datadoghq.eu for EU accounts.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "api_key": api_key,
            "application_key": application_key,
        }
        if api_url is not None:
            self._values["api_url"] = api_url

    @builtins.property
    def api_key(self) -> builtins.str:
        '''Datadog API key.'''
        result = self._values.get("api_key")
        assert result is not None, "Required property 'api_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_key(self) -> builtins.str:
        '''Datadog application key.'''
        result = self._values.get("application_key")
        assert result is not None, "Required property 'application_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_url(self) -> typing.Optional[builtins.str]:
        '''Datadog API URL (defaults to https://api.datadoghq.com) Use https://api.datadoghq.eu for EU accounts.'''
        result = self._values.get("api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogDashboard(
    metaclass=jsii.JSIIMeta,
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogDashboard",
):
    '''Datadog Dashboard 1.0.0.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        dashboard_definition: builtins.str,
        datadog_credentials: DatadogCredentials,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dashboard_definition: JSON string of the dashboard definition.
        :param datadog_credentials: Credentials for the Datadog API.
        '''
        props = DatadogDashboardProps(
            dashboard_definition=dashboard_definition,
            datadog_credentials=datadog_credentials,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogDashboardProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_definition": "dashboardDefinition",
        "datadog_credentials": "datadogCredentials",
    },
)
class DatadogDashboardProps:
    def __init__(
        self,
        *,
        dashboard_definition: builtins.str,
        datadog_credentials: DatadogCredentials,
    ) -> None:
        '''
        :param dashboard_definition: JSON string of the dashboard definition.
        :param datadog_credentials: Credentials for the Datadog API.
        '''
        if isinstance(datadog_credentials, dict):
            datadog_credentials = DatadogCredentials(**datadog_credentials)
        self._values: typing.Dict[str, typing.Any] = {
            "dashboard_definition": dashboard_definition,
            "datadog_credentials": datadog_credentials,
        }

    @builtins.property
    def dashboard_definition(self) -> builtins.str:
        '''JSON string of the dashboard definition.'''
        result = self._values.get("dashboard_definition")
        assert result is not None, "Required property 'dashboard_definition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datadog_credentials(self) -> DatadogCredentials:
        '''Credentials for the Datadog API.'''
        result = self._values.get("datadog_credentials")
        assert result is not None, "Required property 'datadog_credentials' is missing"
        return typing.cast(DatadogCredentials, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogDashboardProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogDowntime(
    metaclass=jsii.JSIIMeta,
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogDowntime",
):
    '''Datadog Monitor Downtime 2.0.0.'''

    def __init__(
        self,
        scope_: aws_cdk.core.Construct,
        id_: builtins.str,
        *,
        datadog_credentials: DatadogCredentials,
        scope: typing.Sequence[builtins.str],
        active: typing.Optional[builtins.bool] = None,
        canceled: typing.Optional[jsii.Number] = None,
        creator_id: typing.Optional[jsii.Number] = None,
        disabled: typing.Optional[builtins.bool] = None,
        downtime_type: typing.Optional[jsii.Number] = None,
        end: typing.Optional[jsii.Number] = None,
        id: typing.Optional[jsii.Number] = None,
        message: typing.Optional[builtins.str] = None,
        monitor_id: typing.Optional[jsii.Number] = None,
        monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        parent_id: typing.Optional[jsii.Number] = None,
        start: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        updater_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope_: -
        :param id_: -
        :param datadog_credentials: Credentials for the Datadog API.
        :param scope: The scope(s) to which the downtime applies.
        :param active: Whether or not this downtime is currently active.
        :param canceled: POSIX Timestamp of cancellation of this downtime (null if not canceled).
        :param creator_id: Id of the user who created this downtime.
        :param disabled: Whether or not this downtime is disabled.
        :param downtime_type: Type of this downtime.
        :param end: POSIX timestamp to end the downtime. If not provided, the downtime is in effect indefinitely (i.e. until you cancel it).
        :param id: Id of this downtime.
        :param message: Message on the downtime.
        :param monitor_id: A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
        :param monitor_tags: A comma-separated list of monitor tags, to which the downtime applies. The resulting downtime applies to monitors that match ALL provided monitor tags.
        :param parent_id: The ID of the parent downtime to this one.
        :param start: POSIX timestamp to start the downtime. If not provided, the downtime starts the moment it is created.
        :param timezone: The timezone for the downtime.
        :param updater_id: Id of the user who updated this downtime.
        '''
        props = DatadogDowntimeProps(
            datadog_credentials=datadog_credentials,
            scope=scope,
            active=active,
            canceled=canceled,
            creator_id=creator_id,
            disabled=disabled,
            downtime_type=downtime_type,
            end=end,
            id=id,
            message=message,
            monitor_id=monitor_id,
            monitor_tags=monitor_tags,
            parent_id=parent_id,
            start=start,
            timezone=timezone,
            updater_id=updater_id,
        )

        jsii.create(self.__class__, self, [scope_, id_, props])


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogDowntimeProps",
    jsii_struct_bases=[],
    name_mapping={
        "datadog_credentials": "datadogCredentials",
        "scope": "scope",
        "active": "active",
        "canceled": "canceled",
        "creator_id": "creatorId",
        "disabled": "disabled",
        "downtime_type": "downtimeType",
        "end": "end",
        "id": "id",
        "message": "message",
        "monitor_id": "monitorId",
        "monitor_tags": "monitorTags",
        "parent_id": "parentId",
        "start": "start",
        "timezone": "timezone",
        "updater_id": "updaterId",
    },
)
class DatadogDowntimeProps:
    def __init__(
        self,
        *,
        datadog_credentials: DatadogCredentials,
        scope: typing.Sequence[builtins.str],
        active: typing.Optional[builtins.bool] = None,
        canceled: typing.Optional[jsii.Number] = None,
        creator_id: typing.Optional[jsii.Number] = None,
        disabled: typing.Optional[builtins.bool] = None,
        downtime_type: typing.Optional[jsii.Number] = None,
        end: typing.Optional[jsii.Number] = None,
        id: typing.Optional[jsii.Number] = None,
        message: typing.Optional[builtins.str] = None,
        monitor_id: typing.Optional[jsii.Number] = None,
        monitor_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        parent_id: typing.Optional[jsii.Number] = None,
        start: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        updater_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param datadog_credentials: Credentials for the Datadog API.
        :param scope: The scope(s) to which the downtime applies.
        :param active: Whether or not this downtime is currently active.
        :param canceled: POSIX Timestamp of cancellation of this downtime (null if not canceled).
        :param creator_id: Id of the user who created this downtime.
        :param disabled: Whether or not this downtime is disabled.
        :param downtime_type: Type of this downtime.
        :param end: POSIX timestamp to end the downtime. If not provided, the downtime is in effect indefinitely (i.e. until you cancel it).
        :param id: Id of this downtime.
        :param message: Message on the downtime.
        :param monitor_id: A single monitor to which the downtime applies. If not provided, the downtime applies to all monitors.
        :param monitor_tags: A comma-separated list of monitor tags, to which the downtime applies. The resulting downtime applies to monitors that match ALL provided monitor tags.
        :param parent_id: The ID of the parent downtime to this one.
        :param start: POSIX timestamp to start the downtime. If not provided, the downtime starts the moment it is created.
        :param timezone: The timezone for the downtime.
        :param updater_id: Id of the user who updated this downtime.
        '''
        if isinstance(datadog_credentials, dict):
            datadog_credentials = DatadogCredentials(**datadog_credentials)
        self._values: typing.Dict[str, typing.Any] = {
            "datadog_credentials": datadog_credentials,
            "scope": scope,
        }
        if active is not None:
            self._values["active"] = active
        if canceled is not None:
            self._values["canceled"] = canceled
        if creator_id is not None:
            self._values["creator_id"] = creator_id
        if disabled is not None:
            self._values["disabled"] = disabled
        if downtime_type is not None:
            self._values["downtime_type"] = downtime_type
        if end is not None:
            self._values["end"] = end
        if id is not None:
            self._values["id"] = id
        if message is not None:
            self._values["message"] = message
        if monitor_id is not None:
            self._values["monitor_id"] = monitor_id
        if monitor_tags is not None:
            self._values["monitor_tags"] = monitor_tags
        if parent_id is not None:
            self._values["parent_id"] = parent_id
        if start is not None:
            self._values["start"] = start
        if timezone is not None:
            self._values["timezone"] = timezone
        if updater_id is not None:
            self._values["updater_id"] = updater_id

    @builtins.property
    def datadog_credentials(self) -> DatadogCredentials:
        '''Credentials for the Datadog API.'''
        result = self._values.get("datadog_credentials")
        assert result is not None, "Required property 'datadog_credentials' is missing"
        return typing.cast(DatadogCredentials, result)

    @builtins.property
    def scope(self) -> typing.List[builtins.str]:
        '''The scope(s) to which the downtime applies.'''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def active(self) -> typing.Optional[builtins.bool]:
        '''Whether or not this downtime is currently active.'''
        result = self._values.get("active")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def canceled(self) -> typing.Optional[jsii.Number]:
        '''POSIX Timestamp of cancellation of this downtime (null if not canceled).'''
        result = self._values.get("canceled")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def creator_id(self) -> typing.Optional[jsii.Number]:
        '''Id of the user who created this downtime.'''
        result = self._values.get("creator_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.bool]:
        '''Whether or not this downtime is disabled.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def downtime_type(self) -> typing.Optional[jsii.Number]:
        '''Type of this downtime.'''
        result = self._values.get("downtime_type")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def end(self) -> typing.Optional[jsii.Number]:
        '''POSIX timestamp to end the downtime.

        If not provided, the downtime is in effect indefinitely (i.e. until you cancel it).
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[jsii.Number]:
        '''Id of this downtime.'''
        result = self._values.get("id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Message on the downtime.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitor_id(self) -> typing.Optional[jsii.Number]:
        '''A single monitor to which the downtime applies.

        If not provided, the downtime applies to all monitors.
        '''
        result = self._values.get("monitor_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A comma-separated list of monitor tags, to which the downtime applies.

        The resulting downtime applies to monitors that match ALL provided monitor tags.
        '''
        result = self._values.get("monitor_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def parent_id(self) -> typing.Optional[jsii.Number]:
        '''The ID of the parent downtime to this one.'''
        result = self._values.get("parent_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start(self) -> typing.Optional[jsii.Number]:
        '''POSIX timestamp to start the downtime.

        If not provided, the downtime starts the moment it is created.
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone for the downtime.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def updater_id(self) -> typing.Optional[jsii.Number]:
        '''Id of the user who updated this downtime.'''
        result = self._values.get("updater_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogDowntimeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogIAMUser(
    metaclass=jsii.JSIIMeta,
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogIAMUser",
):
    '''Datadog Application User 1.2.0.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        datadog_credentials: DatadogCredentials,
        access_role: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[builtins.bool] = None,
        email: typing.Optional[builtins.str] = None,
        handle: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        verified: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param datadog_credentials: Credentials for the Datadog API.
        :param access_role: The role of the user.
        :param disabled: Whether or not the user is disabled.
        :param email: User email.
        :param handle: User handle (a valid email).
        :param name: User name.
        :param verified: Whether or not the user is verified.
        '''
        props = DatadogIAMUserProps(
            datadog_credentials=datadog_credentials,
            access_role=access_role,
            disabled=disabled,
            email=email,
            handle=handle,
            name=name,
            verified=verified,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogIAMUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "datadog_credentials": "datadogCredentials",
        "access_role": "accessRole",
        "disabled": "disabled",
        "email": "email",
        "handle": "handle",
        "name": "name",
        "verified": "verified",
    },
)
class DatadogIAMUserProps:
    def __init__(
        self,
        *,
        datadog_credentials: DatadogCredentials,
        access_role: typing.Optional[builtins.str] = None,
        disabled: typing.Optional[builtins.bool] = None,
        email: typing.Optional[builtins.str] = None,
        handle: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        verified: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param datadog_credentials: Credentials for the Datadog API.
        :param access_role: The role of the user.
        :param disabled: Whether or not the user is disabled.
        :param email: User email.
        :param handle: User handle (a valid email).
        :param name: User name.
        :param verified: Whether or not the user is verified.
        '''
        if isinstance(datadog_credentials, dict):
            datadog_credentials = DatadogCredentials(**datadog_credentials)
        self._values: typing.Dict[str, typing.Any] = {
            "datadog_credentials": datadog_credentials,
        }
        if access_role is not None:
            self._values["access_role"] = access_role
        if disabled is not None:
            self._values["disabled"] = disabled
        if email is not None:
            self._values["email"] = email
        if handle is not None:
            self._values["handle"] = handle
        if name is not None:
            self._values["name"] = name
        if verified is not None:
            self._values["verified"] = verified

    @builtins.property
    def datadog_credentials(self) -> DatadogCredentials:
        '''Credentials for the Datadog API.'''
        result = self._values.get("datadog_credentials")
        assert result is not None, "Required property 'datadog_credentials' is missing"
        return typing.cast(DatadogCredentials, result)

    @builtins.property
    def access_role(self) -> typing.Optional[builtins.str]:
        '''The role of the user.'''
        result = self._values.get("access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disabled(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the user is disabled.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def email(self) -> typing.Optional[builtins.str]:
        '''User email.'''
        result = self._values.get("email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handle(self) -> typing.Optional[builtins.str]:
        '''User handle (a valid email).'''
        result = self._values.get("handle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''User name.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verified(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the user is verified.'''
        result = self._values.get("verified")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogIAMUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogIntegrationAWS(
    metaclass=jsii.JSIIMeta,
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogIntegrationAWS",
):
    '''Datadog Integration 1.1.0.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        account_id: builtins.str,
        datadog_credentials: DatadogCredentials,
        role_name: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account_id: The id of the account with which to integrate.
        :param datadog_credentials: Credentials for the Datadog API.
        :param role_name: The name of the created role.
        '''
        props = DatadogIntegrationAWSProps(
            account_id=account_id,
            datadog_credentials=datadog_credentials,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogIntegrationAWSProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "datadog_credentials": "datadogCredentials",
        "role_name": "roleName",
    },
)
class DatadogIntegrationAWSProps:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        datadog_credentials: DatadogCredentials,
        role_name: builtins.str,
    ) -> None:
        '''
        :param account_id: The id of the account with which to integrate.
        :param datadog_credentials: Credentials for the Datadog API.
        :param role_name: The name of the created role.
        '''
        if isinstance(datadog_credentials, dict):
            datadog_credentials = DatadogCredentials(**datadog_credentials)
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "datadog_credentials": datadog_credentials,
            "role_name": role_name,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The id of the account with which to integrate.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def datadog_credentials(self) -> DatadogCredentials:
        '''Credentials for the Datadog API.'''
        result = self._values.get("datadog_credentials")
        assert result is not None, "Required property 'datadog_credentials' is missing"
        return typing.cast(DatadogCredentials, result)

    @builtins.property
    def role_name(self) -> builtins.str:
        '''The name of the created role.'''
        result = self._values.get("role_name")
        assert result is not None, "Required property 'role_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogIntegrationAWSProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatadogMonitor(
    metaclass=jsii.JSIIMeta,
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogMonitor",
):
    '''Datadog Monitor 3.0.0.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        datadog_credentials: DatadogCredentials,
        query: builtins.str,
        type: "MonitorType",
        message: typing.Optional[builtins.str] = None,
        multi: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional["MonitorOptions"] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param datadog_credentials: Credentials for the Datadog API.
        :param query: The monitor query.
        :param type: The type of the monitor.
        :param message: A message to include with notifications for the monitor.
        :param multi: Whether or not the monitor is multi alert.
        :param name: Name of the monitor.
        :param options: The monitor options.
        :param tags: Tags associated with the monitor.
        '''
        props = DatadogMonitorProps(
            datadog_credentials=datadog_credentials,
            query=query,
            type=type,
            message=message,
            multi=multi,
            name=name,
            options=options,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.DatadogMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "datadog_credentials": "datadogCredentials",
        "query": "query",
        "type": "type",
        "message": "message",
        "multi": "multi",
        "name": "name",
        "options": "options",
        "tags": "tags",
    },
)
class DatadogMonitorProps:
    def __init__(
        self,
        *,
        datadog_credentials: DatadogCredentials,
        query: builtins.str,
        type: "MonitorType",
        message: typing.Optional[builtins.str] = None,
        multi: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        options: typing.Optional["MonitorOptions"] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param datadog_credentials: Credentials for the Datadog API.
        :param query: The monitor query.
        :param type: The type of the monitor.
        :param message: A message to include with notifications for the monitor.
        :param multi: Whether or not the monitor is multi alert.
        :param name: Name of the monitor.
        :param options: The monitor options.
        :param tags: Tags associated with the monitor.
        '''
        if isinstance(datadog_credentials, dict):
            datadog_credentials = DatadogCredentials(**datadog_credentials)
        if isinstance(options, dict):
            options = MonitorOptions(**options)
        self._values: typing.Dict[str, typing.Any] = {
            "datadog_credentials": datadog_credentials,
            "query": query,
            "type": type,
        }
        if message is not None:
            self._values["message"] = message
        if multi is not None:
            self._values["multi"] = multi
        if name is not None:
            self._values["name"] = name
        if options is not None:
            self._values["options"] = options
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def datadog_credentials(self) -> DatadogCredentials:
        '''Credentials for the Datadog API.'''
        result = self._values.get("datadog_credentials")
        assert result is not None, "Required property 'datadog_credentials' is missing"
        return typing.cast(DatadogCredentials, result)

    @builtins.property
    def query(self) -> builtins.str:
        '''The monitor query.'''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "MonitorType":
        '''The type of the monitor.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("MonitorType", result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''A message to include with notifications for the monitor.'''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the monitor is multi alert.'''
        result = self._values.get("multi")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the monitor.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional["MonitorOptions"]:
        '''The monitor options.'''
        result = self._values.get("options")
        return typing.cast(typing.Optional["MonitorOptions"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with the monitor.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatadogMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.MonitorOptions",
    jsii_struct_bases=[],
    name_mapping={
        "enable_logs_sample": "enableLogsSample",
        "escalation_message": "escalationMessage",
        "evaluation_delay": "evaluationDelay",
        "include_tags": "includeTags",
        "locked": "locked",
        "min_location_failed": "minLocationFailed",
        "new_host_delay": "newHostDelay",
        "no_data_timeframe": "noDataTimeframe",
        "notify_audit": "notifyAudit",
        "notify_no_data": "notifyNoData",
        "renotify_interval": "renotifyInterval",
        "require_full_window": "requireFullWindow",
        "synthetics_check_id": "syntheticsCheckID",
        "thresholds": "thresholds",
        "threshold_windows": "thresholdWindows",
        "timeout_h": "timeoutH",
    },
)
class MonitorOptions:
    def __init__(
        self,
        *,
        enable_logs_sample: typing.Optional[builtins.bool] = None,
        escalation_message: typing.Optional[builtins.str] = None,
        evaluation_delay: typing.Optional[jsii.Number] = None,
        include_tags: typing.Optional[builtins.bool] = None,
        locked: typing.Optional[builtins.bool] = None,
        min_location_failed: typing.Optional[jsii.Number] = None,
        new_host_delay: typing.Optional[jsii.Number] = None,
        no_data_timeframe: typing.Optional[jsii.Number] = None,
        notify_audit: typing.Optional[builtins.bool] = None,
        notify_no_data: typing.Optional[builtins.bool] = None,
        renotify_interval: typing.Optional[jsii.Number] = None,
        require_full_window: typing.Optional[builtins.bool] = None,
        synthetics_check_id: typing.Optional[jsii.Number] = None,
        thresholds: typing.Optional["MonitorThresholds"] = None,
        threshold_windows: typing.Optional["MonitorThresholdWindows"] = None,
        timeout_h: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enable_logs_sample: Whether or not to include a sample of the logs.
        :param escalation_message: Message to include with a re-notification when renotify_interval is set.
        :param evaluation_delay: Time in seconds to delay evaluation.
        :param include_tags: Whether or not to include triggering tags into notification title.
        :param locked: Whether or not changes to this monitor should be restricted to the creator or admins.
        :param min_location_failed: Number of locations allowed to fail before triggering alert.
        :param new_host_delay: Time in seconds to allow a host to start reporting data before starting the evaluation of monitor results.
        :param no_data_timeframe: Number of minutes data stopped reporting before notifying.
        :param notify_audit: Whether or not to notify tagged users when changes are made to the monitor.
        :param notify_no_data: Whether or not to notify when data stops reporting.
        :param renotify_interval: Number of minutes after the last notification before the monitor re-notifies on the current status.
        :param require_full_window: Whether or not the monitor requires a full window of data before it is evaluated.
        :param synthetics_check_id: ID of the corresponding synthetics check.
        :param thresholds: The threshold definitions.
        :param threshold_windows: The threshold window definitions.
        :param timeout_h: Number of hours of the monitor not reporting data before it automatically resolves.
        '''
        if isinstance(thresholds, dict):
            thresholds = MonitorThresholds(**thresholds)
        if isinstance(threshold_windows, dict):
            threshold_windows = MonitorThresholdWindows(**threshold_windows)
        self._values: typing.Dict[str, typing.Any] = {}
        if enable_logs_sample is not None:
            self._values["enable_logs_sample"] = enable_logs_sample
        if escalation_message is not None:
            self._values["escalation_message"] = escalation_message
        if evaluation_delay is not None:
            self._values["evaluation_delay"] = evaluation_delay
        if include_tags is not None:
            self._values["include_tags"] = include_tags
        if locked is not None:
            self._values["locked"] = locked
        if min_location_failed is not None:
            self._values["min_location_failed"] = min_location_failed
        if new_host_delay is not None:
            self._values["new_host_delay"] = new_host_delay
        if no_data_timeframe is not None:
            self._values["no_data_timeframe"] = no_data_timeframe
        if notify_audit is not None:
            self._values["notify_audit"] = notify_audit
        if notify_no_data is not None:
            self._values["notify_no_data"] = notify_no_data
        if renotify_interval is not None:
            self._values["renotify_interval"] = renotify_interval
        if require_full_window is not None:
            self._values["require_full_window"] = require_full_window
        if synthetics_check_id is not None:
            self._values["synthetics_check_id"] = synthetics_check_id
        if thresholds is not None:
            self._values["thresholds"] = thresholds
        if threshold_windows is not None:
            self._values["threshold_windows"] = threshold_windows
        if timeout_h is not None:
            self._values["timeout_h"] = timeout_h

    @builtins.property
    def enable_logs_sample(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include a sample of the logs.'''
        result = self._values.get("enable_logs_sample")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def escalation_message(self) -> typing.Optional[builtins.str]:
        '''Message to include with a re-notification when renotify_interval is set.'''
        result = self._values.get("escalation_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_delay(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds to delay evaluation.'''
        result = self._values.get("evaluation_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def include_tags(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include triggering tags into notification title.'''
        result = self._values.get("include_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def locked(self) -> typing.Optional[builtins.bool]:
        '''Whether or not changes to this monitor should be restricted to the creator or admins.'''
        result = self._values.get("locked")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def min_location_failed(self) -> typing.Optional[jsii.Number]:
        '''Number of locations allowed to fail before triggering alert.'''
        result = self._values.get("min_location_failed")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def new_host_delay(self) -> typing.Optional[jsii.Number]:
        '''Time in seconds to allow a host to start reporting data before starting the evaluation of monitor results.'''
        result = self._values.get("new_host_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def no_data_timeframe(self) -> typing.Optional[jsii.Number]:
        '''Number of minutes data stopped reporting before notifying.'''
        result = self._values.get("no_data_timeframe")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notify_audit(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to notify tagged users when changes are made to the monitor.'''
        result = self._values.get("notify_audit")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notify_no_data(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to notify when data stops reporting.'''
        result = self._values.get("notify_no_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def renotify_interval(self) -> typing.Optional[jsii.Number]:
        '''Number of minutes after the last notification before the monitor re-notifies on the current status.'''
        result = self._values.get("renotify_interval")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_full_window(self) -> typing.Optional[builtins.bool]:
        '''Whether or not the monitor requires a full window of data before it is evaluated.'''
        result = self._values.get("require_full_window")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synthetics_check_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the corresponding synthetics check.'''
        result = self._values.get("synthetics_check_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def thresholds(self) -> typing.Optional["MonitorThresholds"]:
        '''The threshold definitions.'''
        result = self._values.get("thresholds")
        return typing.cast(typing.Optional["MonitorThresholds"], result)

    @builtins.property
    def threshold_windows(self) -> typing.Optional["MonitorThresholdWindows"]:
        '''The threshold window definitions.'''
        result = self._values.get("threshold_windows")
        return typing.cast(typing.Optional["MonitorThresholdWindows"], result)

    @builtins.property
    def timeout_h(self) -> typing.Optional[jsii.Number]:
        '''Number of hours of the monitor not reporting data before it automatically resolves.'''
        result = self._values.get("timeout_h")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.MonitorThresholdWindows",
    jsii_struct_bases=[],
    name_mapping={
        "recovery_window": "recoveryWindow",
        "trigger_window": "triggerWindow",
    },
)
class MonitorThresholdWindows:
    def __init__(
        self,
        *,
        recovery_window: typing.Optional[builtins.str] = None,
        trigger_window: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param recovery_window: How long an anomalous metric must be normal before recovering from an alert state.
        :param trigger_window: How long a metric must be anomalous before triggering an alert.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if recovery_window is not None:
            self._values["recovery_window"] = recovery_window
        if trigger_window is not None:
            self._values["trigger_window"] = trigger_window

    @builtins.property
    def recovery_window(self) -> typing.Optional[builtins.str]:
        '''How long an anomalous metric must be normal before recovering from an alert state.'''
        result = self._values.get("recovery_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_window(self) -> typing.Optional[builtins.str]:
        '''How long a metric must be anomalous before triggering an alert.'''
        result = self._values.get("trigger_window")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorThresholdWindows(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@nomadblacky/cdk-datadog-resources.MonitorThresholds",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "critical_recovery": "criticalRecovery",
        "o_k": "oK",
        "warning": "warning",
        "warning_recovery": "warningRecovery",
    },
)
class MonitorThresholds:
    def __init__(
        self,
        *,
        critical: typing.Optional[jsii.Number] = None,
        critical_recovery: typing.Optional[jsii.Number] = None,
        o_k: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[jsii.Number] = None,
        warning_recovery: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param critical: Threshold value for triggering an alert.
        :param critical_recovery: Threshold value for recovering from an alert state.
        :param o_k: Threshold value for recovering from an alert state.
        :param warning: Threshold value for triggering a warning.
        :param warning_recovery: Threshold value for recovering from a warning state.
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if critical is not None:
            self._values["critical"] = critical
        if critical_recovery is not None:
            self._values["critical_recovery"] = critical_recovery
        if o_k is not None:
            self._values["o_k"] = o_k
        if warning is not None:
            self._values["warning"] = warning
        if warning_recovery is not None:
            self._values["warning_recovery"] = warning_recovery

    @builtins.property
    def critical(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for triggering an alert.'''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def critical_recovery(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for recovering from an alert state.'''
        result = self._values.get("critical_recovery")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def o_k(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for recovering from an alert state.'''
        result = self._values.get("o_k")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for triggering a warning.'''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning_recovery(self) -> typing.Optional[jsii.Number]:
        '''Threshold value for recovering from a warning state.'''
        result = self._values.get("warning_recovery")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorThresholds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@nomadblacky/cdk-datadog-resources.MonitorType")
class MonitorType(enum.Enum):
    '''The type of the monitor.'''

    COMPOSITE = "COMPOSITE"
    EVENT_ALERT = "EVENT_ALERT"
    LOG_ALERT = "LOG_ALERT"
    METRIC_ALERT = "METRIC_ALERT"
    PROCESS_ALERT = "PROCESS_ALERT"
    QUERY_ALERT = "QUERY_ALERT"
    SERVICE_CHECK = "SERVICE_CHECK"
    SYNTHETICS_ALERT = "SYNTHETICS_ALERT"
    TRACE_ANALYTICS_ALERT = "TRACE_ANALYTICS_ALERT"


__all__ = [
    "DatadogCredentials",
    "DatadogDashboard",
    "DatadogDashboardProps",
    "DatadogDowntime",
    "DatadogDowntimeProps",
    "DatadogIAMUser",
    "DatadogIAMUserProps",
    "DatadogIntegrationAWS",
    "DatadogIntegrationAWSProps",
    "DatadogMonitor",
    "DatadogMonitorProps",
    "MonitorOptions",
    "MonitorThresholdWindows",
    "MonitorThresholds",
    "MonitorType",
]

publication.publish()
