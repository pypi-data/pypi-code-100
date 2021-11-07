import inspect
from dataclasses import dataclass
from functools import partial
from typing import Callable, List, Union, Any, TYPE_CHECKING

from botco import Bot
from botco.filters import BaseFilter
from botco.types import TelegramObject
from .builtin_filters import FILTERS
from .fsm import FSM

if TYPE_CHECKING:
    from botco.dispatcher import Dispatcher


@dataclass
class CallbackDict:
    callback: Callable
    full_config: dict
    callback_args: inspect.FullArgSpec.args
    args: List[Any] = None


class BaseHandler:
    def __init__(self, dispatcher: "Dispatcher", event_type: str = None):
        self.dispatcher = dispatcher
        self.callbacks: List[CallbackDict] = []
        self.event_type: str = event_type
        self.builtin_filters: List[BaseFilter] = []

        if self.event_type and self.event_type in FILTERS:
            self.builtin_filters.extend([filter_() for filter_ in FILTERS[event_type]])

    def __call__(self, func=None, **kwargs):
        def wrapper(callback):
            kwargs.update(func=func)
            full_config = {}
            for key, value in kwargs.items():
                if value is not None:
                    full_config[key] = value
            self.callbacks.append(
                CallbackDict(callback=callback, full_config=full_config,
                             callback_args=self.get_callback_spec(callback).args)
            )
            return callback

        return wrapper

    def get_state(self, bot: Bot, obj: TelegramObject):
        user_id = getattr(getattr(obj, 'from_user'), 'id') if hasattr(obj, 'from_user') else None
        chat_id = None
        if hasattr(obj, 'chat'):
            chat_id = getattr(getattr(obj, 'chat'), 'id')
        elif hasattr(obj, 'message'):
            chat_id = getattr(getattr(getattr(obj, 'message'), 'chat'), 'id')
        if user_id is not None:
            return FSM(self.dispatcher.storage, bot.id, user_id, chat_id)
        return None

    def check_args(self, bot: Bot, obj: TelegramObject):
        for callback_dict in self.callbacks:
            default_args = [obj, bot]
            state = self.get_state(bot, obj)
            if len(callback_dict.callback_args) > 2 and state is None:
                raise ValueError("This message handler doesn't accept state argument")
            elif state is not None:
                default_args.append(state)
            callback_dict.args = [default_args.pop(0) for _ in range(len(callback_dict.callback_args)) if
                                  len(default_args)]

    @staticmethod
    def get_callback_spec(callback):
        return inspect.getfullargspec(callback)

    def bind_filters(self, filters: List[BaseFilter]):
        for filter_ in filters:
            if not isinstance(filter_, BaseFilter):
                break
            else:
                if filter_ not in self.builtin_filters:
                    self.builtin_filters.append(filter_)
                else:
                    raise ValueError(f"{type(filter_)} already binded")

    @staticmethod
    def clean(kwargs: dict):
        if '__class__' in kwargs:
            kwargs.pop('__class__')
        if 'self' in kwargs:
            kwargs.pop('self')
        kwargs.update(kwargs.pop('kwargs'))
        return kwargs

    def process_update(self, bot: Bot, obj: TelegramObject):
        self.check_args(bot, obj)

        for callback_dict in self.callbacks:
            if self.dispatcher.check_filters(obj, callback_dict, self.builtin_filters):
                if self.dispatcher.threaded:
                    task = self.dispatcher.pool_executor.add_task(callback_dict.callback, *callback_dict.args)
                    task.add_done_callback(partial(self.dispatcher.on_done_callback, obj))
                else:
                    try:
                        callback_dict.callback(*callback_dict.args)
                    except Exception as e:
                        self.dispatcher.exception_handlers(obj, e)
                break


class MessageHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            text: str = None,
            text_iequals: str = None,
            text_startswith: str = None,
            text_istartswith: str = None,
            text_endswith: str = None,
            text_iendswith: str = None,
            state: Union[str, int] = None,
            user_id: Union[str, int] = None,
            chat_id: Union[str, int] = None,
            commands: Union[list, str] = None,
            commands_prefix: str = '/',
            **kwargs
    ):
        return super().__call__(**self.clean(locals()))


class CallbackQueryHandler(MessageHandler):
    pass


class InlineQueryHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            text: str = None,
            text_iequals: str = None,
            text_startswith: str = None,
            text_istartswith: str = None,
            text_endswith: str = None,
            text_iendswith: str = None,
            state: Union[str, int] = None,
            user_id: Union[str, int] = None,
            **kwargs
    ):
        super(InlineQueryHandler, self).__call__(**self.clean(locals()))


class ChosenInlineResultHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            user_id: Union[int, str] = None,
            **kwargs
    ):
        super(ChosenInlineResultHandler, self).__call__(**self.clean(locals()))


class PollHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            text: str = None,
            text_iequals: str = None,
            text_startswith: str = None,
            text_istartswith: str = None,
            text_endswith: str = None,
            text_iendswith: str = None,
    ):
        super(PollHandler, self).__call__(**self.clean(locals()))


class ChatMemberHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            user_id: Union[int, str] = None,
            chat_id: Union[int, str] = None,
            **kwargs
    ):
        super(ChatMemberHandler, self).__call__(**self.clean(locals()))


class ChatJoinRequest(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            user_id: Union[int, str] = None,
            chat_id: Union[int, str] = None,
            **kwargs
    ):
        super(ChatJoinRequest, self).__call__(**self.clean(locals()))


class ShippingQueryHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            user_id: Union[int, str] = None,
            **kwargs
    ):
        super(ShippingQueryHandler, self).__call__(**self.clean(locals()))


class PreCheckoutQueryHandler(BaseHandler):
    def __call__(
            self,
            func: Callable = None,
            user_id: Union[int, str] = None,
            **kwargs
    ):
        super(PreCheckoutQueryHandler, self).__call__(**self.clean(locals()))
