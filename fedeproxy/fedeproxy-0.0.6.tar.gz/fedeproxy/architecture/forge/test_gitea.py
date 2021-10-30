import os

from .gitea import Gitea


def payload_issue_create(name, namespace, id, title):
    return {}


def payload_push(name, namespace, id, hash):
    return {}


params = {
    "name": "Gitea",
    "class": Gitea,
    "url": f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781",
    "hooks": {
        "issue_create": payload_issue_create,
        "push": payload_push,
    },
}


def test_gitea_fork():
    (Forge, url) = (Gitea, f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8781")
    forge = Forge(url)
    forge.authenticate(username="root", password="Wrobyak4")
    password = "Wrobyak4"

    username1 = "testuser1"
    email1 = "testuser1@example.com"
    forge.users.create(username1, password, email1)
    forge.projects.delete(username1, "testproject")

    username2 = "testuser2"
    email2 = "testuser2@example.com"
    forge.users.create(username2, password, email2)
    forge.projects.delete(username2, "testproject")

    forge.authenticate(username=username1, password=password)
    p1 = forge.projects.create(username1, "testproject")

    forge.authenticate(username=username2, password=password)
    p2 = forge.project_fork(username1, "testproject")
    assert p1.id != p2.id
    assert p2.project == "testproject"
    assert p1.project == p2.project

    p3 = forge.project_fork(username1, "testproject")
    assert p2.id == p3.id
    assert p2 == p3

    forge.authenticate(username="root", password="Wrobyak4")
    assert forge.projects.delete(username2, "testproject") is True
    assert forge.users.delete(username2) is True
    assert forge.projects.delete(username1, "testproject") is True
    assert forge.users.delete(username1) is True
