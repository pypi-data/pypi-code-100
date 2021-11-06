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
_PROJ_VERSION = "0.0.3"

_TOML_CONTENTS_DEF = """[release]
[release.0]
[release.0.0.0.Detail]
Header = 'Creation of the project'
Description01 = 'List all the changes to the project here.'
Description02 = 'Changes listed here will be in the release notes under the above heading.'
[release.0.0.0.Changes]
File001 = ['filename01.py','Insert change description here.']
File002 = ['filename02.txt','Insert change description here.']
"""


class ReleaseIt:
    """ReleaseIt manages release notes for Python projects."""

    def __init__(self, p_src, p_parent_log_name="", p_verbose=True):
        """Initialize the class

        Parameters
        ----------
        p_src : Path
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
        >>> rit.src_pth # doctest: +ELLIPSIS
        WindowsPath('.../release.toml')
        """
        self.success = True
        if p_parent_log_name:
            self._log_name = "{}.{}".format(p_parent_log_name, _PROJ_NAME)
            self.logger = logging.getLogger(self._log_name)
        self.verbose = p_verbose

        self.src_pth = Path(p_src, "release.toml")
        if not self.src_pth.exists():
            self._create_def_config()
        self.release_notes = toml.load(self.src_pth)
        self.seq = []
        self._get_config_list()
        self._sort()
        self.curr_pos = 0
        self.element_cntr = len(self.seq)
        pass

    def __iter__(self):
        self.curr_pos = 0
        return self

    def __next__(self):
        if self.curr_pos < self.element_cntr:
            element = self.release_notes["release"][self.seq[self.curr_pos][0]][
                self.seq[self.curr_pos][1]
            ][self.seq[self.curr_pos][2]]
            self.curr_pos += 1
            return element
        else:
            raise StopIteration

    def _create_def_config(self):
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
        self.src_pth.write_text(_TOML_CONTENTS_DEF)
        return self.src_pth

    def _get_config_list(self):
        for major in self.release_notes["release"]:
            for minor in self.release_notes["release"][major]:
                for patch in self.release_notes["release"][major][minor]:
                    self.seq.append([major, minor, patch])
        self.seq

    def _sort(self):
        self.seq = sorted(self.seq, key=lambda release_notes: release_notes[2])
        self.seq = sorted(self.seq, key=lambda release_notes: release_notes[1])
        self.seq = sorted(self.seq, key=lambda release_notes: release_notes[0])
        return self.seq


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
    success = do_example1(p_cls)
    return success


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
    print(releaseit.src_pth)
    print(releaseit.release_notes)
    archiver.print_footer()
    return success


if __name__ == "__main__":
    do_examples()
