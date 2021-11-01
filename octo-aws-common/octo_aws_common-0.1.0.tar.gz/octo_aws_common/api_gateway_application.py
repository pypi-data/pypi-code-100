"""
Base API Gateway Lambda application
"""
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from octo_aws_common.web_application import WebApplication


class APIGatewayApplication(WebApplication):
    """
    Base class for API Gateway Lambda applications
    """

    EVENT_TYPE = APIGatewayProxyEvent
