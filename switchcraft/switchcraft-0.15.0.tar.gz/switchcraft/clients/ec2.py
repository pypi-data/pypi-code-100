"""EC2 Client.

A light-weight client for the EC2 API.
"""

import logging

import boto3
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)


class EC2Client:
    def __init__(self) -> None:
        self.ec2 = boto3.client('ec2')

    def get_public_images(self) -> list:
        """Returns a list of public Images."""

        try:
            resp = self.ec2.describe_images(
                Filters=[
                    {
                        'Name': 'is-public',
                        'Values': [
                            'true'
                        ]
                    }
                ],
                Owners=[
                    'self'
                ]
            )
            images = resp.get('Images')
            if images:
                image_ids = [image.get('ImageId') for image in images]
                log.info(f'Public images found: {image_ids}')
                return image_ids
            else:
                log.info('No public images were found')
                return list()
        except ClientError as err:
            log.error(f'Error while describing images: {err}')
            raise err
