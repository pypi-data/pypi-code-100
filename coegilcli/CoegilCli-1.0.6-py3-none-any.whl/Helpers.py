from typing import IO
from io import BytesIO
import boto3


def put_s3_object(bucket, key, body: IO, content_type: str = None, credential_override=None):
    client = _get_client('s3', credential_override)
    if isinstance(body, str):
        body = str.encode(body)
    if isinstance(body, bytes):
        body = BytesIO(body)
    params = {
        'ACL': 'private'
    }
    if content_type is not None:
        params['ContentType'] = content_type
    client.upload_fileobj(body, bucket, key, params)


def get_s3_object(bucket, key, credential_override=None) -> bytes:
    client = _get_client('s3', credential_override)
    return client.get_object(
        Bucket=bucket,
        Key=key
    ).get('Body').read()


def _get_client(name, credential_override):
    if credential_override is None:
        return boto3.client(name)
    else:
        params = {
            'aws_access_key_id': credential_override['AccessKeyId'],
            'aws_secret_access_key': credential_override['SecretAccessKey'],
        }
        session_token = credential_override.get('SessionToken')
        if session_token is not None:
            params['aws_session_token'] = session_token
        session = boto3.Session(**params)
        client = session.client(name)
        return client
