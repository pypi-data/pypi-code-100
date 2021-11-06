try:
    from .Exception import AuthException
    from knox.auth import TokenAuthentication

    class Authentication(TokenAuthentication):
        def authenticate_credentials(self, token):
            try:
                return super().authenticate_credentials(token)
            except:
                raise AuthException()
except:
    pass
