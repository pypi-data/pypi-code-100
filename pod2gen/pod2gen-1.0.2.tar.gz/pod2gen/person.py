# -*- coding: utf-8 -*-
"""
    pod2gen.person
    ~~~~~~~~~~~~~

    This file contains the Person class, which is used to represent a person or
    an entity.

    :copyright: 2016, Thorben Dahl <thorben@sjostrom.no>
        2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
import warnings
from urllib.parse import urlparse

import validators
from lxml import etree

from pod2gen.warnings import (
    NotSupportedByItunesWarning,
    UnknownPersonGroup,
    UnknownPersonGroupRoleTuple,
    UnknownPersonRole,
)


class Person(object):
    """Data-oriented class representing a single person or entity.

    A Person can represent both real persons and less personal entities like
    organizations. Example::

        >>> p.authors = [Person("Example Radio", "mail@example.org")]

    The RSS Namespace Extension for Podcasting adds a ``<podcast:person>``
    tag for episodes and podcasts. :class:`~pod2gen.Person` can be appended
    to :class:`Episode.persons <pod2gen.Episode.persons>` using
    :meth:`Episode.add_person() <pod2gen.Episode.add_person>` or
    to :class:`Podcast.persons <pod2gen.Podcast.persons>` using
    :meth:`Podcast.add_person() <pod2gen.Podcast.add_person>`.

        >>> director = Person(name="Slim", group="Creative Direction", role="Director")
        >>> p.add_person(director)
        >>> guest = Person(email="mslimbeji@gmail.com", group="Cast", role="Guest")
        >>> my_episode.add_person(guest)

    .. note::

        At any time, one of name or email must be present.
        Both cannot be None or empty at the same time.

    .. warning::

        **Any names and email addresses** you put into a Person object will
        eventually be included and **published** together with
        the feed. If you want to keep a name or email address private, then you
        must make sure it isn't used in a Person object (or to be precise: that
        the Person object with the name or email address isn't used in any
        Podcast or Episode.)

    Example of use::

        >>> from pod2gen import Person, Podcast, Episode
        >>> Person("John Doe")
        Person(name=John Doe, email=None)
        >>> Person(email="johndoe@example.org")
        Person(name=None, email=johndoe@example.org)
        >>> Person()
        ValueError: You must provide either a name or an email address.
        >>> p = Person(name="Slim Beji", href="https://github.com/SlimBeji" img="https://examples.com/slimbeji.jpg")
        >>> p.name
        'Slim Beji'
        >>> p.href
        'https://github.com/SlimBeji'
        >>> p.img
        'https://examples.com/slimbeji.jpg'
        >>> p.img = "https://examples.com/slimbeji_2.png"
        >>> p.img
        'https://examples.com/slimbeji_2.png'
        >>> my_podcast = Podcast()
        >>> my_podcast.add_person(p)
        >>> my_episode = Episode
        >>> my_episode.add_person(p)

    .. seealso::
       :ref:`pod2gen.Person-guide`
          for a more gentle introduction.

    """

    _role_group_taxonomy_mapping = {
        "creative direction": [
            "director",
            "assistant director",
            "executive producer",
            "senior producer",
            "producer",
            "associate producer",
            "development producer",
            "creative director",
        ],
        "cast": [
            "host",
            "co-host",
            "guest host",
            "guest",
            "voice actor",
            "narrator",
            "announcer",
            "reporter",
        ],
        "writing": [
            "author",
            "editorial director",
            "co-writer",
            "writer",
            "songwriter",
            "guest writer",
            "story editor",
            "managing editor",
            "script editor",
            "script coordinator",
            "researcher",
            "editor",
            "fact checker",
            "translator",
            "transcriber",
            "logger",
        ],
        "audio production": [
            "studio coordinator",
            "technical director",
            "technical manager",
            "audio engineer",
            "remote recording engineer",
            "post production engineer",
        ],
        "audio post-production": [
            "audio editor",
            "sound designer",
            "foley artist",
            "composer",
            "theme music",
            "music production",
            "music contributor",
        ],
        "administration": [
            "production coordinator",
            "booking coordinator",
            "production assistant",
            "content manager",
            "marketing manager",
            "sales representative",
            "sales manager",
        ],
        "visuals": [
            "graphic designer",
            "cover art designer",
        ],
        "community": [
            "social media manager",
        ],
        "misc.": [
            "consultant",
            "intern",
        ],
        "video production": [
            "camera operator",
            "lighting designer",
            "camera grip",
            "assistant camera",
        ],
        "video post-production": [
            "editor",
            "assistant editor",
        ],
    }

    _available_role_taxonomy = [
        item for sublist in _role_group_taxonomy_mapping.values() for item in sublist
    ]

    def __init__(
        self, name=None, email=None, group=None, role=None, img=None, href=None
    ):
        """Create new person with a name, email or both.

        You don't need to provide both a name and an email, but you must
        provide one of them.

        :param name: This person's name.
        :type name: str or None
        :param email: This person's email address. The address it made public
            when the feed is published, so be careful about adding a personal
            email address here. The spambots are always on lookout!
        :type email: str or None
        :param group: used to identify what role the person serves on the show or episode.
        :type group: str or None
        :param role: this should be a reference to an official group within the Podcast
            Taxonomy Project list. See the below link for the full taxonomy
            https://github.com/Podcastindex-org/podcast-namespace/blob/main/taxonomy.json
        :type role: str or None
        :param img: This is the url of a picture or avatar of the person.
        :type img: str or None
        :param href: The url to a relevant resource of information about the person,
            such as a homepage or third-party profile platform.
        :type href: str or None

        """
        if not self._is_valid(name, email):
            raise ValueError("You must provide either a name or an email " "address.")

        self.__name = name
        self.__email = email
        self.__group = None
        self.__role = None
        self.__img = None
        self.__href = None

        self.group = group
        self.role = role
        self.img = img
        self.href = href

    def rss_entry(self):
        """Create an RSS ``<podcast:person>`` tag using lxml's etree and return it.

        This is primarily used by the :class:`~pod2gen.Podcast` class and the
        :class:`~pod2gen.Episode` class when generating RSS feeds as the Person
        tag parent is either the channel (podcast) or item (episode)

        :RSS: ``<podcast:person>``

        :returns: :class:`lxml.etree.Element`
        """
        PODCAST_NS = "https://podcastindex.org/namespace/1.0"
        entry = etree.Element("{%s}person" % PODCAST_NS)

        if self.name:
            entry.text = self.name
        else:
            entry.text = self.email

        if self.role:
            entry.attrib["role"] = self.role

        if self.group:
            entry.attrib["group"] = self.group

        if self.img:
            entry.attrib["img"] = self.img

        if self.href:
            entry.attrib["href"] = self.href

        if self.role and self.group:
            if self.role not in self._role_group_taxonomy_mapping.get(self.group, []):
                warnings.warn(
                    "role %s does not belong to the group %s according "
                    "to the podcast taxonomy project." % (self.role, self.group),
                    UnknownPersonGroupRoleTuple,
                    stacklevel=2,
                )

        return entry

    def _is_valid(self, name, email):
        """Check whether one of name and email are usable."""
        return name or email

    @property
    def name(self):
        """This person's name.

        :type: :obj:`str`
        """
        return self.__name

    @name.setter
    def name(self, new_name):
        if not self._is_valid(new_name, self.email):
            raise ValueError(
                "The name or email must be present at any time, "
                'cannot set name to "%s" as long as email is '
                '"%s"' % (new_name, self.email)
            )

        if new_name is not None:
            if len(new_name) > 128:
                raise ValueError("The name must not exceed 128 characters.")

        self.__name = new_name

    @property
    def email(self):
        """This person's public email address.

        :type: :obj:`str`
        """
        return self.__email

    @email.setter
    def email(self, new_email):
        if not self._is_valid(self.name, new_email):
            raise ValueError(
                "The name or email must be present at any time, "
                'cannot set email to "%s" as long as name is '
                '"%s"' % (new_email, self.name)
            )
        self.__email = new_email

    @property
    def group(self):
        """Used to identify what group of roles the person belongs to on the
        show or episode. This should be a reference to an official group within the
        `Podcast Taxonomy Project <https://podcasttaxonomy.com/home>`_ list.

        Check this link for the full Podcast Taxonomy `example
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/taxonomy.json>`_.

        See `podcast-namespace Person attributes
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-5>`_
        for more details about the group attribute.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__group

    @group.setter
    def group(self, group):
        if group:
            if not isinstance(group, str):
                raise ValueError("group must be a valid string")

            group = group.lower()
            if group not in self._role_group_taxonomy_mapping:
                warnings.warn(
                    "The group %s is not part of the official podcast taxonomy" % group,
                    UnknownPersonGroup,
                    stacklevel=2,
                )

            self.__group = group

        else:
            self.__group = None

    @property
    def role(self):
        """Used to identify what role the person serves on the
        show or episode. This should be a reference to an official role within the
        `Podcast Taxonomy Project <https://podcasttaxonomy.com/home>`_ list.

        Check this link for the full Podcast Taxonomy `example
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/taxonomy.json>`_.

        See `podcast-namespace Person attributes
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-5>`_
        for more details about the role attribute.

        :type: :obj:`str` or :obj:`None``
        """
        return self.__role

    @role.setter
    def role(self, role):
        if role:
            if not isinstance(role, str):
                raise ValueError("role must be a valid string")

            role = role.lower()
            if role not in self._available_role_taxonomy:
                warnings.warn(
                    "The role %s is not part of the official podcast taxonomy" % role,
                    UnknownPersonRole,
                    stacklevel=2,
                )

            self.__role = role

        else:
            self.__role = None

    @property
    def img(self):
        """This is the url of a picture or avatar of the person.

        See `podcast-namespace Person attributes
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-5>`_
        for more details about the img attribute.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__img

    @img.setter
    def img(self, img):
        if img is not None:
            if validators.url(img) is not True:
                raise ValueError("Not a valid url: %s" % img)

            parsed_url = urlparse(img)
            if parsed_url.scheme not in ("http", "https"):
                warnings.warn(
                    "URL scheme %s is not supported by iTunes. Make sure "
                    "you use absolute URLs and HTTP or HTTPS." % parsed_url.scheme,
                    NotSupportedByItunesWarning,
                    stacklevel=2,
                )
            self.__img = img
        else:
            self.__img = None

    @property
    def href(self):
        """The url to a relevant resource of information about the person,
        such as a homepage or third-party profile platform.

        See `podcast-namespace Person attributes
        <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-5>`_
        for more details about the href attribute.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__href

    @href.setter
    def href(self, href):
        if href is not None:
            if validators.url(href) is not True:
                raise ValueError("Not a valid url: %s" % href)

            parsed_url = urlparse(href)
            if parsed_url.scheme not in ("http", "https"):
                warnings.warn(
                    "URL scheme %s is not supported by iTunes. Make sure "
                    "you use absolute URLs and HTTP or HTTPS." % parsed_url.scheme,
                    NotSupportedByItunesWarning,
                    stacklevel=2,
                )
            self.__href = href
        else:
            self.__href = None

    def __str__(self):
        if self.email is None:
            return self.name
        elif self.name is None:
            return self.email
        else:
            return "%s (%s)" % (self.email, self.name)

    def __repr__(self):
        return "Person(name=%s, email=%s)" % (self.name, self.email)
