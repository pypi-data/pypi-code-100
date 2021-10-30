import os
import pickle

from .auth import AuthApp, OAuth2Session, OAuth2Token, Union
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


    def get(
        self,
        query: Union[dict, None] = None,
        reference: str = 'school',
        endpoint: str = "users"
        ) -> dict:
        """ Get request to the Sky API
        Args:
            query: Dictionary that defines parameters to be passed to 
            the api
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)
        return self._call("get", url, query=query)

    def post(
        self,
        body: dict,
        reference: str = 'school',
        endpoint: str = "users",
        ) -> dict:
        """Post request to the Sky API
        Args:
            body: Dictionary that defines the request body to be passed to 
            the api in order to create a new record
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        if not body:
            raise ValueError("Request body is required for post requests")
        url = self._get_url(reference, endpoint)
        return self._call("get", url, query=body)

    def patch(
        self,
        reference: str = 'school',
        endpoint: str = "roles",
        body: Union[dict, None] = None
        ) -> dict:
        """Patch requests to the Sky API
        Args:
            body: Dictionary that defines the request body to be passed to 
            the api in order to create a new record
            reference: Which SKY Api refrence are you calling. See them here 
            https://developer.blackbaud.com/skyapi/apis
            endpoint: The specific endpioint that exist in the given api reference

        Returns:
           Dictionary with data from the sky api
        """
        url = self._get_url(reference, endpoint)
        return self._call("get", url, query=body)

    def delete(
        self,
        reference: str = 'school',
        endpoint: str = None,
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
        if not endpoint:
            raise ValueError("Must pass endpont to the sky API")
        url = self._get_url(reference, endpoint)
        return self._call("get", None, **kwargs)

    def _call(
        self, 
        method: str,
        url: Union[str, None],
        query: Union[str, None] = None,
        body: Union[str, None] = None,
        **kwargs
        ) -> dict:
        """Performing the call to the sky api

        Args:
            method:Which method to call
            url: Url for the sky API to call
            query:Dictionary that contains data for get 
            requests
            body: Dictionary that cointains data for patch 
            and posts requests
            kwargs: Arguments to be passed to the delete api 
            call

        Returns:
           Dictionary with data from the sky api

        """
        # Authorizing the user if not already
        if not self.client:
            self._loadClient()

        # Calling sky
        try:
            if method == "get":
                data = self.client.get(url, headers=self.request_header, params=query)
            elif method == "post":
                data = self.client.post(url, headers=self.request_header, data=body)
            elif method == "patch":
                data = self.client.patch(url, headers=self.request_header, data=body)
            elif method == "delete":
                data = self.client.patch(headers=self.request_header, **kwargs)
            else:
                raise ValueError("Not a valid api method")

            # Checking if the token was updated
            if self._loadCachedToken() != self.client.token:
                self._saveToken(self.client.token)

        except Exception as e:
            print(e)
            raise ValueError("Error calling the sky api")

        return data.json()

    
    def _loadClient(self) -> None:
        """ Load OAuth2Session

        A :class:`authlib.integrations.requests_client.OAuth2Session ` is needed in order to 
        call the sky api and save api tokens.
        
        loadClient first attempts to load a token from the users cache but if there's no token 
        available it will automatically launch a local web server in order to authenticate you
        with the Sky API
        """
        if not self._loadCachedToken():
            self._authorizeApp()

        self.client = OAuth2Session(
            token=self.token,
            token_endpoint='https://oauth2.sky.blackbaud.com/token',
            token_endpoint_auth_method='client_secret_basic'
        )


    def _authorizeApp(self) -> None:
        """Launch server to retrieve Sky API token"""
        app = AuthApp.load_credentials(self.file_path)
        self.token = app.run_local_server()
        self._saveToken(self.token)


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