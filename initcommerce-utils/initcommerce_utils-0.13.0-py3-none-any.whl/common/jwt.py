import jwt


class JWT:
    @staticmethod
    def sign_new_token(*, secret: dict, algorithm: str, **claims) -> str:
        return jwt.encode(claims, key=secret, algorithm=algorithm).decode("utf8")

    @staticmethod
    def decode_token(
        token: str, public: str = None, algorithm: str = None, verify: bool = True
    ):
        kwargs = {}
        if verify:
            if not (public and algorithm):
                raise ValueError("public and algorithm must not be None")
            kwargs.update(key=public, algorithm=[algorithm])
        else:
            kwargs.update(options=dict(verify_signature=verify))
        return jwt.decode(token, **kwargs)
