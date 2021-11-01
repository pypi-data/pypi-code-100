# -*- coding: utf-8 -*-
"""
    pod2gen.funding
    ~~~~~~~~~~~~~~~

    This module contains Funding, which represents a funding element.

    :copyright: 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import warnings
from urllib.parse import urlparse

import validators

from pod2gen.warnings import NotSupportedByItunesWarning


class Funding(object):
    """Class representing a Podcast funding page.

    By using this class, you can be sure that the funding object is formatted correctly
    and will be correctly used by the :class:`Podcast` class for feed generation.

    :class:`.Funding` objects can be attached to :class:`.Podcast` objects
    using this method. Fundings are stored in :attr:`.Podcast.fundings`.

    See `podcast-namespace Funding
    <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#funding>`_
    for an overview of the Funding tag

    Example::

        >>> from pod2gen import Funding, Podcast
        >>> f = Funding("Please support me!", "https://examples.com/donation_link.html")
        >>> f.text
        'Please support me!'
        >>> f.url
        'https://examples.com/donation_link.html'
        >>> f.text = "Support us if you like the show!"
        >>> f.text
        'Support us if you like the show!'
        >>> f.url = "https://examples.com/another_donation_link.html"
        >>> f.url
        'https://examples.com/another_donation_link.html'
        >>> p = Podcast()
        >>> p.add_funding(f)
    """

    def __init__(self, text, url):
        """Create new Funding object. See the class description of
        :class:´~pod2gen.funding.Funding`.

        :param text: A funding message (e.g. "Support the show!").
        :type text: str
        :param url: Donation/funding link (Must be a valid url).
        :type url: str
        """

        self.__text = None
        self.__url = None

        self.text = text
        self.url = url

    @property
    def text(self):
        """A message to encourage people donation and support.
        The message should not exceed 128 characters.

        Check `podcast-namespace Funding node value
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#node-value-1>`_
        for more details.

        :type: :obj:`str`
        """
        return self.__text

    @text.setter
    def text(self, text):
        if not text:
            raise ValueError("Funding text cannot be empty or None")

        if not isinstance(text, str):
            raise ValueError("Funding text must be a valid string")

        if len(text) > 128:
            raise ValueError("Funding text must not exceed 128 characters")

        self.__text = text

    @property
    def url(self):
        """The donation/link for a podcast.

        Check `podcast-namespace Funding url attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-2>`_
        for more details.

        :type: :obj:`str`
        """
        return self.__url

    @url.setter
    def url(self, url):
        if not url:
            raise ValueError("url cannot be empty or None")

        if validators.url(url) is not True:
            raise ValueError("Not a valid url: %s" % url)

        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            warnings.warn(
                "URL scheme %s is not supported by iTunes. Make sure "
                "you use absolute URLs and HTTP or HTTPS." % parsed_url.scheme,
                NotSupportedByItunesWarning,
                stacklevel=2,
            )
        self.__url = url

    def __repr__(self):
        return "Funding(text=%s, url=%s)" % (self.text, self.url)
