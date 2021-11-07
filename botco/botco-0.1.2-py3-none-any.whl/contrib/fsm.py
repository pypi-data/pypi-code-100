from typing import Union

from .storage import BaseStorage


class FSM:
    def __init__(self, storage: BaseStorage, bot_id: Union[str, int], user_id: Union[str, int] = None,
                 chat_id: Union[str, int] = None):
        if chat_id is None:
            chat_id = user_id
        self._storage = storage
        self._key = f"{bot_id}:{user_id}:{chat_id}"

    def set(self, state: Union[str, int]):
        self._storage.set_state(self._key, state)

    def get(self):
        return self._storage.get_state(self._key)

    def finish(self, clear=False):
        self._storage.finish(self._key, clear=clear)

    def update_data(self, **kwargs):
        self._storage.update_data(self._key, kwargs)

    def get_data(self):
        return self._storage.get_data(self._key)
