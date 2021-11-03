from argparse import ArgumentParser
from typing import Optional, Sequence

import hooks_vb.build_utils as bu
import hooks_vb.git_utils as git

DEFAULT_MASTER_BRANCH = 'master'
DEFAULT_REMOTE = 'origin'
DEFAULT_VERSION_FILE = '__init__.py'
DEFAULT_VERSION_VAR = '__version__'


def _get_arg_parser() -> ArgumentParser:  # pragma: no cover
    parser = ArgumentParser(
        description='A version git tagging hook for pre-commit library.')
    parser.add_argument('package', help='package dir')
    parser.add_argument(
        '--skip-tag', dest='skip_tag', action='store_true', default=False,
        help='disable git tagging'
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
        '--remote', dest='remote', default=DEFAULT_REMOTE,
        help=f'remote name (default={DEFAULT_REMOTE})'
    )
    parser.add_argument(
        '--branch', dest='branch', default=DEFAULT_MASTER_BRANCH,
        help=f'branch where tags are allowed (default={DEFAULT_MASTER_BRANCH})'
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:  # pragma: no cover
    """Run the script."""
    args = _get_arg_parser().parse_args(argv)
    version = bu.get_package_version(
        package_dir=args.package, version_file_name=args.version_file,
        version_var_name=args.version_var
    )
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


if __name__ == '__main__':  # pragma: no cover
    exit(main())
