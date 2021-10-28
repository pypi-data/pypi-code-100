import re
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Optional

_remote_tag_regex = re.compile(r'.*\srefs/tags/(.+)')
_commit_msg_path = Path('.git/COMMIT_EDITMSG')


def get_current_branch() -> str:
    with Popen(['git', 'symbolic-ref', '--short', 'HEAD'], stdout=PIPE) as p:
        branch = p.communicate()[0]
    return branch.decode('utf-8').strip()


def tag_exists(tag: str, remote: Optional[str] = None) -> bool:
    if tag in ls_tags_local():
        return True
    if remote and tag in ls_tags_remote(remote):
        return True
    return False


def ls_tags_local() -> frozenset:
    with Popen(['git', 'tag', '-l'], stdout=PIPE) as p:
        result = p.communicate()[0]
        if not result:
            return frozenset()
    tags = frozenset(
        tag for tag in
        result.decode('utf-8').split('\n')
        if tag
    )
    return tags


def _extract_remote_tag(data: str) -> Optional[str]:
    tag = next(_remote_tag_regex.finditer(data), None)
    if tag:
        return tag.group(1)


def ls_tags_remote(remote: str) -> frozenset:
    with Popen(['git', 'ls-remote', '--tags', remote]) as p:
        result = p.communicate()[0]
        if not result:
            return frozenset()
    tags = frozenset(
        _extract_remote_tag(row)
        for row in result.decode('utf-8').split('\n')
    )
    return tags


def add_tag(tag: str) -> None:
    with Popen(['git', 'tag', tag]):
        pass


def remove_tag(tag: str) -> None:
    with Popen(['git', 'tag', '-d', tag]):
        pass


def get_commit_msg() -> str:
    if not _commit_msg_path.exists():
        return ''
    with open(_commit_msg_path) as f:
        msg = f.read()
    return msg


def write_commit_msg(msg: str) -> None:
    with open(_commit_msg_path, 'w') as f:
        f.write(msg)
