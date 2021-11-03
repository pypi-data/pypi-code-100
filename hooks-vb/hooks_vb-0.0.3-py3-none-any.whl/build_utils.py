import re
from pathlib import Path
from subprocess import Popen, PIPE
from typing import Union

import pep440
from build import ProjectBuilder


def get_package_name(package_dir: Union[str, Path]) -> str:
    path = Path(package_dir)
    name = path.stem
    return name.replace('_', '-')


def get_package_version(
    package_dir: Union[str, Path], version_file_name: str,
    version_var_name: str,
) -> str:
    path = Path(package_dir) / version_file_name
    with open(path) as f:
        data = f.read()
        version = extract_version_value(data, version_var_name)
        if not version:
            raise ValueError('Version string not found.') from None
        if not check_version_format(version):
            raise ValueError('Invalid version format.')
    return version


def extract_version_value(data: str, version_var: str) -> Union[str, None]:
    version_value_regex = fr'{version_var}\s*=\s*["\'](.+)["\']'
    version = next(re.finditer(version_value_regex, data), None)
    if version:
        return version.group(1)


def check_version_format(version: str) -> bool:
    return pep440.is_canonical(version)


def validate_readme_file(file_path: Union[str, Path]):
    p = Popen(['rst-lint', str(file_path)])
    p.wait()
    if p.returncode != 0:
        raise ValueError(f'Invalid readme file: {file_path}')


def build_package(
    project_dir: Union[str, Path], output_dir: Union[str, Path],
    distribution: str = 'sdist'
) -> Path:
    builder = ProjectBuilder(project_dir)
    package_path = builder.build(distribution=distribution, output_directory=output_dir)
    return Path(package_path)


def check_package_version_in_pypi(package_name: str, version: str) -> bool:
    with Popen(['pip', 'index', 'versions', package_name], stdout=PIPE) as p:
        with Popen(['grep', '-i', 'available'], stdin=p.stdout, stdout=PIPE) as available:
            with Popen(['grep', '-i', version], stdin=available.stdout, stdout=PIPE) as grep:
                output = grep.communicate()[0]
    return bool(output)


def upload_package(package_path: Union[str, Path], repository: str = 'pypi') -> None:
    with Popen(['python3', '-m', 'twine', 'upload', '--repository', repository, package_path], stdout=PIPE) as p:
        p.wait()
