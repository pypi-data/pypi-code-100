import os
import tempfile
from unittest.mock import patch

import requests
from django.conf import settings
from django.test import override_settings
from rest_framework.test import APILiveServerTestCase

from ..activitypub import Follow
from ..activitypub.client import Post
from ..architecture.forge.gitea import Gitea
from ..domain.fedeproxy import Fedeproxy


class ActivityPubTests(APILiveServerTestCase):
    project = "fedeproxy"
    password = "Wrobyak4"

    def setUp(self):
        self.f = Fedeproxy(
            forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
            url=settings.FEDEPROXY_FORGE_URL,
            base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
        )

        self.username = self.f.owner
        self.cleanup()
        email = f"{self.username}@example.com"
        user = self.f.own.users.create(self.username, self.password, email)
        self.i = self.f.identity_create(user, self.password)
        self.f.forge.authenticate(username=self.username, password=self.password)
        self.f.forge.projects.create(self.username, self.project)
        self.f.save()

    def tearDown(self):
        self.cleanup()

    def cleanup(self):
        self.f.own.authenticate(username="root", password="Wrobyak4")
        self.f.own.projects.delete(self.username, self.project)
        self.f.own.users.delete(self.username)


tmpdir_user = tempfile.TemporaryDirectory()


@override_settings(
    FEDEPROXY_FORGE_FACTORY=Gitea,
    FEDEPROXY_FORGE_URL=f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781",
    FEDEPROXY_FORGE_DIRECTORY=tmpdir_user.name,
    DEBUG=True,
)
class UserTests(ActivityPubTests):
    def test_user(self):
        id = f"{self.live_server_url}/user/{self.username}"
        response = requests.get(id)
        response.raise_for_status()
        assert response.json()["type"] == "Person"
        assert response.json()["id"] == id


tmpdir_inbox = tempfile.TemporaryDirectory()


@override_settings(
    FEDEPROXY_FORGE_FACTORY=Gitea,
    FEDEPROXY_FORGE_URL=f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781",
    FEDEPROXY_FORGE_DIRECTORY=tmpdir_inbox.name,
    DEBUG=True,
)
@patch("fedeproxy.domain.fedeproxy.Fedeproxy.inbox")
class InboxTests(ActivityPubTests):
    def test_inbox(self, inbox):
        f = Follow(
            id="https://test.com/user/follow/id",
            actor="follower_id",
            object="followee_id",
        )
        url = f"{self.live_server_url}/user/{self.username}/inbox"

        response = requests.post(url, json=f.to_dict())
        assert "No Signature header found" in response.text
        assert response.status_code == 400

        client = Post(key_username=self.username, key_private=self.i.private, key_url=self.live_server_url)
        response = client.post(url, json=f.to_dict())
        assert response.status_code == 200
