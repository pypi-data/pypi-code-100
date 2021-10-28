import boto3
from datetime import datetime
import hashlib
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
s3 = boto3.resource('s3')


def hashing(s):
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**8


# DynamoDB
def _create_dynamodb_table(table_name, partition_key, sort_key=None):
    attribute_definition = [
        {
            'AttributeName': partition_key,
            'AttributeType': 'S',
        }
    ]
    key_schema = [
                    {
                        'AttributeName': partition_key,  # 20211231
                        'KeyType': 'HASH',  # partition key
                    },
    ]
    if sort_key:
        # docs: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.NamingRulesDataTypes.html
        attribute_definition.append(
            {
                'AttributeName': sort_key,  # format : 2015-12-21T17:42:34Z
                'AttributeType': 'S',
            }
        )
        key_schema.append(
            {
                'AttributeName': sort_key,
                'KeyType': 'RANGE',  # sort key
            }
        )

    try:
        table = dynamodb.create_table(
                TableName=table_name,
                AttributeDefinitions=attribute_definition,
                KeySchema=key_schema,
                BillingMode='PAY_PER_REQUEST',
            )

        # Wait until the table exists.
        table.wait_until_exists()

    except ClientError as e:
        print('dynamodb.create_table():', e)
        return

    return table


def _get_or_create_metadata_table(table_name):
    if table_name not in [table.name for table in dynamodb.tables.all()]:
        table = _create_dynamodb_table(table_name, partition_key="date", sort_key="timestamp")
    else: 
        table = dynamodb.Table(table_name)
    return table


def _get_or_create_state_table(table_name):
    if table_name not in [table.name for table in dynamodb.tables.all()]:
        table = _create_dynamodb_table(table_name, partition_key="consumer")
    else: 
        table = dynamodb.Table(table_name)
    return table


# S3
def _create_s3_bucket(bucket_name, region):
    # Create bucket
    try:
        bucket = s3.create_bucket(
            ACL='private',
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': region
            }
        )
    except ClientError as e:
        print('s3.create_bucket():', e)
        return None
    return bucket

    
def str_to_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')

# metadata >>  n table
#     partition >> date
#     sortkey >> sortkey : timestamp + batch_id

# status-progress >> only 1 table
#     partition >> location-tiger-invoice , location-thaipost-invoice, matching-tiger-invoice
#     sortkey >> datetime
#     field >> 
#         - sortkey : timestamp + batch_id
