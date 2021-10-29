# SPDX-FileCopyrightText: 2021 SanderTheDragon <sanderthedragon@zoho.com>
#
# SPDX-License-Identifier: MIT

from pathlib import Path

from sphinx.application import Sphinx
from sphinx.util import fileutil


def add_js(app: Sphinx, path: Path) -> None:
    source = Path(__file__).parent / '_static' / path
    destination = Path(app.builder.outdir) / '_static' / path

    destination.parent.mkdir(exist_ok=True, parents=True)
    fileutil.copy_asset_file(str(source), str(destination))
    app.add_js_file(str(path))


def add_css(app: Sphinx, path: Path) -> None:
    source = Path(__file__).parent / '_static' / path
    destination = Path(app.builder.outdir) / '_static' / path

    destination.parent.mkdir(exist_ok=True, parents=True)
    fileutil.copy_asset_file(str(source), str(destination))
    app.add_css_file(str(path))


def add_static(app: Sphinx) -> None:
    if app.builder.format != 'html':
        return

    add_js(app, Path('js/clipboard.min.js'))

    add_css(app, Path('css/codeblock.css'))
    add_js(app, Path('js/codeblock.js'))


def setup(app: Sphinx) -> None:
    """Add static files to the HTML."""

    app.connect('builder-inited', add_static)
