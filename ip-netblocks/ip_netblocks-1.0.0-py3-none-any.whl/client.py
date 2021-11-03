import datetime
from json import loads, JSONDecodeError
import re

from .net.http import ApiRequester
from .models.response import Response
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError


class Client:
    __default_url = "https://ip-netblocks.whoisxmlapi.com/api/v2"
    _api_requester: ApiRequester or None
    _api_key: str
    _last_result: Response or None

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)
    _re_domain_name = re.compile(
        r'^(?:[0-9a-z_](?:[0-9a-z-_]{0,62}(?<=[0-9a-z-_])[0-9a-z_])?\.)+'
        + r'[0-9a-z][0-9a-z-]{0,62}[a-z0-9]$', re.IGNORECASE
    )
    _re_ipv4 = re.compile(
        r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}'
        + r'([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    )
    _re_ipv6 = re.compile(
        r'^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}'
        + r'(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|'
        + r'(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
        + r'(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}'
        + r'(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
        + r'(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})'
        + r'|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)'
        + r'(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}'
        + r'(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:'
        + r'((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))'
        + r'|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:'
        + r'((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|'
        + r'(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:'
        + r'((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$'
    )

    _SUPPORTED_FORMATS = ['json', 'xml']
    _PARSABLE_FORMAT = 'json'

    JSON_FORMAT = 'json'
    XML_FORMAT = 'xml'

    __DATETIME_OR_NONE_MSG = 'Value should be None or an instance of ' \
                             'datetime.date'

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :key base_url: str: (optional) API endpoint URL.
        :key timeout: float: (optional) API call timeout in seconds
        """

        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url

        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def last_result(self) -> Response or None:
        return self._last_result

    @last_result.setter
    def last_result(self, value: Response or None):
        if value is None:
            self._last_result = value
        elif isinstance(value, Response):
            self._last_result = value
        else:
            raise ValueError(
                "Values should be an instance of ipnetblocks.Response or None")

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def get(self, ip: str = None,
            asn: int = None,
            org: str = None,
            mask: int = None,
            limit: int = 100) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :key ip: Required. Get ranges by IPv4/IPv6 address or by CIDR depending on input.
            Also, the search by CIDR could be done with the optional mask parameter.
        :key asn: Get ranges by ASN (Autonomous System Number).
            Required one of the following input fields: ip, org, asn.
        :key org: Find IP Netblocks which have the specified search terms
            in their Netblock (netname, description, remarks), or Organisation
            (org.org, org.name, org.email, org.address) fields.
            Required one of the following input fields: ip, org, asn.
        :key mask: Optional for ip parameter only. Get ranges by CIDR.
            Acceptable values: 0 - 128 (0 - 32 for IPv4). Default: 128
        :key limit: Max count of returned records.
            Acceptable values: 1 - 1000
        :return: `Response` instance
        :raises ConnectionError:
        :raises IpNetblocksApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        response = self.get_raw(ip=ip, asn=asn, org=org, mask=mask,
                                limit=limit, output_format=Client._PARSABLE_FORMAT)
        return self._parse_raw_result(response)

    def get_raw(self, ip: str = None,
                asn: int = None,
                org: str = None,
                mask: int = None,
                limit: int = 100,
                output_format:
                str = _PARSABLE_FORMAT) -> str:
        """
        Get raw API response.

        :key ip: Required. Get ranges by IPv4/IPv6 address or by CIDR depending on input.
            Also, the search by CIDR could be done with the optional mask parameter.
        :key asn: Get ranges by ASN (Autonomous System Number).
            Required one of the following input fields: ip, org, asn.
        :key org: Find IP Netblocks which have the specified search terms
            in their Netblock (netname, description, remarks), or Organisation
            (org.org, org.name, org.email, org.address) fields.
            Required one of the following input fields: ip, org, asn.
        :key mask: Optional for ip parameter only. Get ranges by CIDR.
            Acceptable values: 0 - 128 (0 - 32 for IPv4). Default: 128
        :key limit: Max count of returned records.
            Acceptable values: 1 - 1000
        :key output_format: Optional.
            Use Client.JSON_FORMAT and Client.XML_FORMAT constants
        :return: str
        :raises ConnectionError:
        :raises IpNetblocksApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """

        if self.api_key == '':
            raise EmptyApiKeyError('')
        if ip is None and asn is None and org is None:
            raise ParameterError("Required one of the following input fields: ip, org, asn.")

        _ip = Client._validate_ip_address(ip)
        _mask = Client._validate_mask(mask, ip)
        _output_format = Client._validate_output_format(output_format)
        _limit = Client._validate_limit(limit)
        _asn = Client._validate_asn(asn)
        _org = Client._validate_org(org)

        return self._api_requester.get(self._build_payload(
            self.api_key,
            _ip,
            _asn,
            _org,
            _mask,
            _limit,
            _output_format,
        ))

    def get_by_asn(self, asn: int, limit: int = 100) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :key asn: Required. The Autonomous System number.
        :key limit: Max count of returned records.
            Acceptable values: 1 - 1000
        :return: `Response` instance
        :raises ConnectionError:
        :raises IpNetblocksApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """
        response = self.get_raw(asn=asn, limit=limit, output_format=Client._PARSABLE_FORMAT)
        return self._parse_raw_result(response)

    def get_by_org(self, org: str, limit: int = 100) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :key org: Required. str or [str] for multiple terms.
            Find IP Netblocks which have the specified search terms
            in their Netblock (netname, description, remarks), or Organisation
            (org.org, org.name, org.email, org.address) fields.
        :key limit: Max count of returned records.
            Acceptable values: 1 - 1000
        :return: `Response` instance
        :raises ConnectionError:
        :raises IpNetblocksApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """
        response = self.get_raw(org=org, limit=limit, output_format=Client._PARSABLE_FORMAT)
        return self._parse_raw_result(response)

    def _parse_raw_result(self, response: str) -> Response:
        try:
            parsed = loads(str(response))
            if 'result' in parsed:
                self.last_result = Response(parsed)
                return self.last_result
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    @staticmethod
    def _validate_api_key(api_key) -> str:
        if Client._re_api_key.search(str(api_key)):
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_domain_name(value) -> str:
        if Client._re_domain_name.search(str(value)):
            return str(value)

        raise ParameterError("Invalid domain name")

    @staticmethod
    def _validate_ip_address(value) -> str:
        if value is None:
            return None
        if Client._re_ipv4.search(str(value)) or \
                Client._re_ipv6.search(str(value)):
            return str(value)

        raise ParameterError("Invalid ip address name")

    @staticmethod
    def _validate_output_format(value: str):
        if value.lower() in [Client.JSON_FORMAT, Client.XML_FORMAT]:
            return value.lower()

        raise ParameterError(
            f"Response format must be {Client.JSON_FORMAT} "
            f"or {Client.XML_FORMAT}")

    @staticmethod
    def _validate_date(value: datetime.date or None):
        if value is None or isinstance(value, datetime.date):
            return str(value)

        raise ParameterError(Client.__DATETIME_OR_NONE_MSG)

    @staticmethod
    def _validate_mask(value: int or None, ip: str):
        if value is None or \
                (isinstance(value, int) and
                 ((0 < value <= 128 and Client._re_ipv6.search(ip)) or
                  (0 < value <= 32 and Client._re_ipv4.search(ip)))):
            return value

        raise ParameterError("mask should be an int between 0 and 32 for IPv4"
                             " (0 and 128 for IPv6) or None")

    @staticmethod
    def _validate_asn(value):
        if (value is None or
                (isinstance(value, int) and (0 < value <= 4294967295))):
            return value

        raise ParameterError("asn should be an int between 1 and 4294967295 or None")

    @staticmethod
    def _validate_limit(value):
        if (value is None or
                (isinstance(value, int) and (0 < value <= 1000))):
            return value

        raise ParameterError("limit should be an int between 1 and 1000 or None")

    @staticmethod
    def _validate_org(value):
        if (value is None or
                (isinstance(value, str) and (value != '')) or
                (isinstance(value, list) and (len(value) > 0))):
            return value

        raise ParameterError("org should be str or [str] or None")

    @staticmethod
    def _build_payload(
            api_key,
            ip,
            asn,
            org,
            mask,
            limit,
            output_format
    ) -> dict:
        tmp = {
            'apiKey': api_key,
            'ip': ip,
            'asn': asn,
            'org[]': org,
            'mask': mask,
            'limit': limit,
            'outputFormat': output_format
        }

        return {k: v for (k, v) in tmp.items() if v is not None}
