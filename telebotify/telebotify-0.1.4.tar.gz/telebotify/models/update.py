from telebotify.models.jsonable import Jsonable
from telebotify.models.message import Message


class Update(Jsonable):

    def __init__(self,
                 update_id: int = None,
                 message: Message = None,
                 edited_message: Message = None,
                 channel_post: Message = None,
                 edited_channel_post: Message = None,
                 inline_query=None,
                 chosen_inline_result=None,
                 callback_query=None,
                 shipping_query=None,
                 pre_checkout_query=None,
                 poll=None,
                 poll_answer=None,
                 my_chat_member=None,
                 chat_member=None):
        self.update_id = update_id
        self.message = message
        self.edited_message = edited_message
        self.channel_post = channel_post
        self.edited_channel_post = edited_channel_post
        self.inline_query = inline_query
        self.chosen_inline_result = chosen_inline_result
        self.callback_query = callback_query
        self.shipping_query = shipping_query
        self.pre_checkout_query = pre_checkout_query
        self.poll = poll
        self.poll_answer = poll_answer
        self.my_chat_member = my_chat_member
        self.chat_member = chat_member

    @classmethod
    def from_json(cls, json_dict: dict):
        update_id = dict.get(json_dict, "update_id")
        message = None if dict.get(json_dict, "message") is None else Message.from_json(dict.get(json_dict, "message"))
        edited_message = None if dict.get(json_dict, "edited_message") is None else Message.from_json(dict.get(json_dict, "edited_message"))
        channel_post = None if dict.get(json_dict, "channel_post") is None else Message.from_json(dict.get(json_dict, "channel_post"))
        edited_channel_post = None if dict.get(json_dict, "edited_channel_post") is None else Message.from_json(dict.get(json_dict, "edited_channel_post"))
        inline_query = dict.get(json_dict, "inline_query")
        chosen_inline_result = dict.get(json_dict, "chosen_inline_result")
        callback_query = dict.get(json_dict, "callback_query")
        shipping_query = dict.get(json_dict, "shipping_query")
        pre_checkout_query = dict.get(json_dict, "pre_checkout_query")
        poll = dict.get(json_dict, "poll")
        poll_answer = dict.get(json_dict, "poll_answer")
        my_chat_member = dict.get(json_dict, "my_chat_member")
        chat_member = dict.get(json_dict, "chat_member")

        return cls(
                 update_id,
                 message,
                 edited_message,
                 channel_post,
                 edited_channel_post,
                 inline_query,
                 chosen_inline_result,
                 callback_query,
                 shipping_query,
                 pre_checkout_query,
                 poll,
                 poll_answer,
                 my_chat_member,
                 chat_member)
