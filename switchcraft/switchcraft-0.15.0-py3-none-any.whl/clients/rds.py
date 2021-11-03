"""RDS Client.

Provides a client for RDS.
"""

import logging

from typing import Generator

import boto3


log = logging.getLogger(__name__)


class RDSClient:
    def __init__(self):
        self.rds = boto3.client('rds')

    def list_db_instances(self, **kwargs) -> Generator[dict, None, None]:
        """Yields a generator containing db instances.

        :param kwargs: arguments to pass to the underlying API call.
        :return: generator of RDS DB Instances.
        """

        paginator = self.rds.get_paginator('describe_db_instances')

        for page in paginator.paginate(**kwargs):
            yield from page.get('DBInstances')
