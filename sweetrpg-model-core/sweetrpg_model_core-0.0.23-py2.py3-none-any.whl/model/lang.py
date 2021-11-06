# -*- coding: utf-8 -*-
__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""Embedded model for language strings.
"""

from .base import EmbeddedModel
import locale


class LangString(EmbeddedModel):

    def __init__(self, starting_string=None, *args, **kwargs):
        super(EmbeddedModel, self).__init__(*args, **kwargs)

        self.default_locale = locale.getlocale()
        self.strings = {
            self.default_locale: starting_string
        }

    def __str__(self):
        return self.strings.get(self.default_locale)

    def __repr__(self):
        keys = list(map(lambda k: k[0], self.strings.keys()))
        return f"<LangString(default_locale={self.default_locale}, keys={','.join(keys)}"

    def set_string(self, value, loc=None, make_default=False):
        if not loc:
            loc = self.default_locale
        self.strings[loc] = value

        if make_default:
            self.default_locale = loc

    def get_string(self, loc=None):
        if not loc:
            loc = self.default_locale

        return self.strings.get(loc)
