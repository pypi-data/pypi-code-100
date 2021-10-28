import json
import os
from typing import List

import requests
from urllib.parse import urljoin

from i2a_chat_api_client.exceptions import I2AChatApiClientUnauthorizedException, I2AChatApiClientValidationError, \
    I2AChatApiClientNotFoundError


class I2aChatApiServer:
    STAGE = 'https://chat-server-stg.i2asolutions.com'
    PRODUCTION = NotImplemented
    LOCAL = 'http://0.0.0.0:8000'


class I2AChatApiClient:

    def __init__(self, x_application_secret, server_url=I2aChatApiServer.STAGE):
        self.server_url = server_url
        self.api_root_path = 'server-to-server/v1'
        self.x_application_secret = x_application_secret

    def _required_headers(self):
        return {
            'X-Application-Secret': self.x_application_secret
        }

    def _get_full_url(self, uri):
        return urljoin(self.server_url, os.path.join(self.api_root_path, uri))

    @staticmethod
    def _status_code_message(response):
        return f"Service return {response.status_code} status code"

    def ping(self):
        """
        Checks if service is up and running and if you are authorized to use it:
        X-Application-Secret header must be valid
        :return: None
        """

        url = self._get_full_url('ping/')
        response = requests.get(url, headers=self._required_headers())
        if response.status_code == 200:
            return
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        else:
            raise Exception(f'Ping attempt at {url} has failed. {self._status_code_message(response)}')

    def open_session(self, device_identifier: str, fcm_token: str, application_user_identifier: str, custom_data=None):
        """
        Creates new session
        :param device_identifier: str
        :param fcm_token: str
        :param application_user_identifier: str
        :param custom_data: dict -> This data will be added to every message in websocket
        :return: token: str
        """
        if custom_data is None:
            custom_data = {}
        url = self._get_full_url('session/open-session/')
        data = {
            'device_identifier': device_identifier,
            'fcm_token': fcm_token,
            'application_user_identifier': application_user_identifier,
            'custom_data': json.dumps(custom_data)
        }
        response = requests.post(url, data, headers=self._required_headers())
        if response.status_code == 201:
            return response.json()['token']
        elif response.status_code == 400:
            raise I2AChatApiClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        else:
            raise Exception(f'Open session failed. {self._status_code_message(response)}')

    def close_session(self, token: str):
        """
        Deletes session with provided token
        :param token: str
        :return: None
        """
        url = self._get_full_url('session/close-session/')
        data = {
            'token': token
        }
        response = requests.post(url, data, headers=self._required_headers())
        if response.status_code == 200:
            return
        elif response.status_code == 400:
            raise I2AChatApiClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AChatApiClientNotFoundError(data=response.json())
        else:
            raise Exception(f'Close session failed. {self._status_code_message(response)}')

    def create_chat_room(self, application_users_identifiers: List[str]):
        """
        Creates new chat room
        :param application_users_identifiers: [str,]
        :return: chat_room_identifier: str
        """

        url = self._get_full_url('chat-room/')
        data = {
            'application_users_identifiers': application_users_identifiers
        }
        response = requests.post(url, data, headers=self._required_headers())
        if response.status_code == 201:
            return response.json()['identifier']
        elif response.status_code == 400:
            raise I2AChatApiClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        else:
            raise Exception(f'Create chat room failed. {self._status_code_message(response)}')

    def add_users_to_chat_room(self, chat_room_identifier: str, application_users_identifiers: List[str]):
        """
        Adds new users to provided chat room
        :param chat_room_identifier: str
        :param application_users_identifiers: [str, ]
        :return: chat_room_identifier
        """
        url = self._get_full_url(f'chat-room/{chat_room_identifier}/add-users/')
        data = {
            'application_users_identifiers': application_users_identifiers
        }
        response = requests.post(url, data, headers=self._required_headers())
        if response.status_code == 200:
            return response.json()['identifier']
        elif response.status_code == 400:
            raise I2AChatApiClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AChatApiClientNotFoundError(data=response.json())
        else:
            raise Exception(f'Add users to chat room failed. {self._status_code_message(response)}')

    def remove_users_from_chat_room(self, chat_room_identifier: str, application_users_identifiers: List[str]):
        """
        Removes users from provided chat room
        :param chat_room_identifier: str
        :param application_users_identifiers: [str, ]
        :return: chat_room_identifier: str
        """
        url = self._get_full_url(f'chat-room/{chat_room_identifier}/remove-users/')
        data = {
            'application_users_identifiers': application_users_identifiers
        }
        response = requests.post(url, data, headers=self._required_headers())
        if response.status_code == 200:
            return response.json()['identifier']
        elif response.status_code == 400:
            raise I2AChatApiClientValidationError(data=response.json())
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AChatApiClientNotFoundError(data=response.json())
        else:
            raise Exception(f'Remove users from chat room failed. {self._status_code_message(response)}')

    def delete_chat_room(self, chat_room_identifier: str):
        """
        Deletes provided chat room
        :param chat_room_identifier: str
        :return: None
        """
        url = self._get_full_url(f'chat-room/{chat_room_identifier}/')
        response = requests.delete(url, headers=self._required_headers())
        if response.status_code == 204:
            return
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AChatApiClientNotFoundError(data=response.json())
        else:
            raise Exception(f'Delete chat room failed. {self._status_code_message(response)}')

    def send_system_message(self, chat_room_identifier, message):
        """
       Queuing system message to be saved and send on websocket in provided chat room
       :param chat_room_identifier: str
       :param message
       :return: response (str)
       """
        url = self._get_full_url(f'system-message/send-system-message/')
        data = {
            'chat_room_identifier': chat_room_identifier,
            'message': message
        }
        response = requests.post(url, data, headers=self._required_headers())
        if response.status_code == 200:
            return response
        elif response.status_code == 401:
            raise I2AChatApiClientUnauthorizedException(data=response.json())
        elif response.status_code == 404:
            raise I2AChatApiClientNotFoundError(data=response.json())
        else:
            raise Exception(f'Send system message failed. {self._status_code_message(response)}')
