# -*- coding: utf-8 -*-
"""
    pod2gen.license
    ~~~~~~~~~~~~~~~

    This module contains License class that represents a license that is applied
    to the audio/video content of a single episode, or the audio/video of the
    podcast as a whole.

    :copyright: 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import warnings
from urllib.parse import urlparse

import validators

from pod2gen.warnings import NotSupportedByItunesWarning


class License(object):
    """Class representing a license object that is applied to the audio/video content
    of a single episode, or the audio/video of the podcast as a whole.

    Custom licenses must always include a url attribute. Implementors are encouraged to
    read the license tag companion document for a more complete picture of what this tag
    is intended to accomplish.

    By using this class, you can be sure that the license object is formatted correctly
    and will be correctly used by the associated :class:`~.pod2gen.Podcast` or
    :class:`~.pod2gen.Episode` object.

    See `podcast-namespace License
    <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#license>`_
    for an overview of the License tag.

    Example::

        >>> from pod2gen import License
        >>> l = License("my-podcast-license-v1", "https://example.org/mypodcastlicense/full.pdf")
        >>> l.identifier
        'my-podcast-license-v1'
        >>> l.url
        'https://example.org/mypodcastlicense/full.pdf'
        >>> l.identifier = "my-podcast-license-v2"
        >>> l.identifier
        'my-podcast-license-v2'
        >>> l.url = "https://example.org/mypodcastlicense/full_2.pdf"
        >>> l.url
        'https://example.org/mypodcastlicense/full_2.pdf'
    """

    def __init__(self, identifier, url=None):
        """Create new License object. See the class description of
        :class:´~pod2gen.license.License`.

        :param identifier: A license "identifier" defined in the SPDX License List file if
            the license being used is a well-known, public license. Or, if it is a
            custom license, it must be a free form abbreviation of the name of the
            license as you reference it publicly.
        :type identifier: str
        :param url: (Optional) a url that points to the full, legal language of the
            license being referenced.
        :type url: str
        """

        self.__identifier = None
        self.__url = None

        self.identifier = identifier
        self.url = url

    @property
    def identifier(self):
        """A license "identifier" defined in the
        `SPDX License List <https://spdx.org/licenses/>`_ file if
        the license being used is a well-known, public license. If it is a
        custom license, it must be a free form abbreviation of the license
        name as you reference it publicly.

        Check `podcast-namespace License node value
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#node-value-8>`_
        for more details.

        :type: :obj:`str`
        """
        return self.__identifier

    @identifier.setter
    def identifier(self, identifier):
        if not identifier:
            raise ValueError("License identifier cannot be empty or None")

        if not isinstance(identifier, str):
            raise ValueError("License identifier must be a valid string")

        self.__identifier = identifier

    @property
    def url(self):
        """Url that points to the full, legal language of the license being referenced.

        Check `podcast-namespace License url attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-10>`_
        for more details

        :type: :obj:`str` or :obj:`None`
        """
        return self.__url

    @url.setter
    def url(self, url):
        if url:
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

        else:
            self.__url = None

    def __repr__(self):
        if self.url:
            return "License(identifier=%s, url=%s)" % (self.identifier, self.url)
        return "License(identifier=%s)" % self.identifier
