from telebotify.models.jsonable import Jsonable


class User(Jsonable):

    def __init__(self,
                 user_id=None,
                 is_bot=None,
                 first_name=None,
                 last_name=None,
                 username=None,
                 language_code=None,
                 can_join_groups=None,
                 can_read_all_group_messages=None,
                 supports_inline_queries=None):
        self.user_id = user_id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.can_join_groups = can_join_groups
        self.can_read_all_group_messages = can_read_all_group_messages
        self.supports_inline_queries = supports_inline_queries

    @classmethod
    def from_json(cls, json_dict: dict):
        user_id = json_dict["id"]
        is_bot = json_dict["is_bot"]
        first_name = json_dict["first_name"]
        last_name = dict.get(json_dict, "last_name")
        username = json_dict["username"]
        language_code = dict.get(json_dict, "language_code")
        can_join_groups = dict.get(json_dict, "can_join_groups")
        can_read_all_group_messages = dict.get(json_dict, "can_read_all_group_messages")
        supports_inline_queries = dict.get(json_dict, "supports_inline_queries")
        return cls(user_id,
                   is_bot,
                   first_name,
                   last_name,
                   username,
                   language_code,
                   can_join_groups,
                   can_read_all_group_messages,
                   supports_inline_queries)
