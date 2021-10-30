from dataclasses import dataclass

import requests
import requests_http_signature


@dataclass
class Post(object):
    key_username: object
    key_private: object
    key_url: str

    def auth(self):
        key_id = f"{self.key_url}/user/{self.key_username}"
        return requests_http_signature.HTTPSignatureHeaderAuth(
            key=self.key_private,
            key_id=key_id,
            algorithm="rsa-sha256",
            headers=["(request-target)", "host", "date", "digest"],
        )

    def post(self, *args, **kwargs):
        kwargs = {**kwargs, **{"auth": self.auth()}}
        return requests.post(*args, **kwargs)
