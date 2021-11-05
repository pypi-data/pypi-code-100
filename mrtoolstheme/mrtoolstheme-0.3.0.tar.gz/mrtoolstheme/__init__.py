"""Register the Sphinx HTML Theme `mrtools`."""

from os import path


def setup(app):
    """Register the Sphinx HTML Theme `mrtools`."""
    app.add_html_theme('mrtools', path.abspath(path.dirname(__file__)))
