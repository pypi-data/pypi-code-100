from typing import Optional

from ..schema.response import UserError


class UserErrorParserMixin:
    def parse_user_error(self, response) -> [Optional[UserError]]:
        if not response:
            return

        return [UserError(field=user_error['field'], message=user_error['message']) for user_error in response]
