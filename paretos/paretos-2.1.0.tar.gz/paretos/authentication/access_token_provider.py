from paretos.authentication.access_token import AccessToken
from paretos.authentication.keycloak_authenticator import KeycloakAuthenticator


class AccessTokenProvider:
    def __init__(
        self,
        keycloak_authenticator: KeycloakAuthenticator,
        access_token: AccessToken = None,
    ):
        self.__keycloak_authenticator = keycloak_authenticator
        self.__access_token = access_token

    def get_access_token(self) -> str:
        if self.__access_token is None or self.__access_token.is_token_expired():
            self.__access_token = self.__keycloak_authenticator.authenticate()
        return self.__access_token.get_access_token()
