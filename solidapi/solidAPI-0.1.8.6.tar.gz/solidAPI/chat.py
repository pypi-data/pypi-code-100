from json import JSONDecodeError

import requests

from ._base_url import BASE_URL
from .other import get_available_language


def add_chat(chat_id: int, lang="en"):
    """
    :param chat_id:
    :param lang: str
    :return: 201 or 404 or 500
    """
    r = requests.post(f"{BASE_URL}/chats/", json={
        "chat_id": chat_id,
        "lang": lang
    })
    return r.status_code


def get_chat(chat_id: int) -> dict:
    """
    For get information of chat
    :param chat_id: int
    :return: { "chat_id": chat_id, "lang": lang } or {}}
    """
    try:
        r = requests.get(f"{BASE_URL}/chats/{chat_id}")
        return r.json()
    except JSONDecodeError:
        return {}


def set_lang(chat_id: int, lang: str) -> int:
    """
    :param chat_id: int
    :param lang: str
    :return: 200 | 404
    """
    if lang not in get_available_language():
        return 404
    r = requests.put(f"{BASE_URL}/chats/{chat_id}?lang={lang}")
    return r.status_code


def del_chat(chat_id: int):
    """
    :param chat_id: int
    :return: 200 | 404 | 500
    """
    r = requests.delete(f"{BASE_URL}/chats/{chat_id}")
    return r.status_code
