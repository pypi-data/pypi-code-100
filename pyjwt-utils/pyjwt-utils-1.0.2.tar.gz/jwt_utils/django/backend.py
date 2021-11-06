from jwt_utils.backend import JwtDecode as BaseDecode
from jwt_utils.backend import JwtEncode as BaseEncode
from jwt_utils.django.settings import api_settings


class JwtEncode(BaseEncode):
    signing_key = api_settings.SIGNING_KEY
    algorithm = api_settings.ALGORITHM
    iss = api_settings.ISSUER
    sub = api_settings.SUBJECT
    aud = api_settings.AUDIENCE
    exp = api_settings.EXPIRATION
    nbf = api_settings.NOT_BEFORE
    iat = api_settings.IAT
    auto_iat = api_settings.AUTO_IAT
    jti = api_settings.JTI
    auto_jti = api_settings.AUTO_JTI


class JwtDecode(BaseDecode):
    signing_key = api_settings.SIGNING_KEY
    algorithm = api_settings.ALGORITHM
    iss = api_settings.ISSUER
    aud = api_settings.AUDIENCE
    verify_iss = api_settings.VERIFY_ISSUER
    verify_aud = api_settings.VERIFY_AUDIENCE
    verify_exp = api_settings.VERIFY_EXPIRATION
    verify_nbf = api_settings.VERIFY_NOT_BEFORE
    verify_iat = api_settings.VERIFY_IAT
