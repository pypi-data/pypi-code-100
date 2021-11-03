from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, Sequence

import hooks_vb.build_utils as bu

DEFAULT_PACKAGE_OUTPUT = 'dist'
DEFAULT_PYPI_REPOSITORY = 'pypi'
DIST_TYPES = ['sdist', 'wheel']
DEFAULT_VERSION_FILE = '__init__.py'
DEFAULT_VERSION_VAR = '__version__'
README_FILES = ['README.rst', 'AUTHORS.rst', 'CHANGELOG.rst']


def _get_arg_parser() -> ArgumentParser:  # pragma: no cover
    parser = ArgumentParser(
        description='Build and a package in pypi.')
    parser.add_argument('package', help='package dir')
    parser.add_argument(
        '--package-name', dest='package_name', default=None,
        help='customize package name'
    )
    parser.add_argument(
        '--dist-type', dest='dist_type', default=DIST_TYPES[0], choices=DIST_TYPES,
        help=f'package type (default={DIST_TYPES[0]})'
    )
    parser.add_argument(
        '--output', dest='output', default=None,
        help=f'build output directory (default=./{DEFAULT_PACKAGE_OUTPUT})'
    )
    parser.add_argument(
        '--repository', dest='repository', default=DEFAULT_PYPI_REPOSITORY,
        help=f'repository for upload (default={DEFAULT_PYPI_REPOSITORY})'
    )
    parser.add_argument(
        '--version-file', dest='version_file', default=DEFAULT_VERSION_FILE,
        help=f'file with a version string (default={DEFAULT_VERSION_FILE})'
    )
    parser.add_argument(
        '--version-var', dest='version_var', default=DEFAULT_VERSION_VAR,
        help=f'version variable (default={DEFAULT_VERSION_VAR})'
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:  # pragma: no cover
    """Run the script."""
    args = _get_arg_parser().parse_args(argv)
    if args.package_name is None:
        package_name = bu.get_package_name(args.package)
    else:
        package_name = args.package_name
    version = bu.get_package_version(
        package_dir=args.package, version_file_name=args.version_file,
        version_var_name=args.version_var)

    build_dir = Path(args.package).parent

    for filename in README_FILES:
        p = build_dir / filename
        if p.exists():
            bu.validate_readme_file(p)

    if bu.check_package_version_in_pypi(package_name, version):
        print(f'Package {package_name}=={version} is already present in pypi repository.')
        return 0

    if args.output is None:
        output = build_dir / DEFAULT_PACKAGE_OUTPUT
    else:
        output = args.output

    p = bu.build_package(build_dir, output_dir=output, distribution=args.dist_type)
    print(f'Built a new package: {p}')
    bu.upload_package(p, repository=args.repository)
    print(f'Published a new package: {package_name}=={version}.')
    return 0


if __name__ == '__main__':  # pragma: no cover
    exit(main())
