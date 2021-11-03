import re
from collections import UserString
from pydantic import constr, conint
from pydantic.typing import Literal, Dict, List, Type, Tuple

from net_models.validators import *
from net_models.config import LOGGER_FIELDS
from net_models.utils import get_logger, BASE_INTERFACE_REGEX, INTERFACE_NAMES

LOGGER = LOGGER_FIELDS


BASE_INTERFACE_NAME = constr(regex=BASE_INTERFACE_REGEX.pattern)
INTERFACE_NAME = constr(regex=BASE_INTERFACE_REGEX.pattern)

# INTERFACE_NAME = Literal['Ethernet', 'FastEthernet', 'GigabitEthernet', 'TenGigabitEthernet', 'TwentyFiveGigE', 'FortyGigabitEthernet', 'HundredGigE', 'Port-channel', 'Tunnel', 'Vlan', 'BDI', 'Loopback', 'Serial', 'pseudowire']
GENERIC_OBJECT_NAME = constr(strip_whitespace=True, regex=r"\S+")
GENERIC_INTERFACE_NAME = constr(strip_whitespace=True, regex=r"\S+")
LAG_MODE = Literal["active", "passive", "desirable", "auto", "on"]

VRF_NAME = constr(strip_whitespace=True, regex=r"\S+")
VLAN_ID = conint(ge=1, le=4094)
BRIDGE_DOMAIN_ID = conint(ge=1)
CLASS_OF_SERVICE = conint(ge=0, le=7)
ROUTE_MAP_NAME = GENERIC_OBJECT_NAME
ASN = conint(ge=1, le=4294967295)



AFI = Literal["ipv4", "ipv6", "vpnv4", "vpnv6"]
SAFI = Literal["unicast", "multicast"]

ISIS_LEVEL = Literal['level-1', 'level-2']
HSRP_GROUP_NAME = constr(regex=r'\S{1,25}')
interface_name = constr(min_length=3)
SWITCHPORT_MODE = Literal["access", "trunk", "dynamic auto", "dynamic desirable", "dot1q-tunnel", "private-vlan host", "private-vlan promiscuous"]

PRIVILEGE_LEVEL = conint(ge=0, le=15)
AAA_METHOD_NAME = Union[Literal['default'], GENERIC_OBJECT_NAME]


ROUTE_TARGET = constr(regex=r"((?:(?:\d{1,3}\.){3}(?:\d{1,3}))|(?:\d+)):(\d+)")
ROUTE_DISTINGUISHER = ROUTE_TARGET
L2_PROTOCOL = Literal['R4', 'R5', 'R6', 'R8', 'R9', 'RA', 'RB', 'RC', 'RD', 'RF', 'cdp', 'dot1x', 'dtp', 'elmi', 'esmc', 'lacp', 'lldp', 'pagp', 'ptppd', 'stp', 'udld', 'vtp']

class BaseInterfaceName(str):

    INTERFACE_NAMES: Dict[str, str] = None
    INTERFACE_REGEX: Type[re.Pattern] = None
    INTERFACE_TYPE_WEIGHT_MAP: Dict[int, List[str]] = None
    INTEFACE_TYPE_MAX_WEIGHT: int = 255
    INTEFACE_TYPE_DEFAULT_WEIGHT: int = 50

    def __new__(cls, v):
        v = cls.validate_name(v=v)
        return super().__new__(cls, v)


    @classmethod
    def split_interface(cls, interface_name: str) -> Tuple[str, str]:
        try:
            match = re.match(pattern=cls.INTERFACE_REGEX, string=interface_name)
        except TypeError as e:
            LOGGER.error("Expected string or bytes-like object, cannot match on '{}'".format(type(interface_name)))
            return (None, None)
        if match:
            return [match.group("type"), match.group("numbers")]
        else:
            LOGGER.error("Given interface '{}' did not match parsing pattern.".format(interface_name))
            return (None, None)

    @classmethod
    def normalize_interface_name(cls, interface_name: str) -> str:
        interface_type, interface_num = cls.split_interface(interface_name=interface_name)
        if any([x is None for x in [interface_type, interface_num]]):
            msg = f"Failed to split interface_name '{interface_name}'"
            raise ValueError(msg)

        match_found = False
        if interface_type in cls.INTERFACE_NAMES.keys():
            match_found = True
            interface_name = interface_type + interface_num

        if not match_found:
            for full_type, short_types in cls.INTERFACE_NAMES.items():
                for short_type in short_types:
                    if interface_type.lower().startswith(short_type.lower()):
                        match_found = True
                        interface_name = full_type + interface_num

        if not match_found:
            msg = f"Given interface name does not comply with valid interface names for {cls.__name__}. Given: {interface_name}, Expected: {list(INTERFACE_NAMES.keys())}"
            LOGGER.error(msg=msg)
            raise AssertionError(msg)
        else:
            return interface_name

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_name

    @classmethod
    def validate_name(cls, v: str):
        if not isinstance(v, (str, UserString)):
            msg = f"Interface name has to be str, got {type(v)}"
            LOGGER.error(msg=msg)
            raise TypeError(f"Interface name has to be str, got {type(v)}")
        # This is ordinary <class 'str'>
        interface_name = cls.normalize_interface_name(interface_name=v)
        return interface_name

    @property
    def interface_type(self):
        return self.split_interface(interface_name=self)[0]

    @property
    def interface_number(self):
        return self.split_interface(interface_name=self)[1]

    @property
    def short(self):
        return f"{self.INTERFACE_NAMES[self.interface_type][0]}{self.interface_number}"

    @property
    def long(self):
        self.normalize_interface_name(interface_name=self)



class IosInterfaceName(BaseInterfaceName):

    INTERFACE_REGEX = re.compile(pattern=r"(?P<type>^[A-z]{2,}(?:[A-z\-])*)(?P<numbers>\d+(?:\/\d+)*(?:\:\d+)?(?:\.\d+)?)(\s*)$")
    INTERFACE_NAMES = {
        "Ethernet": ["Et", "Eth"],
        "FastEthernet": ["Fa"],
        "GigabitEthernet": ["Gi"],
        "TenGigabitEthernet": ["Te"],
        "TwentyFiveGigE": ["Twe"],
        "FortyGigabitEthernet": ["Fo"],
        "HundredGigE": ["Hu"],
        "Port-channel": ["Po"],
        "Tunnel": ["Tu"],
        "Vlan": ["Vl"],
        "BDI": ["BDI"],
        "Loopback": ["Lo"],
        "Serial": ["Se"],
        "pseudowire": ["pw"],
        "CEM": ["CEM"]
    }
    INTERFACE_TYPE_WEIGHT_MAP = {
        100: ["Loopback"],
        95: ["Vlan"],
        90: ["BDI"],
        80: ["Tunnel"],
        75: ["pseudowire"],
        40: ['Port-channel']

    }

class InterfaceName(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_name

    @classmethod
    def validate_name(cls, v: str):
        if not isinstance(v, (str, UserString)):
            msg = f"Interface name has to be str, got {type(v)}"
            LOGGER.error(msg=msg)
            raise TypeError(f"Interface name has to be str, got {type(v)}")
        # This is ordinary <class 'str'>
        interface_name = normalize_interface_name(interface_name=v)
        return interface_name


class DoubleQoutedString(str):

    pass

class Jinja2String(DoubleQoutedString):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_jinja

    @classmethod
    def validate_jinja(cls, v: str):
        jinja_pattern = re.compile(pattern=r"^\{\{.*?\}\}$", flags=re.MULTILINE)
        if not jinja_pattern.match(v):
            msg = f"Jinja2 String must start with '{{{{' and end with '}}}}'. Got '{v}'"
            # LOGGER.warning(msg=msg)
            raise AssertionError(msg)
        return cls(v)

JINJA_OR_NAME = Union[Jinja2String, GENERIC_OBJECT_NAME]