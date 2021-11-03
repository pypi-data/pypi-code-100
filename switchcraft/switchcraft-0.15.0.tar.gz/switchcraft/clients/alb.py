"""ALB Client.

A light-weight client for the Application Load Balancer API.
"""

import logging
import boto3
from botocore.exceptions import ClientError
from typing import Generator

log = logging.getLogger(__name__)


class AlbClient:
    def __init__(self):
        self.albv2 = boto3.client('elbv2')

    def list_albs(self, **kwargs) -> Generator[dict, None, None]:
        """Yields a generator containing roles.

        :param kwargs: arguments to pass to the underlying API call.
        :return: generator of IAM roles.
        """
        paginator = self.albv2.get_paginator('describe_load_balancers')

        for page in paginator.paginate(**kwargs):
            yield from page.get('LoadBalancers')

    def get_alb_attributes(self, arn: str):
        try:
            resp = self.albv2.describe_load_balancer_attributes(
                LoadBalancerArn=arn
            )
            return resp
        except ClientError as err:
            log.error(
                f'Error occurred while getting attributes for {arn}: {err}'
            )
            raise err
