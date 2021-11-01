""" Bioinformatics """
from orangecontrib.bioinformatics.i18n_config import *


def __(key):
    return i18n.t('bioinformatics.' + key)


NAME = "Bioinformatics"

LABEL = __("package_label")

DESCRIPTION = __("package_desc")

ICON = "icons/Category-Bioinformatics.svg"

BACKGROUND = "light-grass"

# Location of widget help files.
WIDGET_HELP_PATH = (
    # Used for development.
    # You still need to build help pages using
    # make htmlhelp
    # inside doc folder
    ("{DEVELOP_ROOT}/doc/build/html/widgets.html", None),
    # Online documentation url, used when the local documentation is available.
    # Url should point to a page with a section Widgets. This section should
    # includes links to documentation pages of each widget. Matching is
    # performed by comparing link caption to widget name.
    ("https://orange3-bioinformatics.readthedocs.io/en/latest/widgets.html", ""),
)
