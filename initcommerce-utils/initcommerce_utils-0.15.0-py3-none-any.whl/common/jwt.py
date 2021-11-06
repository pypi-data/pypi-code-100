import jwt


class JWT:
    @staticmethod
    def sign_new_token(claims: dict, secret: dict, algorithm: str) -> str:
        return jwt.encode(claims, key=secret, algorithm=algorithm)

    @staticmethod
    def decode_token(
        token: str, public: str = None, algorithm: str = None, verify: bool = True
    ) -> dict:
        kwargs = {}
        if verify:
            if not (public and algorithm):
                raise ValueError("public and algorithm must not be None")
            kwargs.update(key=public, algorithms=[algorithm])
        else:
            kwargs.update(options=dict(verify_signature=verify))
        return jwt.decode(token, **kwargs)
