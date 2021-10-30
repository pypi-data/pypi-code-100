import os
import textwrap
import urllib.parse

import sh

from .dvcs import DVCS


class Hg(DVCS):
    def __init__(self, dir, url):
        self._url = url
        self.d = dir
        self.h = sh.hg.bake("--cwd", self.d, _tty_out=False)

    @property
    def directory(self):
        return self.d

    @property
    def url(self):
        return self._url

    def set_url_from_directory(self):
        self._url = self.h.paths.default().strip()

    @property
    def hash(self):
        return self.h.identify("-i", "--template", "{id}").strip()

    def log(self):
        return [e.strip() for e in self.h.log("--template", "{node}\n", _iter=True)]

    def fetch(self, url, hash):
        try:
            self.h.identify("-r", hash)
            return False
        except sh.ErrorReturnCode_255 as e:
            if "unknown revision" not in e.args[0]:
                raise
        self.h.pull("-f", url)
        self.h.identify("-r", hash)
        return True

    def reset(self, branch, hash):
        self.clone(branch)
        self.h.update("--clean", "-r", hash)
        return True

    def clone(self, branch):
        clone = not os.path.exists(self.d)
        if clone:
            sh.hg.clone(self.url, self.d)
            components = urllib.parse.urlsplit(self.url)
            auth = textwrap.dedent(
                f"""
                [auth]
                test.prefix = {components.hostname}{":%s" % components.port if components.port else ""}
                test.username = {components.username}
                test.password = {components.password}
                test.schemes = {components.scheme}"""
            )
            with open(f"{self.d}/.hg/hgrc", "a") as hgrc:
                hgrc.write(auth)

        try:
            self.h.update(branch)
        except sh.ErrorReturnCode_255:
            self._create_branch(branch)
        return clone

    def pull(self, branch):
        self.h.pull("--branch", branch)
        self.h.update(branch)

    def push(self, branch):
        self.h.push("--branch", branch)

    def commit(self, message):
        self.h.add(".")
        self.h.commit("-m", message)

    def _branch_exists(self, branch):
        try:
            self.h.branches("--rev", branch)
            return True
        except sh.ErrorReturnCode_255:
            return False

    def _create_branch(self, branch):
        if self._branch_exists(branch):
            return False
        self.h.update("--rev", "0")
        self.h.branch(branch)
        self.h.commit("-m" f"create branch {branch}")
        self.h.push("--new-branch", "--branch", branch)
        return True
