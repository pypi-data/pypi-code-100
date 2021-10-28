"""
https://www.python.org/dev/peps/pep-0440
https://pre-commit.com
https://github.com/pre-commit/pre-commit-hooks
"""

import re
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Sequence

import hooks_vb.git_utils as git

DEFAULT_MASTER_BRANCH = 'master'
DEFAULT_REMOTE = 'origin'
DEFAULT_VERSION_FILE = '__init__.py'
DEFAULT_VERSION_VAR = '__version__'

# version tag example: `1.0rc2`
DEFAULT_VERSION_FMT = r'[0-9]+(\.[0-9]+)?((\.[0-9]+)|(rc[0-9]+))?'


def _get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description='A version git tagging hook for pre-commit library.')
    parser.add_argument('package', help='package name')
    parser.add_argument(
        '--skip-tag', dest='skip_tag', action='store_true', default=False,
        help='disable git tagging'
    )
    parser.add_argument(
        '--skip-validation', dest='skip_validation', action='store_true', default=False,
        help='disable version string validation'
    )
    parser.add_argument(
        '--version-file', dest='version_file', default=DEFAULT_VERSION_FILE,
        help=f'file with a version string (default={DEFAULT_VERSION_FILE})'
    )
    parser.add_argument(
        '--version-var', dest='version_var', default=DEFAULT_VERSION_VAR,
        help=f'version variable (default={DEFAULT_VERSION_VAR})'
    )
    parser.add_argument(
        '--version-fmt', dest='version_fmt', default=DEFAULT_VERSION_FMT,
        help=f'version format (default={DEFAULT_VERSION_FMT})'
    )
    parser.add_argument(
        '--remote', dest='remote', default=DEFAULT_REMOTE,
        help=f'remote name (default={DEFAULT_REMOTE})'
    )
    parser.add_argument(
        '--branch', dest='branch', default=DEFAULT_MASTER_BRANCH,
        help=f'branch where tags are allowed (default={DEFAULT_MASTER_BRANCH})'
    )
    return parser


def _get_version(args) -> str:
    path = Path(args.package) / args.version_file
    with open(path) as f:
        data = f.read()
        version = _extract_version(data, args.version_var)
        if not version:
            raise ValueError(f'Version string not found in file: {args.version_file}.') from None
        if args.skip_validation:
            return version
        if not _validate_version(version, args.version_fmt):
            raise ValueError(f'Invalid version string format: {version}.') from None
        return version


def _extract_version(data: str, version_var: str) -> Optional[str]:
    version_value_regex = fr'{version_var}\s*=\s*["\'](.+)["\']'
    version = next(re.finditer(version_value_regex, data), None)
    if version:
        return version.group(1)


def _validate_version(version: str, version_fmt: str) -> bool:
    return bool(re.fullmatch(version_fmt, version))


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run the script."""
    args = _get_arg_parser().parse_args(argv)
    version = _get_version(args)
    if args.branch and git.get_current_branch() != args.branch:
        print('Version tags are not allowed on this branch. Skipping.')
        return 0
    if args.skip_tag:
        print('Version tags are skipped because --skip-tag is set.')
        return 0
    if git.tag_exists(version, args.remote):
        print('Version tag already exists.')
        return 0
    git.add_tag(version)
    print(f'Tagged new version {version}.')
    return 0


if __name__ == '__main__':
    exit(main())
