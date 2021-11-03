"""STS Client.

A client that enables STS Assume Role.
"""

import logging
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)


class STSClient:
    def __init__(self):
        self.sts = boto3.client('sts')

    @staticmethod
    def get_role_credentials(
        role_name: str,
        account: str,
        session_prefix: str
    ) -> Dict[str, Any]:
        sts = boto3.client('sts')
        partition = sts.get_caller_identity()['Arn'].split(":")[1]
        role_session_name = f'{session_prefix}-session-{account}'
        log.debug(f'Role Session Name: {role_session_name}')
        role_arn = f'arn:{partition}:iam::{account}:role/{role_name}'

        try:
            resp = sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName=role_session_name
            )
            return resp.get('Credentials')
        except ClientError as err:
            log.warning(f'Unable to get credentials - {err}')
            return {}
