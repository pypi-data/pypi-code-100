import os
from pathlib import Path

import pytest

from .activitypub import ActivityPub
from .fedeproxy import Fedeproxy, FedeproxyFederation


def test_fedeproxy_load(tmpdir, make_identity, make_project, password, forge_factory):
    f = Fedeproxy(forge_factory["class"], forge_factory["url"], tmpdir)

    assert f.load() is None
    make_identity(f, f.owner)
    assert f.load() == f.owner


def test_fedeproxy_export(fedeproxy):
    expected_dir = Path(f"{fedeproxy.base_directory}/{fedeproxy.forge.username}/fedeproxy")
    assert not expected_dir.exists()
    dvcs = fedeproxy.project_export(fedeproxy.forge.username, "testproject")
    assert Path(f"{dvcs.directory}/project.json").exists()
    assert Path(dvcs.directory) == expected_dir


def test_fedeproxy_save(fedeproxy):
    pathname = fedeproxy.save()
    assert os.path.exists(f"{pathname}/users.json")
    assert os.path.exists(f"{fedeproxy.base_directory}/identities.json")


def test_fedeproxy_inbox(fedeproxy, testuser, password, make_identity, make_project, dvcs_factory):
    if not fedeproxy.own.is_dvcs_supported(dvcs_factory[0]):
        pytest.skip(f"{dvcs_factory[0].__name__} is not supported by {fedeproxy.forge_factory.__name__}")
    from fedeproxy.architecture.dvcs.hg import Hg

    if dvcs_factory[0] == Hg:
        pytest.skip("hg not supported just yet")
    (DVCS, repository) = dvcs_factory
    #
    # fedeproxy project of testuser
    #
    fedeproxy.forge.authenticate(username=testuser, password=password)
    make_project(fedeproxy.forge, testuser, "fedeproxy")
    testuser_project = fedeproxy.forge.projects.create(testuser, "fedeproxy")
    directory = f"{fedeproxy.base_directory}/{testuser}/fedeproxy"
    testuser_dvcs = testuser_project.dvcs(directory)
    assert testuser_dvcs.clone("testbranch") is True
    repository(testuser_dvcs.directory).populate().commit()
    testuser_dvcs.push("testbranch")
    #
    # create otheruser
    #
    otheruser = "otheruser"
    make_identity(fedeproxy, otheruser)
    fedeproxy.forge.authenticate(username=otheruser, password=password)
    make_project(fedeproxy.forge, otheruser, "fedeproxy")
    #
    # notify otheruser the latest activity from testuser
    #
    activity = ActivityPub().commit_get(testuser_dvcs.directory)
    fedeproxy.inbox(otheruser, activity)
    #
    # check that otheruser now knows about the activity of testuser
    #
    directory = f"{fedeproxy.base_directory}/{otheruser}/fedeproxy"
    otheruser_dvcs = fedeproxy.forge.projects.create(otheruser, "fedeproxy").dvcs(directory)
    otheruser_dvcs.clone(testuser_dvcs.url_hashed(activity.context))
    assert otheruser_dvcs.hash == testuser_dvcs.hash


@pytest.mark.forges(["GitLab"])
def test_fedeproxy_hook_receive(
    tmpdir, mocker, make_project, testuser, password, testproject, fedeproxy, forge_factory
):

    title = "ONE TITLE"
    p = make_project(fedeproxy.forge, testuser, testproject)
    i = p.issues.create(title)

    payload = forge_factory["hooks"]["issue_create"](testuser, testproject, i.id, title)
    dvcs = fedeproxy.hook_receive(payload, namespace=testuser, project=testproject)
    assert os.path.exists(f"{dvcs.directory}/project.json")

    payload = forge_factory["hooks"]["push"](testuser, testproject, "HASH")
    assert fedeproxy.hook_receive(payload, namespace=testuser, project=testproject) is None

    modified = mocker.patch("fedeproxy.domain.fedeproxy.Fedeproxy.modified")
    payload = forge_factory["hooks"]["push"](testuser, "fedeproxy", "HASH")
    fedeproxy.hook_receive(payload, namespace=testuser, project="fedeproxy")
    modified.assert_called()


#
# FedeproxyFederation
#


def test_FedeproxyFederation(tmpdir):
    f = FedeproxyFederation(str(tmpdir))
    assert f.load() is False
    url = "URL"
    f.urls.append(url)
    f.save()

    g = FedeproxyFederation(str(tmpdir))
    assert g.load() is True
    assert g.urls == [url]
