from django.urls import reverse
from rest_framework.test import APIClient

from ..domain.fedeproxy import Fedeproxy


def test_hook(tmpdir, mocker, settings, make_identity, make_project, password, forge_factory):
    settings.FEDEPROXY_FORGE_FACTORY = forge_factory["class"]
    settings.FEDEPROXY_FORGE_URL = forge_factory["url"]
    settings.FEDEPROXY_FORGE_DIRECTORY = str(tmpdir)
    f = Fedeproxy(
        forge_factory=settings.FEDEPROXY_FORGE_FACTORY,
        url=settings.FEDEPROXY_FORGE_URL,
        base_directory=settings.FEDEPROXY_FORGE_DIRECTORY,
    )

    make_identity(f, f.owner)
    f.save()

    f.forge.authenticate(username=f.owner, password=password)
    project = "testproject"
    p = make_project(f.forge, f.owner, project)
    title = "ONE TITLE"
    i = p.issues.create(title)

    hook_receive = mocker.patch("fedeproxy.domain.fedeproxy.Fedeproxy.hook_receive")

    client = APIClient()
    payload = forge_factory["hooks"]["issue_create"](f.owner, project, i.id, title)

    url = reverse("hook_project", args=[f.namespace, "fedeproxy"])
    response = client.post(url, data=payload, format="json")
    assert response.status_code == 200, response.content
    hook_receive.assert_called_once_with(payload, namespace=f.namespace, project="fedeproxy")
    hook_receive.reset_mock()

    url = reverse("hook_system")
    response = client.post(url, data=payload, format="json")
    assert response.status_code == 200, response.content
    hook_receive.assert_called_once_with(payload)
    hook_receive.reset_mock()
