import dataclasses
import os
from typing import List

from ..format import format
from ..interfaces import forge as forge_interface
from .identity import IdentitiesPrivate, IdentityPrivate


class Fedeproxy(object):
    def __init__(self, forge_factory, url, base_directory):
        self._forge_factory = forge_factory
        self._url = url
        self._base_directory = base_directory
        self._namespace = "fedeproxy"
        self._owner = "fedeproxy"
        self.own_forge_create()
        self.forge_create()
        self.identities = IdentitiesPrivate(self.base_directory)
        self.federation = FedeproxyFederation(self.base_directory)

    def load(self):
        self.identities.load()
        self.federation.load()
        for i in self.identities.identities:
            self.own.authenticate(token=i.token)
            if self.own.username == self.owner:
                return self.own.username
        return None

    def identity_create(self, user, password):
        self.forge.authenticate(username=user.username, password=password)
        i = IdentityPrivate(url=user.url, token=self.forge.get_token())
        i.create_key()
        self.identities.identities.append(i)
        self.identities.save()
        return i

    @property
    def url(self):
        return self._url

    @property
    def base_directory(self):
        return self._base_directory

    @property
    def forge_factory(self):
        return self._forge_factory

    @property
    def own(self):
        return self._own

    @property
    def owner(self):
        return self._owner

    @property
    def namespace(self):
        return self._namespace

    def own_forge_create(self):
        self._own = self.forge_factory(self.url)

    @property
    def forge(self):
        return self._forge

    def forge_create(self):
        self._forge = self.forge_factory(self.url)

    def project_export(self, namespace, project):
        p = self.forge.projects.create(namespace, project)
        directory = f"{self.base_directory}/{namespace}/fedeproxy"
        d = self.forge.projects.create(namespace, "fedeproxy").dvcs(directory)
        branch = d.url_hashed(p.http_url_to_repo)
        d.clone(branch)
        p.save(d.directory)
        d.commit("exported project")
        d.push(branch)
        return d

    def save(self):
        self.identities.save()
        self.own.save(self.base_directory)
        return self.base_directory

    def modified(self, **kwargs):
        pass  # push to established cnx with other fedeproxy instances

    def hook_receive(self, payload, **kwargs):
        hook = self.own.hook_factory()(payload)
        if isinstance(hook, forge_interface.HookCommit):
            if kwargs.get("project") == "fedeproxy":
                return self.modified(**kwargs)
        elif len(kwargs) > 0:
            return self.project_export(kwargs["namespace"], kwargs["project"])
        return None

    def inbox(self, username, activity):
        identity = self.identities.lookup(lambda i: self.own.users.convert_url_to_username(i.url) == username)
        assert identity is not None, f"No identity found for {username}"
        self.forge.authenticate(token=identity.token)
        if activity.type == "Commit":
            self.inbox_commit(username, activity)

    def inbox_commit(self, username, commit):
        directory = f"{self.base_directory}/{username}/fedeproxy"
        d = self.forge.projects.create(username, "fedeproxy").dvcs(directory)
        branch = d.url_hashed(commit.context)
        d.clone(branch)
        d.fetch(commit.context, commit.hash)
        d.reset(branch, commit.hash)
        d.push(branch)


@dataclasses.dataclass
class FedeproxyFederation(object):
    base_directory: str
    urls: List[str] = dataclasses.field(default_factory=list)

    @property
    def filename(self):
        return f"{self.base_directory}/federation.json"

    def load(self):
        if os.path.exists(self.filename):
            self.urls = format.FormatFederation().load(self.filename)
            return True
        else:
            return False

    def save(self):
        return format.FormatFederation().save(self.filename, self.urls)

    def create_from_json(self, j):
        self.urls = j

    def to_json(self):
        return self.urls
