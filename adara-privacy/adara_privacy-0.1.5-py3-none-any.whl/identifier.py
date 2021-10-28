from adara_privacy.utils import (
    is_stringable,
    is_empty_string,
    sdk_config,
)
import adara_privacy.privacy_token as tokens

IDENTIFIER_KEYWORDS = {
    'social_security': {'social_security'},
    'passport': {'passport'},
    'drivers_license': {'drivers_license'},
    'state_id': {'state_id'},
    'email': {'email'},
    'hashed_email': {'hashed_email'},  # TODO: Change to sha256 name
    'membership_id': {'membership_id'},
    'customer_id': {'customer_id'},
    'cookie': {'cookie'},
    'streetname_zipcode': {'street_name', 'zip_code'},
}


class Identifier():
    KEY_GENERIC_IDENTIFIER = "general"

    def __init__(self, *args, identifier_type: str = None, identifier_dict: dict = None, common_tokens: list = None,
                 label: str = None, **kwargs):
        super().__init__()
        self._general_values = []
        self._named_values = dict()
        self._identifier_type = None
        self._token = None
        self._common_tokens = None
        self._label = None

        if identifier_type:
            if isinstance(identifier_type, str) and identifier_type.strip().lower() in {k for k in
                                                                                        IDENTIFIER_KEYWORDS.keys()}:
                self._identifier_type = identifier_type.strip().lower()
            else:
                raise TypeError(
                    'Argument "identifier_type" be must a valid string value representing a known identifier type.')

        if common_tokens:
            if isinstance(common_tokens, list) and all(isinstance(i, str) for i in common_tokens):
                self._common_tokens = list(common_tokens)
            elif isinstance(common_tokens, str):
                self._common_tokens = [t.strip() for t in common_tokens.replace(';', ',').split(',') if t.strip() != '']
            else:
                raise TypeError('Argument "common_tokens" must be a string (CSV accepted) or list of strings.')

        if label:
            if isinstance(label, str):
                self._label = label.strip()
            elif label:
                raise TypeError('Argument "label" must be of type "str".')
            else:
                self._label = None

        if identifier_dict:
            if isinstance(identifier_dict, dict):
                self._identifier_type, self._general_values, self._named_values = self._extract_values(
                    self._identifier_type, **identifier_dict)
            else:
                raise TypeError('Argument "identifier_dict" must be of type "dict".')
            if identifier_type or len(args) > 0 or len(kwargs) > 0:
                raise ValueError('When argument "identifier_dict" is provided, it must be the only argument.')

        elif args or kwargs:

            if len(args) == 1 and isinstance(args[0], dict) and not kwargs:
                self._identifier_type, self._general_values, self._named_values = self._extract_values(
                    self._identifier_type, **args[0])
            elif (not args or all(is_stringable(arg) for arg in args)) and (
                    not kwargs or all(is_stringable(kwargs[k]) for k in kwargs.keys())):
                self._identifier_type, self._general_values, self._named_values = self._extract_values(
                    self._identifier_type, *args, **kwargs)
                if (
                        sdk_config is None or not sdk_config.privacy.ignore_empty_identifiers) and not self._general_values and not self._named_values:
                    raise ValueError(
                        'At least one identifier argument must be passed as a non-empty string or number value.  You can skip this error by setting the configuration "privacy.ignore_empty_identifiers" to True.')
            else:
                raise TypeError(
                    'Positional arguments must be either all strings (used as identifiers) or must be a single instance of "dict".')
        else:
            raise TypeError(
                'Missing argument value: at least one identifier argument must be passed as a non-empty string or number value.')

    def _extract_values(self, current_identifier_type: str, *args, **kwargs) -> (str, list, dict):
        general_values = list()
        derived_identifier_type = current_identifier_type

        for arg in args:
            # this allows a positional argument to specify the identifier type
            if not derived_identifier_type and arg.strip().lower() in {k for k in IDENTIFIER_KEYWORDS.keys()}:
                derived_identifier_type = arg.strip().lower()
            elif not is_empty_string(arg):
                general_values.append(arg)

        # check kwargs for a identifier combo that we can match
        if not derived_identifier_type:
            id_keys = {k.lower() for k in kwargs}
            for k in IDENTIFIER_KEYWORDS:
                if IDENTIFIER_KEYWORDS[k] == id_keys:
                    derived_identifier_type = k
                    break

            if not derived_identifier_type:
                id_types = set(IDENTIFIER_KEYWORDS.keys())
                for k in id_keys:
                    if isinstance(kwargs[k], list) and k in id_types:
                        derived_identifier_type = k
                        break

        return derived_identifier_type, general_values, dict(**kwargs)

    @property
    def tokenization_value(self) -> str:
        # start with the positional argument values
        v = list(self._general_values)
        # add in keyword argument values
        for k in self._named_values:
            if isinstance(self._named_values[k], list):
                v.extend(self._named_values[k])
            else:
                v.append(self._named_values[k])
        # return the value list, sorted and lower-cased
        token_value = ':'.join(sorted(v.strip().lower() for v in v))
        return tokens._tokenize(token_value, "root")

    @property
    def token(self) -> tokens.Token:
        if not self._token and not self.is_empty:
            self._token = tokens.Token(self)
        return self._token

    @property
    def identifier_type(self) -> str:
        return self._identifier_type if self._identifier_type else Identifier.KEY_GENERIC_IDENTIFIER

    @property
    def label(self) -> str:
        return self._label

    @property
    def common_tokens(self) -> list:
        return self._common_tokens

    @property
    def is_empty(self) -> bool:
        return not (self._general_values or self._named_values)

    @property
    def values(self):
        general_values = list(self._general_values)
        named_values = dict()
        for k in self._named_values:
            if k == self._identifier_type:
                general_values.append(self._named_values[k])
            else:
                named_values[k] = self._named_values[k]
        general_values_dict = dict()
        if general_values:
            general_values_dict[self._identifier_type if self._identifier_type else 'value'] = general_values[0] if len(
                general_values) == 1 else general_values
        return {
            **general_values_dict,
            **named_values,
        }

    def to_dict(self):
        # TODO: add additional attributes here (ex: label)
        return self.values

    def __eq__(self, other):
        return True
