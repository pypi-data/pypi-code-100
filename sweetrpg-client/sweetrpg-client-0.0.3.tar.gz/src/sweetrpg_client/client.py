# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Client.
"""

import logging

import requests
from sweetrpg_client import constants
from sweetrpg_client.exceptions import UnknownDataType, NotFound, UnexpectedResponse
from sweetrpg_client.types import *
from sweetrpg_client.types.registry import _types
from sweetrpg_model_core.model.base import Model


class Client(object):
    """

    """

    def __init__(self, base_url: str, access_token: str = None, register_default_types: bool = True):
        """

        :param str base_url:
        :param str access_token:
        :param bool register_default_types:
        """
        self.base_url = base_url
        self.access_token = access_token
        self.data_types = {}
        if register_default_types:
            for k, v in _types.items():
                self.register_type(k, v)

    def register_type(self, name: str, type_info: dict):
        """

        :param str name:
        :param dict type_info:
        :return None:
        """
        self.data_types[name] = type_info

    def get(self, data_type: str, id: str) -> Model:
        """

        :param str data_type:
        :param str id:
        :return Model:
        """
        logging.debug("Fetching data type %s ID %s...", data_type, id)

        type_info = self.data_types.get(data_type)
        logging.debug("type_info: %s", type_info)
        if not type_info:
            raise UnknownDataType(data_type)

        path = type_info[constants.ENDPOINT_PATH]
        logging.debug("path: %s", path)
        url = f"{self.base_url}/{path}/{id}"
        logging.debug("url: %s", url)
        headers = {}
        if self.access_token:
            logging.debug("adding access token to request headers")
            headers['Authorization'] = f"Bearer {self.access_token}"

        logging.info("Sending request to %s...", url)
        r = requests.get(url, headers=headers)
        logging.debug("r: %s", r)
        if r.status_code == 200:
            schema_class = type_info[constants.API_SCHEMA_CLASS]
            logging.debug("schema_class: %s", schema_class)
            schema = schema_class()
            j = r.json()
            obj = schema.load(j)
            logging.debug("obj: %s", obj)
            return obj
        elif r.status_code == 404:
            raise NotFound(url)

        raise UnexpectedResponse(url, r.status_code, r.text)

    def query(self, data_type: str, page: int = 0, limit: int = constants.DEFAULT_PAGE_SIZE) -> list:
        """

        :param str data_type:
        :param page:
        :param limit:
        :return list[Model]:
        """
        logging.debug("Querying for data type %s, page %d, limit %d...", data_type, page, limit)

        type_info = self.data_types.get(data_type)
        logging.debug("type_info: %s", type_info)
        if not type_info:
            raise UnknownDataType(data_type)

        path = type_info[constants.ENDPOINT_PATH]
        logging.debug("path: %s", path)
        url = f"{self.base_url}/{path}/"
        logging.debug("url: %s", url)
        headers = {}
        if self.access_token:
            logging.debug("adding access token to request headers")
            headers['Authorization'] = f"Bearer {self.access_token}"
        params = {}
        if page > 0:
            params[constants.PAGE_PARAM] = page
        if limit != constants.DEFAULT_PAGE_SIZE:
            params[constants.LIMIT_PARAM] = min(max(limit, 1), constants.MAX_PAGE_SIZE)

        logging.info("Sending request to %s...", url)
        r = requests.get(url, headers=headers, params=params)
        logging.debug("r: %s", r)
        if r.status_code == 200:
            schema_class = type_info[constants.API_SCHEMA_CLASS]
            logging.debug("schema_class: %s", schema_class)
            schema = schema_class()
            objs = []
            j = r.json()
            # for obj_data in j['data']:
            objs = schema.load(j, many=True)
            # logging.debug("obj: %s", obj)
            # objs.append(obj)

            logging.debug("objs: %s", objs)
            return objs
        elif r.status_code == 404:
            raise NotFound(url)

        raise UnexpectedResponse(url, r.status_code, r.text)

    def update(self, data_type: str, id: str, update: dict) -> Model:
        """

        :param data_type:
        :param id:
        :param update:
        :return:
        """
        return None

    def delete(self, data_type: str, id: str) -> bool:
        """

        :param data_type:
        :param id:
        :return:
        """
        return False
