# -*- coding: utf-8 -*-
"""
    pod2gen.alternate_media
    ~~~~~~~~~~~~

    This file contains the AlternateMedia class which is the implementation of the RSS
    element podcast:alternateEnclosure representing an alternative to the RSS element
    enclosure which is implemented in the pod2gen.media.Media class

    :copyright: 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import pycountry
import validators
from lxml import etree


class AlternateMedia(object):
    """Data-oriented class representing several urls pointing to a media file.

    The AlternateMedia class represents the podcast:alternateEnclosure RSS element and is
    an alternative to the :class:`~pod2gen.Media` class representing enclosure RSS element.

    This element is meant to provide different versions of, or companion media to the
    main ``<enclosure>`` file. This could be an audio only version of a video podcast to
    allow apps to switch back and forth between audio/video, lower (or higher) bitrate
    versions for bandwidth constrained areas, alternative codecs for different device
    platforms, alternate URI schemes and download types such as IPFS or WebTorrent,
    commentary tracks or supporting source clips, etc.

        >>> from pod2gen import AlternateMedia
        >>> am = AlternateMedia(
        ...     "audio/mp4",
        ...     43200000,
        ...     bitrate=128000,
        ...     height=1080,
        ...     lang="en-US",
        ...     title="Standard",
        ...     rel="Off stage",
        ...     codecs="mp4a.40.2",
        ...     default=False,
        ...     encryption="sri",
        ...     signature="sha384-ExVqijgYHm15PqQqdXfW95x+Rs6C+d6E/ICxyQOeFevnxNLR/wtJNrNYTjIysUBo",
        ... )
        >>>


    In the `RSS Namespace Extension for Podcasting <https://podcastindex.org/namespace/1.0>`_,
    ``<podcast:alternateEnclosure>`` has two type of child tags:

    * ``<podcast:source>``
    * ``<podcast:integrity>``

    **Source tag**

    ``<podcast:source>`` defines a uri location for a media file. It is meant to be used
    as a child of the ``<podcast:alternateEnclosure>`` element, thus
    :class:`~pod2gen.AlternateMedia` must have at least one source added otherwise no
    ``<podcast:alternateEnclosure>``.

        >>> # Adding a file without specifying the content type
        >>> am.add_source("https://example.com/file-0.mp3")
        >>> # Adding a file, then specifying the content type later on
        >>> am.add_source("ipfs://QmdwGqd3d2gFPGeJNLLCshdiPert45fMu84552Y4XHTy4y")
        >>> am.edit_source_content(
        ...     "ipfs://QmdwGqd3d2gFPGeJNLLCshdiPert45fMu84552Y4XHTy4y",
        ...     "audio/mpeg",
        ... )
        >>> # Adding a file with a specified content type
        >>> am.add_source("https://example.com/file-0.torrent", "application/x-bittorrent")
        >>> # Deleting a source by its uri
        >>> am.delete_source("ipfs://QmdwGqd3d2gFPGeJNLLCshdiPert45fMu84552Y4XHTy4y")

    .. seealso::
       :ref:`pod2gen.Episode-alternateEnclosure-sources`
          for more details about Alternate enclosure sources.

    **Integrity tag**

    ``<podcast:integrity>`` defines a method of verifying integrity of the media
    given either an SRI-compliant integrity string (preferred) or a base64 encoded
    PGP signature. This tag is optional within a ``<podcast:alternateEnclosure>`` element.
    It allows to ensure that the file has not been tampered with.

    ``<podcast:integrity>`` is generated for a group of identical media file when the parent
    :class:`~pod2gen.AlternateMedia` object has a defined :obj:`~pod2gen.AlternateMedia.encryption`
    and :obj:`~pod2gen.AlternateMedia.signature` values.

        >>> am.encryption = "sri"
        >>> am.signature = "sha384-ExVqijgYHm15PqQqdXfW95x+Rs6C+d6E/ICxyQOeFevnxNLR/wtJNrNYTjIysUBo"

    .. seealso::
       :ref:`pod2gen.Episode-alternateEnclosure-integrity`
          for more details about Alternate enclosure integrity tag.

    """

    def __init__(
        self,
        type,
        length,
        bitrate=None,
        height=None,
        lang=None,
        title=None,
        rel=None,
        codecs=None,
        default=None,
        encryption=None,
        signature=None,
    ):

        self.__type = None
        self.__length = None
        self.__bitrate = None
        self.__height = None
        self.__lang = None
        self.__title = None
        self.__rel = None
        self.__codecs = None
        self.__default = None
        self.__encryption = None
        self.__signature = None
        self.__sources = {}

        self.type = type
        self.length = length
        self.bitrate = bitrate
        self.height = height
        self.lang = lang
        self.title = title
        self.rel = rel
        self.codecs = codecs
        self.default = default
        self.encryption = encryption
        self.signature = signature

    def rss_entry(self):
        """Create an RSS ``<podcast:alternateEnclosure>`` using lxml's etree and return it.

        This element is meant to provide different versions of, or companion media to
        the main ``<enclosure>`` file. This could be an audio only version of a video podcast
        to allow apps to switch back and forth between audio/video, lower (or higher)
        bitrate versions for bandwidth constrained areas, alternative codecs for different
        device platforms, alternate URI schemes and download types such as IPFS or WebTorrent,
        commentary tracks or supporting source clips, etc.

        This is primarily used by :class:`~.pod2gen.Episode` for building
        the RSS feed.

        :returns: :class:`lxml.etree.Element`
        :RSS: ``<podcast:alternateEnclosure>``
        """
        PODCAST_NS = "https://podcastindex.org/namespace/1.0"

        if self.__sources:
            element = etree.Element("{%s}alternateEnclosure" % PODCAST_NS)

            element.attrib["type"] = self.__type
            element.attrib["length"] = str(self.__length)

            if self.__bitrate:
                element.attrib["bitrate"] = str(self.__bitrate)

            if self.__height:
                element.attrib["height"] = str(self.__height)

            if self.__lang:
                element.attrib["lang"] = self.__lang

            if self.__title:
                element.attrib["title"] = self.__title

            if self.__rel:
                element.attrib["rel"] = self.__rel

            if self.__codecs:
                element.attrib["codecs"] = self.__codecs

            if self.__default is not None:
                if self.__default:
                    element.attrib["default"] = "true"
                else:
                    element.attrib["default"] = "false"

            for uri, content_type in self.__sources.items():
                source = etree.Element("{%s}source" % PODCAST_NS)
                source.attrib["uri"] = uri
                if content_type:
                    source.attrib["contentType"] = content_type
                element.append(source)

            if self.__encryption and self.__signature:
                integrity = etree.Element("{%s}integrity" % PODCAST_NS)
                integrity.attrib["type"] = self.__encryption
                integrity.attrib["value"] = self.__signature
                element.append(integrity)

            return element

        else:
            return None

    @property
    def type(self):
        """The MIME type of the files within the alternateEnclosure.

        See https://en.wikipedia.org/wiki/Media_type for an introduction.

        :type: :obj:`str`
        """
        return self.__type

    @type.setter
    def type(self, type):
        if not type:
            raise ValueError(
                "type property of SuperMedia objects cannot be empty or None"
            )

        if not isinstance(type, str):
            raise TypeError("File mime type must be a valid string")
        self.__type = type

    @property
    def length(self):
        """The length of the file bytes.

        Check `podcast-namespace Alternate Enclosure length attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`int`
        """
        return self.__length

    @length.setter
    def length(self, length):
        if not length:
            raise ValueError(
                "length property of SuperMedia objects cannot be empty or None"
            )

        try:
            length = int(length)
        except ValueError:
            raise TypeError(
                "length must be an integer. %r could not be converted into integer."
                % length
            )

        self.__length = length

    @property
    def bitrate(self):
        """The Encoding bitrate of media asset.

        Check `podcast-namespace Alternate Enclosure bitrate attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`float` or :obj:`None`
        """
        return self.__bitrate

    @bitrate.setter
    def bitrate(self, bitrate):
        if bitrate:
            try:
                bitrate = float(bitrate)
            except ValueError:
                raise TypeError(
                    "bitrate must be a float. %r could not be converted into float."
                    % bitrate
                )

            self.__bitrate = bitrate

        else:
            self.__bitrate = None

    @property
    def height(self):
        """Height of the media asset for video formats.

        Check `podcast-namespace Alternate Enclosure height attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`int` or :obj:`None`
        """
        return self.__height

    @height.setter
    def height(self, height):
        if height:
            try:
                height = int(height)
            except ValueError:
                raise TypeError(
                    "height must be an integer. %r could not be converted into integer."
                    % height
                )

            self.__height = height

        else:
            self.__height = None

    @property
    def lang(self):
        """An `IETF language tag (BCP 47) code <https://en.wikipedia.org/wiki/IETF_language_tag>`_
        identifying the language of the media files.

        Check `podcast-namespace Alternate Enclosure lang attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__lang

    @lang.setter
    def lang(self, lang):
        if lang:
            language_country = lang.split("-")
            language = language_country[0]
            if len(language_country) > 1:
                country = language_country[1]
            else:
                country = None

            try:
                language = pycountry.languages.get(alpha_2=language).alpha_2
            except Exception as e:
                raise ValueError("Language code %r is unknown" % language)

            if country:
                try:
                    country = pycountry.countries.lookup(country).alpha_2
                    self.__lang = language + "-" + country
                except:
                    raise ValueError("Country code %r is unknown" % country)
            else:
                self.__lang = language

        else:
            self.__lang = None

    @property
    def title(self):
        """A human-readable string identifying the name of the media asset.

        Check `podcast-namespace Alternate Enclosure title attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__title

    @title.setter
    def title(self, title):
        if title:
            if not isinstance(title, str):
                raise ValueError("Title field must be a valid string")

            if len(title) > 32:
                raise ValueError("Title field must not exceed 32 characters")

            self.__title = title

        else:
            self.__title = None

    @property
    def rel(self):
        """Provides a method of offering and/or grouping together different media elements.

        Check `podcast-namespace Alternate Enclosure rel attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__rel

    @rel.setter
    def rel(self, rel):
        if rel:
            if not isinstance(rel, str):
                raise ValueError("rel field must be a valid string")

            if len(rel) > 32:
                raise ValueError("rel field must not exceed 32 characters")

            self.__rel = rel

        else:
            self.__rel = None

    @property
    def codecs(self):
        """An `RFC 6381 string <https://datatracker.ietf.org/doc/html/rfc6381>`_
        specifying the codecs available in this media.

        Check `podcast-namespace Alternate Enclosure codecs attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__codecs

    @codecs.setter
    def codecs(self, codecs):
        if codecs:
            if not isinstance(codecs, str):
                raise ValueError("codecs field must be a valid string")

            self.__codecs = codecs

        else:
            self.__codecs = None

    @property
    def default(self):
        """Boolean specifying whether or not the given media is the same as the episode
        file in the Media object. If :obj:`True`, the given media should be considered the
        default one for the episode.

        Check `podcast-namespace Alternate Enclosure default attribute
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-11>`_
        for more details.

        :type: :obj:`bool`
        """
        return self.__default

    @default.setter
    def default(self, default):
        if default is not None:
            if isinstance(default, bool):
                self.__default = default
            else:
                raise ValueError("default attribute must be a boolean")
        else:
            self.__default = None

    @property
    def encryption(self):
        """Method of verifying integrity of the media file.
        Accepted values are either ``"sri"`` or ``"pgp-signature"``

        When specified with :attr:`AlternateMedia.signature`, a ``<podcast:integrity>``
        tag will be appended to the parent ``<podcast:alternateEnclosure>``.

        Check `podcast-namespace Integrity tag
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#integrity>`_
        for more details.

        :type: :obj:`str`
        """
        return self.__encryption

    @encryption.setter
    def encryption(self, encryption):
        if encryption is not None:
            if encryption not in ["sri", "pgp-signature"]:
                raise ValueError(
                    "encryption value can either be 'sri' or 'pgp-signature'"
                )

            self.__encryption = encryption

        else:
            self.__encryption = None

    @property
    def signature(self):
        """Media signature based on the selected :attr:`AlternateMedia.encryption`:
        ``"sri"`` or ``"pgp-signature"``

        When specified with :attr:`AlternateMedia.encryption`, a ``<podcast:integrity>``
        tag will be appended to the parent ``<podcast:alternateEnclosure>``.

        Check `podcast-namespace Integrity tag
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#integrity>`_
        for more details.

        :type: :obj:`str`
        """

        return self.__signature

    @signature.setter
    def signature(self, signature):
        if signature:
            if not isinstance(signature, str):
                raise TypeError("signature can only be a string")

            self.__signature = signature

        else:
            self.__signature = None

    def add_source(self, uri, type=None):
        """Append a new source to the AlternateMedia object. Use this method
        instead of editing :attr:`AlternateMedia.sources <pod2gen.AlternateMedia.sources>`

        :param uri: The uri where the media file to append resides
        :type uri: str
        :param type: (Optional) MIME type of the media file to append
        :type type: str or None
        """

        if not isinstance(uri, str):
            raise TypeError("uri must be a string.")

        if uri in self.__sources:
            raise ValueError(
                "uri %s already defined. "
                "Please use edit_source method for modifications." % uri
            )

        if type is not None:
            if not isinstance(type, str):
                raise TypeError(
                    "type parameter of add_source method must be a string or None."
                )

            if not type:
                type = None

        if validators.url(uri) is not True:
            if not uri.startswith("ipfs://"):
                raise ValueError("Not a valid url: %s" % uri)

        self.__sources[uri] = type

    def delete_source(self, uri):
        """Delete a source from :attr:`AlternateMedia.sources`. Use this method
        instead of editing :attr:`AlternateMedia.sources <pod2gen.AlternateMedia.sources>`.

        :param uri: The media file uri to remove
        :type uri: str
        """

        if uri in self.__sources:
            del self.__sources[uri]

    def edit_source_content(self, uri, type):
        """Edit a media file content type from :attr:`AlternateMedia.sources`.
        Use this method instead of editing :attr:`AlternateMedia.sources <pod2gen.AlternateMedia.sources>`.

        :param uri: The media file uri to edit.
        :type uri: str
        :param type: The media file content type.
        :type type: str
        """

        if uri not in self.__sources:
            raise LookupError("uri %s does not exists within %r" % (uri, self))

        if type is not None and not isinstance(type, str):
            raise TypeError(
                "type parameter of edit_source_content method must be a string or None."
            )

        if not type:
            type = None

        self.__sources[uri] = type

    @property
    def sources(self):
        """A dictionary with uri as keys and content type as values. Each key/value pair
        represents a media file; the key is the uri where the media file resides and the
        value represents the content type. The content type is optional and :obj:`None` by default.
        It is useful if the transport mechanism is different than the type mentioned for
        the parent AlternateMedia object.

        For each source, a ``<podcast:source>`` is appended to the parent ``<podcast:alternateEnclosure>``.
        when generating the RSS feed.

        Check `podcast-namespace Source
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#source>`_
        for more details about the ``<podcast:source>`` tag.

        :type: :obj:`dict`
            { ``uri``: :obj:`str` : ``content_type``: :obj:`str` or :obj:`None` }
        """
        return self.__sources

    @sources.setter
    def sources(self, sources):
        old_sources = self.__sources

        if not isinstance(sources, dict):
            raise TypeError(
                "sources parameter must be a dictionary with uris "
                "as keys and contentType/None as values."
            )

        try:
            self.__sources = {}
            for k, v in sources.items():
                self.add_source(k, v)
        except Exception as e:
            self.__sources = old_sources
            raise e

    def __repr__(self):
        if self.title:
            return "AlternateMedia(title=%s) at %s" % (self.title, id(self))
        return "AlternateMedia(type=%s, length=%s) at %s" % (
            self.type,
            self.length,
            id(self),
        )
