from typing import Any
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

from .constants import REGION_NAME

def get_secret(secretId: str, regionName=REGION_NAME) -> Any:
    """Returns secret from SecretsManager in region."""
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=regionName
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secretId
        )
    except ClientError as e:
        raise e
    secret = get_secret_value_response['SecretString']

    return secret

def get_offender(offId, identifier, reason, expire_days=1, region=None) -> dict:
    """Returns offender dict with needed parameters."""
    times = get_report_times(expire_days)
    reportTime = times['reportTime']
    expireTime = times['expireTime']
    offender = {'_id': offId,
                'region': region,
                'identifier': identifier,
                'reason':  reason,
                'reportTime': reportTime,
                'expireTime': expireTime
            }

    return offender

def get_report_times(expire_days=1) -> dict[str:Any]:
    """Returns dict with human-readable reportTime and expireTime(POSIX) as a keys."""
    now = datetime.utcnow()
    return {
        'reportTime': str(now),
        'expireTime': int((now + timedelta(days=expire_days)).timestamp())
    }
        