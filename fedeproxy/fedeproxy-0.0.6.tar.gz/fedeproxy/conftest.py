import time

import pytest
import sh

from .architecture.dvcs.git import Git
from .architecture.dvcs.hg import Hg
from .architecture.forge.test_gitea import params as params_gitea
from .architecture.forge.test_gitlab import params as params_gitlab
from .domain.fedeproxy import Fedeproxy

forge_params = [
    params_gitea,
    params_gitlab,
]
forge_ids = [p["name"] for p in forge_params]


def skip_excluded_forges(request):
    marker = request.node.get_closest_marker("forges")
    if marker is not None:
        forges = marker.args[0]
        if request.param["name"] not in forges:
            pytest.skip(f"the test has a 'mark' excluding {request.param['name']} ")


@pytest.fixture
def fedeproxy(forge_factory, tmpdir, make_identity, testuser, password, testproject, make_project):
    (Forge, url) = (forge_factory["class"], forge_factory["url"])
    f = Fedeproxy(Forge, url, f"{tmpdir}/fedeproxy")

    make_identity(f, f.owner)
    f.load()
    make_project(f.own, f.namespace, "fedeproxy")

    make_identity(f, testuser)
    f.forge.authenticate(username=testuser, password=password)
    make_project(f.forge, testuser, testproject)

    return f


@pytest.fixture
def forge(forge_factory):
    (Forge, url) = (forge_factory["class"], forge_factory["url"])
    return Forge(url)


@pytest.fixture(params=forge_params, ids=forge_ids)
def forge_factory(request):
    skip_excluded_forges(request)
    return request.param


@pytest.fixture
def password():
    return "Wrobyak4"


@pytest.fixture
def testuser():
    return "testuser1"


@pytest.fixture
def testproject():
    return "testproject"


@pytest.fixture
def make_user(password):

    contexts = []

    def _make_user(forge, username):
        forge.authenticate(username="root", password="Wrobyak4")
        user = forge.users.get(username)
        if user:
            for project in user.projects:
                forge.projects.delete(username, project.project)

            forge.users.delete(username)
        email = f"{username}@example.com"
        user = forge.users.create(username, password, email)
        contexts.append((forge, username))
        return user

    yield _make_user

    for (forge, username) in contexts:
        if not forge.is_authenticated or not forge.is_admin:
            forge.authenticate(username="root", password="Wrobyak4")
        user = forge.users.get(username)
        if user:
            for project in user.projects:
                forge.projects.delete(username, project.project)
        forge.users.delete(username)


@pytest.fixture
def make_identity(make_user, password):
    def _make_identity(fedeproxy, username):
        user = make_user(fedeproxy.own, username)
        return fedeproxy.identity_create(user, password)

    yield _make_identity


@pytest.fixture
def make_project(password):

    contexts = []

    def _make_project(forge, username, project, **data):
        forge.projects.delete(username, project)
        p = forge.projects.create(username, project, **data)
        contexts.append((forge, username, project))
        return p

    yield _make_project

    for (forge, username, project) in contexts:
        forge.authenticate(username="root", password=password)
        forge.projects.delete(username, project)


class Repository(object):
    def __init__(self, d):
        self.d = d

    def populate(self):
        open(f"{self.d}/README.md", "w").write("# testrepo ")
        open(f"{self.d}/info.txt", "w").write("# someinfo")
        open(f"{self.d}/time.txt", "w").write(f"time {time.time()}")
        return self


class RepositoryGit(Repository):
    def commit(self):
        sh.git("-C", self.d, "add", "README.md", "info.txt", "time.txt")
        sh.git("-C", self.d, "commit", "-m", "initial")
        return self

    def prepare_for_test(self):
        sh.git.init(self.d)
        self.populate()
        self.commit()
        sh.git("-C", self.d, "checkout", "-b", "otherbranch")


class RepositoryHg(Repository):
    def commit(self):
        sh.hg("--cwd", self.d, "add", "README.md", "info.txt", "time.txt")
        sh.hg("--cwd", self.d, "commit", "-m", "initial")
        return self

    def prepare_for_test(self):
        sh.hg.init(self.d)
        open(f"{self.d}/.hgkeep", "w").write("# init")
        sh.hg("--cwd", self.d, "add", ".hgkeep")
        sh.hg("--cwd", self.d, "commit", "-m", "initial")

        sh.hg("--cwd", self.d, "branch", "master")
        self.populate()
        self.commit()

        sh.hg("--cwd", self.d, "branch", "otherbranch")


@pytest.fixture(
    params=[
        (Git, RepositoryGit),
        (Hg, RepositoryHg),
    ],
    ids=[
        "git",
        "hg",
    ],
)
def dvcs_factory(request):
    return request.param
