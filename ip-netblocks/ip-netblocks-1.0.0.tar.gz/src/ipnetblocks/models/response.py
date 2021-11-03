import copy
from datetime import datetime

from .base import BaseModel
import sys

if sys.version_info < (3, 9):
    import typing


def _datetime_from_int(values: dict, key: str) -> datetime or None:
    if key in values and values[key]:
        return datetime.utcfromtimestamp(values[key])
    return None


def _string_value(values: dict, key: str) -> str:
    if key in values and values[key]:
        return str(values[key])
    return ''


def _float_value(values: dict, key: str) -> float:
    if key in values and values[key]:
        return float(values[key])
    return 0.0


def _int_value(values: dict, key: str) -> int:
    if key in values and values[key]:
        return int(values[key])
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _list_of_objects(values: dict, key: str, classname: str) -> list:
    r = []
    if key in values and type(values[key]) is list:
        r = [globals()[classname](x) for x in values[key]]
    return r


def _object_value(values: dict, classname: str) -> object:
    if values is not None:
        return globals()[classname](values)
    return 0


def _bool_value(values: dict, key: str) -> bool:
    if key in values and values[key]:
        return bool(values[key])
    return False


class AutonomousSystem(BaseModel):
    asn: int
    name: str
    type: str
    route: str
    domain: str

    def __init__(self, values):
        super().__init__()
        self.asn = 0
        self.name = ''
        self.type = ''
        self.route = ''
        self.domain = ''

        if values:
            self.asn = _int_value(values, 'asn')
            self.name = _string_value(values, 'name')
            self.type = _string_value(values, 'type')
            self.route = _string_value(values, 'route')
            self.domain = _string_value(values, 'domain')


class Contact(BaseModel):
    id: str
    person: str
    role: str
    email: str
    phone: str
    country: str
    city: str
    address: [str]

    def __init__(self, values):
        super().__init__()
        self.id = ''
        self.person = ''
        self.role = ''
        self.email = ''
        self.phone = ''
        self.country = ''
        self.city = ''
        self.address = []

        if values:
            self.id = _string_value(values, 'id')
            self.person = _string_value(values, 'person')
            self.role = _string_value(values, 'role')
            self.email = _string_value(values, 'email')
            self.phone = _string_value(values, 'phone')
            self.country = _string_value(values, 'country')
            self.city = _string_value(values, 'city')
            self.address = _list_value(values, 'address')


class Maintainer(BaseModel):
    mntner: str
    email: str

    def __init__(self, values):
        super().__init__()
        self.mntner = ''
        self.email = ''

        if values:
            self.mntner = _string_value(values, 'mntner')
            self.email = _string_value(values, 'email')


class Org(BaseModel):
    org: str
    name: str
    email: str
    phone: str
    country: str
    city: str
    postal_code: str
    address: [str]

    def __init__(self, values):
        super().__init__()
        self.org = ''
        self.name = ''
        self.email = ''
        self.phone = ''
        self.country = ''
        self.city = ''
        self.postal_code = ''
        self.address = []

        if values:
            self.org = _string_value(values, 'org')
            self.name = _string_value(values, 'name')
            self.email = _string_value(values, 'email')
            self.phone = _string_value(values, 'phone')
            self.country = _string_value(values, 'country')
            self.city = _string_value(values, 'city')
            self.postal_code = _string_value(values, 'postalCode')
            self.address = _list_value(values, 'address')


class Inetnum(BaseModel):
    inetnum: str
    inetnum_first: int
    inetnum_last: int
    parent: str
    AS: AutonomousSystem
    netname: str
    nethandle: str
    description: [str]
    modified: datetime
    country: str
    city: str
    address: [str]
    org: Org
    if sys.version_info < (3, 9):
        abuse_contact: typing.List[Contact]
        admin_contact: typing.List[Contact]
        tech_contact: typing.List[Contact]
        mnt_by: typing.List[Maintainer]
        mnt_domains: typing.List[Maintainer]
        mnt_lower: typing.List[Maintainer]
        mnt_routes: typing.List[Maintainer]
    else:
        abuse_contact: [Contact]
        admin_contact: [Contact]
        tech_contact: [Contact]
        mnt_by: [Maintainer]
        mnt_domains: [Maintainer]
        mnt_lower: [Maintainer]
        mnt_routes: [Maintainer]
    remarks: [str]
    source: str

    def __init__(self, values):
        super().__init__()
        self.inetnum = ''
        self.inetnum_first = 0
        self.inetnum_last = 0
        self.parent = ''
        self.AS = None
        self.netname = ''
        self.nethandle = ''
        self.description = []
        self.modified = None
        self.country = ''
        self.city = ''
        self.address = []
        self.abuse_contact = None
        self.admin_contact = None
        self.tech_contact = None
        self.org = None
        self.mnt_by = []
        self.mnt_domains = []
        self.mnt_lower = []
        self.mnt_routes = []
        self.remarks = []
        self.source = ''

        if values:
            self.inetnum = _string_value(values, 'inetnum')
            # self.inetnum_first = _int_value(values, 'inetnumFirst')
            # self.inetnum_last = _int_value(values, 'inetnumLast')
            self.inetnum_first = int(_string_value(values, 'inetnumFirstString'))
            self.inetnum_last = int(_string_value(values, 'inetnumLastString'))
            self.parent = _string_value(values, 'parent')
            self.AS = _object_value(values['as'], 'AutonomousSystem')
            self.netname = _string_value(values, 'netname')
            self.nethandle = _string_value(values, 'nethandle')
            self.description = _list_value(values, 'description')
            self.modified = datetime.strptime(_string_value(values, 'modified'), "%Y-%m-%dT%H:%M:%SZ")
            self.country = _string_value(values, 'country')
            self.city = _string_value(values, 'city')
            self.address = _list_value(values, 'address')
            self.abuse_contact = _list_of_objects(values, 'abuseContact', 'Contact')
            self.admin_contact = _list_of_objects(values, 'adminContact', 'Contact')
            self.tech_contact = _list_of_objects(values, 'techContact', 'Contact')
            self.org = _object_value(values['org'], 'Org')
            self.mnt_by = _list_of_objects(values, 'mntBy', 'Maintainer')
            self.mnt_domains = _list_of_objects(values, 'mntDomains', 'Maintainer')
            self.mnt_lower = _list_of_objects(values, 'mntLower', 'Maintainer')
            self.mnt_routes = _list_of_objects(values, 'mntRoutes', 'Maintainer')
            self.remarks = _list_value(values, 'remarks')
            self.source = _string_value(values, 'source')


class Response(BaseModel):
    search: str
    count: int
    limit: int
    if sys.version_info < (3, 9):
        inetnums: typing.List[Inetnum]
    else:
        inetnums: [Inetnum]

    def __init__(self, values):
        super().__init__()
        self.search = ''
        self.count = 0
        self.limit = 0
        self.inetnums = []

        if values is not None:
            self.search = _string_value(values, 'search')
            if values['result'] is not None:
                res = values['result']
                self.count = _int_value(res, 'count')
                self.limit = _int_value(res, 'limit')
                self.inetnums = _list_of_objects(res, 'inetnums', 'Inetnum')


class ErrorMessage(BaseModel):
    code: int
    message: str

    def __init__(self, values):
        super().__init__()

        self.code = 0
        self.message = ''

        if values is not None:
            self.code = _int_value(values, 'code')
            self.message = _string_value(values, 'messages')
