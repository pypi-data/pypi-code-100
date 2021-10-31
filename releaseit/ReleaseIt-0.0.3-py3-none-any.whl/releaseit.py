"""ReleaseIt manages release notes for Python projects.

ReleaseIt keeps release notes for Python projects in a dict structure.
It aims to standardise, facilitate and automate the management of
release notes when publishing a project to GitHub, PyPI and
ReadTheDocs.  It is developed as part of the PackageIt project, but can
be used independently as well.

See also https://pypi.org/project/PackageIt/
"""

import logging
from pathlib import Path
import tempfile
import toml
from beetools.beearchiver import Archiver

_PROJ_DESC = __doc__.split("\n")[0]
_PROJ_PATH = Path(__file__)
_PROJ_NAME = _PROJ_PATH.stem
_PROJ_VERSION = "0.0.1"


class ReleaseIt:
    """ReleaseIt manages release notes for Python projects."""

    def __init__(self, p_dir, p_parent_log_name="", p_verbose=True):
        """Initialize the class

        Parameters
        ----------
        p_dir : Path
            Directory path where the release notes are or will be created in.
        p_parent_log_name : str, default = ''
            Name of the parent.  In combination witt he class name it will
            form the logger name.
        p_verbose: bool, default = True
            Write messages to the console.

        Examples
        --------
        >>> import tempfile
        >>> from pathlib import Path
        >>> rit = ReleaseIt(Path(tempfile.mkdtemp(prefix=_PROJ_NAME)))
        >>> rit.release_pth # doctest: +ELLIPSIS
        WindowsPath('.../release.toml')
        """
        self.success = True
        if p_parent_log_name:
            self._log_name = "{}.{}".format(p_parent_log_name, _PROJ_NAME)
            self.logger = logging.getLogger(self._log_name)
        self.verbose = p_verbose

        self.release_pth = Path(p_dir, "release.toml")
        if not self.release_pth.exists():
            self._create_release_config()
        self.release_cfg = toml.load(self.release_pth)
        pass

    def _create_release_config(self):
        """Create the "release.toml" configuration file.

        Create the "release.toml" configuration file with the default
        contents as if it is the first release (0.0.1).  If the file
        already exists, it will be overwritten.
        This method is called during instantiation of the class.

        Parameters
        ----------

        Returns
        -------
        release_pth : Path
            Path to the "release.toml" file.
        """
        contents = """[release]\n[release.0]\n[release.0.0]\n1 = [\n    'Creation of the project',\n]\n"""
        self.release_pth.write_text(contents)
        return self.release_pth


def do_examples(p_cls=True):
    """A collection of implementation examples for ReleaseIt.

    A collection of implementation examples for ReleaseIt. The examples
    illustrate in a practical manner how to use the methods.  Each example
    show a different concept or implementation.

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the method

    """
    do_example1(p_cls)


def do_example1(p_cls=True):
    """A working example of the implementation of ReleaseIt.

    Example1 illustrate the following concepts:
    1. Creates to object
    2. Create a default 'release.toml' file in teh designated (temp) directory

    Parameters
    ----------
    p_cls : bool, default = True
        Clear the screen or not at startup of Archiver

    Returns
    -------
    success : boolean
        Execution status of the method

    """
    success = True
    archiver = Archiver(_PROJ_NAME, _PROJ_VERSION, _PROJ_DESC, _PROJ_PATH)
    archiver.print_header(p_cls=p_cls)
    releaseit = ReleaseIt(Path(tempfile.mkdtemp(prefix=_PROJ_NAME)))
    print(releaseit.release_pth)
    print(releaseit.release_cfg)
    archiver.print_footer()
    return success


if __name__ == "__main__":
    do_examples()
