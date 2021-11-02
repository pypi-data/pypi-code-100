from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetObjectListResponse200OListItemOAddr")


@attr.s(auto_attribs=True)
class GetObjectListResponse200OListItemOAddr:
    """ """

    country: str
    region: Union[Unset, str] = UNSET
    city: Union[Unset, str] = UNSET
    county: Union[Unset, str] = UNSET
    village: Union[Unset, str] = UNSET
    street: Union[Unset, str] = UNSET
    h_name_nr: Union[Unset, str] = UNSET
    flat_nr: Union[Unset, str] = UNSET
    p_code: Union[Unset, str] = UNSET
    cust_addr_det: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        country = self.country
        region = self.region
        city = self.city
        county = self.county
        village = self.village
        street = self.street
        h_name_nr = self.h_name_nr
        flat_nr = self.flat_nr
        p_code = self.p_code
        cust_addr_det = self.cust_addr_det

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "country": country,
            }
        )
        if region is not UNSET:
            field_dict["region"] = region
        if city is not UNSET:
            field_dict["city"] = city
        if county is not UNSET:
            field_dict["county"] = county
        if village is not UNSET:
            field_dict["village"] = village
        if street is not UNSET:
            field_dict["street"] = street
        if h_name_nr is not UNSET:
            field_dict["hNameNr"] = h_name_nr
        if flat_nr is not UNSET:
            field_dict["flatNr"] = flat_nr
        if p_code is not UNSET:
            field_dict["pCode"] = p_code
        if cust_addr_det is not UNSET:
            field_dict["custAddrDet"] = cust_addr_det

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        country = d.pop("country")

        region = d.pop("region", UNSET)

        city = d.pop("city", UNSET)

        county = d.pop("county", UNSET)

        village = d.pop("village", UNSET)

        street = d.pop("street", UNSET)

        h_name_nr = d.pop("hNameNr", UNSET)

        flat_nr = d.pop("flatNr", UNSET)

        p_code = d.pop("pCode", UNSET)

        cust_addr_det = d.pop("custAddrDet", UNSET)

        get_object_list_response_200o_list_item_o_addr = cls(
            country=country,
            region=region,
            city=city,
            county=county,
            village=village,
            street=street,
            h_name_nr=h_name_nr,
            flat_nr=flat_nr,
            p_code=p_code,
            cust_addr_det=cust_addr_det,
        )

        get_object_list_response_200o_list_item_o_addr.additional_properties = d
        return get_object_list_response_200o_list_item_o_addr

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
