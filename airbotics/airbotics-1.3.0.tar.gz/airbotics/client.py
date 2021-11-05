import os
import re
import json
import requests
from .exceptions import *
from .consts import *
from .modules.account import Account
from .modules.api_keys import ApiKeys
from .modules.maps import Maps

class Client():

    def __init__(self, api_key: str = None):
        '''Initialises the client.'''

        self._api_key = api_key or os.environ.get(ENV_API_KEY)
        if self._api_key is None or not re.match(API_KEY_REGEX, self._api_key):
            raise InvalidApiKeyException()
        
        self.account = Account(self)
        self.api_keys = ApiKeys(self)
        self.maps = Maps(self)

    def _make_request(self, params: RequestParams) -> dict:
        '''Helper function to make a request to the server.'''
        
        make_request = getattr(requests, params['method'].value.lower())

        headers = {
            'user-agent': f'airbotics-python-sdk/{SDK_VERSION}',
            'content-type': params['req_content_type'].value,
            API_KEY_HEADER_NAME: self._api_key,
        }

        try:

            data = params['body']
            if data and params['req_content_type'] == ContentType.JSON:
                data = json.dumps(params['body'])

            # Make request
            response = make_request(BASE_URL+params['path'], headers=headers, data=data, timeout=REQUEST_TIMEOUT)

            if response.status_code == StatusCode.OK.value:
                # Server has returned successfully, parse based on expected content-type
                if params['res_content_type'] == ContentType.JSON:
                    return response.json()
                else: 
                    return response.content

            if response.status_code == StatusCode.BAD_REQUEST.value:
                # Request was bad for some reason, construct error message from response
                message = '. '.join([i for i in response.json()['errors']])
                raise BadRequestException(message)

            if response.status_code == StatusCode.NOT_FOUND.value:
                # That resource could not be found
                raise NotFoundException()

            if response.status_code == StatusCode.UNAUTHORIZED.value:
                # The request could not be authenticated
                raise AuthenticationException()

            if response.status_code == StatusCode.FORBIDDEN.value:
                # The request could not be authorized
                raise AuthorizationException()

            if response.status_code == StatusCode.SERVER_ERROR.value:
                # An internal server error has occured
                raise ServerErrorException()

        except (requests.RequestException, requests.ConnectionError, requests.TooManyRedirects, requests.Timeout) as e:
            # A generic error occured making the request, e.g. timeout, network not available, etc.
            raise RequestException

        except Exception as e:
            # Unknown error
            raise e
