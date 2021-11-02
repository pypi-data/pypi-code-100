from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.error_invalid_params_item import ErrorInvalidParamsItem

T = TypeVar("T", bound="Error")


@attr.s(auto_attribs=True)
class Error:
    """ """

    title: str
    invalid_params: List[ErrorInvalidParamsItem]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        invalid_params = []
        for invalid_params_item_data in self.invalid_params:
            invalid_params_item = invalid_params_item_data.to_dict()

            invalid_params.append(invalid_params_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "invalid-params": invalid_params,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        invalid_params = []
        _invalid_params = d.pop("invalid-params")
        for invalid_params_item_data in _invalid_params:
            invalid_params_item = ErrorInvalidParamsItem.from_dict(invalid_params_item_data)

            invalid_params.append(invalid_params_item)

        error = cls(
            title=title,
            invalid_params=invalid_params,
        )

        error.additional_properties = d
        return error

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
