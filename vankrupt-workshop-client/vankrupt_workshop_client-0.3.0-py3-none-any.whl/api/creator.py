import base64
import hashlib
import json
from dataclasses import asdict
from urllib.parse import urljoin

import requests
from dacite import from_dict

from vankrupt_workshop_client.api import (
    APIEnv,
    Env,
    _env_map,
    api_entities,
)

md5_hash = hashlib.md5()


class AuthError(ValueError):
    ...


def auth_check(f):
    def wrapper(*args, **kwargs):
        assert args[0].authenticated
        try:
            ans = f(*args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code != 401:
                raise e

            try:
                args[0].refresh_token()
            except Exception as e:
                print('Got error refreshing access token')
                print(e)
                raise AuthError()

            ans = f(*args, **kwargs)
        return ans

    return wrapper


def notify_dedup_service(url, upload_id, upload_size, file_md5, bucket_name):
    notification = {
        "message": {
            "attributes": {
                "eventType": "OBJECT_FINALIZE",
                "payloadFormat": "JSON_API_V1",
            },
            "data": base64.encodebytes(json.dumps({
                "bucket": bucket_name,
                "id": "random id",
                "selfLink": "str",
                "name": upload_id,
                "size": upload_size,
                "md5Hash": file_md5,
                "timeCreated": "str",
            }).encode()).decode()
        }
    }
    requests.post(
        url,
        json=notification,
    )


class CreatorClient:
    env: APIEnv
    env_vars: Env

    def __init__(
            self,
            env: APIEnv = APIEnv.release,
    ):
        self.env = env
        self.env_vars = _env_map[env]

        self._auth_header = None
        self._access_token = None
        self._refresh_token = None

        self.authenticated = False

    @staticmethod
    def xml_upload(mod_file, policy_document, file_name):
        files = {
            "file": (file_name, mod_file)
        }

        return requests.post(
            policy_document['url'],
            data=policy_document['fields'],
            files=files,
        )

    def local_upload(self, mod_file, object_name):
        """
        curl -X POST --data-binary @OBJECT_LOCATION \
            -H "Authorization: Bearer OAUTH2_TOKEN" \
            -H "Content-Type: OBJECT_CONTENT_TYPE" \
            ""
        """
        return requests.post(
            (f'http://localhost:8081/upload/storage/v1/b/'
             f'{self.env_vars.upload_bucket_name}/o?uploadType=media&name={object_name}'),
            data=mod_file,
        )

    def register(self, user: dict):
        response = requests.post(
            urljoin(self.env_vars.api_url, '/users/'),
            json=user
        )
        return response

    def authenticate(self, username: str, password: str) -> dict:
        response = requests.post(
            urljoin(self.env_vars.api_url, '/token'),
            data={
                "grant_type": "password",
                "username": username,
                "password": password,
            }
        )
        return self._authenticate(response.json()['access_token'], response.json()['refresh_token'])

    def _authenticate(self, a_t, r_t):
        self._auth_header = {
            'Authorization': 'Bearer ' + a_t
        }
        self._access_token = a_t
        self._refresh_token = r_t
        self.authenticated = True
        return self._auth_header

    def refresh_token(self):
        if not self._refresh_token:
            raise EnvironmentError

        response = requests.post(
            urljoin(self.env_vars.api_url, '/refresh-token'),
            json={
                "refresh_token": self._refresh_token,
            }
        )
        self._auth_header = {
            'Authorization': 'Bearer ' + response.json()['access_token']
        }
        self._access_token = response.json()['access_token']
        self._refresh_token = response.json()['refresh_token']
        return self._auth_header

    @auth_check
    def get_me(self) -> api_entities.User:
        response = requests.get(
            urljoin(self.env_vars.api_url, '/users/me'),
            headers=self._auth_header,
        )
        response.raise_for_status()
        resp = from_dict(data_class=api_entities.User, data=response.json())
        return resp

    @auth_check
    def create_mod(self, mod: api_entities.ModCreate) -> api_entities.ModBase:
        response = requests.post(
            urljoin(self.env_vars.api_url, '/mods/'),
            json=asdict(mod),
            headers=self._auth_header,
        )
        response.raise_for_status()

        res = from_dict(data_class=api_entities.ModBase, data=response.json())
        return res

    @auth_check
    def initiate_upload(
            self, mod_id: int,
            mod_version: api_entities.ModFileUploadRequest
    ) -> api_entities.ModFileUploadResponse:
        response = requests.post(
            urljoin(self.env_vars.api_url, f"/mods/{mod_id}/initiate_upload/"),
            json=asdict(mod_version),
            headers=self._auth_header,
        )
        response.raise_for_status()

        res = from_dict(data_class=api_entities.ModFileUploadResponse, data=response.json())
        return res

    @auth_check
    def my_mods(self):
        response = requests.get(
            urljoin(self.env_vars.api_url, "/mods/my/"),
            # self._api_url + f"/mods/my/",
            headers=self._auth_header,
        )
        response.raise_for_status()
        return response

    def upload_mod(self, mod_size: int, mod_file: bytes, policy_document: dict):
        object_id = policy_document['fields']['key']
        if self.env == APIEnv.local:
            response = self.local_upload(mod_file,
                                         object_name=object_id)

            md5_hash.update(mod_file)
            mod_md5_hash = base64.encodebytes(md5_hash.digest()).decode()
            notify_dedup_service(
                url=self.env_vars.modprocessing_url,
                upload_id=object_id,
                upload_size=mod_size,
                file_md5=mod_md5_hash,
                bucket_name=self.env_vars.upload_bucket_name
            )
        else:
            response = self.xml_upload(mod_file, policy_document, file_name=object_id)
        response.raise_for_status()

        return response
