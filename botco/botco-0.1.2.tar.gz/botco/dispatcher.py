import concurrent.futures
import json
import logging
import time
from typing import List, Optional

from botco.contrib.fsm import FSM
from botco.contrib.handler import (
    BaseHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    PollHandler,
    ChatMemberHandler,
    ChosenInlineResultHandler,
    ShippingQueryHandler,
    PreCheckoutQueryHandler, CallbackDict, ChatJoinRequest)
from .bot import Bot
from .contrib import EventType
from .contrib.builtin_filters import CustomFilters
from .contrib.middlewares import MiddlewareManager
from .contrib.storage import MemoryStorage
from .contrib.thread_pool import ThreadPoolExecutor
from .filters import BaseFilter
from .methods.base import TelegramType
from .types import Update, TelegramObject
from .utils.exceptions import get_exc_info

logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s',
                    datefmt='%Y-%m-%d:%H:%M')
log = logging.getLogger(__name__)

ALL_STATES = ["*"]


class Dispatcher:
    def __init__(self, storage=None, max_workers: int = None, threaded=False):

        self.storage = storage if storage else MemoryStorage()

        self.message = MessageHandler(self, EventType.MESSAGE)
        self.edited_message = MessageHandler(self, EventType.EDITED_MESSAGE)
        self.channel_post = MessageHandler(self, EventType.CHANNEL_POST)
        self.inline_query = InlineQueryHandler(self, EventType.INLINE_QUERY)
        self.chosen_inline_result = ChosenInlineResultHandler(self, EventType.CHOSEN_INLINE_RESULT)
        self.callback_query = CallbackQueryHandler(self, EventType.CALLBACK_QUERY)
        self.shipping_query = ShippingQueryHandler(self, EventType.SHIPPING_QUERY)
        self.pre_checkout_query = PreCheckoutQueryHandler(self, EventType.PRE_CHECKOUT_QUERY)
        self.poll = PollHandler(self, EventType.POLL)
        self.poll_answer = BaseHandler(self, EventType.POLL_ANSWER)
        self.my_chat_member = ChatMemberHandler(self, EventType.MY_CHAT_MEMBER)
        self.chat_member = ChatMemberHandler(self, EventType.CHAT_MEMBER)
        self.chat_join_request = ChatJoinRequest(self, EventType.CHAT_JOIN_REQUEST)

        self.custom_filters = CustomFilters()
        self.error = BaseHandler(self)
        self.stop_on_exception = False
        self.middleware = MiddlewareManager(self)
        self._last_update_id = 0
        self.__polling = False
        self.threaded = threaded
        self._max_workers = max_workers
        if self.threaded:
            self.pool_executor = ThreadPoolExecutor(max_workers=self._max_workers)

    @staticmethod
    def check_builtin_filters(obj: TelegramType, full_config: dict, builtin_filters: List[BaseFilter] = None):
        filters = builtin_filters.copy()
        return_value = True
        for filter_ in filters:
            return_value = return_value and filter_.check(obj, full_config)
        return return_value

    def check_custom_filters(self, obj: TelegramType, full_config: dict = None):
        result = True
        if not self.custom_filters.is_empty:
            for custom_filter in self.custom_filters:
                kwargs = {}
                for key_ in custom_filter.keys:
                    if key_ in full_config:
                        kwargs[key_] = full_config.pop(key_)
                if not kwargs:
                    return True
                result = result and custom_filter.check(obj, kwargs)
        return result

    @staticmethod
    def state_filter(args: list, full_config: dict):
        state: FSM = args[2] if len(args) > 2 else None

        if 'state' in full_config:
            state_filter = full_config.pop('state')
            if state is not None:
                if state_filter == ALL_STATES:
                    return True
                elif state_filter == state.get():
                    return True
            return False
        else:
            if state and state.get() is not None:
                return False
            return True

    @staticmethod
    def check_func(obj, full_config: dict = None):
        if full_config and 'func' in full_config:
            return full_config.pop('func')(obj)
        return True

    def check_filters(self, obj: TelegramType, callback_dict: CallbackDict, builtin_filters: List[BaseFilter] = None):
        full_config = callback_dict.full_config.copy()
        if self.check_builtin_filters(obj, full_config, builtin_filters) is True:
            if self.check_custom_filters(obj, full_config) is True:
                if self.state_filter(callback_dict.args, full_config) is True:
                    if self.check_func(obj, full_config) is True:
                        return True
        return False

    def feed_update(self, bot: Bot, update: Update):
        obj = getattr(update, update.event_type)
        if hasattr(obj, 'set_bot'):
            obj.set_bot(bot)
        handler: BaseHandler = getattr(self, update.event_type)
        handler.process_update(bot, obj)

    def exception_handlers(self, obj: TelegramObject, exception):
        logging.error(get_exc_info() + f" {exception}")
        if self.error.callbacks:
            for callback_dict in self.error.callbacks:
                callback_dict.callback(obj, exception)
        if self.stop_on_exception:
            if self.__polling:
                print('Cancelling...')
                self.__polling = False

    def on_done_callback(self, obj, future: concurrent.futures.Future):
        try:
            future.result()
        except Exception as e:
            self.exception_handlers(obj, e)

    def feed_update_raw(self, bot: Bot, update_raw: dict):
        if isinstance(update_raw, str):
            update_raw = json.loads(update_raw)
        update = Update(**update_raw)
        self.feed_update(bot, update)

    @staticmethod
    def skip_updates(bot: Bot):
        bot.get_updates(offset=-1, timeout=1)

    def __run_polling(self, bot: Bot, drop_pending_updates: bool = False, timeout: Optional[int] = 20,
                      allowed_updates: Optional[List[str]] = None):
        self.__polling = True
        if drop_pending_updates:
            self.skip_updates(bot)
        while self.__polling:
            try:
                updates = bot.get_updates(offset=self._last_update_id, timeout=timeout,
                                          allowed_updates=allowed_updates)
            except Exception as e:
                logging.exception(e)
                self.__polling = False
                bot.session.close()
                break
            if updates:
                self._last_update_id = updates[-1].update_id + 1
                for update in updates:
                    self.feed_update(bot, update)

    def start_polling(self, bot: Bot, drop_pending_updates: bool = True, timeout: Optional[int] = 10,
                      allowed_updates: Optional[List[str]] = None, stop_on_exception: bool = False):
        print('Getting updates!')
        self.stop_on_exception = stop_on_exception
        pool_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = pool_executor.submit(self.__run_polling, bot, drop_pending_updates, timeout,
                                      allowed_updates)
        try:
            while future.running():
                time.sleep(1)
        except KeyboardInterrupt:
            bot.session.close()
            print("Cancelling...")
            self.__polling = False
            stop_future(future)


called = 0


# Just for fun
def stop_future(future: concurrent.futures.Future):
    global called
    called += 1
    try:
        if called == 1:
            pass
        elif called == 2:
            print(f"Please wait for a while...")
        elif called == 3:
            print("Be patient :)")
        else:
            print("Oh noo. Oh no. Oh no no no")
        while future.running():
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_future(future)
