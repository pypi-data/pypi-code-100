from typing import Union

from botco.filters import BaseFilter
from botco.types import Message, CallbackQuery, InlineQuery, Poll, TelegramObject, User, Chat


# Filters 🛑 Don't use them directly 🛑

class TextFilter(BaseFilter):
    keys = (
        # ('key', 'condition', ignore_case)
        ('text', 'equals', False),
        ('text_iequals', 'equals', True),
        ('text_contains', 'contains', False),
        ('text_icontains', 'contains', True),
        ('text_startswith', 'startswith', False),
        ('text_istartswith', 'startswith', True),
        ('text_endswith', 'endswith', False),
        ('text_iendswith', 'endswith', True),
    )

    def check(self, obj: Union[Message, CallbackQuery, InlineQuery, Poll], filters: dict):
        if not filters:
            return True
        if isinstance(obj, Message):
            text = obj.text or obj.caption or ''
            if not text and obj.poll:
                text = obj.poll.question
        elif isinstance(obj, CallbackQuery):
            text = obj.data
        elif isinstance(obj, InlineQuery):
            text = obj.query
        elif isinstance(obj, Poll):
            text = obj.question
        else:
            return False
        has_ = False
        result = True
        for key, condition, ignore_case in self.keys:
            if key not in filters:
                continue
            has_ = True
            t = text
            if ignore_case:
                t = t.lower()
            value = filters.pop(key)

            if key in ['text', 'text_iequals']:
                result = result and t == value
            elif key in ['text_contains', 'text_icontains']:
                result = result and t.__contains__(value)
            elif key in ['text_startswith', 'text_istartswith']:
                result = result and t.startswith(value)
            elif key in ['text_endswith', 'text_iendswith']:
                result = result and t.endswith(value)
        if not has_:
            return True
        else:
            return result


class CommandFilter(BaseFilter):
    keys = ('commands', 'commands_prefix')

    def check(self, obj: Message, filters: dict) -> bool:
        return_value = True
        if self.keys[0] in filters:
            values = filters.pop(self.keys[0])
            if isinstance(values, str):
                values = [values]
            if obj.entities:
                for entity in obj.entities:
                    if entity.type == "bot_command":
                        command = obj.text[entity.offset + 1: entity.length]
                        if '@' in command:
                            command = command.split('@')[0]
                        return command in values
            elif self.keys[1] in filters:
                prefix = filters.pop(self.keys[1])
                if obj.text and obj.text.startswith(prefix):
                    return obj.text in [prefix + v for v in values]
            return False
        elif self.keys[1] in filters:
            filters.pop(self.keys[1])
        return return_value


class ChatFilter(BaseFilter):
    keys = ('chat_id',)

    def check(self, obj: TelegramObject, filters: dict) -> bool:
        result = True
        if hasattr(obj, 'chat'):
            obj: Chat = getattr(obj, 'chat')
        elif hasattr(obj, 'message'):
            obj: Chat = getattr(getattr(obj, 'message'), 'chat')
        if isinstance(obj, Chat):
            for key in self.keys:
                if key in filters:
                    if obj.id == filters.pop(key):
                        result = True
                    else:
                        result = False
        return result


class UserFilter(BaseFilter):
    keys = ('user_id',)

    def check(self, obj: TelegramObject, filters: dict) -> bool:
        result = True
        if hasattr(obj, 'from_user'):
            obj: User = getattr(obj, 'from_user')
            for key in self.keys:
                if key in filters:
                    if obj.id == filters.pop(key):
                        result = True
                    else:
                        result = False
        return result


FILTERS = {
    'message': [TextFilter, UserFilter, ChatFilter, CommandFilter],
    'edited_message': [TextFilter, UserFilter, ChatFilter],
    'channel_post': [TextFilter],
    'edited_channel_post': [TextFilter],
    'inline_query': [TextFilter, UserFilter],
    'callback_query': [TextFilter, UserFilter, ChatFilter],
    'poll': [TextFilter],
    'my_chat_member': [ChatFilter, UserFilter],
    'chat_member': [ChatFilter, UserFilter],
    'chat_join_request': [ChatFilter, UserFilter]
}


class CustomFilters:
    def __init__(self):
        self._filters: list = []

    @property
    def is_empty(self):
        return True if not self._filters else False

    def __iter__(self):
        return self._filters

    def clear(self):
        self._filters.clear()

    def add_filter(self, *custom_filters: BaseFilter):
        for custom_filter in custom_filters:
            if not issubclass(custom_filter, BaseFilter):  # noqa
                ValueError('Unknown type of filter. It must be a subclass of <BaseFilter>')
            if not hasattr(custom_filter, 'keys') and not hasattr(custom_filter, 'check'):
                raise ValueError("Your class must have 'keys' attribute and 'check' function")
            if custom_filter not in self._filters:
                self._filters.append(custom_filter)
            else:
                raise ValueError("This filter is already added. Can not be added twice")
