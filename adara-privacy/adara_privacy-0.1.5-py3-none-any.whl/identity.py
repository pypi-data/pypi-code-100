from adara_privacy.identifier import Identifier
from adara_privacy.streamers.streamer import Streamer
from adara_privacy.privacy_token import (
    Token,
    _tokenize,
    _is_token_as_dict,
)
from adara_privacy.utils import (
    sdk_config,
    is_empty_string,
)
from adara_privacy.exceptions import InstanceNotMutableError


def _is_identity_as_token_dicts(data: dict) -> bool:
    if isinstance(data, dict):
        try:
            if not isinstance(data["package_token"], str):
                return False
            tokens = data["tokens"]
            if isinstance(tokens, list) and all(_is_token_as_dict(t) for t in tokens):
                return True

        except KeyError:
            return False

    return False


def _is_identity_as_identifiers(data: dict) -> bool:
    if isinstance(data, dict):
        try:
            return isinstance(data["identifiers"], list) and all(isinstance(item, dict) for item in data["identifiers"])
        except KeyError:
            return False
    elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return True
    return False


class Identity():
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._identifiers = []
        self._tokens = []
        self._mutable = True
        self._package_token = None

        if args and all(isinstance(arg, Identifier) for arg in args):
            for arg in args:
                if not arg.is_empty:
                    self._identifiers.append(arg)
        # this handles cases for identity list instantiation
        elif len(args) == 1 and _is_identity_as_identifiers(args[0]):
            if isinstance(args[0], list):
                self._identifiers.extend(Identifier(item) for item in args[0])
            else:
                self._identifiers.extend(Identifier(item) for item in args[0]["identifiers"])
        # this is for a collection of tokens (no identifiers, will lock the instance)
        elif len(args) == 1 and _is_identity_as_token_dicts(args[0]):
            self._mutable = False
            self._package_token = args[0]["package_token"]
            self._tokens = [Token(t) for t in args[0]["tokens"]]
        elif len(args) > 0:
            raise TypeError('Arguments passed to constructor must be all of type Identifier, or a single argument as a list of deserializable token dicts.')

        if kwargs and all(isinstance(kwargs[k], (str, int, float)) for k in kwargs):
            self._identifiers.extend([Identifier(kwargs[k], identifier_type=k)] for k in kwargs)

    def add_identifier(self, identifier):
        if not self._mutable:
            raise InstanceNotMutableError("Identity")

        if isinstance(identifier, Identifier):
            if not identifier.is_empty:
                self._identifiers.append(identifier)
        else:
            raise TypeError('Argument "identifier" must be an instance of type Identifier.')

    @property
    def identifiers(self):
        return list(self._identifiers)

    @property
    def tokens(self):
        if not self._mutable and self._tokens:
            return self._tokens
        else:
            return [
                identifier.token for identifier in self._identifiers
            ]

    def get_package_token(self, private_salt: str = None):
        if not self._mutable:
            return self._package_token

        if is_empty_string(private_salt):
            try:
                private_salt = sdk_config.privacy.private_salt
            except AttributeError:
                raise ValueError('A "private" salt must be specified, either via configuration or as an argument.') from None
        return _tokenize(':'.join(sorted({t.get_private(private_salt=private_salt) + t.identifier_type for t in self.tokens})), private_salt)

    package_token = property(get_package_token)

    def save(self, streamer):
        if not isinstance(streamer, Streamer):
            raise TypeError('Argument "streamer" must be an instance of type "Streamer".')
        streamer.save(self)

    def to_dict(self, format: str = 'identity', private_salt: str = None, salts: dict = None, **kwargs):
        if format == 'identity':
            return {
                'identifiers': [i.to_dict() for i in self._identifiers]
            }
        elif format == 'token':
            return self.to_tokens(private_salt=private_salt, salts=salts, **kwargs)
        else:
            raise ValueError('Argument "format" must be either "identity" (default) or "token".')

    def to_tokens(self, private_salt: str = None, salts: dict = None, **kwargs):
        if not self._mutable:
            return {
                'package_token': self._package_token,
                'tokens': [t.to_dict() for t in self._tokens]
            }
        else:
            return {
                'package_token': self.get_package_token(private_salt=private_salt),
                'tokens': [i.token.to_dict(private_salt=private_salt, salts=salts, **kwargs) for i in self._identifiers]
            }

    def __eq__(self, other):
        pass
