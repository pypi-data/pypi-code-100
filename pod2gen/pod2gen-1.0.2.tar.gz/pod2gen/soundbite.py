# -*- coding: utf-8 -*-
"""
    pod2gen.soundbite
    ~~~~~~~~~~~~~~~

    This module contains Soundbite, which represents an episode soundbite.

    :copyright: 2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""


class Soundbite(object):
    """Class representing an Episode soundbite object.

    By using this class, you can be sure that the soundbite object is formatted correctly
    and will be correctly used by the associated :class:`~.pod2gen.Episode` object.

    :class:`.Soundbite` objects can be attached to :class:`.Episode` objects
    using this method. Soundbites are stored in :attr:`.Episode.soundbites`.

    See `podcast-namespace Soundbite
    <https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#soundbite>`_
    for an overview of the Soundbite tag.

    Example::

        >>> from pod2gen import Soundbite, Episode
        >>> s = Soundbite(1234.5, 42.25, text="Why the Podcast Namespace Matters")
        >>> s.start_time
        1234.5
        >>> s.duration
        42.25
        >>> s.text
        'Why the Podcast Namespace Matters'
        >>> e = Episode()
        >>> e.add_soundbite(s)
        >>> s = Soundbite(73.0, 60)
        >>> s.start_time
        73.0
        >>> s.duration
        60
        >>> e.add_soundbite(s)
        >>> len(e.soundbites)
        2
        >>> # Editing attributes
        >>> s.start_time = 80
        >>> s.start_time
        80
        >>> s.text = "Soundbite example sample"
        >>> s.text
        'Soundbite example sample'
    """

    def __init__(self, start_time, duration, text=None):
        """Create new Soundbite object. See the class description of
        :class:´~pod2gen.soundbite.Soundbite`.

        :param start_time: The time where the soundbite begins in seconds.
        :type start_time: float or int
        :param duration: How long is the soundbite (recommended between 15 and 120 seconds).
        :type duration: float or int
        :param text: (Optional) Free form string to specify a title for the soundbite.
        :type text: str
        """

        self.__start_time = None
        self.__duration = None
        self.__text = None

        self.start_time = start_time
        self.duration = duration
        self.text = text

    @property
    def start_time(self):
        """The time where the soundbite begins in seconds.

        Check https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-4
        for more details.

        :type: :obj:`float`
        """
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time):
        if start_time:
            if not isinstance(start_time, int) and not isinstance(start_time, float):
                try:
                    start_time = float(start_time)
                except:
                    raise ValueError(
                        "start_time value %r could not be converted into a numeric value"
                        % start_time
                    )

            if start_time - int(start_time) == 0:
                start_time = int(start_time)

            self.__start_time = start_time
        else:
            raise ValueError("start_time value cannot be None")

    @property
    def duration(self):
        """How long is the soundbite in seconds.

        Check https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#attributes-4
        for more details.

        :type: :obj:`float`
        """
        return self.__duration

    @duration.setter
    def duration(self, duration):
        if duration is not None:
            if not isinstance(duration, int) and not isinstance(duration, float):
                try:
                    duration = float(duration)
                except:
                    raise ValueError(
                        "duration value %r could not be converted into a numeric value"
                        % duration
                    )

            if duration - int(duration) == 0:
                duration = int(duration)

            self.__duration = duration
        else:
            raise ValueError("duration value cannot be None")

    @property
    def text(self):
        """A free form string from the podcast creator to specify
        a title for the soundbite.

        Check https://github.com/Podcastindex-org/podcast-namespace/blob/main/docs/1.0.md#node-value-2
        for more details.

        :type: :obj:`str` or :obj:`None`
        """
        return self.__text

    @text.setter
    def text(self, text):
        if text is not None:
            if not isinstance(text, str):
                raise ValueError("Soundbite text must be a valid string")

            if len(text) > 128:
                raise ValueError("Soundbite text must not exceed 128 characters")

            self.__text = text
        else:
            self.__text = None

    def __repr__(self):
        if self.__text:
            return "Soundbite(start_time=%s, duration=%s, text=%s)" % (
                self.start_time,
                self.duration,
                self.text,
            )
        return "Soundbite(start_time=%s, duration=%s)" % (
            self.start_time,
            self.duration,
        )
