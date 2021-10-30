import os
from pathlib import Path

import git
import gitdb
import sh

from .dvcs import DVCS


class Git(DVCS):
    def __init__(self, dir, url):
        self._url = url
        self.d = dir
        self.g = sh.git.bake("-C", self.d, _tty_out=False)

    @property
    def directory(self):
        return self.d

    @property
    def url(self):
        return self._url

    def set_url_from_directory(self):
        self._url = git.Repo(self.d).remotes.origin.url

    @property
    def hash(self):
        return git.Repo(self.d).head.commit.hexsha

    def log(self):
        return [e.strip() for e in self.g.log("--pretty=tformat:%H", _iter=True)]

    def fetch(self, url, hash):
        if self._commit_exists(hash):
            return False
        url_hashed = self.url_hashed(url)
        r = git.Repo(self.d)
        if not hasattr(r.remotes, url_hashed):
            r.create_remote(url_hashed, url)
        remote = r.remote(url_hashed)
        remote.fetch(hash)
        return True

    def reset(self, branch, hash):
        self.clone(branch)
        r = git.Repo(self.d)
        r.head.reset(r.commit(hash), index=True, working_tree=True)
        return True

    def clone(self, branch):
        clone = not os.path.exists(self.d)
        if clone:
            sh.git.clone(self.url, self.d)
        try:
            self.g.checkout(branch)
        except sh.ErrorReturnCode_1:
            self._create_branch(branch)
        return clone

    def _branch_exists(self, branch):
        r = git.Repo(self.d)
        try:
            r.commit(f"origin/{branch}")
            return True
        except gitdb.exc.BadName:
            return False

    def _commit_exists(self, commit):
        r = git.Repo(self.d)
        try:
            r.commit(commit)
            return True
        except ValueError:
            return False

    def _create_branch(self, branch):
        if self._branch_exists(branch):
            return False
        self.g.checkout("--orphan", branch)
        gitkeep = f"{self.d}/.gitkeep"
        Path(gitkeep).touch()
        self.g.add(gitkeep)
        self.g.commit("-m", ".gitkeep", gitkeep)
        self.g.push("origin", branch)
        self.g.reset("--hard", branch)
        return True

    def pull(self, branch):
        self.g.checkout(branch)
        self.g.pull()

    def push(self, branch):
        self.g.checkout(branch)
        self.g.push("--force", "origin", branch)

    def commit(self, message):
        self.g.add("--all")
        self.g.commit("-m", message)
