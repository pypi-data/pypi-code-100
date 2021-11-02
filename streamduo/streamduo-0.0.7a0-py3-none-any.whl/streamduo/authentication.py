import requests

class Authentication:
    def __init__(self, client_id, client_secret):
        """Constructor"""
        self.auth_endpoint = "https://dev-v475zrua.us.auth0.com/oauth/token"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.set_oauth_token()

    def set_oauth_token(self):
        header = {'content-type': 'application/x-www-form-urlencoded'}
        token_req_payload = {'grant_type': 'client_credentials',
         'client_id': self.client_id,
         'client_secret': self.client_secret,
         'audience': 'https://api.streamduo.com'}
        token_response = requests.post(self.auth_endpoint,
                                       data=token_req_payload,
                                       headers=header)
        self.token = token_response.json()['access_token']
