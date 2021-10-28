from importlib import import_module
from typing import Any, Dict, Optional

from neuroio import constants
from neuroio.auth_token import AuthorizationTokenAuth
from neuroio.utils import cached_property, get_package_version


class Catcher:
    def __init__(
        self, prev: str, is_async: bool, settings: dict, api_version: int
    ) -> None:
        self.prev = prev
        self.settings = settings
        self.is_async = is_async
        self.api_version = api_version

    def __getattr__(self, item: str) -> Any:
        return Catcher(
            prev=f"{self.prev}.{item}",
            is_async=self.is_async,
            settings=self.settings,
            api_version=self.api_version,
        )

    def __call__(self, *args: list, **kwargs: dict) -> Any:
        method = self.prev.split(".")[-1]
        path = ".".join(self.prev.split(".")[:-1])
        module_path = f"neuroio.{path}.v{self.api_version}"
        v1_module = import_module(module_path)
        if v1_module:
            cls = getattr(
                v1_module, ("ImplAsync" if self.is_async else "Impl")
            )
            inst = cls(settings=self.settings)
            if inst:
                return getattr(inst, method)(*args, **kwargs)


class Client:
    def __init__(
        self,
        api_token: Optional[str] = None,
        api_version: int = 1,
        timeout: float = constants.HTTP_CLIENT_TIMEOUT,
    ):
        """
        Creates and manages singleton of HTTP client, that is used to make
        request to API.
        """
        self.api_version = api_version

        self.csettings = self.client_settings(timeout=timeout, token=api_token)
        self.init()

    def init(self) -> None:
        self.api_atrr_names = [
            "sources",
            "entries",
            "streams",
            "utility",
            "settings",
            "groups",
            "persons",
            "notifications",
        ]
        self.iam_atrr_names = [
            "auth",
            "spaces",
            "lists",
            "licenses",
            "whoami",
            "tokens",
            "billing",
        ]

    @cached_property
    def is_async(self) -> bool:
        return self.__class__.__name__ == "AsyncClient"

    @property
    def common_headers(self) -> dict:
        root = "neuroio-python"
        if self.is_async:
            root = "neuroio-async-python"
        return {"User-Agent": f"{root}/{get_package_version()}"}

    def client_settings(
        self, timeout: float, token: str = None
    ) -> Dict[Any, Any]:
        settings = {
            "timeout": timeout,
            "headers": self.common_headers,
        }
        if token:
            settings["auth"] = AuthorizationTokenAuth(api_token=token)

        return settings

    def __getattr__(self, item: str) -> Any:
        if item in self.api_atrr_names + self.iam_atrr_names:
            return Catcher(
                prev=item,
                is_async=self.is_async,
                settings=self.csettings,
                api_version=self.api_version,
            )
        else:
            # Default behaviour
            raise AttributeError


class AsyncClient(Client):
    pass
