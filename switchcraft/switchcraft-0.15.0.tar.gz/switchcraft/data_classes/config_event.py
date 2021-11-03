"""Config Event.

Data Class representing AWS Config Events.
"""

import json
from typing import Any, Dict, Optional

from switchcraft.data_classes.base import DictWrapper


class ConfigInvokingEvent(DictWrapper):
    @property
    def account_id(self) -> str:
        """Returns the account id of the account where the event originated."""
        return self['awsAccountId']

    @property
    def notification_creation_time(self) -> str:
        """Returns a timestamp representing the creation date/time."""
        return self['notificationCreationTime']

    @property
    def message_type(self) -> str:
        """Returns the type of the AWS Config message."""
        return self['messageType']


class ConfigEvent(DictWrapper):
    """An AWS Config Scheduled Event."""

    @property
    def invoking_event(self) -> ConfigInvokingEvent:
        """Returns a ConfigInvokingEvent object.

        This object contains details about the Config event that was
        invoked.
        """
        return ConfigInvokingEvent(json.loads(self['invokingEvent']))

    @property
    def rule_parameters(self) -> Optional[Dict[str, Any]]:
        """Returns a dictionary containing rule parameters.

        This is an optional field that only gets generated when an AWS
        Config Rule contains parameters.
        """
        rule_parameters = self.get('ruleParameters')
        return None if rule_parameters is None else json.loads(rule_parameters)

    @property
    def result_token(self) -> str:
        """Returns a result token.

        Result tokens ensure that results for the originating event can
        easily be returned to the AWS Config service.
        """
        return self['resultToken']

    @property
    def event_left_scope(self) -> bool:
        """Indicates if the AWS resource to be evaluated has been removed from
        the rule's scope.

        If the value is true, the function indicates that the evaluation
        can be ignored by passing NOT_APPLICABLE as the value for the
        ComplianceType attribute in the PutEvaluations call.
        """
        return self['eventLeftScope']

    @property
    def execution_role_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the role used to execute the
        rule."""
        return self['executionRoleArn']

    @property
    def config_rule_arn(self) -> str:
        """The Amazon Resource Name (ARN) of the AWS Config Rule."""
        return self['configRuleArn']

    @property
    def config_rule_name(self) -> str:
        """Returns the name of the AWS Config Rule."""
        return self['configRuleName']

    @property
    def config_rule_id(self) -> str:
        """Returns the ID of the AWS Config Rule."""
        return self['configRuleId']

    @property
    def account_id(self) -> str:
        """Returns the AWS Account ID."""
        return self['accountId']
