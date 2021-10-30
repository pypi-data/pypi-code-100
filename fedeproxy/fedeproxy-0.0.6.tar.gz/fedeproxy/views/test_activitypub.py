from django.urls import reverse
from rest_framework.test import APIClient

from ..domain.activitypub import ActivityPub
from ..domain.fedeproxy import Fedeproxy


def test_user(tmpdir, settings, make_identity, make_project, password, forge_factory):
    settings.FEDEPROXY_FORGE_FACTORY = forge_factory["class"]
    settings.FEDEPROXY_FORGE_URL = forge_factory["url"]
    settings.FEDEPROXY_FORGE_DIRECTORY = str(tmpdir)
    f = Fedeproxy(
        forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
        url=settings.FEDEPROXY_FORGE_URL,
        base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
    )

    make_identity(f, f.owner)
    f.own.authenticate(username=f.owner, password=password)
    f.save()

    username = f.owner
    url = reverse("user", args=[username])
    client = APIClient()
    response = client.get(url)
    assert response.status_code == 200
    user = response.json()
    owner = user["publicKey"]["owner"]
    assert owner.endswith(username)
    assert user["publicKey"]["publicKeyPem"].startswith("-----BEGIN PUBLIC KEY-----")


def test_commit(mocker, tmpdir, settings, make_identity, make_project, password, forge_factory):
    mocker.patch("fedeproxy.views.activitypub.verified_signature_active", return_value=False)
    settings.FEDEPROXY_FORGE_FACTORY = forge_factory["class"]
    settings.FEDEPROXY_FORGE_URL = forge_factory["url"]
    settings.FEDEPROXY_FORGE_DIRECTORY = str(tmpdir)
    f = Fedeproxy(
        forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
        url=settings.FEDEPROXY_FORGE_URL,
        base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
    )

    make_identity(f, f.owner)
    username1 = "testuser1"
    make_identity(f, username1)
    make_project(f.forge, username1, "fedeproxy")
    username2 = "testuser2"
    make_identity(f, username2)
    make_project(f.forge, username2, "fedeproxy")
    f.own.authenticate(username=f.owner, password=password)
    f.save()

    client = APIClient()
    #
    # Get username1 last activity as a Commit
    #
    f.forge.authenticate(username=username1, password=password)
    directory1 = f"{f.base_directory}/{username1}/fedeproxy"
    dvcs1 = f.forge.projects.create(username1, "fedeproxy").dvcs(directory1)
    assert dvcs1.clone("otherbranch") is True
    activity = ActivityPub().commit_get(dvcs1.directory)
    #
    # Let username2 know about username1 last activity
    #
    f.forge.authenticate(username=username2, password=password)
    directory2 = f"{f.base_directory}/{username2}/fedeproxy"
    dvcs2 = f.forge.projects.create(username2, "fedeproxy").dvcs(directory2)
    assert dvcs2.clone("otherbranch") is True
    url = reverse("inbox", args=[username2])
    response = client.post(url, data=activity.to_dict(), format="json")
    assert response.status_code == 200
    dvcs2.clone(dvcs2.url_hashed(activity.context))
    assert dvcs1.hash == dvcs2.hash
