import requests
from . import emoji
from ._base_url import BASE_URL


def get_message(chat_id: int, key: str) -> str:
    r = requests.get(f"{BASE_URL}/message", params={
        "chat_id": chat_id,
        "key": key
    })
    message = r.json()["message"]
    return message


def get_available_language(lang: str = None):
    if not lang:
        r = requests.get(f"{BASE_URL}/langs")
        language = r.json()["language"]
        return list(language)
    r = requests.get(f"{BASE_URL}/langs", params={
        "lang": lang
    })
    key = r.json()["key"]
    return dict(key)


def paste(content: str):
    """
    :param content: str
    :return: {"link": link, "preview": link_preview}
    """
    r = requests.post(f"{BASE_URL}/paste", json={"content": content})
    return r.json()


def get_stats():
    res = requests.get(f"{BASE_URL}/gstats").json()
    chats = res["chats"]
    pms = res["pm"]
    return chats, pms


kode = get_available_language()
lang_flags = {
    "en": f"{emoji.FLAG_UNITED_STATES} English",
    "id": f"{emoji.FLAG_INDONESIA} Indonesia",
    "su": f"{emoji.FLAG_INDONESIA} Sundanese",
    "jv": f"{emoji.FLAG_INDONESIA} Javanese",
    "pt": f"{emoji.FLAG_PORTUGAL} Portuguese",
}
