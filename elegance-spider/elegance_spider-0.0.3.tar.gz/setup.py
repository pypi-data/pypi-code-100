from os.path import dirname, join

from setuptools import (
    find_packages,
    setup,
)


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


with open(join(dirname(__file__), 'VERSION.txt'), 'rb') as f:
    version = f.read().decode('ascii').strip()

setup(
    name='elegance_spider',
    version=version,
    description='A spider framework',
    packages=find_packages(exclude=[]),
    author='kirintang',
    author_email='215936564@qq.com',
    license='MIT',
    package_data={'': ['*.*']},
    url='https://kirintang.github.io',
    install_requires=parse_requirements("requirements.txt"),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
