import threading
from typing import TYPE_CHECKING

import requests

from botco.methods.base import TelegramType, TelegramMethod

if TYPE_CHECKING:
    pass

API_URL = "https://api.telegram.org"

thread_local = threading.local()


class Session:
    def __init__(self, api_url=API_URL):
        self._api_url = api_url

    def api_url(self, token: str, method: str):
        return f"{self._api_url}/bot{token}/{method}"

    @staticmethod
    def get_session(reset: bool = False, close: bool = False):
        if reset is True:
            setattr(thread_local, 'session', requests.Session())
        elif not hasattr(thread_local, 'session'):
            if not close:
                setattr(thread_local, 'session', requests.Session())
        return getattr(thread_local, 'session', None)

    def close(self):
        session = self.get_session(close=True)
        if session:
            session.close()
            del thread_local.session

    def __call__(self, bot, method: TelegramMethod[TelegramType]):
        request = method.build_request(bot)
        url = self.api_url(bot.token, request.method)
        session: requests.Session = self.get_session()
        response = session.post(url, data=request.data)
        return method.build_response(response.json())
