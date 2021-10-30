import os
import pickle

from .utils import *
from logging import warn


class Sky:

    def __init__(
        self, 
        api_key: Union[str, None] = None, 
        file_path: str = "sky_credentials.json", 
        token_path: Union[str, None]  = None
        ):
        """Blackbaud Sky API client 

        This class uses a :class:`authlib.integrations.requests_client.OAuth2Session` for 
        calls to the Blackbaud Sky API.
        
        """
        self.token = None
        self.client = None
        self.file_path = file_path

        # Seeing if the user saved the api key as an environment variable
        if os.getenv('BB_API_KEY'):
            self.api_key = os.getenv('BB_API_KEY')
        elif api_key:
            self.api_key = api_key
        else:
            warn("""
            A api key is needed to call the Blackbaud sky api. You can either initialize it when calling 
            the Sky class or you can save it in a environment variable called BB_API_KEY
            """)

        # Path to cached token
        if token_path:
            self.token_path = token_path
        elif os.getenv('BB_TOKEN_PATH'):
            self.token_path = os.getenv('BB_TOKEN_PATH')
        else:
            self.token_path = '.sky-token'

    @authorize
    def get(
        self,
        params: Union[dict, None] = None,
        reference: str = 'school',
        endpoint: str = "roles"
        ) -> dict:
        """ Get request to the Sky API
        Args:
            params: Dictionary that defines parameters to be passed to 
            the api
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = GetRequest(
            self.client,
            url,
            self.request_header,
            params=params
        )

        data = apiCall.getData()
        self._saveToken(apiCall.updateToken(self.token))
        return data


    @authorize
    def post(
        self,
        data: dict,
        reference: str = 'school',
        endpoint: str = "users",
        ) -> dict:
        """Post request to the Sky API
        Args:
            data: Dictionary that defines the request data to be passed to 
            the api in order to create a new record
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        if not data:
            raise ValueError("Request data is required for post requests")
        url = self._get_url(reference, endpoint)

        apiCall = PostRequest(
            self.client,
            url,
            self.request_header,
            data=data
        )

        data = apiCall.getData()
        self._saveToken(apiCall.updateToken(self.token))
        return data


    @authorize
    def patch(
        self,
        reference: str = 'school',
        endpoint: str = "roles",
        params: Union[dict, None] = None,
        data: Union[dict, None] = None,
        **kwargs
        ) -> dict:
        """Patch requests to the Sky API
        Args:
            data: Dictionary that defines the request data to be passed to 
            the api in order to create a new record
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = PatchRequest(
            self.client,
            url,
            self.request_header,
            params=params,
            data=data
        )

        data = apiCall.getData(**kwargs)
        self._saveToken(apiCall.updateToken(self.token))
        return data


    @authorize
    def delete(
        self,
        reference: str = 'school',
        endpoint: str = "roles",
        params: Union[dict, None] = None,
        data: Union[dict, None] = None,
        **kwargs
        ) -> dict:
        """Delete requests to the sky API

        Args:
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference
            **kwargs: ... Honestly don't know yet. Never used this endpoint. Just 
            adding for testing

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)

        apiCall = DeleteRequest(
            self.client,
            url,
            self.request_header,
            params = params,
            data=data
        )

        data = apiCall.getData(**kwargs)
        self._saveToken(apiCall.updateToken(self.token))
        return data


    def _loadCachedToken(self) -> Union[None, OAuth2Token]:
        """Load Sky API token from cache"""
        # Loading token from binary file
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.token = pickle.load(token)          
        return self.token


    def _get_url(self, reference: str, endpoint: str) -> str:
        """Format api requests url

        Args:
            reference: 
            endpoint: 

        Returns:
            API url to call
        """
        return f'https://api.sky.blackbaud.com/{reference}/v1/{endpoint}'


    def _saveToken(
        self, 
        token: OAuth2Token
        ) -> None:
        """Save OAuth2Token for future use"""
        with open(self.token_path,  'wb') as f:
            pickle.dump(token, f)
        self.token = token


    @property
    def request_header(self):
        """API key to pass to Request header"""
        return {"Bb-Api-Subscription-Key": self.api_key}