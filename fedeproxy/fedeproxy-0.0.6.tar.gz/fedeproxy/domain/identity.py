import dataclasses
import hashlib
import os
from typing import List

from Crypto import Random
from Crypto.PublicKey import RSA

from ..format import format


@dataclasses.dataclass
class Identity(object):
    url: str = None
    public: str = None
    emails: List[str] = dataclasses.field(default_factory=list)
    owned: bool = False

    def asdict(self):
        return dataclasses.asdict(self)

    def create_key(self):
        random_generator = Random.new().read
        key = RSA.generate(2048, random_generator)
        self.private = key.export_key().decode("utf8")
        self.public = key.publickey().export_key().decode("utf8")

    def is_staged(self):
        return len(self.emails) == 0

    def is_owned(self):
        return self.owned


@dataclasses.dataclass
class IdentityPrivate(Identity):
    token: str = None
    private: str = None


@dataclasses.dataclass
class IdentityPublic(Identity):
    def from_private(self, identity):
        self.emails = [hashlib.sha256(e.encode("UTF-8")).hexdigest() for e in identity.emails]
        self.url = identity.url
        self.owned = identity.owned
        self.public = identity.public


class Identities(object):
    def __init__(self, d):
        self.d = d
        if not os.path.exists(self.d):
            os.makedirs(self.d)
        self.p = f"{self.d}/identities.json"
        self.email = None
        self.identities = []

    def load(self):
        if os.path.exists(self.p):
            f = format.FormatIdentities()
            identities = f.load(self.p)
            f.validate(identities)
            for i in identities:
                self.identities.append(self.IdentityClass(**i))
            return True
        else:
            return False

    def save(self):
        format.FormatIdentities().save(self.p, [i.asdict() for i in self.identities])

    def lookup(self, cmp):
        for i in self.identities:
            if cmp(i):
                return i
        return None


class IdentitiesPrivate(Identities):

    IdentityClass = IdentityPrivate


class IdentitiesPublic(Identities):

    IdentityClass = IdentityPublic
