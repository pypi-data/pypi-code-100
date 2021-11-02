

from MSApi.ObjectMS import ObjectMS, check_init


class AttributeInfo(ObjectMS):
    def __init__(self, json):
        super().__init__(json)

    @check_init
    def get_id(self) -> str:
        return self._json.get('id')

    @check_init
    def get_name(self) -> str:
        return self._json.get('name')

    @check_init
    def get_type(self) -> str:
        return self._json.get('type')

    @check_init
    def is_required(self) -> bool:
        return self._json.get('required')

    @check_init
    def get_description(self) -> str:
        return self._json.get('description')
