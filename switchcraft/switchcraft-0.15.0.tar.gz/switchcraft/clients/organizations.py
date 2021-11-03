"""Organization Client.

This module provides a simple client for interacting with the
'Organizations' API.
"""

import logging

import boto3

from botocore.exceptions import ClientError


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class OrganizationClient:
    def __init__(self, role_arn: str = None):
        if role_arn:
            self.credentials = self.__get_role_credentials(role_arn)
            self.organization = boto3.client(
                'organizations',
                aws_access_key_id=self.credentials.get('AccessKeyId'),
                aws_secret_access_key=self.credentials.get('SecretAccessKey'),
                aws_session_token=self.credentials.get('SessionToken')
            )
        else:
            self.organization = boto3.client('organizations')

    @property
    def id(self) -> str:
        try:
            org = self.organization.describe_organization().get('Organization')
            return org.get('Id')
        except ClientError as err:
            log.error(err)
            raise

    def scan_org(self, **kwargs):
        paginator = self.organization.get_paginator('list_accounts')
        for page in paginator.paginate(**kwargs):
            yield from page.get("Accounts")

    def get_accounts(self) -> list:
        accounts = self.scan_org()
        account_ids = [account.get('Id') for account in accounts]
        return account_ids

    @staticmethod
    def __get_role_credentials(role_arn) -> dict:
        sts = boto3.client('sts')
        role_session_name = 'organizations-session'

        resp = sts.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name
        )
        return resp.get('Credentials')
