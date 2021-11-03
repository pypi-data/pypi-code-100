import logging
import boto3
from sqlalchemy import create_engine
from .helper import get_value_from_ssm
import requests
import json
from loguru import logger

# AWS Credential
AWS_REGION = 'us-east-1'
# Channel Analytics
ANALYTICS_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
SHOPIFY_API_VERSION = '2021-01'


class SecretsManager:
    client = boto3.client('ssm', region_name=AWS_REGION)

    # refactor this into a connection object
    def __init__(self, host: str, port: str, username: str, password: str, database: str):
        self.connection_string = self._create_connection_string(host, port, username, password, database)
        self.engine = create_engine(self.connection_string)
        self.conn = None

    def _create_connection_string(self, host: str, port: str, username: str, password: str, database: str):
        return f"postgres://{username}:{password}@{host}:{port}/{database}"

    def _get_connection(self):
        """Create a singleton connection object."""
        if self.conn is None:
            self.conn = self.engine.connect()
        return self.conn

    def get_facebook_act_ids(self):
        channel = 'facebook'
        sql_statement = f"""
            -- choose the latest if multiple apply
            SELECT distinct ad_object_id
            FROM {channel}_integration
        """
        logger.info("Fetching all act_ids for channel facebook")
        logger.debug(sql_statement)
        results = self._get_connection().execute(sql_statement)
        act_ids = [result[0] for result in results]
        return act_ids

    def get_facebook_access_token(self, id: str):
        if not id.startswith("act_"):
            act_id = f"act_{id}"
        else:
            act_id = id

        channel = "facebook"
        sql_statement = f"""
            -- choose the latest if multiple apply
            SELECT access_token
            FROM {channel}_integration
            where ad_object_id = '{act_id}'
            order by created_at desc
      """
        logger.debug(sql_statement)
        try:
            results = self._get_connection().execute(sql_statement)
            access_tokens = [result[0] for result in results]
            if len(access_tokens) > 1:
                logger.warning("channel: {channel}, id: {id} has more than 1 secrets in the database")
            access_token = access_tokens[0]
            return access_token
        except Exception as e:
            logger.exception(f"Problem get {channel} credential for account: {id}")
            raise e

    def _adwords_get_refresh_token(self, id):
        channel = "adwords"
        sql_statement = f"""
            -- choose the latest if multiple apply
            SELECT refresh_token
            FROM {channel}_integrations
            where customer_id = '{id}'
            order by created_at desc
      """
        print(sql_statement)
        try:
            results = self._get_connection().execute(sql_statement)
            refresh_tokens = [result[0] for result in results]
            if len(refresh_tokens) > 1:
                logging.warning("channel: {channel}, id: {id} has more than 1 secrets in the database")
                refresh_token = refresh_tokens[0]
            return refresh_token
        except Exception as e:
            logger.exception(f"Problem get {channel} credential for account: {id}")
            raise e

    def _shopify_get_access_token(self, id):
        channel = 'shopify'
        sql_statement = f"""
            -- choose the latest if multiple apply
            SELECT access_token
            FROM {channel}_integrations
            where shop_name = '{id}'
            order by created_at desc
      """
        print(sql_statement)
        try:
            results = self._get_connection().execute(sql_statement)
            tokens = [result[0] for result in results]
            if len(tokens) > 1:
                logging.warning("channel: {channel}, id: {id} has more than 1 secrets in the database")
                token = tokens[0]
            return token
        except Exception as e:
            logger.exception(f"Problem get {channel} credential for account: {id}")
            raise e


if __name__ == '__main__':
    host = 'localhost'
    port = '5432'
    username = 'postgres'
    password = 'postgres'
    database = 'postgres'
    secrets_manager = SecretsManager(host=host, port=port, username=username, password=password, database=database)
    print(secrets_manager.get_facebook_act_ids())
    print([secrets_manager.get_facebook_access_token(act_id) for act_id in secrets_manager.get_facebook_act_ids()])

# @staticmethod
# def _facebook_get_client_id(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/facebook/CLIENT_ID", client)

# @staticmethod
# def _facebook_get_client_secret(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/facebook/CLIENT_SECRET", client)

# @staticmethod
# def _adwords_get_client_id(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/adwords/CLIENT_ID", client)

# @staticmethod
# def _adwords_get_client_secret(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/adwords/CLIENT_SECRET", client)

# @staticmethod
# def _adwords_get_developer_token(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/adwords/DEVELOPER_TOKEN", client)

# def get_credential(self, channel, id, environment):
#     """Get Credential."""
#     if channel == 'analytics':
#         credential = self._analytics_get_credential(id)
#     if channel == 'facebook':
#         credential = {}
#         credential['access_token'] = self._facebook_get_access_token(id)
#         credential['app_id'] = self._facebook_get_client_id(self.client, environment)
#         credential['app_secret'] = self._facebook_get_client_secret(self.client, environment)
#     if channel == 'adwords':
#         credential = {}
#         credential['client_id'] = self._adwords_get_client_id(self.client, environment)
#         credential['client_secret'] = self._adwords_get_client_secret(self.client, environment)
#         credential['developer_token'] = self._adwords_get_developer_token(self.client, environment)
#         credential['refresh_token'] = self._adwords_get_refresh_token(id)
#     if channel == 'shopify':
#         import shopify
#         credential = {}
#         shop_url = f"{id}.myshopify.com"
#         access_token = self._shopify_get_access_token(id)
#         session = shopify.Session(shop_url, SHOPIFY_API_VERSION, access_token)
#         credential['session'] = session
#     return credential

# @staticmethod
# def _analytics_get_client_id(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/analytics/CLIENT_ID", client)

# @staticmethod
# def _analytics_get_client_secret(client, environment):
#     return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/analytics/CLIENT_SECRET", client)

# @classmethod
# def _analytics_get_access_token(cls, refresh_token):
#     client_id = cls._analytics_get_client_id(cls.client, "prd")
#     client_secret = cls._analytics_get_client_secret(cls.client, "prd")
#     grant_type = "refresh_token"
#     payload = {
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'refresh_token': refresh_token,
#         'grant_type': grant_type
#     }

#     headers = {'content-type': 'application/x-www-form-urlencoded'}
#     # 'https://oauth2.googleapis.com/token',
#     response = requests.post(
#         cls.ANALYTICS_TOKEN_URI,
#         data=payload,
#         headers=headers
#     )
#     access_token = json.loads(response.text)['access_token']
#     return access_token

# def _analytics_get_credential(self, id: str) -> str:
#     # current take the latest strategy
#     # TODO:
#     channel = "analytics"
#     sql_statement = f"""
#       -- choose the latest if multiple apply
#       SELECT refresh_token
#       FROM {channel}_integrations
#       where account_id = '{id}'
#       order by created_at desc
#   """
#     print(sql_statement)
#     try:
#         results = self._get_connection().execute(sql_statement)
#         refresh_tokens = [result[0] for result in results]
#         if len(refresh_tokens) > 1:
#             logging.warning(f"channel: {channel}, id: {id} has more than 1 secrets in the database")
#         refresh_token = refresh_tokens[0]
#         access_token = self._analytics_get_access_token(refresh_token)
#         credential = google.oauth2.credentials.Credentials(
#             access_token,
#             refresh_token=refresh_token,
#             token_uri=self.ANALYTICS_TOKEN_URI,
#             client_id=self._analytics_get_client_id(self.client, "prd"),
#             client_secret=self._analytics_get_client_secret(self.client, "prd")
#         )
#         return credential
#     except Exception as e:
#         logging.exception(f"Problem get {channel} credential for account: {id}")
#         raise e


#   @staticmethod
#   def _shopify_get_client_id(client, environment):
#       """API Key."""
#       return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/shopify/CLIENT_ID", client)

#   @staticmethod
#   def _shopify_get_client_secret(client, environment):
#       return get_value_from_ssm(f"/rubix/insights/{environment}/secrets_engine/shopify/CLIENT_SECRET", client)
