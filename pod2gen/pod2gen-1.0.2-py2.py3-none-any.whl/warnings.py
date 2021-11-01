# -*- coding: utf-8 -*-
"""
    pod2gen.warnings
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This file contains pod2gen-specific warnings.
    They can be imported directly from ``pod2gen``.

    :copyright: 2019, Thorben Dahl <thorben@sjostrom.no>
        2021, Slim Beji <mslimbeji@gmail.com>
    :license: FreeBSD and LGPL, see license.* for more details.
"""


class Pod2genWarning(UserWarning):
    """
    Superclass for all warnings defined by pod2gen.
    """

    pass


class NotRecommendedWarning(Pod2genWarning):
    """
    Warns against behaviour or usage which is usually discouraged. However,
    there may exist exceptions where there is no better way.
    """

    pass


class LegacyCategoryWarning(Pod2genWarning):
    """
    Indicates that the category created is an old category. It will still be
    accepted by Apple Podcasts, but it would be wise to use the new categories
    since they may have more relevant options for your podcast.

    .. seealso::

       `What's New: Enhanced Apple Podcasts Categories <https://itunespartner.apple.com/podcasts/whats-new/100002564>`_
          Consequences of using old categories.

       `Podcasts Connect Help: Apple Podcasts categories <https://help.apple.com/itc/podcasts_connect/#/itc9267a2f12>`_
          Up-to-date list of available categories.

       `Podnews: New and changed Apple Podcasts categories <https://podnews.net/article/apple-changed-podcast-categories-2019>`_
          List of changes between the old and the new categories.
    """

    pass


class NotSupportedByItunesWarning(Pod2genWarning):
    """
    Indicates that pod2gen is used in a way that may not be compatible with Apple
    Podcasts (previously known as iTunes).

    In some cases, this may be because pod2gen has not been kept up-to-date with
    new features which Apple Podcasts has added support for. Please add an issue
    if that is the case!
    """

    pass


class LockedTagCannotBeSet(Pod2genWarning):
    """
    Indicates that the tag ``<podcast:locked>`` cannot be generated.

    The Locked tag requires the podcast owner email to be defined
    """

    pass


class UnknownPersonGroup(Pod2genWarning):
    """
    Indicates that the person group for the tag ```<podcast:person>``` is not
    within the Podcast Taxonomy Project list.

    Check the below link for the full podcast taxonomy:
    https://github.com/Podcastindex-org/podcast-namespace/blob/main/taxonomy.json
    """

    pass


class UnknownPersonRole(Pod2genWarning):
    """
    Indicates that the person role for the tag ``<podcast:person>`` is not
    within the Podcast Taxonomy Project list.

    Check the below link for the full podcast taxonomy:
    https://github.com/Podcastindex-org/podcast-namespace/blob/main/taxonomy.json
    """

    pass


class UnknownPersonGroupRoleTuple(Pod2genWarning):
    """
    Indicates that the person role and group for the tag ``<podcast:person>`` does
    not match according to the Podcast Taxonomy Project list.

    Check the below link for the full podcast taxonomy:
    https://github.com/Podcastindex-org/podcast-namespace/blob/main/taxonomy.json
    """

    pass
