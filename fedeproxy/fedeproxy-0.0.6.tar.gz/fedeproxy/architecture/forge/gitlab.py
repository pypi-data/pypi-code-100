import copy
import logging
import time

import gitlab
import requests

from fedeproxy.common.retry import retry

from ..dvcs.git import Git
from ..dvcs.hg import Hg
from . import forge

logger = logging.getLogger(__name__)


class GitLab(forge.Forge):
    def __init__(self, url):
        super().__init__(url)

    def authenticate(self, **kwargs):
        if "token" in kwargs:
            self.set_token(kwargs["token"])
        else:
            self.login(kwargs["username"], kwargs["password"])
        self._s = gitlab.Gitlab(url=self.url, oauth_token=self.token)
        self.s.auth()

    @property
    def is_authenticated(self):
        return hasattr(self, "_s")

    @property
    def username(self):
        return self.s.user.username

    @property
    def is_admin(self):
        if hasattr(self.s.user, "is_admin"):
            return self.s.user.is_admin
        else:
            return False

    def login(self, username, password):
        r = requests.post(
            self.url + "/oauth/token",
            json={
                "username": username,
                "password": password,
                "grant_type": "password",
            },
        )
        logger.debug(r.text)
        r.raise_for_status()
        self.set_token(r.json()["access_token"])

    def get_token(self):
        return self.token

    def is_dvcs_supported(self, DVCS):
        """Read access to GitLab application settings requires an admin account"""
        if not self.is_authenticated:
            raise Exception("Authentication required")

        dvcs_to_id = {"git": Git, "hg": Hg, "hg_git": Hg}
        return DVCS in set(dvcs_to_id[x] for x in self._s.settings.get().vcs_types)

    def set_token(self, token):
        self.token = token

    def get_namespace_id(self, name):
        r = self.s.namespaces.list(search=name)
        return r[0].id

    def hook_factory(self):
        def factory(payload):
            if payload["object_kind"] == "push":
                return GitLabHookCommit(payload)
            else:
                return forge.Hook(payload)

        return factory

    def users_factory(self):
        return GitLabUsers

    def projects_factory(self):
        return GitLabProjects


class GitLabHookCommit(forge.HookCommit):
    @property
    def hash(self):
        return self.payload["checkout_sha"]


class GitLabProjects(forge.Projects):
    def project_factory(self):
        return GitLabProject

    def get(self, namespace, project):
        try:
            p = self.s.projects.get(f"{namespace}/{project}")
            return self.project_factory()(self.forge, p)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                return None
            raise

    class DeletionInProgress(Exception):
        pass

    @retry(DeletionInProgress, tries=5)
    def _create(self, namespace, project, **data):
        namespace_id = self.forge.get_namespace_id(namespace)
        data.update(
            {
                "name": project,
                "namespace_id": int(namespace_id),
                "visibility": "public",
                "initialize_with_readme": True,
                "default_branch": "main",
            }
        )
        try:
            self.s.projects.create(data)
        except gitlab.exceptions.GitlabCreateError as e:
            if e.response_code == 400 and (
                "still being deleted" in e.response_body.decode()
                or "has already been taken" in e.response_body.decode()
            ):
                raise GitLabProjects.DeletionInProgress()
            raise
        return self.get(namespace, project)

    def create(self, namespace, project, vcs=None):
        """vcs parameter allowed values:
        * 'git',
        * 'hg_git' (partial native mode of HGitaly1),
        * 'hg' (fully native Mercurial, not enabled by default within Heptapod)."""
        info = self.get(namespace, project)
        if info is None:
            data = {}
            if vcs:
                data["vcs_type"] = vcs
            return self._create(namespace, project, **data)
        else:
            return info

    def delete(self, namespace, project):
        p = self.get(namespace, project)
        if p is None:
            return False
        self.s.projects.delete(f"{namespace}/{project}")
        while self.get(namespace, project) is not None:
            time.sleep(1)
        return True

    def list(self):
        for p in self.s.projects.list(visibility="public"):
            yield GitLabProject(self.forge, p)


class GitLabProject(forge.Project):
    @property
    def id(self):
        return self._project.id

    @property
    def namespace(self):
        return self._project.namespace["path"]

    @property
    def project(self):
        return self._project.path

    def milestones_factory(self):
        return GitLabMilestones

    def issues_factory(self):
        return GitLabIssues

    @property
    def ssh_url_to_repo(self):
        return self._project.ssh_url_to_repo

    def dvcs_factory(self):
        return Git if self._project.vcs_type == "git" else Hg

    @property
    def http_url_to_repo(self):
        return self._project.http_url_to_repo

    def hook_register(self, url):
        for hook in self._project.hooks.list():
            if hook.url == url:
                return False
        self._project.hooks.create({"url": url, "issues_events": 1, "push_events": 1})
        return True


class GitLabMilestones(forge.Milestones):
    def get(self, id):
        try:
            milestone = self._project._project.milestones.get(id)
            return GitLabMilestone(self.project, milestone)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                return None
            else:
                raise

    def delete(self, id):
        try:
            self._project._project.milestones.delete(id)
        except gitlab.exceptions.GitlabDeleteError as e:
            if e.response_code == 404:
                return False
            else:
                raise
        return True

    def create(self, title, **data):
        milestone = self._project._project.milestones.create({"title": title})
        return GitLabMilestone(self.project, milestone)

    def list(self):
        for milestone in self._project._project.milestones.list():
            yield GitLabMilestone(self.project, milestone)


class GitLabMilestone(forge.Milestone):
    @property
    def id(self):
        return self._milestone.id

    @property
    def title(self):
        return self._milestone.title


class GitLabIssues(forge.Issues):
    def get(self, id):
        try:
            i = self.project._project.issues.get(id)
            return GitLabIssue(self.project, i)
        except gitlab.exceptions.GitlabGetError as e:
            if e.response_code == 404:
                return None
            raise

    def delete(self, id):
        info = self.get(id)
        if info is None:
            return False
        self.project._project.issues.delete(id)
        return True

    def create(self, title, **data):
        data = copy.copy(data)
        data.update({"title": title})
        i = self.project._project.issues.create(data)
        return self.get(i.iid)

    def list(self):
        for i in self.project._project.issues.list(scope="all"):
            yield GitLabIssue(self.project, i)


class GitLabIssue(forge.Issue):
    @property
    def id(self):
        return self._issue.iid

    def to_json(self):
        i = self._issue
        j = {
            "url": i.web_url,
            "title": i.title,
            "description": i.description or "",
            "repository": self.project.http_url_to_repo,
            "user": i.author["web_url"],
            "created_at": i.created_at,
            "state": i.state == "closed" and "closed" or "open",
            "comments": [],
            "id": str(i.iid),
        }
        if i.closed_at is not None:
            j["closed_at"] = i.closed_at
        return j

    def from_json(self, j):
        self._issue.title = j["title"]
        self._issue.description = j["description"]
        if self._issue.state != j["state"]:
            if j["state"] == "closed":
                self._issue.state_event = "close"
            elif j["state"] == "open":
                self._issue.state_event = "reopen"
            else:
                raise ValueError(f"Unsupported value: {j['state']=}")
        self._issue.save()


class GitLabUsers(forge.Users):
    def get(self, username):
        if username == self.forge.username:
            return GitLabUser(self.forge, self.s.user)

        for found in self.s.users.list(username=username):
            #
            # There may be more than one match because the search is case insensitive
            #
            if found.username == username:
                return GitLabUser(self.forge, found)
        return None

    def delete(self, username):
        user = self.get(username)
        if user is None:
            return False
        while True:
            try:
                self.s.users.delete(user.id)
            except gitlab.exceptions.GitlabDeleteError as e:
                if e.response_code == 404:
                    break
                raise
            time.sleep(0.1)
        return True

    def create(self, username, password, email, **data):
        info = self.get(username)
        if info is None:
            self.s.users.create(
                {
                    "name": username,
                    "username": username,
                    "email": email,
                    "password": password,
                    "skip_confirmation": True,
                    "admin": data.get("admin", False),
                }
            )
            info = self.get(username)
        return info

    def list(self):
        for u in self.s.users.list():
            yield GitLabUser(self.forge, u)


class GitLabUser(forge.User):
    @property
    def url(self):
        return self._user.web_url

    @property
    def username(self):
        return self._user.username

    @property
    def emails(self):
        if hasattr(self._user, "email"):
            return [self._user.email]
        elif hasattr(self._user, "public_email"):
            return [self._user.public_email]
        else:
            return []

    @property
    def projects(self):
        for project in self._user.projects.list(visibility="public"):
            yield GitLabProject(self.forge, project)

    @property
    def id(self):
        return self._user.id

    def to_json(self):
        return {
            "url": self.url,
            "username": self.username,
        }

    def from_json(self, j):
        pass
