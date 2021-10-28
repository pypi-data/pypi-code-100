import abc

from httpx import AsyncClient, Client

from neuroio import constants


class Base:
    def __init__(self, settings: dict) -> None:
        self.settings = settings


class APIBaseBase:
    base_url = constants.API_BASE_URL


class IAMBaseBase:
    base_url = constants.IAM_BASE_URL


class APIBase(abc.ABC, Base, APIBaseBase):
    def get_client(self) -> Client:
        return Client(**self.settings)


class APIBaseAsync(abc.ABC, Base, APIBaseBase):
    def get_client(self) -> AsyncClient:
        return AsyncClient(**self.settings)


class IAMBase(abc.ABC, Base, IAMBaseBase):
    def get_client(self) -> Client:
        return Client(**self.settings)


class IAMBaseAsync(abc.ABC, Base, IAMBaseBase):
    def get_client(self) -> AsyncClient:
        return AsyncClient(**self.settings)
