"""Unit tests argument parsing utility functions."""
from argparse import ArgumentTypeError

import pytest

from czmodel.util.argument_parsing import dir_path, dir_file


def test_dir_path_raises_error_on_invalid_directory() -> None:
    """Tests argument parsing for paths raises an exception when an invalid directory is passed."""
    # ARRANGE / ACT / ASSERT
    with pytest.raises(ArgumentTypeError):
        dir_path("abc")


def test_dir_file_raises_error_on_invalid_directory() -> None:
    """Tests argument parsing for files raises an exception when an invalid directory is passed."""
    # ARRANGE / ACT / ASSERT
    with pytest.raises(ArgumentTypeError):
        dir_file("abc")
