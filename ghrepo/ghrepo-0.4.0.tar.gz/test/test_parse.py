from typing import List
import pytest
from ghrepo import GHRepo

REPO_URLS = [
    (
        "git://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git://github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git@github.com:jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git@github.com:jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "ssh://git@github.com:jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "ssh://git@github.com:jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://api.github.com/repos/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/headerparser/",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/none.git",
        GHRepo("jwodder", "none"),
    ),
    (
        "https://x-access-token:1234567890@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    (
        "https://my.username@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
]

BAD_REPOS = [
    "https://github.com/none/headerparser.git",
    "/repo",
    "none/repo",
    "jwodder/headerparser.git",
    "jwodder/",
    "https://api.github.com/repos/jwodder/headerparser.git",
    "https://api.github.com/repos/jwodder/headerparser.git/",
    "https://api.github.com/repos/jwodder/headerparser/",
]


@pytest.mark.parametrize(
    "spec,repo",
    REPO_URLS
    + [
        ("jwodder/headerparser", GHRepo("jwodder", "headerparser")),
        ("headerparser", GHRepo("jwodder", "headerparser")),
        ("jwodder/none", GHRepo("jwodder", "none")),
        ("none", GHRepo("jwodder", "none")),
        ("nonely/headerparser", GHRepo("nonely", "headerparser")),
        ("none-none/headerparser", GHRepo("none-none", "headerparser")),
        ("nonenone/headerparser", GHRepo("nonenone", "headerparser")),
    ],
)
def test_parse(spec: str, repo: GHRepo) -> None:
    assert GHRepo.parse(spec, default_owner="jwodder") == repo


@pytest.mark.parametrize("spec", BAD_REPOS)
def test_parse_bad_spec(spec: str) -> None:
    with pytest.raises(ValueError):
        GHRepo.parse(spec)


@pytest.mark.parametrize("url,repo", REPO_URLS)
def test_parse_url(url: str, repo: GHRepo) -> None:
    assert GHRepo.parse_url(url) == repo


@pytest.mark.parametrize("url", BAD_REPOS)
def test_parse_bad_url(url: str) -> None:
    with pytest.raises(ValueError):
        GHRepo.parse_url(url)


def test_parse_name_only_no_owner() -> None:
    with pytest.raises(ValueError):
        GHRepo.parse("headerparser")


def test_parse_owner_name_no_default_owner() -> None:
    assert GHRepo.parse("jwodder/headerparser") == GHRepo("jwodder", "headerparser")


def test_parse_name_only_callable_owner() -> None:
    assert GHRepo.parse("headerparser", lambda: "jwodder") == GHRepo(
        "jwodder", "headerparser"
    )


def test_parse_owner_name_callable_default_owner() -> None:
    calls: List[int] = []

    def defowner() -> str:
        calls.append(1)
        return "jwodder"

    assert GHRepo.parse("octocat/Hello-World") == GHRepo("octocat", "Hello-World")
    assert calls == []
