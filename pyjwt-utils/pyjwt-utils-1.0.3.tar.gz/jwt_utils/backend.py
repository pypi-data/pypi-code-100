from calendar import timegm
from datetime import datetime, timedelta
from typing import List, Union
from uuid import uuid4

from jwt import InvalidAlgorithmError, InvalidTokenError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode


class BaseJwtToken:
    signing_key = None
    algorithm = 'HS256'
    iss = None
    aud = None

    def __init__(self, signing_key=None, algorithm='HS256', iss: str = None, aud: Union[str, List[str]] = None):
        """
            signing_key: str -> key used to encoder, ex: "1234"
            algorithm: str -> algorithm used to encode, exs: 'HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512'
            iss: str -> set token issuer
            aud: str | [str] -> set token subject
        """
        self.signing_key, self.algorithm = (signing_key or self.signing_key), (algorithm or self.algorithm)
        self.iss, self.aud = (iss or self.iss), (aud or self.aud)

        assert isinstance(self.signing_key, str) and self.signing_key is not None, "`signing_key` is required"
        assert self.algorithm in ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512']


class JwtEncode(BaseJwtToken):
    payload = {}
    sub = None
    exp = None
    nbf = None
    auto_iat = None
    iat = None
    auto_jti = None
    jti = None
    from_time = None

    def __init__(self, payload: dict = None, sub: str = None, exp: timedelta = None, nbf: timedelta = None,
                 auto_iat: bool = False, iat: datetime = None, auto_jti: bool = False, jti: str = None,
                 from_time: datetime = None, **kwargs):
        """
            payload: dict -> custom data, ex: {}
            sub: str -> set token subject
            exp: timedelta -> added to `from_time` to get token lifetime, ex: timedelta(minutes=5)
            nbf: timedelta -> added to `from_time` to get token invalid begore time, ex: timedelta(minutes=5)
            auto_iat: bool -> add `iat` with value `datetime.utcnow()`
            iat: datetime -> set issued token time
            auto_jti: bool -> add `jti` with `uuid4().hex`
            jti: str -> set token unique identifier
            from_time: datetime -> base datetime to calc `exp` and `nbf`, must be utc, ex: datetime.utcnow() (default)
            kwargs:
                signing_key: str -> key used to encoder, ex: "1234"
                algorithm: str -> algorithm used to encode, exs: 'HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512'
                iss: str -> set token issuer
                aud: str | [str] -> set token subject
        """
        super().__init__(**kwargs)
        self.payload = payload or self.payload
        self.from_time = from_time
        self.sub, self.exp, nbf = (sub or self.sub), (exp or self.exp), (nbf or self.nbf)
        self.auto_iat, self.iat = (auto_iat or self.auto_iat), (iat or self.iat),
        self.auto_jti, self.jti = (auto_jti or self.auto_jti), (jti or self.jti)
        self.from_time = (from_time or self.from_time)

    def set_claim(self, field, value=None):
        if value:
            self.payload[field] = value

    def mount_claims(self):
        self.payload, base_time = self.payload, self.from_time or datetime.utcnow()
        self.set_claim(field='iss', value=self.iss)
        self.set_claim(field='sub', value=self.sub)
        self.set_claim(field='aud', value=self.aud)

        if self.jti or self.auto_jti:
            jti = uuid4().hex if self.auto_jti and not self.jti else self.jti
            self.set_claim(field='jti', value=jti)

        if self.iat or self.auto_iat:
            iat = base_time if self.auto_iat and not self.iat else self.iat
            self.set_claim(field='iat', value=timegm(iat.utctimetuple()))

        if self.exp:
            exp = base_time + self.exp
            self.set_claim(field='exp', value=timegm(exp.utctimetuple()))

        if self.nbf:
            nbf = base_time + self.nbf
            self.set_claim(field='nbf', value=timegm(nbf.utctimetuple()))

    @staticmethod
    def mount_headers():
        return {}

    def encode(self):
        self.mount_claims()
        return jwt_encode(self.payload, self.signing_key, algorithm=self.algorithm, headers=self.mount_headers())


class JwtDecode(BaseJwtToken):
    verify_iss = False
    verify_aud = False
    verify_exp = False
    verify_nbf = False,
    verify_iat = False
    leeway = 0

    def __init__(self, token: str = None, verify_iss=False, verify_aud=False, verify_exp=False, verify_nbf=False,
                 verify_iat=False, leeway=0, **kwargs):
        """
            token: str -> valid jwt token, ex: ""
            verify_iss: bool -> verify jwt `issuer`
            verify_aud: bool -> verify jwt `audience`
            verify_exp: bool -> verify jwt `expiration`
            verify_nbf: bool -> verify jwt `not before time`
            verify_iat: bool -> verify jwt `issued at`
            leeway: int -> time margin for validation, ex: 30
            kwargs:
                signing_key: str -> key used to encoder, ex: "1234"
                algorithm: str -> algorithm used to encode, exs: 'HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512'
                iss: str -> set token issuer
                aud: str | [str] -> set token subject
        """
        super().__init__(**kwargs)
        self.token = token
        self.verify_iss, self.verify_aud = (verify_iss or self.verify_iss), (verify_aud or self.verify_aud)
        self.verify_exp, self.verify_nbf = (verify_exp or self.verify_exp), (verify_nbf or self.verify_nbf)
        self.verify_iat, self.leeway = (verify_iat or self.verify_iat), (leeway or self.leeway)

    def decode_raw(self):
        return jwt_decode(
            self.token,
            self.signing_key,
            algorithms=[self.algorithm] if not isinstance(self.algorithm, list) else self.algorithm,
            audience=self.aud,
            issuer=self.iss,
            leeway=self.leeway,
            options={
                'verify_iss': self.verify_iss,
                'verify_aud': self.verify_aud,
                'verify_exp': self.verify_exp,
                'verify_nbf': self.verify_nbf,
                'verify_iat': self.verify_iat,
                'verify_signature': True,
            },
        )

    def decode(self, raise_except=False):
        if raise_except:
            return self.decode_raw()
        
        else:
            try:
                return self.decode_raw()
            except InvalidAlgorithmError:
                return None
            except InvalidTokenError:
                return None
