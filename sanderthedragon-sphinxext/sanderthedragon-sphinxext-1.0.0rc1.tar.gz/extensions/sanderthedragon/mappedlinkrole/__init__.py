# SPDX-FileCopyrightText: 2021 SanderTheDragon <sanderthedragon@zoho.com>
#
# SPDX-License-Identifier: MIT

from functools import partial
from typing import Any, Optional

from docutils.parsers.rst.states import Inliner
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.util import logging, nodes as nodesutil


def make_link(name: str, rawtext: str, text: str, lineno: int, inliner: Inliner,
              options: dict[str, Any] = {}, content: list[str] = [],
              target: Optional[str] = None, mapping: dict[str, str] = {}) \
                  -> tuple[list[nodes.reference], list[nodes.reference]]:
    # Split text into text, key and anchor
    anchor = None

    ( _, text, key ) = nodesutil.split_explicit_title(text)
    if ':' in key:
        ( key, anchor ) = key.split(':', maxsplit=1)

    if len(key) == 0:
        key = text
        if ':' in key:
            ( key, anchor ) = key.split(':', maxsplit=1)

    # Get the URL
    value = mapping.get(key, None if target is None else key)
    if value is None:
        error = inliner.reporter.error(f'"{key}" is not defined for "{name}"',
                                       line=lineno)
        problematic = inliner.problematic(rawtext, rawtext, error)
        return ( [ problematic ], [ error ] )


    url = value
    if target is not None:
        url = target.format(value)

    # Append anchor (if given)
    if anchor is not None:
        if not url.startswith('http://') and not url.startswith('https://'):
            anchor = nodes.make_id(anchor)

        url += '#' + anchor

    node = nodes.reference(rawtext, text, refuri=url)

    return ( [ node ], [] )


def setup(app: Sphinx) -> None:
    """Register nodes and roles."""

    config = app.config._raw_config  # `raw_config` is available in setup

    role_mapping = config.get('role_mapping', {})
    for ( key, value ) in role_mapping.items():
        item_mapping = config.get(key + '_mapping', {})
        if value is None:
            if len(item_mapping.keys()) == 0:
                logger = logging.getLogger('mappedlinkrole')
                logger.warning(f'"{key}" is defined as `None`, but no mapping' \
                                ' is defined')

            app.add_role(key, partial(make_link, mapping=item_mapping))
        else:
            app.add_role(key, partial(make_link, mapping=item_mapping,
                                      target=value))
