"""
Base DynamoDB streams Lambda application
"""
from aws_lambda_powertools.utilities.data_classes import DynamoDBStreamEvent
from spine_aws_common.batch_application import BatchApplication


class DynamoDBStreamsApplication(BatchApplication):
    """
    Base class for SQS Lambda applications
    """

    EVENT_TYPE = DynamoDBStreamEvent
