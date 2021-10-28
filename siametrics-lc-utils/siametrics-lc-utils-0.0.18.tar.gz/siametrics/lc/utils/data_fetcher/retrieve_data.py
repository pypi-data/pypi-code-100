import boto3
from boto3.dynamodb.conditions import Key
from datetime import timedelta, datetime

from .settings import settings
from .utils import _get_or_create_metadata_table, _get_or_create_state_table, str_to_datetime


region = settings.AWS_REGION
dynamodb_state_table_name = settings.DYNAMODB_STATE_TABLE_NAME+'-'+settings.ENVIRONMENT
bucket_name = settings.S3_BUCKET_NAME

dynamodb = boto3.resource('dynamodb', endpoint_url=f"https://dynamodb.{region}.amazonaws.com")
s3 = boto3.resource('s3', endpoint_url=f"https://s3.{region}.amazonaws.com")


def _get_latest_processed_timestamp(consumer):
    # get from state table (dynamo)

    table = _get_or_create_state_table(dynamodb_state_table_name)
    response = table.get_item(
        Key={
            'consumer': consumer 
        },
        ConsistentRead=True
    )
    if 'Item' not in response:
        return None
    
    return response["Item"]["latest_processed_timestamp"]


def _update_latest_processed_timestamp(consumer, latest_timestamp):
    table = _get_or_create_metadata_table(dynamodb_state_table_name)
    item = {
        "consumer": consumer,
        'latest_processed_timestamp': latest_timestamp
    }
    _ = table.put_item(Item=item)


def _get_metadata_from_dynamodb(data_source, latest_timestamp):
    """
    query dynamodb to get location (bucket_name, file_name) of one batch data after input timestamp
    get from meta-data tables (dynamo)
    """

    table = _get_or_create_metadata_table(data_source)
    print('table status :', table.table_status)

    if latest_timestamp is None:  # haven't processed any job yet
        print("start scan dynamo table")
        response = table.scan(
            ProjectionExpression="#dt, #ts, s3_location.bucket_name, s3_location.file_name",
            ExpressionAttributeNames={"#dt": "date", "#ts": "timestamp"},
            ConsistentRead=True,
        )
        print(response.keys())
        if "Items" in response:
            # print(response)
            job = None
            for item in response["Items"]:
                if job is None:
                    job = item
                else:
                    dt = datetime.strptime(item["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
                    if dt < datetime.strptime(job["timestamp"], '%Y-%m-%d %H:%M:%S.%f'):
                        job = item          
            # job = min(map(to_datetime, response['Items']))
            return {
                "bucket_name": job["s3_location"]["bucket_name"], 
                "file_name": job["s3_location"]["file_name"],
                "timestamp": job["timestamp"]
            }
        
    else:
        # date = datetime.strptime(latest_timestamp, '%Y-%m-%d %H:%M:%S.%f').date()
        date = str_to_datetime(latest_timestamp).date()
        while date <= datetime.now().date():
         
            response = table.query(
                ProjectionExpression="#dt, #ts, s3_location.bucket_name, s3_location.file_name", 
                ExpressionAttributeNames={"#dt": "date", "#ts": "timestamp"},
                KeyConditionExpression=Key('date').eq(str(date)) & Key('timestamp').gt(latest_timestamp),
                ScanIndexForward=True,
                ConsistentRead=True,
                Limit=1
            )
            print("response['Items']: ", response["Items"])
            if response["Items"]:
                return {
                    "bucket_name": response["Items"][0]["s3_location"]["bucket_name"], 
                    "file_name": response["Items"][0]["s3_location"]["file_name"],
                    "timestamp": response["Items"][0]["timestamp"],
                }

            date += timedelta(days=1)
        return None


def _get_one_batch_after_timestamp(data_source, latest_timestamp):
    """
    get from S3
    """

    metadata = _get_metadata_from_dynamodb(data_source, latest_timestamp)
    if metadata is None:
        return None, None, None, None

    batch = s3.Object(metadata["bucket_name"], metadata["file_name"]).get()['Body'].read()
    return batch, metadata["timestamp"], metadata['file_name'], metadata
    

def start_processor(process, consumer, data_source):
    latest_timestamp = _get_latest_processed_timestamp(f'{consumer}-{data_source}')  # from state
    while True:
        print('latest_timestamp before : ', latest_timestamp)
        batch, latest_timestamp, file_name, metadata = _get_one_batch_after_timestamp(data_source, latest_timestamp)
        print('latest_timestamp after : ', latest_timestamp)
        if batch is None:
            print("batch is None")
            return
        process(batch, latest_timestamp, file_name, metadata)
        _update_latest_processed_timestamp(f'{consumer}-{data_source}', latest_timestamp)
