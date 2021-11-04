from jose import jwt
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakError

from paretos.authentication.authentication_error import AuthenticationError


class KeycloakService:
    KEYCLOAK_DECODE_ALGORITHMS = ["RS256"]

    def __init__(self, keycloak_open_id: KeycloakOpenID):
        self.__public_key = None
        self.__keycloak_open_id = keycloak_open_id

    def get_authentication_token(self, username: str, password: str) -> dict:
        try:
            token = self.__keycloak_open_id.token(
                username=username, password=password, grant_type="password"
            )
        except KeycloakError as error:
            raise AuthenticationError(
                "Could not authenticate as a Paretos user: " + str(error)
            )

        if token is None or "access_token" not in token:
            raise AuthenticationError(
                "Could not authenticate as a Paretos user: " "no access token returned"
            )

        self.decode_token(token["access_token"])

        return token

    def decode_token(self, token: str) -> dict:
        try:
            decoded_token = self.__keycloak_open_id.decode_token(
                token, self.get_public_key(), algorithms=self.KEYCLOAK_DECODE_ALGORITHMS
            )
        except jwt.JWTError as error:
            raise AuthenticationError(
                "Could not authenticate as a Paretos user: " + str(error)
            )
        if decoded_token is None:
            raise AuthenticationError(
                "Could not authenticate as a Paretos user: "
                "access token could not be decoded"
            )
        return decoded_token

    def get_public_key(self) -> str:
        if self.__public_key is None:
            self.__public_key = self.__keycloak_open_id.public_key()
            self.__add_pem_headers_and_footers_to_public_key()
        return self.__public_key

    def __add_pem_headers_and_footers_to_public_key(self):
        self.__public_key = (
            """-----BEGIN PUBLIC KEY-----\n"""
            + self.__public_key
            + "\n-----END PUBLIC KEY-----"
            ""
        )
