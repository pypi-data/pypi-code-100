"""DynamoDB Client.

Provides a client for DynamoDB.
"""

import logging

import boto3

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


log = logging.getLogger(__name__)


class DynamoDBClient:

    def __init__(self, table_name: str, hash_key: str = None):
        self.dynamodb = boto3.resource('dynamodb')

        try:
            self.hash_key = hash_key
            self.table = self.dynamodb.Table(table_name)
        except ClientError as err:
            log.error(err)
            raise

    def get_item(
        self,
        partition_key_value: str,
        consistent_read: bool = True
    ) -> dict:
        log.debug(
            f'Querying table "{self.table.table_name}" for item with '
            f'hash value {partition_key_value}'
        )
        try:
            return self.table.get_item(
                Key={self.hash_key: partition_key_value},
                ConsistentRead=consistent_read
            )
        except ClientError as err:
            log.error(err)
            raise

    def put_item(self, item: dict, condition_expression: Attr = None):
        try:
            hash_value = item.get(self.hash_key)
            log.debug(
                f'Putting item with hash value "{hash_value}" into '
                f'{self.table}'
            )
            args = {'Item': item}
            if condition_expression:
                args['ConditionExpression'] = condition_expression

            return self.table.put_item(**args)
        except (ClientError, KeyError) as err:
            log.error(err)
            raise

    def delete_item(self, partition_key_value: str):
        try:
            log.info(
                f'Deleting item with hash value "{partition_key_value}" '
                f'from {self.table}'
            )
            return self.table.delete_item(
                Key={self.hash_key: partition_key_value}
            )
        except ClientError as err:
            log.error(err)
            raise

    def scan(self, limit=None):
        log.info(f'Scanning table: {self.table.table_name}')
        try:
            scan_args = {
                'Select': 'ALL_ATTRIBUTES'
            }

            response = self.table.scan(**scan_args)
            data = response.get('Items')

            while 'LastEvaluatedKey' in response:
                if limit and len(data) >= limit:
                    break

                scan_args['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = self.table.scan(**scan_args)
                data.extend(response.get('Items'))

            if limit:
                data = data[:limit]
                log.warning(
                    f'A limit has been set - only {limit} '
                    f'items(s) will be retrieved.'
                )
            log.info(f'Retrieved {len(data)} item(s)')
            return data
        except ClientError as err:
            log.error(err)
            raise
