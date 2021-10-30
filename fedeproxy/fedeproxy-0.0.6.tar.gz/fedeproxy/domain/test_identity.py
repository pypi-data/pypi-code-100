import pytest

from . import identity


@pytest.fixture
def identity_sample():
    emails = ["one@example.com", "two@example.com"]
    url = "url"
    owned = True
    token = "TOKEN"
    return {
        "emails": emails,
        "url": url,
        "owned": owned,
        "token": token,
        "private": "privatekey",
        "public": "publickey",
    }


def test_identity_private(identity_sample):
    i = identity.IdentityPrivate()
    assert i.asdict() == {
        "emails": [],
        "url": None,
        "owned": False,
        "token": None,
        "private": None,
        "public": None,
    }
    assert i.is_owned() is False
    assert i.is_staged() is True
    i.create_key()
    assert i.private is not None
    assert i.public is not None
    i = identity.IdentityPrivate(**identity_sample)
    assert i.asdict() == identity_sample
    assert i.is_owned() is True
    assert i.is_staged() is False


def test_identity_public(identity_sample):
    i_private = identity.IdentityPrivate(**identity_sample)
    i_public = identity.IdentityPublic()
    i_public.from_private(i_private)
    expected = {
        "emails": [
            "d25354f658256d3988a0a1f07ae2dbfa64c0141b3eaa5650fd268b3fdd903b7d",
            "1f6c1f35fba8e0f461ef40adaec3cbda883f6a5bcfa5fddef2df80af49fc0832",
        ],
        "owned": True,
        "url": "url",
        "public": "publickey",
    }
    assert i_public.asdict() == expected
    assert identity.IdentityPublic(**expected).asdict() == expected


def test_identities(tmpdir, identity_sample):
    identities = identity.IdentitiesPrivate(tmpdir)
    assert identities.load() is False
    assert identities.identities == []
    i = identity.IdentityPrivate(**identity_sample)
    identities.identities.append(i)
    identities.save()

    identities = identity.IdentitiesPrivate(tmpdir)
    assert identities.load() is True
    identity_loaded = identities.identities[0]
    assert identity_loaded.asdict() == identity_sample
