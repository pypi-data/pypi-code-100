import time

from requests_oauthlib import OAuth1

from . import config
from .constants.errors import NotFoundError

class AuthHandler:

    def __init__(self, api, apiKey):
        
        self.apiKey = apiKey
        self.api = api
    
    def addAuthKey(self, data):
        data['key'] = self.apiKey
        return data