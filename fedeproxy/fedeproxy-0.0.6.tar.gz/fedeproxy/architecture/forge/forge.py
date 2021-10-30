import abc
import os

from furl import furl

from ...format import format
from ...interfaces import forge
from ..dvcs import git


class Persistent(forge.Persistent):
    @abc.abstractmethod
    def create_from_json(self, j):
        ...

    @abc.abstractmethod
    def list(self):
        ...


class Forge(forge.Forge):
    def save(self, pathname):
        return self.users.save(f"{pathname}/users.json")

    def load(self, pathname):
        return self.users.load(f"{pathname}/users.json")

    def hook_register(self, url):
        r = []
        for p in self.projects.list():
            r.append(p.hook_register(f"{url}/hook/project/{p.namespace}/{p.project}"))
        return r


class Hook(forge.Hook):
    pass


class HookCommit(forge.HookCommit):
    pass


class Projects(forge.Projects):
    pass


class Project(forge.Project):
    def to_json(self):
        return {
            "namespace": self.namespace,
            "project": self.project,
        }

    def save(self, pathname):
        format.FormatProject().save(f"{pathname}/project.json", self.to_json())
        return self.issues.save(f"{pathname}/issues.json")

    def load(self, pathname):
        project = format.FormatProject().load(f"{pathname}/project.json")
        assert project == self.to_json()
        return self.issues.load(f"{pathname}/issues.json")

    def dvcs_factory(self):
        return git.Git

    def dvcs(self, directory):
        o = furl(self.http_url_to_repo)
        o.username = "oauth2"
        o.password = self.forge.get_token()
        return self.dvcs_factory()(directory, o.tostr())


class Milestones(forge.Milestones, Persistent):
    @property
    def format(self):
        ...

    def load(self, filename):
        ...

    def save(self, filename):
        ...

    def create_from_json(self, j):
        ...


class Milestone(forge.Milestone):
    pass


class Issues(forge.Issues, Persistent):
    def load(self, filename):
        return format.FormatIssues().load(filename, self.create_from_json)

    def save(self, filename):
        return format.FormatIssues().save(filename, self.list())

    def create_from_json(self, j):
        i = self.get(j["id"])
        if i is None:
            i = self.create(j["title"])
        i.from_json(j)
        return i


class Issue(forge.Issue):
    pass


class Users(forge.Users, Persistent):
    def load(self, filename):
        return format.FormatUsers().load(filename, self.create_from_json)

    def save(self, filename):
        return format.FormatUsers().save(filename, self.list())

    def create_from_json(self, j):
        i = self.get(j["username"])
        if i is None:
            i = self.create(j["username"], "no password", "foo@example.com")
        i.from_json(j)
        return i

    def convert_url_to_username(self, url):
        return os.path.basename(url)


class User(forge.User):
    pass
