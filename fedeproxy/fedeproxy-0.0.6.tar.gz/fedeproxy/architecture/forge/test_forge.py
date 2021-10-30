import os

import pytest
import requests

from ...interfaces import forge as forge_interface

#
# forge.Forge
#


def test_authenticate(forge):
    (Forge, url) = (type(forge), forge.url)
    forgeA = Forge(url)
    forgeA.authenticate(username="root", password="Wrobyak4")
    assert forgeA.users.get("root") is not None
    forgeB = Forge(url)
    forgeB.authenticate(token=forgeA.get_token())
    assert forgeB.users.get("root") is not None


@pytest.mark.forges(["Gitea"])
def test_gitea_is_dvcs_supported_true(forge):
    from ..dvcs.git import Git

    assert forge.is_dvcs_supported(Git) is True


@pytest.mark.forges(["GitLab"])
def test_gitlab_is_dvcs_supported_true(forge):
    from ..dvcs.git import Git
    from ..dvcs.hg import Hg

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.is_dvcs_supported(Git) is True
    assert forge.is_dvcs_supported(Hg) is True


@pytest.mark.forges(["Gitea"])
def test_gitea_is_dvcs_supported_false(forge):
    assert forge.is_dvcs_supported("unknown") is False


@pytest.mark.forges(["GitLab"])
def test_gitlab_is_dvcs_supported_false(forge):
    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.is_dvcs_supported("unknown") is False


@pytest.mark.forges(["GitLab"])
def test_gitlab_is_dvcs_supported_unauthenticated(forge):
    with pytest.raises(Exception):
        forge.is_dvcs_supported("unknown")


@pytest.mark.forges(["GitLab"])
def test_forge_hook_register(tmpdir, forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")
    url = "http://example.com"
    assert forge.hook_register(url) == [True]
    assert forge.hook_register(url) == [False]
    assert p.hook_register(f"{url}/hook/project/{username}/testproject") is False


#
# forge.Projects & forge.Project
#


def test_project_create(forge, make_user, password):
    username = "testuser1"
    make_user(forge, username)
    forge.authenticate(username=username, password=password)

    forge.projects.delete(username, "testproject")
    assert forge.projects.get(username, "testproject") is None
    p = forge.projects.create(username, "testproject")
    assert p.project == "testproject"
    assert p.id == forge.projects.create(username, "testproject").id
    forges = list(forge.projects.list())
    assert forges and len(forges) == 1 and forges[0] == p
    assert forge.projects.delete(username, "testproject") is True
    assert forge.projects.delete(username, "testproject") is False
    forges = list(forge.projects.list())
    assert not forges and len(forges) == 0


def test_project_save(tmpdir, forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")
    p.issues.create("ISSUE ONE")
    p.issues.create("ISSUE TWO")
    p.save(tmpdir)
    assert p.load(tmpdir) == 2
    assert os.path.exists(f"{tmpdir}/project.json")


def test_project_dvcs(request, tmpdir, forge, make_user, password, make_project, dvcs_factory):
    from ..dvcs.git import Git
    from ..dvcs.hg import Hg

    forge.authenticate(username="root", password="Wrobyak4")
    if not forge.is_dvcs_supported(dvcs_factory[0]):
        pytest.skip(f"{dvcs_factory[0].__name__} is not supported by {type(forge).__name__}")

    username = "testuser1"
    make_user(forge, username)

    params = {}
    # Gitea handles only Git
    if request.getfixturevalue("forge").__module__.endswith("gitlab"):
        gitlab_vcs_ids = {Git: "git", Hg: "hg_git"}
        params["vcs"] = gitlab_vcs_ids[dvcs_factory[0]]

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject", **params)

    directory = f"{tmpdir}/somewhere"
    d = p.dvcs(directory)
    assert not os.path.exists(d.directory)
    assert d.clone("master") is True
    assert os.path.exists(d.directory)


@pytest.mark.forges(["GitLab"])
def test_project_hook_register(tmpdir, forge, make_user, password, make_project):
    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")
    url = "http://example.com"
    assert p.hook_register(url) is True
    assert p.hook_register(url) is False


#
# forge.Users & forge.User
#


def test_users_save(tmpdir, forge, make_user):
    username = "testuser1"
    make_user(forge, username)

    assert forge.save(tmpdir) == len(list(forge.users.list()))
    assert forge.load(tmpdir) == len(list(forge.users.list()))


def test_user_create_regular(forge):
    forge.authenticate(username="root", password="Wrobyak4")
    username = "testuser1"
    email = "testuser1@example.com"
    password = "Wrobyak4"
    forge.users.delete(username)

    u = forge.users.create(username, password, email)
    assert u.url == forge.users.create(username, password, email).url
    assert any([x.username == username for x in forge.users.list()])
    forge.authenticate(username=username, password=password)
    assert forge.username == username
    assert forge.is_admin is False

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.users.delete(username) is True
    assert forge.users.get(username) is None
    assert forge.users.delete(username) is False


@pytest.mark.forges(["GitLab"])
def test_user_create_admin(forge):
    forge.authenticate(username="root", password="Wrobyak4")
    username = "testuser1"
    email = "testuser1@example.com"
    password = "Wrobyak4"
    forge.users.delete(username)

    forge.users.create(username, password, email, admin=True)
    forge.authenticate(username=username, password=password)
    assert forge.is_admin is True

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.users.delete(username) is True


def test_user_get(forge):
    forge.authenticate(username="root", password="Wrobyak4")

    password = "Wrobyak4"

    username1 = "testuser1"
    email1 = "testuser1@example.com"
    forge.users.delete(username1)
    u1 = forge.users.create(username1, password, email1)

    username2 = "testuser2"
    email2 = "testuser2@example.com"
    forge.users.delete(username2)
    u2 = forge.users.create(username2, password, email2)

    assert u1 != u2

    #
    # As an admin, the email of all users is exposed
    #
    u1_view_admin = forge.users.get(username1)
    assert u1_view_admin.emails == [email1]

    #
    # When authenticated as a user, its email is exposed
    #
    forge.authenticate(username=username1, password=password)
    u1_view_self = forge.users.get(username1)
    assert u1_view_self.emails == [email1]

    #
    # When authenticated as an unprivileged user, its email is unknown
    # and is either not returned at all or replaced by a placeholder
    # that is different from the real email
    #
    forge.authenticate(username=username2, password=password)
    u1_view_unpriv = forge.users.get(username1)
    assert u1_view_unpriv.emails == [] or u1_view_unpriv.emails[0] != email1
    assert u1_view_admin == u1_view_self == u1_view_unpriv

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.users.delete(username1) is True
    assert forge.users.delete(username2) is True


def test_user_url(forge):
    forge.authenticate(username="root", password="Wrobyak4")
    username = "testuser1"
    email = "testuser1@example.com"
    password = "Wrobyak4"
    forge.users.delete(username)
    u = forge.users.create(username, password, email)
    assert u.username == username
    r = requests.get(u.url)
    r.raise_for_status()


def test_user_projects(forge, make_user, password):
    username = "testuser1"
    user1 = make_user(forge, username)
    forge.authenticate(username=username, password=password)

    forges = list(user1.projects)
    assert not forges and len(forges) == 0

    p = forge.projects.create(username, "testproject")
    forges = list(user1.projects)
    assert forges and len(forges) == 1 and forges[0] == p

    assert forge.projects.delete(username, "testproject") is True
    forges = list(user1.projects)
    assert not forges and len(forges) == 0


#
# forge.Milestones & forge.Milestone
#


def test_milestone_create(forge, make_user, password, make_project):
    from ...interfaces.forge import Milestone

    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    milestones = list(p.milestones.list())
    assert not milestones and len(milestones) == 0

    title = "THE TITLE"
    i = p.milestones.create(title)
    assert i.title == title
    assert i.id == p.milestones.get(i.id).id
    assert i == p.milestones.get(i.id)
    milestones = list(p.milestones.list())
    assert milestones and len(milestones) == 1 and milestones[0].id == i.id
    assert milestones[0] == i
    assert isinstance(milestones[0], Milestone)
    assert p.milestones.delete(i.id) is True
    assert not list(p.milestones.list())
    assert p.milestones.get(i.id) is None
    assert p.milestones.delete(i.id) is False


#
# forge.Issues & forge.Issue
#


def test_issue_create(request, forge, make_user, password, make_project):
    from ...interfaces.forge import Issue, Project

    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    title = "THE TITLE"
    i = p.issues.create(title)
    assert i.id == p.issues.get(i.id).id
    assert isinstance(i, Issue)
    assert isinstance(i.project, Project)
    for x in p.issues.list():
        assert isinstance(x, Issue)
        assert isinstance(x.project, Project)
        assert x.id == i.id

    # Gitea doesn't implement delete (https://github.com/go-gitea/gitea/issues/923)
    if not request.getfixturevalue("forge").__module__.endswith("gitea"):
        assert p.issues.delete(i.id) is True
        assert p.issues.get(i.id) is None
        assert p.issues.delete(i.id) is False
    else:
        assert p.issues.get(i.id + 1) is None


def test_issue_save(tmpdir, forge, make_user, password, make_project):
    from ...interfaces.forge import Issue, Project

    username = "testuser1"
    make_user(forge, username)

    forge.authenticate(username=username, password=password)
    p = make_project(forge, username, "testproject")

    title = "THE TITLE"
    i = p.issues.create(title)
    assert isinstance(i, Issue)
    assert isinstance(i.project, Project)

    # Get an existent issue from a JSON export (an issue isn't created)
    save_path = f"{tmpdir}/issue.json"
    p.issues.save(save_path)
    assert p.issues.load(save_path) == 1
    imported = p.issues.create_from_json(i.to_json())
    assert isinstance(imported, Issue)
    assert isinstance(imported.project, Project)
    assert imported.id == i.id
    assert imported.to_json() == i.to_json()

    # Create a new issue from a JSON export
    exported = i.to_json()
    new_issue = {
        "title": "another title",
        "description": "blah",
        "state": "closed",
        "user": exported["user"],
        "repository": exported["repository"],
        # "url": ...,
        # "created_at": exported["created_at"],
        # "closed_at": exported["closed_at"]
        "id": "-1",  # a non existent id
    }

    assert p.issues.get(new_issue["id"]) is None
    another = p.issues.create_from_json(new_issue)
    assert isinstance(another, Issue)
    assert isinstance(another.project, Project)
    another_issue_exported = another.to_json()
    for k, v in new_issue.items():
        assert k == "id" or another_issue_exported[k] == v, k


#
# forge.Hook
#


@pytest.mark.forges(["GitLab"])
def test_hook(forge_factory):
    (Forge, url) = (forge_factory["class"], forge_factory["url"])
    forge = Forge(url)

    issue_create = forge_factory["hooks"]["issue_create"]
    h = forge.hook_factory()(issue_create("NAME", "NAMESPACE", "ID", "TITLE"))
    assert isinstance(h, forge_interface.HookCommit) is False

    push = forge_factory["hooks"]["push"]
    hash = "HASH"
    h = forge.hook_factory()(push("NAME", "NAMESPACE", hash))
    assert isinstance(h, forge_interface.HookCommit) is True
    print(h.payload)
    assert h.hash == hash
