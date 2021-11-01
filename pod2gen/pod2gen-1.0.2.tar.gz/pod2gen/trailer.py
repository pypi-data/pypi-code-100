# -*- coding: utf-8 -*-
"""
    pod2gen.trailer
    ~~~~~~~~~~~~~~~

    This module contains Trailer, which represents a podcast trailer.

    :copyright: 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import mimetypes
from datetime import datetime
from urllib.parse import urlparse

import validators
from lxml import etree

from pod2gen.util import formatRFC2822
from pod2gen.warnings import NotSupportedByItunesWarning


class Trailer(object):
    """Class representing a podcast Trailer object.

    By using this class, you can be sure that the soundbite object is formatted correctly
    and will be correctly used by the associated :class:`~.pod2gen.Podcast` object.

    :class:`.Trailer` objects can be attached to :class:`.Podcast` objects
    using this method. Trailers are stored in :attr:`.Podcast.trailers`.

    See `podcast-namespace Trailer
    <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#trailer>`_
    for an overview of the Trailer tag

    Example::

        >>> from pod2gen import Trailer, Podcast
        >>> from datetime import datetime
        >>> from dateutil import tz
        >>> pubdate = datetime(2021, 8, 15, 8, 15, 12, 0, tz.UTC)
        >>> p = Podcast()
        >>> t = Trailer("Coming April 1st, 2021", "https://example.org/trailers/teaser", pubdate)
        >>> t.text
        'Coming April 1st, 2021'
        >>> t.url
        'https://example.org/trailers/teaser'
        >>> t.pubdate
        datetime.datetime(2021, 8, 15, 8, 15, 12, tzinfo=<UTC>)
        >>> t.text = "Coming August 15th, 2021"
        >>> t.text
        'Coming August 15th, 2021'
        >>> t.length = 12345678
        >>> t.length
        12345678
        >>> t.type = "audio/mp3"
        >>> t.type
        'audio/mp3'
        >>> t.season = 2
        >>> t.season
        2
        >>> p.add_trailer(t)
        >>> t2 = Trailer("Another teaser", "https://example.org/trailers/teaser", pubdate, type="audio/mp3")
        >>> t2.type
        'audio/mp3'
        >>> p.add_trailer(t2)

    """

    def __init__(self, text, url, pubdate, length=None, type=None, season=None):
        """Create new Trailer object. See the class description of
        :class:´~pod2gen.trailer.Trailer`.

        :param text: The title of the trailer.
        :type text: str
        :param url: Link of the audio or video file to be played
        :type url: str
        :param pubdate: The date the trailer was published. Must be a timezone aware
            datetime object.
        :type pubdate: datetime.datetime
        :param length: (Optional) The length of the file in bytes.
        :type length: int
        :param type: (Optional) The mime type of the file.
        :type type: str
        :param season: (Optional) Specifies that this trailer is for a particular season number.
        :type season: int
        """

        self.__text = None
        self.__url = None
        self.__pubdate = None
        self.__length = None
        self.__type = None
        self.__season = None

        self.text = text
        self.url = url
        self.pubdate = pubdate
        self.length = length
        self.type = type
        self.season = season

        # Trying to guess the mime type from the url
        # if no explicit type was provided
        if self.type is None:
            try:
                self.type = mimetypes.guess_type(self.url)
            except:
                pass

    def rss_entry(self):
        """Create an RSS ``<podcast:trailer>`` tag using lxml's etree and return it.

        This is primarily used by :class:`~.pod2gen.Podcast` for building
        the RSS feed.

        :RSS: ``<podcast:location>``

        :returns: :class:`lxml.etree.Element`
        """

        PODCAST_NS = "https://podcastindex.org/namespace/1.0"
        entry = etree.Element("{%s}trailer" % PODCAST_NS)

        entry.text = self.text
        entry.attrib["url"] = self.url
        entry.attrib["pubdate"] = formatRFC2822(self.pubdate)

        if self.length:
            entry.attrib["length"] = str(self.length)

        if self.type:
            entry.attrib["type"] = self.type

        if self.season:
            entry.attrib["season"] = str(self.season)

        return entry

    @property
    def text(self):
        """The title of the trailer. It should not exceed 128 characters.

        Check `podcast-namespace Trailer node value
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#node-value-7>`_
        for more details.

        :type: :obj:`str`
        """
        return self.__text

    @text.setter
    def text(self, text):
        if not text:
            raise ValueError("Trailer text cannot be None or empty")

        if not isinstance(text, str):
            raise ValueError("Trailer text must be a valid string")

        if len(text) > 128:
            raise ValueError("Trailer text must not exceed 128 characters")

        self.__text = text

    @property
    def url(self):
        """The url/link that points to the audio or video file to be played.

        Check `podcast-namespace Trailer url attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-9>`_
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

    @property
    def pubdate(self):
        """The date the trailer was published. It must a be timezone aware
        :obj:`datetime.datetime` object.
        Ideally use :mod:`dateutil.tz` module for handling timezones. Alternatively,
        :mod:`pytz` can also be used.

        Check `podcast-namespace Trailer pubdate attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-9>`_
        for more details.

        :type: :obj:`datetime.datetime`
        """
        return self.__pubdate

    @pubdate.setter
    def pubdate(self, pubdate):
        if pubdate is None:
            raise ValueError("pubdate cannot be None")

        if isinstance(pubdate, datetime):
            if not pubdate.tzinfo:
                raise ValueError("pubdate must have a defined timezone.")
        else:
            raise TypeError("pubdate must be a timezone aware datetime")

        self.__pubdate = pubdate

    @property
    def length(self):
        """The length of the trailer audio/video file in bytes.

        Check `podcast-namespace Trailer length attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-9>`_
        for more details.

        :type: :obj:`int` or :obj:`None`
        """
        return self.__length

    @length.setter
    def length(self, length):
        if length:
            try:
                length = int(length)
            except ValueError:
                raise TypeError(
                    "length must be an integer. %r could not be converted into integer."
                    % length
                )

            self.__length = length
        else:
            self.__length = None

    @property
    def type(self):
        """The mime type of the trailer file.

        Check `podcast-namespace Trailer type attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-9>`_
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__type

    @type.setter
    def type(self, type):
        if type:
            if not isinstance(type, str):
                raise TypeError("File mime type must be a valid string")
            self.__type = type

        else:
            self.__type = None

    @property
    def season(self):
        """If this attribute is present it specifies that the trailer is for a particular
        season number.

        Check `podcast-namespace Trailer season attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-9>`_
        for more details.

        :type: :obj:`int` or :obj:`None`
        """
        return self.__season

    @season.setter
    def season(self, season):
        if season:
            try:
                season = int(season)
            except ValueError:
                raise TypeError(
                    "season must be an integer. %r could not be converted into integer."
                    % season
                )

            self.__season = season
        else:
            self.__season = None

    def __repr__(self):
        kwargs = {
            "text": self.text,
            "url": self.url,
            "pubdate": self.pubdate,
            "length": self.length,
            "type": self.type,
            "season": self.season,
        }

        output = ""
        for k, v in kwargs.items():
            if v:
                if k == "pubdate":
                    v = formatRFC2822(self.pubdate)

                output = "%s%s='%s', " % (output, k, str(v))

        return "Trailer(%s)" % output[:-2]
