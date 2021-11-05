import os

from botocore.client import Config


REGION_NAME = os.environ.get("AWS_REGION")

# Default boto3 config, will prevent long timeouts
BOTO3_CONFIG = Config(connect_timeout=5, retries={"max_attempts": 10})
