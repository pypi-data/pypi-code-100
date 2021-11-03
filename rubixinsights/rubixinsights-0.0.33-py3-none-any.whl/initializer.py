import os
from collections import namedtuple
import datetime
import boto3
from typing import Optional, List
from .metadata import Metadata
from .secrets_engine import SecretsManager
from .helper import get_value_from_ssm, read_yaml


class Initializer:
    def __init__(self, 
                 channel: str, 
                 execution_date: datetime.date, 
                 business_key: List[str],
                 metadata_environment: str,
                 secrets_manager_environment: str, 
                 config_path='', 
                 aws_region_name='us-east-1'
        ):
        self.channel = channel
        self.execution_date = execution_date
        self.version = os.environ.get('version', 'v1')
        self.bk = namedtuple('BusinessKey', business_key)

        self.aws_region_name = aws_region_name
        self.ssm_client = boto3.client('ssm', region_name=aws_region_name)
        self.s3_client = boto3.client('s3', region_name=aws_region_name)

        self.config_path=config_path
        self.config = self.init_config()

        self.metadata = self.init_metadata_backend('prd')
        self.secrets_manager = self.init_secrets_backend('prd')

    def init_metadata_backend(self, environment: str):
        metadata = Metadata(
            host = get_value_from_ssm(f"/rubix/insights/{environment}/metadata/endpoint", self.ssm_client),
            port = get_value_from_ssm(f"/rubix/insights/{environment}/metadata/port", self.ssm_client),
            username = get_value_from_ssm(f"/rubix/insights/{environment}/metadata/username", self.ssm_client),
            password = get_value_from_ssm(f"/rubix/insights/{environment}/metadata/password", self.ssm_client),
            database = get_value_from_ssm(f"/rubix/insights/{environment}/metadata/database", self.ssm_client),
            data_source = self.channel
        )
        return metadata

    def init_secrets_backend(self, environment: str):
        secrets_manager = SecretsManager(
            host = get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/endpoint", self.ssm_client),
            port = get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/port", self.ssm_client),
            username = get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/username", self.ssm_client),
            password = get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/password", self.ssm_client),
            database = get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/database", self.ssm_client)
        )
        return secrets_manager

    def init_config(self) -> dict:
        if self.config_path != '':
            config = read_yaml(self.config_path)
            return config
        else:
            return {}
    
    @property
    def accounts(self) -> list:
        """ Get a list of accounts of this channel."""
        # TODO: get now from config file, later from a database table
        return self.config[self.channel]['accounts']
    
    @staticmethod
    def extract_components_from_execution_date(execution_date: datetime):
        year = execution_date.strftime("%Y")
        month = execution_date.strftime("%m")
        day = execution_date.strftime("%d")
        return year, month, day
    
    def get_s3_path(self, account: str, filename: str):
        s3_year, s3_month, s3_day = self.extract_components_from_execution_date(self.execution_date)
        return f"{self.channel}/{self.version}/{account}/{s3_year}/{s3_month}/{s3_day}/{filename}"