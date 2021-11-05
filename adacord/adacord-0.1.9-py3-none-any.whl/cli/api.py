import urllib
from typing import Any, Dict, List, Union, Callable
from dataclasses import dataclass

import requests
from requests.auth import AuthBase

from .commons import get_token
from .exceptions import AdacordApiError

HTTP_TIMEOUT = 10


class AccessTokenAuth(AuthBase):
    """A class that adds a Bearer token to the request headers."""

    def __init__(self, token_getter: Callable[[], str]):
        self._token_getter = token_getter
        self._token = None

    def get_token(self):

        if not self._token:
            self._token = self._token_getter()
        return self._token

    def __call__(self, request):

        request.headers["Authorization"] = f"Bearer {self.get_token()}"
        return request


class CustomHTTPAdapter(requests.adapters.HTTPAdapter):
    """
    This adapter is a wrapper for the default HTTPAdapter for further
    customization. It does:
        - custom exception raising.
    """

    def send(self, req, *args, **kwargs):
        response = super().send(req, *args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            raise AdacordApiError(
                response.json(), status_code=response.status_code
            ) from error
        else:
            return response


class HTTPClient(requests.Session):
    """A class to make HTTP requests using the CustomHTTPAdapter."""

    def __init__(self, auth: AuthBase = None):
        super().__init__()
        self.auth: AuthBase = auth
        adapter = CustomHTTPAdapter()
        self.mount("http://", adapter)
        self.mount("https://", adapter)

    def request(self, method: str, url: str, *args, **kwargs):
        response = super().request(
            method, url, timeout=HTTP_TIMEOUT, *args, **kwargs
        )
        if not response.ok:
            raise AdacordApiError(
                response.json(), status_code=response.status_code
            )
        return response

    @classmethod
    def with_token(cls, token: str) -> "HTTPClient":
        return cls(auth=AccessTokenAuth(token_getter=lambda: token))


class ApiClient:
    """Client for the Adacord API"""

    def __init__(self, client: HTTPClient):
        self.client = client

    @property
    def base_path(self) -> str:
        return "https://api.adacord.com"

    def url_for(self, endpoint: str, version: str = "v0") -> str:
        """Return the absolute URL to the endpoint for the given API version."""
        suffix = f"{version}/{endpoint}" if endpoint else version
        return urllib.parse.urljoin(self.base_path, suffix)


class User(ApiClient):
    def create(self, email: str, password: str):
        data = {"email": email, "password": password}
        url = self.url_for("/users")
        self.client.post(url, json=data, auth=False)

    def login(self, email: str, password: str) -> Dict[str, Any]:
        data = {"email": email, "password": password}
        url = self.url_for("/users/token")
        response = self.client.post(url, json=data, auth=False)
        return response.json()

    def request_password_reset(self, email: str) -> Dict[str, Any]:
        data = {"email": email}
        url = self.url_for("/users/password_reset")
        response = self.client.post(url, json=data, auth=False)
        return response.json()

    def request_verification_email(
        self, email: str, password: str
    ) -> Dict[str, Any]:
        data = {"email": email, "password": password}
        url = self.url_for("/users/verification_email")
        response = self.client.post(url, json=data, auth=False)
        return response.json()


class Buckets(ApiClient):
    def _bucket_from_payload(
        self, bucket_payload: Dict[str, Any]
    ) -> Union["Bucket", List["Bucket"]]:
        bucket_args = BucketArgs(**bucket_payload)
        return Bucket(bucket_args, buckets_router=self)

    def create(self, description: str, schemaless: bool = False) -> "Bucket":
        data = {"description": description, "schemaless": schemaless}
        url = self.url_for("/buckets")
        response = self.client.post(url, json=data)
        bucket_payload = response.json()
        return self._bucket_from_payload(bucket_payload)

    def list(self) -> List["Bucket"]:
        endpoint = "/buckets"
        url = self.url_for(endpoint)
        response = self.client.get(url)
        bucket_payload = response.json()
        return [
            self._bucket_from_payload(payload) for payload in bucket_payload
        ]

    def get(self, bucket: str) -> "Bucket":
        """Return a Bucket.
        Args:
            bucket: the name or the uuid of the bucket.
        """
        endpoint = f"/buckets/{bucket}"
        url = self.url_for(endpoint)
        response = self.client.get(url)
        bucket_payload = response.json()
        return self._bucket_from_payload(bucket_payload)

    def delete(self, bucket: str) -> Dict[str, Any]:
        url = self.url_for(f"/buckets/{bucket}")
        response = self.client.delete(url)
        return response.json()

    def create_token(self, bucket: str, description: str = None):
        data = {"description": description}
        url = self.url_for(f"/buckets/{bucket}/tokens")
        response = self.client.post(url, json=data)
        return response.json()

    def get_tokens(self, bucket: str):
        url = self.url_for(f"/buckets/{bucket}/tokens")
        response = self.client.get(url)
        return response.json()

    def delete_token(self, bucket: str, token_uuid: str):
        url = self.url_for(f"/buckets/{bucket}/tokens/{token_uuid}")
        response = self.client.delete(url)
        return response.json()

    def query(self, query: str) -> List[Dict[str, Any]]:
        data = {"query": query}
        response = self.client.post(self.url_for("/buckets/query"), json=data)
        return response.json()

    def push_data(self, bucket: str, rows: List[Dict[str, Any]]):
        data = {"data": rows}
        response = self.client.post(
            self.url_for(f"/buckets/{bucket}/data"), json=data
        )
        return response.json()

    def get_data(self, bucket: str) -> List[Dict[str, Any]]:
        response = self.client.get(self.url_for(f"/buckets/{bucket}/data"))
        return response.json()


class ApiTokens(ApiClient):
    def create(self, description: str = None):
        data = {"description": description}
        url = self.url_for("/api_tokens")
        response = self.client.post(url, json=data)
        return response.json()

    def list(self):
        url = self.url_for("/api_tokens")
        response = self.client.get(url)
        return response.json()

    def delete(self, token_uuid: str):
        url = self.url_for(f"/api_tokens/{token_uuid}")
        response = self.client.delete(url)
        return response.json()


@dataclass
class BucketArgs:
    uuid: str
    name: str
    description: str
    url: str
    schemaless: bool


class Bucket:
    def __init__(
        self,
        bucket_payload: BucketArgs,
        buckets_router: "Buckets",
    ):
        self.uuid = bucket_payload.uuid
        self.name = bucket_payload.name
        self.description = bucket_payload.description
        self.url = bucket_payload.url
        self.schemaless = bucket_payload.schemaless
        self._buckets_router = buckets_router

    def __repr__(self):
        return f"Bucket<{self.name}>"

    def delete(self) -> Dict[str, Any]:
        return self._buckets_router.delete(self.uuid)

    def create_token(self, description: str = None) -> Dict[str, Any]:
        return self._buckets_router.create_token(self.uuid, description)

    def get_tokens(self) -> List[Dict[str, Any]]:
        return self._buckets_router.get_tokens(self.uuid)

    def delete_token(self, token_uuid: str) -> Dict[str, Any]:
        return self._buckets_router.delete_token(self.uuid, token_uuid)

    def push_data(self, rows: List[Dict[str, Any]]):
        return self._buckets_router.push_data(self.uuid, rows)

    def get_data(self) -> List[Dict[str, Any]]:
        return self._buckets_router.get_data(self.uuid)


class AdacordApi:
    """A facade to the Adacord API"""

    def __init__(self, client: HTTPClient = None):
        self.client = client or HTTPClient(auth=AccessTokenAuth(get_token))

    @property
    def User(self) -> User:
        return User(self.client)

    @property
    def Buckets(self) -> Buckets:
        return Buckets(self.client)

    @property
    def ApiTokens(self) -> Buckets:
        return ApiTokens(self.client)

    def Bucket(self, bucket_uuid: str) -> Bucket:
        return self.Buckets.get(bucket_uuid)

    @classmethod
    def Client(cls, with_auth: bool = True, token: str = None) -> "AdacordApi":
        if token:
            client = HTTPClient.with_token(token)
        elif with_auth:
            client = None
        else:
            client = HTTPClient()
        return cls(client)

    def create_bucket(self, description: str, schemaless: bool) -> Bucket:
        return self.Buckets.create(description, schemaless)

    def get_bucket(self, bucket_uuid: str) -> Bucket:
        return self.Buckets.get(bucket_uuid)


def create_api(with_auth: bool = True) -> AdacordApi:
    return AdacordApi.Client(with_auth=with_auth)
