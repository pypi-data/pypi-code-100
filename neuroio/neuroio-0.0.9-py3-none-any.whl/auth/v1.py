from httpx import Response

from neuroio.base import IAMBase, IAMBaseAsync, IAMBaseBase


class AuthBase(IAMBaseBase):
    def get_url(self, key: str) -> str:
        return self.base_url + f"/v1/auth/{key}/"


class Impl(IAMBase, AuthBase):
    def login(self, username: str, password: str) -> Response:
        data = {"username": username, "password": password}

        with self.get_client() as client:
            return client.post(url=self.get_url("token"), json=data)

    def password_change(
        self, old_password: str, new_password: str, reset_tokens: bool = False
    ) -> Response:
        data = {
            "old_password": old_password,
            "password": new_password,
            "password2": new_password,
            "reset_tokens": reset_tokens,
        }

        with self.get_client() as client:
            return client.post(url=self.get_url("password/change"), json=data)


class ImplAsync(IAMBaseAsync, AuthBase):
    async def login(self, username: str, password: str) -> Response:
        data = {"username": username, "password": password}

        async with self.get_client() as client:
            return await client.post(url=self.get_url("token"), json=data)

    async def password_change(
        self, old_password: str, new_password: str, reset_tokens: bool = False
    ) -> Response:
        data = {
            "old_password": old_password,
            "password": new_password,
            "password2": new_password,
            "reset_tokens": reset_tokens,
        }

        async with self.get_client() as client:
            return await client.post(
                url=self.get_url("password/change"), json=data
            )
