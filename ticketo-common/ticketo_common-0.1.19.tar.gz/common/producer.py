import json

import boto3
from django.conf import settings


class Sqs:
    @classmethod
    def publish(cls, topic_name, body):
        sns_client_options = {
            "region_name": settings.AWS_REGION_NAME,
            "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
            "endpoint_url": settings.AWS_SNS_ENDPOINT_URL,
        }
        sns_client = boto3.client("sns", **sns_client_options)
        sns_client.publish(
            TopicArn=settings.AWS_TOPIC_ARN_BASE + topic_name,
            Subject=topic_name,
            Message=json.dumps(body),
        )
