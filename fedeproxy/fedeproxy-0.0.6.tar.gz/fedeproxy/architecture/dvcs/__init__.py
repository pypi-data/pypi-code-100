import os

from .git import Git
from .hg import Hg


def factory(directory):
    if os.path.exists(f"{directory}/.git"):
        r = Git(directory, None)
    elif os.path.exists(f"{directory}/.hg"):
        r = Hg(directory, None)
    else:
        assert 0, f"{directory} has no .git or .hg sub-directory"
    r.set_url_from_directory()
    return r
