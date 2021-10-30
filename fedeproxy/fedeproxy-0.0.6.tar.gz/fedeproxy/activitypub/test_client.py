import responses

from ..domain.identity import IdentityPrivate
from .client import Post


@responses.activate
def test_client_post():
    i = IdentityPrivate(url="URL")
    i.create_key()
    username = "USERNAME"
    key_url = "http://key_url"
    c = Post(key_username=username, key_private=i.private, key_url=key_url)
    post_url = "http://post-url"
    responses.add(responses.POST, post_url, status=200)
    c.post(post_url, json={"some": "thing"})
    assert len(responses.calls) == 1
    h = responses.calls[0].request.headers
    assert h["Digest"] == "SHA-256=N+EBWhdyAhXa7cUDmXbnyKubV1yTuTuwaiHOrniOrVo="
    assert "signature=" in h["Signature"]
    assert key_url in h["Signature"]
    assert "Date" in h
