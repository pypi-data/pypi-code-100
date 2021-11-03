from loguru import logger
from sqlalchemy import create_engine
import pandas as pd
import requests
import json
from provider import Provider

mockup_all_datastreams = None


class DataStreamControllerBase:
    """Base Class of Data Streams
    """

    def __init__(self, provider: Provider, template: dict, connection_string):
        self.provider = provider
        self.template = template
        self.engine = create_engine(connection_string)

    def get_headers(self):
        token = self.provider.get_token()
        return {
            'Authorization': f"Token {token}",
            'Content-Type': 'application/json'
        }

    def get_metadata(self):
        pass

    def get_datastream_id(self):
        """Retrieve datastream id from name
        """
        pass

    def get_all_datastreams(self, environment: str):
        """Get all datastreams in environment

        :param environment: valid value is dev and prd
        :type environment: str
        """
        # https://rubix.datatap.adverity.com/api/datastreams/
        url = f"https://rubix.datatap.adverity.com/api/datastream-types/"
        headers = self.get_headers()
        logger.debug(url)
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        return data

    def create(self, stack: int, auth: str, name: str):
        """Create a data stream in workspace

        :param stack: adverity workspace id
        :type stack: int
        :param auth: adverity connection id
        :type auth: str
        :param name: data stream name
        :type name: str
        """
        data = {**self.template, **{'stack': stack, 'auth': auth, 'name': name}}
        headers = self.get_headers()
        url = f"https://rubix.datatap.adverity.com/api/datastream-types/{self.datastream_type_id}/datastreams/"
        logger.debug(url)
        logger.debug(data)
        logger.debug(headers)
        response = requests.post(url, json=data, headers=headers)
        logger.info(response.text)

    def enable_datastream(self, datastream_id: int):
        """Enable a data stream

        :param datastream_id: data stream id
        :type datastream_id: int
        """
        url = f"https://rubix.datatap.adverity.com/api/datastreams/{datastream_id}/"
        headers = self.get_headers()
        logger.debug(url)
        data = {
            "enabled": True
        }
        response = requests.patch(url, json=data, headers=headers)
        logger.info(response.text)

    def delete(self, datastream_id: int):
        """Delete a data stream

        :param datastream_id: data stream id
        :type datastream_id: int
        """
        url = f"https://rubix.datatap.adverity.com/api/datastream-types/{self.datastream_type_id}/datastreams/{datastream_id}/"
        headers = self.get_headers()
        logger.debug(url)
        data = {
            "enabled": True
        }
        response = requests.delete(url, json=data, headers=headers)
        logger.info(response.text)

    def apply(self):
        # get metadata from database
        metadata = pd.read_sql_query(
            "select * from adverity.metadata_datastream_controller",
            engine=self.engine
        )
        # get existing datastream

        # create data streams which does not exist
        # delete data streams which is redundant
        pass
