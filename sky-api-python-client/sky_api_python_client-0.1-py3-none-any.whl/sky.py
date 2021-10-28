import os
import pickle

from .auth import Flow, OAuth2Session
from logging import warn

class Sky():

    def __init__(
        self, 
        api_key=None, 
        file_path="sky_credentials.json", 
        token_path=None
        ):
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


    def call(self, endpoint='roles', reference='school',query=None,body=None):
        """
        """
        # Authorizing the user if not already
        if not self.client:
            self.loadClient()

        # Constructing api url
        url = f'https://api.sky.blackbaud.com/{reference}/v1/{endpoint}'

        # Calling sky
        try:
            data = self.client.get(url, headers=self.request_header, data=body, params=query)

            # Checking if the token was updated
            if self.loadCachedToken() != self.client.token:
                self.saveToken(self.client.token)
        except Exception as e:
            print(e)
            raise ValueError("Error calling the sky api")

        return data.json()

    
    def loadClient(self):
        """
        """
        if not self.loadCachedToken():
            self.authorizeApp()

        self.client = OAuth2Session(
            token=self.token,
            token_endpoint='https://oauth2.sky.blackbaud.com/token',
            token_endpoint_auth_method='client_secret_basic'
        )


    def authorizeApp(self):
        """
        """
        flow = Flow.load_credentials(self.file_path)
        self.token = flow.run_local_server()
        self.saveToken(self.token)
        return True


    def loadCachedToken(self):
        """
        """
        # Loading token from binary file
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.token = pickle.load(token)          
        return self.token


    @property
    def request_header(self):
        """
        API key to pass to Request header
        """
        return {"Bb-Api-Subscription-Key": self.api_key}


    def saveToken(self, token):
        """
        """
        with open(self.token_path,  'wb') as f:
            pickle.dump(token, f)
        self.token = token