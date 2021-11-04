from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="OAuthTokenRequest")


@attr.s(auto_attribs=True)
class OAuthTokenRequest:
    """  """

    client_id: str
    client_secret: str
    grant_type: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        client_id = self.client_id
        client_secret = self.client_secret
        grant_type = self.grant_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type,}
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        grant_type = d.pop("grant_type")

        o_auth_token_request = cls(client_id=client_id, client_secret=client_secret, grant_type=grant_type,)

        o_auth_token_request.additional_properties = d
        return o_auth_token_request

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
