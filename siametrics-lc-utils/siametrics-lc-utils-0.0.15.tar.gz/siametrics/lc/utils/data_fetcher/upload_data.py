import boto3
from datetime import datetime
from .settings import settings
from .utils import _get_or_create_metadata_table, _create_s3_bucket

region = settings.AWS_REGION
bucket_name = settings.S3_BUCKET_NAME
dynamo_state_table_name = settings.DYNAMODB_STATE_TABLE_NAME

dynamodb = boto3.resource('dynamodb', endpoint_url=f"https://dynamodb.{region}.amazonaws.com")
s3 = boto3.resource('s3', endpoint_url=f"https://s3.{region}.amazonaws.com")


def _upload_metadata(data_type, source_company, item):
    """
    - check whether the table exists ? then create accordingly
    - create of update item to the table (make sure the item object has "date", "timestamp")
    """
    # get or create table
    table_name = f'{data_type}-{source_company}'
    table = _get_or_create_metadata_table(table_name)
    _ = table.put_item(Item=item)
    

def _upload_data_to_s3(object_in, filename):
    if bucket_name not in [bucket.name for bucket in s3.buckets.all()]:
        _ = _create_s3_bucket(bucket_name=bucket_name, region=settings.AWS_REGION)
    obj = s3.Object(bucket_name, filename)
    response = obj.put(Body=object_in)
    
    return response


def upload_to_datalake(object_in, data_type, source_company, file_name):
    # upload object to S3
    now = datetime.now()
    date = now.date()
    # uid = hashing(now)
    # ts = int(now.timestamp() * 1000)

    key = f"{source_company}-{data_type}/{file_name}"
    _ = _upload_data_to_s3(object_in, key)

    # upload meta data to DynamoDB
    item = {
        "date": str(date),
        "timestamp": str(now),
        'upload_duration': str(datetime.now() - now),
        's3_location': {
            "bucket_name": bucket_name,
            "file_name": key
        }
    }
    _upload_metadata(data_type, source_company, item)
