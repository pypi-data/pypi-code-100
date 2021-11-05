from pathlib import Path
import pytest
from ghrepo import is_git_repo

THIS_DIR = str(Path(__file__).parent)


@pytest.mark.usefixtures("local_repo")
def test_is_git_repo() -> None:
    assert is_git_repo(THIS_DIR)


def test_is_not_git_repo(tmp_path: Path) -> None:
    assert not is_git_repo(tmp_path)
