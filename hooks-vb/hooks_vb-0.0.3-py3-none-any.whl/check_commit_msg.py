import re
from argparse import ArgumentParser
from typing import Optional, Sequence, Collection

import hooks_vb.git_utils as git

DEFAULT_CATEGORIES = (
    'fix',                      # bugfix
    'feat', 'feature',          # feature
    'wip',                      # work-in-progress changes (not ready to use)
    'maint', 'maintenance',     # code maintenance (dependences, configs)
    'backport',                 # backport to an older branch
    'test', 'tests',            # tests related
    'doc', 'docs',              # documentation related
    'style'                     # code style and minor refactoring
)
# header example:  `fix(db) #101: fixed database connection drops`
DEFAULT_MSG_TEMPLATE = r'^({categories})(\(.{{1,15}}\))?(\s#[0-9]+)?:\s(.{{5,50}})\n*(\n(\n.{{0,120}})*)?$'


def _get_arg_parser() -> ArgumentParser:  # pragma: no cover
    parser = ArgumentParser(
        description='A version git tagging hook for pre-commit library.')
    parser.add_argument(
        '--categories', dest='msg_categories', default=DEFAULT_CATEGORIES,
        help=f'file with a version string (default={",".join(DEFAULT_CATEGORIES)})'
    )
    parser.add_argument(
        '--msg-fmt', dest='msg_fmt', nargs='+', default=DEFAULT_MSG_TEMPLATE,
        help=f'file with a version string (default={DEFAULT_MSG_TEMPLATE})'
    )
    return parser


def _check_message_fmt(template: str, categories: Collection[str], msg: str) -> bool:
    categories = '|'.join(categories)
    pattern = template.format(categories=categories)
    return bool(re.match(pattern, msg))


def _remove_trailing_stuff(msg: str) -> str:
    header, *body = msg.strip().split('\n', maxsplit=1)
    header = header.strip().strip('.')
    if body:
        body = body[0]
        body = body.strip().capitalize()
        return '\n'.join((header, body))
    else:
        return header


def main(argv: Optional[Sequence[str]] = None) -> int:  # pragma: no cover
    """Run the script."""
    args = _get_arg_parser().parse_args(argv)
    msg = git.get_commit_msg()
    msg = _remove_trailing_stuff(msg)
    if not msg:
        print('ERROR: No commit message provided.')
        return 1
    if not _check_message_fmt(args.msg_fmt, args.msg_categories, msg):
        print('ERROR: Invalid message format.')
        return 1
    git.write_commit_msg(msg)
    return 0


if __name__ == '__main__':  # pragma: no cover
    exit(main())
