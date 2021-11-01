from telebotify.models.jsonable import Jsonable


class Chat(Jsonable):
    def __init__(self, chat_id, chat_type, title=None, username=None, first_name=None, last_name=None,
                 all_members_are_administrators=None, photo=None, description=None, invite_link=None,
                 pinned_message=None, sticker_set_name=None, can_set_sticker_set=None):
        self.chat_type = chat_type
        self.last_name = last_name
        self.first_name = first_name
        self.username = username
        self.chat_id = chat_id
        self.title = title
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set

    @classmethod
    def from_json(cls, json_dict: dict):
        chat_type = dict.get(json_dict, "type")
        last_name = dict.get(json_dict, "last_name")
        first_name = dict.get(json_dict, "first_name")
        username = dict.get(json_dict, "username")
        chat_id = dict.get(json_dict, "id")
        title = dict.get(json_dict, "title")
        all_members_are_administrators = dict.get(json_dict, "all_members_are_administrators")
        photo = dict.get(json_dict, "photo")
        description = dict.get(json_dict, "description")
        invite_link = dict.get(json_dict, "invite_link")
        pinned_message = dict.get(json_dict, "pinned_message")
        sticker_set_name = dict.get(json_dict, "sticker_set_name")
        can_set_sticker_set = dict.get(json_dict, "can_set_sticker_set")

        return cls(chat_id,
                   chat_type,
                   title,
                   username,
                   first_name,
                   last_name,
                   all_members_are_administrators,
                   photo,
                   description,
                   invite_link,
                   pinned_message,
                   sticker_set_name,
                   can_set_sticker_set)
