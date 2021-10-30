import logging
import os
import tempfile
from unittest.mock import patch

import gitlab
import sh
from django.conf import settings
from django.test import override_settings
from rest_framework.test import APILiveServerTestCase

from fedeproxy.common.retry import retry
from tests.gitlab_helpers import GitLabHelpers

from ..architecture.forge.gitlab import GitLab
from ..architecture.forge.test_gitlab import payload_issue_create, payload_push
from ..domain.fedeproxy import Fedeproxy

logger = logging.getLogger(__name__)


def get_host_to_connect():
    if "MY_IP" not in os.environ:
        # outside of the CI the live test server is bound to the gateway and gitlab
        # must connect to the gateway
        return sh.docker.inspect(
            "-f", "{{range .NetworkSettings.Networks}}{{.Gateway}}{{end}}", "test-gitlab1"
        ).strip()
    else:
        # in the CI MY_IP is set and gitlab is allowed to connect to the container
        # running the tests
        return sh.hostname("-I").strip()


class HookTestsBase(APILiveServerTestCase):
    project = "fedeproxy"
    password = "Wrobyak4"
    # override the default from django/test/testcases.py
    host = "0.0.0.0"

    def setUp(self):
        self.f = Fedeproxy(
            forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
            url=settings.FEDEPROXY_FORGE_URL,
            base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
        )

        self.username = self.f.owner
        self.cleanup()
        GitLabHelpers(self.f.own.s).hooks_relax_restrictions()
        email = f"{self.username}@example.com"
        user = self.f.own.users.create(self.username, self.password, email)
        self.i = self.f.identity_create(user, self.password)
        self.f.forge.authenticate(username=self.username, password=self.password)
        self.f.forge.projects.create(self.username, self.project)
        self.f.save()

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        forge = self.f.own
        forge.authenticate(username="root", password="Wrobyak4")
        forge.projects.delete(self.username, self.project)
        forge.users.delete(self.username)

    def install_hook(self):
        forge = self.f.own
        forge.authenticate(username="root", password="Wrobyak4")
        url = f"http://{get_host_to_connect()}:{self.server_thread.port}"
        logger.error(f"test_hook: registering {url}")

        #
        # the retry is necessary because hooks_relax_restrictions is asynchronous
        # and may not yet be finalized
        #
        @retry(gitlab.exceptions.GitlabCreateError, tries=5)
        def wait_for_register():
            assert forge.hook_register(url) == [True]

        wait_for_register()


#
# Debugging tips if the following fails.
#
# There is no API that would display the reason why a webhook fails
# https://docs.gitlab.com/ce/api/projects.html#get-project-hook
# Go to http://0.0.0.0:8181/fedeproxy/fedeproxy/-/hooks
# manually run the test and see the error message
#
@retry(AssertionError, tries=7)
def wait_for_hook(hook, predicate):
    for call_args in hook.call_args_list:
        payload = call_args.args[0]
        if predicate(payload):
            return payload
    assert 0, hook.call_args_list


tmpdir_issue = tempfile.TemporaryDirectory()


@override_settings(
    FEDEPROXY_FORGE_FACTORY=GitLab,
    FEDEPROXY_FORGE_URL=f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8181",
    FEDEPROXY_FORGE_DIRECTORY=tmpdir_issue.name,
    DEBUG=True,
)
@patch("fedeproxy.domain.fedeproxy.Fedeproxy.hook_receive")
class HookIssueCreateTests(HookTestsBase):
    def test_hook(self, hook_receive):
        self.install_hook()
        assert hook_receive.called is False

        self.f.forge.authenticate(username=self.username, password=self.password)
        p = self.f.forge.projects.create(self.username, self.project)
        title = "ISSUE ONE"
        i = p.issues.create(title)

        payload = wait_for_hook(hook_receive, lambda h: h["object_kind"] == "issue")
        actual = {
            "iid": payload["object_attributes"]["iid"],
            "object_kind": payload["object_kind"],
            "project": {
                "name": payload["project"]["name"],
                "namespace": payload["project"]["namespace"],
            },
            "object_attributes": {
                "title": payload["object_attributes"]["title"],
            },
        }
        assert actual == payload_issue_create(self.username, self.project, i.id, title)


tmpdir_push = tempfile.TemporaryDirectory()


@override_settings(
    FEDEPROXY_FORGE_FACTORY=GitLab,
    FEDEPROXY_FORGE_URL=f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8181",
    FEDEPROXY_FORGE_DIRECTORY=tmpdir_push.name,
    DEBUG=True,
)
@patch("fedeproxy.domain.fedeproxy.Fedeproxy.hook_receive")
class HookCommitTests(HookTestsBase):
    def test_hook(self, hook_receive):
        self.install_hook()
        assert hook_receive.called is False

        self.f.forge.authenticate(username=self.username, password=self.password)
        p = self.f.forge.projects.create(self.username, self.project)
        directory = f"{self.f.base_directory}/{self.project}"
        d = p.dvcs(directory)
        d.clone("master")
        filename = f"{directory}/README"
        open(filename, "w").write("SOME")
        d.commit("add README")
        d.push("master")

        def predicate(payload):
            return payload["object_kind"] == "push" and payload["checkout_sha"] == d.hash

        payload = wait_for_hook(hook_receive, predicate)
        actual = {
            "object_kind": "push",
            "project": {
                "name": payload["project"]["name"],
                "namespace": payload["project"]["namespace"],
            },
            "checkout_sha": d.hash,
        }
        assert actual == payload_push(self.username, self.project, d.hash)
