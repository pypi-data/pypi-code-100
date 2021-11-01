from dataclasses import dataclass


__version__ = '0.3.0'


@dataclass
class Auth:
    access_token: str
    refresh_token: str

    env: str
