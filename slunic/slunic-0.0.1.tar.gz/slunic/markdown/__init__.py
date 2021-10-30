import logging
import mistune
import bleach
from functools import partial
from slunic.markdown.plugins import gist, twitter, youtube, linkify

from .renderer import SlunicRenderer
from .bleaching import (
    embedder,
    ALLOWED_TAGS,
    ALLOWED_STYLES,
    ALLOWED_ATTRIBUTES,
    ALLOWED_PROTOCOLS,
)


logger = logging.getLogger("engine")


def safe(f):
    """
    Safely call an object without causing errors
    """

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as exc:
            logger.error(f"Error with {f.__name__}: {exc}")
            text = kwargs.get("text", args[0])
            return text

    return inner


def linkifier(text):

    # List of links to embed
    embed = []

    # Try embedding patterns
    targets = [
        (gist.GIST_PATTERN, lambda x: gist.GIST_HTML % x),
        (twitter.TWITTER_PATTERN, twitter.get_tweet),
        (youtube.YOUTUBE_PATTERN1, lambda x: youtube.YOUTUBE_HTML % x),
        (youtube.YOUTUBE_PATTERN2, lambda x: youtube.YOUTUBE_HTML % x),
        (youtube.YOUTUBE_PATTERN3, lambda x: youtube.YOUTUBE_HTML % x),
        (linkify.LINK_PATTERN, lambda x: youtube.linkify.LINK_HTML % (x, x)),
    ]

    html = bleach.linkify(
        text=text,
        callbacks=[
            partial(embedder, targets=targets, embed=embed),
            bleach.callbacks.nofollow,
        ],
        skip_tags=["pre", "code"],
    )

    # Embed links into html.
    for em in embed:
        source, target = em
        emb = f'<a href="{source}" rel="nofollow">{source}</a>'
        html = html.replace(emb, target)
    return html


@safe
def parse(text, clean=False, escape=False):
    """
    Parses markdown into html.
    Expands certain patterns into HTML.

    clean : Applies bleach clean BEFORE mistune escapes unsafe characters.
            Also removes unbalanced tags at this stage.
    escape  : Escape html originally found in the markdown text.
    allow_rewrite : Serve images with relative url paths from the static directory.
                  eg. images/foo.png -> /static/images/foo.png
    """

    renderer = SlunicRenderer(escape=escape)
    markdown = mistune.create_markdown(
        renderer=renderer,
        escape=escape,
        plugins=[
            gist.plugin_gist,
            twitter.plugin_twitter,
            youtube.plugin_youtube,
            linkify.plugin_linkify,
            "strikethrough",
            "footnotes",
            "table",
        ],
    )
    output = markdown(text)

    # Bleach clean the html.
    if clean:
        output = bleach.clean(
            text=output,
            tags=ALLOWED_TAGS,
            styles=ALLOWED_STYLES,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
        )

    # Embed sensitive links into html
    output = linkifier(text=output)

    return output


@safe
def parse_simple(text, clean=True, escape=True):
    """
    Parses markdown into html.
    Expands certain patterns into HTML.

    clean : Applies bleach clean BEFORE mistune escapes unsafe characters.
            Also removes unbalanced tags at this stage.
    escape  : Escape html originally found in the markdown text.
    allow_rewrite : Serve images with relative url paths from the static directory.
                  eg. images/foo.png -> /static/images/foo.png
    """

    renderer = SlunicRenderer(escape=escape)
    markdown = mistune.create_markdown(
        renderer=renderer,
        escape=escape,
        plugins=[
            linkify.plugin_linkify,
            "strikethrough",
            "footnotes",
            "table",
        ],
    )
    output = markdown(text)

    # Bleach clean the html.
    if clean:
        output = bleach.clean(
            text=output,
            tags=ALLOWED_TAGS,
            styles=ALLOWED_STYLES,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOLS,
        )

    # Embed sensitive links into html
    output = linkifier(text=output)

    return output
