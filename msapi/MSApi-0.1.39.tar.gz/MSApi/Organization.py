from MSApi.ObjectMS import ObjectMS, check_init
from MSApi.MSLowApi import MSLowApi, error_handler
from MSApi.Employee import Employee
from MSApi.Meta import Meta
from typing import Optional


class Account(ObjectMS):

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

    def get_account_number(self) -> str:
        return self._json.get('accountNumber')


class Organization(ObjectMS):

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

    @check_init
    def get_owner(self) -> Optional[Employee]:
        return Employee(self._json.get('owner'))

    @check_init
    def get_shared(self) -> bool:
        return self._json.get('shared')

    @check_init
    def get_group(self) -> Optional[Meta]:
        return self._json.get('group')

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')

    def gen_accounts(self):
        response = MSLowApi.auch_get(f"entity/organization/{self.get_id()}/accounts")
        error_handler(response)
        for account_json in response.json()["rows"]:
            yield Account(account_json)

