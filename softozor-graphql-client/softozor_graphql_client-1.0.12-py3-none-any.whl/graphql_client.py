from six.moves import urllib
from http.cookies import SimpleCookie

import json


class GraphQLClient:

    def __init__(self, endpoint, admin_secret=None):
        self.endpoint = endpoint
        self.token = None
        self.headername = None
        self.admin_secret = admin_secret

    def execute(self, query, variables=None, auth_token=None, run_as_admin=False):
        self.__clear_token()
        if auth_token:
            self.__inject_token(auth_token)
        return self._send(query, variables, run_as_admin)

    def __inject_token(self, token, headername='Authorization'):
        self.token = token
        self.headername = headername

    def __clear_token(self):
        self.token = None
        self.headername = None

    def _send(self, query, variables, run_as_admin):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = f'Bearer {self.token}'

        if run_as_admin:
            headers['x-hasura-admin-secret'] = self.admin_secret

        req = urllib.request.Request(
            self.endpoint, json.dumps(data).encode('utf-8'), headers)

        try:
            response = urllib.request.urlopen(req)
            header_cookies = response.getheader('set-cookie')
            cookies = SimpleCookie()
            if header_cookies:
                cookies.load(header_cookies)
            return json.loads(response.read().decode('utf-8')), cookies
        except urllib.error.HTTPError as e:
            print((e.read()))
            print('')
            raise e
