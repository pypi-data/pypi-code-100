"""
    Title: access_token
    Author: Kushagra A.
    Language: Python
    Date Created: 23-09-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ##      Generates a access token on bitbucket account        ## 
         ###############################################################
 """

import requests
from requests.auth import HTTPBasicAuth
from buildpan import setting


info = setting.info

# getting env variable
key = info["key"]
secret_key = info["secret_key"]

def access_token(refresh_token):
    access_url = "https://bitbucket.org/site/oauth2/access_token"
    grant_body = {
        "grant_type": 'refresh_token',
        "refresh_token": refresh_token
    }

    # generating access token
    response = requests.post(access_url, auth=HTTPBasicAuth(key, secret_key), data=grant_body)
    token = response.json()['access_token']

    return token