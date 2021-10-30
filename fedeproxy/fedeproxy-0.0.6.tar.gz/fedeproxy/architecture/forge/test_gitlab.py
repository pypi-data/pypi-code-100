import os

from .gitlab import GitLab


def payload_issue_create(name, namespace, id, title):
    return {
        "iid": id,
        "object_kind": "issue",
        "project": {
            "name": name,
            "namespace": namespace,
        },
        "object_attributes": {
            "title": title,
        },
    }


def payload_push(name, namespace, hash):
    return {
        "object_kind": "push",
        "project": {
            "name": name,
            "namespace": namespace,
        },
        "checkout_sha": hash,
    }


params = {
    "name": "GitLab",
    "class": GitLab,
    "url": f"http://{os.environ.get('MY_IP', '0.0.0.0')}:8181",
    "hooks": {
        "issue_create": payload_issue_create,
        "push": payload_push,
    },
}
