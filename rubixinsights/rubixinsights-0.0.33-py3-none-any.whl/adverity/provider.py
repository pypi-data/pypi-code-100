import requests
import json
from loguru import logger


class Provider:
    def __init__(self, stack: str, username: str, password: str):
        self.username = username
        self.password = password
        self.stack = stack
        self.endpoint = f"{self.stack}.datatap.adverity.com"

    def get_token(self):
        payload = {
            'username': self.username,
            'password': self.password
        }
        headers = {'content-type': 'application/json'}
        try:
            r = requests.post(f"https://{self.endpoint}/api/auth/token/",
                              data=json.dumps(payload), headers=headers)
            token = json.loads(r.text)['token']
        except:
            logger.exception("Failed to get login token")
        return token


if __name__ == '__main__':
    p = Provider(stack='rubix', username='rohan+api@rubixagency.com', password='AeUDm6Bp7d2jqJE6')
    print(p.get_token())
