import os

import pytest

from . import factory


@pytest.fixture
def dvcs(dvcs_factory, tmpdir):
    (DVCS, repository) = dvcs_factory
    directory = f"{tmpdir}/testrepository"
    origin = f"{tmpdir}/origin"
    repository(origin).prepare_for_test()
    return DVCS(dir=directory, url=origin)


def test_dvcs_properties(dvcs):
    assert dvcs.directory
    assert dvcs.url
    assert dvcs.clone("master") is True
    assert dvcs.hash


def test_dvcs_clone_master(dvcs):
    assert dvcs.clone("master") is True
    assert os.path.exists(f"{dvcs.directory}/README.md")
    assert dvcs.clone("master") is False


def test_dvcs_clone_not_master(dvcs):
    assert dvcs.clone("other") is True
    assert not os.path.exists(f"{dvcs.directory}/README.md")
    assert dvcs.clone("other") is False


def test_dvcs_commit(dvcs, tmpdir):
    assert dvcs.clone("master") is True
    content = "C"
    open(f"{dvcs.directory}/README.md", "w").write(content)
    dvcs.commit("message")
    dvcs.push("master")

    DVCS = type(dvcs)
    other_dvcs = DVCS(dir=f"{tmpdir}/other", url=dvcs.url)
    assert other_dvcs.clone("master") is True
    assert open(f"{other_dvcs.directory}/README.md").read() == content


def test_dvcs_log(dvcs, tmpdir):
    assert dvcs.clone("master") is True
    hash1 = dvcs.hash
    content = "C"
    open(f"{dvcs.directory}/README.md", "w").write(content)
    dvcs.commit("message")
    dvcs.push("master")
    hash0 = dvcs.hash
    log = dvcs.log()
    assert log[0] == hash0
    assert log[1] == hash1


def test_dvcs_push_pull(dvcs, tmpdir):
    assert dvcs.clone("master") is True

    DVCS = type(dvcs)
    other_dvcs = DVCS(dir=f"{tmpdir}/other", url=dvcs.url)
    assert other_dvcs.clone("master") is True
    content = "C"
    open(f"{other_dvcs.directory}/README.md", "w").write(content)
    other_dvcs.commit("message")
    other_dvcs.push("master")

    dvcs.pull("master")
    assert open(f"{dvcs.directory}/README.md").read() == content


def test_dvcs_factory(dvcs):
    DVCS = type(dvcs)
    assert dvcs.clone("master") is True
    other_dvcs = factory(dvcs.directory)
    assert type(other_dvcs) == DVCS
    assert other_dvcs.url == dvcs.url


def test_dvcs_fetch_reset(dvcs_factory, dvcs, tmpdir):
    (DVCS, repository) = dvcs_factory
    other_origin = f"{tmpdir}/other_origin"
    repository(other_origin).prepare_for_test()
    other_dvcs = DVCS(dir=f"{tmpdir}/other", url=other_origin)
    assert other_dvcs.clone("master") is True
    other_hash = other_dvcs.hash

    assert dvcs.clone("master") is True
    hash = dvcs.hash
    assert dvcs.fetch(other_origin, other_hash) is True
    assert dvcs.hash == hash
    assert dvcs.fetch(other_origin, other_hash) is False
    assert dvcs.hash == hash
    assert dvcs.reset("master", other_hash) is True
    assert dvcs.hash == other_hash
