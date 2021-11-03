"""S3 Client.

This module provides a simple client for interacting with the
'S3' API.
"""

import json
import logging
import sys
from pathlib import PurePath

import boto3
from botocore.exceptions import ClientError

log = logging.getLogger()


class S3Client:
    def __init__(self, client=None):
        """Init."""
        if not client:
            self.s3_client = boto3.client('s3')

    def read_json(self, bucket_name, object_name):
        """Streams a JSON file from S3.

        Returns a dict containing the contents of the S3 object.
        """
        try:
            log.info(
                f'Getting {PurePath(object_name).name} from '
                f'{bucket_name}/{PurePath(object_name).parent} S3 bucket'
            )
            s3_object = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=object_name
            )
            data = s3_object['Body'].read().decode('utf-8')

            return json.loads(data)

        except ClientError as exc:
            log.error(f'Error while retrieving file: {exc}')
            sys.exit(1)
