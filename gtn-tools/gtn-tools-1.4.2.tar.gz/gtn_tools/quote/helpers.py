# *- encoding utf-8 -*
"""helper functions"""
import os

language_codes = \
    {
        "de": "deu",
        "en": "eng",
        "fr": "fra",
        "it": "ita",
        "nl": "nld",
        "es": "spa",
        "sq": "sqi",
        "am": "amh",
        "ar": "ara",
        "az": "aze",
        "bs": "bos",
        "bg": "bul",
        "zh_sim": "chi_sim",
        "zh_tra": "chi_tra",
        "da": "dan",
        "et": "est",
        "fi": "fin",
        "ka": "kat",
        "el": "ell",
        "he": "heb",
        "hi": "hin",
        "id": "ind",
        "ja": "jpn",
        "hr": "hrv",
        "lv": "lav",
        "lt": "lit",
        "mk": "mkd",
        "mo": "ron",
        "no": "nor",
        "fa": "fas",
        "pl": "pol",
        "pt": "por",
        "pa": "pan",
        "ro": "ron",
        "ru": "rus",
        "sr": "srp",
        "sk": "slk",
        "sl": "slv",
        "ta": "tam",
        "th": "tha",
        "cs": "ces",
        "tr": "tur",
        "uk": "ukr",
        "hu": "hun",
        "ur": "urd",
        "vi": "vie"
    }


def ISO_to_tess(iso: str) -> str:
    return language_codes[iso]


def get_source_files(orders_dir: str, order_id: int) -> list:
    """Return a list of Documents form the order directory"""
    ext = ('.pdf', '.jpg', '.jpeg', '.docx', '.doc', '.pptx', '.ppt')
    source_path = os.path.join(orders_dir, str(order_id), 'src')
    files = [os.path.join(source_path, f)
             for f in os.listdir(source_path)
             if f.endswith(ext)]
    return files
