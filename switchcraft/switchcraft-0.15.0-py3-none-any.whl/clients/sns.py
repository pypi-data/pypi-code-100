"""SNS Client.

A light-weight client for the Simple Notification System API.
"""

import logging
import json

import boto3
from botocore.exceptions import ClientError


log = logging.getLogger(__name__)


class SNSClient:
    def __init__(self) -> None:
        self.sns = boto3.client('sns')

    def publish(self, arn: str, subject: str, message: dict):
        try:
            resp = self.sns.publish(
                TopicArn=arn,
                Subject=subject,
                Message=json.dumps({'default': json.dumps(message)}),
                MessageStructure='json'
            )
            return resp
        except ClientError as err:
            log.error(
                f'Error occurred while publishing Alert message to SNS: {err}'
            )
            raise err
