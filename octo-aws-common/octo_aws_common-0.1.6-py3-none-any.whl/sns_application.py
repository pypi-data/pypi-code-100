"""
Base SNS Lambda application
"""
from aws_lambda_powertools.utilities.data_classes import SNSEvent
from octo_aws_common.batch_application import BatchApplication


class SNSApplication(BatchApplication):
    """
    Base class for SNS Lambda applications
    """

    EVENT_TYPE = SNSEvent
