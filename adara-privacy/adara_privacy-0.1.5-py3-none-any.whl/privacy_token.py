import hashlib

from adara_privacy.utils import (
    sdk_config,
    is_empty_string,
)

from adara_privacy.exceptions import MissingEnvironmentVariableError

import adara_privacy

KEY_TOKEN_TYPE = 'type'
KEY_TOKEN_COMMON = 'common'
KEY_TOKEN_PRIVATE = 'private'
KEY_TOKEN_ROOT = 'root'


def _tokenize(value: str, salt: str) -> str:
    return hashlib.sha256(str(salt + hashlib.sha256(value.encode()).hexdigest()).encode()).hexdigest()


def _is_token_as_dict(data: dict) -> bool:
    if isinstance(data, dict):
        try:
            # private key required
            if not "private" in data:
                return False
            # return true if all keys are strings
            return all(isinstance(data[k], str) for k in data)
        except KeyError:
            return False


class Token():
    def __init__(self, *args, identifier=None, token_dict: dict = None):
        super().__init__()
        self._identifier = None
        self._private_token = None
        self._root_token = None
        self._common_tokens = None

        if len(args) == 1:
            if identifier or token_dict:
                raise ValueError("Token constructor accepts a single input and multiple were given.")
            if isinstance(args[0], adara_privacy.Identifier):
                identifier = args[0]
            elif _is_token_as_dict(args[0]):
                token_dict = args[0]
            else:
                raise TypeError("Token constructor only accepts either an Identifier instance or dict.")
        elif len(args) > 1:
            raise ValueError("Token constructor accepts a single input and multiple were given.")

        if identifier and token_dict:
            raise ValueError("Token constructor accepts a single input and multiple were given.")
        elif not (identifier or token_dict):
            raise ValueError("Token constructor requires a single input but none was given.")

        if isinstance(identifier, adara_privacy.Identifier):
            self._identifier = identifier
        elif isinstance(token_dict, dict):
            self._common_tokens = dict()
            for k in token_dict:
                if k == KEY_TOKEN_PRIVATE:
                    self._private_token = token_dict[KEY_TOKEN_PRIVATE]
                elif k == KEY_TOKEN_ROOT:
                    self._root_token = token_dict[KEY_TOKEN_ROOT]
                elif k == KEY_TOKEN_TYPE:
                    self._identifier_type = token_dict[KEY_TOKEN_TYPE]
                else:
                    self._common_tokens[k] = token_dict[k]
        else:
            raise Exception('Token() was not passed arguments required for instantiation.')

    @property
    def identifier_type(self):
        return self._identifier.identifier_type if self._identifier else self._identifier_type

    def get_common(self, salts: dict = None, **kwargs):
        if self._common_tokens:
            return self._common_tokens

        if salts and not isinstance(salts, dict):
            raise TypeError('Argument "salts" must be of type "dict".')

        if salts or kwargs:
            if salts and kwargs:
                common_salts = {**salts, **kwargs}
            elif salts:
                common_salts = salts
            else:
                common_salts = kwargs
        elif sdk_config and sdk_config.privacy:
            common_salts = sdk_config.privacy.common_salts
        else:
            common_salts = {}

        return {k: _tokenize(self._identifier.tokenization_value, common_salts[k]) for k in common_salts}

    common = property(get_common)

    def get_private(self, private_salt=None):
        if self._private_token:
            return self._private_token

        if is_empty_string(private_salt):
            try:
                private_salt = sdk_config.privacy.private_salt
            except AttributeError:
                raise ValueError('A "private" salt must be specified, either via configuration or as an argument.') from None

        return _tokenize(self._identifier.tokenization_value, private_salt)

    private = property(get_private)

    def get_root(self):
        if self._root_token:
            return self._root_token
        elif self._identifier:
            return self._identifier.tokenization_value
        else:
            return None

    root = property(get_root)

    def to_dict(self, private_salt: str = None, salts: dict = None, **kwargs):
        if is_empty_string(private_salt):
            if (salts and isinstance(salts, dict)) or kwargs:
                try:
                    private_salt = salts[KEY_TOKEN_PRIVATE]
                except KeyError:
                    pass
                if is_empty_string(private_salt):
                    try:
                        private_salt = kwargs[KEY_TOKEN_PRIVATE]
                    except KeyError:
                        pass
                else:
                    if KEY_TOKEN_PRIVATE in kwargs and kwargs[KEY_TOKEN_PRIVATE] != private_salt:
                        raise ValueError('Salt value for "private" was passed more than once.')
        elif (salts and isinstance(salts, dict)) or kwargs:
            if (salts and KEY_TOKEN_PRIVATE in salts and salts[KEY_TOKEN_PRIVATE] != private_salt) or (kwargs and KEY_TOKEN_PRIVATE in kwargs and kwargs[KEY_TOKEN_PRIVATE] != private_salt):
                raise ValueError('Salt value for "private" was passed more than once.')

        root = {}
        if sdk_config.privacy.transmit_root_token and self.root:
            root[KEY_TOKEN_ROOT] = self.root

        tokens = {KEY_TOKEN_PRIVATE: self.get_private(private_salt=private_salt), **self.get_common(salts=salts, **kwargs)}
        if self._identifier and self._identifier.common_tokens:
            tokens = {k: tokens[k] for k in tokens if k in set(self._identifier.common_tokens)}

        metadata = {KEY_TOKEN_TYPE: self.identifier_type}
        if self._identifier and self._identifier.label:
            metadata['label'] = self._identifier.label

        return {**root, **tokens, **metadata}
