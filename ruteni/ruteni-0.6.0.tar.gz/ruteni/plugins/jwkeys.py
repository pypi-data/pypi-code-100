import logging
from typing import Optional

from anyio import open_file
from jwcrypto.common import json_decode, json_encode
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT, JWTExpired
from ruteni import configuration
from ruteni.utils.jwkset import JWKSet
from starlette.applications import Starlette

logger = logging.getLogger(__name__)

JWKEYS_FILE = configuration.get("RUTENI_JWKEYS_FILE")


class KeyManager:
    def __init__(self, key_file: str) -> None:
        self.key_file = key_file
        self.public_key: JWK = None
        self.private_key: JWK = None

    @staticmethod
    def is_private(keyset: JWKSet) -> bool:
        for key in keyset:
            return key.has_private  # only check first one
        return False

    def encrypt(self, payload: str) -> str:
        protected_header = {
            "alg": "RSA-OAEP-256",
            "enc": "A256CBC-HS512",
            "typ": "JWE",
            "kid": self.public_key.get("kid"),
        }
        jwetoken = JWE(
            payload.encode("utf-8"),
            recipient=self.public_key,
            protected=protected_header,
        )
        return jwetoken.serialize()

    def decrypt(self, token: str) -> Optional[dict]:
        # @todo we should clear the access_token cookie on error
        try:
            return json_decode(JWT(jwt=token, key=self.keyset).claims)
        except JWTExpired:
            return None

    def create_token(self, claims: dict) -> str:
        # header = dict(alg='RS256', typ='JWT', kid=key.key_id)
        kid = self.private_key.get("kid")
        header = '{"alg":"RS256","typ":"JWT","kid":"' + kid + '"}'
        jwt = JWT(header=header, claims=json_encode(claims))
        jwt.make_signed_token(self.private_key)
        return jwt.serialize()

    def get_claims(self, token: str, issuer: str) -> dict:
        claims = self.decrypt(token)
        assert claims
        if claims["iss"] != issuer:
            raise Exception(f"invalid issuer, expected {issuer}, got {claims['iss']}")
        return claims

    async def startup(self, starlette: Starlette) -> None:

        async with await open_file(self.key_file) as f:
            content = await f.read()

        self.keyset = JWKSet.from_json(content)

        if len(self.keyset) == 0:
            raise Exception("empty key file")

        keyset_ids = set(int(key.get("kid")) for key in self.keyset)

        # max(self.keyset, key=lambda item: int(item.get("kid")))

        kid: Optional[str] = None
        for key in self.keyset:
            if kid is None or int(kid) < int(key.get("kid")):
                kid = key.get("kid")

        if KeyManager.is_private(self.keyset):
            logger.debug(f"private key {kid} out of {keyset_ids} from {self.key_file}")
            self.private_key = key
            self.public_key = JWK()
            self.public_key.import_key(**json_decode(self.private_key.export_public()))
        else:
            logger.debug(f"installing public keys from {self.key_file}")
            self.public_key = key
        logger.info("started")

    async def shutdown(self, starlette: Starlette) -> None:
        logger.info("stopped")


jwkeys = KeyManager(JWKEYS_FILE)
configuration.add_service("jwkeys", jwkeys.startup, jwkeys.shutdown)

logger.info("loaded")
