import re
import html
import unidecode
import string
from string import digits

from typing import Optional, List

from bs4 import BeautifulSoup


class TextCleaner:
    REMOVE_HTML_TAGS = "remove_html_tags"
    DECODE_HTML_ENTITIES = "decode_html_entities"
    REPLACE_ACCENTED = "replace_accented"
    REPLACE_UNICODE_NBSP = "replace_unicode_nbsp"
    REPLACE_NEWLINES_TABS = "replace_newlines_tabs"
    REMOVE_EXTRA_QUOTATION = "remove_extra_quotation"
    REMOVE_EXTRA_WHITESPACES = "remove_extra_whitespaces"
    REMOVE_URLS = "remove_urls"
    REMOVE_PUNCTUATION = "remove_punctuation"
    LOWERCASE = "lowercase"
    REMOVE_DIGITS = "remove_digits"

    def __init__(self, text: str):
        self._steps = [
            self.REMOVE_HTML_TAGS,
            self.DECODE_HTML_ENTITIES,
            self.REPLACE_ACCENTED,
            self.REPLACE_UNICODE_NBSP,
            self.REPLACE_NEWLINES_TABS,
            self.REMOVE_EXTRA_QUOTATION,
            self.REMOVE_EXTRA_WHITESPACES,
            self.REMOVE_URLS,
            self.REMOVE_PUNCTUATION,
            self.LOWERCASE,
            self.REMOVE_DIGITS,
        ]

        self._text = text.strip()

    def clean(
        self,
        steps: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None
    ) -> str:

        if not steps:
            steps = self._steps

        if exclude:
            steps = [step for step in steps if step not in exclude]

        for step in steps:
            try:
                class_method = getattr(TextCleaner, f"_{step}")
            except AttributeError:
                continue

            class_method(self)

        return self._text

    def _remove_html_tags(self) -> None:
        """ Removes html tags """
        soup = BeautifulSoup(self._text, "html.parser")

        self._text = soup.get_text(separator=" ")

    def _decode_html_entities(self) -> None:
        """ Converts html entities in the corresponding unicode string"""
        self._text = html.unescape(self._text)

    def _remove_extra_whitespaces(self) -> None:
        """ Removes extra whitespaces """
        pattern = re.compile(r'\s+')

        self._text = re.sub(pattern, " ", self._text)

    def _replace_accented(self) -> None:
        """ Removes all accented characters"""
        self._text = unidecode.unidecode(self._text)

    def _replace_unicode_nbsp(self) -> None:
        """ Removes unicode whitespaces"""
        self._text = self._text.replace(u'\xa0', u' ')

    def _remove_extra_quotation(self) -> None:
        """ Removes extra quotation marks """
        text = re.sub(r'\"{2,}', '"', self._text)

        self._text = re.sub(r'\'{2,}', "'", text)

    def _replace_newlines_tabs(self) -> None:
        """ Removes all the occurrences of newlines, tabs, and combinations like: \\n, \\. """
        self._text = self._text.replace("\\n", " ").replace("\n", ' ').replace("\t", " ").replace("\\", " ")

    def _remove_urls(self) -> None:
        """ Removes all urls from text"""
        pattern = r'(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?'

        self._text = re.sub(pattern, '', self._text, flags=re.MULTILINE)

    def _remove_punctuation(self) -> None:
        """ Removes punctuation from text """
        punctuation = string.punctuation + '¿¡'
        table = str.maketrans('', '', punctuation)
        words = self._text.split()

        stripped = [word.translate(table) for word in words]

        self._text = ' '.join(stripped)

    def _lowercase(self) -> None:
        """ Transform text to lowercase"""
        self._text = self._text.lower()

    def _remove_digits(self) -> None:
        """ Remove digits from text"""
        table = str.maketrans('', '', digits)

        self._text = self._text.translate(table)
