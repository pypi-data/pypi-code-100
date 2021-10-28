import logging
from typing import Sequence

from babel.core import Locale, get_locale_identifier
from starlette.requests import Request

logger = logging.getLogger(__name__)


def parse_accept_language(accept_language: str) -> Sequence[Locale]:
    """
    TODO: properly manage format https://pypi.org/project/parse-accept-language/
    """
    locales: list[Locale] = []
    for locale in accept_language.split(","):
        if ";" in locale:
            locale, quality = locale.split(";")
        locales.append(Locale.parse(locale, sep="-"))
    return locales


def get_locale_from_request(request: Request, available: Sequence[Locale]) -> Locale:
    accept_language = request.headers.get("Accept-Language", None)
    if accept_language is None:
        return Locale("fr", "FR")  # TODO: pref

    preferred = parse_accept_language(accept_language)
    locale = Locale.negotiate(
        [str(locale) for locale in preferred], [str(locale) for locale in available]
    )
    logger.debug(f"negotiate_locale {preferred} from {available} -> {locale}")
    return locale


def get_html_lang(locale: Locale) -> str:
    return get_locale_identifier(
        (locale.language, locale.territory, locale.script, locale.variant), sep="-"
    )
