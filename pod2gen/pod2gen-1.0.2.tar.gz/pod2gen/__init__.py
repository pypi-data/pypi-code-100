# -*- coding: utf-8 -*-
"""
    pod2gen
    ~~~~~~

    Package which makes it easy to generate podcast RSS using Python.

    See the official documentation at https://pod2gen.caproni.fm

    :copyright: 2016, Thorben Dahl <thorben@sjostrom.no>
        2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""
from .alternate_media import AlternateMedia
from .category import Category
from .constants import EPISODE_TYPE_BONUS, EPISODE_TYPE_FULL, EPISODE_TYPE_TRAILER
from .episode import Episode
from .funding import Funding
from .license import License
from .location import Location
from .media import Media
from .person import Person
from .podcast import Podcast
from .soundbite import Soundbite
from .trailer import Trailer
from .transcript import Transcript
from .util import htmlencode
from .warnings import (
    LegacyCategoryWarning,
    NotRecommendedWarning,
    NotSupportedByItunesWarning,
    Pod2genWarning,
)
