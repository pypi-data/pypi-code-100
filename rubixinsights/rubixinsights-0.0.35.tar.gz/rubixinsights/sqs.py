import json


def get_sqs_messages(context):
    messages = context['task_instance'].xcom_pull(key='messages', task_ids='listen_to_s3')['Messages']
    for message in messages:
        receipt_handle = message['ReceiptHandle']
        records = json.loads(message['Body'])['Records']
        for record in records:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            print(f"ReceiptHandle: {receipt_handle}  Bucket: {bucket}  Key: {key}")
            yield receipt_handle, bucket, key
