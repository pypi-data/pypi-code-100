import copy
import logging
import time

import requests

from fedeproxy.common.retry import retry

from ..dvcs.git import Git
from . import forge

logger = logging.getLogger(__name__)


class Gitea(forge.Forge):
    def __init__(self, url):
        super().__init__(url)
        self._s = requests.Session()

    def authenticate(self, **kwargs):
        self._session()
        if "token" in kwargs:
            self.set_token(kwargs["token"])
        else:
            self.login(kwargs["username"], kwargs["password"])
        self._user = self.s.get(f"{self.s.api}/user").json()

    @property
    def is_authenticated(self):
        return hasattr(self, "_user")

    @property
    def username(self):
        return self._user["login"]

    @property
    def is_admin(self):
        return self._user["is_admin"]

    def _session(self):
        self.s.api = f"{self.url}/api/v1"

    def login(self, username, password):
        r = self.s.post(
            f"{self.s.api}/users/{username}/tokens",
            auth=(username, password),
            json={
                "name": f"TEST{time.time()}",
            },
        )
        r.raise_for_status()
        self.set_token(r.json()["sha1"])

    def get_token(self):
        return self.token

    def is_dvcs_supported(self, DVCS):
        return DVCS == Git

    def set_token(self, token):
        self.token = token
        self.s.headers["Authorization"] = f"token {token}"

    def hook_factory(self):
        return forge.Hook

    def users_factory(self):
        return GiteaUsers

    def projects_factory(self):
        return GiteaProjects

    class ForkingInProgress(Exception):
        pass

    @retry(ForkingInProgress, tries=5)
    def _project_wait_fork(self, namespace, project):
        p = self.projects.get(namespace, project)
        if p is None:
            raise Gitea.ForkingInProgress(f"Waiting for {namespace}/{project} fork to finish.")
        return p

    def project_fork(self, namespace, project, target_namespace=None):
        data = {}
        if target_namespace is None:
            target_namespace = self.username
        else:
            data["organization"] = target_namespace
        p = self.projects.get(target_namespace, project)
        if p is not None:
            return p
        r = self.s.post(f"{self.s.api}/repos/{namespace}/{project}/forks", json=data)
        r.raise_for_status()
        return self._project_wait_fork(target_namespace, project)


class GiteaProjects(forge.Projects):
    def project_factory(self):
        return GiteaProject

    def get(self, namespace, project):
        r = self.s.get(f"{self.s.api}/repos/{namespace}/{project}")
        if r.status_code == requests.codes.ok:
            return self.project_factory()(self.forge, r.json())
        else:
            return None

    class DeletionInProgress(Exception):
        pass

    @retry(DeletionInProgress, tries=5)
    def _create(self, namespace, project, **data):
        data.update(
            {
                "name": project,
            }
        )
        r = self.s.post(f"{self.s.api}/user/repos", data=data)
        logger.info(r.text)
        if r.status_code == 201:
            return self.get(namespace, project)
        r.raise_for_status()

    def create(self, namespace, project, **data):
        p = self.get(namespace, project)
        if p is None:
            return self._create(namespace, project, **data)
        else:
            return p

    def delete(self, namespace, project):
        p = self.get(namespace, project)
        if p is None:
            return False
        r = self.s.delete(f"{self.s.api}/repos/{namespace}/{project}")
        r.raise_for_status()
        while self.get(namespace, project) is not None:
            time.sleep(1)
        return True

    def list(self):
        projects = self.s.get(f"{self.s.api}/repos/search")
        projects.raise_for_status()
        raw = projects.json()
        assert raw["ok"]
        for project in raw["data"]:
            yield GiteaProject(self.forge, project)


class GiteaProject(forge.Project):
    @property
    def id(self):
        return self._project["id"]

    @property
    def namespace(self):
        return self._project["owner"]["login"]

    @property
    def project(self):
        return self._project["name"]

    def milestones_factory(self):
        return GiteaMilestones

    def issues_factory(self):
        return GiteaIssues

    @property
    def ssh_url_to_repo(self):
        return self._project["ssh_url"]

    @property
    def http_url_to_repo(self):
        return self._project["clone_url"]

    def hook_register(self, url):
        ...


class GiteaMilestones(forge.Milestones):
    def _build_url(self):
        return f"{self.s.api}/repos/{self.project.namespace}/{self.project.project}/milestones"

    def get(self, id):
        r = self.s.get(f"{self._build_url()}/{id}")
        if r.status_code == requests.codes.ok:
            return GiteaMilestone(self.project, r.json())
        else:
            return None

    def delete(self, id):
        p = self.get(id)
        if p is None:
            return False
        r = self.s.delete(f"{self._build_url()}/{id}")
        r.raise_for_status()
        return True

    def create(self, title, **data):
        data = copy.copy(data)
        data.update({"title": title})
        r = self.s.post(self._build_url(), data=data)
        logger.info(r.text)
        if r.status_code == 201:
            m = r.json()
            return self.get(m["id"])
        r.raise_for_status()

    def list(self):
        r = self.s.get(self._build_url())
        r.raise_for_status()
        for m in r.json():
            yield GiteaMilestone(self.project, m)


class GiteaMilestone(forge.Milestone):
    @property
    def id(self):
        return self._milestone["id"]

    @property
    def title(self):
        return self._milestone["title"]


class GiteaIssues(forge.Issues):
    def _build_url(self):
        return f"{self.s.api}/repos/{self.project.namespace}/{self.project.project}/issues"

    def get(self, id):
        response = self.s.get(f"{self._build_url()}/{int(id)}")  # ensure id is not None
        if response.status_code == 404:
            return None
        else:
            response.raise_for_status()
            return GiteaIssue(self._project, response.json())

    def delete(self, id):
        pass

    def create(self, title, **data):
        data = copy.copy(data)
        data.update({"title": title})
        response = self.s.post(f"{self._build_url()}", data=data)
        logger.info(response.text)
        if response.status_code == 201:
            issue = response.json()
            return self.get(issue["number"])
        response.raise_for_status()

    def list(self):
        response = self.s.get(f"{self._build_url()}")
        response.raise_for_status()
        for issue in response.json():
            yield GiteaIssue(self._project, issue)


class GiteaIssue(forge.Issue):
    @property
    def id(self):
        return self._issue["number"]

    def to_json(self):
        i = self._issue
        j = {
            "url": i["html_url"],
            "title": i["title"],
            "description": i["body"],
            "repository": f"{self.s.api}/repos/{i['repository']['full_name']}",
            "user": f"{self.s.api}/users/{i['user']['username']}",
            "created_at": i["created_at"],
            "state": i["state"] == "closed" and "closed" or "open",
            "comments": [],
            "id": str(i["number"]),
        }
        if i["closed_at"] is not None:
            j["closed_at"] = i["closed_at"]
        return j

    def from_json(self, j):
        self._issue["title"] = j["title"]
        self._issue["body"] = j["description"]
        self._issue["state"] = j["state"]
        url = f"{self.s.api}/repos/{self._issue['repository']['full_name']}/issues/{self._issue['number']}"
        response = self.s.patch(f"{url}", json=self._issue)
        logger.info(response.text)
        if response.status_code == 201:
            self._issue = response.json()
            return
        response.raise_for_status()


class GiteaUsers(forge.Users):
    def get(self, username):
        if username == self.forge.username:
            r = self.s.get(f"{self.s.api}/user")
        elif self.forge.is_admin:
            r = self.s.get(f"{self.s.api}/user", params={"sudo": username})
        else:
            r = self.s.get(f"{self.s.api}/users/{username}")
        if r.status_code == 404:
            return None
        else:
            r.raise_for_status()
            return GiteaUser(self.forge, r.json())

    def delete(self, username):
        user = self.get(username)
        if user is None:
            return False
        while True:
            r = self.s.delete(f"{self.s.api}/admin/users/{username}")
            if r.status_code == 404:
                break
            logger.debug(r.text)
            r.raise_for_status()
        return True

    def create(self, username, password, email, **data):
        # the API does not support creating an admin user
        assert data.get("admin") is not True, "Creating an admin user with Gitea is not implemented"
        info = self.get(username)
        if info is None:
            r = self.s.post(
                f"{self.s.api}/admin/users",
                data={
                    "username": username,
                    "email": email,
                    "password": password,
                },
            )
            logger.debug(r.text)
            r.raise_for_status()
            info = r.json()
            Gitea(self.forge.url).users._finalize_user_create(username, password)
            info = self.get(username)
        return info

    def _finalize_user_create(self, username, password):
        r = self.s.post(
            f"{self.forge.url}/user/login",
            data={
                "user_name": username,
                "password": password,
            },
        )
        r.raise_for_status()
        r = self.s.post(
            f"{self.forge.url}/user/settings/change_password",
            data={
                "password": password,
                "retype": password,
                "_csrf": self.s.cookies["_csrf"],
            },
        )
        r.raise_for_status()

    def list(self):
        r = self.s.get(f"{self.s.api}/users/search")
        r.raise_for_status()
        j = r.json()
        assert j["ok"]
        for u in j["data"]:
            yield GiteaUser(self.forge, u)


class GiteaUser(forge.User):
    @property
    def url(self):
        return f"{self.forge.url}/{self.username}"

    @property
    def username(self):
        return self._user["username"]

    @property
    def emails(self):
        return [self._user["email"]]

    @property
    def projects(self):
        params = {"uid": self._user["id"]}
        projects = self.s.get(f"{self.s.api}/repos/search", params=params)
        projects.raise_for_status()
        raw = projects.json()
        assert raw["ok"]
        for project in raw["data"]:
            yield GiteaProject(self.forge, project)

    def to_json(self):
        return {
            "url": self.url,
            "username": self.username,
        }

    def from_json(self, j):
        pass
