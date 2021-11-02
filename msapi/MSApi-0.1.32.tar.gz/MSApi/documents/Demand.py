from MSApi.MSLowApi import MSLowApi, error_handler, string_to_datetime
from MSApi.State import State
from MSApi.Organization import Account
from MSApi.Attribute import Attribute
from MSApi.Counterparty import Counterparty
from MSApi.ObjectMS import ObjectMS, check_init
from typing import Optional
from datetime import datetime
from MSApi.documents import CustomerOrder


class Demand(ObjectMS):

    @classmethod
    def gen_states(cls):
        response = MSLowApi.auch_get(f"entity/demand/metadata")
        error_handler(response)
        for states_json in response.json()["states"]:
            yield State(states_json)

    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_account_id(self) -> str:
        return self._json.get('accountId')

    @check_init
    def get_sync_id(self) -> Optional[str]:
        return self._json.get('syncId')

    @check_init
    def get_updated_time(self) -> datetime:
        return string_to_datetime(self._json.get('updated'))

    @check_init
    def get_deleted_time(self) -> Optional[datetime]:
        return self._get_optional_object('deleted', string_to_datetime)

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')

    @check_init
    def get_description(self) -> Optional[str]:
        return self._json.get('description')

    @check_init
    def get_code(self) -> Optional[str]:
        return self._json.get('code')

    @check_init
    def get_external_code(self) -> Optional[str]:
        return self._json.get('externalCode')

    @check_init
    def get_moment_time(self) -> datetime:
        return string_to_datetime(self._json.get('moment'))

    @check_init
    def is_applicable(self) -> bool:
        return bool(self._json.get('applicable'))

    @check_init
    def is_vat_enabled(self) -> bool:
        return bool(self._json.get('vatEnabled'))

    @check_init
    def is_vat_included(self) -> Optional[bool]:
        return self._get_optional_object('vatIncluded', bool)

    @check_init
    def get_agent(self) -> Optional[Counterparty]:
        return self._get_optional_object('agent', Counterparty)

    @check_init
    def get_state(self) -> Optional[State]:
        return self._get_optional_object('state', State)

    @check_init
    def gen_attributes(self):
        for attr in self._json.get('attributes', []):
            yield Attribute(attr)

    def get_attribute_by_name(self, name: str) -> Optional[Attribute]:
        for attr in self.gen_attributes():
            if attr.get_name() == name:
                return attr
        return None

    @check_init
    def get_organization_account(self) -> Optional[Account]:
        result = self._json.get('organizationAccount')
        if result is not None:
            return Account(result)
        return None


def create_demand(demand: Demand, **kwargs) -> Demand:
    response = MSLowApi.auch_post(f'entity/demand', json=demand.get_json(), **kwargs)
    error_handler(response)
    return Demand(response.json())


def get_demand_template_by_customer_order(customer_order: CustomerOrder, **kwargs) -> Demand:
    json_data = {
        "customerOrder": {
            "meta": customer_order.get_meta().get_json()
        }
    }
    response = MSLowApi.auch_put(f'entity/demand/new', json=json_data, **kwargs)
    error_handler(response)
    return Demand(response.json())


