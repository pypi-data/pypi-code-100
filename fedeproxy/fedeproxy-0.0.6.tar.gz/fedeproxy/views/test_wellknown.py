from django.urls import reverse
from rest_framework.test import APIClient


def test_nodeinfo(tmpdir, settings, forge_factory):
    settings.FEDEPROXY_FORGE_FACTORY = forge_factory["class"]
    settings.FEDEPROXY_FORGE_URL = forge_factory["url"]
    settings.FEDEPROXY_FORGE_DIRECTORY = str(tmpdir)

    client = APIClient()
    url = reverse("wellknown-nodeinfo")
    response = client.get(url)
    assert response.status_code == 200
    url = response.json()["links"][0]["href"]
    assert url.endswith("/nodeinfo/2.0")

    response = client.get(url)
    assert response.status_code == 200
    payload = response.json()
    assert payload["software"]["name"] == "fedeproxy"
