import pytest

from . import format


@pytest.fixture
def project():
    return {
        "namespace": "NAMESPACE",
        "project": "PROJECT",
    }


def test_format_project(project, tmpdir):
    f = format.FormatProject()
    assert f.schema.validate().valid
    p = f"{tmpdir}/project.json"
    f.save(p, project)
    assert f.load(p) == project
    assert f.validate(project)


@pytest.fixture
def issue():
    return {
        "url": "http://example.com/issue",
        "title": "title",
        "description": "description",
        "repository": "http://example.com/repository",
        "user": "http://example.com/issue-user",
        "created_at": "2016-01-04T15:31:51.081Z",
        "closed_at": "2021-01-02 10:30:50",
        "state": "closed",
        "comments": [
            {
                "url": "http://example.com/comment1",
                "body": "body1",
                "user": "http://example.com/comment-user1",
                "created_at": "2021-01-01 10:30:50",
                "id": "comment1",
            },
            {
                "url": "http://example.com/comment2",
                "body": "body2",
                "user": "http://example.com/comment-user2",
                "created_at": "2021-01-01 10:30:50",
                "id": "comment2",
            },
        ],
        "id": "issue1234",
    }


def test_format_issue(issue, tmpdir):
    f = format.FormatIssue()
    assert f.schema.validate().valid
    p = f"{tmpdir}/issue.json"
    f.save(p, issue)
    assert f.load(p) == issue
    assert f.validate(issue)


@pytest.fixture
def identities():
    return [
        {
            "url": "http://example.com/user",
            "public": "PUBLIC-KEY",
            "private": "PRIVATE-KEY",
            "owned": False,
            "token": "TOKEN",
            "emails": ["some@example.com", "other@example.com"],
        },
        {
            "url": "http://example.com/user",
            "public": "PUBLIC-KEY",
            "private": None,
            "owned": False,
            "token": None,
            "emails": ["some@example.com", "other@example.com"],
        },
    ]


def test_format_identities(identities, tmpdir):
    f = format.FormatIdentities()
    assert f.schema.validate().valid
    p = f"{tmpdir}/identities.json"
    f.save(p, identities)
    assert f.load(p) == identities
    assert f.validate(identities)


@pytest.fixture
def user():
    return {
        "url": "http://example.com/user",
        "username": "USERNAME",
    }


def test_format_user(user, tmpdir):
    f = format.FormatUser()
    assert f.schema.validate().valid
    p = f"{tmpdir}/user.json"
    f.save(p, user)
    assert f.load(p) == user
    assert f.validate(user)


@pytest.fixture
def federation():
    return [
        {"url": "URL1"},
        {"url": "URL2"},
    ]


def test_format_federation(federation, tmpdir):
    f = format.FormatFederation()
    assert f.schema.validate().valid
    p = f"{tmpdir}/federation.json"
    f.save(p, federation)
    assert f.load(p) == federation
    assert f.validate(federation)
