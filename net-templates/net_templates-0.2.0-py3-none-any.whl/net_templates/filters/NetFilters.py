import json
import ipaddress
from copy import deepcopy
import jmespath
from pydantic.typing import Callable, Union, Dict, List, Literal

from net_models.utils.get_logger import get_logger
from net_models.models import models_map
from net_models.models.BaseModels import BaseNetModel
from net_models.inventory.Config import VLANHostMapping


def namespace_decorator(namespace: str = None):
    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> dict:
            mapping = function(*args, **kwargs)
            if namespace is not None:
                return {f"{namespace}.{k}": v for k, v in mapping.items()}
            else:
                return mapping

        return wrapper

    return decorator


class NetFilters(object):

    def __init__(self):
        self.logger = get_logger(name="NetFilters")

    @namespace_decorator(namespace='mihudec.net_filters')
    def filters(self):
        filters = {}
        for name, method in self.__class__.__dict__.items():
            if not name.startswith("_") and callable(method):
                filters[name] = getattr(self, name)
        del filters["filters"]
        return filters

    def to_model(self, data: Union[Dict, List], model: str, many: bool = True, serialize: bool = True,
                 dict_params: dict = None) -> Union[dict, list]:
        if dict_params is not None:
            dict_params = self._parse_pydantic_filter(data=dict_params)
        model_data = None
        model_class: BaseNetModel = models_map.get(model)
        if model_class is None:
            msg = f"Unknown model: '{model}'. Current models are: '{models_map}'."
            self.logger.error(msg=msg)
            raise ValueError(msg)
        # dict_params must be a dict or none
        if dict_params is not None:
            if not isinstance(dict_params, dict):
                msg = f"Got unexpected type for 'dict_params'. Expected Union[dict, None], got {type(dict_params)} ({dict_params}) instead."
                self.logger.error(msg=msg)
                dict_params = None
        if many is False:
            if isinstance(data, dict):
                if serialize:
                    if dict_params is not None:
                        model_data = model_class.parse_obj(data).serial_dict(**dict_params)
                    else:
                        model_data = model_class.parse_obj(data).serial_dict()
                else:
                    model_data = model_class.parse_obj(data)
            else:
                msg = f"Got unexpected type of data. Expected dict, got {type(data)}."
                self.logger.error(msg=msg)
                raise TypeError(msg)

        elif many is True:
            if isinstance(data, list):
                if serialize:
                    if dict_params is not None:
                        model_data = [model_class.parse_obj(x).serial_dict(**dict_params) for x in data]
                    else:
                        model_data = [model_class.parse_obj(x).serial_dict() for x in data]
                else:
                    model_data = [model_class.parse_obj(x) for x in data]
            else:
                msg = f"Got unexpected type of data. Expected list, got {type(data)}."
                self.logger.error(msg=msg)
                raise TypeError(msg)
        return model_data

    def _parse_pydantic_filter(self, data: Union[dict, list]):
        """

        """
        data = deepcopy(data)
        if isinstance(data, list):
            return set(data)
        elif isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, str):
                    if v == '...':
                        data[k] = ...
                elif isinstance(v, dict):
                    data[k] = self._parse_pydantic_filter(data=v)
                elif isinstance(v, list):
                    data[k] = set(v)
        return data

    def validate_data(self, data: Union[dict, list], model: str, many=False) -> bool:
        try:
            model_data = self.to_model(data=data, model=model, many=many, serialize=False)
        except Exception as e:
            msg = f"Got Exception while validating data with model '{model}'. Exception: {repr(e)}."
            self.logger.error(msg=msg)
            return False
        if model_data is None:
            return False
        elif isinstance(model_data, BaseNetModel):
            return True
        elif isinstance(model_data, list):
            if all([isinstance(x, BaseNetModel) for x in model_data]):
                return True
            else:
                return False
        else:
            msg = f"Unexpected type - 'model_data' is {type(model_data)}. {model_data}"
            raise TypeError(msg)

    def to_vlan_range(self, vlans: Union[List[int], Literal["none", "all"]]) -> str:

        if isinstance(vlans, str):
            if vlans == "none":
                return "none"
            elif vlans == "all":
                return "all"
            else:
                raise ValueError(f"Invalid string value: {vlans}")
        min_diff = 1
        # Assume vlans is List[int]
        vlans = sorted(list(set(vlans)))
        parts = []
        current_entry = [None, None]
        for vlan in vlans:
            if current_entry[0] is None:
                current_entry[0] = vlan
            elif current_entry[1] is None:
                if current_entry[0] + 1 == vlan:
                    current_entry[1] = vlan
                else:
                    # Flush
                    parts.append(str(current_entry[0]))
                    current_entry = [vlan, None]
            else:
                if current_entry[1] + 1 == vlan:
                    current_entry[1] = vlan
                else:
                    # Flush
                    if (current_entry[1] - current_entry[0]) > min_diff:
                        parts.append(f"{current_entry[0]}-{current_entry[1]}")
                    else:
                        parts.extend(map(str, current_entry))
                    current_entry = [vlan, None]
        # Flush remainder
        if not any(current_entry):
            pass
        elif all(current_entry):
            if (current_entry[1] - current_entry[0]) > min_diff:
                parts.append(f"{current_entry[0]}-{current_entry[1]}")
            else:
                parts.extend(map(str, current_entry))
                current_entry = [None, None]
        else:
            parts.append(str(current_entry[0]))
        vlan_range = ",".join(parts)
        if vlan_range == "":
            return "none"
        elif vlan_range == "1-4094":
            return "all"
        return vlan_range

    def ipaddress(self, ip_address: Union[
        ipaddress.IPv4Address, ipaddress.IPv4Interface, ipaddress.IPv4Network, ipaddress.IPv6Address,
        ipaddress.IPv6Interface, ipaddress.IPv6Network],
                  operation: str = None):
        address = None
        for func in [ipaddress.ip_address, ipaddress.ip_interface, ipaddress.ip_network]:
            if address is None:
                try:
                    address = func(ip_address)
                except Exception as e:
                    pass
        if operation is None:
            if address:
                return True
            else:
                return False
        if operation == "address":
            if isinstance(address, (ipaddress.IPv4Interface, ipaddress.IPv6Interface)):
                return str(address.ip)
            elif isinstance(address, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
                return str(address)
        elif operation == "netmask":
            if isinstance(address, (ipaddress.IPv4Interface, ipaddress.IPv6Interface)):
                return str(address.with_netmask).split("/")[1]
        elif operation == 'prefixlen':
            if isinstance(address, (ipaddress.IPv4Interface, ipaddress.IPv6Interface)):
                return str(address.network.prefixlen)
            elif isinstance(address, (ipaddress.IPv4Network, ipaddress.IPv6Network)):
                return str(address.prefixlen)
        raise ValueError("Invalid IP Given")

    def get_vlans(self, vlan_definitions: list, host_name: str, vlan_ids: List[int] = None) -> List[Dict]:
        host_vlans = []
        if isinstance(vlan_definitions, list):
            vlan_definitions = map(VLANHostMapping.parse_obj, vlan_definitions)

            vlan_definitions_w_hosts = [x for x in vlan_definitions if x.hosts is not None]
            for vlan_definition in vlan_definitions_w_hosts:
                for host in vlan_definition.hosts:
                    if host.name == host_name:
                        self.logger.debug(msg=f"Host {host_name} is member of VLAN {vlan_definition.vlan_id}")
                        host_vlans.append(vlan_definition)
            return [x.serial_dict(exclude_none=True) for x in host_vlans]
        else:
            return []

    def to_wildcard(self, mask):
        parts = mask.split(".")
        wildcard_parts = [str(255 - int(x)) for x in parts]
        return ".".join(wildcard_parts)

    def str_to_obj(self, string: str):
        return eval(string)

    def json_query(self, data: Union[list, dict], query: str):
        return jmespath.search(query, data)

    def str_to_obj(self, string: str):
        return eval(string)

    def to_json(self, data: Union[list, dict]) -> str:
        return json.dumps(data)

    def type_debug(self, var) -> str:
        return str(type(var))
