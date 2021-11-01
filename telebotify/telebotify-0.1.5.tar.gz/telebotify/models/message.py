from telebotify.models.jsonable import Jsonable
from telebotify.models.user import User


class Message(Jsonable):

    def __init__(self,
                 message_id,
                 from_user: User,
                 date,
                 chat,
                 text=None):
        self.message_id = message_id
        self.from_user = from_user
        self.date = date
        self.chat = chat
        self.text = text

    @classmethod
    def from_json(cls, json_dict: dict):
        message_id = json_dict["message_id"]
        from_user = User.from_json(json_dict["from"])
        date = json_dict["date"]
        chat = Chat.from_json(json_dict["chat"])
        text = dict.get(json_dict, "text")
        return cls(message_id,
                   from_user,
                   date,
                   chat,
                   text)
