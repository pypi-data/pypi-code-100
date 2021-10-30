from .auth import AuthApp, OAuth2Token
from authlib.integrations.requests_client import OAuth2Session
from typing import Union


def authorize(func):
    """ Load OAuth2Session

    A :class:`authlib.integrations.requests_client.OAuth2Session ` is needed in order to 
    call the sky api and save api tokens.
    
    loadClient first attempts to load a token from the users cache but if there's no token 
    available it will automatically launch a local web server in order to authenticate you
    with the Sky API
    """    

    def wrap(*args, **kwargs):
        # Assing the sky instance
        skyObject = args[0]
        
        # Chcking if theres a client existant
        if not skyObject.client:
            # Chccking if the user already has a token caced
            if not skyObject._loadCachedToken():
                authorizationApp(skyObject)
            # Initalizing the client class
            skyObject.client = OAuth2Session(
                    token= skyObject.token,
                    client_id = skyObject.token['client_id'],
                    client_secret = skyObject.token['client_secret'],
                    token_endpoint='https://oauth2.sky.blackbaud.com/token',
                    token_endpoint_auth_method='client_secret_basic'
                )
        # Running the call function
        return func(*args, **kwargs)
    return wrap


def authorizationApp(skyObject) -> None:
    """Launch server to retrieve Sky API token"""
    app = AuthApp.load_credentials(skyObject.file_path)
    skyObject.token = app.run_local_server()
    skyObject._saveToken(skyObject.token)


class BaseRequest:

    def __init__(
        self,
        client: OAuth2Session,
        url: str,    
        header: dict,
        params: Union[dict, None] = None,
        data: Union[dict, None] = None
        ):
        self.client = client
        self.url = url
        self.header = header
        self.params = params
        self.data = data

    def getData(self):
        pass

    def cleanData(self):
        pass

    def updateToken(self, cache_token):
        self.client.token['client_id'] = cache_token['client_id']
        self.client.token['client_secret'] = cache_token['client_secret']
        if self.client.token != cache_token:
            return self.client.token
        return cache_token


class GetRequest(BaseRequest):

    def getData(self):
        data = self.client.get(
            self.url, 
            headers = self.header, 
            params=self.params)
        return data.json()

    def cleanData(self):
        pass


class PostRequest(BaseRequest):

    def getData(self):
        data = self.client.post(
            self.url, 
            headers = self.header, 
            data=self.data)
        return data

    def cleanData(self):
        pass


class PatchRequest(BaseRequest):

    def getData(self, **kwargs):
        data = self.client.patch(
            self.url, 
            headers=self.header, 
            params=self.params, 
            data=self.data, 
            **kwargs
        )
        return data

    def cleanData(self):
        pass

  
class DeleteRequest(BaseRequest):

    def getData(self, **kwargs):
        data = self.client.delete(
            self.url, 
            headers=self.header, 
            params=self.params, 
            data=self.data, 
            **kwargs
        )
        return data

    def cleanData(self):
        pass